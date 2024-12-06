import os
import sys
import asyncio
import re
import platform
from json_repair import repair_json
import aiohttp
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class BugExplainer:
    def __init__(self, repo):
        self.repo = repo
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def initial_setup(self, role):
        """Set up the initial prompt for the bug-fixing agent."""
        prompt = (
            f"You are a world-class, highly experienced bug analysis agent. Analyze the project context and errors, identify root causes, and provide structured steps to fix each bug. Focus on the root cause, not applying fixes to all affected files. Rules:\n"
            f"User OS: {platform.system()}\n"
            "1. Each step involves one file only.\n"
            "2. 'file_name' must include full file path using OS-appropriate separators.\n"
            "3. 'list_related_file_name' includes full paths of potentially impacted files; empty list if none.\n"
            "4. 'is_new' is 'True' for new files, 'False' otherwise.\n"
            "5. 'new_file_location' specifies relative path for new files.\n"
            "Respond with valid JSON only without additional text or symbols or MARKDOWN, following this format:\n"
            "{\n"
            "    \"steps\": [\n"
            "        {\n"
            "            \"Step\": 1,\n"
            "            \"file_name\": \"Full/Path/To/File.ext\",\n"
            "            \"tech_stack\": \"Language\",\n"
            "            \"is_new\": \"True/False\",\n"
            "            \"new_file_location\": \"Relative/Path\",\n"
            "            \"list_related_file_name\": [\"Full/Path/To/Related1.ext\", \"Full/Path/To/Related2.ext\"],\n"
            "            \"Solution_detail_title\": \"Brief issue description\",\n"
            "            \"all_comprehensive_solutions_for_each_bug\": \"Detailed fix instructions with OS-appropriate commands\"\n"
            "        }\n"
            "    ]\n"
            "}\n"
            "For paths with spaces, preserve the original spaces without escaping or encoding.\n"
            "All file paths and commands should be compatible with the user's OS."
        )

        self.conversation_history.append({"role": "system", "content": prompt})

    async def get_bugFixed_suggest_request(self, bug_logs, all_file_contents, overview, file_attachments=None, focused_files=None):
        """
        Get development plan for all txt files from Azure OpenAI based on user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            overview (str): Project overview description.

        Returns:
            dict: Development plan or error reason.
        """

        error_prompt = (
            f"Current working file:\n{all_file_contents}\n\n"
            f"Tree:\n{self.repo.print_tree()}\n\n"
            f"Project overview:\n{overview}\n\n"
            f"Bug logs:\n{bug_logs}\n\n"
            "Return only a valid JSON format bug fix response without additional text or Markdown symbols or invalid escapes.\n\n"
        )

        file_attachments = file_attachments or []
        focused_files = focused_files or []
        
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        all_attachment_file_contents = ""
        all_focused_files_contents = ""

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if focused_files:
            for file_path in focused_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            error_prompt += f"\nUser has attached these files for you, use them appropriately: {all_attachment_file_contents}"

        if all_focused_files_contents:
            error_prompt += f"\nUser has focused on these files in the current project, pay special attention to them according if need: {all_focused_files_contents}"

        self.conversation_history.append({"role": "user", "content": error_prompt})

        try:
            response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  `BugExplainer`: Failed to get bug fix suggestion: {e}")
            return {
                "reason": e
            }


    async def get_bugFixed_suggest_requests(self, bug_logs, files, overview, file_attachments=None, focused_files=None):
        """
        Get development plans for a list of txt files from Azure OpenAI based on user prompt.

        Args:
            bug_logs (str): bug_logs.
            files (list): List of file paths.
            overview (str): Overview description.

        Returns:
            dict: Development plan or error reason.
        """
        # Step to remove all empty files from the list
        filtered_lists = [file for file in files if file]

        logger.debug(f" #### `BugExplainer`: Initiating file scan for bug analysis")

        all_file_contents = ""

        # Scan needed files based on the filtered list
        final_files_paths = filtered_lists

        for file_path in final_files_paths:
            try:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {os.path.relpath(file_path)}\n{file_content}"
            except Exception as e:
                all_file_contents += f"\n\nBugExplainer: Failed to read file {file_path}: {str(e)}"

        logger.info(f" #### `BugExplainer`: File content compilation completed, proceeding to create a bug fix plan.")

        # Get the bug-fixed suggestion request
        plan = await self.get_bugFixed_suggest_request(bug_logs, all_file_contents, overview, file_attachments, focused_files)
        return plan