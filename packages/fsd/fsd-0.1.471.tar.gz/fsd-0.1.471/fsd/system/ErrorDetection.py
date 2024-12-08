import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class ErrorDetection:
    """
    A class to plan and manage tasks using AI-powered assistance, including error handling and suggestions.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self):
        """
        Initialize the conversation with a system prompt and user context.
        """

        system_prompt = (
            "You're a DevOps expert analyzing run, build, or compile errors. Determine if it's a code issue (type 1), configuration/dependency issue (type 2), or ambiguous requiring human confirmation (type 3). Provide a clear analysis.\n\n"
            "Instructions:\n"
            "1. Examine the error message.\n"
            "2. Categorize as type 1, 2, or 3.\n"
            "3. Extract only error-related info.\n"
            "4. Return JSON:\n"
            "   {\n"
            "     'error_type': <1, 2, or 3>,\n"
            "     'error_message': <error info>\n"
            "   }\n\n"
            "Type 1 (Code):\n"
            "- Syntax errors\n"
            "- Logic errors\n"
            "- Type mismatches\n"
            "- Undefined variables\n"
            "- Incorrect function calls\n"
            "- Import errors for relative imports (e.g., from .module import func)\n"
            "- Import errors from project source (e.g., from src.utils import helper)\n"
            "- Indentation errors\n"
            "- Name errors (undefined name)\n"
            "- Attribute errors (object has no attribute)\n"
            "- Index errors (list index out of range)\n"
            "- Key errors (dictionary key not found)\n"
            "- Value errors (incorrect value type)\n"
            "- Runtime errors (general Python errors)\n\n"
            "Type 2 (Config/Dependency):\n"
            "- Missing repositories\n"
            "- Failed installations\n"
            "- Missing external dependencies\n"
            "- System-wide misconfigurations\n"
            "- Version conflicts\n"
            "- Port blocks\n"
            "- Environment setup issues\n"
            "- Import errors for external libraries (e.g., import numpy, import requests)\n"
            "- Permission errors\n"
            "- File not found errors (for config files)\n"
            "- Database connection errors\n"
            "- Network-related errors\n"
            "- Memory allocation errors\n"
            "- Disk space issues\n\n"
            "Type 3 (Ambiguous/Needs Human Confirmation):\n"
            "- Error could be either code or dependency related\n"
            "- Root cause is unclear\n"
            "- Multiple potential causes\n"
            "- Requires more context or investigation\n\n"
            "Examples:\n"
            "1. {'error_type': 1, 'error_message': 'SyntaxError: invalid syntax (file.py, line 10)'}\n"
            "2. {'error_type': 2, 'error_message': 'ImportError: No module named \"requests\"'}\n"
            "3. {'error_type': 1, 'error_message': 'ModuleNotFoundError: No module named \"src.utils\"'}\n"
            "4. {'error_type': 2, 'error_message': 'PermissionError: [Errno 13] Permission denied: \"/etc/config.ini\"'}\n"
            "5. {'error_type': 3, 'error_message': 'ImportError: No module named \"utils\"'}\n"
            "6. {'error_type': 3, 'error_message': 'FileNotFoundError: [Errno 2] No such file or directory: \"config.json\"'}\n"
            "Provide only JSON, no additional text or Markdown."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
    

    async def get_task_plan(self, error):
        """
        Get a dependency installation plan based on the error, config context, and OS architecture using AI.

        Args:
            error (str): The error message encountered during dependency installation.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        prompt = (
             f"Analyze the following error and determine if it's a code error or a dependency error. Provide a comprehensive explanation and suggested action.\n\n"
             f"Error: {error}\n"
             "Return your analysis in a JSON format with the following structure:\n"
             "{\n"
             "  'error_type': <1, 2, or 3 as an integer (3 if unsure/ambiguous)>,\n"
             "  'error_message': <combined error information as a string>\n"
             "}\n"
             "Provide only the JSON response without additional text or Markdown symbols.\n"
             "Use error_type 3 if:\n"
             "- The error could be either code or dependency related\n"
             "- You are unsure about the root cause\n"
             "- Human investigation is needed to determine the exact issue"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, 4096, 0.2, 0.1)
            self.remove_latest_conversation()
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"ErrorDetection failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, error):
        """
        Get development plans based on the error, config context, and OS architecture.

        Args:
            error (str): The error message encountered during dependency installation.
            config_context (str): The configuration context of the project.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug(f" #### The `ErrorDetection` agent is analyzing the error and generating a task plan")
        plan = await self.get_task_plan(error)
        logger.debug(f" #### The `ErrorDetection` agent has completed the error analysis and produced a plan")
        return plan
