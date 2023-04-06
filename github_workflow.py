import base64
import git
import os
import requests
import uuid
import shutil
from urllib.parse import urlparse
from git.exc import GitCommandError


# create_github_repo
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

# determine_file_name
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

# commit_to_github
def commit_to_github(file_name, commit_message, code_content, repo_name, branch, repo_owner="sirkant"):
    github_api_token = os.environ.get("GIT_API_KEY")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {github_api_token}",
    }

    # Get the default branch's ref
    default_branch_response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}", headers=headers)
    default_branch = default_branch_response.json()["default_branch"]
    default_branch_ref = f"heads/{default_branch}"

    # Check if the new branch exists
    new_branch_ref = f"heads/{branch_name}"
    branch_response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/{new_branch_ref}", headers=headers)
    branch_exists = branch_response.status_code == 200

    # Create the new branch if it doesn't exist
    if not branch_exists:
        default_branch_sha = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/{default_branch_ref}", headers=headers).json()["object"]["sha"]
        new_branch_data = {
            "ref": f"refs/{new_branch_ref}",
            "sha": default_branch_sha,
        }
        requests.post(f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs", headers=headers, json=new_branch_data)

    # Check if file exists
    file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name}?ref={branch_name}"
    file_response = requests.get(file_url, headers=headers)
    file_exists = file_response.status_code == 200

    # Commit to GitHub
    commit_data = {
        "message": commit_message,
        "content": base64.b64encode(code_content.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }

    if file_exists:
        commit_data["sha"] = file_response.json()["sha"]

    commit_response = requests.put(file_url, headers=headers, json=commit_data)

    if commit_response.status_code in (200, 201):
        print(f"Code committed successfully to {file_name} on branch {branch_name}")
    else:
        print(f"Error committing code: {commit_response.json()}")

# create_and_checkout_branch
def create_and_checkout_branch(repo, branch_name):
    # Check if the branch already exists
    branch_exists = any([branch.name == branch_name for branch in repo.branches])

    if not branch_exists:
            # Create the new branch
            repo.git.checkout("-b", branch_name)

            print(repo.git.status())
    else:
            # Checkout the existing branch
            repo.git.checkout(branch_name)
            print(repo.git.status())


# create_static_json_file
def create_static_json_file():
    return '{"root": "public/", "routes": {"/**": "index.html"}}'


def clone_repo(repo_url, repo_directory):
    if os.path.exists(repo_directory):
        shutil.rmtree(repo_directory)

    repo = git.Repo.clone_from(repo_url, repo_directory)
    return repo


def commit_files(repo, file_data):
    for file_name, commit_message, code_content in file_data:
        with open(os.path.join(repo.working_tree_dir, file_name), "w") as f:
            f.write(code_content)
        repo.git.add(file_name)
        if repo.is_dirty():
            repo.git.commit("-m", commit_message)
        else:
            print(f"No changes to commit for {file_name}")


def push_changes(repo, repo_url, branch_name):
    github_api_key = os.environ.get("GIT_API_KEY")
    parsed_url = urlparse(repo_url)
    modified_url = parsed_url._replace(netloc=f"{github_api_key}@{parsed_url.netloc}").geturl()

    repo.git.checkout(branch_name)
    repo.git.add(".")

    try:
        repo.git.commit("-m", f"Commit message for branch {branch_name}")
    except GitCommandError:
        print(f"No changes to commit in branch {branch_name}")

    repo.git.fetch(modified_url, "master")

    try:
        repo.git.merge("FETCH_HEAD", "--allow-unrelated-histories")
    except GitCommandError as e:
        if "Merge conflict" in str(e):
            print("Resolving merge conflict by keeping local changes...")
            # Replace this part with a loop to resolve conflicts for each file in file_data
            # Resolve conflict for index.html
            repo.git.checkout("--ours", "index.html")
            repo.git.add("index.html")

            # Resolve conflict for styles.css
            repo.git.checkout("--ours", "styles.css")
            repo.git.add("styles.css")

            # Resolve conflict for scripts.js
            repo.git.checkout("--ours", "scripts.js")
            repo.git.add("scripts.js")

            # Resolve conflict for static.json
            repo.git.checkout("--ours", "static.json")
            repo.git.add("static.json")

            print("Git status after resolving conflicts:")
            print(repo.git.status())

            # Commit the merge
            repo.git.commit("-m", f"Merging master into {branch_name}")

    print("Git status after resolving conflicts:")
    print(repo.git.status())

    origin = repo.remote("origin")
    origin_url = origin.set_url(modified_url)
    repo.git.push("--set-upstream", origin_url, branch_name)

    print(f"Local branches:")
    for local_branch in repo.branches:
        print(f"  {local_branch.name}")

    print("Remote branches:")
    for remote_branch in repo.remote().refs:
        print(f"  {remote_branch.name}")

    print(f"Current branch: {repo.active_branch}")


# Example usage
if __name__ == "__main__":
    repo_url = "https://github.com/sirkant/gpt-test.git"
    repo_directory = "temp_repo"
    branch_name = str(uuid.uuid4())[:8] + "_prompts"

    # Clone the repository and create the new branch
    repo = clone_repo(repo_url, repo_directory)
    create_and_checkout_branch(repo, branch_name)

    # Define the file data you want to commit
    file_data = [
        ("index.html", "Generated HTML code", "<html>...</html>"),
        ("styles.css", "Generated CSS code", "body { ... }"),
        ("scripts.js", "Generated JavaScript code", "console.log('Hello, World!');"),
    ]

    # Commit the files to the local repository
    commit_files(repo, file_data)

    # Add the static.json file to the repository
    with open(os.path.join(repo.working_tree_dir, "static.json"), "w") as f:
        f.write(create_static_json_file())
    repo.git.add("static.json")
    if repo.is_dirty():
        repo.git.commit("-m", "Added static.json for Heroku static buildpack")
    else:
        print("No changes to commit for static.json")

    # Push the changes to the remote repository
    push_changes(repo, repo_url, branch_name)
