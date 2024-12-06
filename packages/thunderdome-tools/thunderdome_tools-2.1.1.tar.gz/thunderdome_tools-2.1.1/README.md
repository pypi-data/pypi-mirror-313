### Updated Documentation for ThunderTools

# ThunderTools

**ThunderTools** is a Python package designed to streamline development and provide consistent, reusable tools for projects like Thunderdome. It includes utilities for API configuration, validation, and interaction with external systems, promoting efficient and standardized workflows.

---

## Tools in ThunderTools

1. **ThunderConfig**
   - A comprehensive utility for creating, validating, and serializing API configurations.
   - Supports environment variable integration for dynamic and flexible configuration management.
   - Enables seamless integration with machine learning models, external APIs, and custom workflows.

---

## Installation

Install ThunderTools using pip:

```bash
pip install thunderdome-tools
```

---

# ThunderTools Documentation

## Overview

The **ThunderTools** package is designed to house a variety of tools that support AI-driven applications. Each tool within the package is modular and serves a specific purpose. This documentation provides an in-depth guide to the first tool in the package: **ThunderConfig**. Future tools can be added following the structure and principles outlined here.

---

## Table of Contents

1. **ThunderConfig Tool**
   - Purpose
   - Classes
     - InputModel
     - ConfigModel
     - ThunderInput
     - ThunderConfigHandler
   - Environment Variables
   - Usage Examples
   - Error Handling
2. **Adding New Tools**
   - Guidelines
   - Code Structure
   - Best Practices
3. **Future Additions**

---

## 1. ThunderConfig Tool

### Purpose

**ThunderConfig** is a configuration management tool that simplifies the setup and initialization of AI-driven agents. It provides a structured way to handle user inputs, application configurations, and model parameters.

---

### Classes

#### 1. InputModel

Represents the main input for the agent.

**Attributes**:

- `input_value` (`str`): The main input value for the agent, such as a command or query.

#### 2. ConfigModel

Handles the configuration details for the agent.

**Attributes**:

- `user_id` (`str`): The user ID for whom the agent is executed.
- `actions` (`Optional[List[str]]`): List of actions the agent can perform.
- `app` (`Optional[str]`): The application for which the agent is configured.
- `integration_id` (`Optional[str]`): Integration ID for the app.
- `max_tokens` (`Optional[int]`): Maximum tokens for the model.
- `model` (`Optional[str]`): Model name.
- `model_provider` (`Optional[str]`): Model provider (e.g., OpenAI, Azure, LiteLLM).
- `prompt` (`Optional[str]`): Prompt for the agent.
- `provider_kwargs` (`Optional[Dict[str, Any]]`): Additional provider-specific keyword arguments.
- `temperature` (`Optional[float]`): Temperature for the model.

#### 3. ThunderInput

A wrapper model that combines `InputModel` and `ConfigModel`.

**Attributes**:

- `input` (`InputModel`): Contains the agent input value.
- `config` (`ConfigModel`): Holds the configuration details for the agent.
- `kwargs` (`Dict`): Additional keyword arguments.

#### 4. ThunderConfigHandler

The main handler class for processing configurations and initializing the LLM.

**Methods**:

1. `__init__(config)`: Initializes the configuration handler.
2. `load_defaults()`: Loads default values from environment variables.
3. `set_langchain_env_variables()`: Sets environment variables for LangChain.
4. `process_config(input_config: ThunderInput) -> Dict[str, Any]`: Processes the input configuration and merges it with defaults.
5. `init_llm()`: Initializes the language model using the processed configuration.

---

### Environment Variables

The following environment variables are used for default configuration:

#### LangChain Variables

- `LANGCHAIN_API_KEY`
- `LANGCHAIN_TRACING_V2`
- `LANGCHAIN_ENDPOINT`
- `LANGCHAIN_PROJECT`

#### Model Configuration

- `DEFAULT_MODEL_PROVIDER`
- `DEFAULT_MODEL`
- `DEFAULT_TEMPERATURE`
- `DEFAULT_MAX_TOKENS`
- `DEFAULT_APP`
- `DEFAULT_PROMPT`
- `DEFAULT_ACTIONS`
- `DEFAULT_INTEGRATION`

#### Provider-Specific Variables

- OpenAI: `OPENAI_API_KEY`, `OPENAI_API_BASE`
- Azure OpenAI: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_API_BASE`, `AZURE_OPENAI_API_VERSION`, `AZURE_DEPLOYMENT_NAME`
- LiteLLM: `LITELLM_API_KEY`, `LITELLM_SERVER_URL`

---

### Usage Examples

#### Example 1: Basic Configuration Input

```python
from ThunderTools.ThunderConfig import ThunderInput, ThunderConfigHandler

input_data = ThunderInput(
    input={
        "input_value": "Send an email to someone@example.com saying hi"
    },
    config={
        "user_id": "user123",
        "actions": ["GMAIL_SEND_EMAIL"],
        "app": "GMAIL",
        "integration_id": "your_integration_id",
        "max_tokens": 1000,
        "model": "gpt-4",
        "model_provider": "openai",
        "prompt": "You are a helpful assistant.",
        "provider_kwargs": {
            "openai_api_key": "your_openai_api_key"
        },
        "temperature": 0.7
    },
    kwargs={}
)

handler = ThunderConfigHandler(config=input_data)
llm = handler.init_llm()
```

---

### Error Handling

1. **Missing Required Fields**:

   - Example: `ValueError: user_id is required in config or .env`
   - Solution: Ensure `user_id` is provided in the configuration or environment variables.

2. **Unsupported Model Provider**:

   - Example: `ValueError: Model provider {provider_name} is not supported.`
   - Solution: Ensure `model_provider` is one of the supported options (`openai`, `azure`, `litellm`).

3. **Invalid Provider-Specific Configurations**:
   - Example: `provider_kwargs must be a dictionary`
   - Solution: Ensure `provider_kwargs` is a valid dictionary.

---

## 2. Adding New Tools

### Guidelines

1. **Create a New Tool**:

   - Add a new class or module in the `ThunderTools` package.

2. **Follow the Structure**:

   - Use `BaseModel` for structured data models.
   - Provide thorough docstrings and examples.

3. **Environment Variable Integration**:
   - Use `os.getenv` for default values.
   - Include necessary environment variables in the documentation.
