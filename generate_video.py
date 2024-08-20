import os
import re
import cv2
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
from zoom import zoom

def generate_video(project_directory, soundtrack):

    # Define the folder containing the images, soundtrack, and the output video file name
    soundtrack_path = os.path.join('soundtracks', soundtrack + '.mp3')
    image_directory_path = os.path.join(project_directory, 'images')
    video_path = os.path.join(project_directory, 'output_video.mp4')
    resized_directory_path = os.path.join(project_directory, 'resized_images')

    # Create resized images directory if it doesn't exist
    if not os.path.exists(resized_directory_path):
        os.makedirs(resized_directory_path)

    # Get a sorted list of image file paths
    image_files = sorted(
        [os.path.join(image_directory_path, f) for f in os.listdir(image_directory_path) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=lambda x: int(re.search(r'_(\d+)\.', x).group(1))
    )

    # Set the duration for each image
    image_duration = 3.2  # Duration set to 2.5 seconds
    fps = 24  # Frames per second

    # Create a list to hold the video clips
    clips = []

    # Iterate over the images and create an ImageClip for each one
    for i, image_file in enumerate(image_files):
        print(f"Processing image {i + 1}/{len(image_files)}...", end="")  # Print status update with \r

        # Load the image
        img = cv2.imread(image_file)
        
        # Convert the image from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize the image to 1080x1080
        img_resized = cv2.resize(img_rgb, (1080, 1080))

        # Create the background image by resizing and applying Gaussian blur
        img_blurred = cv2.GaussianBlur(img_rgb, (25, 25), 0)

        # Resize the blurred image to 1920x1920
        img_blurred_resized = cv2.resize(img_blurred, (1920, 1920))

        # Crop the blurred image to 1080x1920
        x_center = (img_blurred_resized.shape[1] - 1080) // 2
        img_blurred_cropped = img_blurred_resized[:, x_center:x_center + 1080]

        # Save the blurred image to the resized folder (for debugging or future use)
        blurred_image_path = os.path.join(resized_directory_path, f"blurred_{i}.png")
        cv2.imwrite(blurred_image_path, cv2.cvtColor(img_blurred_cropped, cv2.COLOR_RGB2BGR))

        # Create an ImageClip for the blurred background
        background_clip = ImageClip(img_blurred_cropped).set_duration(image_duration).set_fps(fps)

        # Create an ImageClip for the main image
        main_clip = ImageClip(img_resized).set_duration(image_duration).set_fps(fps)

        # Apply smooth zoom effect to the main image
        zoomed_main_clip = zoom(main_clip, mode='in', position='center', speed=1)

        # Combine the background and the zoomed main image
        combined_clip = CompositeVideoClip([background_clip, zoomed_main_clip.set_position("center")])

        # Add the combined clip to the list of clips
        clips.append(combined_clip)
        print("done.")

    # Concatenate all the clips into a single video
    final_clip = concatenate_videoclips(clips, method="compose")

    # Calculate the total duration of the video
    total_duration = len(clips) * image_duration

    # Add audio and loop it to match the video duration if necessary
    audio = AudioFileClip(soundtrack_path)
    if total_duration > audio.duration:
        audio = audio.audio_loop(duration=total_duration)
    else:
        audio = audio.subclip(0, total_duration)

    final_clip = final_clip.set_audio(audio)

    # Write the final video to a file
    final_clip.write_videofile(video_path, fps=fps, codec='libx264', threads=4, preset='ultrafast', audio_codec='aac')
    print(f"\nVideo saved.")

    # Return output video
    return video_path
