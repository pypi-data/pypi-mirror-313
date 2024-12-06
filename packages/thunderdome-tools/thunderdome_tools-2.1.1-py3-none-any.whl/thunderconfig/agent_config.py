from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict, List, Optional
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# Updated ConfigModel with agentauthtkn and handler
class InputModel(BaseModel):
    input_value: str = Field(..., description="The main input value for the agent, such as a command or query.")

class ConfigModel(BaseModel):
    user_id: str = Field(..., description="User ID for whom the agent is executed.")
    userkey: Optional[str] = Field(None, description="User-specific key for authentication or identification.")
    agentauthtkn: Optional[str] = Field(None, description="Agent authentication token for secure agent operations.")
    actions: Optional[List[str]] = Field(None, description="List of actions the agent can perform.")
    app: Optional[str] = Field(None, description="The app for which the agent is configured.")
    integration_id: Optional[str] = Field(None, description="Integration ID for the app.")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for the model.")
    model: Optional[str] = Field(None, description="Model name.")
    llm_provider: Optional[str] = Field(None, description="Model provider, e.g., 'openai'.")
    prompt: Optional[str] = Field(None, description="Prompt for the agent.")
    provider_kwargs: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional provider-specific keyword arguments."
    )
    temperature: Optional[float] = Field(None, description="Temperature for the model.")
    handler: Optional[str] = Field( 
        None, description="Specifies the handler logic or endpoint for processing."
    )
    class Config:
        
        json_schema_extra = {
            "examples": [
                {
                    "user_id": "testing-langserve",
                    "userkey": "example_user_key_12345",
                    "agentauthtkn": "example_agent_auth_token_67890",
                    "actions": [
                        "GMAIL_SEND_EMAIL",
                        "GMAIL_FETCH_EMAILS"
                    ],
                    "app": "GMAIL",
                    "integration_id": "your_integration_id",
                    "max_tokens": 16384,
                    "model": "gpt-4",
                    "llm_provider": "openai",
                    "prompt": "You are a helpful assistant that can perform tasks with the user's email account.",
                    "provider_kwargs": {
                        "openai_api_base": "https://your-custom-openai-endpoint.com/v1",
                        "openai_api_key": "your_override_openai_api_key"
                    },
                    "temperature": 0,
                    "handler": "whatsapp"  # Updated field name
                }
            ]
        }

class ThunderInput(BaseModel):
    input: InputModel = Field(..., description="The input message for the agent, containing 'input_value'.")
    config: ConfigModel = Field(..., description="Configuration parameters for the agent.")
    kwargs: Dict = Field({}, description="Additional keyword arguments for the agent.")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "config": {
                        "user_id": "testing-langserve",
                        "userkey": "example_user_key_12345",
                        "agentauthtkn": "example_agent_auth_token_67890",
                        "actions": [
                            "GMAIL_SEND_EMAIL",
                            "GMAIL_FETCH_EMAILS"
                        ],
                        "app": "GMAIL",
                        "integration_id": "your_integration_id",
                        "max_tokens": 16384,
                        "model": "gpt-4",
                        "llm_provider": "openai",
                        "prompt": "You are a helpful assistant that can perform tasks with the user's email account.",
                        "provider_kwargs": {
                            "openai_api_base": "https://your-custom-openai-endpoint.com/v1",
                            "openai_api_key": "your_override_openai_api_key"
                        },
                        "temperature": 0,
                        "handler": "whatsapp"  # Updated field name
                    },
                    "input": {
                        "input_value": "Send an email to someone@example.com saying hi"
                    },
                    "kwargs": {}
                }
            ]
        }

class ThunderConfigHandler:
    def __init__(self, input_config: ThunderInput):
        self.load_defaults()
        # self.set_langchain_env_variables()
        self.config = self.process_config(input_config)
        self.agentauthtoken = self.config.get('agentauthtkn') # Store agent auth token

    def load_defaults(self):
        # LangChain configuration
        load_dotenv()
        self.LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', 'your_default_langchain_api_key')
        self.LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'true')
        self.LANGCHAIN_ENDPOINT = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
        self.LANGCHAIN_PROJECT = os.getenv('LANGCHAIN_PROJECT', 'default_project')

        # Default model configuration
        self.DEFAULT_LLM_PROVIDER = os.getenv('DEFAULT_LLM_PROVIDER', 'openai')

        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
        self.OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

        self.AZURE_OPENAI_API_KEY=os.getenv('AZURE_OPENAI_API_KEY','your_azure_openai_api_key')
        self.AZURE_ENDPOINT=os.getenv('AZURE_ENDPOINT','https://your-resource-name.openai.azure.com/')
        self.AZURE_OPENAI_API_VERSION=os.getenv('AZURE_OPENAI_API_VERSION','2023-05-15')
        self.AZURE_DEPLOYMENT_NAME=os.getenv('AZURE_DEPLOYMENT_NAME','your-deployment-name')
        
        self.LITELLM_API_KEY=os.getenv('LITELLM_API_KEY','your-litellm-key')
        self.LITELLM_BASE_URL=os.getenv('LITELLM_BASE_URL', 'your-LITELLM_BASE_URL')

        self.DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gpt-4o')
        self.DEFAULT_TEMPERATURE = float(os.getenv('DEFAULT_TEMPERATURE', '0.0'))
        self.DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS', '16384'))
        self.DEFAULT_APP = os.getenv('DEFAULT_APP', 'GMAIL')
        self.DEFAULT_PROMPT = os.getenv('DEFAULT_PROMPT', 'You are a helpful assistant.')
        self.DEFAULT_ACTIONS = os.getenv('DEFAULT_ACTIONS', 'GMAIL_SEND_EMAIL/GMAIL_FETCH_EMAILS').split('/')
        self.DEFAULT_INTEGRATION = os.getenv('DEFAULT_INTEGRATION', '1867d112-4e54-4c25-a589-f418f56b72b7')
        self.DEFAULT_HANDLER = os.getenv('DEFAULT_HANDLER', 'default_handler')  # Updated default handler

      
    # def set_langchain_env_variables(self):
    #     # Set environment variables for LangChain
    #     os.environ['LANGCHAIN_API_KEY'] = self.LANGCHAIN_API_KEY
    #     os.environ['LANGCHAIN_TRACING_V2'] = self.LANGCHAIN_TRACING_V2
    #     os.environ['LANGCHAIN_ENDPOINT'] = self.LANGCHAIN_ENDPOINT
    #     os.environ['LANGCHAIN_PROJECT'] = self.LANGCHAIN_PROJECT

    def process_config(self, input_config: ThunderInput) -> Dict[str, Any]:
        config = {}

        # User ID
        config['user_id'] = input_config.config.user_id
        if not config['user_id']:
            raise ValueError("user_id is required in config or .env")
        # User key
        config['userkey'] = input_config.config.userkey

        # Agent authentication token
        config['agentauthtkn'] = input_config.config.agentauthtkn
        if not config['agentauthtkn']:
            raise ValueError("agentauthtkn is required for agent authentication")

        # App name
        config['app'] = input_config.config.app or self.DEFAULT_APP

        # Integration ID
        config['integration_id'] = input_config.config.integration_id or self.DEFAULT_INTEGRATION

        # Prompt
        config['prompt'] = input_config.config.prompt or self.DEFAULT_PROMPT

        # Actions
        config['actions'] = input_config.config.actions or self.DEFAULT_ACTIONS

        # Handler
        config['handler'] = input_config.config.handler or self.DEFAULT_HANDLER

        # Model configuration
        config['model'] = input_config.config.model or self.DEFAULT_MODEL
        config['temperature'] = input_config.config.temperature if input_config.config.temperature is not None else self.DEFAULT_TEMPERATURE
        config['max_tokens'] = input_config.config.max_tokens or self.DEFAULT_MAX_TOKENS
        config['llm_provider'] = input_config.config.llm_provider or self.DEFAULT_LLM_PROVIDER

        # Provider-specific kwargs
        config['provider_kwargs'] = input_config.config.provider_kwargs or {}

        return config

    def init_llm(self):
        # Basic LLM configuration
        llm_config = {
            "model": self.config.get('model'),
            "max_tokens": self.config.get('max_tokens'),
            "temperature": self.config.get('temperature'),
        }


        # Initialize provider-specific keyword arguments
        provider_kwargs = {}

        if self.config['llm_provider']== 'openai':
            provider_kwargs = {
                "model_provider": self.config['llm_provider'],
                "openai_api_key": self.OPENAI_API_KEY,
                "openai_api_base": self.OPENAI_API_BASE
            }
        elif self.config['llm_provider'] == 'azure' or self.config['llm_provider'] == 'azure_openai':
            provider_kwargs = {
                "model_provider": self.config['llm_provider'],
                "api_key": self.AZURE_OPENAI_API_KEY,
                "azure_endpoint": self.AZURE_ENDPOINT,
                "api_version":self.AZURE_OPENAI_API_VERSION
            }
        elif self.config['llm_provider'] == 'litellm':
            provider_kwargs = {
                "api_key": self.LITELLM_API_KEY,
                "base_url": self.LITELLM_BASE_URL
            }
        else:
            raise ValueError(f"Unsupported model provider: {self.llm_provider}")

        # Merge any additional provider_kwargs from the config
        additional_kwargs = self.config.get('provider_kwargs', {})
        if additional_kwargs:
            if isinstance(additional_kwargs, dict):
                provider_kwargs.update(additional_kwargs)
            else:
                raise ValueError("provider_kwargs must be a dictionary")
    
        # Combine all configurations, excluding any None values
        filtered_config = {k: v for k, v in llm_config.items() if v is not None}
        filtered_config.update(provider_kwargs)
        
        print("Final LLM Configuration:", filtered_config)

        try:
            llm = init_chat_model(**filtered_config)
            return llm
        except Exception as e:
            print(f"Error initializing chat model: {e}")
            raise
