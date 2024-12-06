import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ImageFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_dependency_file_content(self, file_path):
        """
        Read the content of a dependency file.

        Args:
            file_path (str): Path to the dependency file to read.

        Returns:
            str: Content of the dependency file, or None if an error occurs.
        """
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            logger.debug(f" #### `ImageFileFinderAgent` encountered an issue while reading dependency file:\n{file_path}\nError: {e}")
            return None


    async def get_style_file_planning(self, tree):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """

        prompt = (
            f"Identify ONLY THE MOST CRITICAL style and configuration files (MAXIMUM 3 FILES) in the project structure.\n\n"
            f"User OS: {platform.system()}\n"
            f"Based on the OS above, ensure all file paths use the correct separators:\n"
            f"Windows example: C:\\Users\\name\\project\\styles\\theme.css\n"
            f"macOS/Linux example: /Users/name/project/styles/theme.css\n\n"
            "CRITICAL REQUIREMENTS:\n"
            "1. RETURN NO MORE THAN 3 FILES TOTAL - only the absolute most essential ones\n"
            "2. Each file path MUST be a complete absolute path starting from the project directory\n"
            "3. ONLY include files that ACTUALLY EXIST in the given project structure\n"
            "4. STRICTLY EXCLUDE:\n"
            "   - ALL lock files (package-lock.json, yarn.lock, Podfile.lock, etc)\n"
            "   - Generated folders (node_modules/, build/, dist/, etc)\n"
            "   - Third-party library code files\n"
            "   - Cache directories\n"
            "   - Any files generated after dependency installation\n"
            "   - Main code files from the user's project\n"
            "5. FOCUS ON:\n"
            "   - Primary style configuration files\n"
            "   - Theme/color definition files\n"
            "   - Core UI styling manifests\n\n"
            "Return ONLY this JSON format:\n"
            "{\n"
            f"    \"style_files\": [\"{self.repo.get_repo_path()}/path/to/file1\"]\n"
            "}\n"
            "Provide only JSON. No additional text. Ensure paths match OS format."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the current project structure:\n{tree}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.debug(f" #### `ImageFileFinderAgent` failed to obtain dependency file planning:\nError: {e}")
            return {
                "reason": str(e)
            }


    async def get_style_file_plannings(self):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """
        logger.debug("\n #### `ImageFileFinderAgent` is initiating the style file planning process")
        all_tree_file_contents = self.repo.print_tree()
        plan = await self.get_style_file_planning(all_tree_file_contents)
        logger.debug("\n #### `ImageFileFinderAgent` has successfully completed the style file planning")
        return plan
