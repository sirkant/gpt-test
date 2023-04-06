import os
import github_workflow
import uuid

openai_api_key = os.environ.get("OPENAI_API_KEY")
repo_owner = "sirkant"
repo_url = "https://github.com/sirkant/gpt-test.git"
repo_directory = "temp_repo"
branch_name = "test" + str(uuid.uuid4())[:8] + "_prompts"

from github_workflow import commit_files, push_changes, create_static_json_file, create_and_checkout_branch, clone_repo
from config_builder import create_static_json_file
from heroku import deploy_to_heroku

def generate_test_output():
    user_name = "test user"
    html_code = "your HTML code"
    css_code = "your CSS code"
    js_code = "your JavaScript code"
    return user_name, html_code, css_code, js_code


def generate_test_structure(site_title, primary_color, sections):
    # Generate code for each part
    html_code = '<!DOCTYPE html> <html lang="en"> <head>\n  <title>My Site Title</title>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">\n</head>\n<body>\n  <!-- Create a navigation menu -->\n  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">\n    <a class="navbar-brand" href="#">Logo</a>\n    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">\n      <span class="navbar-toggler-icon"></span>\n    </button>\n\n    <div class="collapse navbar-collapse" id="navbarSupportedContent">\n      <ul class="navbar-nav mr-auto">\n        <li class="nav-item active">\n          <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>\n        </li>\n        <li class="nav-item">\n          <a class="nav-link" href="#">About</a>\n        </li>\n        <li class="nav-item">\n          <a class="nav-link" href="#">Contacts</a>\n        </li>\n      </ul>\n    </div>\n  </nav>\n  \n  <!-- Container to add content to the page -->\n  <div class="container">\n\n  </div>\n\n  <!-- Import jquery, popper and bootstrap scripts -->\n  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>\n  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>\n  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>\n\n</body>\n</html>'
    css_code = 'body { background-color: lightblue; } h1 { color: white; text-align: center; }'
    js_code = 'console.log(Hello, World!)'

    return html_code, css_code, js_code

def test():

    # Begins the test run
    user_name, site_title, primary_color, sections = generate_test_output()

    # Generate website structure
    html_code, css_code, js_code = generate_test_structure(site_title, primary_color, sections)


    # Commits
    repo = clone_repo(repo_url, repo_directory)
    create_and_checkout_branch(repo, branch_name)

    file_data = [
        ("index.html", "Generated HTML code", "<html>...</html>"),
        ("styles.css", "Generated CSS code", "body { ... }"),
        ("scripts.js", "Generated JavaScript code", "console.log('Hello, World!');"),
    ]

    commit_files(repo, file_data)

    with open(os.path.join(repo.working_tree_dir, "static.json"), "w") as f:
        f.write(create_static_json_file())
    repo.git.add("static.json")
    if repo.is_dirty():
        repo.git.commit("-m", "Added static.json for Heroku static buildpack")
    else:
        print("No changes to commit for static.json")

    push_changes(repo, repo_url, branch_name)
    print("Successful push to Github")

    # Deploys

test()

