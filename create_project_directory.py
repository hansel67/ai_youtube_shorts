import os

def create_project_name(story_seed):
    # Remove non-alphanumeric characters except spaces and convert to lowercase
    cleaned = ''.join(char.lower() if char.isalnum() or char.isspace() else '' for char in story_seed)
    
    # Split the string into words
    words = cleaned.split()
    
    # Take the first four words
    first_four_words = words[:4]
    
    # Join the first four words with underscores
    result = '_'.join(first_four_words)
    
    return result

def create_project_directory(project_name):

    # Make projects folder if it doesn't already exist
    if not(os.path.exists("projects")):
        os.makedirs("projects")

    # Define the path where you want to create the new directory
    directory_path = os.path.join(os.getcwd(), "projects", project_name)
    
    # If the directory already exists, append a number to the name
    count = 1
    while os.path.exists(directory_path):
        new_project_name = f"{project_name}_{count}"
        directory_path = os.path.join(os.getcwd(), "projects",new_project_name)
        count += 1
    
    # Create the directory
    os.makedirs(directory_path)

    # Create images folders
    os.makedirs(os.path.join(directory_path,f"images"))
    
    print(f"Project directory created.")

    return directory_path