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
                    "11. ABSOLUTELY CRITICAL: Lead-Follow Principle - For EVERY type of component or file group, identify and implement a 'lead' file first that establishes patterns for others to follow. Examples:\n"
                    "    - Pages: Implement index.html first as lead page to establish page structure, then other pages follow its pattern\n"
                    "    - Components: Create a lead Button component first to define component architecture, then other components follow\n"
                    "    - Models: Implement a lead User model first to define model structure, then other models follow\n"
                    "    - Controllers: Create a lead BaseController first to define controller patterns, then specific controllers follow\n"
                    "    - CSS: Global styles first as lead, then component styles following its conventions\n"
                    "    - Tests: Lead test file establishes testing patterns, other tests follow\n"
                    "    - APIs: Lead API endpoint defines REST patterns, other endpoints follow\n"
                    "    - Database: Lead table schema defines database conventions, other schemas follow\n"
                    "12. REQUIRED: After each lead file is complete, group 'follower' files that can be executed concurrently.\n"
                    "13. ESSENTIAL: For components or layers not directly relevant to each other, group them together if they can be executed concurrently, even if they have different tech stacks.\n"
                    "14. MANDATORY: All SVG files must be strictly grouped together in the last group, without exception.\n"
                    "15. CRITICAL: Critically analyze dependencies between files. If file A depends on file B, ensure B is implemented before A, but group independent files together when possible.\n"
                    "16. REQUIRED: The order of groups is crucial. Always prioritize providing necessary context for subsequent tasks while maximizing concurrent execution within groups.\n"
                    "17. ESSENTIAL: Each file should appear only once in the entire plan. Ensure correct ordering to avoid repetition.\n"
                    "18. MUST: Generate a commit message for the changes/updates, for specific work. The commit message must use the imperative tense and be structured as follows: <type>: <description>. Use these for <type>: bugfix, feature, optimize, update, config, document, format, restructure, enhance, verify. The commit message should be a single line.\n"
                    "19. ABSOLUTELY MANDATORY: ALWAYS implement small, reusable components group BEFORE any main/global group. Here are the REQUIRED orderings by tech stack:\n"
                    "    - Frontend Components (HTML/CSS/JS):\n"
                    "        1. MUST START WITH Global Styles:\n"
                    "           - Global CSS variables and tokens\n"
                    "           - Theme definitions\n"
                    "           - Base styles and resets\n"
                    "        2. THEN Atomic HTML Components:\n"
                    "           - Button templates\n"
                    "           - Form input templates\n"
                    "           - Icon templates\n"
                    "           - Typography elements\n"
                    "        3. THEN Atomic CSS Components:\n"
                    "           - Button styles\n"
                    "           - Form input styles\n"
                    "           - Icon styles\n"
                    "           - Typography styles\n"
                    "        4. THEN Molecular HTML Components:\n"
                    "           - Navigation templates\n"
                    "           - Search templates\n"
                    "           - Card templates\n"
                    "           - Form group templates\n"
                    "        5. THEN Molecular CSS Components:\n"
                    "           - Navigation styles\n"
                    "           - Search styles\n"
                    "           - Card styles\n"
                    "           - Form group styles\n"
                    "        6. THEN Organism HTML Components:\n"
                    "           - Header templates\n"
                    "           - Footer templates\n"
                    "           - Sidebar templates\n"
                    "        7. THEN Organism CSS Components:\n"
                    "           - Header styles\n"
                    "           - Footer styles\n"
                    "           - Sidebar styles\n"
                    "        8. THEN Template HTML:\n"
                    "           - Layout templates\n"
                    "           - Grid templates\n"
                    "        9. THEN Template CSS:\n"
                    "           - Layout styles\n"
                    "           - Grid styles\n"
                    "        10. THEN Page HTML:\n"
                    "           - Main pages\n"
                    "           - Index pages\n"
                    "        11. FINALLY Page CSS:\n"
                    "           - Page-specific styles\n"
                    "    - Backend Components (Python/Node/Java/etc):\n"
                    "        1. MUST START WITH Core Utils:\n"
                    "           - Helper functions\n"
                    "           - Data validators\n"
                    "           - Error handlers\n"
                    "           - Logger setup\n"
                    "        2. THEN Data Layer:\n"
                    "           - Base model classes\n"
                    "           - Entity models\n"
                    "           - Data mappers\n"
                    "           - Repository interfaces\n"
                    "        3. FOLLOWED BY Services:\n"
                    "           - Auth service\n"
                    "           - CRUD services\n"
                    "           - Business logic services\n"
                    "           - Integration services\n"
                    "        4. THEN Controllers:\n"
                    "           - Base controller\n"
                    "           - Resource controllers\n"
                    "           - API controllers\n"
                    "        5. FINALLY Routes/API:\n"
                    "           - Route definitions\n"
                    "           - API endpoints\n"
                    "           - Main router\n"
                    "    - Database Components:\n"
                    "        1. MUST START WITH Core:\n"
                    "           - Connection handlers\n"
                    "           - Base repositories\n"
                    "        2. THEN Schemas:\n"
                    "           - Table definitions\n"
                    "           - Index configurations\n"
                    "        3. FINALLY Migrations:\n"
                    "           - Migration scripts\n"
                    "           - Seeders\n"
                    "    - Testing Components:\n"
                    "        1. MUST START WITH Test Utils:\n"
                    "           - Test helpers\n"
                    "           - Mock factories\n"
                    "        2. THEN Unit Tests:\n"
                    "           - Component tests\n"
                    "           - Service tests\n"
                    "        3. FINALLY Integration Tests:\n"
                    "           - API tests\n"
                    "           - E2E tests\n"
                    "20. ABSOLUTELY CRITICAL: Separate interdependent components into different groups to ensure proper dependency management and maximize parallel development in software development. For example:\n"
                    "    - Frontend:\n"
                    "        - Global CSS file MUST be first to establish theme and variables\n"
                    "        - Small component HTML files MUST precede their CSS files\n"
                    "        - Small component CSS files MUST follow their HTML files\n"
                    "        - Main HTML files (index, home) MUST come after all small components\n"
                    "        - Main CSS files MUST follow their corresponding HTML files\n"
                    "        - JavaScript files should be separate from HTML and CSS files\n"
                    "        - UI component definitions should be in a group before their implementations\n"
                    "        - State management logic (e.g., Redux, MobX) should be in a separate group from UI components\n"
                    "        - Client-side routing configuration should be in its own group\n"
                    "        - Utility functions and helpers should be in an early group\n"
                    "    - Backend:\n"
                    "        - Database schema definitions should precede ORM models\n"
                    "        - ORM models should be in a group before business logic files\n"
                    "        - API endpoint definitions should be separate from their implementations\n"
                    "        - Middleware (e.g., authentication, logging) should be in a group before route handlers\n"
                    "        - Database migration scripts should be separate from application code\n"
                    "        - Data access layer should be implemented before business logic\n"
                    "    - Full-stack:\n"
                    "        - Backend API implementation should be in a group before frontend API client code\n"
                    "        - WebSocket server code should be separate from WebSocket client code\n"
                    "        - Shared types or interfaces should be in an early group\n"
                    "    - Configuration and Environment:\n"
                    "        - Environment variable definitions should be in the earliest group\n"
                    "        - Configuration files should be in an early group, separate from the files that use them\n"
                    "    - Testing:\n"
                    "        - Test utilities and mocks should be in a group before actual test files\n"
                    "        - Unit test files should be in a separate group from integration test files\n"
                    "        - Test files should be in a group after the files they are testing\n"
                    "    - Documentation:\n"
                    "        - Inline documentation (comments) should be written alongside the code\n"
                    "        - API documentation should be in a group after API implementation\n"
                    "    - Internationalization and Localization:\n"
                    "        - Localization files should be in a separate group from the components that use them\n"
                    "        - Translation keys should be defined before their usage in components\n"
                    "    - Security:\n"
                    "        - Security utility functions should be in an early group\n"
                    "        - Authentication logic should be separate from authorization logic\n"
                    "        - Input validation and sanitization functions should be in an early group\n"
                    "    - Performance and Optimization:\n"
                    "        - Core algorithms and data structures should be implemented early\n"
                    "        - Caching mechanisms should be implemented after the main functionality\n"
                    "    - Third-party Integrations:\n"
                    "        - Third-party API client implementations should be in a separate group\n"
                    "        - Integration configurations should be separate from their usage in the application\n"
                    "    - Data Processing:\n"
                    "        - Data models should be defined before data processing logic\n"
                    "        - Data validation rules should be in a group before their usage\n"
                    "    - Error Handling:\n"
                    "        - Custom error classes should be defined in an early group\n"
                    "        - Error handling middleware or utilities should be implemented before usage\n"
                    "    - Asynchronous Operations:\n"
                    "        - Promise wrappers or async utilities should be in an early group\n"
                    "        - Event emitters or pub/sub systems should be implemented before usage\n"
                    "    - Code Generation:\n"
                    "        - If using code generators, generated code should be in a group after its dependencies\n"
                    "    - Dependency Injection:\n"
                    "        - DI container configuration should be in an early group\n"
                    "        - Service interfaces should be defined before their implementations\n"
                    "    - Logging:\n"
                    "        - Logging configuration and utilities should be in an early group\n"
                    "    - Feature Flags:\n"
                    "        - Feature flag definitions should be in a group before their usage in code\n"
                    "21. ABSOLUTELY CRITICAL: Lead-Follow Examples for Each Stack:\n"
                    "    - Pages:\n"
                    "        1. Lead: index.html (establishes page structure, navigation flow)\n"
                    "        2. Followers: about.html, contact.html (follow index.html patterns)\n"
                    "    - Components:\n"
                    "        1. Lead: Button.jsx (defines component architecture)\n"
                    "        2. Followers: Input.jsx, Card.jsx (follow Button.jsx patterns)\n"
                    "    - Models:\n"
                    "        1. Lead: User.model.js (establishes model structure)\n"
                    "        2. Followers: Product.model.js, Order.model.js\n"
                    "    - Controllers:\n"
                    "        1. Lead: BaseController.py (defines controller patterns)\n"
                    "        2. Followers: UserController.py, ProductController.py\n"
                    "    - CSS:\n"
                    "        1. Lead: global.css (establishes styling conventions)\n"
                    "        2. Followers: components.css, pages.css\n"
                    "    - Tests:\n"
                    "        1. Lead: user.test.js (establishes testing patterns)\n"
                    "        2. Followers: product.test.js, order.test.js\n"
                    "    - APIs:\n"
                    "        1. Lead: users.api.js (defines API patterns)\n"
                    "        2. Followers: products.api.js, orders.api.js\n"
                    "    - Database:\n"
                    "        1. Lead: users.schema.sql (establishes schema patterns)\n"
                    "        2. Followers: products.schema.sql, orders.schema.sql\n"
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
                "content": f"Create a grouped task list following Pyramid architecture using only files from:\n{file_list} - MUST Only include files from the provided 'file_list' for all task, no exception\n\nPrioritize grouping by logical components and system layers (foundation, business logic, integration, UI, etc.). Maximize concurrent execution within groups. Apply the lead-follow principle across all relevant stacks (e.g., models, views, controllers, HTML, CSS, JS). Place each lead file in its own group to be completed first, with other files in the same stack grouped together when they can be executed concurrently without needing context from other stacks. Group components or layers not directly relevant to each other if they can be executed concurrently, even if they have different tech stacks. Order groups to provide context, adhering to Pyramid principles. Analyze dependencies: if A depends on B, B precedes A, but group independent files together. Each file appears once.\n\nFrontend Group Ordering Rules:\n1. Global Styles First:\n   - Global CSS files (global.css, variables.css) before any other styles\n2. Component Structure Second:\n   - Small component HTML files before their CSS\n   - Main component HTML files after small components\n   - Component CSS files after their HTML\n3. Page Structure Third:\n   - Page HTML files after components\n   - Page CSS files after their HTML\n4. JavaScript Last:\n   - Component scripts after all HTML/CSS\n   - Main scripts after component scripts\n\nOriginal instruction: {instruction}\n\n"
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