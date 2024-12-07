import os
import aiohttp
import json
import sys
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class DependencyTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, os_architecture, original_prompt_language):
        """
        Get a dependency installation plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for dependency installation planning.
            os_architecture (str): The operating system and architecture of the target environment.
            original_prompt_language (str): The language to use for the prompts.

        Returns:
            dict: Dependency installation plan or error reason.
        """
        logger.debug("\n #### The `DependencyTaskPlanner` is initiating the task planning process")
        messages = [
            {
                "role": "system", 
                "content": (
                    f"Create a JSON step-by-step dependency installation plan for '{self.repo.get_repo_path()}' following pyramid architecture from provided plan.\n"
                    f"User OS: {platform.system()}\n"
                    "Rules:\n"
                    f"1. Start with 'cd' to project directory as a separate step. For {platform.system()}, " + 
                    ("cd \"C:\\Program Files\\MyApp\" (use backslashes and enclose paths with spaces in double quotes)\n" if platform.system() == "Windows" else 
                    "cd '/path/to/my app' (use forward slashes and enclose paths with spaces in single quotes)\n") +
                    "2. For all echo commands or similar configuration instructions, use the 'update' method and provide a detailed prompt specifying exactly what content needs to be added, modified, or removed in the file.\n" 
                    "3. All 'cd' commands must always be in separate steps, DO NOT combine with other commands.\n"
                    "4. Include only essential steps - no verification or double-checking steps.\n"
                    "5. Only Set is_localhost_command to '1' only for commands that start a local development server or build process that needs to stay running (e.g. npm run dev, tauri dev). Set to '0' for all other commands including installations.\n"
                    "6. Generate a commit message for specific work. The commit message must use the imperative tense and be structured as follows: <type>: <description>. Use these for <type>: bugfix, feature, optimize, update, config, document, format, restructure, enhance, verify. The commit message should be a single line.\n"
                    "Format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "N/A or full path",\n'
                    f'            "prompt": "Detailed description of exact content to be updated, including specific lines, configurations, or dependencies to be added, modified, or removed.",\n'
                    '            "method": "update or bash",\n'
                    '            "command": "Exact command (for bash only, omit for update method)",\n'
                    '            "is_localhost_command": "0 or 1 (1 only for local dev server commands that need to stay running)"\n'
                    '        }\n'
                    '    ]\n'
                    '    "commits": ""\n'
                    "}\n\n"
                    f"Provide only valid JSON. No additional text or Markdown. Include only essential steps. All commands must be compatible with {platform.system()} - do not provide commands for other operating systems. For paths with spaces use " +
                    ("double quotes and backslashes (e.g. \"C:\\Program Files\\App\")" if platform.system() == "Windows" else 
                    "single quotes and forward slashes (e.g. '/path/to/my app')")
                )
            },
            {
                "role": "user",
                "content": f"Create dependency installation plan. OS: {os_architecture}. Project tree:\n\n{self.repo.print_tree()}\n\nFollow this plan strictly:\n{instruction}\n\nRespond using the language: {original_prompt_language}"
            }
        ]

        try:
            logger.debug("\n #### The `DependencyTaskPlanner` is dispatching a request to the AI for task planning")
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `DependencyTaskPlanner` has successfully obtained and parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `DependencyTaskPlanner` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  The `DependencyTaskPlanner` encountered an error while retrieving the task plan:\n Error: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, original_prompt_language):
        logger.debug("\n #### The `DependencyTaskPlanner` is commencing the retrieval of task plans")
        plan = await self.get_task_plan(instruction, original_prompt_language)
        logger.debug("\n #### The `DependencyTaskPlanner` has finalized the retrieval of task plans")
        return plan
