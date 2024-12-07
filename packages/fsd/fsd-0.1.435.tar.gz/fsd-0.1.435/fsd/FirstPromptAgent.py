import os
import sys
import json
from json_repair import repair_json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = get_logger(__name__)

class FirstPromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.ai = AIGateway()

    async def get_prePrompt_plans(self, user_prompt):
        """
        Get development plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        try:
            logger.info("#### Hi there! The `Receptionist Agent` is processing your request.")
            messages = self._create_messages(user_prompt)
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f" The `FirstPromptAgent` encountered an error during pre-prompt planning:\n{str(e)}")
            return {"reason": str(e)}

    def _create_messages(self, user_prompt):
        logger.debug("#### The `FirstPromptAgent` is constructing messages for the AI gateway")
        system_content = (
            "You are a senior developer and prompt engineering specialist. "
            "Analyze the user's prompt and respond in JSON format. Follow these guidelines strictly:\n\n"
            "pipeline: Choose the most appropriate pipeline based on the user's prompt. "
            "Respond with a number (1, 2, or 3) for the specific pipeline:\n"
            "1. Talkable: Use this for general conversation, non-code related requests, or when the user wants to discuss something. "
            "This includes explanations, Q&A, general interactions where AI can converse with people, "
            "requests to write sample code, show project structure, show this code or show that code, "
            "discuss coding topics without modifying a project, greetings like 'hello world', expressions of feelings, "
            "desire to talk about any topic (technical or non-technical), questions about history, or any other general conversational topic. "
            "Also use this for requests to find bugs, read files, compare files, or find issues in files without making changes to the project.\n"
            "2. Actionable: Use this ONLY for requests to create new code, files, or modify existing code in a real project. "
            "This includes requests to run, compile, build, fix, or write serious code for an actual project. "
            "Do NOT use this for non-code-related tasks or sample code requests. "
            "Pay special attention to keywords like 'write', 'build', 'create', 'implement' when followed by specific technical requirements - "
            "these usually indicate actionable requests (e.g. 'Write an ETL pipeline using Apache Flink' or 'Build a microservice architecture'). "
            "Such detailed technical implementation requests should be treated as actionable even without explicit project context.\n"
            "3. Ambiguous: Use this when the request could be interpreted as either talkable (1) or actionable (2) and requires human confirmation. "
            "For example, if a user says 'help me with this bug' - it's unclear if they want to discuss the bug (1) or want you to fix it (2). "
            "Choose this when you need clarification on whether the user wants to discuss/analyze something or wants actual changes made to the project.\n"
            "Return '2' if the user directly asks for any of the following:\n"
            "   - Directly Fix errors command for user\n"
            "   - Create/add files or folders\n"
            "   - Move files or folders\n"
            "   - Install dependencies\n"
            "   - Open/run/compile project\n"
            "   - Deploy project\n"
            "   - Generate images\n"
            "   - Any direct coding work for this project like adding new features or fixing issues\n"
            "   - Build something (this is always actionable)\n"
            "   - Write/implement/create specific technical solutions with detailed requirements\n"
            "If you're certain it's not '2', choose '1'. Choose '3' when you need clarification between discussion (1) and action (2).\n"
            "Example JSON response:\n"
            '{"pipeline": "1"}\n'
            "Return only a valid JSON response without additional text, symbols, or MARKDOWN."
        )
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"User original prompt:\n{user_prompt}. Return only a valid PLAIN JSON response STRICTLY without additional text, symbols, or MARKDOWN."}
        ]

    def _parse_response(self, response):
        logger.debug("#### The `FirstPromptAgent` is parsing the AI gateway response")
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.error(f" The `Receptionist Agent` encountered an error and is attempting to repai itself.")
            logger.debug(f"DAMAGE RESPOND: {response.choices[0].message.content}")
            repaired_json = repair_json(response.choices[0].message.content)
            return json.loads(repaired_json)
