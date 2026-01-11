from openai import OpenAI
from config import OPENAI_API_KEY, LLM_CONFIG
from prompts import TABLE_DESCRIPTION_PROMPT, COLUMN_DESCRIPTION_PROMPT, DESCRIPTION_SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_description(item_name, item_type, data_type=None):
    """Generate a description for a table or column using OpenAI's API"""
    if item_type == "table":
        prompt = TABLE_DESCRIPTION_PROMPT.format(item_name=item_name)
    elif item_type == "column":
        prompt = COLUMN_DESCRIPTION_PROMPT.format(item_name=item_name, data_type=data_type)

    response = client.chat.completions.create(
        model=LLM_CONFIG['model'],
        messages=[
            {"role": "system", "content": DESCRIPTION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=LLM_CONFIG['max_tokens'],
        temperature=LLM_CONFIG['temperature']
    )

    description = response.choices[0].message.content.strip()
    return description
