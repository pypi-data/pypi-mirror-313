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
                    "2. MANDATORY: Prioritize grouping tasks by logical components and system layers:\n"
                    "   a. Foundation layers (e.g., database setup, core utilities)\n"
                    "   b. Application layout and structure\n"
                    "   c. Business logic and core functionality\n"
                    "   d. Integration (API integration, external services)\n"
                    "   e. User Interface (UI) components\n"
                    "   f. User Experience (UX) enhancements\n"
                    "3. CRITICAL: Focus on logical relationships and dependencies rather than grouping strictly by tech stack.\n"
                    "4. REQUIRED: Maximize concurrent execution within each group while adhering to dependencies.\n"
                    "5. ESSENTIAL: Each group should contain tasks that can be worked on concurrently without violating dependencies or architectural principles.\n"
                    "6. MANDATORY: Enforce separation of concerns, but allow flexibility in grouping when appropriate.\n"
                    "7. CRITICAL: Order groups following Pyramid architecture principles, ensuring each group provides necessary context for subsequent groups.\n"
                    "8. REQUIRED: Provide `file_name` (full path) and `techStack` for each task.\n"
                    "9. MUST: Omit configuration, dependencies, and non-essential files.\n"
                    "10. MANDATORY: Exclude all image files except `.svg` and all audio asset files.\n"
                    "11. ABSOLUTELY CRITICAL: Lead-Follow Principle with Concurrent Execution:\n"
                    "    - For EVERY tech stack (HTML, CSS, JS, Python, etc.), identify ONE lead file that establishes patterns\n"
                    "    - Lead file MUST be in its own group and implemented first\n"
                    "    - Group similar 'follower' files together for concurrent execution\n"
                    "    - Example HTML Lead-Follow with Concurrent Execution:\n"
                    "      Group 1: index.html (LEAD - establishes page structure patterns)\n"
                    "      Group 2: about.html, contact.html, community.html (FOLLOW - concurrent implementation using index.html patterns)\n"
                    "    - Example CSS Lead-Follow with Concurrent Execution:\n"
                    "      Group 1: global.css (LEAD - establishes styling patterns)\n"
                    "      Group 2: components.css, layout.css, utilities.css (FOLLOW - concurrent implementation using global.css patterns)\n"
                    "    - Example Backend Lead-Follow with Concurrent Execution:\n"
                    "      Group 1: base_model.py (LEAD - establishes model patterns)\n"
                    "      Group 2: user_model.py, product_model.py, order_model.py (FOLLOW - concurrent implementation using base_model.py patterns)\n"
                    "12. ABSOLUTELY MANDATORY: Frontend Core-Before-Style Rule with Concurrent Execution:\n"
                    "    - ONLY global theme styles can be implemented first\n"
                    "    - For ALL other frontend components:\n"
                    "      * Core files (HTML) MUST be implemented before their style files (CSS)\n"
                    "      * Group similar core files together for concurrent execution\n"
                    "      * Group corresponding style files together for concurrent execution\n"
                    "      * MUST complete smaller components before any main/global components\n"
                    "      * ABSOLUTELY CRITICAL: Each HTML file MUST be implemented BEFORE its corresponding CSS file\n"
                    "      * NEVER implement a CSS file before its corresponding HTML file is complete\n"
                    "    - Strict Ordering Example with Concurrent Execution:\n"
                    "      Group 1: theme.css, variables.css (Global theme - concurrent)\n"
                    "      Group 2: button.html, input.html, icon.html (Small component cores - concurrent)\n"
                    "      Group 3: button.css, input.css, icon.css (Small component styles - concurrent)\n"
                    "      Group 4: card.html, modal.html, form.html (Small component cores - concurrent)\n"
                    "      Group 5: card.css, modal.css, form.css (Small component styles - concurrent)\n"
                    "      Group 6: header.html, footer.html, nav.html (Main component cores - concurrent)\n"
                    "      Group 7: header.css, footer.css, nav.css (Main component styles - concurrent)\n"
                    "      Group 8: index.html (Lead page core)\n"
                    "      Group 9: about.html, contact.html, community.html (Page cores - concurrent)\n"
                    "      Group 10: index.css, about.css, contact.css, community.css (Page styles - concurrent)\n"
                    "13. CRITICAL: Apply Lead-Follow to ALL Tech Stacks with Concurrent Execution:\n"
                    "    - Frontend JS:\n"
                    "      Group 1: main.js (LEAD - core functionality patterns)\n"
                    "      Group 2: utils.js, helpers.js, validators.js (FOLLOW - concurrent)\n"
                    "    - Backend Routes:\n"
                    "      Group 1: base_router.py (LEAD - routing patterns)\n"
                    "      Group 2: auth_routes.py, api_routes.py, user_routes.py (FOLLOW - concurrent)\n"
                    "    - Database:\n"
                    "      Group 1: base_schema.sql (LEAD - schema patterns)\n"
                    "      Group 2: user_schema.sql, product_schema.sql, order_schema.sql (FOLLOW - concurrent)\n"
                    "14. REQUIRED: Group 'follower' files from the same stack together when they can be executed concurrently without needing context from other stacks.\n"
                    "15. ESSENTIAL: For components or layers not directly relevant to each other, group them together if they can be executed concurrently, even if they have different tech stacks.\n"
                    "16. MANDATORY: All SVG files must be strictly grouped together in the last group, without exception.\n"
                    "17. CRITICAL: Critically analyze dependencies between files. If file A depends on file B, ensure B is implemented before A, but group independent files together when possible.\n"
                    "18. REQUIRED: The order of groups is crucial. Always prioritize providing necessary context for subsequent tasks while maximizing concurrent execution within groups.\n"
                    "19. ESSENTIAL: Each file should appear only once in the entire plan. Ensure correct ordering to avoid repetition.\n"
                    "20. MUST: Generate a commit message for the changes/updates, for specific work. The commit message must use the imperative tense and be structured as follows: <type>: <description>. Use these for <type>: bugfix, feature, optimize, update, config, document, format, restructure, enhance, verify. The commit message should be a single line.\n"
                    "21. ABSOLUTELY MANDATORY: ALWAYS implement small, reusable components group BEFORE any main/global group, with concurrent execution where possible.\n"
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
                "content": f"Create a grouped task list following Pyramid architecture using only files from:\n{file_list} - MUST Only include files from the provided 'file_list' for all task, no exception\n\nPrioritize grouping by logical components and system layers (foundation, business logic, integration, UI, etc.). Maximize concurrent execution within groups. Apply the lead-follow principle across all relevant stacks (e.g., models, views, controllers, HTML, CSS, JS). Place each lead file in its own group to be completed first, with other files in the same stack grouped together when they can be executed concurrently without needing context from other stacks. Group components or layers not directly relevant to each other if they can be executed concurrently, even if they have different tech stacks. Order groups to provide context, adhering to Pyramid principles. Analyze dependencies: if A depends on B, B precedes A, but group independent files together. Each file appears once.\n\nFrontend Group Ordering Rules with Concurrent Execution:\n1. Global Theme First:\n   - ONLY global theme files (theme.css, variables.css) - concurrent\n2. Small Components Second:\n   - Small component core files (HTML) before their styles - group similar components for concurrent execution\n   - Complete all small components before main components\n3. Main Components Third:\n   - Main component core files (HTML) before their styles - group similar components for concurrent execution\n4. Pages Last:\n   - Lead page core file (e.g., index.html) first\n   - Similar page core files grouped for concurrent execution\n   - Page style files grouped for concurrent execution\n   - ABSOLUTELY CRITICAL: Each HTML file MUST be implemented BEFORE its corresponding CSS file\n   - NEVER implement a CSS file before its corresponding HTML file is complete\n   - Example Concurrent Groups:\n     Group 1: index.html (Lead)\n     Group 2: about.html, contact.html, community.html (Concurrent follower pages)\n     Group 3: index.css, about.css, contact.css, community.css (Concurrent styles)\n\nOriginal instruction: {instruction}\n\n"
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