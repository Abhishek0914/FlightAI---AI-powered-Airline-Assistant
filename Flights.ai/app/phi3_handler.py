import requests
import json

class Phi3Chat:
    def __init__(self, model_name="phi3:mini"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434/api/generate"  # Ollama local endpoint

    def chat(self, prompt):
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.base_url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "I'm sorry, I couldn't generate a reply.")
            else:
                return f"Error: {response.status_code} from Ollama"
        except Exception as e:
            return f"Model error: {e}"


def chat(prompt, model_name="phi3:mini"):
    """Module-level helper to match existing imports.
    Creates a Phi3Chat and returns its response for the given prompt.
    """
    client = Phi3Chat(model_name=model_name)
    return client.chat(prompt)
