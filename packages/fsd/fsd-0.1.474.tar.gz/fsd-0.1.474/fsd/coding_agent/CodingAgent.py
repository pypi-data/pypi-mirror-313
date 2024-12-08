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
        is_svg = file_ext == '.svg'

        # Read current file content
        current_file_content = read_file_content(file)
        if current_file_content:
            self.conversation_history.append({"role": "user", "content": f"Here is the current content of {file_name} that needs to be updated:\n{current_file_content}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this file content as context for the updates."})

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

        # Determine specialized prompt based on file extension
        specialized_prompt = ""
        if is_svg:
            specialized_prompt = (
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
        elif file_ext in ['.html', '.htm', '.vue', '.svelte']:
            specialized_prompt = (
                "As a world-class web developer focused on delivering exceptional quality:\n"
                "- Use semantic HTML5 elements with precision:\n"
                "  • <header>, <nav>, <main>, <article>, <section>, <aside>, <footer> for clear document structure\n"
                "  • <figure>, <figcaption> for image content with proper descriptions\n" 
                "  • <time> for standardized date/time formatting\n"
                "  • <mark>, <strong>, <em> for meaningful text emphasis\n"
                "  • Custom data-* attributes for component-specific metadata\n"
                "- Create bulletproof document structure:\n"
                "  • Single descriptive <h1> per page with proper heading hierarchy\n"
                "  • Logical content grouping matching visual design\n"
                "  • Clear separation of concerns between structure/style/behavior\n"
                "  • Consistent class naming matching existing patterns\n"
                "- Implement comprehensive accessibility:\n"
                "  • ARIA landmarks, labels, roles and states for screen readers\n"
                "  • Skip navigation links and visible keyboard focus states\n"
                "  • Descriptive alt text and aria-labels matching brand voice\n"
                "  • Form validation with clear error messaging\n"
                "  • Support for text resizing and high contrast modes\n"
                "  • Keyboard navigation matching existing patterns\n"
                "- Create responsive layouts with precision:\n"
                "  • Viewport meta tags optimized for devices\n"
                "  • CSS Grid/Flexbox matching existing grid system\n"
                "  • Consistent breakpoints across components\n"
                "  • Fluid typography scale matching brand guidelines\n"
                "  • Responsive images with art direction\n"
                "- Optimize for performance and SEO:\n"
                "  • Meta tags matching existing SEO strategy\n"
                "  • Structured data using established schemas\n"
                "  • Semantic heading structure for crawlability\n"
                "  • Lazy loading for images and components\n"
                "  • Critical CSS path optimization\n"
                "- Follow established component architecture:\n"
                "  • Reusable components matching existing patterns\n"
                "  • Strict props validation and documentation\n"
                "  • State management following project conventions\n"
                "  • Event handling with error boundaries\n"
                "  • Lifecycle hooks with cleanup\n"
                "- Implement robust form handling:\n"
                "  • Client/server validation matching requirements\n"
                "  • Clear error states matching design system\n"
                "  • Accessible form controls with ARIA\n"
                "  • Progressive enhancement for older browsers\n"
                "  • Form analytics and tracking\n"
                "- Add polished interactions:\n"
                "  • Smooth transitions matching existing animations\n"
                "  • Consistent loading states and spinners\n"
                "  • Toast notifications in brand style\n"
                "  • Modal dialogs following patterns\n"
                "  • Micro-interactions for feedback\n"
                "- Ensure total browser compatibility:\n"
                "  • Vendor prefixes for CSS\n"
                "  • Feature detection with fallbacks\n"
                "  • Polyfills for legacy support\n"
                "  • Graceful degradation strategy\n"
                "  • Cross-browser testing plan\n"
            )
        elif file_ext in ['.css', '.scss', '.sass', '.less', '.styl']:
            specialized_prompt = (
                "As a world-class CSS developer focused on pixel-perfect implementation:\n"
                "- Create flawless responsive designs:\n"
                "  • Mobile-first approach matching breakpoints\n"
                "  • Container queries for component-level responsiveness\n"
                "  • Fluid typography matching brand scale\n"
                "  • Logical properties for RTL support\n"
                "  • Custom properties matching design tokens\n"
                "- Master layout precision:\n"
                "  • CSS Grid matching existing grid system\n"
                "  • Flexbox for component layouts\n"
                "  • Subgrid for nested alignment\n"
                "  • Multi-column text layouts\n"
                "  • Masonry for dynamic content\n"
                "- Follow strict BEM methodology:\n"
                "  • Block__Element--Modifier matching conventions\n"
                "  • Flat selectors for performance\n"
                "  • Modular components with isolation\n"
                "  • Single responsibility principle\n"
                "  • Clear documentation\n"
                "- Optimize for maximum performance:\n"
                "  • Efficient selector specificity\n"
                "  • Critical CSS path optimization\n"
                "  • Containment for render hints\n"
                "  • Strategic will-change usage\n"
                "  • Layer optimization for paint\n"
                "- Create buttery-smooth animations:\n"
                "  • Hardware-accelerated transforms\n"
                "  • Optimized keyframe animations\n"
                "  • Transform/opacity for performance\n"
                "  • Motion paths matching design\n"
                "  • Scroll-based animations\n"
                "- Implement cutting-edge features:\n"
                "  • Custom properties for theming\n"
                "  • CSS modules for scoping\n"
                "  • CSS-in-JS when needed\n"
                "  • Feature queries with fallbacks\n"
                "  • Modern layout techniques\n"
                "- Guarantee cross-browser consistency:\n"
                "  • Automated vendor prefixing\n"
                "  • Graceful fallbacks\n"
                "  • Progressive enhancement\n"
                "  • Feature detection\n"
                "  • Thorough testing\n"
                "- Build maintainable systems:\n"
                "  • ITCSS architecture\n"
                "  • Design token system\n"
                "  • Utility class strategy\n"
                "  • Component isolation\n"
                "  • CSS module patterns\n"
            )
        elif file_ext in ['.js', '.jsx', '.mjs', '.cjs']:
            specialized_prompt = (
                "As a world-class JavaScript/React developer focused on excellence:\n"
                "- Leverage modern ES6+ features:\n"
                "  • Optional chaining for safe access\n"
                "  • Nullish coalescing for defaults\n"
                "  • Array methods for data transformation\n"
                "  • Async/await with proper error handling\n"
                "  • Module system best practices\n"
                "- Master React patterns:\n"
                "  • Pure functional components\n"
                "  • Custom hooks for reusability\n"
                "  • Strategic memoization\n"
                "  • Context API for state\n"
                "  • Error boundaries with recovery\n"
                "- Optimize for peak performance:\n"
                "  • Code splitting by route/component\n"
                "  • Tree shaking unused code\n"
                "  • Lazy loading with Suspense\n"
                "  • Virtualized lists for scale\n"
                "  • Web workers for computation\n"
                "- Implement robust state management:\n"
                "  • Redux/MobX following patterns\n"
                "  • Immutable updates with Immer\n"
                "  • Memoized selectors\n"
                "  • Typed action creators\n"
                "  • Custom middleware\n"
                "- Ensure bulletproof security:\n"
                "  • XSS prevention in rendering\n"
                "  • CSRF tokens in requests\n"
                "  • Input sanitization\n"
                "  • JWT handling\n"
                "  • Content security policy\n"
                "- Build reusable component systems:\n"
                "  • Compound components\n"
                "  • Render props patterns\n"
                "  • Higher-order components\n"
                "  • Custom hooks library\n"
                "  • Form controls\n"
                "- Handle side effects properly:\n"
                "  • Effect cleanup\n"
                "  • API integration\n"
                "  • WebSocket management\n"
                "  • Storage abstraction\n"
                "  • Service worker caching\n"
            )
        elif file_ext in ['.ts', '.tsx']:
            specialized_prompt = (
                "As a world-class TypeScript/Angular developer focused on type-safety:\n"
                "- Utilize advanced TypeScript:\n"
                "  • Generic constraints\n"
                "  • Utility type transformations\n"
                "  • Mapped type modifications\n"
                "  • Conditional type logic\n"
                "  • Template literal types\n"
                "- Implement Angular best practices:\n"
                "  • Smart/Dumb component separation\n"
                "  • Container pattern implementation\n"
                "  • Dependency injection hierarchy\n"
                "  • Change detection strategy\n"
                "  • Lifecycle hook management\n"
                "- Maximize performance:\n"
                "  • OnPush change detection\n"
                "  • Route-level code splitting\n"
                "  • Virtual scroll implementation\n"
                "  • Web worker offloading\n"
                "  • Server-side rendering\n"
                "- Implement robust state management:\n"
                "  • NgRx store architecture\n"
                "  • Side effect handling\n"
                "  • Memoized selectors\n"
                "  • Action creators\n"
                "  • State persistence\n"
                "- Create maintainable services:\n"
                "  • Singleton service pattern\n"
                "  • Hierarchical injection\n"
                "  • HTTP interceptors\n"
                "  • Route guards\n"
                "  • Data resolvers\n"
                "- Build solid routing:\n"
                "  • Lazy module loading\n"
                "  • Auth guards\n"
                "  • Child routes\n"
                "  • Data resolvers\n"
                "  • Navigation tracking\n"
                "- Implement robust forms:\n"
                "  • Reactive form validation\n"
                "  • Custom validators\n"
                "  • Dynamic form arrays\n"
                "  • Form builder patterns\n"
                "  • Error handling\n"
            )
        elif file_ext in ['.py', '.pyw']:
            specialized_prompt = (
                "As a world-class Python developer focused on quality:\n"
                "- Follow strict PEP standards:\n"
                "  • PEP 8 style conventions\n"
                "  • PEP 484 type annotations\n"
                "  • PEP 526 variable typing\n"
                "  • PEP 557 dataclasses\n"
                "  • PEP 585 generic types\n"
                "- Build clean architecture:\n"
                "  • SOLID principle adherence\n"
                "  • Dependency injection patterns\n"
                "  • Repository abstraction\n"
                "  • Service layer pattern\n"
                "  • Domain model design\n"
                "- Maximize performance:\n"
                "  • Generator optimization\n"
                "  • Async/await patterns\n"
                "  • Process pooling\n"
                "  • Strategic caching\n"
                "  • Memory profiling\n"
                "- Implement error handling:\n"
                "  • Custom exception hierarchy\n"
                "  • Context manager usage\n"
                "  • Structured logging\n"
                "  • Debug tooling\n"
                "  • Recovery strategies\n"
                "- Ensure maintainability:\n"
                "  • Comprehensive docstrings\n"
                "  • Complete type hints\n"
                "  • Unit test coverage\n"
                "  • API documentation\n"
                "  • Code organization\n"
                "- Enforce security:\n"
                "  • Input sanitization\n"
                "  • Secure configuration\n"
                "  • Auth implementation\n"
                "  • Permission checks\n"
                "  • Data encryption\n"
            )
        elif file_ext in ['.rs']:
            specialized_prompt = (
                "As a world-class Rust/Tauri developer focused on safety:\n"
                "- Master Rust fundamentals:\n"
                "  • Ownership semantics\n"
                "  • Lifetime annotations\n"
                "  • Trait implementations\n"
                "  • Smart pointer usage\n"
                "  • Thread safety patterns\n"
                "- Build Tauri features:\n"
                "  • Custom command APIs\n"
                "  • Window management\n"
                "  • System tray integration\n"
                "  • File system security\n"
                "  • IPC architecture\n"
                "- Optimize aggressively:\n"
                "  • Zero-cost abstractions\n"
                "  • Memory optimization\n"
                "  • Binary size reduction\n"
                "  • Async runtime tuning\n"
                "  • Native performance\n"
                "- Handle errors robustly:\n"
                "  • Result type usage\n"
                "  • Custom error types\n"
                "  • Error propagation\n"
                "  • Panic prevention\n"
                "  • Recovery logic\n"
                "- Implement security:\n"
                "  • Memory safety checks\n"
                "  • Thread safety guards\n"
                "  • Secure defaults\n"
                "  • Permission model\n"
                "  • Process isolation\n"
                "- Create thorough tests:\n"
                "  • Unit test coverage\n"
                "  • Integration testing\n"
                "  • Performance benchmarks\n"
                "  • Doc test examples\n"
                "  • Property testing\n"
            )
        elif file_ext in ['.go']:
            specialized_prompt = (
                "As a world-class Go developer focused on performance:\n"
                "- Master Go idioms:\n"
                "  • Interface composition\n"
                "  • Error handling patterns\n"
                "  • Goroutine management\n"
                "  • Channel communication\n"
                "  • Context usage\n"
                "- Build concurrent systems:\n"
                "  • Worker pools\n"
                "  • Fan-out/fan-in patterns\n"
                "  • Rate limiting\n"
                "  • Graceful shutdown\n"
                "  • Deadlock prevention\n"
                "- Optimize performance:\n"
                "  • Memory allocation\n"
                "  • Zero-copy operations\n"
                "  • CPU profiling\n"
                "  • Garbage collection tuning\n"
                "  • Benchmark-driven optimization\n"
                "- Implement microservices:\n"
                "  • gRPC services\n"
                "  • RESTful APIs\n"
                "  • Service discovery\n"
                "  • Circuit breaking\n"
                "  • Load balancing\n"
                "- Ensure reliability:\n"
                "  • Structured logging\n"
                "  • Metrics collection\n"
                "  • Distributed tracing\n"
                "  • Health checking\n"
                "  • Failure recovery\n"
            )
        elif file_ext in ['.R', '.Rmd']:
            specialized_prompt = (
                "As a world-class R developer focused on statistical computing:\n"
                "- Master tidyverse ecosystem:\n"
                "  • dplyr data manipulation\n"
                "  • ggplot2 visualization\n"
                "  • tidyr data cleaning\n"
                "  • purrr functional programming\n"
                "  • tibble data frames\n"
                "- Implement statistical methods:\n"
                "  • Regression analysis\n"
                "  • Time series modeling\n"
                "  • Hypothesis testing\n"
                "  • Bayesian inference\n"
                "  • Machine learning\n"
                "- Create reproducible research:\n"
                "  • R Markdown documents\n"
                "  • Shiny applications\n"
                "  • Package development\n"
                "  • Version control\n"
                "  • Documentation\n"
                "- Optimize performance:\n"
                "  • Vectorization\n"
                "  • Parallel processing\n"
                "  • Memory management\n"
                "  • C++ integration\n"
                "  • GPU acceleration\n"
            )
        elif file_ext in ['.swift']:
            specialized_prompt = (
                "As a world-class Swift developer focused on iOS:\n"
                "- Master Swift features:\n"
                "  • Protocol-oriented programming\n"
                "  • Value types and structs\n"
                "  • Generic constraints\n"
                "  • Property wrappers\n"
                "  • Result type handling\n"
                "- Build UI with SwiftUI:\n"
                "  • Declarative syntax\n"
                "  • View composition\n"
                "  • State management\n"
                "  • Animations\n"
                "  • Gestures\n"
                "- Implement app architecture:\n"
                "  • MVVM pattern\n"
                "  • Dependency injection\n"
                "  • Navigation flow\n"
                "  • Data persistence\n"
                "  • Networking layer\n"
                "- Ensure iOS integration:\n"
                "  • App lifecycle\n"
                "  • Background tasks\n"
                "  • Push notifications\n"
                "  • Deep linking\n"
                "  • Permissions\n"
            )
        elif file_ext in ['.kt']:
            specialized_prompt = (
                "As a world-class Kotlin developer focused on Android:\n"
                "- Master Kotlin features:\n"
                "  • Coroutines for async\n"
                "  • Flow for reactive\n"
                "  • Extension functions\n"
                "  • Data classes\n"
                "  • Sealed classes\n"
                "- Build UI with Jetpack Compose:\n"
                "  • Composable functions\n"
                "  • State hoisting\n"
                "  • Side effects\n"
                "  • Custom layouts\n"
                "  • Navigation\n"
                "- Implement app architecture:\n"
                "  • MVVM with Clean\n"
                "  • Repository pattern\n"
                "  • Use cases\n"
                "  • DI with Hilt\n"
                "  • Room database\n"
                "- Ensure Android integration:\n"
                "  • Lifecycle awareness\n"
                "  • WorkManager\n"
                "  • Notifications\n"
                "  • Permissions\n"
                "  • Deep links\n"
            )
        elif file_ext in ['.java']:
            specialized_prompt = (
                "As a world-class Java developer focused on enterprise:\n"
                "- Master Spring ecosystem:\n"
                "  • Spring Boot configuration\n"
                "  • Dependency injection\n"
                "  • AOP programming\n"
                "  • Transaction management\n"
                "  • Security implementation\n"
                "- Build microservices:\n"
                "  • RESTful APIs\n"
                "  • Service discovery\n"
                "  • Circuit breakers\n"
                "  • Message queues\n"
                "  • API gateway\n"
                "- Implement persistence:\n"
                "  • JPA/Hibernate\n"
                "  • Query optimization\n"
                "  • Cache strategies\n"
                "  • Connection pooling\n"
                "  • Migration management\n"
                "- Ensure scalability:\n"
                "  • Thread management\n"
                "  • Resource pooling\n"
                "  • Load balancing\n"
                "  • Clustering\n"
                "  • Monitoring\n"
            )
        elif file_ext in ['.ipynb']:
            specialized_prompt = (
                "As a world-class Data Science developer focused on insights:\n"
                "- Optimize data processing:\n"
                "  • Pandas vectorization\n"
                "  • NumPy optimization\n"
                "  • Dask scaling\n"
                "  • Data cleansing\n"
                "  • Feature engineering\n"
                "- Create clear visualizations:\n"
                "  • Matplotlib customization\n"
                "  • Seaborn styling\n"
                "  • Plotly interactions\n"
                "  • Bokeh dashboards\n"
                "  • Custom visualization\n"
                "- Maximize performance:\n"
                "  • Memory management\n"
                "  • Parallel processing\n"
                "  • GPU acceleration\n"
                "  • Caching strategy\n"
                "  • Code optimization\n"
                "- Implement ML/AI:\n"
                "  • Scikit-learn workflow\n"
                "  • Deep learning models\n"
                "  • Model validation\n"
                "  • Parameter tuning\n"
                "  • Cross-validation\n"
                "- Ensure reproducibility:\n"
                "  • Environment control\n"
                "  • Version tracking\n"
                "  • Data versioning\n"
                "  • Random seeds\n"
                "  • Documentation\n"
                "- Scale for big data:\n"
                "  • Chunked processing\n"
                "  • Stream handling\n"
                "  • Distributed compute\n"
                "  • Memory efficiency\n"
                "  • ETL pipelines\n"
            )
        else:
            specialized_prompt = (
                f"As a world-class {techStack} developer:\n"
                "For UI/UX Implementation:\n"
                "- Create stunning, elegant and clean designs:\n"
                "  • Use consistent spacing and padding throughout\n"
                "  • Follow visual hierarchy principles\n"
                "  • Implement proper whitespace and breathing room\n"
                "  • Ensure pixel-perfect alignment and positioning\n"
                "  • Use balanced color schemes and typography\n"
                "  • Create smooth visual flow and transitions\n"
                "- For Headers & Footers:\n"
                "  • If existing header/footer exists:\n"
                "    - Match exact styling, spacing and layout\n"
                "    - Use identical color schemes and typography\n"
                "    - Follow same responsive behavior\n"
                "    - Keep consistent navigation patterns\n"
                "    - Maintain same interactive elements\n"
                "  • If creating new header/footer:\n"
                "    - Design stunning, compelling layouts\n"
                "    - Add smooth hover animations\n"
                "    - Include elegant dropdown menus\n"
                "    - Create sticky/fixed positioning options\n"
                "    - Add scroll-triggered effects\n"
                "    - Implement mobile-friendly navigation\n"
                "    - Use modern glassmorphism/blur effects\n"
                "    - Add subtle parallax scrolling\n"
                "    - Include search functionality\n"
                "    - Optimize for all screen sizes\n"
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
                "- Maintain consistent style with existing codebase:\n"
                "  • Match header/footer structure and styling\n"
                "  • Use same navigation patterns and menus\n"
                "  • Follow established CSS class naming conventions\n"
                "  • Keep consistent color schemes and typography\n"
                "  • Reuse existing components and layouts\n"
                "  • Maintain same responsive breakpoints\n"
                "  • Follow project's CSS methodology (BEM, etc)\n"
                "  • Use identical grid systems and spacing\n"
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

        user_prompt = specialized_prompt + (
            f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}\n"
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