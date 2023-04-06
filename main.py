
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")

from user_input import ask_user_questions, generate_test_output
from openai_code_generation import generate_website_structure, generate_code
from github_workflow import create_github_repo, commit_to_github, determine_file_name
from heroku import deploy_to_heroku
from config_builder import create_static_json_file


def main():
    user_name, site_title, primary_color, sections = generate_test_output()
    html_code, css_code, js_code = generate_website_structure(site_title, primary_color, sections)


# Gather user input
if __name__ == "__main__":
    user_name, site_title, primary_color, sections = ask_user_questions()

    # Generate website structure
    html_code, css_code, js_code = generate_website_structure(site_title, primary_color, sections)


# Accept subsequent prompts and update the code in the repository
if __name__ == "__main__":
    while True:
        new_prompt = input("Enter your next prompt or type 'exit' to quit: ")
        if new_prompt.lower() == "exit":
            break
        updated_code = generate_code(new_prompt)

        # Determine the updated file name based on the new prompt
        updated_file_name = determine_file_name(new_prompt)
        commit_message = "Updated code from prompt"
        commit_to_github(updated_file_name, commit_message, updated_code, repo_name=repo_name, repo_owner="sirkant")