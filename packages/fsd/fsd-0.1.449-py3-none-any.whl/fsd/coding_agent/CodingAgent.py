import os
import sys
from datetime import datetime
import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class CodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, crawl_logs, file_attachments, assets_link):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### The `CodingAgent` is initializing setup with provided instructions and context")

        prompt = f"""You are an expert software engineer. Follow these guidelines strictly when responding to instructions:

                **Response Guidelines:**
                1. Use ONLY the following SEARCH/REPLACE block format for ALL code changes, additions, or deletions:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. CRITICAL: The SEARCH section MUST match the existing code with EXACT precision - every character, whitespace, indentation, newline, and comment must be identical.

                4. For large files, focus on relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. MUST break complex changes or large files into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of SEARCH/REPLACE blocks. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                9. CRITICAL: Never include code markdown formatting, syntax highlighting, or any other decorative elements. Code must be provided in its raw form.

                10. STRICTLY FORBIDDEN: Do not hallucinate, invent, or make assumptions about code. Only provide concrete, verified code changes based on the actual codebase.

                11. MANDATORY: Code must be completely plain without any formatting, annotations, explanations or embellishments. Only pure code is allowed.

                Remember: Your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.

        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Development plan: {instructions['Implementation_plan']} and original raw request, use if Implementation_plan missing some pieces: {instructions['original_prompt']}"},
            {"role": "assistant", "content": "Understood!"},
            {"role": "user", "content": f"Current working file: {context}"},
            {"role": "assistant", "content": "Understood!"},
        ]

        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this context when implementing changes."})

        if crawl_logs:
            self.conversation_history.append({"role": "user", "content": f"This is supported data for this entire process, use it if appropriate: {crawl_logs}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        all_attachment_file_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            self.conversation_history.append({"role": "user", "content": f"User has attached these files for you, use them appropriately: {all_attachment_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the original Development plan, and use these images as support!"}]

        # Add image files to the user content
        for base64_image in image_files:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": message_content})
        self.conversation_history.append({"role": "assistant", "content": "Understood."})



    async def get_coding_request(self, file, techStack):
        """
        Get coding response for the given instruction and context from Azure OpenAI.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The specific task or instruction for coding.

        Returns:
            str: The code response.
        """
        file_name = os.path.basename(file)
        is_svg = file_name.lower().endswith('.svg')

        # Read current file content
        current_file_content = read_file_content(file)
        if current_file_content:
            self.conversation_history.append({"role": "user", "content": f"Here is the current content of {file_name} that needs to be updated:\n{current_file_content}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this file content as context for the updates."})

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

        user_prompt = f"As a world-class, highly experienced {'SVG designer' if is_svg else f'{techStack} developer'}, implement the following task with utmost efficiency and precision:\n"

        if is_svg:
            user_prompt += (
                "Create SVG that matches project's existing visual style and use case.\n"
                "For brand assets and vector graphics:\n"
                "- Keep official colors, proportions and brand identity intact\n"
                "- Follow brand guidelines strictly and maintain visual consistency\n"
                "- Optimize SVG code for performance and file size\n"
                "- Ensure cross-browser compatibility and responsiveness\n"
                "- Use semantic element names and proper grouping\n"
                "- Include ARIA labels and accessibility attributes\n"
                "- Implement smooth animations and transitions if needed\n"
            )
        else:
            user_prompt += (
                f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}\n"
                "For UI/UX Implementation:\n"
                "- Create stunning, elegant and clean designs:\n"
                "  • Use consistent spacing and padding throughout\n"
                "  • Follow visual hierarchy principles\n"
                "  • Implement proper whitespace and breathing room\n"
                "  • Ensure pixel-perfect alignment and positioning\n"
                "  • Use balanced color schemes and typography\n"
                "  • Create smooth visual flow and transitions\n"
                "- ABSOLUTELY CRITICAL: Resource Loading & Path Resolution:\n"
                "  • Web Resource Loading:\n"
                "    - Always use type attribute for stylesheets: <link href='style.css' rel='stylesheet' type='text/css'>\n"
                "    - Proper protocol for external resources: https:// not //\n"
                "    - No local file:// URLs - use relative or absolute paths\n"
                "    - Correct MIME types: text/css, text/javascript, image/png etc\n"
                "    - Proper nonce/integrity attributes for CDN resources\n"
                "  • Import Resolution:\n"
                "    - Use absolute imports from project root\n"
                "    - Follow consistent import patterns\n"
                "    - Handle circular dependencies\n"
                "  • Path Resolution:\n"
                "    - Use proper path aliases (@/, ~/, etc)\n"
                "    - Handle cross-platform path separators\n"
                "    - Resolve relative vs absolute paths\n"
                "    - Never use file:// protocol for local resources\n"
                "  • Component Integration:\n"
                "    - Match existing component structure\n"
                "    - Follow established naming conventions\n"
                "    - Maintain consistent prop interfaces\n"
                "  • Layout Integration:\n"
                "    - Use shared layout components\n"
                "    - Maintain consistent page structure\n"
                "    - Handle responsive breakpoints\n"
                "  • Style Integration:\n"
                "    - Import shared style modules/themes\n"
                "    - Follow CSS/SCSS naming conventions\n"
                "    - Use design tokens consistently\n"
                "- MANDATORY: Asset Integration:\n"
                "  • Web:\n"
                "    - Use correct public/ or static/ paths\n"
                "    - Never use file:// URLs for local assets\n"
                "    - Always specify width/height for images\n"
                "    - Use proper <picture> and srcset for responsive images\n"
                "    - Implement proper CDN configurations with SRI hashes\n"
                "    - Handle image optimization and lazy loading\n"
                "    - Example:\n"
                "      <link href='/css/styles.css' rel='stylesheet' type='text/css'>\n"
                "      <script src='/js/app.js' type='text/javascript'></script>\n"
                "      <img src='/images/logo.png' width='200' height='100' alt='Logo'>\n"
                "  • iOS:\n"
                "    - Asset catalogs (.xcassets) for images\n"
                "    - Bundle.main.path(forResource:) for local files\n"
                "    - SF Symbols integration with proper scaling\n"
                "    - Example:\n"
                "      if let path = Bundle.main.path(forResource: 'data', ofType: 'json') {\n"
                "          let url = URL(fileURLWithPath: path)\n"
                "      }\n"
                "  • Android:\n"
                "    - res/drawable organization with proper densities\n"
                "    - Vector drawables with compat support\n"
                "    - Resource qualifiers for different configs\n"
                "    - Example:\n"
                "      context.resources.openRawResource(R.raw.data)\n"
                "      ContextCompat.getDrawable(context, R.drawable.icon)\n"
                "  • Desktop:\n"
                "    - Bundle resources with proper paths\n"
                "    - System theme integration\n"
                "    - High DPI assets with scaling\n"
                "    - Example (Electron):\n"
                "      const path = require('path')\n"
                "      path.join(__dirname, 'assets', 'icon.png')\n"
                "- CRITICAL: Common Components Integration:\n"
                "  • Headers/Navigation:\n"
                "    - Web: <header>, nav components, breadcrumbs\n"
                "    - iOS: UINavigationBar, UITabBar\n"
                "    - Android: Toolbar, BottomNavigationView\n"
                "    - Desktop: MenuBar, Ribbon\n"
                "  • Footers:\n"
                "    - Web: <footer>, sticky footers\n"
                "    - Mobile: TabBar, BottomSheet\n"
                "    - Desktop: StatusBar, Dock\n"
                "  • Sidebars/Drawers:\n"
                "    - Web: Collapsible panels, off-canvas\n"
                "    - Mobile: DrawerLayout, SideMenu\n"
                "    - Desktop: DockPanel, SplitView\n"
                "  • Product Cards/Lists:\n"
                "    - Web: Grid/List views with proper styling\n"
                "    - Mobile: RecyclerView/UICollectionView with styles\n"
                "    - Desktop: DataGrid/ListView with themes\n"
                "  • Forms/Input:\n"
                "    - Web: Styled form controls with validation\n"
                "    - Mobile: Native input fields with themes\n"
                "    - Desktop: Themed input controls\n"
                "  • Modals/Dialogs:\n"
                "    - Web: Styled modal windows/popups\n"
                "    - Mobile: Native alert dialogs/sheets\n"
                "    - Desktop: Themed dialog windows\n"
                "- REQUIRED: Framework-Specific Integration:\n"
                "  • React/Next.js:\n"
                "    - _app.js/_app.tsx layout structure\n"
                "    - pages/ directory routing\n"
                "    - Link component with proper href\n"
                "    - Example:\n"
                "      import Image from 'next/image'\n"
                "      <Image src='/logo.png' width={200} height={100} alt='Logo' />\n"
                "  • Vue/Nuxt:\n"
                "    - layouts/ directory usage\n"
                "    - Nested router-view\n"
                "    - Example:\n"
                "      <NuxtImg src='/images/logo.png' width='200' height='100' />\n"
                "  • Angular:\n"
                "    - Module organization\n"
                "    - Router configuration\n"
                "    - Example:\n"
                "      <img [src]='assets/logo.png' width='200' height='100' alt='Logo'>\n"
                "  • Svelte/SvelteKit:\n"
                "    - routes/ structure\n"
                "    - Layout components\n"
                "    - Example:\n"
                "      <img src='$lib/images/logo.png' alt='Logo'>\n"
                "  • iOS:\n"
                "    - UIKit view hierarchy\n"
                "    - SwiftUI view composition\n"
                "    - Example:\n"
                "      Image('logo').resizable().frame(width: 200, height: 100)\n"
                "  • Android:\n"
                "    - Activity/Fragment lifecycle\n"
                "    - Navigation component\n"
                "    - Example:\n"
                "      <ImageView android:src='@drawable/logo' />\n"
                "  • Rust/Tauri:\n"
                "    - Window management\n"
                "    - IPC commands\n"
                "    - Example:\n"
                "      tauri::WindowBuilder::new('label', 'index.html')\n"
                "- Follow UI/UX standards for each tech stack:\n"
                "  • Web: Use semantic HTML5, ARIA, CSS Grid/Flexbox\n"
                "  • React/Vue: Component-based architecture, hooks/composition API\n"
                "  • Mobile: Follow iOS/Material Design guidelines\n"
                "  • Desktop: Use native UI components and patterns\n"
                "- Create consistent interfaces across platforms:\n"
                "  • Implement responsive/adaptive layouts\n"
                "  • Support mobile, tablet, desktop breakpoints\n"
                "  • Use relative units (rem, em, %) over pixels\n"
                "  • Ensure consistent spacing across viewports\n"
                "  • Maintain visual harmony at all sizes\n"
                "- Perfect visual details and polish:\n"
                "  • Precise padding and margins using design system\n"
                "  • Consistent component spacing and alignment\n"
                "  • Proper visual rhythm and balance\n"
                "  • Refined typography and font scaling\n"
                "  • Optimized imagery and icons\n"
                "- Ensure accessibility compliance:\n"
                "  • WCAG 2.1 AA standards\n"
                "  • Proper heading structure and landmarks\n"
                "  • Keyboard navigation and screen readers\n"
                "  • Sufficient color contrast ratios\n"
                "- Optimize performance:\n"
                "  • Lazy loading and code splitting\n"
                "  • Asset optimization and caching\n"
                "  • Virtual scrolling for long lists\n"
                "  • Optimized animations and transitions\n"
                "- Add meaningful interactions:\n"
                "  • Loading states and transitions\n"
                "  • Form validation with clear feedback\n"
                "  • Error handling with recovery options\n"
                "  • Micro-interactions and hover states\n"
                "  • Smooth page transitions\n"
                "- Follow tech stack best practices:\n"
                "  • Web: BEM/SMACSS CSS, Progressive Enhancement\n"
                "  • React: Hooks patterns, Context API usage\n"
                "  • Vue: Composition API, State management\n"
                "  • Mobile: Platform UI guidelines, Native features\n"
                "\nFor Architecture & Code Quality:\n"
                "- Write clean, self-documenting code following DRY/KISS principles\n"
                "- Use meaningful names reflecting domain concepts\n"
                "- Structure code for maximum maintainability (SOLID principles)\n"
                "- Implement proper separation of concerns\n"
                "- Use appropriate design patterns (Factory, Strategy, Observer etc)\n"
                "- Follow clean architecture principles\n"
                "- Add comprehensive documentation\n"
                "\nFor Performance & Reliability:\n"
                "- Optimize algorithmic complexity (time/space)\n"
                "- Implement proper caching strategies\n"
                "- Use efficient data structures\n"
                "- Add comprehensive error handling with recovery\n"
                "- Ensure thread-safety and handle race conditions\n"
                "- Implement retry mechanisms for external services\n"
                "- Add proper logging and monitoring hooks\n"
                "\nFor Security & Data Integrity:\n"
                "- Follow security best practices (OWASP)\n"
                "- Implement proper input validation and sanitization\n"
                "- Use parameterized queries to prevent injection\n"
                "- Add proper authentication/authorization checks\n"
                "- Implement secure session management\n"
                "- Follow principle of least privilege\n"
                "- Ensure data consistency and referential integrity\n"
                "\nFor Testing & Quality Assurance:\n"
                "- Write comprehensive unit tests with good coverage\n"
                "- Add integration and e2e tests where needed\n"
                "- Follow TDD/BDD practices\n"
                "- Include performance and load tests\n"
                "- Add security and penetration tests\n"
                "- Implement proper test data management\n"
                "- Visual regression testing for UI components\n"
                "\nFor Code Correctness & Error Prevention:\n"
                "- Follow strict type checking and validation\n"
                "- Use proper null/undefined checks\n"
                "- Handle all edge cases and error conditions\n"
                "- Validate function parameters and return values\n"
                "- Use TypeScript/static typing where possible\n"
                "- Implement proper error boundaries\n"
                "- Add runtime checks and assertions\n"
                "\nFor Syntax & Language Features:\n"
                "- Use modern language features correctly\n"
                "- Follow language-specific best practices\n"
                "- Implement proper async/await patterns\n"
                "- Use correct module import/export syntax\n"
                "- Follow framework-specific conventions\n"
                "- Use appropriate data structures\n"
                "- Implement proper memory management\n"
                "\nFor Logic & Business Rules:\n"
                "- Validate all business logic thoroughly\n"
                "- Handle all possible states and transitions\n"
                "- Implement proper data validation rules\n"
                "- Add comprehensive error messages\n"
                "- Follow domain-driven design principles\n"
                "- Ensure consistent state management\n"
                "- Add proper logging for debugging\n"
            )

        user_prompt += f"{lazy_prompt}\n" if not is_svg else ""
        user_prompt += f"Providing update for this {file_name}.\n"
        user_prompt += "NOTICE: Your response must ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        self.conversation_history.append({"role": "user", "content": user_prompt})

        try:
            response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
            content = response.choices[0].message.content
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if lines and "> REPLACE" in lines[-1]:
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
            else:
                logger.info(" #### Extending response - generating additional context (1/10)")
                self.conversation_history.append({"role": "assistant", "content": content})
                # The response was cut off, prompt AI to continue
                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                continuation_content = continuation_response.choices[0].message.content
                continuation_lines = [line.strip() for line in continuation_content.splitlines() if line.strip()]

                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                    # Combine the incomplete and continuation responses
                    complete_content = content + continuation_content
                    self.conversation_history = self.conversation_history[:-2]
                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                    return complete_content
                else:
                    logger.info(" #### Extending response - generating additional context (2/10)")
                    content = content + continuation_content
                    self.conversation_history.append({"role": "assistant", "content": content})
                    # The response was cut off, prompt AI to continue
                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                    continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                    continuation_content1 = continuation_response.choices[0].message.content
                    continuation_lines = [line.strip() for line in continuation_content1.splitlines() if line.strip()]

                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                        # Combine the incomplete and continuation responses
                        complete_content = content + continuation_content1
                        self.conversation_history = self.conversation_history[:-4]
                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                        return complete_content
                    else:
                        logger.info(" #### Extending response - generating additional context (3/10)")
                        content = content + continuation_content1
                        self.conversation_history.append({"role": "assistant", "content": content})
                        # The response was cut off, prompt AI to continue
                        continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                        self.conversation_history.append({"role": "user", "content": continuation_prompt})

                        continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                        continuation_content2 = continuation_response.choices[0].message.content
                        continuation_lines = [line.strip() for line in continuation_content2.splitlines() if line.strip()]

                        if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                            # Combine the incomplete and continuation responses
                            complete_content = content + continuation_content2
                            self.conversation_history = self.conversation_history[:-6]
                            self.conversation_history.append({"role": "assistant", "content": complete_content})
                            return complete_content
                        else:
                            logger.info(" #### Extending response - generating additional context (4/10)")
                            content = content + continuation_content2
                            self.conversation_history.append({"role": "assistant", "content": content})
                            continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                            self.conversation_history.append({"role": "user", "content": continuation_prompt})

                            continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                            continuation_content3 = continuation_response.choices[0].message.content
                            continuation_lines = [line.strip() for line in continuation_content3.splitlines() if line.strip()]

                            if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                complete_content = content + continuation_content3
                                self.conversation_history = self.conversation_history[:-8]
                                self.conversation_history.append({"role": "assistant", "content": complete_content})
                                return complete_content
                            else:
                                logger.info(" #### Extending response - generating additional context (5/10)")
                                content = content + continuation_content3
                                self.conversation_history.append({"role": "assistant", "content": content})
                                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                continuation_content4 = continuation_response.choices[0].message.content
                                continuation_lines = [line.strip() for line in continuation_content4.splitlines() if line.strip()]

                                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                    complete_content = content + continuation_content4
                                    self.conversation_history = self.conversation_history[:-10]
                                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                                    return complete_content
                                else:
                                    logger.info(" #### Extending response - generating additional context (6/10)")
                                    content = content + continuation_content4
                                    self.conversation_history.append({"role": "assistant", "content": content})
                                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                    continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                    continuation_content5 = continuation_response.choices[0].message.content
                                    continuation_lines = [line.strip() for line in continuation_content5.splitlines() if line.strip()]

                                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                        complete_content = content + continuation_content5
                                        self.conversation_history = self.conversation_history[:-12]
                                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                                        return complete_content
                                    else:
                                        logger.info(" #### Extending response - generating additional context (7/10)")
                                        content = content + continuation_content5
                                        self.conversation_history.append({"role": "assistant", "content": content})
                                        continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                        self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                        continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                        continuation_content6 = continuation_response.choices[0].message.content
                                        continuation_lines = [line.strip() for line in continuation_content6.splitlines() if line.strip()]

                                        if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                            complete_content = content + continuation_content6
                                            self.conversation_history = self.conversation_history[:-14]
                                            self.conversation_history.append({"role": "assistant", "content": complete_content})
                                            return complete_content
                                        else:
                                            logger.info(" #### Extending response - generating additional context (8/10)")
                                            content = content + continuation_content6
                                            self.conversation_history.append({"role": "assistant", "content": content})
                                            continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                            self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                            continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                            continuation_content7 = continuation_response.choices[0].message.content
                                            continuation_lines = [line.strip() for line in continuation_content7.splitlines() if line.strip()]

                                            if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                                complete_content = content + continuation_content7
                                                self.conversation_history = self.conversation_history[:-16]
                                                self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                return complete_content
                                            else:
                                                logger.info(" #### Extending response - generating additional context (9/10)")
                                                content = content + continuation_content7
                                                self.conversation_history.append({"role": "assistant", "content": content})
                                                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                                continuation_content8 = continuation_response.choices[0].message.content
                                                continuation_lines = [line.strip() for line in continuation_content8.splitlines() if line.strip()]

                                                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                                    complete_content = content + continuation_content8
                                                    self.conversation_history = self.conversation_history[:-18]
                                                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                    return complete_content
                                                else:
                                                    logger.info(" #### Extending response - generating additional context (10/10)")
                                                    content = content + continuation_content8
                                                    self.conversation_history.append({"role": "assistant", "content": content})
                                                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                                    continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                                    continuation_content9 = continuation_response.choices[0].message.content
                                                    continuation_lines = [line.strip() for line in continuation_content9.splitlines() if line.strip()]

                                                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                                        complete_content = content + continuation_content9
                                                        self.conversation_history = self.conversation_history[:-20]
                                                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                        return complete_content
                                                    else:
                                                        complete_content = content + continuation_content9
                                                        self.conversation_history = self.conversation_history[:-20]
                                                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                        logger.error(f"  The `CodingAgent` encountered an error while getting coding request")
                                                        return complete_content

        except Exception as e:
            logger.error(f" The `CodingAgent` encountered an error while getting coding request")
            logger.error(f" {e}")
            raise


    async def get_coding_requests(self, file, techStack):
        """
        Get coding responses for a file from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The coding task prompt.

        Returns:
            str: The code response or error reason.
        """
        return await self.get_coding_request(file, techStack)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        logger.debug("\n #### The `CodingAgent` is clearing conversation history")
        self.conversation_history = []

    def destroy(self):
        """De-initialize and destroy this instance."""
        logger.debug("\n #### The `CodingAgent` is being destroyed")
        self.repo = None
        self.conversation_history = None
        self.ai = None
