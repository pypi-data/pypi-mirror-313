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

class ShortIdeaDevelopment:
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
            f"As a senior {role}, provide a concise, specific plan:\n\n"
            "File Updates\n"
            f"- {self.repo.get_repo_path()}/path/to/file1.ext:\n"
            "  - Update: [1-2 sentences what need to be done here!]\n"
            "  - Reason: [brief justification]\n"
            f"- {{self.repo.get_repo_path()}}/path/to/file2.ext:\n"
            "  - Update: [1-2 sentences what need to be done here!]\n"
            "  - Reason: [brief justification]\n\n"
            "New Files (only if file doesn't exist)\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file1.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file2.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n\n"
            "Directory Structure (MANDATORY - ONLY for new files being added or files being moved):\n"
            "```plaintext\n"
            "project_root/\n"
            "├── path/                         # Only show directories containing new/moved files\n"
            "│   └── to/\n"
            "│       ├── new_file1.ext         # New file\n"
            "│       └── new_file2.ext         # New file\n"
            "└── new_location/                 # Only if files are being moved\n"
            "    └── moved_file.ext            # Moved from: old/path/moved_file.ext\n"
            "```\n"
            "IMPORTANT: Tree structure is MANDATORY but ONLY for:\n"
            "- New files being created\n" 
            "- Files being moved (must show source and destination)\n"
            "DO NOT include existing files that are only being modified in the tree.\n"
            "DO NOT include any files/directories not directly involved in additions/moves.\n\n"
            "Note: If no new files need to be created, omit the 'New Files' section.\n"
            "API Usage\n"
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
            "Asset Integration\n"
            "- Describe usage of image/video/audio assets in new files (filename, format, placement)\n"
            "- For new images: Provide content, style, colors, dimensions, purpose\n"
            "- For social icons: Specify platform (e.g., Facebook, TikTok), details, dimensions, format\n"
            "- Only propose creatable files (images, code, documents). No fonts or audio or video files.\n"

            "Dependencies Required (Only if task requires dependencies):\n"
            "For each file that requires dependencies, specify:\n"
            f"- {self.repo.get_repo_path()}/file_path:\n"
            "  - Existing Dependencies (if found in requirements.txt, package.json, etc):\n"
            "    - dependency_name: Explain specific usage in this file\n"
            "  - New Dependencies (if not found in any dependency files):\n"
            "    - dependency_name: Explain why needed and specific usage\n"
            "    - Version (only if specific version required)\n"
            "Note: Skip this section if task has no dependency requirements\n"

            "DO NOT MENTION THESE ACTIONS - (SINCE THEY WILL BE HANDLED AUTOMATICALLY): \n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Project Setup and Deployment:\n"
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

            "Important: When you encounter a file that already exists but is empty, do not propose to create a new one. Instead, treat it as an existing file and suggest modifications or updates to it.\n"
            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition\n"
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
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original development plan guidelines strictly. No additional crawling or API calls needed."})
        
        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""
          

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE - NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"

            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update or provide context. \n{all_working_files_contents}"})
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
                "   - Precise alignments (left/right/center/justified)\n"
                "   - Layout arrangements and positioning\n"
                "   - Spacing and padding measurements\n\n"
                "2. Content Analysis:\n"
                "   - All text content with exact fonts and sizes\n"
                "   - Every icon and graphic element\n"
                "   - Patterns and textures\n"
                "   - Image assets and their placement\n\n"
                "3. Implementation Requirements:\n"
                "   - Exact pixel dimensions\n"
                "   - Specific margins and padding\n"
                "   - Component hierarchy and structure\n"
                "   - Interactive elements and states\n\n"
                "4. Context & Purpose:\n"
                "   - Whether this needs to be an exact replica or just inspiration\n"
                "   - How closely to follow the reference image\n"
                "   - Which elements are essential vs optional\n"
                "   - Any modifications needed to match user requirements\n\n"
                "Your description must be thorough enough that another agent can implement it perfectly without seeing the original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, covering all visual elements, content, measurements, and implementation requirements. I'll clearly indicate whether each image should be replicated exactly or used as inspiration, ensuring other agents can implement the design precisely as needed."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Provide a concise file implementation for:\n\n{user_prompt}\n\n"
            f"Ultimate Goal: Clearly describe what this implementation will achieve for the user when completed.\n\n"
            "For EACH file that needs to be worked on, you MUST specify:\n"
            "1. File Status:\n"
            "   - Whether it's an existing file being modified\n"
            "   - Whether it's a new file being created\n" 
            "   - Whether it's a reference file to learn from\n\n"
            "2. Current State (for existing files):\n"
            "   - Detailed description of current content and structure\n"
            "   - Existing components, functions, or features\n"
            "   - Current dependencies and relationships\n\n"
            "3. Planned Changes:\n"
            "   - Specific components/sections to be added or modified\n"
            "   - Detailed description of new functionality\n"
            "   - Integration points with other files\n"
            "   - Required props, methods, or data structures\n\n"
            "4. Learning Points (for reference files):\n"
            "   - Specific patterns or approaches to adopt\n"
            "   - Implementation details to reference\n"
            "   - Architectural decisions to follow\n\n"
            "5. Design Inspiration:\n"
            "   - Overall aesthetic and style direction\n"
            "   - Color palette with specific hex codes (e.g., #FF0000 for red)\n"
            "   - Typography choices and pairings:\n"
            "     * Primary font: MUST use existing system fonts or Google Fonts - NO custom font files (.woff/.woff2/etc)\n"
            "     * Secondary font: MUST use existing system fonts or Google Fonts - NO custom font files\n"
            "     * Font sizes in px/rem:\n"
            "       - Headings: h1 (32px/2rem), h2 (28px/1.75rem), h3 (24px/1.5rem)\n"
            "       - Body text: 16px/1rem\n"
            "       - Small text: 14px/0.875rem\n"
            "       - Micro text: 12px/0.75rem\n"
            "   - Animation and interaction patterns with timing\n"
            "   - Layout principles and whitespace usage (in px/rem)\n\n"
            "6. Features & Components:\n"
            "   - Core features for initial version with detailed specs\n"
            "   - Key UI components with exact measurements:\n"
            "     * Buttons: height, width, padding in px\n"
            "     * Forms: input sizes, spacing in px\n"
            "     * Cards: dimensions, margins in px\n"
            "   - Navigation structure with hierarchy\n"
            "   - Interactive elements with states\n"
            "   - Content sections with padding/margins in px\n"
            "   - For maps: MUST use real map integration (e.g. Google Maps, Leaflet) instead of static images\n"
            "   - For schedules/calendars: MUST implement with actual calendar/scheduling components\n"
            "   - For any functional features: MUST use actual code implementation instead of placeholder images\n\n"
            "7. Design Elements:\n"
            "   - Detailed color scheme with hex codes for:\n"
            "     * Primary colors (e.g., #1A73E8)\n"
            "     * Secondary colors (e.g., #34A853)\n"
            "     * Accent colors (e.g., #EA4335)\n"
            "   - Typography specifications:\n"
            "     * Font families: ONLY use system fonts or Google Fonts - NO custom font files (.woff/.woff2/etc)\n"
            "     * Font sizes (8px to 48px scale)\n"
            "     * Font weights (400 regular, 500 medium, 700 bold)\n"
            "     * Line heights (1.2 to 1.6)\n"
            "     * Letter spacing (-0.5px to 0.5px)\n"
            "   - Animation timings (200ms to 500ms) with easing functions\n"
            "   - Spacing scale in 4px increments (4px, 8px, 16px, etc)\n"
            "   - Component-specific styling with exact measurements\n\n"
            "8. Image Assets:\n"
            "   - SVG: Best for:\n"
            "     * Company logos that need to scale (e.g., header-logo.svg)\n"
            "     * UI icons like menu, search, cart (e.g., menu-icon.svg)\n"
            "     * Simple illustrations with solid colors (e.g., empty-state.svg)\n"
            "   - PNG: Best for:\n"
            "     * Icons with transparency (e.g., close-button.png)\n"
            "     * Screenshots with text clarity (e.g., app-preview.png)\n"
            "     * Badges with transparent backgrounds (e.g., award-badge.png)\n"
            "   - JPG: Best for:\n"
            "     * Product photos (e.g., blue-tshirt.jpg)\n"
            "     * Background images (e.g., hero-background.jpg)\n"
            "     * Banner images with gradients (e.g., sale-banner.jpg)\n"
            "   - Size Guidelines:\n"
            "     * Icons:\n"
            "       - Small UI icons: 24x24px (e.g., close-icon.svg)\n"
            "       - Medium icons: 128x128px (e.g., category-icon.png)\n"
            "       - Large icons: 512x512px (e.g., app-icon.png)\n"
            "     * Illustrations:\n"
            "       - Small: 400x400px (e.g., spot-illustration.svg)\n"
            "       - Medium: 800x600px (e.g., feature-graphic.svg)\n"
            "       - Large: 1024x1024px (e.g., hero-illustration.svg)\n"
            "     * Product Images:\n"
            "       - Thumbnails: 400x400px (e.g., product-thumb.jpg)\n"
            "       - Detail views: 1200x1200px (e.g., product-large.jpg)\n"
            "       - Full size: 2048x2048px (e.g., product-zoom.jpg)\n"
            "   - IMPORTANT: For functional features like maps, schedules, etc - DO NOT use static images\n"
            "     * Maps: Use map libraries/APIs (Google Maps, Leaflet, etc)\n"
            "     * Schedules: Use calendar/scheduling components\n"
            "     * Charts: Use charting libraries\n"
            "     * Any interactive features: Implement with actual code\n\n"
            "CRITICAL FILE NAMING RULES:\n"
            "1. Before creating any new file:\n"
            "   - Check if a file with same/similar name exists in target directory\n"
            "   - Verify file name doesn't conflict with existing files\n"
            "   - Use unique, descriptive names that reflect purpose\n"
            "2. File naming conventions:\n"
            "   - Use lowercase with hyphens for separation\n"
            "   - Include component type in name (e.g., button.component.ts)\n"
            "   - Add suffixes for different file types (.service, .model, etc.)\n"
            "3. Avoid name collisions:\n"
            "   - Check across all project directories\n"
            "   - Use prefixes for feature modules\n"
            "   - Add version numbers if needed (v2, etc.)\n\n"
            "UI-Related Files - MANDATORY STYLING STRUCTURE:\n"
            "src/\n"
            "├── styles/\n"
            "│   ├── global.css          # Global styles only:\n"
            "│   │                       # - CSS reset/normalize\n"
            "│   │                       # - Typography\n"
            "│   │                       # - Color variables\n"
            "│   │                       # - Utility classes\n"
            "│   │\n"
            "│   └── main.css           # Main application styles:\n"
            "│                          # - Layout grid systems\n"
            "│                          # - Common animations\n"
            "│                          # - Shared mixins\n"
            "│                          # - Media queries\n"
            "│\n"
            "├── components/            # Each component MUST have its own CSS:\n"
            "│   ├── Button/\n"
            "│   │   ├── Button.jsx\n"
            "│   │   └── Button.css     # Button-specific styles only\n"
            "│   │\n"
            "│   └── Card/\n"
            "│       ├── Card.jsx\n"
            "│       └── Card.css       # Card-specific styles only\n"
            "│\n"
            "└── pages/                 # Each page MUST have its own CSS:\n"
            "    ├── Home/\n"
            "    │   ├── Home.jsx\n"
            "    │   ├── Home.css       # Home page-specific styles\n"
            "    │   └── index.css      # REQUIRED: Dedicated CSS for index.html\n"
            "    │\n"
            "    └── About/\n"
            "        ├── About.jsx\n"
            "        ├── About.css      # About page-specific styles\n"
            "        └── index.css      # REQUIRED: Dedicated CSS for index.html\n\n"
            "STYLING RULES:\n"
            "1. Global Styles (global.css):\n"
            "   - CSS reset/normalize\n"
            "   - Typography system\n"
            "   - Color variables\n"
            "   - Utility classes\n\n"
            "2. Main Styles (main.css):\n"
            "   - Layout grid systems\n"
            "   - Common animations\n"
            "   - Shared mixins\n"
            "   - Media queries\n\n"
            "3. Component/Page Styles (*.css):\n"
            "   - Component-specific styles\n"
            "   - Local animations\n"
            "   - Component states\n"
            "   - Layout modifications\n\n"
            "4. Index.html Styles (index.css) - MANDATORY:\n"
            "   - EVERY index.html MUST have its own dedicated CSS file\n"
            "   - Styles specific to index.html structure\n"
            "   - Page-level layout and positioning\n"
            "   - Container and wrapper styles\n"
            "   - DO NOT mix with component styles\n\n"
            "CRITICAL RULES:\n"
            "1. NEVER combine styles for multiple components\n"
            "2. ALWAYS create dedicated CSS for each component/page\n"
            "3. MANDATORY: Create index.css for EVERY index.html\n"
            "4. Use BEM or similar naming convention\n"
            "5. Keep specificity low\n"
            "6. Avoid !important\n"
            "7. NEVER create or include custom font files (.woff/.woff2/etc)\n"
            "8. ONLY use system fonts or Google Fonts\n"
            "9. For maps, schedules, and functional features:\n"
            "   - MUST use actual code implementation\n"
            "   - NO static images for functional elements\n"
            "   - Integrate real map services/APIs\n"
            "   - Use proper calendar/scheduling components\n\n"
            f"User OS: {platform.system()}\n"
            f"Based on the OS above, ensure all file paths and tree structures use the correct path separators and formatting.\n"
            f"Use clear headings (h4 ####) to organize your response.\n\n"
            f"CRITICAL: Under '#### Directory Structure', you MUST provide ONE SINGLE tree structure that ONLY shows:\n"
            f"1. New files being added\n" 
            f"2. Files being moved from one location to another\n"
            f"3. New or moved image assets\n"
            f"DO NOT include any other files in the tree, even if they are being modified.\n"
            f"DO NOT duplicate folders or files in the tree structure.\n"
            f"VERIFY all paths are unique and clear before including them.\n"
            f"Example of CORRECT tree structure:\n"
            f"```plaintext\n"
            f"project_root/\n"
            f"├── src/                          # New file being added here\n"
            f"│   ├── new_feature/\n"
            f"│   │   ├── new_file.py           # New file\n"
            f"│   │   ├── index.html            # New HTML file\n"
            f"│   │   └── index.css             # REQUIRED: Dedicated CSS for index.html\n"
            f"│   └── assets/\n"
            f"│       └── new_image.png         # New image\n"
            f"└── new_location/                 # File being moved here\n"
            f"    ├── moved_file.py             # Moved from old location\n"
            f"    ├── index.html                # Moved HTML file\n"
            f"    └── index.css                 # REQUIRED: Dedicated CSS for index.html\n"
            f"```\n"
            f"INCORRECT tree structure examples:\n"
            f"- Including duplicate folders/paths\n"
            f"- Including files just being modified\n"
            f"- Having unclear or ambiguous paths\n"
            f"- Multiple trees for different purposes\n"
            f"- Missing index.css for any index.html\n"
            f"Show complete paths for all affected files and images with action but not inside tree.\n\n"
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
            "- DO NOT create or modify any font files (.woff/.woff2/etc)\n"
            "- ONLY use system fonts or Google Fonts\n"
            "- VERIFY every index.html has its own index.css\n"
            "- For maps, schedules and functional features:\n"
            "  * Use actual code implementation instead of images\n"
            "  * Integrate real map services/APIs\n"
            "  * Use proper calendar/scheduling components\n"
            "- For each file and image, specify:\n"
            "  * Current content and structure (if existing)\n"
            "  * Planned changes and additions\n"
            "  * Integration points with other files\n"
            "  * Implementation patterns to follow\n"
            "  * Required components and features\n"
            "  * Data structures and dependencies\n"
            "  * Usage context and placement\n"
            "CRITICAL FILE AND IMAGE VERIFICATION:\n"
            "Before finalizing the plan:\n"
            "1. Scan entire project structure for:\n"
            "   - Duplicate file/image names\n"
            "   - Similar file/image names that could cause confusion\n"
            "   - Name conflicts across different directories\n"
            "   - Missing index.css files for any index.html\n"
            "2. For each new file/image:\n"
            "   - Verify unique name in target directory\n"
            "   - Check for conflicts in parent/sibling directories\n"
            "   - Validate against project naming conventions\n"
            "   - Ensure index.html has matching index.css\n"
            "3. For moved files/images:\n"
            "   - Confirm no name conflicts at destination\n"
            "   - Update all references to maintain integrity\n"
            "   - Preserve version history if applicable\n"
            "   - Move both index.html and index.css together\n"
            "4. For modified files/images:\n"
            "   - Verify correct target identified\n"
            "   - Check for similarly named items to avoid confusion\n"
            "   - Validate changes won't break existing references\n"
            "   - Confirm index.css exists for modified index.html\n\n"
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
