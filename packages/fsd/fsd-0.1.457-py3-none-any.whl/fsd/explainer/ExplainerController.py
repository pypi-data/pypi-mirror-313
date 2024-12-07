from .ExplainablePrePromptAgent import ExplainablePrePromptAgent
from .GeneralExplainerAgent import GeneralExplainerAgent
from .ExplainableFileFinderAgent import ExplainableFileFinderAgent
from .MainExplainerAgent import MainExplainerAgent
from .ExplainableActionCheckAgent import ExplainableActionCheckAgent
from fsd.coding_agent.ControllerAgent import ControllerAgent
from fsd.log.logger_config import get_logger
from fsd.Crawler.CrawlerAgent import CrawlerAgent
from fsd.Crawler.CrawlerTaskPlanner import CrawlerTaskPlanner
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
from fsd.util.utils import parse_payload
logger = get_logger(__name__)

class ExplainerController:

    def __init__(self, repo):
        self.repo = repo
        self.preprompt = ExplainablePrePromptAgent(repo)
        self.normalExplainer = GeneralExplainerAgent(repo)
        self.mainExplainer = MainExplainerAgent(repo)
        self.fileFinder = ExplainableFileFinderAgent(repo)
        self.crawler = CrawlerAgent()
        self.crawlerPlaner = CrawlerTaskPlanner(repo)
        self.imageAgent = PromptImageUrlAgent(repo)
        self.actionCheck = ExplainableActionCheckAgent(repo)
        self.coder = ControllerAgent(repo, self)
        self.conversation_history = []

    def initial_setup(self):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### The `GeneralExplainerAgent` is initializing setup with provided instructions and context")

        prompt = f"""Your name is Zinley, expert code analyst.

        You need to reply to the user prompt and respond in the provided request language.

        Do not hallucinate what you don't know, your response must be based on truth, comprehensive and detailed, in the easiest way to help people understand.

        Only if asked about the AI model you are using, mention that you are using a model configured by the Zinley team. If they don't ask, don't say anything.

        YOU MUST NEVER LEAK ANY FOUNDATION MODEL INFORMATION UNDER ANY CIRCUMSTANCES!

        #### Response Guidelines:
        1. Formatting:
           - Return a nicely formatted response
           - Use clear headings (no larger than h4)
           - For bash commands, use markdown code blocks with 'bash' syntax highlighting

        2. Readability:
           - Space wisely
           - Ensure the text is clear and easy to read
           - Avoid crowding content together

        3. Clarity:
           - No weird symbols or unnecessary text
           - Avoid distractions or patterns

        4. AI Model Information:
           - If asked, state that you use a model configured by the Zinley team

        5. Bash Commands:
           - Format all bash commands using the following structure:
             ```bash
             command here
             ```

        6. Project Tree Structure:
           - When displaying a project tree structure, use this markdown format:
             ```plaintext
             project/
             ├── src/
             │   ├── main.py
             │   └── utils.py
             ├── tests/
             │   └── test_main.py
             └── README.md
             ```

        Respond directly to support the user's request. Do not provide irrelevant information or hallucinate. Only provide the project tree structure if explicitly asked or if it's directly relevant to the user's question.
        Only answer what the user is asking for. Do not engage in unnecessary talk or provide any additional information.
        """

        self.conversation_history = [
            {"role": "system", "content": prompt}
        ]

    async def get_prePrompt(self, user_prompt, file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt, file_attachments, focused_files)

    async def get_normal_answer(self, user_prompt, language, role, file_attachments, focused_files, assets_link, crawl_logs):
        """Generate idea plans based on user prompt and available files."""
        return await self.normalExplainer.get_normal_answer_plans(self.conversation_history, user_prompt, language, role, file_attachments, focused_files, assets_link, crawl_logs)

    async def get_file_answer(self, user_prompt, language, files, role, file_attachments, focused_files, assets_link, crawl_logs):
        """Generate idea plans based on user prompt and available files."""
        return await self.mainExplainer.get_answer_plans(self.conversation_history, user_prompt, language, files, role, file_attachments, focused_files, assets_link, crawl_logs)

    async def get_explaining_files(self, prompt, file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileFinder.get_file_plannings(prompt, file_attachments, focused_files)

    async def get_started(self, user_prompt, file_attachments, focused_files, snow_mode):
        logger.info(" #### The `Support Agent` was assigned to process your request.")
        logger.info("-------------------------------------------------")
        isFirst = True
        assets_link = []

        while True:
            if not isFirst:
                last_log = ""
                if len(self.conversation_history) >= 2:
                    last_assistant_log = self.conversation_history[-1]["content"]
                    last_log = f"{last_assistant_log}"

                try:
                    if last_log:
                        logger.info(" #### You're in `QA Mode`! Type your question to get support, click `take action` so Zinley can apply the suggested solution, or click `Exit` to leave.")
                        logger.info(" ### Click take action so Zinley can apply the above solution to the current project:  ")

                        user_permission = input()

                        user_prompt, tier, file_attachments, focused_files, snow_mode = parse_payload(self.repo.get_repo_path(), user_permission)
                        user_prompt = user_prompt.lower()
                        
                        if user_prompt == "exit":
                            break

                    else:
                        logger.info(" #### You're in `QA Mode`! Type your question to get support, or click `Exit` to leave.")
                        logger.info(" #### Are you satisfied with this development plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

                        user_permission = input()

                        user_prompt, _, file_attachments, focused_files, snow_mode = parse_payload(self.repo.get_repo_path(), user_permission)
                        user_prompt = user_prompt.lower()
                
                        if user_prompt == "exit":
                            break
                except:
                    logger.info(" #### You're in `QA Mode`! Type your question to get support, or click `Exit` to leave.")
                    logger.info(" #### Are you satisfied with this development plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

                    user_permission = input()

                    user_prompt, _, file_attachments, focused_files, snow_mode = parse_payload(self.repo.get_repo_path(), user_permission)
                    user_prompt = user_prompt.lower()
            
                    if user_prompt == "exit":
                        break

            else:
                isFirst = False

            if user_prompt == "h":
                await self.coder.explainer_code_task_pipeline(tier, last_log, "Top notch software engineer", "English", file_attachments, assets_link, snow_mode)
                self.conversation_history.append({"role": "user", "content": "Apply above solution."})
                self.conversation_history.append({"role": "assistant", "content": "Already done. No further action needed."})
                logger.info("-------------------------------------------------")
            else:
                crawl_plan = await self.crawlerPlaner.get_crawl_plans(user_prompt)
                crawl_logs = []
                if isinstance(crawl_plan, dict):
                    for step in crawl_plan.get('crawl_tasks', []):
                        crawl_url = step.get('crawl_url')
                        if crawl_url:
                            logger.info(f" #### The `Crawler Agent` is reading: [{crawl_url}]({crawl_url})")
                            result = self.crawler.process(crawl_url)
                            logger.info(f" #### The `Crawler Agent` has finished reading: [{crawl_url}]({crawl_url})")
                            crawl_logs.append({
                                'url': crawl_url,
                                'result': result
                            })

                image_result = await self.imageAgent.process_image_links(user_prompt)
                assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []
                prePrompt = await self.get_prePrompt(user_prompt, file_attachments, focused_files)
                pipeline = prePrompt.get('pipeline', '')
                language = prePrompt.get('original_prompt_language', '')
                role = prePrompt.get('role', '')

                if pipeline == "1" or pipeline == 1:
                    logger.debug("\n #### The `File Finder Agent` is currently embarking on a quest to locate relevant files.")
                    file_result = await self.get_explaining_files(user_prompt, file_attachments, focused_files)
                    working_files = file_result.get('working_files', []) if isinstance(file_result, dict) else []
                    all_files = set(working_files)
                    if file_attachments:
                        all_files.update(file_attachments)
                    if focused_files:
                        all_files.update(focused_files)
                    if all_files:
                        files_list = "\n".join([f"  - {file}" for file in all_files])
                        logger.info(f" #### The `Support Agent` is reading these files:\n{files_list}")
                    self.conversation_history = await self.get_file_answer(user_prompt, language, working_files, role, file_attachments, focused_files, assets_link, crawl_logs)
                elif pipeline == "2" or pipeline == 2:
                    logger.debug("\n #### The `General Explainer Agent` is presently engaged in processing your query and formulating a comprehensive response.")
                    self.conversation_history = await self.get_normal_answer(user_prompt, language, role, file_attachments, focused_files, assets_link, crawl_logs)

                logger.info("-------------------------------------------------")
