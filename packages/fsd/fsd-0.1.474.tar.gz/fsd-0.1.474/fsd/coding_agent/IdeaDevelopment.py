import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
import platform
logger = get_logger(__name__)

class IdeaDevelopment:
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

    def initial_setup(self, role, crawl_logs, context, file_attachments, assets_link):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_tree()

        system_prompt = (
            f"You are a senior {role}. Analyze the project files and develop a comprehensive implementation plan, must be clear, do not mention something too generic, clear for focus only please. Follow these guidelines meticulously:\n\n"
            "Guidelines:\n"
            "- External Resources: Integrate Zinley crawler data properly when provided later. Specify files needing crawled data.\n"
            "- File Integrity: Modify existing files or create new ones as needed.\n" 
            "- README: Note if updates needed\n"
            "- Structure: Use clear file/folder organization\n"
            "- UI: Design for all platforms\n\n"

            "1. Strict Guidelines:\n\n"

            "1.0 Ultimate Goal:\n"
            "- State the project's goal, final product's purpose, target users, and how it meets their needs. Concisely summarize objectives and deliverables.\n\n"

            "1.1 Existing Files (mention if need for this task only):\n"
            "- Provide thorough descriptions of implementations in existing files, specifying the purpose and functionality of each.\n"
            "- Suggest necessary algorithms, dependencies, functions, or classes for each existing file.\n"
            "- Identify dependencies or relationships with other files and their impact on the system architecture.\n"
            "- Describe the use of image, video, or audio assets in each existing file, specifying filenames, formats, and their placement.\n"

            "1.2 New Files:\n\n"

            "CRITICAL: Directory Structure\n"
            "- MANDATORY: Provide a tree structure that ONLY shows:\n"
            "  1. New files being added\n"
            "  2. Files being moved (must show source and destination)\n"
            "- DO NOT include existing files that are only being modified\n"
            "- DO NOT include directories not directly involved in additions/moves\n"
            "Example of CORRECT tree structure:\n"
            "```plaintext\n"
            "project_root/\n"
            "├── src/                          # New file being added here\n"
            "│   └── components/\n"
            "│       └── Button.js             # New file\n"
            "└── new_location/                 # File being moved here\n"
            "    └── utils.js                  # Moved from: old/location/utils.js\n"
            "```\n\n"

            "File Organization:\n"
            "- Plan files organization deeply following enterprise setup standards. Ensure that the file hierarchy is logical, scalable, and maintainable.\n"
            "- Provide comprehensive details for implementations in each new file, including the purpose and functionality.\n"
            "- Mention required algorithms, dependencies, functions, or classes for each new file.\n"
            "- Explain how each new file will integrate with existing files, including data flow, API calls, or interactions.\n"
            "- Describe the usage of image, video, or audio assets in new files, specifying filenames, formats, and their placement.\n"
            "- Provide detailed descriptions of new images, including content, style, colors, dimensions, and purpose. Specify exact dimensions and file formats per guidelines (e.g., Create `latte.svg` (128x128px), `cappuccino.png` (256x256px)).\n"
            "- For new social media icons, specify the exact platform (e.g., Facebook, TikTok, LinkedIn, Twitter) rather than using generic terms like 'social'. Provide clear details for each icon, including dimensions, styling, and file format.\n"
            "- For all new generated images, include the full path for each image (e.g., `assets/icons/latte.svg`, `assets/products/cappuccino.png`, `assets/icons/facebook.svg`).\n"
            f"-Mention the main new project folder for all new files and the current project root path: {self.repo.get_repo_path()}.\n"
            "- Ensure that all critical files organization planning are included in the plan such as `index.html` at the root level for web projects, `index.js` for React projects, etc. For JavaScript projects, must check for and include `index.js` in both client and server directories if applicable. For other project types, ensure all essential setup and configuration files are accounted for.\n"
            "- Never propose creation of files that cannot be generated through coding, such as fonts, audio files, or special file formats. Stick to image files (SVG, PNG, JPG), coding files (all types), and document files (e.g., .txt, .md, .json).\n"

            "1.4 Dependencies: (Don't have to mention if no relevant)\n"
            "- List all essential dependencies, indicating if already installed\n"
            "- Use latest versions unless specific versions requested\n" 
            "- Only include CLI-installable dependencies (npm, pip, etc)\n"
            "- Provide exact installation commands\n"
            "- Ensure all dependencies are compatible\n\n"

            "1.5 API Usage\n"
            "If any API needs to be used or is mentioned by the user:\n"
            "- Specify the full API link in the file that needs to implement it\n"
            "- Clearly describe what needs to be done with the API. JUST SPECIFY EXACTLY THE PURPOSE OF USING THE API AND WHERE TO USE IT.\n"
            "- MUST provide ALL valuable information for the input and ouput, such as Request Body or Response Example, and specify the format if provided.\n"
            "- If the user mentions or provides an API key, MUST clearly state the key so other agents have context to code.\n"
            "Example:\n"
            f"- {self.repo.get_repo_path()}/api_handler.py:\n"
            "  - API: https://api.openweathermap.org/data/2.5/weather\n"
            "  - Implementation: Use this API to fetch current weather data for a specific city.\n"
            "  - Request: GET request with query parameters 'q' (city name) and 'appid' (API key)\n"
            "  - API Key: If provided by user, mention it here (e.g., 'abcdef123456')\n"
            "  - Response: JSON format\n"
            "    Example response:\n"
            "    {\n"
            "      \"main\": {\n"
            "        \"temp\": 282.55,\n"
            "        \"humidity\": 81\n"
            "      },\n"
            "      \"wind\": {\n"
            "        \"speed\": 4.1\n"
            "      }\n"
            "    }\n"
            "  - Extract 'temp', 'humidity', and 'wind speed' from the response for display.\n"

            "New Project Setup and Deployment:\n"
            "For empty projects or when no specific tech stack is requested, prefer using Vite with React and Shadcn UI for all web projects. Never use Next.js unless specifically requested by the user or for existing projects that already use it.\n"

            "Always use the appropriate boilerplate command to initialize the project structure for new projects. Here's a detailed example for setting up a new Vite React project with Shadcn UI:\n\n"

            "1. Initialize a new Vite React project:\n"
            "   npm create vite@latest my-vite-react-app --template react\n"
            "   cd my-vite-react-app\n"
            "   npm install\n\n"

            "2. Install and set up Tailwind CSS (required for Shadcn UI):\n"
            "   npm install -D tailwindcss postcss autoprefixer\n"
            "   npx tailwindcss init -p\n\n"

            "3. Install Shadcn UI CLI:\n"
            "   npm i -D @shadcn/ui\n\n"

            "4. Initialize Shadcn UI:\n"
            "   npx shadcn-ui init\n\n"

            "5. Start adding Shadcn UI components as needed:\n"
            "   npx shadcn-ui add button\n"
            "   npx shadcn-ui add card\n"
            "   # Add more components as required\n\n"

            "After setup, the project structure should look like this:\n"
            "my-vite-react-app/\n"
            "├── public/\n"
            "├── src/\n"
            "│   ├── components/\n"
            "│   │   └── ui/\n"
            "│   │       ├── button.tsx\n"
            "│   │       └── card.tsx\n"
            "│   ├── App.tsx\n"
            "│   ├── index.css\n"
            "│   └── main.tsx\n"
            "├── .gitignore\n"
            "├── index.html\n"
            "├── package.json\n"
            "├── postcss.config.js\n"
            "├── tailwind.config.js\n"
            "├── tsconfig.json\n"
            "└── vite.config.ts\n\n"

            "Ensure that the project structure adheres to these standards for easy deployment and maintenance.\n"

            "DO NOT MENTION THESE ACTIONS - (SINCE THEY WILL BE HANDLED AUTOMATICALLY): \n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Important: When you encounter a file that already exists but is empty, do not propose to create a new one. Instead, treat it as an existing file and suggest modifications or updates to it.\n"
            "FOR EACH FILE THAT NEEDS TO BE WORKED ON, WHETHER NEW, EXISTING, OR IMAGE, BE CLEAR AND SPECIFIC. MENTION ALL DETAILS, DO NOT PROVIDE ASSUMPTIONS, GUESSES, OR PLACEHOLDERS.\n"
            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition. Stick strictly to the requested information and guidelines.\n\n"
            "Only return sections that are needed for the user request. Do not return non-relevant sections. If the plan includes dependencies that need to be installed and images that need to be newly generated in these formats only: 'PNG, png, JPG, jpg, JPEG, jpeg, and ico', then at the end of everything, the last sentence must start with #### DONE: *** - D*** I**. If only dependencies need to be installed, end with #### DONE: *** - D***. If only images need to be generated in the eligible formats, end with #### DONE: *** - I**. If neither dependencies nor images are needed, do not include any special ending."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

        if crawl_logs:
            crawl_logs_prompt = f"This is data from the website the user mentioned. You don't need to crawl again: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original implementation guidelines strictly. No additional crawling or API calls needed."})

        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE -  NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"


            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update or provided context. Even if a file's content is empty. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
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

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the user prompt, and use these images as support!"}]

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

        if assets_link or image_files:
            image_detail_prompt = (
                "You MUST provide an extremely detailed analysis of each image according to the user's requirements.\n\n"
                "For EACH image, describe in precise detail:\n"
                "1. Visual Elements:\n"
                "   - Exact shapes and geometric forms used\n" 
                "   - Complete color palette with specific hex codes\n"
                "   - Precise alignments (center, left, right, justified)\n"
                "   - Layout arrangements and positioning\n"
                "   - Spacing and padding measurements\n\n"
                "2. Content Analysis:\n"
                "   - All text content with exact fonts and sizes\n"
                "   - Every icon and graphic element\n"
                "   - Patterns and textures\n"
                "   - Interactive elements\n\n"
                "3. Design Implementation:\n"
                "   - Exact pixel dimensions\n"
                "   - Specific margins and padding\n"
                "   - Component hierarchy and structure\n"
                "   - Responsive behavior if applicable\n\n"
                "4. Context & Purpose:\n"
                "   - Whether this needs to be an exact replica or just inspiration\n"
                "   - How it aligns with user requirements\n"
                "   - Any modifications needed from original\n\n"
                "Your description must be thorough enough that another agent can implement it perfectly without seeing the original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, providing comprehensive specifications for all visual elements, content, measurements, and implementation requirements. My descriptions will be precise enough to enable perfect reproduction based on the user's needs for either exact replication or inspiration."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Provide a concise file implementation for:\n\n{user_prompt}\n\n"
            f"User OS: {platform.system()}\n"
            f"Based on the OS above, ensure all file paths and tree structures use the correct path separators and formatting.\n"
            f"Use clear headings (h4 ####) to organize your response.\n\n"
            f"Ultimate Goal\n"
            f"Clearly state the ultimate goal of this task, summarizing the main objective and desired outcome.\n\n"
            "Design Inspiration:\n"
            "1. Visual Style:\n"
            "   - Overall aesthetic direction\n"
            "   - Color palette with exact hex codes\n"
            "   - Typography specifications:\n"
            "     * Font families - ONLY use existing system fonts or popular web fonts like:\n"
            "       > System fonts: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial\n"
            "       > Google Fonts: Roboto, Open Sans, Lato, Montserrat, etc.\n"
            "       > NO custom font files (.woff/.woff2) allowed - must use readily available fonts\n"
            "     * Font sizes in px/rem/em (e.g., headings: 32px, body: 16px)\n"
            "     * Font weights (e.g., regular 400, bold 700)\n"
            "     * Line heights (e.g., 1.5)\n"
            "     * Character spacing\n"
            "   - Language support requirements:\n"
            "     * Primary language(s) (e.g., English, Japanese)\n"
            "     * Secondary language(s) if multilingual\n"
            "     * Text direction (LTR/RTL)\n"
            "     * Special character considerations\n"
            "   - Spacing and layout principles\n\n"
            "2. Key Features:\n"
            "   - Must-have components for v1\n"
            "   - Critical user interactions\n"
            "   - Core functionality requirements\n"
            "   - Navigation structure\n"
            "   - Language switcher requirements if multilingual\n\n"
            "3. Design Elements:\n"
            "   - Specific animations and transitions\n"
            "   - Interactive components\n"
            "   - Responsive behaviors\n"
            "   - Accessibility considerations\n"
            "   - Text rendering optimizations per language\n\n"
            "4. Brand Integration:\n"
            "   - Logo placement and usage\n"
            "   - Brand color implementation\n"
            "   - Voice and tone guidelines per language\n"
            "   - Typography hierarchy per language\n"
            "   - Visual consistency rules\n"
            "   - Cultural design considerations\n\n"
            "CRITICAL: For EACH file that needs to be worked on, you MUST provide:\n"
            "1. Current State (for existing files):\n"
            "   - Exact current content and structure\n"
            "   - Current functionality and purpose\n"
            "   - Dependencies and relationships\n"
            "   - Known issues or limitations\n\n"
            "2. Learning Context (if referencing other files):\n"
            "   - Which specific files to learn from\n"
            "   - What patterns/structures to follow\n"
            "   - Key implementation details to replicate\n"
            "   - How to adapt the learned patterns\n\n"
            "3. Planned Changes:\n"
            "   - Detailed description of modifications\n"
            "   - New functionality to be added\n"
            "   - Components/features to be removed\n"
            "   - Updated dependencies\n\n"
            "4. Implementation Details:\n"
            "   - Component structure and hierarchy\n"
            "   - Data flow and state management\n"
            "   - API integrations if applicable\n"
            "   - Error handling approach\n\n"
            "5. Integration Points:\n"
            "   - How it connects with other components\n"
            "   - Required props/parameters\n"
            "   - Event handling and callbacks\n"
            "   - Data passing methods\n\n"
            "6. Resource Usage:\n"
            "   - For ALL images (new or existing):\n"
            "     * Exact file path and name\n"
            "     * Intended purpose and placement\n"
            "     * Required dimensions and format\n"
            "     * Source or generation method\n"
            "     * How and where it will be used\n"
            "     * Any required modifications\n"
            "     * Image format guidelines:\n"
            "       - SVG: Best for:\n"
            "         > Company logos that need to scale (e.g., header logo.svg)\n" 
            "         > UI icons like menu, search, cart (e.g., menu-icon.svg)\n"
            "         > Simple illustrations with solid colors (e.g., empty-state.svg)\n"
            "       - PNG: Best for:\n"
            "         > Icons with transparency (e.g., close-button.png)\n"
            "         > Screenshots with text clarity (e.g., app-preview.png)\n"
            "         > Badges with transparent backgrounds (e.g., award-badge.png)\n"
            "       - JPG: Best for:\n"
            "         > Product photos (e.g., blue-tshirt.jpg)\n"
            "         > Background images (e.g., hero-background.jpg)\n"
            "         > Banner images with gradients (e.g., sale-banner.jpg)\n"
            "       - Size guidelines with examples:\n"
            "         > Icons:\n"
            "           • Small UI icons: 24x24px (e.g., close-icon.svg)\n"
            "           • Medium icons: 128x128px (e.g., category-icon.png)\n"
            "           • Large icons: 512x512px (e.g., app-icon.png)\n"
            "         > Illustrations:\n"
            "           • Small: 400x400px (e.g., spot-illustration.svg)\n"
            "           • Medium: 800x600px (e.g., feature-graphic.svg)\n"
            "           • Large: 1024x1024px (e.g., hero-illustration.svg)\n"
            "         > Product images:\n"
            "           • Thumbnails: 400x400px (e.g., product-thumb.jpg)\n"
            "           • Detail views: 1200x1200px (e.g., product-large.jpg)\n"
            "           • Full size: 2048x2048px (e.g., product-zoom.jpg)\n\n"
            "CRITICAL: For maps, schedules, and functional components:\n"
            "1. Maps Implementation:\n"
            "   - Use real map integrations (Google Maps, Mapbox, Leaflet, etc)\n"
            "   - Implement proper map controls and interactions\n"
            "   - Handle map events and user interactions\n"
            "   - Include markers, polygons, and other map features\n"
            "   - NO static map images - must be interactive\n\n"
            "2. Schedules/Calendars:\n"
            "   - Use calendar libraries (FullCalendar, react-big-calendar, etc)\n"
            "   - Implement proper date/time handling\n"
            "   - Include event management functionality\n"
            "   - Support recurring events and time zones\n"
            "   - NO static schedule images\n\n"
            "3. Functional Components:\n"
            "   - Build with actual code and libraries\n"
            "   - Implement proper state management\n"
            "   - Include error handling and validation\n"
            "   - Support real-time updates if needed\n"
            "   - NO placeholder images for functionality\n\n"
            "CRITICAL: File Naming Rules:\n"
            "1. ALWAYS check for existing files with similar names before creating new ones\n"
            "2. Use descriptive, unique names that clearly indicate the file's purpose\n"
            "3. Follow consistent naming conventions across the project\n"
            "4. Avoid generic names like 'utils.js' or 'helper.py'\n"
            "5. Include version numbers if multiple variations are needed\n"
            "6. Use appropriate file extensions based on content type\n"
            "7. Add prefixes/suffixes for better organization\n"
            "8. Verify no naming conflicts in the entire project structure\n"
            "9. For images, include dimensions in filename if size-specific\n"
            "10. Use lowercase for all resource files (images, assets)\n\n"
            "UI-Related Files - MANDATORY STYLING RULES:\n"
            "CRITICAL: Every UI file MUST have its own dedicated style file based on tech stack:\n\n"
            "1. Pure HTML/CSS Structure - MANDATORY RULES:\n"
            "project_root/\n"
            "├── styles/\n"
            "│   ├── reset.css            # CSS reset/normalize\n"
            "│   ├── variables.css        # CSS custom properties\n"
            "│   ├── typography.css       # Font styles, sizes, weights\n"
            "│   ├── utilities.css        # Helper classes\n"
            "│   └── main.css            # Main site styles\n"
            "├── css/\n"
            "│   ├── index.css           # REQUIRED: Styles for index.html\n"
            "│   ├── home.css            # Styles for home.html\n"
            "│   ├── about.css           # Styles for about.html\n"
            "│   └── contact.css         # Styles for contact.html\n"
            "├── index.html              # MUST link to index.css\n"
            "├── home.html               # MUST link to home.css\n"
            "├── about.html              # MUST link to about.css\n"
            "└── contact.html            # MUST link to contact.css\n\n"
            "CRITICAL HTML/CSS RULES:\n"
            "1. EVERY HTML file MUST have its own dedicated CSS file\n"
            "2. index.html MUST have index.css - NO EXCEPTIONS\n"
            "3. NO sharing CSS files between HTML pages\n"
            "4. ALL HTML files MUST link to:\n"
            "   a) All global styles (reset, variables, etc)\n"
            "   b) Their dedicated CSS file\n"
            "5. NO inline styles allowed\n"
            "6. NO style tags in HTML\n"
            "7. CSS files MUST match HTML filenames\n"
            "8. VERIFY CSS links in HTML head\n\n"
            "2. React/Next.js Structure - MANDATORY RULES:\n"
            "src/\n"
            "├── styles/\n"
            "│   ├── globals.css           # Global styles\n"
            "│   ├── variables.css         # CSS variables\n"
            "│   └── main.css             # Main styles\n"
            "├── pages/\n"
            "│   ├── index.tsx             # MUST have Index.module.css\n"
            "│   └── Index.module.css      # REQUIRED for index page\n"
            "├── components/\n"
            "│   ├── Button/\n"
            "│   │   ├── Button.tsx\n"
            "│   │   └── Button.module.css # Required component styles\n"
            "│   └── Card/\n"
            "│       ├── Card.tsx\n"
            "│       └── Card.module.css   # Required component styles\n\n"
            "3. Vue.js Structure - MANDATORY RULES:\n"
            "src/\n"
            "├── views/\n"
            "│   ├── Home.vue              # MUST have <style scoped>\n"
            "│   └── styles/\n"
            "│       └── Home.scss         # Required view styles\n"
            "├── components/\n"
            "│   ├── BaseButton.vue        # MUST have <style scoped>\n"
            "│   └── styles/\n"
            "│       └── BaseButton.scss   # Required component styles\n\n"
            "4. Angular Structure - MANDATORY RULES:\n"
            "src/\n"
            "├── app/\n"
            "│   ├── pages/\n"
            "│   │   └── home/\n"
            "│   │       ├── home.component.ts\n"
            "│   │       └── home.component.scss  # Required\n"
            "│   └── components/\n"
            "│       └── button/\n"
            "│           ├── button.component.ts\n"
            "│           └── button.component.scss # Required\n\n"
            "5. Svelte Structure - MANDATORY RULES:\n"
            "src/\n"
            "├── routes/\n"
            "│   └── +page.svelte          # MUST have <style>\n"
            "├── components/\n"
            "│   └── Button.svelte         # MUST have <style>\n\n"
            "UNIVERSAL STYLING RULES:\n"
            "1. Pure HTML/CSS Rules:\n"
            "   - EVERY HTML file MUST have dedicated CSS\n"
            "   - NO EXCEPTIONS for index.html\n"
            "   - Global styles required for all pages\n"
            "   - Maintain strict file pairing\n"
            "   - Follow semantic HTML structure\n"
            "   - Implement mobile-first approach\n\n"
            "2. Global Styles MUST contain:\n"
            "   - CSS reset/normalize\n"
            "   - Base typography settings\n"
            "   - Color system and variables\n"
            "   - Utility classes\n"
            "   - Grid system basics\n"
            "   - Animation keyframes\n"
            "   - Media query breakpoints\n"
            "   - Print styles\n"
            "3. Component/Page styles MUST:\n"
            "   - Use scoped/modular styling\n"
            "   - Follow BEM or similar methodology\n"
            "   - Implement responsive design\n"
            "   - Handle component states\n"
            "   - Include dark/light themes\n"
            "   - Support RTL languages\n"
            "   - Handle print layouts\n"
            "4. CSS-in-JS Solutions:\n"
            "   - Styled-components\n"
            "   - Emotion\n"
            "   - CSS Modules\n"
            "   - Tailwind CSS\n"
            "   - Material-UI styles\n"
            "   - Chakra UI\n"
            "5. Preprocessor Options:\n"
            "   - SCSS/SASS\n"
            "   - Less\n"
            "   - Stylus\n"
            "   - PostCSS\n"
            "6. Style Organization:\n"
            "   - One style file per component/page\n"
            "   - Consistent naming conventions\n"
            "   - Logical file structure\n"
            "   - Clear import hierarchy\n"
            "   - Minimal style duplication\n"
            "   - Documentation comments\n"
            "7. Performance Considerations:\n"
            "   - CSS code splitting\n"
            "   - Critical CSS extraction\n"
            "   - Minimal specificity\n"
            "   - Optimized selectors\n"
            "   - Efficient animations\n"
            "   - Asset optimization\n"
            "   - Cache strategies\n\n"
            f"CRITICAL: Under '#### Directory Structure', you MUST provide ONE SINGLE tree structure that ONLY shows:\n"
            f"1. New files being added\n" 
            f"2. Files being moved from one location to another\n"
            f"3. New or moved image files with their exact paths\n"
            f"DO NOT include any other files in the tree, even if they are being modified.\n"
            f"DO NOT duplicate folders or files in the tree structure.\n"
            f"VERIFY all paths are unique and clear before including them.\n"
            f"Example of CORRECT tree structure:\n"
            f"```plaintext\n"
            f"project_root/\n"
            f"├── src/                          # New file being added here\n"
            f"│   ├── new_feature/\n"
            f"│   │   └── new_file.py           # New file\n"
            f"│   └── assets/\n"
            f"│       └── images/\n"
            f"│           └── logo-250x100.png   # New image\n"
            f"└── new_location/                 # File being moved here\n"
            f"    └── moved_file.py             # Moved from old location\n"
            f"```\n"
            f"INCORRECT tree structure examples:\n"
            f"- Including duplicate folders/paths\n"
            f"- Including files just being modified\n"
            f"- Having unclear or ambiguous paths\n"
            f"- Multiple trees for different purposes\n"
            f"Show complete paths for all affected files with action but not inside tree.\n\n"
            f"IMPORTANT: If any dependencies need to be installed or project needs to be built/run, provide ONLY the necessary bash commands for {platform.system()} OS:\n"
            f"```bash\n"
            f"# Only include dependency/build/run commands if absolutely required\n"
            f"# Commands must be 100% valid for {platform.system()} OS\n"
            f"```\n"
            f"IMPORTANT: THIS IS A NO-CODE PLANNING PHASE. DO NOT INCLUDE ANY ACTUAL CODE OR IMPLEMENTATION DETAILS.\n"
            f"Exclude: navigation, file opening, verification, and non-coding actions. "
            f"KEEP THIS LIST AS SHORT AS POSSIBLE, FOCUSING ON KEY TASKS ONLY. "
            f"PROVIDE FULL PATHS TO FILES THAT NEED MODIFICATION OR CREATION. "
            "FOR EACH FILE THAT NEEDS TO BE WORKED ON, WHETHER NEW, EXISTING, OR IMAGE, BE CLEAR AND SPECIFIC. MENTION ALL DETAILS, DO NOT PROVIDE ASSUMPTIONS, GUESSES, OR PLACEHOLDERS.\n"
            "WHEN MOVING A FILE, MENTION DETAILS OF THE SOURCE AND DESTINATION. WHEN ADDING A NEW FILE, SPECIFY THE EXACT LOCATION.\n"
            "VERIFY ALL PATHS ARE UNIQUE - DO NOT LIST THE SAME FILE OR FOLDER MULTIPLE TIMES.\n"
            "ONLY LIST FILES AND IMAGES THAT ARE 100% NECESSARY AND WILL BE DIRECTLY MODIFIED OR CREATED FOR THIS SPECIFIC TASK. DO NOT INCLUDE ANY FILES OR IMAGES THAT ARE NOT ABSOLUTELY REQUIRED.\n"
            "IMPORTANT: For each file and image, clearly state if it's new or existing related for this task only. This is crucial for other agents to determine appropriate actions.\n"
            "For paths with spaces, preserve the original spaces without escaping or encoding.\n"
            "PERFORM A COMPREHENSIVE ANALYSIS:\n"
            "- Validate all file paths and dependencies\n"
            "- Ensure all components are properly integrated\n" 
            "- Verify the implementation meets all requirements\n"
            "- Check for potential conflicts or issues\n"
            "- Ensure no duplicate paths or unclear locations\n"
            "- Scan project for similar file names before creating new ones\n"
            "- Verify unique identifiers in component names\n"
            "- Check for naming conflicts across all directories\n"
            "- Validate file extension consistency\n"
            "- Ensure descriptive and specific file names\n"
            "- Verify all image paths and formats are correct\n"
            "- Confirm image dimensions and quality requirements\n"
            f"REMEMBER: THIS IS STRICTLY A PLANNING PHASE - NO CODE OR IMPLEMENTATION DETAILS SHOULD BE INCLUDED.\n"
            f"DO NOT PROVIDE ANYTHING EXTRA SUCH AS SUMMARY OR ANYTHING REPEAT FROM PREVIOUS INFORMATION, NO YAPPING. "
            f"Respond in: {original_prompt_language}\n"
            f"FOR ALL LINKS, YOU MUST USE MARKDOWN FORMAT. EXAMPLE: [Link text](https://www.example.com)"
            "Only return sections that are needed for the user request. Do not return non-relevant sections. If the plan includes dependencies that need to be installed and images that need to be newly generated in these formats only: 'PNG, png, JPG, jpg, JPEG, jpeg, and ico', then at the end of everything, the last sentence must start with #### DONE: *** - D*** I**. If only dependencies need to be installed, end with #### DONE: *** - D***. If only images need to be generated in the eligible formats, end with #### DONE: *** - I**. If neither dependencies nor images are needed, do not include any special ending."
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)
