import os
from openai import OpenAI
from dotenv import load_dotenv
from create_project_directory import create_project_name, create_project_directory
from generate_video import generate_video
from download_images import download_images
from parse_response import parse_response
from upload_video import upload_video
load_dotenv()

# Input story topic

story_seed = input("Story topic      : ")
num_parts = 17
soundtrack = 'let_her_go'

project_name = create_project_name(story_seed)

project_directory_path = create_project_directory(project_name)

with open(os.path.join(project_directory_path,"story_seed.txt"), "w") as file:
    file.write(story_seed)

text_prompt = f"""
Write a storyboard for a story based on the following topic: {story_seed}.
Format your answer as a numbered list from 0-{num_parts} with periods after each number.
Item 0 will contain both the title and description of the story.
They will be separated by a '/'.
The title will have max 8 words and the description will have max 30 words.
The title will start with: 'Ginger Cat 😻', contain additional emojis, and be extremely simple and easy to understand.
The description will include appropriate hashtags at the end.
The storyboard will have {num_parts} parts, which are written as items 1-{num_parts}.
Each part will have a prompt for an AI image generation.
Make sure that the scenes are written with appropriate pacing so the story lasts 17 frames.
Each prompt will have the three following items in order:
Character(s) and their appearance and clothing,
Scene/location,
Action and emotion to be depicted.
Write the three items with / inbetween so you don't forget.
Do not include any labels such as "Prompt:" before each prompt.
"""

# Set client
client = OpenAI()

# Text Prompt
print("Generating image prompts...",end="")

text_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": text_prompt}]
)

prompt_list_path = os.path.join(project_directory_path,"prompt_list.txt")

with open(prompt_list_path, "w", encoding="utf-8") as file:
    file.write(text_response.choices[0].message.content)
print("done.")
os.startfile(prompt_list_path)

input("Check story. Press 'Enter' to continue or 'ctrl-c' to quit.")

title, description, prompt_list = parse_response(prompt_list_path)

with open("standard_seo.txt",'r') as file:
    description += file.read()

# Write url list
url_list_path = os.path.join(project_directory_path,"url_list.txt")

# Generate the images
with open(url_list_path, "w") as file:
    for i, prompt_text in enumerate(prompt_list):
        print("Generating image "+str(i+1)+f"/{num_parts}...",end="")
        try:
            image_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text +", art style: Pixar 3D Animation",
            size="1024x1024",
            quality="hd",
            style = "vivid",
            n=1
            )
            file.write(image_response.data[0].url + "\n")
            print("done.")
        except:
            print("skipped.")
            continue

# Download images
download_images(project_directory_path)

# Generate movie
video_path = generate_video(project_directory_path,soundtrack)

# Automatically open the first video file
os.startfile(video_path)

with open("standard_seo.txt", "r") as file:
    content = file.read()

# Remove the '#' symbols and split the content into a list of strings
keywords = content.replace("#", "").split()

upload_video(title,description, keywords)