from typing import Dict, Any
import json
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ..base import AIProvider
from app.core.settings import get_settings

class LangchainLLMProvider(AIProvider):
    def __init__(self):
        self.settings = get_settings()
        self.llm = None

    async def initialize(self) -> None:
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            temperature=0.2,
            openai_api_key=self.settings.OPENAI_API_KEY
        )

    async def generate_response(self, prompt: str, **kwargs) -> Any:
        if not self.llm:
            await self.initialize()

        system_prompt = """You are a technical mentor creating learning paths. 
List key technologies and concepts in this format:

1. HTML & CSS
   - Core technologies for web structure and styling
   - Resource: [MDN Web Docs] https://developer.mozilla.org/en-US/docs/Web
   - Subtopics:
     a) Flexbox
        - Modern layout system for responsive design
        - Resource: [Flexbox Guide] https://css-tricks.com/snippets/css/a-guide-to-flexbox/

2. JavaScript
   - Programming language for web interactivity
   - Resource: [JavaScript.info] https://javascript.info
   - Subtopics:
     a) ES6 Features
        - Modern JavaScript capabilities
        - Resource: [ES6 Tutorial] https://www.javascripttutorial.net/es6/

Use simple titles, one-line descriptions, and real learning resources.
Focus on fundamental concepts and popular tools."""

        user_prompt = f"Create a learning path for {prompt} with 2-3 main topics and 1-2 subtopics each. Use simple titles and brief descriptions."

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        try:
            response = self.llm.invoke(prompt_template.format())
            return response.content
        except Exception as e:
            print(f"Error getting AI response: {str(e)}")
            raise ValueError(f"Failed to generate response: {str(e)}") 