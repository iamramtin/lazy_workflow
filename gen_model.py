import os
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(format="%(levelname)s - %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

class GenModel:
    def __init__(self, api_key=None, model_name='gemini-pro', verbose=False):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.model_name = model_name
        self.model = None

        self._set_logging_level(verbose)
        self._configure()

    def _configure(self):
        """
        Configure the generative AI model with the provided API key.
        """
        if not self.api_key:
            logger.error("GOOGLE_API_KEY is not set.")
            raise ValueError("GOOGLE_API_KEY is not set.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        logger.debug(f"Configured Gemini model '{self.model_name}' with provided API key.")

    def _set_logging_level(self, verbose):
        """
        Set logging level.
        """
        level = logging.DEBUG if verbose else logging.INFO
        logger.setLevel(level)

    def generate_from_prompt(self, prompt, **kwargs):
        """
        Generate content using the configured Gemini model based on the given prompt.
        
        Parameters:
            prompt (str): The prompt to generate content from. Can include placeholders for keyword arguments.
            **kwargs: Keyword arguments to customize the generation.

        Returns:
            str: Generated content.
        """
        if not self.model:
            raise ValueError("Gemini model not configured. Call configure() first.")
        
        logger.debug("Generating content with prompt")
        full_prompt = prompt.format(**kwargs)
        
        return self.model.generate_content(full_prompt).text
