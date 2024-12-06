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
            "- Image Assets:\n"
            "    - SVG: Logos, icons, illustrations\n"
            "    - PNG: Graphics needing transparency\n"
            "    - JPG: Photos and gradients\n"
            "    - Sizes: Icons 24-512px, Illustrations ≤1024px, Products ≤2048px\n"
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
            "Only return sections that are needed for the user request. Do not return non-relevant sections. If the plan includes dependencies that need to be installed, always include \"MUST INSTALL DEPENDENCY\". If the plan includes images that need to be newly generated in these formats only: 'PNG, png, JPG, jpg, JPEG, jpeg, and ico', then always include \"MUST GENERATE IMAGE\". At the end of everything, the last sentence, MUST ALWAYS start with #### DONE: \"MUST INSTALL DEPENDENCY\", \"MUST GENERATE IMAGE\""
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

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Provide a concise file implementation for:\n\n{user_prompt}\n\n"
            f"User OS: {platform.system()}\n"
            f"Based on the OS above, ensure all file paths and tree structures use the correct path separators and formatting.\n"
            f"Use clear headings (h4 ####) to organize your response.\n\n"
            f"Ultimate Goal\n"
            f"Clearly state the ultimate goal of this task, summarizing the main objective and desired outcome.\n\n"
            "UI-Related Files - MANDATORY STYLING RULES:\n"
            "CRITICAL: Every UI file MUST have its own dedicated style file AND reusable components, regardless of tech stack:\n\n"
            "1. HTML/CSS Projects:\n"
            "Example structure:\n"
            "src/\n"
            "├── components/                    # Reusable components\n"
            "│   ├── navbar/\n"
            "│   │   ├── navbar.html           # Navigation component\n"
            "│   │   └── navbar.css            # Navigation styles\n"
            "│   ├── header/\n"
            "│   │   ├── header.html           # Header component\n"
            "│   │   └── header.css            # Header styles\n"
            "│   ├── footer/\n"
            "│   │   ├── footer.html           # Footer component\n"
            "│   │   └── footer.css            # Footer styles\n"
            "│   ├── button/\n"
            "│   │   ├── button.html           # Reusable button component\n"
            "│   │   └── button.css            # Button styles\n"
            "│   └── card/\n"
            "│       ├── card.html             # Reusable card component\n"
            "│       └── card.css              # Card styles\n"
            "├── pages/\n"
            "│   ├── home/\n"
            "│   │   ├── home.html\n"
            "│   │   └── home.css              # Page-specific styles\n"
            "│   └── products/\n"
            "│       ├── products.html\n"
            "│       └── products.css          # Page-specific styles\n"
            "└── styles/\n"
            "    └── global.css                # Global styles only\n\n"
            "2. React Projects:\n"
            "src/\n"
            "├── components/                    # Reusable components\n"
            "│   ├── ui/                       # Basic UI components\n"
            "│   │   ├── Button/\n"
            "│   │   │   ├── Button.tsx\n"
            "│   │   │   └── Button.module.css # Reusable button styles\n"
            "│   │   ├── Card/\n"
            "│   │   │   ├── Card.tsx\n"
            "│   │   │   └── Card.module.css   # Reusable card styles\n"
            "│   │   └── Input/\n"
            "│   │       ├── Input.tsx\n"
            "│   │       └── Input.module.css  # Reusable input styles\n"
            "│   ├── layout/                   # Layout components\n"
            "│   │   ├── Header/\n"
            "│   │   │   ├── Header.tsx\n"
            "│   │   │   └── Header.module.css # Header styles\n"
            "│   │   ├── Footer/\n"
            "│   │   │   ├── Footer.tsx\n"
            "│   │   │   └── Footer.module.css # Footer styles\n"
            "│   │   └── Navbar/\n"
            "│   │       ├── Navbar.tsx\n"
            "│   │       └── Navbar.module.css # Navbar styles\n"
            "├── pages/\n"
            "│   ├── Dashboard/\n"
            "│   │   ├── Dashboard.tsx\n"
            "│   │   └── Dashboard.module.css  # Page-specific styles\n"
            "│   └── Profile/\n"
            "│       ├── Profile.tsx\n"
            "│       └── Profile.module.css    # Page-specific styles\n"
            "└── styles/\n"
            "    └── global.css                # Global styles only\n\n"
            "3. Vue Projects:\n"
            "src/\n"
            "├── components/                    # Reusable components\n"
            "│   ├── ui/                       # Basic UI components\n"
            "│   │   ├── BaseButton/\n"
            "│   │   │   ├── BaseButton.vue\n"
            "│   │   │   └── BaseButton.scss   # Reusable button styles\n"
            "│   │   ├── BaseCard/\n"
            "│   │   │   ├── BaseCard.vue\n"
            "│   │   │   └── BaseCard.scss     # Reusable card styles\n"
            "│   │   └── BaseInput/\n"
            "│   │       ├── BaseInput.vue\n"
            "│   │       └── BaseInput.scss    # Reusable input styles\n"
            "│   └── layout/                   # Layout components\n"
            "│       ├── TheNavbar/\n"
            "│       │   ├── TheNavbar.vue\n"
            "│       │   └── TheNavbar.scss    # Navbar styles\n"
            "│       ├── TheHeader/\n"
            "│       │   ├── TheHeader.vue\n"
            "│       │   └── TheHeader.scss    # Header styles\n"
            "│       └── TheFooter/\n"
            "│           ├── TheFooter.vue\n"
            "│           └── TheFooter.scss    # Footer styles\n"
            "└── views/\n"
            "    ├── Home/\n"
            "    │   ├── Home.vue\n"
            "    │   └── Home.scss             # View-specific styles\n"
            "    └── About/\n"
            "        ├── About.vue\n"
            "        └── About.scss            # View-specific styles\n\n"
            "STYLING RULES:\n"
            "1. NEVER combine styles for multiple components/pages in one file\n"
            "2. ALWAYS create a dedicated style file for each:\n"
            "   - Page/View\n"
            "   - Component (both layout and UI)\n"
            "   - Layout template\n"
            "3. Use global.css/scss ONLY for:\n"
            "   - CSS reset/normalize\n"
            "   - Typography\n"
            "   - Color variables\n"
            "   - Common utility classes\n"
            "4. Component styles MUST be scoped/modular\n"
            "5. Follow naming convention matching the component/page name\n"
            "6. Reusable components MUST be:\n"
            "   - Small and focused on a single responsibility\n"
            "   - Highly customizable through props/attributes\n"
            "   - Well-documented with clear usage examples\n"
            "   - Consistent across the application\n\n"
            f"CRITICAL: Under '#### Directory Structure', you MUST provide ONE SINGLE tree structure that ONLY shows:\n"
            f"1. New files being added\n" 
            f"2. Files being moved from one location to another\n"
            f"DO NOT include any other files in the tree, even if they are being modified.\n"
            f"DO NOT duplicate folders or files in the tree structure.\n"
            f"VERIFY all paths are unique and clear before including them.\n"
            f"Example of CORRECT tree structure:\n"
            f"```plaintext\n"
            f"project_root/\n"
            f"├── src/                          # New file being added here\n"
            f"│   └── new_feature/\n"
            f"│       └── new_file.py           # New file\n"
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
            "IMPORTANT: For each file, clearly state if it's new or existing related for this task only. This is crucial for other agents to determine appropriate actions.\n"
            "For paths with spaces, preserve the original spaces without escaping or encoding.\n"
            "PERFORM A COMPREHENSIVE ANALYSIS:\n"
            "- Validate all file paths and dependencies\n"
            "- Ensure all components are properly integrated\n" 
            "- Verify the implementation meets all requirements\n"
            "- Check for potential conflicts or issues\n"
            "- Ensure no duplicate paths or unclear locations\n"
            f"REMEMBER: THIS IS STRICTLY A PLANNING PHASE - NO CODE OR IMPLEMENTATION DETAILS SHOULD BE INCLUDED.\n"
            f"DO NOT PROVIDE ANYTHING EXTRA SUCH AS SUMMARY OR ANYTHING REPEAT FROM PREVIOUS INFORMATION, NO YAPPING. "
            f"Respond in: {original_prompt_language}\n"
            f"FOR ALL LINKS, YOU MUST USE MARKDOWN FORMAT. EXAMPLE: [Link text](https://www.example.com)"
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
