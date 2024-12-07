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

class DependencyFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_dependency_file_planning(self, tree):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """
        logger.debug("\n #### The `DependencyFileFinderAgent` is initiating dependency file planning")

        prompt = (
            f"Identify ONLY THE MOST CRITICAL dependency and configuration files (MAXIMUM 3 FILES) in the project structure.\n\n"
            f"User OS: {platform.system()}\n"
            f"Based on the OS above, ensure all file paths use the correct separators:\n"
            f"Windows example: C:\\Users\\name\\project\\package.json\n"
            f"macOS/Linux example: /Users/name/project/package.json\n\n"
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
            "5. For dependencies, ONLY include primary manifest files like:\n"
            "   - package.json (NOT package-lock.json)\n"
            "   - Podfile (NOT Podfile.lock)\n"
            "   - requirements.txt\n"
            "   - pom.xml\n\n"
            "Return ONLY this JSON format:\n"
            "{\n"
            f"    \"dependency_files\": [\"{self.repo.get_repo_path()}/path/to/file1\"]\n"
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
            logger.debug("\n #### The `DependencyFileFinderAgent` is sending a request to the AI Gateway")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.debug("\n #### The `DependencyFileFinderAgent` encountered a JSON decoding error and is attempting to repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  The `DependencyFileFinderAgent` encountered an error during dependency file planning: {e}")
            return {
                "reason": str(e)
            }


    async def get_dependency_file_plannings(self):
        logger.debug("\n #### The `DependencyFileFinderAgent` is starting to gather dependency file plannings")
        all_dependency_file_contents = self.repo.print_tree()

        logger.debug("\n #### The `DependencyFileFinderAgent` is processing the project structure")
        plan = await self.get_dependency_file_planning(all_dependency_file_contents)
        return plan
