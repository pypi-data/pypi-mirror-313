import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlannerPro:
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
                    "You are a principal engineer specializing in Pyramid architecture. Generate an ordered list of task groups for implementing a system based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. MUST Only include files from the provided 'file_list' for all task, no exception.\n"
                    "2. MUST prioritize small, atomic components before larger global/main files:\n"
                    "   - Individual UI components before container components\n" 
                    "   - Utility functions before service layers\n"
                    "   - Base styles before global styles\n"
                    "   - Helper modules before core modules\n"
                    "   - Atomic components before composite components\n"
                    "   - Individual routes before route aggregators\n"
                    "   - Single model definitions before model relationships\n"
                    "3. Prioritize grouping tasks by logical components and system layers:\n"
                    "   a. Foundation layers (e.g., database setup, core utilities)\n"
                    "   b. Application layout and structure\n"
                    "   c. Business logic and core functionality\n"
                    "   d. Integration (API integration, external services)\n"
                    "   e. User Interface (UI) components\n"
                    "   f. User Experience (UX) enhancements\n"
                    "4. Focus on logical relationships and dependencies rather than grouping strictly by tech stack.\n"
                    "5. Maximize concurrent execution within each group while adhering to dependencies.\n"
                    "6. Each group should contain tasks that can be worked on concurrently without violating dependencies or architectural principles.\n"
                    "7. Enforce separation of concerns, but allow flexibility in grouping when appropriate.\n"
                    "8. Order groups following Pyramid architecture principles, ensuring each group provides necessary context for subsequent groups.\n"
                    "9. Provide `file_name` (full path) and `techStack` for each task.\n"
                    "10. Omit configuration, dependencies, and non-essential files.\n"
                    "11. Exclude all image files except `.svg` and all audio asset files.\n"
                    "12. Apply the lead-follow principle across all relevant stacks (e.g., models, views, controllers, HTML, CSS, JS). Create a separate group for a 'lead' file within each relevant stack. The lead file must be implemented first and defines the structure, patterns, and conventions for that stack.\n"
                    "13. Group 'follower' files from the same stack together when they can be executed concurrently without needing context from other stacks.\n"
                    "14. For components or layers not directly relevant to each other, group them together if they can be executed concurrently, even if they have different tech stacks.\n"
                    "15. All SVG files must be strictly grouped together in the last group, without exception.\n"
                    "16. Critically analyze dependencies between files. If file A depends on file B, ensure B is implemented before A, but group independent files together when possible.\n"
                    "17. The order of groups is crucial. Always prioritize providing necessary context for subsequent tasks while maximizing concurrent execution within groups.\n"
                    "18. Each file should appear only once in the entire plan. Ensure correct ordering to avoid repetition.\n"
                    "19. Generate a commit message for the changes/updates, for specific work. The commit message must use the imperative tense and be structured as follows: <type>: <description>. Use these for <type>: bugfix, feature, optimize, update, config, document, format, restructure, enhance, verify. The commit message should be a single line.\n"
                    "20. Separate interdependent components into different groups to ensure proper dependency management and maximize parallel development in software development. For example:\n"
                    "    - Frontend:\n"
                    "        - Individual UI components before container components\n"
                    "        - Base/reset CSS before theme CSS before global CSS\n"
                    "        - Individual component styles before layout styles\n"
                    "        - Utility functions before component logic\n"
                    "        - Individual form components before form containers\n"
                    "        - Individual route components before route configuration\n"
                    "        - State slice reducers before root reducer\n"
                    "        - Individual hooks before hook composition\n"
                    "        - Individual animations before animation systems\n"
                    "        - Base components before composite components\n"
                    "    - Backend:\n"
                    "        - Individual model attributes before relationships\n"
                    "        - Base repository classes before specific repositories\n"
                    "        - Individual endpoints before route groups\n"
                    "        - Individual validators before validation chains\n"
                    "        - Base service classes before specific services\n"
                    "        - Individual middleware before middleware chains\n"
                    "        - Individual database migrations before schema updates\n"
                    "        - Base DTO classes before specific DTOs\n"
                    "    - Full-stack:\n"
                    "        - Individual API contracts before client implementation\n"
                    "        - Base WebSocket handlers before specific handlers\n"
                    "        - Individual type definitions before type composition\n"
                    "        - Base error classes before specific errors\n"
                    "    - Testing:\n"
                    "        - Individual test helpers before test suites\n"
                    "        - Individual mocks before mock factories\n"
                    "        - Unit tests before integration tests\n"
                    "        - Individual test cases before test aggregation\n"
                    "    - Documentation:\n"
                    "        - Individual component docs before module docs\n"
                    "        - API endpoint docs before API overview\n"
                    "        - Individual type docs before type system docs\n"
                    "    - Internationalization:\n"
                    "        - Individual translation keys before translation bundles\n"
                    "        - Base locale config before locale extensions\n"
                    "    - Security:\n"
                    "        - Individual security rules before security chains\n"
                    "        - Base auth handlers before specific handlers\n"
                    "        - Individual permission checks before RBAC system\n"
                    "    - Performance:\n"
                    "        - Individual cache handlers before cache system\n"
                    "        - Base optimizations before specific optimizations\n"
                    "    - Data Processing:\n"
                    "        - Individual transformers before pipelines\n"
                    "        - Base validators before validation chains\n"
                    "        - Individual processors before process orchestration\n"
                    "    - Error Handling:\n"
                    "        - Individual error types before error hierarchies\n"
                    "        - Base error handlers before error chains\n"
                    "    - Events:\n"
                    "        - Individual event handlers before event systems\n"
                    "        - Base emitters before specific emitters\n"
                    "    - Code Generation:\n"
                    "        - Individual templates before template systems\n"
                    "        - Base generators before specific generators\n"
                    "    - Dependency Injection:\n"
                    "        - Individual services before service containers\n"
                    "        - Base providers before provider composition\n"
                    "    - Logging:\n"
                    "        - Individual loggers before logging system\n"
                    "        - Base formatters before specific formatters\n"
                    "    - Feature Flags:\n"
                    "        - Individual flags before flag systems\n"
                    "        - Base toggles before toggle composition\n"
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
                    '        },\n'
                    '        {\n'
                    '            "group_name": "",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.html",\n'
                    '                    "techStack": "html"\n'
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
                "content": f"Create a grouped task list following Pyramid architecture using only files from:\n{file_list} - MUST Only include files from the provided 'file_list' for all task, no exception\n\nPrioritize grouping by logical components and system layers (foundation, business logic, integration, UI, etc.). Maximize concurrent execution within groups. Apply the lead-follow principle across all relevant stacks (e.g., models, views, controllers, HTML, CSS, JS). Place each lead file in its own group to be completed first, with other files in the same stack grouped together when they can be executed concurrently without needing context from other stacks. Group components or layers not directly relevant to each other if they can be executed concurrently, even if they have different tech stacks. Order groups to provide context, adhering to Pyramid principles. Analyze dependencies: if A depends on B, B precedes A, but group independent files together. Each file appears once. Ensure HTML files are grouped before CSS files, and one main CSS file (global, home, or main) is in a group before other CSS files to establish the theme. Original instruction: {instruction}\n\n"
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