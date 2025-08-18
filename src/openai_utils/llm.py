import instructor
from openai import OpenAI
from pydantic import BaseModel
from typing import Type, TypeVar, List, Dict

T = TypeVar("T", bound=BaseModel)

def get_json_from_llm(
    schema: Type[T],
    prompts: List[Dict[str, str]],
    model: str = "gpt-4.1",
    temperature: float = 0.1
) -> T:
    """
    Generic function to generate structured JSON output from OpenAI using instructor.

    Args:
        schema (Type[T]): Pydantic model class for expected output.
        prompts (List[Dict[str, str]]): List of messages in OpenAI chat format:
                                        [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        model (str): The OpenAI model name (default: gpt-4.1).
        temperature (float): Sampling temperature.

    Returns:
        T: An instance of the provided schema class with the parsed data.
    """
    # Create OpenAI client with instructor patch
    client = instructor.patch(OpenAI())

    # Generate structured output directly into Pydantic schema
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=prompts,
        response_model=schema
    )

    return response
