import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class PromptImageUrlAgent:
    def __init__(self, repo):
        """
        Initialize the PromptImageUrlAgent with the repository.

        Args:
            repo: The repository object.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_image_links(self, idea):
        """
        Extract image links from the given idea.

        Args:
            idea (str): The user's idea or request.

        Returns:
            dict: JSON response with the extracted image links.
        """
        logger.debug("\n #### PromptImageUrlAgent is checking for image links")
        prompt = (
            "Analyze the provided development plan and extract only valid image links that end with .png, .jpg, .jpeg, .svg, or .webp. "
            "Do not include any links that do not have these exact file extensions. "
            "Only include valid image links. Do not invent or hallucinate links. "
            "If the user provides an incomplete URL (e.g., missing 'https://', 'www', etc.), correct it to a fully valid URL. "
            "Provide the response as a JSON object with the following format:"
            "{\n"
            "    \"assets_link\": [\"https://example.com/image1.png\", \"https://www.example.com/image2.jpg\"]\n"
            "}\n\n"
            "If no valid image links (ending with .png, .jpg, .jpeg, .svg, or .webp) are found, return an empty list:"
            "{\n"
            "    \"assets_link\": []\n"
            "}\n\n"
            "Return only valid JSON without any additional text or Markdown formatting. "
            "Strictly enforce the file extension rule: only .png, .jpg, .jpeg, .svg, or .webp are allowed."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the user's request. STRICTLY EXTRACT ONLY EXISTING IMAGE URLS FROM THE FOLLOWING TEXT. DO NOT GENERATE, INVENT, OR HALLUCINATE ANY URLS. ONLY INCLUDE URLS THAT ARE EXPLICITLY PRESENT IN THE TEXT:\n{idea}\n"
            }
        ]

        try:
            logger.debug("\n #### PromptImageUrlAgent is sending request to AI for image link extraction")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            logger.debug("\n #### PromptImageUrlAgent has received response from AI")
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.debug("\n #### PromptImageUrlAgent encountered JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  PromptImageUrlAgent encountered an error: `{e}`")
            return {
                "reason": str(e)
            }

    async def process_image_links(self, idea):
        logger.debug("\n #### PromptImageUrlAgent is starting image link extraction process")
        result = await self.get_image_links(idea)
        
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.PNG', '.JPG', '.JPEG', '.ico')
        validated_links = [link for link in result.get('assets_link', []) if link.lower().endswith(valid_extensions) or any(ext in link for ext in valid_extensions)]
        logger.debug(validated_links)
        return {"assets_link": validated_links}
