import os
import json
import logging
from litellm import completion, acompletion

logger = logging.getLogger(__name__)


def _construct_prompts_and_messages(
    user_prompt: str,
    system_prompt: str,
    images: list[str] | None,
    model: str,
) -> list[dict]:
    """
    Constructs the input messages for the LLM call based on user prompts, system prompts, and optional images.
    """

    # Construct user prompts
    prompts = []
    for image in images or []:
        prompts.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}",
                    "detail": "high",
                },
            }
        )
    prompts.append({"type": "text", "text": user_prompt})

    # Add system prompt
    messages = []
    if system_prompt and model not in {
        "groq/llava-v1.5-7b-4096-preview",
        "groq/llama-3.2-11b-vision-preview",
        "groq/llama-3.2-90b-vision-preview",
    }:
        messages.append({"content": system_prompt, "role": "system"})
    messages.append({"content": prompts, "role": "user"})

    return messages


def _process_response(response, json_mode: bool):
    """
    Processes the response from the LLM, extracting JSON data if required.
    """

    resp_txt = response.choices[0].message.content

    if json_mode:
        resp_txt = resp_txt[resp_txt.find("{") : resp_txt.rfind("}") + 1]
        output_json = json.loads(resp_txt)
        logger.debug(f"LLM JSON resp: {json.dumps(output_json, indent=4)}")
        return output_json
    else:
        logger.debug(f"LLM text resp: {resp_txt}")
        return resp_txt


async def call_llm_async(
    user_prompt: str,
    system_prompt: str = "",
    images: list[str] | None = None,
    model: str = "claude-3-5-sonnet-20241022",
    temperature: float = 0,
    max_tokens: int = 3000,
    timeout: int | None = None,
    max_retry: int = 3,
    json_mode: bool = True,
) -> str | dict:
    """
    Makes an asynchronous call to the LLM with retries and processes the response.
    """

    messages = _construct_prompts_and_messages(
        user_prompt, system_prompt, images, model
    )

    retry = 0
    response = None
    while True:
        try:
            logger.info(f"Attempt: {retry}")
            logger.info(f"Calling LLM {model}")

            response = await acompletion(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )

            result = _process_response(response, json_mode)
            break
        except Exception as e:
            logger.error(f"LLM call failed: {e}", exc_info=True)
            retry += 1
            if retry > max_retry:
                logger.error(f"Gave up after {max_retry} retries")
                raise e
    if response:
        logger.info(str(response.usage))

    return result


def call_llm(
    user_prompt: str,
    system_prompt: str = "",
    images: list[str] | None = None,
    model: str = "claude-3-5-sonnet-20241022",
    temperature: float = 0,
    max_tokens: int = 3000,
    timeout: int | None = None,
    max_retry: int = 3,
    json_mode: bool = True,
) -> str | dict:
    """
    Makes a synchronous call to the LLM with retries and processes the response.
    """

    messages = _construct_prompts_and_messages(
        user_prompt, system_prompt, images, model
    )

    retry = 0
    response = None
    while True:
        try:
            logger.info(f"Attempt: {retry}")
            logger.info(f"Calling LLM {model}")

            response = completion(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )

            result = _process_response(response, json_mode)
            break
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            retry += 1
            if retry > max_retry:
                logger.error(f"Gave up after {max_retry} retries")
                raise e
    if response:
        logger.info(str(response.usage))

    return result
