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

class CompileFileFinderAgent:
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
            logger.debug(f" #### `CompileFileFinderAgent` encountered an error while reading dependency file:\n{file_path}\nError: {e}")
            return None


    async def get_compile_file_planning(self, userRequest, tree):
        """
        Request compile file planning from Azure OpenAI API for a given project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            userRequest (str): The user's request or context.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the compile file plan.
        """
        prompt = (
            f"Identify THE MOST CRITICAL build/run and dependency files (MAXIMUM 3 FILES) in the project structure.\n\n"
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
            "5. Include BOTH dependency manifest files AND main build/run files:\n"
            "   Dependency manifest examples:\n"
            "   - package.json (NOT package-lock.json)\n"
            "   - Podfile (NOT Podfile.lock)\n"
            "   - requirements.txt\n"
            "   - pom.xml\n"
            "   Main build/run file examples:\n"
            "   - Python: main.py, app.py, run.py\n"
            "   - JavaScript: index.js, main.js, app.js\n"
            "   - Java: Main.java, App.java\n"
            "   - Go: main.go\n"
            "   - C#: Program.cs\n"
            "   - Ruby: main.rb, app.rb\n"
            "   - PHP: index.php\n"
            "   - Rust: main.rs\n"
            "   - C/C++: main.c, main.cpp\n"
            "   - Swift: main.swift\n"
            "   - Kotlin: Main.kt\n"
            "   Run script files:\n"
            "   - Windows: run.bat, start.bat\n"
            "   - macOS/Linux: run.sh, start.sh\n\n"
            "Return ONLY this JSON format:\n"
            "{\n"
            f"    \"crucial_files\": [\"{self.repo.get_repo_path()}/path/to/file1\"]\n"
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
                "content": f"User Request: {userRequest}\nThis is the current project structure:\n{tree}\n"
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
            logger.error(f"  `CompileFileFinderAgent` failed to obtain dependency file planning:\nError: {e}")
            return {
                "reason": str(e)
            }


    async def get_compile_file_plannings(self, userRequest):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """
        logger.debug("\n #### `CompileFileFinderAgent` is initiating the file processing task")
        all_dependency_file_contents = self.repo.print_tree()

        plan = await self.get_compile_file_planning(userRequest, all_dependency_file_contents)
        logger.debug("\n #### `CompileFileFinderAgent` has successfully completed the file processing task")
        return plan
