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
                    "You are a principal engineer specializing in bug fixing and code quality. Generate an ordered list of task groups for implementing bug fixes based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. MUST Only include files from the provided 'file_list' for all tasks, no exception.\n"
                    "2. Prioritize grouping tasks by bug impact and dependencies:\n"
                    "   a. Critical bugs affecting core functionality\n" 
                    "   b. Security vulnerabilities\n"
                    "   c. Data integrity issues\n"
                    "   d. Performance bottlenecks\n"
                    "   e. UI/UX defects\n"
                    "   f. Minor enhancements\n"
                    "3. Focus on minimizing regression risks and maintaining system stability.\n"
                    "4. Each group should contain related bug fixes that can be tested together.\n"
                    "5. Enforce proper testing coverage for all bug fixes.\n"
                    "6. Order groups by criticality while respecting dependencies.\n"
                    "7. Provide `file_name` (full path) and `techStack` for each task.\n"
                    "8. Exclude configuration and non-essential files.\n"
                    "9. Exclude all image files except `.svg` and all audio asset files.\n"
                    "10. Group related bug fixes together to minimize context switching.\n"
                    "11. Ensure proper error handling and logging for all fixes.\n"
                    "12. Consider data migration needs for bug fixes.\n"
                    "13. Group validation and sanitization fixes together.\n"
                    "14. Place SVG fixes in the last group.\n"
                    "15. Analyze fix dependencies carefully - if fix A depends on fix B, ensure B is implemented first.\n"
                    "16. Each file should appear only once in the plan.\n"
                    "17. Generate clear commit messages for each bug fix using format: bugfix: <description>.\n"
                    "18. Separate interdependent fixes:\n"
                    "    - Core System:\n"
                    "        - Database schema fixes before data fixes\n"
                    "        - Authentication fixes before authorization fixes\n"
                    "        - API endpoint fixes before client fixes\n"
                    "    - Frontend:\n"
                    "        - HTML structure fixes before styling fixes\n"
                    "        - Core component fixes before dependent components\n"
                    "        - State management fixes before UI fixes\n"
                    "    - Backend:\n"
                    "        - Model fixes before business logic fixes\n"
                    "        - Middleware fixes before route fixes\n"
                    "        - Data access fixes before service fixes\n"
                    "    - Testing:\n"
                    "        - Test utility fixes before test fixes\n"
                    "        - Unit test fixes before integration test fixes\n"
                    "    - Security:\n"
                    "        - Input validation fixes early\n"
                    "        - Authentication fixes before feature fixes\n"
                    "    - Performance:\n"
                    "        - Core algorithm fixes first\n"
                    "        - Caching fixes after core fixes\n"
                    "    - Error Handling:\n"
                    "        - Error class fixes before usage fixes\n"
                    "        - Logging fixes early\n"
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
                    "Return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user", 
                "content": f"Create a grouped task list for bug fixing using only files from:\n{file_list} - MUST Only include files from the provided 'file_list' for all tasks, no exception\n\nPrioritize grouping by bug impact and dependencies. Group related fixes together while respecting dependencies between fixes. Place critical fixes early while ensuring proper testing coverage. Original instruction: {instruction}\n\n"
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