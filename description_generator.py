from config import LLM_CONFIG
from prompts import TABLE_DESCRIPTION_PROMPT, COLUMN_DESCRIPTION_PROMPT, DESCRIPTION_SYSTEM_PROMPT
from llm_provider import get_provider

def generate_description(item_name, item_type, data_type=None):
    """Generate a description for a table or column using configured LLM"""
    if item_type == "table":
        prompt = TABLE_DESCRIPTION_PROMPT.format(item_name=item_name)
    elif item_type == "column":
        prompt = COLUMN_DESCRIPTION_PROMPT.format(item_name=item_name, data_type=data_type)

    provider = get_provider()
    description = provider.chat(
        messages=[
            {"role": "system", "content": DESCRIPTION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=LLM_CONFIG['max_tokens'],
        temperature=LLM_CONFIG['temperature']
    )

    return description
