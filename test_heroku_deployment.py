# test_heroku_deployment.py
import requests
import uuid
from heroku import generate_and_deploy_web_page
import subprocess
import os

heroku_git_url = "https://git.heroku.com/coder-gpt-tests.git"
repo_url = "https://github.com/sirkant/gpt-test.git"
repo_directory = "temp_repo"
branch_name = str(uuid.uuid4())[:8] + "_prompts"


def test_deployment():
    # Prepare your test data
    html_code = f"<!DOCTYPE html><html><head><title>Test Page</title></head><body><h1>Hello, World! {str(uuid.uuid4())[:8]}</h1></body></html>"
    css_code = "body { background-color: lightblue; } h1 { color: white; text-align: center; }"
    js_code = "console.log('Hello, World!');"

    # Prepare the test branch
    def commit_and_push_to_github(repo_directory, branch_name, html_code, css_code, js_code):
        os.chdir(repo_directory)
        subprocess.run(["git", "checkout", "-b", branch_name])

        with open("index.html", "w") as f:
            f.write(html_code)
        with open("style.css", "w") as f:
            f.write(css_code)
        with open("script.js", "w") as f:
            f.write(js_code)

        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Test deployment on branch {branch_name}"])
        subprocess.run(["git", "push", "origin", branch_name])

    # Call the function with test data
    commit_and_push_to_github(repo_directory, branch_name, html_code, css_code, js_code)
    deployed_url = generate_and_deploy_web_page(repo_url, heroku_git_url, branch_name)
    return deployed_url

if __name__ == "__main__":
    deployed_url = test_deployment()
    if deployed_url is not None:
        print("Deployed URL:", deployed_url)
        response = requests.get(deployed_url)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert "<h1>Hello, World!</h1>" in response.text, "Expected content not found in the deployed web page"

