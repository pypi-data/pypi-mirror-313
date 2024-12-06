import os
import sys
import json
import asyncio
import aiofiles
from .CodingAgent import CodingAgent
from .FileManagerAgent import FileManagerAgent
from .FileFinderAgent import FileFinderAgent
from .IdeaDevelopment import IdeaDevelopment
from .ShortIdeaDevelopment import ShortIdeaDevelopment
from .PrePromptAgent import PrePromptAgent
from .TaskPlanner import TaskPlanner
from .TaskPlannerPro import TaskPlannerPro
from .PlanCheckAgent import PlanCheckAgent
from .ContextPrepareAgent import ContextPrepareAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.ImageAgent.ImageControllerAgent import ImageControllerAgent
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.MainOperation.ProjectsRunner import ProjectsRunner
from fsd.system.FileContentManager import FileContentManager
from fsd.Crawler.CrawlerAgent import CrawlerAgent
from fsd.Crawler.CrawlerTaskPlanner import CrawlerTaskPlanner
from fsd.dependency.DependencyControllerAgent import DependencyControllerAgent
from fsd.Deployment.DeploymentControllerAgent import DeploymentControllerAgent 
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
from fsd.compile.CompileControllerAgent import CompileControllerAgent
logger = get_logger(__name__)

class ControllerAgent:
    def __init__(self, repo, explainer_controller):
        self.repo = repo
        directory_path = self.repo.get_repo_path()
        self.directory_path = directory_path
        self.explainer_controller = explainer_controller
        self.idea = IdeaDevelopment(repo)
        self.short_idea = ShortIdeaDevelopment(repo)
        self.planCheckAgent = PlanCheckAgent(repo)
        self.preprompt = PrePromptAgent(repo)
        self.taskPlanner = TaskPlanner(repo)
        self.taskPlannerPro = TaskPlannerPro(repo)
        self.coder = CodingAgent(repo)
        self.project = ProjectManager(repo)
        self.image = ImageControllerAgent(repo)
        self.compile = CompileControllerAgent(repo)
        self.runner = ProjectsRunner(repo)
        self.fileManager = FileManagerAgent(repo)
        self.fileFinder = FileFinderAgent(repo)
        self.deploy = DeploymentControllerAgent(repo)
        self.code_manager = FileContentManager(repo)  # Initialize CodeManager in the constructor
        self.crawler = CrawlerAgent()
        self.crawlerPlaner = CrawlerTaskPlanner(repo)
        self.dependency = DependencyControllerAgent(repo)
        self.context = ContextPrepareAgent(repo)
        self.imageAgent = PromptImageUrlAgent(repo)
        self.explainer_controller.initial_setup()


    async def get_pro_coding_requests(
        self, instructions, context, file_lists, context_files,
        role, crawl_logs, original_prompt_language,file_attachments, assets_link
    ):
        """Generate coding requests based on instructions and context."""
        logger.info("#### The `Uni` agent is preparing the task.")
        plan = await self.get_taskPlanner_pro(instructions['Implementation_plan'], file_lists, original_prompt_language)
        commits = plan.get('commits', "")
        logger.info("-------------------------------------------------")
        logger.info("#### The `Coding Agent Pro` is starting the coding phase in Snow mode.")
        conversation_history = []
        logger.debug(file_lists)

        async def process_task(task, coding_agent):
            full_file = task.get('file_name')
            if self.is_coding_file(full_file):
                main_path = full_file
                if main_path:
                    techStack = task.get('techStack')

                    logger.info(
                        f"#### The `{techStack.upper()} Agent` is processing file: `{os.path.relpath(full_file, self.directory_path)}`."
                    )

                    try:

                        file_name = os.path.basename(full_file)
                        is_svg = file_name.lower().endswith('.svg')

                        result = await coding_agent.get_coding_request(full_file, techStack)

                        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

                        user_prompt = f"As a world-class, highly experienced {'SVG designer' if is_svg else f'{techStack} developer'}, implement the following task with utmost efficiency and precision:\n"
                        user_prompt += f"For: {file_name}:\n"
                        
                        if is_svg:
                            user_prompt += (
                                "Create a visually appealing design with elegant UI. "
                                "Balance aesthetics and functionality, ensuring each element enhances the user experience. "
                                "Prioritize smooth performance and sophistication in all visual aspects.\n"
                            )
                        else:
                            user_prompt += (
                                "For UI-related tasks:\n"
                                "- Ensure perfect alignment and consistent padding for a clean, modern look.\n"
                                "- Implement a visually striking design with NICE UI and interactions.\n"
                                "- Apply responsive design principles and prioritize whitespace usage.\n"
                                "- Enhance user experience while maintaining optimal performance.\n"
                            )
                            user_prompt += "Always refer back to the High level development instruction to ensure alignment and completeness.\n"

                        user_prompt += f"{lazy_prompt}\n" if not is_svg else ""
                        user_prompt += "NOTICE: Your response should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

                        if conversation_history and conversation_history[-1]["role"] == "user":
                            conversation_history.append({"role": "assistant", "content": "Understood."})

                        conversation_history.append({"role": "user", "content": user_prompt})
                        conversation_history.append({"role": "assistant", "content": result})

                        #await self.log_result(main_path, result)
                        await self.code_manager.handle_coding_agent_response(main_path, result)

                        logger.info(
                            f"\n #### `{techStack.upper()} Agent` finished successfully: `{os.path.relpath(full_file, self.directory_path)}`."
                        )
                    except Exception as e:
                        logger.error(f"  Error processing file `{full_file}`: {str(e)}")
                else:
                    logger.debug(f" #### File not found: `{full_file}`")

        for group in plan.get('groups', []):
            group_name = group.get('group_name')
            tasks = group.get('tasks', [])
            logger.info(f"#### Processing group: {group_name}")

            # Create a pool of CodingAgents for this group
            coding_agents = [CodingAgent(self.repo) for _ in range(len(tasks))]

            # Initialize all agents in the pool
            for agent in coding_agents:
                agent.initial_setup(context_files, instructions, context, crawl_logs, file_attachments, assets_link)
                agent.conversation_history.extend(conversation_history)

            # Process all tasks in the group concurrently
            results = await asyncio.gather(
                *[process_task(task, agent) for task, agent in zip(tasks, coding_agents)],
                return_exceptions=True
            )

            # Handle exceptions if any
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"An error occurred: {result}")

            # Clean up the agents after the group is processed
            for agent in coding_agents:
                agent.clear_conversation_history()
                agent.destroy()

            logger.info(f"#### Completed group: {group_name}")
            logger.info("-------------------------------------------------")

        return commits
    

    async def log_result(self, main_path: str, result: str):
        """
        Asynchronously log the result to a file, appending new entries and separating them.

        :param log_path: The name of the log file (e.g., 'log1.txt')
        :param main_path: The main path of the current operation
        :param result: The result to be logged
        """
        full_log_path = os.path.join(self.repo.get_repo_path(), "log1.txt")
        
        try:
            async with aiofiles.open(full_log_path, 'a') as log_file:
                await log_file.write(f"\n\n-----------------\n")
                await log_file.write(f"Main Path: {main_path}\n")
                await log_file.write(f"Result:\n{result}\n")
            
            logger.info(f" #### Successfully appended log to {full_log_path}")
        except Exception as e:
            logger.error(f"  Error writing to log file {full_log_path}: {str(e)}")



    def filter_non_asset_files(self, file_set):
        # Define a set of non-code file extensions (assets and binary files)
        non_code_extensions = {
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico',
            # Audio
            '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a',
            # Video
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
            # Archives
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
            # Fonts
            '.ttf', '.otf', '.woff', '.woff2', '.eot',
            # Documents
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            # Other binary formats
            '.exe', '.dll', '.so', '.dylib', '.bin', '.dat',
            # Database files
            '.db', '.sqlite', '.mdb',
        }

        # Use a set comprehension to filter out non-code files
        code_files = {file for file in file_set if not any(file.lower().endswith(ext) for ext in non_code_extensions)}

        return code_files

    def is_coding_file(self, filename):
        # Define a set of non-code file extensions (assets and binary files)
        non_code_extensions = {
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico',
            # Audio
            '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a',
            # Video
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
            # Archives
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
            # Fonts
            '.ttf', '.otf', '.woff', '.woff2', '.eot',
            # Documents
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            # Other binary formats
            '.exe', '.dll', '.so', '.dylib', '.bin', '.dat',
            # Database files
            '.db', '.sqlite', '.mdb',
        }

        # Get the file extension
        _, extension = os.path.splitext(filename.lower())

        # If the file has no extension or its extension is not in the non-code list, consider it a code file
        return extension not in non_code_extensions

    async def get_prompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.prompt.get_prompt_plans(user_prompt)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)

    async def get_taskPlanner(self, instruction, file_lists, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.taskPlanner.get_task_plans(instruction, file_lists, original_prompt_language)
    
    async def get_taskPlanner_pro(self, instruction, file_lists, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.taskPlannerPro.get_task_plans(instruction, file_lists, original_prompt_language)

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.idea.get_idea_plans(user_prompt, original_prompt_language)

    async def get_lightIdea_plans(self, user_prompt, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.short_idea.get_idea_plans(user_prompt, original_prompt_language)

    async def get_bugs_plans(self, files, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.bug_scanner.get_idea_plans(files, user_prompt)

    async def get_long_idea_plans(self, files, user_prompt, is_first):
        """Generate idea plans based on user prompt and available files."""
        return await self.long.get_idea_plans(files, user_prompt, is_first)

    async def get_file_planning(self, idea_plan):
        """Generate file planning based on idea plan and directory tree."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def get_adding_file_planning(self, idea_plan, tree, file_attachments):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_adding_file_plannings(idea_plan, tree, file_attachments)

    async def get_moving_file_planning(self, idea_plan, tree, file_attachments):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_moving_file_plannings(idea_plan, tree, file_attachments)

    async def get_formatting_files(self, prompt):
        """Generate formatting plans based on user prompt and directory tree."""
        return await self.fileFinder.get_file_plannings(prompt)

    async def run_requests(self, request_list, role, original_prompt_language, file_attachments, focused_files):
        """Run project requests."""
        return await self.runner.run_project(request_list, role, original_prompt_language, file_attachments, focused_files)


    async def process_creation(self, data):
        """Process the creation and moving of files based on provided data."""
        # Process creation of new files
        if data.get('Is_creating'):
            new_files = data.get('Adding_new_files', [])
            if new_files:
                await self.project.execute_files_creation(new_files)
            else:
                logger.debug(" #### `FileCreationManager`: No new files need to be created.")
        else:
            logger.debug(" #### `FileCreationManager`: Creation flag is not set.")

        # Process moving of files
        moving_processes = data.get('Moving_files', [])
        if moving_processes:
            logger.debug(" #### `FileCreationManager`: about to moving files")
            logger.debug(moving_processes)
            await self.project.execute_files_creation(moving_processes)
        else:
            logger.debug(" #### `FileCreationManager`: No files need to be moved this time.")

        # If no files to create or move
        if not data.get('Is_creating') and not moving_processes:
            logger.debug(" #### `FileCreationManager`: No new files need to be added or moved at this time.")

    async def process_moving(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_moving'):
            processes = data.get('Moving_files', [])
            await self.project.execute_files_creation(processes)

    async def build_existing_context(self, existing_files):
        """Build and return the context of existing files."""
        all_context = ""
        for path in existing_files:
            file_context = read_file_content(path)
            if file_context:
                all_context += f"\n\nFile: {path}:\n{file_context}"
            else:
                all_context += f"\n\nFile: {path}: This file exists but is empty"

        return all_context

    async def get_coding_requests(self, instructions, context, file_lists, context_files, role, crawl_logs, original_prompt_language, file_attachments, assets_link):
        """Generate coding requests based on instructions and context."""
        self.coder.initial_setup(context_files, instructions, context, crawl_logs, file_attachments, assets_link)

        logger.info("#### The `Uchi` agent is preparing the task.")
        plan = await self.get_taskPlanner(instructions['Implementation_plan'], file_lists, original_prompt_language)
        commits = plan.get('commits', "")
        logger.info("-------------------------------------------------")
        logger.info("#### The `Coding Agent` is starting the coding phase.")
        for step in plan.get('steps', []):
            file_name = step.get('file_name')
            if self.is_coding_file(file_name):
                main_path = file_name
                if main_path:
                    techStack = step.get('techStack')

                    logger.info("-------------------------------------------------")
                    logger.info(f"#### The `{techStack.upper()} Agent` is processing file: `{os.path.relpath(file_name, self.directory_path)}`.")

                    try:
                        result = await self.coder.get_coding_requests(file_name, techStack)

                        await self.code_manager.handle_coding_agent_response(main_path, result)

                        logger.info(f" #### The `{techStack.upper()} Agent` finished successfully: `{os.path.relpath(file_name, self.directory_path)}`.")
                    except Exception as e:
                        logger.error(f"  Error processing file `{file_name}`: {str(e)}")
                else:
                    logger.debug(f" #### File not found: `{file_name}`")

        return commits


    async def build_and_fix_compile_error(self, file_list, role, original_prompt_language, file_attachments, focused_files):
        """Build project and fix compile errors."""
        await self.run_requests(file_list, role, original_prompt_language, file_attachments, focused_files)


    async def fix_compile_error_pipeline(self,file_list, role, original_prompt_language, file_attachments, focused_files):
        """Pipeline for fixing compile errors."""
        logger.info("-------------------------------------------------")
        await self.build_and_fix_compile_error(file_list, role, original_prompt_language, file_attachments, focused_files)
        logger.info("-------------------------------------------------")


    async def add_files_folders_pipeline(self, finalPrompt, role, file_attachments):
        """Pipeline for adding files and folders."""
        logger.info("-------------------------------------------------")
        logger.debug(" #### Initiating add_files_folders_pipeline")
        logger.info(" #### The `File Manager Agent` is processing files.")
        file_result = await self.get_adding_file_planning(finalPrompt, self.repo.print_tree(), file_attachments)
        await self.process_creation(file_result)
        commits = file_result.get('commits', "")
        if commits:
            self.repo.add_all_files(f"Zinley - {commits}")

        logger.info("-------------------------------------------------")

    async def move_files_folders_pipeline(self, finalPrompt, role, file_attachments):
        """Pipeline for adding files and folders."""
        logger.info("-------------------------------------------------")
        logger.debug("\n #### Initiating move_files_folders_pipeline")
        logger.info(" #### The `File Manager Agent` is processing files.")
        file_result = await self.get_moving_file_planning(finalPrompt, self.repo.print_tree(), file_attachments)
        await self.process_moving(file_result)
        commits = file_result.get('commits', "")
        if commits:
            self.repo.add_all_files(f"Zinley - {commits}")
        logger.info("-------------------------------------------------")

    async def explainer_code_task_pipeline(self, tier, solution, role, original_prompt_language, file_attachments, assets_link, snow_mode):
        """Pipeline for regular coding tasks."""

        try:
            logger.info("-------------------------------------------------")
            logger.debug("#### Initiating regular_code_task_pipeline")
            crawl_plan = await self.crawlerPlaner.get_crawl_plans(solution)
            crawl_logs = []
            if crawl_plan:
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

            logger.debug(" #### The `Dependency Agent` is performing dependency checks.")
            await self.dependency.get_started_coding_pipeline(solution, original_prompt_language, [], [])
            logger.debug(" #### The `Dependency Agent` has finished with dependency checks.")
            logger.debug("-------------------------------------------------")

            logger.info(" #### The `File Manager Agent` is processing files.")
            file_result = await self.get_file_planning(solution)
            await self.process_creation(file_result)
            add = file_result.get('Adding_new_files', [])
            move = file_result.get('Moving_files', [])
            if add or move:
                commits = file_result.get('commits', "")
                if commits:
                    self.repo.add_all_files(f"Zinley - {commits}")
            logger.debug("\n #### The `File Manager Agent` has completed processing files.")
            logger.debug("-------------------------------------------------")
            
            logger.debug(file_result)
            existing_files = file_result.get('Existing_files', [])
            new_adding_files = [item['Parameters']['full_path'] for item in file_result.get('Adding_new_files', [])]
            new_moving_files = [item['Parameters']['new_full_path'] for item in file_result.get('Moving_files', [])]
            context_files = []

            # Create a dictionary of basename to full path for new_moving_files
            new_moving_dict = {os.path.basename(path): path for path in new_moving_files}

            # Prioritize new_moving_files over existing_files with the same basename
            final_working_files = set()
            for file in existing_files:
                basename = os.path.basename(file)
                if basename in new_moving_dict:
                    final_working_files.add(new_moving_dict[basename])
                else:
                    final_working_files.add(file)

            # Add new_adding_files
            final_working_files.update(new_adding_files)

            final_working_files = self.filter_non_asset_files(final_working_files)
            all_context = await self.build_existing_context(list(final_working_files))

            final_request = {"original_prompt": "", "Implementation_plan": solution}

            commits = await self.get_pro_coding_requests(
                    final_request, all_context, list(final_working_files), context_files, role, crawl_logs, original_prompt_language, file_attachments, assets_link
                )

            self.repo.add_all_files(f"Zinley - {commits}")

            self.idea.clear_conversation_history()
            self.short_idea.clear_conversation_history()
            self.coder.clear_conversation_history()

            await self.image.get_started_image_generation(tier, solution, original_prompt_language, snow_mode)
        except:
            logger.debug(" #### The `Coding Agent` has encountered some bugs. We apologize for the inconvenience. Please try again!")

    async def regular_code_task_pipeline(self, tier, finalPrompt, role, original_prompt_language, file_attachments, focused_files, snow_mode, auto_mode):
        try:
            """Pipeline for regular coding tasks."""
            logger.info("-------------------------------------------------")
            logger.debug("#### Initiating regular_code_task_pipeline")  

            await self.codingProgress(tier, finalPrompt, role, original_prompt_language, file_attachments, focused_files, snow_mode, auto_mode)

            logger.info(" #### The `Coding Agent` has completed the coding phase.")
            logger.info("-------------------------------------------------")
        except Exception as e:
            logger.debug(f" #### The `Coding Agent` has encountered an error. We apologize for the inconvenience. Please try again!")

    async def codingProgress(self, tier, finalPrompt, role, original_prompt_language, file_attachments, focused_files, snow_mode, auto_mode):
        crawl_logs = []
        idea_plan = ""
        isLight = True
        crawled_urls = set()  # Store already crawled URLs
        while True:
            self.idea.clear_conversation_history()
            self.short_idea.clear_conversation_history()
            if idea_plan and not auto_mode:
                logger_message = " #### The `Planner Agent" + (" Pro" if not isLight else "") + "` is requesting feedback. Click `Approve` if you feel satisfied, click `Skip` to end this process, or type your feedback below."
                logger.info(logger_message)
                logger.info(" ### Press a or Approve to execute this step, or Enter to skip: ")

                user_prompt_json = input()
                user_prompt, tier, file_attachments, focused_files, snow_mode = parse_payload(self.repo.get_repo_path(), user_prompt_json)
                user_prompt = user_prompt.lower()

                if user_prompt == 's':
                    logger.info(f" #### The `Planner Agent{' Pro' if not isLight else ''}` has detected that the coding process has been skipped.")
                    logger.info("-------------------------------------------------")
                    return set()

                if user_prompt == "a":
                    break
                else:
                    finalPrompt += "." + user_prompt
            elif idea_plan and auto_mode:
                break

            logger.info(" #### The `Context Agent` is gathering context and preparing relevant data...")
            crawl_plan = await self.crawlerPlaner.get_crawl_plans(finalPrompt)
            if crawl_plan:
                for step in crawl_plan.get('crawl_tasks', []):
                    crawl_url = step.get('crawl_url')
                    if crawl_url and crawl_url not in crawled_urls:
                        logger.info(f" #### The `Crawler Agent` is reading: `{crawl_url}`")
                        result = self.crawler.process(crawl_url)
                        logger.info(f" #### The `Crawler Agent` has finished reading: `{crawl_url}`")
                        crawl_logs.append({
                            'url': crawl_url,
                            'result': result
                        })
                        crawled_urls.add(crawl_url)
                    elif crawl_url in crawled_urls:
                        logger.info(f" #### The `Crawler Agent` is reusing previously crawled data for: `{crawl_url}`")

            image_result = await self.imageAgent.process_image_links(finalPrompt)
            assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []
            
            result_check = await self.planCheckAgent.get_idea_check_plans(finalPrompt)
            isLight = result_check.get('result') != '1'

            logger.info("#### `Zinley` is thinking...")
            context = await self.context.get_file_planning(finalPrompt, file_attachments, focused_files, assets_link)
            all_files = set(context.get('working_files', []))
            if file_attachments:
                all_files.update(file_attachments)
            if focused_files:
                all_files.update(focused_files)
            if all_files:
                files_list = "\n".join([f"  - {file}" for file in all_files])
                logger.info(f" #### The `Coding Agent` is reading these files:\n{files_list}")
            logger.info("#### Thinking completed.")

            (self.short_idea if isLight else self.idea).initial_setup(role, crawl_logs, context, file_attachments, assets_link)

            if idea_plan:
                logger.info(f" #### The `Planner Agent{' Pro' if not isLight else ''}` is updating development plan.")
            else:
                logger.info(f" #### The `Planner Agent{' Pro' if not isLight else ''}` is creating an initial development plan.")

            idea_getter = self.get_lightIdea_plans if isLight else self.get_idea_plans
            idea_plan = await idea_getter(finalPrompt + (f" crawled data: {crawl_logs}" if crawl_logs else ""), original_prompt_language)

        if "MUST INSTALL DEPEDENCY" in str(idea_plan):
            logger.info(" #### The `Dependency Agent` is performing dependency checks.")
            await self.dependency.get_started_coding_pipeline(idea_plan, original_prompt_language, file_attachments, focused_files)
            logger.debug(" #### The `Dependency Agent` has finished with dependency checks.")
            logger.debug("-------------------------------------------------")

        logger.info(" #### The `File Manager Agent` is processing files.")
        file_result = await self.get_file_planning(idea_plan)
        await self.process_creation(file_result)
        add = file_result.get('Adding_new_files', [])
        move = file_result.get('Moving_files', [])
        if add or move:
            commits = file_result.get('commits', "")
            if commits:
                self.repo.add_all_files(f"Zinley - {commits}")
        logger.debug("\n #### The `File Manager Agent` has completed processing files.")

        logger.debug("-------------------------------------------------")
        
        existing_files = file_result.get('Existing_files', [])
        new_adding_files = [item['Parameters']['full_path'] for item in file_result.get('Adding_new_files', [])]
        new_moving_files = [item['Parameters']['new_full_path'] for item in file_result.get('Moving_files', [])]
        totalcontext = context.get('working_files', [])
        context_files = [file for file in totalcontext if file not in existing_files]

        new_moving_dict = {os.path.basename(path): path for path in new_moving_files}

        final_working_files = set()
        for file in existing_files:
            basename = os.path.basename(file)
            if basename in new_moving_dict:
                final_working_files.add(new_moving_dict[basename])
            else:
                final_working_files.add(file)

        final_working_files.update(new_adding_files)

        final_working_files = self.filter_non_asset_files(final_working_files)
        all_context = await self.build_existing_context(list(final_working_files))

        final_request = {"original_prompt": finalPrompt, "Implementation_plan": idea_plan}

        commits = await self.get_pro_coding_requests(
                final_request, all_context, list(final_working_files), context_files, role, crawl_logs, original_prompt_language, file_attachments, assets_link
            )

        self.repo.add_all_files(f"Zinley - {commits}")

        self.idea.clear_conversation_history()
        self.short_idea.clear_conversation_history()
        self.coder.clear_conversation_history()
            
        await self.image.get_started_image_generation(tier, idea_plan, original_prompt_language, snow_mode, auto_mode)

        return final_working_files


    async def get_started(self, user_prompt, tier, file_attachments, focused_files, snow_mode, auto_mode):
        """Process the user prompt."""
        logger.info("-------------------------------------------------")
        logger.info(" #### The `Captain Agent` will now begin processing your request.")

        prePrompt = await self.get_prePrompt(user_prompt)
        role = prePrompt['role']
        pipeline = prePrompt['pipeline']
        original_prompt_language = prePrompt['original_prompt_language']

        if pipeline in ["2", 2]:
            await self.add_files_folders_pipeline(user_prompt, role, file_attachments)
        elif pipeline in ["3", 3]:
            await self.move_files_folders_pipeline(user_prompt, role, file_attachments)
        elif pipeline in ["4", 4]:
            await self.regular_code_task_pipeline(tier, user_prompt, role, original_prompt_language, file_attachments, focused_files, snow_mode, auto_mode)
        elif pipeline in ["7", 7]:
            await self.deploy.get_started_deploy_pipeline()
        elif pipeline in ["5", 5]:
            await self.dependency.get_started(user_prompt, original_prompt_language, file_attachments, focused_files)
        elif pipeline in ["6", 6]:
            await self.compile.get_started(user_prompt, original_prompt_language, file_attachments, focused_files)
        elif pipeline in ["8", 8]:
            await self.image.get_started(tier, user_prompt, original_prompt_language, file_attachments, focused_files, snow_mode, auto_mode)
        elif pipeline in ["9", 9]:
            await self.explainer_controller.get_started(user_prompt, file_attachments, focused_files, snow_mode)
        else:
            logger.error(user_prompt)

        logger.info("#### `Captain Agent` has verified that all requested tasks have been completed.")
        logger.info("-------------------------------------------------")
