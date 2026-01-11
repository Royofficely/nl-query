import json
import re
import pandas as pd
from colorama import Fore, Style
from openai import OpenAI
from utils import agent_print, chunk_data
from db_connector import get_db_schema, get_db_structure
from query_optimizer import optimize_query
from sql_generator import generate_sql, refine_sql
from query_executor import execute_query
from clarification_handler import ask_for_clarification
from chat_history_manager import ChatHistoryManager
from config import LLM_CONFIG, OPENAI_API_KEY
from prompts import REFINE_PROMPT, SHORT_QUERY_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)
chat_history = ChatHistoryManager()

def extract_sql_query(text):
    # Remove markdown code block syntax
    text = re.sub(r'```sql\s*', '', text)
    text = re.sub(r'\s*```', '', text)

    # Try to extract SQL query from the text
    match = re.search(r'\s*(SELECT[\s\S]*?;)\s*$', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()  # Return original text if no SQL found, but stripped

def process_natural_language_query(prompt, schema, config, db_structure):
    chat_history.add_message("user", prompt)

    if len(prompt.split()) <= 3:
        return handle_short_query(prompt, schema, config, db_structure)

    context = chat_history.get_context()

    optimized_prompt = optimize_query(prompt, schema, db_structure, context)

    schema_chunks = chunk_data(schema)
    config_chunks = chunk_data(list(config.items()))
    db_structure_chunks = chunk_data(list(db_structure.items()))

    sql_queries = []
    for schema_chunk, config_chunk, db_structure_chunk in zip(schema_chunks, config_chunks, db_structure_chunks):
        config_chunk = dict(config_chunk)
        db_structure_chunk = dict(db_structure_chunk)
        sql_query = generate_sql(optimized_prompt, schema_chunk, config_chunk, db_structure_chunk, context)
        sql_queries.append(sql_query)

    if len(sql_queries) > 1:
        combined_query = "\n".join(sql_queries)
        final_query = refine_sql(combined_query, schema[:100], dict(list(config.items())[:10]), dict(list(db_structure.items())[:10]), context)
    else:
        final_query = sql_queries[0]

    # Extract and clean SQL query
    final_query = extract_sql_query(final_query)

    agent_print("Orchestrator", f"Generated SQL Query: {final_query}", Fore.WHITE)

    try:
        result = execute_query(final_query)
        if isinstance(result, str) and "error" in result.lower():
            agent_print("Error Handler", "Error executing query. Initiating clarification process.", Fore.RED)
            clarification = ask_for_clarification(prompt, schema, db_structure)
            return process_natural_language_query(clarification, schema, config, db_structure)

        if isinstance(result, pd.DataFrame) and result.empty:
            agent_print("Result Handler", "The query returned no results. Initiating clarification process.", Fore.YELLOW)
            clarification = ask_for_clarification(prompt, schema, db_structure)
            return process_natural_language_query(clarification, schema, config, db_structure)

        chat_history.add_message("assistant", f"SQL Query: {final_query}\nResult: {str(result)}")
        return result
    except Exception as e:
        agent_print("Error Handler", f"An error occurred: {str(e)}", Fore.RED)
        clarification = ask_for_clarification(prompt, schema, db_structure)
        return process_natural_language_query(clarification, schema, config, db_structure)

def handle_short_query(prompt, schema, config, db_structure):
    agent_print("Short Query Handler", "Handling short query...", Fore.CYAN)

    message = SHORT_QUERY_PROMPT.format(
        prompt=prompt,
        db_structure=json.dumps(db_structure, indent=2)
    )

    response = client.chat.completions.create(
        model=LLM_CONFIG['model'],
        messages=[
            {"role": "system", "content": "You are a helpful assistant that interprets short database queries."},
            {"role": "user", "content": message}
        ],
        max_tokens=300
    )

    interpretations = response.choices[0].message.content.strip()

    print(f"\n{Fore.YELLOW}Your query was quite short. Here are some possible interpretations:{Style.RESET_ALL}")
    print(interpretations)

    user_choice = input(f"\n{Fore.YELLOW}Please choose the number of the correct interpretation, or rephrase your query: {Style.RESET_ALL}")

    if user_choice.isdigit() and 1 <= int(user_choice) <= 3:
        interpretation_lines = [line for line in interpretations.split('\n') if line.strip()]
        if int(user_choice) <= len(interpretation_lines):
            chosen_query = interpretation_lines[int(user_choice) - 1].split('. ', 1)[1] if '. ' in interpretation_lines[int(user_choice) - 1] else interpretation_lines[int(user_choice) - 1]
            return execute_query(chosen_query)

    # If the user rephrased the query or made an invalid choice, process the new query
    return process_natural_language_query(user_choice, schema, config, db_structure)
