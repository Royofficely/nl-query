import json
from openai import OpenAI
from datetime import datetime
from colorama import Fore
from utils import agent_print
from config import LLM_CONFIG, OPENAI_API_KEY
from prompts import SYSTEM_PROMPT, USER_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_sql(prompt, schema_chunk, config_chunk, db_structure_chunk, context):
    """Generate SQL query from natural language prompt using OpenAI"""
    agent_print("Query Generator", "Generating SQL query...", Fore.GREEN)

    schema_info = "\n".join([f"Table: {row[0]}, Column: {row[1]}, Type: {row[2]}" for row in schema_chunk])
    config_info = json.dumps(config_chunk, indent=2)
    structure_info = json.dumps(db_structure_chunk, indent=2)

    current_time = datetime.now()
    time_info = f"""
    Current date and time: {current_time}
    Current date: {current_time.date()}
    Current time: {current_time.time()}
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(
            schema_info=schema_info,
            config_info=config_info,
            structure_info=structure_info
        )},
        {"role": "system", "content": f"Current time information:\n{time_info}"},
        {"role": "system", "content": f"Recent chat history:\n{context}"},
        {"role": "system", "content": "You are an SQL query generator. Respond only with the SQL query, without any explanation or additional text."},
        {"role": "user", "content": USER_PROMPT.format(prompt=prompt)}
    ]

    response = client.chat.completions.create(
        model=LLM_CONFIG['model'],
        messages=messages,
        max_tokens=LLM_CONFIG['max_tokens'],
        temperature=LLM_CONFIG['temperature']
    )

    sql_query = response.choices[0].message.content.strip()

    agent_print("Query Generator", "SQL query generated successfully!", Fore.GREEN)
    return sql_query

def refine_sql(combined_query, schema, config, db_structure, context):
    """Refine multiple SQL queries into a single optimized query"""
    agent_print("Query Refiner", "Refining SQL queries...", Fore.BLUE)

    schema_info = "\n".join([f"Table: {row[0]}, Column: {row[1]}, Type: {row[2]}" for row in schema[:100]])
    config_info = json.dumps(dict(list(config.items())[:10]), indent=2)
    structure_info = json.dumps(dict(list(db_structure.items())[:10]), indent=2)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(
            schema_info=schema_info,
            config_info=config_info,
            structure_info=structure_info
        )},
        {"role": "system", "content": f"Recent chat history:\n{context}"},
        {"role": "system", "content": "You are an SQL query optimizer. Your task is to refine multiple SQL queries into a single optimized query. Respond only with the optimized SQL query, without any explanation or additional text."},
        {"role": "user", "content": f"Refine the following SQL queries into a single optimized query:\n{combined_query}"}
    ]

    response = client.chat.completions.create(
        model=LLM_CONFIG['model'],
        messages=messages,
        max_tokens=LLM_CONFIG['max_tokens'],
        temperature=LLM_CONFIG['temperature']
    )

    refined_query = response.choices[0].message.content.strip()

    agent_print("Query Refiner", "SQL queries refined successfully!", Fore.BLUE)
    return refined_query
