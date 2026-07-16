from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from config import (
    BASE_URL,
    TEMPERATURE,
    NUM_CTX,
    NUM_PREDICT,
    LLAMA_MODEL_ID,
    GPT_MODEL_ID,
)


def initialize_model(model_id):
    return ChatOllama(
        model=model_id,
        base_url=BASE_URL,
        temperature=TEMPERATURE,
        num_ctx=NUM_CTX,
        nu_predict=NUM_PREDICT,
    )


llama_llm = initialize_model(LLAMA_MODEL_ID)
gpt_llm = initialize_model(GPT_MODEL_ID)


llama3_2_template = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpful assistant.
{system_prompt}

CRITICAL: You must output ONLY a valid JSON object populated with real data. 
DO NOT output the JSON schema itself. DO NOT include keys like "properties", "type", or "required" in your final answer.
Fill in the values based on the user's input.
The JSON must have EXACTLY this structure:
{{
"summary": "Summary of the user's message",
"sentiment": 45,
"response": "Suggested response to the user",
"category": "technical",
"action": "Recommended action for the support rep"
}}

{format_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
""",
    input_variables=["system_prompt", "format_prompt", "user_prompt"],
)

gpt_oss_template = PromptTemplate(
    template="""<|system|>{system_prompt}{format_prompt}<|user|>{user_prompt}<|assistant|>
""",
    input_variables=["system_prompt", "format_prompt", "user_prompt"],
)


class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(
        description="Sentiment score from 0 (negative) to 100 (positive)"
    )
    response: str = Field(description="Suggested response to the user")
    category: str = Field(
        description="Category of the inquiry (e.g., billing, technical, general)"
    )
    action: str = Field(description="Recommended action for the support rep")


json_parser = JsonOutputParser(pydantic_object=AIResponse)


def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke(
        {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "format_prompt": json_parser.get_format_instructions(),
        }
    )


def llama_response(system_prompt, user_prompt):
    return get_ai_response(llama_llm, llama3_2_template, system_prompt, user_prompt)


def gpt_oss_response(system_prompt, user_prompt):
    return get_ai_response(gpt_llm, gpt_oss_template, system_prompt, user_prompt)
