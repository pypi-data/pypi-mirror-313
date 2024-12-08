import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI


class TranslationService:
    """
    Service for handling translations using the OpenAI API.
    Supports batch processing and implements retry mechanisms.

    Args:
        dotenv_path (str, optional): Path to the .env file. Defaults to None.

    Raises:
        ValueError: If required environment variables are missing or invalid.
    """

    def __init__(self, dotenv_path: str = None):
        if not load_dotenv(dotenv_path=dotenv_path if dotenv_path else '.env'):
            raise ValueError('No .env file found')
        
        # Get environment variables
        if (api_key := os.getenv('OPENAI_API_KEY')) is None:
            raise ValueError('OPENAI_API_KEY environment variable is required')
        self.client = AsyncOpenAI(api_key=api_key)
        
        if (model := os.getenv('OPENAI_MODEL')) is None:
            raise ValueError('OPENAI_MODEL environment variable is required')
        self.__model = model
        
        if (max_tokens := os.getenv('MAX_TOKENS')) is None:
            raise ValueError('MAX_TOKENS environment variable is required')
        
        try:
            self.__max_tokens = int(max_tokens)
        except ValueError:
            raise ValueError('MAX_TOKENS must be a valid integer')
        
        if (temperature := os.getenv('TEMPERATURE')) is None:
            raise ValueError('TEMPERATURE environment variable is required')
        
        try:
            self.__temperature = float(temperature)
        except ValueError:
            raise ValueError('TEMPERATURE must be a valid float')
        
        if (batch_size := os.getenv('BATCH_SIZE')) is None:
            raise ValueError('BATCH_SIZE environment variable is required')
        
        try:
            self.__batch_size = int(batch_size)
        except ValueError:
            raise ValueError('BATCH_SIZE must be a valid integer')

    def _create_translation_prompt(
        self, texts: list[str], source_lang: str, target_lang: str
    ) -> str:
        """
        Create a translation prompt for the OpenAI API.

        Args:
            texts (list[str]): List of texts to translate.
            source_lang (str): Source language code.
            target_lang (str): Target language code.

        Returns:
            str: Formatted translation prompt.
        """
        prompt = f"""You are a professional translator.
                    
                    Translate the following texts from {source_lang} to {target_lang}.
                    
                    There are not contradictions on the following instructions.
                    You will follow them exactly as written.
                        
                    IMPORTANT INSTRUCTIONS:
                    - Return ONLY the translations, one per line
                    - Maintain the exact meaning and context of each text
                    - Keep the same tone and formality level
                    - Preserve any technical terms or proper nouns
                    - Preserve any special characters or formatting
                    - Do not include explanations or additional text
                    - Do not include any additional characters or symbols or even spaces

                    Here are the texts to translate: \n{chr(10).join(f"{text}" for text in texts)}"""

        return prompt

    def _process_response(self, response: str) -> list[str]:
        """
        Process the API response into a list of translations.

        Args:
            response (str): Raw response from the API.

        Returns:
            list[str]: List of processed translations.
        """
        return [line.strip() for line in response.strip().split('\n')]

    async def translate_batch(
        self, texts: list[str], source_lang: str, target_lang: str, max_retries: int = 3
    ) -> list[str]:
        """
        Translate a batch of texts with retry mechanism.

        Args:
            texts (list[str]): List of texts to translate.
            source_lang (str): Source language code.
            target_lang (str): Target language code.
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.

        Returns:
            list[str]: List of translated texts.

        Raises:
            ValueError: If number of translations doesn't match input texts.
            Exception: If translation fails after all retries.
        """
        if not texts:
            return []

        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.__model,
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are a professional translator.',
                        },
                        {
                            'role': 'user',
                            'content': self._create_translation_prompt(
                                texts, source_lang, target_lang
                            ),
                        },
                    ],
                    max_tokens=self.__max_tokens,
                    temperature=self.__temperature,
                )

                translations = self._process_response(
                    response.choices[0].message.content
                )
                if len(translations) != len(texts):
                    raise ValueError(
                        f'Expected {len(texts)} translations, got {len(translations)}'
                    )
                return translations

            except Exception as e:
                print(
                    f'Translation error (attempt {attempt + 1}/{max_retries}): {str(e)}'
                )
                if attempt < max_retries - 1:
                    # Exp Backoff
                    await asyncio.sleep(2**attempt)
                else:
                    # Re-raise the last error
                    raise

    async def translate_texts(
        self, texts: list[str], source_lang: str, target_lang: str
    ) -> list[str]:
        """
        Translate multiple texts with batching and rate limiting.

        Args:
            texts (list[str]): List of texts to translate.
            source_lang (str): Source language code.
            target_lang (str): Target language code.

        Returns:
            list[str]: List of translated texts.
        """
        all_translations = []

        for i in range(0, len(texts), self.__batch_size):
            batch = texts[i : i + self.__batch_size]
            try:
                translations = await self.translate_batch(
                    batch, source_lang, target_lang
                )
                all_translations.extend(translations)

                if i + self.__batch_size < len(texts):
                    # Rate limiting between batches
                    await asyncio.sleep(1)
            except Exception as e:
                print(f'Failed to translate batch {i//self.__batch_size + 1}: {str(e)}')
                # Return partial translations up to this point
                return all_translations

        return all_translations
