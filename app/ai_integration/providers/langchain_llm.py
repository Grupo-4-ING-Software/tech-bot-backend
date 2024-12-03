from typing import Dict, Any
import json
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ..base import AIProvider
from core.settings import get_settings

class LangchainLLMProvider(AIProvider):
    def __init__(self):
        self.settings = get_settings()
        self.llm = None
        # Keywords in both English and Spanish
        self.tech_keywords = [
            # English keywords
            "developer", "programmer", "coder", "engineer", "architect",
            "software", "web", "app", "mobile", "cloud", "data", "ai", "ml",
            "devops", "security", "cyber", "blockchain", "game",
            "frontend", "backend", "full-stack", "fullstack", "full stack",
            "qa", "tester", "analyst", "administrator", "designer",
            "python", "javascript", "java", "react", "angular", "vue",
            "node", "aws", "azure", "google cloud", "docker", "kubernetes",
            "computer science", "programming", "coding", "development",
            "software engineering", "web development", "data science",
            # Spanish keywords
            "desarrollador", "programador", "ingeniero", "arquitecto",
            "desarrollo", "aplicaciones", "móvil", "nube", "datos", "seguridad",
            "pruebas", "analista", "administrador", "diseñador",
            "ciencias de la computación", "programación", "desarrollo web",
            "ciencia de datos", "inteligencia artificial", "aprendizaje automático",
            "ciberseguridad", "computación", "sistemas", "redes"
        ]

    def _is_tech_career(self, prompt: str) -> bool:
        """Check if the input is related to a tech career"""
        # Convert prompt to lowercase for case-insensitive matching
        prompt_lower = prompt.lower()
        
        # Check for exact matches first
        if any(keyword == prompt_lower for keyword in self.tech_keywords):
            return True
            
        # Check for partial matches
        if any(keyword in prompt_lower for keyword in self.tech_keywords):
            return True
            
        # Check for compound terms
        words = prompt_lower.split()
        if len(words) > 1:
            if any(word in self.tech_keywords for word in words):
                return True
                
        return False

    def _detect_language(self, text: str) -> str:
        """Detect if the input is in Spanish or English"""
        spanish_indicators = [
            "desarrollador", "programador", "ingeniero", "desarrollo",
            "aplicaciones", "móvil", "datos", "seguridad", "computación"
        ]
        
        text_lower = text.lower()
        for indicator in spanish_indicators:
            if indicator in text_lower:
                return "es"
        return "en"

    def _get_error_message(self, prompt: str) -> Dict:
        language = self._detect_language(prompt)
        
        if language == "es":
            return {
                "data": {
                    "id": "error",
                    "title": "Carrera No Válida",
                    "description": (
                        "🤖 ¡Hola! Soy TechBot, tu asesor en carreras tecnológicas.\n\n"
                        "Me especializo en crear rutas de aprendizaje para carreras como:\n"
                        "• Desarrollo de Software (Frontend, Backend, Full Stack)\n"
                        "• Ciencia de Datos e Ingeniería de IA/ML\n"
                        "• Ingeniería DevOps y Cloud\n"
                        "• Ciberseguridad y Redes\n"
                        "• QA y Testing de Software\n\n"
                        f"He notado que '{prompt}' podría no ser una carrera tecnológica. "
                        "¡Por favor, intenta de nuevo con una carrera relacionada con tecnología!\n\n"
                        "Ejemplo: 'Desarrollador Frontend' o 'Científico de Datos'"
                    ),
                    "resources": [
                        {
                            "title": "Guía de Carreras Tech",
                            "url": "https://roadmap.sh",
                            "type": "article"
                        }
                    ],
                    "children": []
                }
            }
        else:
            return {
                "data": {
                    "id": "error",
                    "title": "Invalid Career Path",
                    "description": (
                        "🤖 Hello! I'm TechBot, your technology career advisor.\n\n"
                        "I specialize in creating learning paths for technology careers such as:\n"
                        "• Software Development (Frontend, Backend, Full Stack)\n"
                        "• Data Science & AI/ML Engineering\n"
                        "• Cloud & DevOps Engineering\n"
                        "• Cybersecurity & Network Engineering\n"
                        "• QA & Software Testing\n\n"
                        f"I noticed that '{prompt}' might not be a tech career. "
                        "Please try again with a technology-related role!\n\n"
                        "Example: 'Frontend Developer' or 'Data Scientist'"
                    ),
                    "resources": [
                        {
                            "title": "Tech Career Guide",
                            "url": "https://roadmap.sh",
                            "type": "article"
                        }
                    ],
                    "children": []
                }
            }

    async def initialize(self) -> None:
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            temperature=0.2,
            openai_api_key=self.settings.OPENAI_API_KEY
        )

    async def generate_response(self, prompt: str, **kwargs) -> Any:
        if not self.llm:
            await self.initialize()

        # Input validation
        if not prompt or len(prompt.strip()) < 2:
            return self._get_error_message("empty input")

        # Check for non-tech inputs
        if not self._is_tech_career(prompt):
            return self._get_error_message(prompt)

        # Detect language
        language = self._detect_language(prompt)
        
        system_prompt = """You are an expert technical mentor creating learning paths for technology careers.
You must respond in the same language as the user's input (Spanish or English).
Create a structured, practical learning path following these rules:

1. Format each topic exactly as shown:
   1. Main Topic Name (2-3 words maximum)
      - Brief, clear description (one line)
      - Resource: [Resource Name] https://real-url.com
      - Subtopics:
        a) Subtopic Name (2-3 words maximum)
           - Brief description
           - Resource: [Resource Name] https://real-url.com

2. Content rules:
   - Use simple, clear titles
   - Keep descriptions concise and practical
   - Include only real, accessible learning resources
   - Focus on fundamental concepts first
   - Include 2-3 main topics with 1-2 subtopics each

3. Resource guidelines:
   - Use well-known platforms (MDN, freeCodeCamp, Udemy, etc.)
   - Mix resource types (articles, videos, courses)
   - Ensure all URLs are real and accessible
   - Prefer free resources when possible

Remember: Keep everything simple, practical, and focused on core concepts.
IMPORTANT: Respond in the same language as the input prompt."""

        user_prompt = f"Create a focused learning path for {prompt}. Include essential skills and technologies only."

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        try:
            response = self.llm.invoke(prompt_template.format())
            return response.content
        except Exception as e:
            print(f"Error getting AI response: {str(e)}")
            raise ValueError(f"Failed to generate learning path: {str(e)}") 