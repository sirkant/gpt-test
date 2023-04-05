import base64
import json
import subprocess
import os
import requests
import openai

openai_api_key = os.environ.get("OPENAI_API_KEY")


def get_user_input():
    user_input = input("Enter your prompt: ")
    return user_input


def generate_code(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 2049,  # Adjust as needed
    }
    response = requests.post("https://api.openai.com/v1/engines/text-davinci-003/completions", headers=headers, json=data)
    print(response.json())
    response_data = response.json()
    generated_code = response_data["choices"][0]["text"].strip()
    return generated_code


def create_github_repo(repo_name):
    github_api_token = os.environ.get("GIT_API_KEY")
    repo_owner = "sirkant"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {github_api_token}",
    }
    data = {
        "name": repo_name,
        "private": False,  # Change to True if you want to create a private repository
    }

    # Check if repository already exists
    repo_response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}", headers=headers)
    if repo_response.status_code == 200:
        print(f"Repository {repo_name} already exists.")
        return repo_response.json()["clone_url"]

    # Create new repository
    response = requests.post(f"https://api.github.com/user/repos", headers=headers, json=data)
    if response.status_code in (200, 201):
        print(f"Repository {repo_name} created successfully.")
        return response.json()["clone_url"]
    elif response.status_code == 422:  # Unprocessable Entity
        error_message = response.json()["errors"][0]["message"]
        if "name already exists" in error_message:
            print(f"Repository {repo_name} already exists.")
            return None
    else:
        print(f"Error creating repository: {response.json()}")
        return None


def determine_file_name(prompt):
    prompt = prompt.lower()

    if "readme" in prompt:
        return "README.md"
    elif "html" in prompt:
        return "index.html"
    elif "python" in prompt:
        return "main.py"
    else:
        return "output.txt"


def commit_to_github(file_name, commit_message, code_content, repo_name, repo_owner="sirkant"):
    github_api_token = os.environ.get("GIT_API_KEY")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {github_api_token}",
    }

    # Check if file exists
    file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name}"
    file_response = requests.get(file_url, headers=headers)
    file_exists = file_response.status_code == 200

    # Commit to GitHub
    commit_data = {
        "message": commit_message,
        "content": base64.b64encode(code_content.encode("utf-8")).decode("utf-8"),
    }

    if file_exists:
        commit_data["sha"] = file_response.json()["sha"]

    commit_response = requests.put(file_url, headers=headers, json=commit_data)

    if commit_response.status_code in (200, 201):
        print(f"Code committed successfully to {file_name}")
    else:
        print(f"Error committing code: {commit_response.json()}")



def deploy_to_heroku(app_name, repo_url):
    heroku_api_key = os.environ.get("HEROKU_API_KEY")
    os.environ["HEROKU_API_KEY"] = heroku_api_key

    # Check if the app already exists
    apps_list = json.loads(subprocess.check_output(["heroku", "apps", "--json"]).decode("utf-8"))

    app_exists = False
    for app in apps_list:
        if app["name"] == app_name:
            app_exists = True
            break

    # Create a new Heroku app if it doesn't exist
    if not app_exists:
        subprocess.run(["heroku", "create", app_name])

    # Set the buildpack
    subprocess.run(["heroku", "buildpacks:set", "heroku/python", "--app", app_name])

    # Push the code to Heroku
    push_result = subprocess.run(["git", "push", f"heroku+{repo_url}", "HEAD:master"])

    if push_result.returncode == 0:
        print("Deployment successful!")
    else:
        print("Deployment failed.")

    # Open the deployed app in the browser
    subprocess.run(["heroku", "open", "--app", app_name])




# Get user input
prompt = get_user_input()

# Generate code using OpenAI API
generated_code = generate_code(prompt)

# Create a new repository on GitHub
repo_name = "gpt-test"
repo_url = create_github_repo(repo_name)
if not repo_url:
    print("Failed to create GitHub repository.")
    exit(1)

# Commit the code to GitHub
file_name = "index.html"  # Replace with desired file name
commit_message = "Generated code from prompt"
commit_to_github(file_name, commit_message, generated_code, repo_name=repo_name)

# Deploy the code to Heroku
app_name = "coder-gpt-tests" # Replace with desired Heroku app name
deploy_to_heroku(app_name, repo_url)

#Accept subsequent prompts and update the code in the repository
while True:
    new_prompt = input("Enter your next prompt or type 'exit' to quit: ")
    if new_prompt.lower() == "exit":
        break
    updated_code = generate_code(new_prompt)

    # Determine the updated file name based on the new prompt
    updated_file_name = determine_file_name(new_prompt)
    commit_message = "Updated code from prompt"
    commit_to_github(updated_file_name, commit_message, updated_code, repo_name=repo_name, repo_owner="sirkant")
