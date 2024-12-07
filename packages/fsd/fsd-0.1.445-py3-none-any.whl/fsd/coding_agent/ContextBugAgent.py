import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ContextBugAgent:
    def __init__(self, repo):
        """
        Initialize the ContextBugAgent with the repository.

        Args:
            repo: The repository object containing project information.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, bugs):
        """
        Request file planning from AI for fixing bugs.

        Args:
            bugs (str): The bug logs and error messages to analyze.

        Returns:
            dict: JSON response with the plan including working files needed to fix the bugs.
        """
        logger.debug("\n #### Context bug agent is initiating file planning process")
        prompt = (
            "Based on the provided bug logs and project structure, create a JSON response with one list: 'working_files'. "
            "Provide only a JSON response without any additional text or Markdown formatting. "
            "'working_files' must include the full path for THE MOST RELEVANT existing files (UP TO A MAXIMUM OF 5) that are DIRECTLY and CRITICALLY related to fixing these bugs. Include ONLY files that are ABSOLUTELY NECESSARY for resolving the errors. Rigorously evaluate and prioritize each file's relevance before inclusion. "
            "Carefully examine the provided project structure. ONLY include files that ACTUALLY EXIST in the given project structure. "
            "Include ALL levels of the project folder hierarchy in the file paths. Do not skip any directory levels. "
            "Be EXTREMELY CAREFUL to include all relative paths in the filenames EXACTLY as they appear in the project structure. The paths must be complete from the project root. "
            "Do not include any files if you're unsure of their relevance. "
            "Exclude all third-party libraries, generated folders, and dependency-generated files like: "
            "- node_modules/ and any files within it "
            "- package-lock.json, yarn.lock, pnpm-lock.yaml "
            "- Pods/ and Podfile.lock "
            "- vendor/ and Gemfile.lock "
            "- .gradle/ and gradle/wrapper "
            "- target/ and build/ directories "
            "- Any other lock files, cache directories, or generated dependency files "
            "For dependencies, ONLY include the primary manifest files like: "
            "- package.json "
            "- Podfile (not Podfile.lock) "
            "- Gemfile (not Gemfile.lock) "
            "- pom.xml "
            "- build.gradle "
            "DO NOT include any source code files from dependencies or third-party libraries. "
            "DO NOT INVENT OR HALLUCINATE FILES THAT ARE NOT PRESENT IN THE GIVEN STRUCTURE. Use ONLY the paths that exist in the provided project structure. "
            "ONLY include files that you are 100% certain are needed for fixing these specific bugs, based on: "
            "1. Files mentioned in error messages and stack traces "
            "2. Files that contain code causing the errors "
            "3. Files from the project tree that are DIRECTLY related to the bug fixes "
            "If you have ANY doubt about a file's relevance, DO NOT include it. Other agents rely on this list being precise and accurate. "
            "RETURN NO MORE THAN 5 FILES TOTAL, prioritizing only the most critical and directly relevant ones. You do not need to reach 5 files - include only what is absolutely necessary. "
            "If no files are found, return an empty list. "
            "Use this JSON format:"
            "{\n"
            "    \"working_files\": [\"/absolute/path/to/project/root/folder1/subfolder/file1.extension\", \"/absolute/path/to/project/root/folder2/file2.extension\"],\n"
            "}\n\n"
            "If the list is empty, return:"
            "{\n"
            "    \"working_files\": [],\n"
            "}\n\n"
            f"The current project path is \"{self.repo.get_repo_path()}\". Ensure all file paths start with this project path and EXACTLY match the paths in the provided project structure.\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system", 
                "content": prompt
            },
            {
                "role": "user",
                "content": f"These are the bug logs to analyze:\n{bugs}\nThis is the current project structure:\n{self.repo.print_summarize_with_tree()}\n"
            }
        ]

        try:
            logger.debug("\n #### Context bug agent is sending request to AI for file planning")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            logger.debug("\n #### Context bug agent has received response from AI")
            plan_json = json.loads(response.choices[0].message.content)
            
            # Ensure working_files list exists and contains only unique elements
            plan_json["working_files"] = list(set(plan_json.get("working_files", [])))
            
            return plan_json
        except json.JSONDecodeError:
            logger.debug("\n #### Context bug agent encountered JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  Context bug agent encountered an error: `{e}`")
            return {
                "working_files": [],
                "reason": str(e)
            }

    async def get_file_plannings(self, bugs):
        logger.debug("\n #### Context bug agent is starting file planning process")
        return await self.get_file_planning(bugs)
