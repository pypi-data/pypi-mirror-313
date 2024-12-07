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
            "     * Any required modifications\n\n"
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
            "UI-Related Files - MANDATORY STYLING AND INTEGRATION RULES:\n"
            "CRITICAL: Every UI file MUST have:\n"
            "1. Its own dedicated style file\n"
            "2. Integration file for component loading/management\n"
            "3. Reusable components structure\n\n"
            "1. HTML/CSS/JS Projects:\n"
            "Example structure:\n"
            "src/\n"
            "├── components/                    # Reusable components\n"
            "│   ├── navbar/\n"
            "│   │   ├── navbar.html           # Navigation component\n"
            "│   │   ├── navbar.css            # Navigation styles\n"
            "│   │   └── navbar.js             # Navigation integration\n"
            "│   ├── header/\n"
            "│   │   ├── header.html           # Header component\n"
            "│   │   ├── header.css            # Header styles\n"
            "│   │   └── header.js             # Header integration\n"
            "│   ├── footer/\n"
            "│   │   ├── footer.html           # Footer component\n"
            "│   │   ├── footer.css            # Footer styles\n"
            "│   │   └── footer.js             # Footer integration\n"
            "│   ├── button/\n"
            "│   │   ├── button.html           # Reusable button\n"
            "│   │   ├── button.css            # Button styles\n"
            "│   │   └── button.js             # Button integration\n"
            "│   └── card/\n"
            "│       ├── card.html             # Reusable card\n"
            "│       ├── card.css              # Card styles\n"
            "│       └── card.js               # Card integration\n"
            "├── pages/\n"
            "│   ├── home/\n"
            "│   │   ├── home.html\n"
            "│   │   ├── home.css              # Page styles\n"
            "│   │   └── home.js               # Page integration\n"
            "│   └── products/\n"
            "│       ├── products.html\n"
            "│       ├── products.css          # Page styles\n"
            "│       └── products.js           # Page integration\n"
            "├── assets/                       # All media files\n"
            "│   ├── images/                   # By feature/component\n"
            "│   │   ├── logos/\n"
            "│   │   ├── icons/\n"
            "│   │   └── backgrounds/\n"
            "│   └── media/                    # Other media files\n"
            "├── js/\n"
            "│   └── main.js                   # Main integration file\n"
            "└── styles/\n"
            "    └── global.css                # Global styles only\n\n"
            "2. React Projects:\n"
            "src/\n"
            "├── components/                    # Reusable components\n"
            "│   ├── ui/                       # Basic UI components\n"
            "│   │   ├── Button/\n"
            "│   │   │   ├── Button.tsx\n"
            "│   │   │   ├── Button.module.css\n"
            "│   │   │   └── ButtonContext.tsx # Component context\n"
            "│   │   ├── Card/\n"
            "│   │   │   ├── Card.tsx\n"
            "│   │   │   ├── Card.module.css\n"
            "│   │   │   └── CardContext.tsx   # Component context\n"
            "│   │   └── Input/\n"
            "│   │       ├── Input.tsx\n"
            "│   │       ├── Input.module.css\n"
            "│   │       └── InputContext.tsx  # Component context\n"
            "│   ├── layout/                   # Layout components\n"
            "│   │   ├── Header/\n"
            "│   │   │   ├── Header.tsx\n"
            "│   │   │   ├── Header.module.css\n"
            "│   │   │   └── HeaderContext.tsx # Component context\n"
            "│   │   ├── Footer/\n"
            "│   │   │   ├── Footer.tsx\n"
            "│   │   │   ├── Footer.module.css\n"
            "│   │   │   └── FooterContext.tsx # Component context\n"
            "│   │   └── Navbar/\n"
            "│   │       ├── Navbar.tsx\n"
            "│   │       ├── Navbar.module.css\n"
            "│   │       └── NavbarContext.tsx # Component context\n"
            "├── pages/\n"
            "│   ├── Dashboard/\n"
            "│   │   ├── Dashboard.tsx\n"
            "│   │   ├── Dashboard.module.css\n"
            "│   │   └── DashboardContext.tsx  # Page context\n"
            "│   └── Profile/\n"
            "│       ├── Profile.tsx\n"
            "│       ├── Profile.module.css\n"
            "│       └── ProfileContext.tsx    # Page context\n"
            "├── assets/                       # All media files\n"
            "│   ├── images/                   # By feature/component\n"
            "│   │   ├── logos/\n"
            "│   │   ├── icons/\n"
            "│   │   └── backgrounds/\n"
            "│   └── media/                    # Other media files\n"
            "└── styles/\n"
            "    └── global.css                # Global styles only\n\n"
            "3. Vue.js Projects:\n"
            "src/\n"
            "├── components/                    # Reusable components\n"
            "│   ├── ui/                       # Basic UI components\n"
            "│   │   ├── Button/\n"
            "│   │   │   ├── Button.vue        # Single file component\n"
            "│   │   │   └── ButtonStore.js    # Component store\n"
            "│   │   └── Card/\n"
            "│   │       ├── Card.vue\n"
            "│   │       └── CardStore.js      # Component store\n"
            "│   └── layout/\n"
            "│       ├── Header/\n"
            "│       │   ├── Header.vue\n"
            "│       │   └── HeaderStore.js    # Component store\n"
            "│       └── Footer/\n"
            "│           ├── Footer.vue\n"
            "│           └── FooterStore.js    # Component store\n"
            "├── views/                        # Page components\n"
            "│   ├── Home/\n"
            "│   │   ├── Home.vue\n"
            "│   │   └── HomeStore.js          # View store\n"
            "│   └── About/\n"
            "│       ├── About.vue\n"
            "│       └── AboutStore.js         # View store\n"
            "└── store/                        # Vuex stores\n"
            "    └── index.js                  # Root store\n\n"
            "4. Angular Projects:\n"
            "src/\n"
            "├── app/\n"
            "│   ├── components/               # Reusable components\n"
            "│   │   ├── button/\n"
            "│   │   │   ├── button.component.ts\n"
            "│   │   │   ├── button.component.html\n"
            "│   │   │   ├── button.component.scss\n"
            "│   │   │   └── button.service.ts # Component service\n"
            "│   │   └── card/\n"
            "│   │       ├── card.component.ts\n"
            "│   │       ├── card.component.html\n"
            "│   │       ├── card.component.scss\n"
            "│   │       └── card.service.ts   # Component service\n"
            "│   ├── pages/                    # Page components\n"
            "│   │   └── home/\n"
            "│   │       ├── home.component.ts\n"
            "│   │       ├── home.component.html\n"
            "│   │       ├── home.component.scss\n"
            "│   │       └── home.service.ts   # Page service\n"
            "│   └── services/                 # Shared services\n"
            "│       └── data.service.ts\n"
            "└── assets/                       # Static assets\n\n"
            "COMPONENT INTEGRATION RULES:\n"
            "1. HTML/CSS/JS:\n"
            "   - Each component MUST have integration JS file\n"
            "   - Use jQuery/JS for dynamic loading\n"
            "   - Handle component lifecycle and events\n"
            "   - Manage component state and interactions\n\n"
            "2. React:\n"
            "   - Use Context API for component state\n"
            "   - Implement proper prop drilling\n"
            "   - Handle component composition\n"
            "   - Use hooks for lifecycle management\n\n"
            "3. Vue.js:\n"
            "   - Implement component stores\n"
            "   - Use Vue composition API\n"
            "   - Handle component registration\n"
            "   - Manage component events\n\n"
            "4. Angular:\n"
            "   - Create component services\n"
            "   - Use dependency injection\n"
            "   - Implement proper modules\n"
            "   - Handle component lifecycle\n\n"
            "STYLING RULES:\n"
            "1. NEVER combine styles for multiple components\n"
            "2. ALWAYS create dedicated style files for:\n"
            "   - Each component\n"
            "   - Each page/view\n"
            "   - Each layout template\n"
            "3. Use global styles ONLY for:\n"
            "   - CSS reset/normalize\n"
            "   - Typography\n"
            "   - Color variables\n"
            "   - Common utilities\n"
            "4. Component styles MUST be scoped\n"
            "5. Match file names to components\n"
            "6. Make components:\n"
            "   - Single responsibility\n"
            "   - Highly customizable\n"
            "   - Well-documented\n"
            "   - Consistent\n\n"
            f"CRITICAL: Under '#### Directory Structure', provide ONE tree showing:\n"
            f"1. New files being added\n" 
            f"2. Files being moved\n"
            f"3. New/moved image files\n"
            f"DO NOT include modified files.\n"
            f"DO NOT duplicate paths.\n"
            f"VERIFY unique paths.\n"
            f"Example tree:\n"
            f"```plaintext\n"
            f"project_root/\n"
            f"├── src/                          # New file location\n"
            f"│   ├── new_feature/\n"
            f"│   │   └── new_file.py           # New file\n"
            f"│   └── assets/\n"
            f"│       └── images/\n"
            f"│           └── logo-250x100.png   # New image\n"
            f"└── new_location/                 # Move destination\n"
            f"    └── moved_file.py             # Moved file\n"
            f"```\n"
            f"INCORRECT examples:\n"
            f"- Duplicate folders/paths\n"
            f"- Including modified files\n"
            f"- Unclear paths\n"
            f"- Multiple trees\n"
            f"Show complete paths with actions.\n\n"
            f"IMPORTANT: If dependencies/build needed, provide {platform.system()} commands:\n"
            f"```bash\n"
            f"# Only if required\n"
            f"# Valid for {platform.system()}\n"
            f"```\n"
            f"IMPORTANT: NO-CODE PLANNING PHASE. NO IMPLEMENTATION DETAILS.\n"
            f"Exclude: navigation, file opening, verification, non-coding actions. "
            f"KEEP TASKS FOCUSED AND MINIMAL. "
            f"USE FULL PATHS. "
            "BE SPECIFIC ABOUT FILES. NO ASSUMPTIONS OR PLACEHOLDERS.\n"
            "SPECIFY SOURCE/DESTINATION FOR MOVES. SPECIFY EXACT LOCATION FOR NEW FILES.\n"
            "VERIFY UNIQUE PATHS - NO DUPLICATES.\n"
            "LIST ONLY 100% NECESSARY FILES.\n"
            "CLEARLY STATE NEW VS EXISTING.\n"
            "PRESERVE SPACES IN PATHS.\n"
            "ANALYZE COMPREHENSIVELY:\n"
            "- Validate paths/dependencies\n"
            "- Check component integration\n" 
            "- Verify requirements\n"
            "- Check conflicts\n"
            "- Ensure unique paths\n"
            "- Check for similar names\n"
            "- Verify unique identifiers\n"
            "- Check naming conflicts\n"
            "- Validate extensions\n"
            "- Ensure descriptive names\n"
            "- Verify image paths/formats\n"
            "- Confirm image requirements\n"
            f"REMEMBER: PLANNING ONLY - NO CODE.\n"
            f"NO EXTRA/REPEAT INFO, NO SUMMARIES.\n"
            f"Respond in: {original_prompt_language}\n"
            f"USE MARKDOWN FOR LINKS: [text](url)\n"
            "Only return needed sections. Skip non-relevant ones. If plan needs dependencies installed and images generated (PNG/JPG/JPEG/ico only), end with #### DONE: *** - D*** I**. If only dependencies needed, end with #### DONE: *** - D***. If only eligible images needed, end with #### DONE: *** - I**. Otherwise, no special ending."
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
