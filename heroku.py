import subprocess
import os
import json

def deploy_to_heroku(app_name, repo_url, branch):
    heroku_api_key = os.environ.get("HEROKU_API_KEY")
    github_api_token = os.environ.get("GIT_API_KEY")
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

    # Check if the Heroku remote already exists
    remotes_output = subprocess.check_output(["git", "remote"]).decode("utf-8")
    if "heroku" not in remotes_output:
        subprocess.run(["git", "remote", "add", "heroku", repo_url])

    # Push the code to Heroku
    heroku_git_url = repo_url.replace("https://", f"https://{github_api_token}@", 1)

    push_command = ["git", "push", "--set-upstream", heroku_git_url, f"{branch}:main"]
    push_process = subprocess.Popen(push_command, stdin=subprocess.PIPE, universal_newlines=True)
    push_process.communicate(f"{github_api_token}\n")

    if push_process.returncode == 0:
        print("Deployment successful!")
        app_url = get_app_url(app_name)
        return app_url
    else:
        print("Deployment failed.")
        return None

    # Open the deployed app in the browser
    subprocess.run(["heroku", "open", "--app", app_name])

def get_app_url(app_name):
    print(f"https://{app_name}.herokuapp.com/")
    return f"https://{app_name}.herokuapp.com/"




def generate_and_deploy_web_page(repo_url, heroku_git_url, branch_name):
    app_name = "coder-gpt-tests"  # Replace with desired Heroku app name
    subprocess.run(["heroku", "git:remote", "-a", app_name])
    subprocess.run(["heroku", "config:set", f"MY_APP_NAME={app_name}"])
    subprocess.run(["heroku", "config:set", f"MY_GIT_URL={heroku_git_url}"])
    subprocess.run(["heroku", "config:set", f"MY_BRANCH={branch_name}"])
    deploy_to_heroku(app_name, repo_url, branch_name)


