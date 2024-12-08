import os
import sys
import json
import subprocess
import asyncio
import re

from .ImagePrePromptAgent import CompilePrePromptAgent
from .ImageTaskPlanner import ImageTaskPlanner
from .ImageFileFinderAgent import ImageFileFinderAgent
from .ImageAnalysAgent import ImageAnalysAgent
from .ImageGenAgent import ImageGenAgent
from .ImageCheckAgent import ImageCheckAgent
from .ImageCheckSpecialAgent import ImageCheckSpecialAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
logger = get_logger(__name__)

class ImageControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.preprompt = CompilePrePromptAgent(repo)
        self.fileFinder = ImageFileFinderAgent(repo)
        self.analysAgent = ImageAnalysAgent(repo)
        self.taskPlanner = ImageTaskPlanner(repo)
        self.imageGenAgent = ImageGenAgent(repo)
        self.imageCheckAgent = ImageCheckAgent(repo)
        self.imageCheckSpecialAgent = ImageCheckSpecialAgent(repo)
        self.imageAgent = PromptImageUrlAgent(repo)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def start_image_process(self, tier, instruction, original_prompt_language, snow_mode, auto_mode):
        if not auto_mode:
            logger.info(" #### Image generation needed. Click `Approve` to proceed or `Skip` to cancel.")
            logger.info(f" \n ### Press a or Approve to execute this step, or Enter to skip: ")
            user_permission = input()
            user_prompt, tier, _, _, snow_mode  = parse_payload(self.repo.get_repo_path(), user_permission)
            user_prompt = user_prompt.lower()
            
            if user_prompt != "a":
                logger.info(" #### The `Image Generation Agent` has skipped as per user request.")
                return

        logger.info(f" #### `Image Task Planner` is organizing and preparing the task. ")
        task = await self.taskPlanner.get_task_plan(instruction)
        await self.imageGenAgent.generate_images(task, tier, snow_mode)
        commits = task.get('commits', "")
        self.repo.add_all_files(f"Zinley - {commits}")
        logger.info(f" #### Image generation process completed.")


    async def get_started(self, tier, instruction, original_prompt_language, file_attachments, focused_files, snow_mode, auto_mode):
        """Start the processing of the user prompt."""
        
        logger.info(" #### `Image Analysis Agent` is finding relevant style content.")
        
        file_result = await self.fileFinder.get_style_file_plannings()

        style_files = file_result.get('style_files', [])

        all_files = set(style_files)
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)

        if all_files:
            files_list = "\n".join([f"- {file}" for file in all_files])
            logger.info(f" #### The `Image Agent` is reading these files:\n{files_list}")

        self.analysAgent.initial_setup(style_files)

        logger.info(" #### `Image Analysis Agent` is preparing an initial image plan for clarification.")

        image_result = await self.imageAgent.process_image_links(instruction)
        assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []

        idea_plan = await self.analysAgent.get_idea_plans(instruction, original_prompt_language, file_attachments, focused_files, assets_link)

        if not auto_mode:
            while True:
                logger.info(" #### The `Image Analysis Agent` is requesting feedback. Click `Approve` if you feel satisfied, click `Skip` to end this process, or type your feedback below.")

                logger.info(" ### Press a or Approve to execute this step, or Enter to skip: ")

                user_prompt_json = input()
                user_prompt,tier,file_attachments, focused_files, snow_mode = parse_payload(self.repo.get_repo_path(), user_prompt_json)
                user_prompt = user_prompt.lower()

                if user_prompt == 's':
                    logger.info(" #### The `Image Generation Agent` has skipped as per user request.")
                    return

                if user_prompt == "a":
                    break
                else:
                    logger.info(f" #### `Image Analysis Agent` is updating the image plan based on user feedback.")
                    instruction = instruction + "." + user_prompt
                    self.analysAgent.remove_latest_conversation()
                    image_result = await self.imageAgent.process_image_links(instruction)
                    assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []
                    idea_plan = await self.analysAgent.get_idea_plans(instruction, original_prompt_language, file_attachments, focused_files, assets_link)

        self.analysAgent.clear_conversation_history()

        logger.info(f" #### `Image Task Planner` is organizing and preparing the task. ")
        task = await self.taskPlanner.get_task_plan(idea_plan)
        await self.imageGenAgent.generate_images(task, tier, snow_mode)
        commits = task.get('commits', "")
        self.repo.add_all_files(f"Zinley - {commits}")
        logger.info(f" #### Image generation process completed.")


    async def get_started_image_generation(self, tier, user_prompt, original_prompt_language, snow_mode, auto_mode):
        """Start the processing of the user prompt."""
        
        logger.debug(" #### Image generation agent initialized and ready to process image requests")

        if "#### DONE: *** - D*** I**" in user_prompt or "#### DONE: *** - I**" in user_prompt:
            finalPrompt = await self.imageCheckSpecialAgent.get_image_check_plans(user_prompt, original_prompt_language)
            await self.start_image_process(tier, finalPrompt, original_prompt_language, snow_mode, auto_mode)
        else:
            logger.info(" #### `Image generation agent` has determined that no additional images need to be generated")

        logger.debug(f" #### Image generation process completed!")
