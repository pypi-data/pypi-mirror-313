import os
import sys
import aiohttp
import asyncio
import json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
import platform

logger = get_logger(__name__)

class BugPlanner:
    def __init__(self, repo):
        self.repo = repo
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def initial_setup(self, role):
        """Set up the initial prompt for the bug analysis agent."""
        prompt = (
            f"You are a senior bug analysis agent. Analyze the project files and develop a comprehensive bug fix plan. Follow these guidelines meticulously:\n\n"
            f"User OS: {platform.system()}\n"
            f"Project root path: {self.repo.get_repo_path()}\n\n"
            "Guidelines:\n"
            "- Focus on high-level bug fix planning and analysis\n"
            "- Only provide code snippets if absolutely critical to explain the fix\n"
            "- Prioritize clear explanation of issues and solutions\n\n"
            
            "For each bug:\n"
            "1. Root Cause Analysis:\n"
            "- Identify the core issue and affected files\n"
            "- Explain the bug's impact on system functionality\n"
            "- List any related files that may need changes with full paths from project root\n\n"
            
            "2. Fix Strategy:\n"
            "- Describe the high-level approach to fix each bug\n"
            "- Specify which files need modification (with full paths from project root)\n"
            "- Note any new files or dependencies needed\n"
            "- DO NOT include detailed code implementations unless critical\n\n"
            
            "3. Testing Considerations:\n"
            "- Note key test scenarios\n"
            "- Identify potential regression risks\n\n"
            
            "Important:\n"
            f"- Use OS-appropriate file paths starting from project root: {self.repo.get_repo_path()}\n"
            "- Focus on planning and analysis, not implementation details\n"
            "- Provide clear reasoning for suggested changes\n"
            "- Only include minimal code snippets if essential to explain the fix\n\n"
            
            "DO NOT INCLUDE:\n"
            "- Detailed code implementations\n"
            "- File navigation steps\n"
            "- Browser/device actions\n"
            "- Manual verifications\n"
            "- Non-coding actions\n\n"
            
            "Keep responses focused on bug analysis and fix planning. Minimize code examples."
        )

        self.conversation_history.append({"role": "system", "content": prompt})

    async def get_bugFixed_suggest_request(self, bug_logs, all_file_contents, overview, file_attachments=None, focused_files=None):
        """Get bug fix suggestions based on logs and files."""
        error_prompt = (
            f"Current working file:\n{all_file_contents}\n\n"
            f"Tree:\n{self.repo.print_tree()}\n\n"
            f"Project overview:\n{overview}\n\n"
            f"Bug logs:\n{bug_logs}\n\n"
            "Analyze the bugs and provide a clear fix plan.\n\n"
            "IMPORTANT: This is a high-level bug fix planning phase. Focus on:\n"
            "- Identifying root causes and affected components\n" 
            "- Explaining the issues and proposed solutions\n"
            "- Listing files that need changes (with full paths)\n"
            "- Describing fix approaches and testing needs\n\n"
            "DO NOT provide detailed code implementations unless absolutely critical for explaining the fix.\n"
            "Keep the plan short and focused on essential changes only.\n"
            "Keep responses focused on analysis and planning rather than implementation details.\n"
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
            error_prompt += f"\nUser has attached these files for reference: {all_attachment_file_contents}"

        if all_focused_files_contents:
            error_prompt += f"\nFocused files requiring special attention: {all_focused_files_contents}"

        self.conversation_history.append({"role": "user", "content": error_prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"BugPlanner: Failed to get bug fix suggestion: {e}")
            return f"Error: {str(e)}"

    async def get_bugFixed_suggest_requests(self, bug_logs, files, overview, file_attachments=None, focused_files=None):
        """Get bug fix suggestions for multiple files."""
        filtered_lists = [file for file in files if file]

        logger.debug("BugPlanner: Initiating file scan for bug analysis")

        all_file_contents = ""

        for file_path in filtered_lists:
            try:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {os.path.relpath(file_path)}\n{file_content}"
            except Exception as e:
                all_file_contents += f"\n\nBugPlanner: Failed to read file {file_path}: {str(e)}"

        logger.info("BugPlanner: File content compilation completed, proceeding with bug analysis")

        plan = await self.get_bugFixed_suggest_request(bug_logs, all_file_contents, overview, file_attachments, focused_files)
        return plan