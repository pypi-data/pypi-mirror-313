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
        file_ext = os.path.splitext(file_name)[1].lower()

        # Read current file content
        current_file_content = read_file_content(file)
        if current_file_content:
            self.conversation_history.append({"role": "user", "content": f"Here is the current content of {file_name} that needs to be updated:\n{current_file_content}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this file content as context for the updates."})

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

        base_prompt = f"As a world-class, highly experienced developer, implement the following task with utmost efficiency and precision:\n"
        base_prompt += f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}\n"

        # Extension specific prompts
        extension_prompts = {
            # Web Development (Frontend and Backend)
            '.html': """
                For HTML Implementation:
                - Use semantic HTML5 elements appropriately
                - Implement proper document structure and landmarks
                - Add ARIA roles and accessibility attributes
                - Ensure proper meta tags and SEO optimization
                - Create clean, maintainable markup
                - Follow W3C standards and best practices
                - Implement proper form validation attributes
                - Use microdata/schema.org markup
                - Implement responsive images
                - Add proper security headers
                - Use proper caching strategies
                - Implement proper performance optimization
            """,
            '.svg': """
                Create SVG that matches project's existing visual style and use case.
                For brand assets and vector graphics:
                - Keep official colors, proportions and brand identity intact
                - Follow brand guidelines strictly and maintain visual consistency
                - Optimize SVG code for performance and file size
                - Ensure cross-browser compatibility and responsiveness
                - Use semantic element names and proper grouping
                - Include ARIA labels and accessibility attributes
                - Implement smooth animations and transitions if needed
            """,
            '.css': """
                For CSS Implementation:
                - Follow BEM/SMACSS/OOCSS methodology
                - Use modern CSS features (Grid, Flexbox, Custom Properties)
                - Implement responsive design with proper breakpoints
                - Create maintainable and scalable stylesheets
                - Optimize performance with efficient selectors
                - Add smooth transitions and animations
                - Ensure cross-browser compatibility
                - Use CSS modules or CSS-in-JS when appropriate
                - Implement proper CSS architecture
                - Use PostCSS/SASS/LESS features effectively
                - Implement CSS containment
                - Use logical properties
                - Add print stylesheets
                - Implement proper dark mode support
                - Use proper CSS custom properties
            """,
            '.scss': """
                For SCSS Implementation:
                - Use SCSS features effectively (variables, mixins, functions)
                - Follow SCSS best practices and patterns
                - Implement proper nesting structure
                - Use extends and placeholders appropriately
                - Create reusable components and utilities
                - Optimize compilation output
                - Follow modular architecture
                - Use proper import structure
                - Implement proper theming system
                - Follow naming conventions
            """,
            '.sass': """
                For Sass Implementation:
                - Use Sass features effectively
                - Follow proper indentation syntax
                - Implement modular architecture
                - Use mixins and functions appropriately
                - Create maintainable stylesheets
                - Optimize compilation output
                - Follow naming conventions
                - Use proper import structure
                - Implement proper theming
            """,
            '.js': """
                For JavaScript Implementation:
                - Use modern ES6+ features appropriately
                - Implement proper error handling and validation
                - Follow functional programming principles
                - Create modular and reusable code
                - Optimize performance and memory usage
                - Add proper event handling and delegation
                - Implement async operations correctly
                - Use appropriate design patterns
                - Follow SOLID principles
                - Implement proper testing with Jest/Mocha
                - Use Web Workers for heavy computations
                - Implement service workers
                - Use proper memory management
                - Add proper security measures
                - Implement proper caching strategies
                - Use proper bundling and tree shaking
                - Implement proper code splitting
            """,
            '.jsx': """
                For React Implementation:
                - Follow React best practices and patterns
                - Use hooks effectively (useState, useEffect, useContext)
                - Implement proper component lifecycle
                - Create reusable and composable components
                - Manage state efficiently
                - Handle side effects properly
                - Implement proper prop types and validation
                - Use React.memo and useMemo for optimization
                - Implement error boundaries
                - Follow React performance best practices
            """,
            '.ts': """
                For TypeScript Implementation:
                - Use TypeScript features effectively
                - Implement proper type definitions
                - Create type-safe code
                - Follow TypeScript best practices
                - Use generics appropriately
                - Implement proper type guards
                - Use utility types effectively
                - Follow TypeScript patterns
                - Add proper error handling
                - Use proper configuration
            """,
            '.tsx': """
                For React TypeScript Implementation:
                - Use TypeScript features effectively
                - Implement proper type definitions and interfaces
                - Create type-safe components and hooks
                - Follow TypeScript best practices
                - Add proper error boundaries
                - Implement strict null checks
                - Use generics where appropriate
                - Follow TypeScript patterns
            """,
            '.json': """
                For JSON Implementation:
                - Follow JSON schema standards
                - Validate JSON structure
                - Use proper formatting
                - Implement proper error handling
                - Follow naming conventions
                - Use proper data types
                - Optimize file size
                - Add proper documentation
            """,
            '.xml': """
                For XML Implementation:
                - Follow XML standards
                - Use proper schema validation
                - Implement proper structure
                - Use namespaces appropriately
                - Follow naming conventions
                - Add proper documentation
                - Optimize file size
                - Use proper encoding
            """,
            '.yaml': """
                For YAML Implementation:
                - Follow YAML standards
                - Use proper indentation
                - Implement proper structure
                - Use anchors and aliases effectively
                - Follow naming conventions
                - Add proper documentation
                - Validate syntax
                - Use proper data types
            """,
            '.yml': """
                For YAML Implementation:
                - Follow YAML standards
                - Use proper indentation
                - Implement proper structure
                - Use anchors and aliases effectively
                - Follow naming conventions
                - Add proper documentation
                - Validate syntax
                - Use proper data types
            """,
            '.csv': """
                For CSV Implementation:
                - Follow CSV standards
                - Use proper delimiters
                - Handle special characters
                - Implement proper headers
                - Validate data types
                - Add proper documentation
                - Optimize file size
                - Handle encoding properly
            """,
            '.md': """
                For Markdown Implementation:
                - Follow Markdown syntax
                - Use proper formatting
                - Implement proper structure
                - Add proper documentation
                - Use proper links and references
                - Follow style guide
                - Optimize readability
                - Use proper extensions
            """,
            '.php': """
                For PHP Implementation:
                - Follow PSR standards
                - Use modern PHP features
                - Implement proper error handling
                - Follow framework best practices
                - Use composer effectively
                - Implement proper testing
                - Follow SOLID principles
                - Use type system effectively
            """,
            '.asp': """
                For ASP Implementation:
                - Follow ASP best practices
                - Implement proper error handling
                - Use proper session management
                - Follow security guidelines
                - Optimize performance
                - Add proper documentation
                - Use proper database access
                - Implement proper caching
            """,
            '.aspx': """
                For ASP.NET Implementation:
                - Follow ASP.NET best practices
                - Use proper controls
                - Implement proper error handling
                - Follow security guidelines
                - Optimize performance
                - Add proper documentation
                - Use proper data binding
                - Implement proper validation
            """,
            '.jsp': """
                For JSP Implementation:
                - Follow JSP best practices
                - Use proper tags
                - Implement proper error handling
                - Follow security guidelines
                - Optimize performance
                - Add proper documentation
                - Use proper expression language
                - Implement proper validation
            """,
            '.erb': """
                For ERB Implementation:
                - Follow Ruby/Rails conventions
                - Use proper templating
                - Implement proper error handling
                - Follow security guidelines
                - Optimize performance
                - Add proper documentation
                - Use proper helpers
                - Implement proper layouts
            """,
            '.vue': """
                For Vue Implementation:
                - Follow Vue 3 Composition API patterns
                - Implement proper component structure
                - Use reactive refs and computed properties
                - Handle component lifecycle correctly
                - Create reusable composables
                - Implement proper prop validation
                - Use proper event handling
                - Implement state management
            """,
            '.svelte': """
                For Svelte Implementation:
                - Follow Svelte best practices
                - Use reactive statements
                - Implement proper component structure
                - Handle lifecycle correctly
                - Create reusable stores
                - Use proper event handling
                - Implement proper transitions
                - Follow proper patterns
            """,
            '.twig': """
                For Twig Implementation:
                - Follow Twig best practices
                - Use proper templating
                - Implement proper inheritance
                - Use filters effectively
                - Create reusable blocks
                - Follow naming conventions
                - Add proper documentation
                - Use proper functions
            """,
            '.hbs': """
                For Handlebars Implementation:
                - Follow Handlebars best practices
                - Use proper helpers
                - Implement proper partials
                - Create reusable templates
                - Follow naming conventions
                - Add proper documentation
                - Use proper expressions
                - Implement proper logic
            """,
            '.ejs': """
                For EJS Implementation:
                - Follow EJS best practices
                - Use proper templating
                - Implement proper includes
                - Create reusable partials
                - Follow naming conventions
                - Add proper documentation
                - Use proper expressions
                - Implement proper logic
            """,
            '.liquid': """
                For Liquid Implementation:
                - Follow Liquid best practices
                - Use proper filters
                - Implement proper tags
                - Create reusable snippets
                - Follow naming conventions
                - Add proper documentation
                - Use proper expressions
                - Implement proper logic
            """,
            # Backend Development
            '.py': """
                For Python Implementation:
                - Follow PEP 8 style guide
                - Use type hints and docstrings
                - Implement proper error handling
                - Create modular and testable code
                - Use appropriate design patterns
                - Optimize for performance
                - Follow SOLID principles
                - Use virtual environments
            """,
            '.r': """
                For R Implementation:
                - Follow R style guide
                - Use proper data structures
                - Implement proper error handling
                - Optimize for performance
                - Use appropriate packages
                - Add proper documentation
                - Follow best practices
                - Use proper testing
            """,
            '.java': """
                For Java Implementation:
                - Follow Java coding standards
                - Use proper OOP principles
                - Implement exception handling
                - Use collections framework effectively
                - Follow Spring/Spring Boot best practices
                - Implement proper dependency injection
                - Use appropriate design patterns
                - Optimize performance
            """,
            '.kt': """
                For Kotlin Implementation:
                - Use Kotlin idioms and features
                - Implement null safety
                - Use coroutines for async operations
                - Follow SOLID principles
                - Use extension functions effectively
                - Implement proper error handling
                - Create clean architecture
                - Use Kotlin DSLs when appropriate
            """,
            '.scala': """
                For Scala Implementation:
                - Follow Scala style guide
                - Use functional programming principles
                - Implement proper error handling
                - Use type system effectively
                - Follow best practices
                - Optimize performance
                - Use proper concurrency
                - Implement proper testing
            """,
            '.cs': """
                For C# Implementation:
                - Follow C# coding standards
                - Use LINQ effectively
                - Implement async/await properly
                - Use proper dependency injection
                - Follow .NET best practices
                - Implement proper error handling
                - Use appropriate design patterns
                - Follow SOLID principles
            """,
            '.go': """
                For Go Implementation:
                - Follow Go style guide
                - Use proper error handling
                - Implement concurrent programming
                - Use interfaces effectively
                - Follow Go idioms and patterns
                - Optimize for performance
                - Implement proper testing
                - Use Go modules
            """,
            '.rb': """
                For Ruby Implementation:
                - Follow Ruby style guide
                - Use Ruby idioms effectively
                - Follow Rails conventions if applicable
                - Implement proper error handling
                - Use blocks and procs effectively
                - Follow best practices
                - Implement proper testing
                - Use metaprogramming appropriately
            """,
            '.pl': """
                For Perl Implementation:
                - Follow Perl best practices
                - Use proper error handling
                - Implement proper testing
                - Use modules effectively
                - Follow naming conventions
                - Add proper documentation
                - Use proper data structures
                - Implement proper validation
            """,
            '.sh': """
                For Shell Script Implementation:
                - Follow shell scripting best practices
                - Use proper error handling
                - Implement proper logging
                - Use proper variables
                - Follow naming conventions
                - Add proper documentation
                - Use proper functions
                - Implement proper validation
            """,
            '.bat': """
                For Batch File Implementation:
                - Follow batch scripting best practices
                - Use proper error handling
                - Implement proper logging
                - Use proper variables
                - Follow naming conventions
                - Add proper documentation
                - Use proper functions
                - Implement proper validation
            """,
            '.ps1': """
                For PowerShell Implementation:
                - Follow PowerShell best practices
                - Use proper error handling
                - Implement proper logging
                - Use proper variables
                - Follow naming conventions
                - Add proper documentation
                - Use proper functions
                - Implement proper validation
            """,
            '.rs': """
                For Rust Implementation:
                - Follow Rust idioms
                - Use ownership system correctly
                - Implement proper error handling
                - Use traits effectively
                - Follow safety principles
                - Optimize for performance
                - Use cargo effectively
                - Implement proper testing
            """,
            '.lua': """
                For Lua Implementation:
                - Follow Lua best practices
                - Use proper error handling
                - Implement proper testing
                - Use modules effectively
                - Follow naming conventions
                - Add proper documentation
                - Use proper data structures
                - Implement proper validation
            """,
            '.swift': """
                For Swift Implementation:
                - Follow Swift style guide
                - Use proper protocol-oriented programming
                - Implement error handling
                - Use Swift concurrency features
                - Follow iOS/macOS guidelines
                - Implement proper memory management
                - Use type system effectively
                - Follow SwiftUI best practices
            """,
            '.m': """
                For Objective-C Implementation:
                - Follow Objective-C best practices
                - Use proper memory management
                - Implement error handling
                - Use proper design patterns
                - Follow iOS/macOS guidelines
                - Add proper documentation
                - Use proper testing
                - Implement proper validation
            """,
            # Data Science and Analysis
            '.ipynb': """
                For Jupyter Notebook Implementation:
                - Follow notebook best practices
                - Use proper markdown documentation
                - Implement proper error handling
                - Optimize for performance
                - Use appropriate libraries
                - Add proper visualization
                - Follow proper structure
                - Use proper testing
            """,
            '.rmd': """
                For R Markdown Implementation:
                - Follow R Markdown best practices
                - Use proper chunks
                - Implement proper documentation
                - Use appropriate packages
                - Add proper visualization
                - Follow proper structure
                - Use proper testing
                - Implement proper validation
            """,
            '.sql': """
                For SQL Implementation:
                - Follow SQL best practices
                - Optimize query performance
                - Use proper indexing
                - Implement proper transactions
                - Follow database normalization
                - Use proper constraints
                - Implement proper security
                - Use proper stored procedures
            """,
            '.db': """
                For Database Implementation:
                - Follow database best practices
                - Use proper schema design
                - Implement proper indexing
                - Use proper constraints
                - Follow normalization rules
                - Add proper documentation
                - Use proper backup strategies
                - Implement proper security
            """,
            '.dbf': """
                For DBF Implementation:
                - Follow DBF best practices
                - Use proper field types
                - Implement proper indexing
                - Handle data properly
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper backup
            """,
            '.parquet': """
                For Parquet Implementation:
                - Follow Parquet best practices
                - Use proper compression
                - Implement proper schema
                - Optimize for performance
                - Use proper partitioning
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.h5': """
                For HDF5 Implementation:
                - Follow HDF5 best practices
                - Use proper groups and datasets
                - Implement proper compression
                - Optimize for performance
                - Use proper attributes
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.pickle': """
                For Pickle Implementation:
                - Follow pickle best practices
                - Use proper serialization
                - Implement proper security
                - Handle errors properly
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.pkl': """
                For Pickle Implementation:
                - Follow pickle best practices
                - Use proper serialization
                - Implement proper security
                - Handle errors properly
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.dta': """
                For Stata Data Implementation:
                - Follow Stata best practices
                - Use proper data types
                - Implement proper labels
                - Handle missing values
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.sav': """
                For SPSS Implementation:
                - Follow SPSS best practices
                - Use proper data types
                - Implement proper labels
                - Handle missing values
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.mat': """
                For MATLAB Implementation:
                - Follow MATLAB best practices
                - Use proper data types
                - Implement proper functions
                - Optimize for performance
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.feather': """
                For Feather Implementation:
                - Follow Feather best practices
                - Use proper data types
                - Implement proper schema
                - Optimize for performance
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.orc': """
                For ORC Implementation:
                - Follow ORC best practices
                - Use proper compression
                - Implement proper schema
                - Optimize for performance
                - Use proper striping
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.arff': """
                For ARFF Implementation:
                - Follow ARFF best practices
                - Use proper attributes
                - Implement proper data types
                - Handle missing values
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.xpt': """
                For SAS Transport Implementation:
                - Follow SAS best practices
                - Use proper data types
                - Implement proper labels
                - Handle missing values
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.sas': """
                For SAS Implementation:
                - Follow SAS best practices
                - Use proper data steps
                - Implement proper procedures
                - Optimize for performance
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.do': """
                For Stata Do-File Implementation:
                - Follow Stata best practices
                - Use proper commands
                - Implement proper error handling
                - Optimize for performance
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.ctl': """
                For Control File Implementation:
                - Follow best practices
                - Use proper syntax
                - Implement proper error handling
                - Follow structure guidelines
                - Use proper parameters
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            '.st': """
                For Stata Implementation:
                - Follow Stata best practices
                - Use proper commands
                - Implement proper error handling
                - Optimize for performance
                - Follow naming conventions
                - Add proper documentation
                - Use proper validation
                - Implement proper handling
            """,
            # General Purpose Programming
            '.cpp': """
                For C++ Implementation:
                - Follow modern C++ standards
                - Use RAII principles
                - Implement proper memory management
                - Use STL effectively
                - Follow C++ best practices
                - Optimize for performance
                - Use templates appropriately
                - Implement proper error handling
            """,
            '.c': """
                For C Implementation:
                - Follow C standards
                - Use proper memory management
                - Implement proper error handling
                - Optimize for performance
                - Follow best practices
                - Use proper pointers
                - Add proper documentation
                - Implement proper validation
            """,
            '.h': """
                For Header Implementation:
                - Follow header best practices
                - Use proper include guards
                - Implement proper declarations
                - Follow naming conventions
                - Add proper documentation
                - Use proper macros
                - Implement proper interfaces
                - Follow proper structure
            """,
            '.hpp': """
                For C++ Header Implementation:
                - Follow C++ header best practices
                - Use proper include guards
                - Implement proper templates
                - Follow naming conventions
                - Add proper documentation
                - Use proper declarations
                - Implement proper interfaces
                - Follow proper structure
            """,
            '.ino': """
                For Arduino Implementation:
                - Follow Arduino best practices
                - Use proper pin management
                - Implement proper timing
                - Handle interrupts properly
                - Follow naming conventions
                - Add proper documentation
                - Use proper libraries
                - Implement proper validation
            """,
            '.dart': """
                For Dart/Flutter Implementation:
                - Follow Dart style guide
                - Use Flutter widgets effectively
                - Implement proper state management
                - Follow Flutter best practices
                - Use proper error handling
                - Implement proper testing
                - Use proper logging
                - Add proper security measures
            """,
            '.vb': """
                For Visual Basic Implementation:
                - Follow VB best practices
                - Use proper error handling
                - Implement proper validation
                - Follow naming conventions
                - Add proper documentation
                - Use proper data types
                - Implement proper testing
                - Follow proper structure
            """,
            '.f90': """
                For Fortran Implementation:
                - Follow Fortran best practices
                - Use proper arrays
                - Implement proper procedures
                - Optimize for performance
                - Follow naming conventions
                - Add proper documentation
                - Use proper modules
                - Implement proper validation
            """,
            '.pas': """
                For Pascal Implementation:
                - Follow Pascal best practices
                - Use proper procedures
                - Implement proper error handling
                - Follow naming conventions
                - Add proper documentation
                - Use proper data types
                - Implement proper validation
                - Follow proper structure
            """,
            '.asm': """
                For Assembly Implementation:
                - Follow assembly best practices
                - Use proper registers
                - Implement proper memory management
                - Optimize for performance
                - Follow naming conventions
                - Add proper documentation
                - Use proper instructions
                - Implement proper validation
            """,
            '.ml': """
                For OCaml Implementation:
                - Follow OCaml best practices
                - Use proper pattern matching
                - Implement proper types
                - Follow functional principles
                - Add proper documentation
                - Use proper modules
                - Implement proper validation
                - Follow proper structure
            """,
            '.v': """
                For Verilog Implementation:
                - Follow Verilog best practices
                - Use proper modules
                - Implement proper timing
                - Follow naming conventions
                - Add proper documentation
                - Use proper parameters
                - Implement proper validation
                - Follow proper structure
            """,
            '.sv': """
                For SystemVerilog Implementation:
                - Follow SystemVerilog best practices
                - Use proper classes
                - Implement proper interfaces
                - Follow naming conventions
                - Add proper documentation
                - Use proper assertions
                - Implement proper validation
                - Follow proper structure
            """,
            '.groovy': """
                For Groovy Implementation:
                - Follow Groovy best practices
                - Use proper closures
                - Implement proper error handling
                - Follow naming conventions
                - Add proper documentation
                - Use proper metaprogramming
                - Implement proper testing
                - Follow proper structure
            """,
            '.adb': """
                For Ada Implementation:
                - Follow Ada best practices
                - Use proper types
                - Implement proper error handling
                - Follow naming conventions
                - Add proper documentation
                - Use proper packages
                - Implement proper validation
                - Follow proper structure
            """,
            # Markup and Config
            '.toml': """
                For TOML Implementation:
                - Follow TOML best practices
                - Use proper formatting
                - Implement proper structure
                - Follow naming conventions
                - Add proper documentation
                - Use proper data types
                - Implement proper validation
                - Follow proper hierarchy
            """,
            '.ini': """
                For INI Implementation:
                - Follow INI best practices
                - Use proper sections
                - Implement proper structure
                - Follow naming conventions
                - Add proper documentation
                - Use proper values
                - Implement proper validation
                - Follow proper format
            """,
            '.cfg': """
                For Config Implementation:
                - Follow configuration best practices
                - Use proper structure
                - Implement proper validation
                - Follow naming conventions
                - Add proper documentation
                - Use proper values
                - Implement proper handling
                - Follow proper format
            """,
            '.conf': """
                For Config Implementation:
                - Follow configuration best practices
                - Use proper structure
                - Implement proper validation
                - Follow naming conventions
                - Add proper documentation
                - Use proper values
                - Implement proper handling
                - Follow proper format
            """,
            '.env': """
                For Environment Implementation:
                - Follow env file best practices
                - Use proper naming
                - Implement proper security
                - Follow conventions
                - Add proper documentation
                - Use proper values
                - Implement proper validation
                - Follow proper format
            """,
            '.properties': """
                For Properties Implementation:
                - Follow properties best practices
                - Use proper key-value pairs
                - Implement proper structure
                - Follow naming conventions
                - Add proper documentation
                - Use proper encoding
                - Implement proper validation
                - Follow proper format
            """,
            '.xhtml': """
                For XHTML Implementation:
                - Follow XHTML standards
                - Use proper elements
                - Implement proper structure
                - Follow W3C guidelines
                - Add proper documentation
                - Use proper attributes
                - Implement proper validation
                - Follow proper format
            """,
            '.rss': """
                For RSS Implementation:
                - Follow RSS standards
                - Use proper elements
                - Implement proper structure
                - Follow specifications
                - Add proper documentation
                - Use proper attributes
                - Implement proper validation
                - Follow proper format
            """,
            '.atom': """
                For Atom Implementation:
                - Follow Atom standards
                - Use proper elements
                - Implement proper structure
                - Follow specifications
                - Add proper documentation
                - Use proper attributes
                - Implement proper validation
                - Follow proper format
            """,
            '.pug': """
                For Pug Implementation:
                - Follow Pug best practices
                - Use proper indentation
                - Implement proper mixins
                - Follow naming conventions
                - Add proper documentation
                - Use proper attributes
                - Implement proper includes
                - Follow proper structure
            """,
            # Testing and Documentation
            '.spec.js': """
                For JavaScript Test Implementation:
                - Follow testing best practices
                - Use proper assertions
                - Implement proper mocks
                - Follow naming conventions
                - Add proper documentation
                - Use proper test structure
                - Implement proper coverage
                - Follow proper patterns
            """,
            '.test.js': """
                For JavaScript Test Implementation:
                - Follow testing best practices
                - Use proper assertions
                - Implement proper mocks
                - Follow naming conventions
                - Add proper documentation
                - Use proper test structure
                - Implement proper coverage
                - Follow proper patterns
            """,
            '.spec.ts': """
                For TypeScript Test Implementation:
                - Follow testing best practices
                - Use proper type definitions
                - Implement proper mocks
                - Follow naming conventions
                - Add proper documentation
                - Use proper test structure
                - Implement proper coverage
                - Follow proper patterns
            """,
            '.test.ts': """
                For TypeScript Test Implementation:
                - Follow testing best practices
                - Use proper type definitions
                - Implement proper mocks
                - Follow naming conventions
                - Add proper documentation
                - Use proper test structure
                - Implement proper coverage
                - Follow proper patterns
            """,
            '.feature': """
                For Cucumber Implementation:
                - Follow BDD best practices
                - Use proper Gherkin syntax
                - Implement proper scenarios
                - Follow naming conventions
                - Add proper documentation
                - Use proper step definitions
                - Implement proper validation
                - Follow proper structure
            """,
            '.rst': """
                For RST Documentation:
                - Follow RST best practices
                - Use proper formatting
                - Implement proper structure
                - Follow conventions
                - Add proper cross-references
                - Use proper directives
                - Implement proper sections
                - Follow proper hierarchy
            """,
            '.txt': """
                For Text Implementation:
                - Follow documentation best practices
                - Use proper formatting
                - Implement proper structure
                - Follow conventions
                - Add proper sections
                - Use proper organization
                - Implement proper formatting
                - Follow proper style
            """,
            '.log': """
                For Log Implementation:
                - Follow logging best practices
                - Use proper format
                - Implement proper levels
                - Follow conventions
                - Add proper timestamps
                - Use proper categories
                - Implement proper rotation
                - Follow proper structure
            """
        }

        # Get extension specific prompt or use default
        specific_prompt = extension_prompts.get(file_ext, """
            For Implementation:
            - Write clean, maintainable code
            - Follow language/framework best practices
            - Implement proper error handling
            - Create modular and reusable components
            - Optimize for performance
            - Add proper documentation
            - Follow project conventions
        """)

        user_prompt = base_prompt + specific_prompt
        user_prompt += f"{lazy_prompt}\n"
        user_prompt += f"Providing update for this {file_name}.\n"
        user_prompt += "NOTICE: Your response must ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        self.conversation_history.append({"role": "user", "content": user_prompt})

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
