# XLiteLLM: A Lightweight Wrapper for LLM API Calls

XLiteLLM is a Python library designed to simplify interaction with Large Language Models (LLMs). It provides both synchronous and asynchronous interfaces for making requests to LLMs, with built-in support for retries, JSON response handling, and logging. XLiteLLM supports passing user, system, assistant prompts, optional images, and various configuration options for controlling model behavior.

## Features

- Synchronous and Asynchronous API Calls: Support for both blocking and non-blocking interaction with LLMs.
- Flexible Prompt Construction: Combine user, system, assistant prompts, with optional image inputs.
- JSON Response Processing: Easily extract structured data from model responses.
- Retry Mechanism: Automatically retry failed requests up to a configurable limit.
- Configurable Parameters: Customize model settings such as temperature, token limits, and timeout.
- Logging Integration: Built-in logging for monitoring requests, responses, and errors.

## Repository Structure

The project is organized as follows:

```
.
├── README.md                # Project documentation
├── examples/
│   ├── example_usage.py     # Example usage of the library
│   ├── requirements.txt     # Dependencies for running examples
│   └── .env.example         # Template for environment variables
├── setup.py                 # Installation script
├── xlitellm/
│   ├── __init__.py          # Module initialization
│   └── client.py            # Core functionality for interacting with LLMs
```

### Key Files:
- `xlitellm/client.py`: Contains the core functions (`call_llm` and `call_llm_async`) to interact with LLM APIs.
- `examples/example_usage.py`: Demonstrates how to use the library in synchronous and asynchronous contexts.
- `examples/.env.example`: A template for the environment variables required to run the examples.

## Installation

### Requirements

- Python 3.11 or higher

### Setup

```bash
pip install xlitellm
```

## Configuration

Before running the example scripts, you need to provide values for the required environment variables. Use the `.env.example` file in the `examples/` directory as a starting point:

### `.env.example`:

```
LOG_LEVEL=
MISTRAL_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=
ANTHROPIC_API_KEY=
GROQ_API_KEY=
```

1. Duplicate the `.env.example` file and rename it to `.env`:

    ```bash
    cp examples/.env.example examples/.env
    ```

2. Populate the `.env` file with appropriate values for your environment.

## Usage

### Core Functions

#### `call_llm`

Synchronous function for making LLM API calls.

- Parameters:
  - `user_prompt` (str): The user's input prompt.
  - `system_prompt` (str): Optional system message to guide the LLM's behavior.
  - `assist_prompt` (str): Optional assistant message to guide the LLM's behavior. This works on Mistral, Claude, Gemini, Groq, but not on GPT.
  - `images` (list[str], optional): List of image URLs or base64 strings for visual context.
  - `model` (str): Model identifier (e.g., `claude-3-5-sonnet-20241022`).
  - `temperature` (float): Sampling temperature to control response randomness.
  - `max_tokens` (int): Maximum number of tokens in the response.
  - `timeout` (int, optional): Time (in seconds) before the request times out.
  - `max_retry` (int): Maximum number of retries for failed requests.
  - `json_mode` (bool): Whether to parse the response as JSON.

- Returns: Response as a string or dictionary.

#### `call_llm_async`

Asynchronous version of `call_llm`, supporting the same parameters and functionality.

### Running the Examples

1. Navigate to the `examples` folder:

    ```bash
    cd examples
    ```

2. Ensure you have created and populated the `.env` file as described above.

3. Run the synchronous and asynchronous examples:

    ```bash
    python example_usage.py
    ```

---

Last updated: 2024/12/05
