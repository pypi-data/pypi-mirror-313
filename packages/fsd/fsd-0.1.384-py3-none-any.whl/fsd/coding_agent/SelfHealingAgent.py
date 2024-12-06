import os
import sys
import asyncio
import re
import aiohttp
import json
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.system.FileContentManager import FileContentManager
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class SelfHealingAgent:

    def __init__(self, repo):
        self.repo = repo
        self.conversation_history = []
        self.code_manager = FileContentManager(repo)  # Initialize CodeManager in the constructor
        self.ai = AIGateway()

    def get_current_time_formatted(self):
        """Get the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def initial_setup(self, role):
        """
        Initialize the conversation with a system prompt and user context.
        """
        prompt = f"""You are an expert software engineer. Follow these guidelines strictly when responding to instructions:

                **Response Guidelines:**
                1. Use ONLY the following SEARCH/REPLACE block format for ALL code changes, additions, or deletions:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. CRITICAL: The SEARCH section MUST match the existing code with 100% EXACT precision - every character, whitespace, indentation, newline, and comment must be identical. Even a single character difference will cause the match to fail.

                4. For large files, focus on relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. MUST break complex changes or large files into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of SEARCH/REPLACE blocks. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                9. CRITICAL: Never include code markdown formatting, syntax highlighting, or any other decorative elements. Code must be provided in its raw form.

                10. STRICTLY FORBIDDEN: Do not hallucinate, invent, or make assumptions about code. Only provide concrete, verified code changes based on the actual codebase.

                11. MANDATORY: Code must be completely plain without any formatting, annotations, explanations or embellishments. Only pure code is allowed.

                Remember: Your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.

        """

        self.conversation_history.append({"role": "system", "content": prompt})

    def read_all_file_content(self, all_path):
        """
        Read the content of all specified files.

        Args:
            all_path (list): List of file paths.

        Returns:
            str: Concatenated content of all files.
        """
        all_context = ""

        for path in all_path:
            file_context = read_file_content(path)
            all_context += f"\n\nFile: {path}\n{file_context}"

        return all_context

    async def get_fixing_request(self, instruction, file_content, all_file_content, tech_stack):
        """
        Get fixing response for the given instruction and context from Azure OpenAI.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            instruction (str): The fixing instructions.
            file_content (str): The content of the file to be fixed.
            all_file_content (str): The content of all related files.

        Returns:
            dict: Fixing response or error reason.
        """

        prompt = ""

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

        if all_file_content != "":
            prompt = (
                f"Current damaged file:\n{file_content}\n\n"
                f"Related files context:\n{all_file_content}\n\n"
                f"Follow this instructions to fix bugs:\n{instruction}\n\n"
                f"Please strictly follow the exact syntax and formatting for {tech_stack}\n\n"
                "For any mockup or placeholder data you create, label it clearly as mock information so readers can identify it.\n"
                "- MUST follow existing UI style if present, otherwise MUST create nice-looking and elegant design\n" 
                "- Enforce perfect spacing, alignment and visual hierarchy\n"
                "- Ensure fully responsive layout with precise breakpoints\n"
                "- Create smooth, intuitive interactions with clear feedback\n"
                "- Maintain pixel-perfect layouts across all views\n"
                "- Implement visual consistency between UI elements\n"
                "For logic code:\n"
                "- Write clean, efficient code with optimal algorithmic complexity and memory usage\n"
                "- Use descriptive variable/function names following domain-driven design principles\n"
                "- Structure code for maximum reusability and maintainability using SOLID principles\n"
                "- Implement comprehensive error handling with contextual logging\n"
                "- Leverage enterprise design patterns appropriately\n"
                "- Ensure thread-safety through proper synchronization\n"
                "- Add thorough input validation and defensive programming\n"
                "- Use proper dependency injection patterns\n"
                "- Implement null checks and edge cases\n"
                "- Ensure consistent state management and data integrity\n"
                "- Follow project's coding standards\n"
                "- Follow security best practices\n"
                f"{lazy_prompt}\n"
                "Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."
            )
        else:
            prompt = (
                "You are world-class, highly experienced bug fixing agent\n"
                f"Current damaged file:\n{file_content}\n\n"
                f"Follow this instructions to fix bugs:\n{instruction}\n\n"
                f"Please strictly follow the exact syntax and formatting for {tech_stack}\n\n"
                "For any mockup or placeholder data you create, label it clearly as mock information so readers can identify it.\n"
                "- Follow existing UI style if present, otherwise create nice-looking and elegant design\n" 
                "- Enforce perfect spacing, alignment and visual hierarchy\n"
                "- Ensure fully responsive layout with precise breakpoints\n"
                "- Create smooth, intuitive interactions with clear feedback\n"
                "- Maintain pixel-perfect layouts across all views\n"
                "- Implement visual consistency between UI elements\n"
                "For logic code:\n"
                "- Write clean, efficient code with optimal algorithmic complexity and memory usage\n"
                "- Use descriptive variable/function names following domain-driven design principles\n"
                "- Structure code for maximum reusability and maintainability using SOLID principles\n"
                "- Implement comprehensive error handling with contextual logging\n"
                "- Leverage enterprise design patterns appropriately\n"
                "- Ensure thread-safety through proper synchronization\n"
                "- Add thorough input validation and defensive programming\n"
                "- Use proper dependency injection patterns\n"
                "- Implement null checks and edge cases\n"
                "- Ensure consistent state management and data integrity\n"
                "- Follow project's coding standards\n"
                "- Follow security best practices\n"
                f"{lazy_prompt}\n"
                "Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."
            )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
            content = response.choices[0].message.content
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if lines and "> REPLACE" in lines[-1]:
                self.conversation_history.pop()
                return content
            else:
                logger.info(" #### Extending response - generating additional context (1/5)")
                self.conversation_history.append({"role": "assistant", "content": content})
                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                continuation_content = continuation_response.choices[0].message.content
                continuation_lines = [line.strip() for line in continuation_content.splitlines() if line.strip()]

                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                    complete_content = content + continuation_content
                    self.conversation_history = self.conversation_history[:-2]
                    self.conversation_history.pop()
                    return complete_content
                else:
                    logger.info(" #### Extending response - generating additional context (2/5)")
                    content = content + continuation_content
                    self.conversation_history.append({"role": "assistant", "content": content})
                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                    continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                    continuation_content1 = continuation_response.choices[0].message.content
                    continuation_lines = [line.strip() for line in continuation_content1.splitlines() if line.strip()]

                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                        complete_content = content + continuation_content1
                        self.conversation_history = self.conversation_history[:-4]
                        self.conversation_history.pop()
                        return complete_content
                    else:
                        logger.info(" #### Extending response - generating additional context (3/5)")
                        content = content + continuation_content1
                        self.conversation_history.append({"role": "assistant", "content": content})
                        continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                        self.conversation_history.append({"role": "user", "content": continuation_prompt})

                        continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                        continuation_content2 = continuation_response.choices[0].message.content
                        continuation_lines = [line.strip() for line in continuation_content2.splitlines() if line.strip()]

                        if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                            complete_content = content + continuation_content2
                            self.conversation_history = self.conversation_history[:-6]
                            self.conversation_history.pop()
                            return complete_content
                        else:
                            logger.info(" #### Extending response - generating additional context (4/5)")
                            content = content + continuation_content2
                            self.conversation_history.append({"role": "assistant", "content": content})
                            continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                            self.conversation_history.append({"role": "user", "content": continuation_prompt})

                            continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                            continuation_content3 = continuation_response.choices[0].message.content
                            continuation_lines = [line.strip() for line in continuation_content3.splitlines() if line.strip()]

                            if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                complete_content = content + continuation_content3
                                self.conversation_history = self.conversation_history[:-8]
                                self.conversation_history.pop()
                                return complete_content
                            else:
                                logger.info(" #### Extending response - generating additional context (5/5)")
                                content = content + continuation_content3
                                self.conversation_history.append({"role": "assistant", "content": content})
                                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                continuation_content4 = continuation_response.choices[0].message.content
                                complete_content = content + continuation_content4
                                self.conversation_history = self.conversation_history[:-10]
                                self.conversation_history.pop()
                                return complete_content

        except Exception as e:
            logger.error(f"  The `SelfHealingAgent` encountered an error during the fixing request: {e}")
            return {
                "reason": str(e)
            }

    async def get_fixing_requests(self, instructions):
        """
        Get fixing responses for a list of instructions from Azure OpenAI based on user prompt.

        Args:
            instructions (list): List of instructions for fixing bugs.

        Returns:
            dict: Fixing response or error reason.
        """
        for instruction in instructions:
            file_name = instruction['file_name']
            tech_stack = instruction['tech_stack']
            list_related_file_name = instruction['list_related_file_name']
            all_comprehensive_solutions_for_each_bugs = instruction['all_comprehensive_solutions_for_each_bug']
            if file_name in list_related_file_name:
                list_related_file_name.remove(file_name)

            if len(list_related_file_name) == 0:
                main_path = file_name
                file_content = read_file_content(main_path)
                logger.info(f" #### The `Self-Healing Agent` is initiating work on: `{instruction['Solution_detail_title']}`")
                result = await self.get_fixing_request(all_comprehensive_solutions_for_each_bugs, file_content, "", tech_stack)
                await self.replace_all_code_in_file(main_path, result)
                logger.info(f" #### The `Self-Healing Agent` has completed tasks for: `{instruction['Solution_detail_title']}`.")
            else:
                main_path = file_name
                all_path = list_related_file_name
                file_content = read_file_content(main_path)
                all_file_content = self.read_all_file_content(all_path)
                logger.info(f" #### The `Self-Healing Agent` is beginning work on: `{instruction['Solution_detail_title']}`.")
                result = await self.get_fixing_request(all_comprehensive_solutions_for_each_bugs, file_content, all_file_content, tech_stack)
                await self.replace_all_code_in_file(main_path, result)
                logger.info(f" #### The `Self-Healing Agent` has successfully completed tasks for: `{instruction['Solution_detail_title']}`.")

    async def replace_all_code_in_file(self, file_path, result):
        """
        Replace the entire content of a file with the new code snippet.

        Args:
            file_path (str): Path to the file.
            new_code_snippet (str): New code to replace the current content.
        """
        if file_path:
            await self.code_manager.handle_coding_agent_response(file_path, result)
        else:
            logger.debug(f" #### The `SelfHealingAgent` could not locate the file: `{file_path}`")
