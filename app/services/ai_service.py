from typing import Dict, List
import re
from app.ai_integration.factory import AIProviderFactory
from app.core.settings import get_settings

class AIService:
    def __init__(self):
        settings = get_settings()
        self.ai_provider = AIProviderFactory.get_provider("langchain")

    def _parse_topics(self, content: str) -> List[Dict]:
        topics = []
        current_topic = None
        current_subtopic = None
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Main topic (starts with number)
            if re.match(r'^\d+\.', line):
                if current_topic:
                    topics.append(current_topic)
                topic_name = re.sub(r'^.*?:\s*', '', line.split('.', 1)[1].strip())
                current_topic = {
                    "id": self._create_id(topic_name),
                    "title": topic_name,
                    "description": "",
                    "resources": [],
                    "children": []
                }
                current_subtopic = None

            # Subtopic
            elif re.match(r'^[a-z]\)', line):
                if current_topic:
                    subtopic_name = re.sub(r'^.*?:\s*', '', re.sub(r'^[a-z]\)\s*', '', line))
                    current_subtopic = {
                        "id": self._create_id(subtopic_name),
                        "title": subtopic_name,
                        "description": "",
                        "resources": []
                    }
                    current_topic["children"].append(current_subtopic)

            # Resource line
            elif 'Resource:' in line or 'http' in line.lower():
                resource = self._parse_resource(line)
                if current_subtopic:
                    current_subtopic["resources"].append(resource)
                elif current_topic:
                    current_topic["resources"].append(resource)

            # Description line
            elif line.startswith('-'):
                description = line.lstrip('- ').strip()
                description = re.sub(r'^Description:\s*', '', description)
                if current_subtopic:
                    current_subtopic["description"] = description
                elif current_topic:
                    current_topic["description"] = description

        if current_topic:
            topics.append(current_topic)

        return topics

    def _parse_resource(self, line: str) -> Dict:
        resource_type = "article"
        if "video" in line.lower() or "youtube" in line.lower():
            resource_type = "video"
        elif "course" in line.lower() or "tutorial" in line.lower():
            resource_type = "course"

        url_match = re.search(r'https?://[^\s]+', line)
        url = url_match.group(0) if url_match else "https://roadmap.sh"

        title_match = re.search(r'\[(.*?)\]', line)
        if title_match:
            title = title_match.group(1)
        else:
            title = line.split('Resource:', 1)[-1].split('http')[0].strip()
            if not title:
                title = "Learning Resource"

        return {
            "title": title,
            "url": url,
            "type": resource_type
        }

    def _create_id(self, title: str) -> str:
        return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    async def generate_response(self, prompt: str) -> Dict:
        raw_response = await self.ai_provider.generate_response(prompt)
        
        # If the response is already a dictionary (error message), return it directly
        if isinstance(raw_response, dict):
            return raw_response
            
        # Otherwise, parse the content and create the learning path
        topics = self._parse_topics(raw_response)
        
        return {
            "data": {
                "id": "root",
                "title": prompt,
                "description": f"Complete learning path for {prompt}",
                "resources": [
                    {
                        "title": f"{prompt} Roadmap",
                        "url": "https://roadmap.sh",
                        "type": "article"
                    }
                ],
                "children": topics
            }
        } 