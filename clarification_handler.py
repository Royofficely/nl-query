import json
from openai import OpenAI
from colorama import Fore, Style
from utils import agent_print
from config import LLM_CONFIG, OPENAI_API_KEY
from prompts import CLARIFICATION_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_for_clarification(prompt, schema, db_structure):
    agent_print("Clarification", "Asking user for clarification...", Fore.CYAN)

    schema_info = "\n".join([f"Table: {row[0]}, Column: {row[1]}, Type: {row[2]}" for row in schema[:20]])  # Limit to first 20 rows for brevity
    structure_info = json.dumps({k: v for k, v in list(db_structure.items())[:5]}, indent=2)  # Limit to first 5 tables for brevity

    message = CLARIFICATION_PROMPT.format(
        schema_info=schema_info,
        structure_info=structure_info,
        prompt=prompt
    )

    response = client.chat.completions.create(
        model=LLM_CONFIG['model'],
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides clarifications for database queries."},
            {"role": "user", "content": message}
        ],
        max_tokens=300
    )

    clarifications = response.choices[0].message.content.strip()

    print(f"\n{Fore.YELLOW}I'm not sure I understood your query correctly. Here are some possible interpretations:{Style.RESET_ALL}")
    print(clarifications)

    user_choice = input(f"\n{Fore.YELLOW}Please choose the number of the correct interpretation, rephrase your query, or type 'explain' for more details about the database structure: {Style.RESET_ALL}")

    if user_choice.lower() == 'explain':
        print(f"\n{Fore.CYAN}Database Structure:{Style.RESET_ALL}")
        print(structure_info)
        return ask_for_clarification(prompt, schema, db_structure)
    elif user_choice.isdigit() and 1 <= int(user_choice) <= 3:
        clarification_lines = [line for line in clarifications.split('\n') if line.strip()]
        if int(user_choice) <= len(clarification_lines):
            clarification = clarification_lines[int(user_choice) - 1].split('. ', 1)[1] if '. ' in clarification_lines[int(user_choice) - 1] else clarification_lines[int(user_choice) - 1]
        else:
            print(f"{Fore.RED}Invalid choice. Using your input as a new query.{Style.RESET_ALL}")
            clarification = user_choice
    else:
        clarification = user_choice

    return clarification
