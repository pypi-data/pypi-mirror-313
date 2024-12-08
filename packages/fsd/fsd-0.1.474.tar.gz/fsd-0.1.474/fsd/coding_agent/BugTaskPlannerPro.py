import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class BugTaskPlannerPro:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list, original_prompt_language):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            file_list (list): List of available files.
            original_prompt_language (str): The language of the original prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in bug fixing and code quality. STRICTLY generate an ordered list of task groups for implementing bug fixes based on the user's instruction and provided file list.\n\n"
                    "MANDATORY Guidelines:\n"
                    "1. ABSOLUTELY MUST Only include files from the provided 'file_list' for all tasks - NO EXCEPTIONS ALLOWED.\n"
                    "2. STRICTLY ENFORCE small components first, then main components:\n"
                    "   a. Utility/Helper functions and classes\n"
                    "   b. Base components and foundational modules\n"
                    "   c. Shared services and middleware\n"
                    "   d. Feature-specific components\n"
                    "   e. Main application components\n"
                    "3. CRITICAL Tech Stack Grouping (examples):\n"
                    "   - Python: utils, helpers, models, services, controllers\n"
                    "   - JavaScript: utils, hooks, contexts, components, pages\n"
                    "   - Java: utils, models, repositories, services, controllers\n"
                    "   - Go: utils, interfaces, repositories, services, handlers\n"
                    "   - Ruby: helpers, models, services, controllers\n"
                    "   - TypeScript: types, utils, hooks, components, pages\n"
                    "4. MANDATORY Bug Priority Order:\n"
                    "   a. CRITICAL system crashes and data corruption\n"
                    "   b. SEVERE security vulnerabilities\n"
                    "   c. HIGH IMPACT data integrity issues\n"
                    "   d. MAJOR performance bottlenecks\n"
                    "   e. SIGNIFICANT UI/UX defects\n"
                    "   f. MINOR enhancements\n"
                    "5. STRICTLY ENFORCE dependency chain:\n"
                    "   - MUST fix foundational bugs before dependent ones\n"
                    "   - REQUIRED to fix shared components before specific ones\n"
                    "   - MANDATORY to fix data layer before business logic\n"
                    "6. ABSOLUTELY REQUIRED Testing Coverage:\n"
                    "   - MUST include unit tests for utils/helpers first\n"
                    "   - REQUIRED integration tests for services\n"
                    "   - MANDATORY end-to-end tests for complete flows\n"
                    "7. CRITICAL File Requirements:\n"
                    "   - MUST provide `file_name` with full path\n"
                    "   - REQUIRED `techStack` specification\n"
                    "   - NO duplicates allowed\n"
                    "8. STRICTLY ENFORCE Component Dependencies:\n"
                    "   - Core Utils/Helpers:\n"
                    "     * Fix utility functions first\n"
                    "     * Fix helper classes second\n"
                    "   - Base Components:\n"
                    "     * Fix shared hooks/utils first\n"
                    "     * Fix base components second\n"
                    "   - Services:\n"
                    "     * Fix data services first\n"
                    "     * Fix business logic second\n"
                    "   - Main Components:\n"
                    "     * Fix core features last\n"
                    "9. MANDATORY Commit Message Format:\n"
                    "   bugfix(scope): <precise_description>\n"
                    "Response Format:\n"
                    '{\n'
                    '    "groups": [\n'
                    '        {\n'
                    '            "group_name": "",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.py",\n'
                    '                    "techStack": "python"\n'
                    '                }\n'
                    '            ]\n'
                    '        }\n'
                    '    ],\n'
                    '    "commits": ""\n'
                    '}'
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "MUST return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user", 
                "content": f"STRICTLY create a grouped task list for bug fixing using ONLY files from:\n{file_list} - ABSOLUTELY MUST Only include files from the provided 'file_list' for all tasks, NO EXCEPTIONS.\n\nMANDATORY: Start with smallest components (utils, helpers, base components) before main components. Group by tech stack following the examples provided. CRITICAL: Respect all dependency chains and ensure comprehensive testing coverage. Original instruction: {instruction}\n\n"
            }
        ]

        try:
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f"  The `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists, original_prompt_language):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists, original_prompt_language)
        logger.debug("\n #### The `TaskPlanner` has completed generating the task plans")
        return plan