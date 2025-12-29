import os
import csv

def create_album_list(music_folder):
    """
    Scans a music directory and creates a text file listing artists and albums.

    The script assumes a folder structure like:
    music_folder/
    ├── Artist_A/
    │   ├── Album_1/
    │   │   ├── song1.mp3
    │   │   └── song2.mp3
    │   └── Album_2/
    │       └── song1.mp3
    └── Artist_B/
        └── Album_3/
            └── song1.mp3

    Args:
        music_folder (str): The absolute path to the main music folder.
        output_file (str): The name of the text file to create.
    """

    element_list = []

    # --- Safety Check ---
    # Ensure the specified music folder exists before proceeding.
    if not os.path.isdir(music_folder):
        print(f"Error: The folder '{music_folder}' does not exist. Please check the path.")
        return

    # --- Main Logic ---
    try:
        # Open the output file in 'write' mode. This will create the file
        # or overwrite it if it already exists.
        print(f"Scanning '{music_folder}'...")
        
        # Get the list of artist folders.
        # os.listdir() returns a list of all files and directories in a path.
        artist_folders = os.listdir(music_folder)
        
        # Sort the list alphabetically for a clean output file.
        artist_folders.sort()

        # Loop through each item in the main music folder.
        for artist_name in artist_folders:
            artist_path = os.path.join(music_folder, artist_name)

            # Check if the item is a directory (i.e., an artist folder).
            if os.path.isdir(artist_path):
                
                # Now, get the list of album folders inside the artist folder.
                album_folders = os.listdir(artist_path)
                album_folders.sort()

                # Loop through each item in the artist folder.
                for album_name in album_folders:
                    album_path = os.path.join(artist_path, album_name)

                    # Check if this item is also a directory (an album folder).
                    if os.path.isdir(album_path):
                        # Write the formatted string to the file.
                        # f.write(f"{artist_name} - {album_name}\n")
                        element_list.append([artist_name, album_name])

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return element_list

def save_results(_myList, _output_file):

    with open(_output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";")
        # writer.writerows(_myList)
        for entry in _myList:
            writer.writerow(entry)

    print(f"Saved to {_output_file}")

if __name__ == "__main__":

    # --- User Configuration ---
    root_music_directory = r'C:\Users\pierr\Music\Musique Pierre HQ' 

    # The name of the output file that will be created in the same
    # directory where you run this script.
    output_filename = os.path.join(root_music_directory,'album_list.csv')

    # --- Run the function ---
    myList = create_album_list(root_music_directory)
    save_results(myList, output_filename)

