import time
import json
from os import getenv
from typing import Optional

from phi.agent import Agent
from phi.tools import Toolkit
from phi.utils.log import logger

try:
    import requests
except ImportError:
    raise ImportError("`requests` not installed. Please install using `pip install requests`")


class ModelsLabs(Toolkit):
    def __init__(
        self,
        api_key: Optional[str] = None,
        url: str = "https://modelslab.com/api/v6/video/text2video",
        wait_for_completion: bool = False,
    ):
        super().__init__(name="models_labs")

        self.url = url
        self.wait_for_completion = wait_for_completion
        self.api_key = api_key or getenv("MODELS_LAB_API_KEY")
        if not self.api_key:
            logger.error("MODELS_LAB_API_KEY not set. Please set the MODELS_LAB_API_KEY environment variable.")

        self.register(self.generate_video)

    def generate_video(self, agent: Agent, prompt: str) -> str:
        """Use this function to generate a video given a prompt.

        Args:
            prompt (str): A text description of the desired video.

        Returns:
            str: A message indicating if the video has been generated successfully or an error message.
        """
        if not self.api_key:
            return "Please set the MODELS_LAB_API_KEY"

        try:
            payload = json.dumps(
                {
                    "key": self.api_key,
                    "prompt": prompt,
                    "height": 512,
                    "width": 512,
                    "num_frames": 25,
                    "webhook": None,
                    "output_type": "gif",
                    "track_id": None,
                    "negative_prompt": "low quality",
                    "model_id": "cogvideox",
                    "instant_response": False,
                }
            )

            headers = {"Content-Type": "application/json"}
            logger.debug(f"Generating video for prompt: {prompt}")
            response = requests.request("POST", self.url, data=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            if "error" in result:
                logger.error(f"Failed to generate video: {result['error']}")
                return f"Error: {result['error']}"

            eta = result["eta"]
            video_url_links = result["future_links"]
            logger.info(f"Video will be ready in {eta} seconds")
            logger.info(f"Video URLs: {video_url_links}")

            video_data = []
            for video_url in video_url_links:
                video_data.append(
                    {
                        "eta": eta,
                        "url": video_url,
                    }
                )
            result["data"] = video_data
            logger.debug(f"Result: {result}")

            # Update the run response with the image URLs
            agent.add_video(json.dumps(result))

            if self.wait_for_completion and isinstance(eta, int):
                logger.info(f"Waiting for {eta} seconds for video to be ready")
                time.sleep(eta)

            return f"Video has been generated successfully and will be ready in {eta} seconds"
        except Exception as e:
            logger.error(f"Failed to generate video: {e}")
            return f"Error: {e}"
