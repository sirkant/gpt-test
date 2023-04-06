

def ask_user_questions():
    print("Please answer the following questions to help us create your website:")

    user_name = input("What is your name? ")
    site_title = input("What is the title of your website? ")
    primary_color = input("What is the primary color for your website (e.g., #4CAF50)? ")
    num_sections = int(input("How many sections do you want on your website? "))

    sections = []
    for i in range(num_sections):
        section_title = input(f"What is the title of section {i + 1}? ")
        section_description = input(f"What is the description of section {i + 1}? ")
        sections.append((section_title, section_description))

    return user_name, site_title, primary_color, sections




