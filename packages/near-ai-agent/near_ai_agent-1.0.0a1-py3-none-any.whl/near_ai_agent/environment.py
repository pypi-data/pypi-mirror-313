import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NearAIEnvironment")

class NearAIEnvironment:
    """
    Interface to NEAR AI Environment API.
    """
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url

    def get_context(self):
        """
        Retrieve the current context from the NEAR AI environment.
        """
        response = requests.get(f"{self.base_url}/context")
        if response.status_code == 200:
            logger.info(f"Context Retrieved: {response.json()}")
            return response.json()
        else:
            logger.error(f"Failed to get context: {response.text}")
            response.raise_for_status()

    def set_context(self, key, value):
        """
        Set a specific context key-value pair.
        """
        response = requests.post(f"{self.base_url}/context", json={key: value})
        if response.status_code == 200:
            logger.info(f"Context Updated: {key}={value}")
            return response.json()
        else:
            logger.error(f"Failed to set context: {response.text}")
            response.raise_for_status()

    def output(self, message):
        """
        Output a response via the NEAR AI environment.
        """
        response = requests.post(f"{self.base_url}/output", json={"message": message})
        if response.status_code == 200:
            logger.info(f"Output Sent: {message}")
            return response.json()
        else:
            logger.error(f"Failed to send output: {response.text}")
            response.raise_for_status()