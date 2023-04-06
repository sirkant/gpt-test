import os
import requests

openai_api_key = os.environ.get("OPENAI_API_KEY")
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


def generate_website_structure(site_title, primary_color, sections):
    # Generate prompts for each part of the website
    html_prompt = f"Create a basic HTML structure with a head and body, including a title {site_title} and a responsive navbar with Bootstrap."
    css_prompt = f"Create a basic CSS structure for a website with primary color {primary_color}."
    js_prompt = "Create a basic JavaScript structure for a website with a responsive navbar using Bootstrap."

    # Generate code for each part
    html_code = generate_code(html_prompt)
    css_code = generate_code(css_prompt)
    js_code = generate_code(js_prompt)

    # Generate code for sections
    section_code = ""
    for title, description in sections:
        section_prompt = f"Create an HTML section with a title '{title}' and a description '{description}'."
        section_code += generate_code(section_prompt)

    # Combine the generated code
    html_code = html_code.replace("<!-- Insert sections here -->", section_code)

    return html_code, css_code, js_code

