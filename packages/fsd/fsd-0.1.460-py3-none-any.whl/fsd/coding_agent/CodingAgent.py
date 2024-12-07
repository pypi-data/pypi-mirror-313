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
                - Follow UI/UX standards for semantic structure
                - Create consistent interfaces across browsers
                - Ensure accessibility compliance (WCAG 2.1)
                - Optimize for performance and SEO
                - Add meaningful interactions and states
                - Follow HTML5 best practices
                - Match existing document patterns
                - Use proper meta viewport settings
                - Implement proper Open Graph tags
                - Add proper favicon markup
                - Use proper language attributes
                - Follow progressive enhancement
                - Create stunning, elegant and clean markup
                - Use proper heading hierarchy and landmarks
                - Implement proper form validation UX
                - Add proper error messaging and states
                - Follow mobile-first responsive design
                - Use proper input types and attributes
                - Implement proper focus management
                - Add proper skip navigation links
                - Use proper table markup and captions
                - Follow proper list structure
                - Add proper form labels and hints
                - Implement proper dialog/modal markup
                - Use proper button vs link semantics
                - Add proper image alt text
                - Follow proper sectioning
                - Use proper time element markup
                - Implement proper video/audio controls
                - Add proper iframe titles
                - Use proper figure/figcaption
                - Follow proper article/section usage
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
                - Follow UI/UX standards for vector graphics
                - Create consistent visual style
                - Ensure accessibility compliance
                - Optimize performance and file size
                - Add meaningful interactions
                - Follow SVG best practices
                - Match existing design patterns
                - Use proper viewBox settings
                - Implement proper path optimization
                - Add proper title and desc elements
                - Use proper naming conventions
                - Follow progressive enhancement
                - Create pixel-perfect vector graphics
                - Use proper gradient definitions
                - Implement proper mask/clip paths
                - Add proper filter effects
                - Follow proper animation timing
                - Use proper transform origin
                - Implement proper symbol/use
                - Add proper marker elements
                - Use proper pattern fills
                - Follow proper text paths
                - Add proper event handlers
                - Implement proper responsive scaling
                - Use proper coordinate systems
                - Add proper metadata
                - Follow proper grouping logic
                - Use proper stroke properties
                - Implement proper shape morphing
                - Add proper hover states
                - Use proper path commands
                - Follow proper layer structure
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
                - Follow UI/UX standards for styling
                - Create consistent visual interfaces
                - Ensure accessibility compliance
                - Optimize performance and loading
                - Add meaningful interactions
                - Follow CSS best practices
                - Match existing style patterns
                - Use proper media queries
                - Implement proper vendor prefixes
                - Add proper fallbacks
                - Use proper specificity
                - Follow progressive enhancement
                - Create stunning visual designs
                - Use proper cascade layering
                - Implement proper container queries
                - Add proper scroll snap points
                - Follow proper CSS grid areas
                - Use proper aspect ratio boxes
                - Implement proper CSS shapes
                - Add proper CSS masks
                - Use proper CSS filters
                - Follow proper CSS variables scope
                - Add proper CSS counters
                - Implement proper CSS regions
                - Use proper CSS columns
                - Add proper CSS transforms
                - Follow proper CSS animations
                - Use proper CSS gradients
                - Implement proper CSS blend modes
                - Add proper CSS clipping paths
                - Use proper CSS custom properties
                - Follow proper CSS nesting
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
                - Follow UI/UX standards for styling
                - Create consistent visual interfaces
                - Ensure accessibility compliance
                - Optimize performance and output
                - Add meaningful interactions
                - Follow SCSS best practices
                - Match existing style patterns
                - Use proper media queries
                - Implement proper mixins
                - Add proper error handling
                - Use proper functions
                - Follow progressive enhancement
                - Create stunning visual designs
                - Use proper SCSS maps
                - Implement proper SCSS loops
                - Add proper SCSS conditionals
                - Follow proper SCSS modules
                - Use proper SCSS interpolation
                - Implement proper SCSS math
                - Add proper SCSS color functions
                - Use proper SCSS lists/maps
                - Follow proper SCSS imports
                - Add proper SCSS debugging
                - Implement proper SCSS testing
                - Use proper SCSS architecture
                - Add proper SCSS documentation
                - Follow proper SCSS patterns
                - Use proper SCSS utilities
                - Implement proper SCSS themes
                - Add proper SCSS variables
                - Use proper SCSS mixins
                - Follow proper SCSS structure
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
                - Follow UI/UX standards for styling
                - Create consistent visual interfaces
                - Ensure accessibility compliance
                - Optimize performance and output
                - Add meaningful interactions
                - Follow Sass best practices
                - Match existing style patterns
                - Use proper media queries
                - Implement proper mixins
                - Add proper error handling
                - Use proper functions
                - Follow progressive enhancement
                - Create stunning visual designs
                - Use proper Sass maps
                - Implement proper Sass loops
                - Add proper Sass conditionals
                - Follow proper Sass modules
                - Use proper Sass interpolation
                - Implement proper Sass math
                - Add proper Sass color functions
                - Use proper Sass lists/maps
                - Follow proper Sass imports
                - Add proper Sass debugging
                - Implement proper Sass testing
                - Use proper Sass architecture
                - Add proper Sass documentation
                - Follow proper Sass patterns
                - Use proper Sass utilities
                - Implement proper Sass themes
                - Add proper Sass variables
                - Use proper Sass mixins
                - Follow proper Sass structure
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
                - Follow UI/UX standards for interactivity
                - Create consistent behavior
                - Ensure accessibility compliance
                - Optimize performance and loading
                - Add meaningful interactions
                - Follow JS best practices
                - Match existing code patterns
                - Use proper event handling
                - Implement proper async/await
                - Add proper error boundaries
                - Use proper types
                - Follow progressive enhancement
                - Create stunning interactive features
                - Use proper JS modules
                - Implement proper JS classes
                - Add proper JS decorators
                - Follow proper JS promises
                - Use proper JS generators
                - Implement proper JS proxies
                - Add proper JS reflection
                - Use proper JS symbols
                - Follow proper JS iterators
                - Add proper JS maps/sets
                - Implement proper JS regex
                - Use proper JS dates
                - Add proper JS validation
                - Follow proper JS patterns
                - Use proper JS optimization
                - Implement proper JS security
                - Add proper JS documentation
                - Use proper JS debugging
                - Follow proper JS structure
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
                - Follow UI/UX standards for components
                - Create consistent component interfaces
                - Ensure accessibility compliance
                - Optimize performance and rendering
                - Add meaningful interactions
                - Follow React best practices
                - Match existing component patterns
                - Use proper hooks patterns
                - Implement proper state management
                - Add proper error handling
                - Use proper types
                - Follow progressive enhancement
                - Create stunning React components
                - Use proper React context
                - Implement proper React refs
                - Add proper React portals
                - Follow proper React suspense
                - Use proper React lazy loading
                - Implement proper React testing
                - Add proper React PropTypes
                - Use proper React events
                - Follow proper React patterns
                - Add proper React documentation
                - Implement proper React security
                - Use proper React optimization
                - Add proper React validation
                - Follow proper React structure
                - Use proper React architecture
                - Implement proper React routing
                - Add proper React forms
                - Use proper React styling
                - Follow proper React conventions
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
                - Follow UI/UX standards for typing
                - Create consistent type interfaces
                - Ensure type safety compliance
                - Optimize performance and compilation
                - Add meaningful type guards
                - Follow TS best practices
                - Match existing type patterns
                - Use proper generics
                - Implement proper interfaces
                - Add proper error types
                - Use proper utility types
                - Follow progressive enhancement
                - Create stunning type-safe code
                - Use proper TS decorators
                - Implement proper TS modules
                - Add proper TS namespaces
                - Follow proper TS mixins
                - Use proper TS enums
                - Implement proper TS classes
                - Add proper TS interfaces
                - Use proper TS types
                - Follow proper TS patterns
                - Add proper TS documentation
                - Implement proper TS testing
                - Use proper TS architecture
                - Add proper TS validation
                - Follow proper TS structure
                - Use proper TS optimization
                - Implement proper TS security
                - Add proper TS debugging
                - Use proper TS conventions
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
                - Follow UI/UX standards for components
                - Create consistent type interfaces
                - Ensure type safety compliance
                - Optimize performance and compilation
                - Add meaningful type guards
                - Follow TSX best practices
                - Match existing component patterns
                - Use proper generics
                - Implement proper interfaces
                - Add proper error types
                - Use proper utility types
                - Follow progressive enhancement
                - Create stunning type-safe components
                - Use proper TSX components
                - Implement proper TSX hooks
                - Add proper TSX context
                - Follow proper TSX patterns
                - Use proper TSX props
                - Implement proper TSX state
                - Add proper TSX events
                - Use proper TSX refs
                - Follow proper TSX lifecycle
                - Add proper TSX documentation
                - Implement proper TSX testing
                - Use proper TSX architecture
                - Add proper TSX validation
                - Follow proper TSX structure
                - Use proper TSX optimization
                - Implement proper TSX security
                - Add proper TSX debugging
                - Use proper TSX conventions
                - Follow proper TSX best practices
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
                - Follow data structure standards
                - Create consistent schemas
                - Ensure data integrity
                - Optimize parsing performance
                - Add meaningful validation
                - Follow JSON best practices
                - Match existing schema patterns
                - Use proper types
                - Implement proper validation
                - Add proper error messages
                - Use proper formatting
                - Follow schema standards
                - Create stunning data structures
                - Use proper JSON pointers
                - Implement proper JSON patch
                - Add proper JSON merge
                - Follow proper JSON path
                - Use proper JSON references
                - Implement proper JSON schema
                - Add proper JSON validation
                - Use proper JSON types
                - Follow proper JSON patterns
                - Add proper JSON documentation
                - Implement proper JSON testing
                - Use proper JSON architecture
                - Add proper JSON security
                - Follow proper JSON structure
                - Use proper JSON optimization
                - Implement proper JSON versioning
                - Add proper JSON debugging
                - Use proper JSON conventions
                - Follow proper JSON standards
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
                - Follow data structure standards
                - Create consistent schemas
                - Ensure data integrity
                - Optimize parsing performance
                - Add meaningful validation
                - Follow XML best practices
                - Match existing schema patterns
                - Use proper types
                - Implement proper validation
                - Add proper error messages
                - Use proper formatting
                - Follow schema standards
                - Create stunning XML structures
                - Use proper XML namespaces
                - Implement proper XML schema
                - Add proper XML validation
                - Follow proper XML path
                - Use proper XML transformations
                - Implement proper XML security
                - Add proper XML documentation
                - Use proper XML patterns
                - Follow proper XML structure
                - Add proper XML testing
                - Implement proper XML versioning
                - Use proper XML architecture
                - Add proper XML optimization
                - Follow proper XML conventions
                - Use proper XML encoding
                - Implement proper XML parsing
                - Add proper XML debugging
                - Use proper XML formatting
                - Follow proper XML standards
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
                - Follow configuration standards
                - Create consistent structure
                - Ensure data integrity
                - Optimize parsing performance
                - Add meaningful validation
                - Follow YAML best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error messages
                - Use proper formatting
                - Follow schema standards
                - Create stunning YAML structures
                - Use proper YAML anchors
                - Implement proper YAML aliases
                - Add proper YAML tags
                - Follow proper YAML flow
                - Use proper YAML scalars
                - Implement proper YAML sequences
                - Add proper YAML mappings
                - Use proper YAML inheritance
                - Follow proper YAML patterns
                - Add proper YAML documentation
                - Implement proper YAML testing
                - Use proper YAML architecture
                - Add proper YAML security
                - Follow proper YAML structure
                - Use proper YAML optimization
                - Implement proper YAML validation
                - Add proper YAML debugging
                - Use proper YAML conventions
                - Follow proper YAML standards
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
                - Follow configuration standards
                - Create consistent structure
                - Ensure data integrity
                - Optimize parsing performance
                - Add meaningful validation
                - Follow YAML best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error messages
                - Use proper formatting
                - Follow schema standards
                - Create stunning YAML structures
                - Use proper YAML anchors
                - Implement proper YAML aliases
                - Add proper YAML tags
                - Follow proper YAML flow
                - Use proper YAML scalars
                - Implement proper YAML sequences
                - Add proper YAML mappings
                - Use proper YAML inheritance
                - Follow proper YAML patterns
                - Add proper YAML documentation
                - Implement proper YAML testing
                - Use proper YAML architecture
                - Add proper YAML security
                - Follow proper YAML structure
                - Use proper YAML optimization
                - Implement proper YAML validation
                - Add proper YAML debugging
                - Use proper YAML conventions
                - Follow proper YAML standards
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
                - Follow data structure standards
                - Create consistent format
                - Ensure data integrity
                - Optimize parsing performance
                - Add meaningful validation
                - Follow CSV best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow file standards
                - Create stunning CSV structures
                - Use proper CSV parsing
                - Implement proper CSV writing
                - Add proper CSV validation
                - Follow proper CSV format
                - Use proper CSV escaping
                - Implement proper CSV headers
                - Add proper CSV documentation
                - Use proper CSV patterns
                - Follow proper CSV structure
                - Add proper CSV testing
                - Implement proper CSV security
                - Use proper CSV architecture
                - Add proper CSV optimization
                - Follow proper CSV conventions
                - Use proper CSV encoding
                - Implement proper CSV validation
                - Add proper CSV debugging
                - Use proper CSV formatting
                - Follow proper CSV standards
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
                - Follow documentation standards
                - Create consistent structure
                - Ensure content clarity
                - Optimize rendering performance
                - Add meaningful organization
                - Follow MD best practices
                - Match existing patterns
                - Use proper syntax
                - Implement proper hierarchy
                - Add proper metadata
                - Use proper formatting
                - Follow documentation standards
                - Create stunning documentation
                - Use proper MD headings
                - Implement proper MD lists
                - Add proper MD tables
                - Follow proper MD links
                - Use proper MD images
                - Implement proper MD code blocks
                - Add proper MD quotes
                - Use proper MD emphasis
                - Follow proper MD structure
                - Add proper MD testing
                - Implement proper MD validation
                - Use proper MD architecture
                - Add proper MD optimization
                - Follow proper MD conventions
                - Use proper MD extensions
                - Implement proper MD rendering
                - Add proper MD debugging
                - Use proper MD formatting
                - Follow proper MD standards
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
                - Follow UI/UX standards for backend
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow PHP best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning PHP applications
                - Use proper PHP namespaces
                - Implement proper PHP classes
                - Add proper PHP interfaces
                - Follow proper PHP traits
                - Use proper PHP generators
                - Implement proper PHP closures
                - Add proper PHP attributes
                - Use proper PHP patterns
                - Follow proper PHP structure
                - Add proper PHP testing
                - Implement proper PHP security
                - Use proper PHP architecture
                - Add proper PHP optimization
                - Follow proper PHP conventions
                - Use proper PHP debugging
                - Implement proper PHP validation
                - Add proper PHP documentation
                - Use proper PHP formatting
                - Follow proper PHP standards
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
                - Follow UI/UX standards for backend
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow ASP best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning ASP applications
                - Use proper ASP components
                - Implement proper ASP sessions
                - Add proper ASP caching
                - Follow proper ASP security
                - Use proper ASP validation
                - Implement proper ASP testing
                - Add proper ASP documentation
                - Use proper ASP patterns
                - Follow proper ASP structure
                - Add proper ASP optimization
                - Implement proper ASP debugging
                - Use proper ASP architecture
                - Add proper ASP conventions
                - Follow proper ASP standards
                - Use proper ASP formatting
                - Implement proper ASP validation
                - Add proper ASP security
                - Use proper ASP testing
                - Follow proper ASP practices
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
                - Follow UI/UX standards for backend
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow ASP.NET best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning ASP.NET applications
                - Use proper ASP.NET controls
                - Implement proper ASP.NET routing
                - Add proper ASP.NET security
                - Follow proper ASP.NET patterns
                - Use proper ASP.NET validation
                - Implement proper ASP.NET testing
                - Add proper ASP.NET documentation
                - Use proper ASP.NET architecture
                - Follow proper ASP.NET structure
                - Add proper ASP.NET optimization
                - Implement proper ASP.NET debugging
                - Use proper ASP.NET conventions
                - Add proper ASP.NET standards
                - Follow proper ASP.NET practices
                - Use proper ASP.NET formatting
                - Implement proper ASP.NET caching
                - Add proper ASP.NET security
                - Use proper ASP.NET testing
                - Follow proper ASP.NET patterns
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
                - Follow UI/UX standards for backend
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow JSP best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning JSP applications
                - Use proper JSP tags
                - Implement proper JSP actions
                - Add proper JSP security
                - Follow proper JSP patterns
                - Use proper JSP validation
                - Implement proper JSP testing
                - Add proper JSP documentation
                - Use proper JSP architecture
                - Follow proper JSP structure
                - Add proper JSP optimization
                - Implement proper JSP debugging
                - Use proper JSP conventions
                - Add proper JSP standards
                - Follow proper JSP practices
                - Use proper JSP formatting
                - Implement proper JSP caching
                - Add proper JSP security
                - Use proper JSP testing
                - Follow proper JSP patterns
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
                - Follow UI/UX standards for views
                - Create consistent templates
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow ERB best practices
                - Match existing patterns
                - Use proper helpers
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning ERB templates
                - Use proper ERB tags
                - Implement proper ERB helpers
                - Add proper ERB security
                - Follow proper ERB patterns
                - Use proper ERB validation
                - Implement proper ERB testing
                - Add proper ERB documentation
                - Use proper ERB architecture
                - Follow proper ERB structure
                - Add proper ERB optimization
                - Implement proper ERB debugging
                - Use proper ERB conventions
                - Add proper ERB standards
                - Follow proper ERB practices
                - Use proper ERB formatting
                - Implement proper ERB caching
                - Add proper ERB security
                - Use proper ERB testing
                - Follow proper ERB patterns
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
                - Follow UI/UX standards for components
                - Create consistent interfaces
                - Ensure accessibility compliance
                - Optimize performance and reactivity
                - Add meaningful interactions
                - Follow Vue best practices
                - Match existing patterns
                - Use proper composition
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning Vue components
                - Use proper Vue directives
                - Implement proper Vue mixins
                - Add proper Vue plugins
                - Follow proper Vue patterns
                - Use proper Vue slots
                - Implement proper Vue testing
                - Add proper Vue documentation
                - Use proper Vue architecture
                - Follow proper Vue structure
                - Add proper Vue optimization
                - Implement proper Vue debugging
                - Use proper Vue conventions
                - Add proper Vue standards
                - Follow proper Vue practices
                - Use proper Vue formatting
                - Implement proper Vue security
                - Add proper Vue validation
                - Use proper Vue testing
                - Follow proper Vue patterns
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
                - Follow UI/UX standards for components
                - Create consistent interfaces
                - Ensure accessibility compliance
                - Optimize performance and reactivity
                - Add meaningful interactions
                - Follow Svelte best practices
                - Match existing patterns
                - Use proper reactivity
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning Svelte components
                - Use proper Svelte stores
                - Implement proper Svelte actions
                - Add proper Svelte transitions
                - Follow proper Svelte patterns
                - Use proper Svelte slots
                - Implement proper Svelte testing
                - Add proper Svelte documentation
                - Use proper Svelte architecture
                - Follow proper Svelte structure
                - Add proper Svelte optimization
                - Implement proper Svelte debugging
                - Use proper Svelte conventions
                - Add proper Svelte standards
                - Follow proper Svelte practices
                - Use proper Svelte formatting
                - Implement proper Svelte security
                - Add proper Svelte validation
                - Use proper Svelte testing
                - Follow proper Svelte patterns
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
                - Follow UI/UX standards for templates
                - Create consistent interfaces
                - Ensure template inheritance
                - Optimize performance and caching
                - Add meaningful blocks
                - Follow Twig best practices
                - Match existing patterns
                - Use proper filters
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning Twig templates
                - Use proper Twig filters
                - Implement proper Twig functions
                - Add proper Twig macros
                - Follow proper Twig patterns
                - Use proper Twig blocks
                - Implement proper Twig testing
                - Add proper Twig documentation
                - Use proper Twig architecture
                - Follow proper Twig structure
                - Add proper Twig optimization
                - Implement proper Twig debugging
                - Use proper Twig conventions
                - Add proper Twig standards
                - Follow proper Twig practices
                - Use proper Twig formatting
                - Implement proper Twig security
                - Add proper Twig validation
                - Use proper Twig testing
                - Follow proper Twig patterns
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
                - Follow UI/UX standards for templates
                - Create consistent interfaces
                - Ensure template reuse
                - Optimize performance and caching
                - Add meaningful helpers
                - Follow HBS best practices
                - Match existing patterns
                - Use proper helpers
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning Handlebars templates
                - Use proper HBS helpers
                - Implement proper HBS partials
                - Add proper HBS blocks
                - Follow proper HBS patterns
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
                - Follow UI/UX standards for templates
                - Create consistent interfaces
                - Ensure template reuse
                - Optimize performance and caching
                - Add meaningful includes
                - Follow EJS best practices
                - Match existing patterns
                - Use proper includes
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning, elegant layouts
                - Use semantic HTML structure
                - Implement proper whitespace
                - Follow visual hierarchy
                - Add smooth transitions
                - Optimize template performance
                - Use proper EJS syntax
                - Add comprehensive error handling
                - Follow accessibility guidelines
                - Implement responsive design
                - Use proper CSS methodologies
                - Add proper SEO markup
                - Implement proper caching
                - Use proper template inheritance
                - Add proper security measures
                - Follow component architecture
                - Use proper data flow
                - Add proper testing
                - Implement proper debugging
                - Follow proper deployment
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
                - Follow UI/UX standards for templates
                - Create consistent interfaces
                - Ensure template reuse
                - Optimize performance and caching
                - Add meaningful filters
                - Follow Liquid best practices
                - Match existing patterns
                - Use proper filters
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Create stunning Shopify themes
                - Use proper section blocks
                - Implement proper schema
                - Follow Shopify standards
                - Add proper translations
                - Use proper asset handling
                - Implement proper checkout
                - Add proper cart functionality
                - Follow collection structure
                - Use proper product templates
                - Add proper search functionality
                - Implement proper filters
                - Use proper pagination
                - Add proper customer accounts
                - Follow proper blog structure
                - Use proper navigation
                - Add proper social media
                - Implement proper analytics
                - Use proper payment gateways
                - Follow proper shipping rules
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow Python best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper dependency injection
                - Implement proper logging
                - Add proper testing
                - Use proper ORM patterns
                - Follow microservices patterns
                - Implement proper authentication
                - Use proper caching strategies
                - Add proper monitoring
                - Follow proper deployment
                - Use proper containerization
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper security
                - Use proper encryption
                - Add proper backup strategies
                - Follow proper scaling
                - Use proper load balancing
                - Implement proper failover
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
                - Follow data science standards
                - Create consistent analysis
                - Ensure reproducibility
                - Optimize performance
                - Add meaningful validation
                - Follow R best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper statistical methods
                - Implement proper data cleaning
                - Add proper visualization
                - Use proper machine learning
                - Follow proper modeling
                - Implement proper feature engineering
                - Use proper cross-validation
                - Add proper model evaluation
                - Follow proper deployment
                - Use proper package management
                - Implement proper version control
                - Add proper documentation
                - Use proper data import/export
                - Follow proper data transformation
                - Implement proper data validation
                - Use proper parallel processing
                - Add proper memory management
                - Follow proper project structure
                - Use proper debugging tools
                - Implement proper logging
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow Java best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper JVM tuning
                - Implement proper garbage collection
                - Add proper memory management
                - Use proper threading
                - Follow proper microservices
                - Implement proper security
                - Use proper logging
                - Add proper monitoring
                - Follow proper deployment
                - Use proper containerization
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper testing
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and coroutines
                - Add meaningful validation
                - Follow Kotlin best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper functional programming
                - Implement proper collections
                - Add proper scope functions
                - Use proper delegation
                - Follow proper Android patterns
                - Implement proper Jetpack
                - Use proper navigation
                - Add proper dependency injection
                - Follow proper MVVM
                - Use proper data binding
                - Implement proper testing
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper CI/CD
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure type safety
                - Optimize performance and concurrency
                - Add meaningful validation
                - Follow Scala best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper pattern matching
                - Implement proper implicits
                - Add proper type classes
                - Use proper monads
                - Follow proper Akka patterns
                - Implement proper actors
                - Use proper streams
                - Add proper reactive programming
                - Follow proper Play framework
                - Use proper dependency injection
                - Implement proper testing
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper CI/CD
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and async
                - Add meaningful validation
                - Follow C# best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper garbage collection
                - Implement proper memory management
                - Add proper threading
                - Use proper Task Parallel Library
                - Follow proper ASP.NET Core
                - Implement proper Entity Framework
                - Use proper logging
                - Add proper monitoring
                - Follow proper deployment
                - Use proper containerization
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper testing
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and goroutines
                - Add meaningful validation
                - Follow Go best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper memory management
                - Implement proper garbage collection
                - Add proper concurrency patterns
                - Use proper channels
                - Follow proper microservices
                - Implement proper logging
                - Use proper monitoring
                - Add proper tracing
                - Follow proper deployment
                - Use proper containerization
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper testing
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance and caching
                - Add meaningful validation
                - Follow Ruby best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper garbage collection
                - Implement proper memory management
                - Add proper concurrency
                - Use proper threading
                - Follow proper Rails patterns
                - Implement proper ActiveRecord
                - Use proper logging
                - Add proper monitoring
                - Follow proper deployment
                - Use proper containerization
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper testing
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure security compliance
                - Optimize performance
                - Add meaningful validation
                - Follow Perl best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper memory management
                - Implement proper garbage collection
                - Add proper threading
                - Use proper concurrency
                - Follow proper CGI patterns
                - Implement proper logging
                - Use proper monitoring
                - Add proper debugging
                - Follow proper deployment
                - Use proper containerization
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper testing
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow shell standards
                - Create consistent scripts
                - Ensure security compliance
                - Optimize performance
                - Add meaningful validation
                - Follow shell best practices
                - Match existing patterns
                - Use proper variables
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper process management
                - Implement proper signal handling
                - Add proper file handling
                - Use proper string manipulation
                - Follow proper security
                - Implement proper permissions
                - Use proper environment
                - Add proper debugging
                - Follow proper deployment
                - Use proper version control
                - Implement proper testing
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper logging
                - Use proper monitoring
                - Add proper backup
                - Follow proper recovery
                - Use proper cleanup
                - Implement proper maintenance
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
                - Follow batch standards
                - Create consistent scripts
                - Ensure security compliance
                - Optimize performance
                - Add meaningful validation
                - Follow batch best practices
                - Match existing patterns
                - Use proper variables
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper process management
                - Implement proper error levels
                - Add proper file handling
                - Use proper string manipulation
                - Follow proper security
                - Implement proper permissions
                - Use proper environment
                - Add proper debugging
                - Follow proper deployment
                - Use proper version control
                - Implement proper testing
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper logging
                - Use proper monitoring
                - Add proper backup
                - Follow proper recovery
                - Use proper cleanup
                - Implement proper maintenance
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
                - Follow PowerShell standards
                - Create consistent scripts
                - Ensure security compliance
                - Optimize performance
                - Add meaningful validation
                - Follow PS best practices
                - Match existing patterns
                - Use proper variables
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper cmdlets
                - Implement proper pipeline
                - Add proper modules
                - Use proper remoting
                - Follow proper security
                - Implement proper permissions
                - Use proper profiles
                - Add proper debugging
                - Follow proper deployment
                - Use proper version control
                - Implement proper testing
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper logging
                - Use proper monitoring
                - Add proper backup
                - Follow proper recovery
                - Use proper cleanup
                - Implement proper maintenance
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
                - Follow backend standards
                - Create consistent APIs
                - Ensure memory safety
                - Optimize performance
                - Add meaningful validation
                - Follow Rust best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper memory management
                - Implement proper concurrency
                - Add proper async/await
                - Use proper macros
                - Follow proper patterns
                - Implement proper logging
                - Use proper monitoring
                - Add proper debugging
                - Follow proper deployment
                - Use proper containerization
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper version control
                - Follow proper branching
                - Implement proper testing
                - Use proper build tools
                - Add proper dependency management
                - Follow proper project structure
                - Use proper debugging
                - Implement proper profiling
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
                - Follow scripting standards
                - Create consistent modules
                - Ensure performance
                - Optimize memory usage
                - Add meaningful validation
                - Follow Lua best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper coroutines
                - Implement proper metatables
                - Add proper garbage collection
                - Use proper modules
                - Follow proper patterns
                - Implement proper logging
                - Use proper debugging
                - Add proper profiling
                - Follow proper deployment
                - Use proper version control
                - Implement proper testing
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper error handling
                - Use proper memory management
                - Add proper optimization
                - Follow proper security
                - Use proper sandboxing
                - Implement proper integration
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
                - Follow UI/UX standards for iOS
                - Create consistent interfaces
                - Ensure accessibility compliance
                - Optimize performance and memory
                - Add meaningful interactions
                - Follow Swift best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper optionals
                - Implement proper generics
                - Add proper protocols
                - Use proper extensions
                - Follow proper patterns
                - Implement proper logging
                - Use proper debugging
                - Add proper testing
                - Follow proper deployment
                - Use proper version control
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper error handling
                - Use proper memory management
                - Add proper optimization
                - Follow proper security
                - Use proper encryption
                - Implement proper authentication
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
                - Follow UI/UX standards for iOS
                - Create consistent interfaces
                - Ensure accessibility compliance
                - Optimize performance and memory
                - Add meaningful interactions
                - Follow ObjC best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper memory management
                - Implement proper ARC
                - Add proper protocols
                - Use proper categories
                - Follow proper patterns
                - Implement proper logging
                - Use proper debugging
                - Add proper testing
                - Follow proper deployment
                - Use proper version control
                - Implement proper CI/CD
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper error handling
                - Use proper memory management
                - Add proper optimization
                - Follow proper security
                - Use proper encryption
                - Implement proper authentication
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
                - Follow data science standards
                - Create consistent analysis
                - Ensure reproducibility
                - Optimize computation
                - Add meaningful visualization
                - Follow Jupyter best practices
                - Match existing patterns
                - Use proper libraries
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper data cleaning
                - Implement proper EDA
                - Add proper feature engineering
                - Use proper modeling
                - Follow proper evaluation
                - Implement proper validation
                - Use proper visualization
                - Add proper documentation
                - Follow proper deployment
                - Use proper version control
                - Implement proper testing
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper logging
                - Use proper monitoring
                - Add proper optimization
                - Follow proper security
                - Use proper data handling
                - Implement proper backup
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
                - Follow data science standards
                - Create consistent analysis
                - Ensure reproducibility
                - Optimize computation
                - Add meaningful visualization
                - Follow RMD best practices
                - Match existing patterns
                - Use proper packages
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper data cleaning
                - Implement proper EDA
                - Add proper feature engineering
                - Use proper modeling
                - Follow proper evaluation
                - Implement proper validation
                - Use proper visualization
                - Add proper documentation
                - Follow proper deployment
                - Use proper version control
                - Implement proper testing
                - Add proper documentation
                - Use proper branching
                - Follow proper project structure
                - Implement proper logging
                - Use proper monitoring
                - Add proper optimization
                - Follow proper security
                - Use proper data handling
                - Implement proper backup
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
                - Follow database standards
                - Create consistent schemas
                - Ensure data integrity
                - Optimize query execution
                - Add meaningful indices
                - Follow SQL best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper joins
                - Implement proper subqueries
                - Add proper views
                - Use proper functions
                - Follow proper triggers
                - Implement proper procedures
                - Use proper partitioning
                - Add proper backup
                - Follow proper recovery
                - Use proper replication
                - Implement proper monitoring
                - Add proper documentation
                - Use proper version control
                - Follow proper deployment
                - Implement proper security
                - Use proper access control
                - Add proper auditing
                - Follow proper maintenance
                - Use proper optimization
                - Implement proper cleanup
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
                - Follow database standards
                - Create consistent schemas
                - Ensure data integrity
                - Optimize performance
                - Add meaningful indices
                - Follow DB best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper normalization
                - Implement proper relationships
                - Add proper constraints
                - Use proper triggers
                - Follow proper procedures
                - Implement proper functions
                - Use proper views
                - Add proper indices
                - Follow proper partitioning
                - Use proper replication
                - Implement proper backup
                - Add proper recovery
                - Use proper monitoring
                - Follow proper security
                - Implement proper access control
                - Use proper auditing
                - Add proper maintenance
                - Follow proper optimization
                - Use proper cleanup
                - Implement proper archiving
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
                - Follow database standards
                - Create consistent schemas
                - Ensure data integrity
                - Optimize performance
                - Add meaningful indices
                - Follow DBF best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper field types
                - Implement proper indexing
                - Add proper validation
                - Use proper relationships
                - Follow proper backup
                - Implement proper recovery
                - Use proper maintenance
                - Add proper optimization
                - Follow proper security
                - Use proper access control
                - Implement proper auditing
                - Add proper documentation
                - Use proper version control
                - Follow proper deployment
                - Implement proper monitoring
                - Use proper cleanup
                - Add proper archiving
                - Follow proper migration
                - Use proper conversion
                - Implement proper integration
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
                - Follow data standards
                - Create consistent schemas
                - Ensure data integrity
                - Optimize storage
                - Add meaningful partitioning
                - Follow Parquet best practices
                - Match existing patterns
                - Use proper types
                - Implement proper validation
                - Add proper error handling
                - Use proper formatting
                - Follow coding standards
                - Use proper compression
                - Implement proper encoding
                - Add proper schema evolution
                - Use proper partitioning
                - Follow proper statistics
                - Implement proper metadata
                - Use proper column pruning
                - Add proper predicate pushdown
                - Follow proper optimization
                - Use proper memory management
                - Implement proper parallel processing
                - Add proper documentation
                - Use proper version control
                - Follow proper deployment
                - Implement proper monitoring
                - Use proper backup
                - Add proper recovery
                - Follow proper security
                - Use proper access control
                - Implement proper auditing
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
                - Use chunking for large datasets
                - Implement proper metadata
                - Follow hierarchical structure
                - Add proper indexing
                - Optimize memory usage
                - Use proper data types
                - Add proper error recovery
                - Follow naming conventions
                - Ensure data consistency
                - Implement proper backup
                - Use proper caching
                - Add proper versioning
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
                - Use protocol version properly
                - Add proper error recovery
                - Implement proper versioning
                - Follow security guidelines
                - Use proper data structures
                - Add proper type checking
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize performance
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
                - Use protocol version properly
                - Add proper error recovery
                - Implement proper versioning
                - Follow security guidelines
                - Use proper data structures
                - Add proper type checking
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize performance
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
                - Use proper encoding
                - Add proper metadata
                - Implement proper indexing
                - Follow data structure
                - Use proper compression
                - Add proper error handling
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize performance
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
                - Use proper encoding
                - Add proper metadata
                - Implement proper indexing
                - Follow data structure
                - Use proper compression
                - Add proper error handling
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize performance
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
                - Use proper matrix operations
                - Add proper error handling
                - Implement proper vectorization
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper toolboxes
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper compression
                - Add proper metadata
                - Implement proper indexing
                - Follow data structure
                - Use proper memory mapping
                - Add proper error handling
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize storage
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
                - Use proper encoding
                - Add proper metadata
                - Implement proper indexing
                - Follow data structure
                - Use proper memory mapping
                - Add proper error handling
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize storage
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
                - Use proper encoding
                - Add proper metadata
                - Implement proper indexing
                - Follow data structure
                - Use proper parsing
                - Add proper error handling
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize performance
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
                - Use proper encoding
                - Add proper metadata
                - Implement proper indexing
                - Follow data structure
                - Use proper compression
                - Add proper error handling
                - Ensure data consistency
                - Implement proper backup
                - Use proper memory management
                - Add proper logging
                - Follow best practices
                - Optimize performance
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
                - Use proper macros
                - Add proper error handling
                - Implement proper functions
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper libraries
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper macros
                - Add proper error recovery
                - Implement proper functions
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper packages
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper formatting
                - Add proper error recovery
                - Implement proper logic
                - Follow coding standards
                - Use proper variables
                - Add proper debugging
                - Ensure file consistency
                - Implement proper testing
                - Use proper includes
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper macros
                - Add proper error recovery
                - Implement proper functions
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper packages
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use smart pointers
                - Add proper exception handling
                - Implement proper inheritance
                - Follow SOLID principles
                - Use proper design patterns
                - Add proper unit tests
                - Ensure thread safety
                - Implement proper logging
                - Use proper namespaces
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper structs
                - Add proper error checking
                - Implement proper functions
                - Follow coding standards
                - Use proper memory allocation
                - Add proper debugging
                - Ensure code safety
                - Implement proper testing
                - Use proper macros
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper forward declarations
                - Add proper comments
                - Implement proper templates
                - Follow coding standards
                - Use proper visibility
                - Add proper versioning
                - Ensure header safety
                - Implement proper testing
                - Use proper namespaces
                - Add proper documentation
                - Follow best practices
                - Optimize includes
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
                - Use proper forward declarations
                - Add proper comments
                - Implement proper classes
                - Follow coding standards
                - Use proper visibility
                - Add proper versioning
                - Ensure header safety
                - Implement proper testing
                - Use proper namespaces
                - Add proper documentation
                - Follow best practices
                - Optimize includes
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
                - Use proper memory management
                - Add proper error handling
                - Implement proper functions
                - Follow coding standards
                - Use proper variables
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper hardware
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper async/await
                - Add proper error boundaries
                - Implement proper routing
                - Follow widget lifecycle
                - Use proper providers
                - Add proper animations
                - Ensure code efficiency
                - Implement proper testing
                - Use proper packages
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper exception handling
                - Add proper logging
                - Implement proper functions
                - Follow coding standards
                - Use proper variables
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper modules
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper data types
                - Add proper error handling
                - Implement proper functions
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper libraries
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper units
                - Add proper error recovery
                - Implement proper functions
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper modules
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper addressing modes
                - Add proper error handling
                - Implement proper procedures
                - Follow coding standards
                - Use proper stack management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper macros
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper recursion
                - Add proper error handling
                - Implement proper functions
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper libraries
                - Add proper comments
                - Follow best practices
                - Optimize algorithms
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
                - Use proper always blocks
                - Add proper error checking
                - Implement proper functions
                - Follow coding standards
                - Use proper memory elements
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper libraries
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper packages
                - Add proper coverage
                - Implement proper verification
                - Follow coding standards
                - Use proper constraints
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper libraries
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper builders
                - Add proper logging
                - Implement proper DSLs
                - Follow coding standards
                - Use proper traits
                - Add proper debugging
                - Ensure code efficiency
                - Implement proper testing
                - Use proper libraries
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper generics
                - Add proper exception handling
                - Implement proper tasking
                - Follow coding standards
                - Use proper memory management
                - Add proper debugging
                - Ensure code safety
                - Implement proper testing
                - Use proper libraries
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper tables
                - Add proper comments
                - Implement proper arrays
                - Follow specification
                - Use proper quoting
                - Add proper organization
                - Ensure file consistency
                - Implement proper nesting
                - Use proper syntax
                - Add proper documentation
                - Follow best practices
                - Optimize structure
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
                - Use proper keys
                - Add proper comments
                - Implement proper hierarchy
                - Follow specification
                - Use proper escaping
                - Add proper organization
                - Ensure file consistency
                - Implement proper includes
                - Use proper syntax
                - Add proper documentation
                - Follow best practices
                - Optimize structure
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
                - Use proper sections
                - Add proper comments
                - Implement proper hierarchy
                - Follow specification
                - Use proper types
                - Add proper organization
                - Ensure file consistency
                - Implement proper includes
                - Use proper syntax
                - Add proper documentation
                - Follow best practices
                - Optimize structure
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
                - Use proper sections
                - Add proper comments
                - Implement proper hierarchy
                - Follow specification
                - Use proper types
                - Add proper organization
                - Ensure file consistency
                - Implement proper includes
                - Use proper syntax
                - Add proper documentation
                - Follow best practices
                - Optimize structure
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
                - Use proper variables
                - Add proper comments
                - Implement proper structure
                - Follow specification
                - Use proper quoting
                - Add proper organization
                - Ensure file consistency
                - Implement proper includes
                - Use proper syntax
                - Add proper documentation
                - Follow best practices
                - Optimize structure
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
                - Use proper escaping
                - Add proper comments
                - Implement proper hierarchy
                - Follow specification
                - Use proper types
                - Add proper organization
                - Ensure file consistency
                - Implement proper includes
                - Use proper syntax
                - Add proper documentation
                - Follow best practices
                - Optimize structure
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
                - Use proper DOCTYPE
                - Add proper metadata
                - Implement proper semantics
                - Follow accessibility
                - Use proper encoding
                - Add proper organization
                - Ensure markup validity
                - Implement proper CSS
                - Use proper namespaces
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper channel
                - Add proper items
                - Implement proper feeds
                - Follow syndication
                - Use proper encoding
                - Add proper organization
                - Ensure feed validity
                - Implement proper dates
                - Use proper namespaces
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper feed
                - Add proper entries
                - Implement proper links
                - Follow syndication
                - Use proper encoding
                - Add proper organization
                - Ensure feed validity
                - Implement proper dates
                - Use proper namespaces
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper filters
                - Add proper interpolation
                - Implement proper extends
                - Follow templating
                - Use proper variables
                - Add proper organization
                - Ensure template validity
                - Implement proper blocks
                - Use proper conditionals
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper describes
                - Add proper before/after
                - Implement proper spies
                - Follow BDD/TDD
                - Use proper async
                - Add proper setup
                - Ensure test isolation
                - Implement proper cleanup
                - Use proper fixtures
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper describes
                - Add proper before/after
                - Implement proper spies
                - Follow BDD/TDD
                - Use proper async
                - Add proper setup
                - Ensure test isolation
                - Implement proper cleanup
                - Use proper fixtures
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper interfaces
                - Add proper before/after
                - Implement proper spies
                - Follow BDD/TDD
                - Use proper async
                - Add proper setup
                - Ensure test isolation
                - Implement proper cleanup
                - Use proper fixtures
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper interfaces
                - Add proper before/after
                - Implement proper spies
                - Follow BDD/TDD
                - Use proper async
                - Add proper setup
                - Ensure test isolation
                - Implement proper cleanup
                - Use proper fixtures
                - Add proper comments
                - Follow best practices
                - Optimize performance
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
                - Use proper features
                - Add proper backgrounds
                - Implement proper hooks
                - Follow specification
                - Use proper tags
                - Add proper organization
                - Ensure scenario isolation
                - Implement proper steps
                - Use proper parameters
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper roles
                - Add proper tables
                - Implement proper lists
                - Follow specification
                - Use proper links
                - Add proper organization
                - Ensure document validity
                - Implement proper includes
                - Use proper syntax
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper paragraphs
                - Add proper headings
                - Implement proper lists
                - Follow specification
                - Use proper spacing
                - Add proper organization
                - Ensure readability
                - Implement proper hierarchy
                - Use proper emphasis
                - Add proper comments
                - Follow best practices
                - Optimize structure
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
                - Use proper severity
                - Add proper context
                - Implement proper filtering
                - Follow specification
                - Use proper formatting
                - Add proper organization
                - Ensure searchability
                - Implement proper retention
                - Use proper fields
                - Add proper metadata
                - Follow best practices
                - Optimize structure
            """
        }

        # Get extension specific prompt or use default
        specific_prompt = extension_prompts.get(file_ext, """
            For UI/UX Implementation:
            - Create stunning, elegant and clean designs:
              • Use consistent spacing and padding throughout
              • Follow visual hierarchy principles
              • Implement proper whitespace and breathing room
              • Ensure pixel-perfect alignment and positioning
              • Use balanced color schemes and typography
              • Create smooth visual flow and transitions
            - For Headers & Footers:
              • If existing header/footer exists:
                - Match exact styling, spacing and layout
                - Use identical color schemes and typography
                - Follow same responsive behavior
                - Keep consistent navigation patterns
                - Maintain same interactive elements
              • If creating new header/footer:
                - Design stunning, compelling layouts
                - Add smooth hover animations
                - Include elegant dropdown menus
                - Create sticky/fixed positioning options
                - Add scroll-triggered effects
                - Implement mobile-friendly navigation
                - Use modern glassmorphism/blur effects
                - Add subtle parallax scrolling
                - Include search functionality
                - Optimize for all screen sizes
            - Follow UI/UX standards for each tech stack:
              • Web: Use semantic HTML5, ARIA, CSS Grid/Flexbox
              • React/Vue: Component-based architecture, hooks/composition API
              • Mobile: Follow iOS/Material Design guidelines
              • Desktop: Use native UI components and patterns
            - Create consistent interfaces across platforms:
              • Implement responsive/adaptive layouts
              • Support mobile, tablet, desktop breakpoints
              • Use relative units (rem, em, %) over pixels
              • Ensure consistent spacing across viewports
              • Maintain visual harmony at all sizes
            - Perfect visual details and polish:
              • Precise padding and margins using design system
              • Consistent component spacing and alignment
              • Proper visual rhythm and balance
              • Refined typography and font scaling
              • Optimized imagery and icons
            - Ensure accessibility compliance:
              • WCAG 2.1 AA standards
              • Proper heading structure and landmarks
              • Keyboard navigation and screen readers
              • Sufficient color contrast ratios
            - Optimize performance:
              • Lazy loading and code splitting
              • Asset optimization and caching
              • Virtual scrolling for long lists
              • Optimized animations and transitions
            - Add meaningful interactions:
              • Loading states and transitions
              • Form validation with clear feedback
              • Error handling with recovery options
              • Micro-interactions and hover states
              • Smooth page transitions
            - Follow tech stack best practices:
              • Web: BEM/SMACSS CSS, Progressive Enhancement
              • React: Hooks patterns, Context API usage
              • Vue: Composition API, State management
              • Mobile: Platform UI guidelines, Native features
            - Maintain consistent style with existing codebase:
              • Match header/footer structure and styling
              • Use same navigation patterns and menus
              • Follow established CSS class naming conventions
              • Keep consistent color schemes and typography
              • Reuse existing components and layouts
              • Maintain same responsive breakpoints
              • Follow project's CSS methodology (BEM, etc)
              • Use identical grid systems and spacing

            For Architecture & Code Quality:
            - Write clean, self-documenting code following DRY/KISS principles
            - Use meaningful names reflecting domain concepts
            - Structure code for maximum maintainability (SOLID principles)
            - Implement proper separation of concerns
            - Use appropriate design patterns (Factory, Strategy, Observer etc)
            - Follow clean architecture principles
            - Add comprehensive documentation

            For Performance & Reliability:
            - Optimize algorithmic complexity (time/space)
            - Implement proper caching strategies
            - Use efficient data structures
            - Add comprehensive error handling with recovery
            - Ensure thread-safety and handle race conditions
            - Implement retry mechanisms for external services
            - Add proper logging and monitoring hooks

            For Security & Data Integrity:
            - Follow security best practices (OWASP)
            - Implement proper input validation and sanitization
            - Use parameterized queries to prevent injection
            - Add proper authentication/authorization checks
            - Implement secure session management
            - Follow principle of least privilege
            - Ensure data consistency and referential integrity

            For Testing & Quality Assurance:
            - Write comprehensive unit tests with good coverage
            - Add integration and e2e tests where needed
            - Follow TDD/BDD practices
            - Include performance and load tests
            - Add security and penetration tests
            - Implement proper test data management
            - Visual regression testing for UI components

            For Code Correctness & Error Prevention:
            - Follow strict type checking and validation
            - Use proper null/undefined checks
            - Handle all edge cases and error conditions
            - Validate function parameters and return values
            - Use TypeScript/static typing where possible
            - Implement proper error boundaries
            - Add runtime checks and assertions

            For Syntax & Language Features:
            - Use modern language features correctly
            - Follow language-specific best practices
            - Implement proper async/await patterns
            - Use correct module import/export syntax
            - Follow framework-specific conventions
            - Use appropriate data structures
            - Implement proper memory management

            For Logic & Business Rules:
            - Validate all business logic thoroughly
            - Handle all possible states and transitions
            - Implement proper data validation rules
            - Add comprehensive error messages
            - Follow domain-driven design principles
            - Ensure consistent state management
            - Add proper logging for debugging
        """)

        user_prompt = base_prompt + specific_prompt
        user_prompt += f"{lazy_prompt}\n"
        user_prompt += f"Providing update for this {file_name}.\n"
        user_prompt += "NOTICE: Your response must ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        self.conversation_history.append({"role": "user", "content": user_prompt})

        # Add check for SVG files
        is_svg = file_ext.lower() == '.svg'

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
