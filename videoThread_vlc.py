# -*-coding:utf-8 -*-
"""

Author: Pierre Mermillod
Date: 2024-11-23 17:17:21
License: Valeo // 74 Rue Auguste Perret 94046 Creteil, France

Insert Description

"""
__author__ = "Pierre Mermillod (Valeo)"
__email__ = "pierre.mermillod@valeo.com"
__license__ = "strictly for use of Valeo"
__date__ = "2024-11-23 17:17:21"


import os
import random
import vlc
import time

# Constants for window size and positioning (adjust as needed)
NUM_VIDEOS = 4  # Define how many videos to display
WIDTH = 640    # Width of each video
HEIGHT = 480   # Height of each video

def select_random_file(folder_path, file_extension='.mp4'):
    # List all files in the given folder with the specified extension
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) 
             and f.lower().endswith(file_extension.lower())
             and not f.startswith('.')]
    
    if not files:
        raise ValueError(f"No files with extension {file_extension} found in the folder.")
    
    # Select a random file
    random_file = random.choice(files)
    return os.path.join(folder_path, random_file)


if __name__ == "__main__":

    # folder
    myFolder = r'E:\# Videos B'

    # Create instances and players
    instances = [vlc.Instance() for _ in range(NUM_VIDEOS)]
    players = [instance.media_player_new() for instance in instances]

    # Load media
    media_files = [select_random_file(myFolder) for _ in range(NUM_VIDEOS)]
    medias = [instances[i].media_new(media_files[i]) for i in range(NUM_VIDEOS)]


    for i in range(NUM_VIDEOS):
        
        #print(f"Loading video: {media_files[i]}")  # Confirm the file is loaded
        players[i].set_media(medias[i])

        # players[i].set_media(medias[i].add_option('start-time=10.00'))

        # Set output window properties  (replace with HWNDs if using real windows)
        players[i].video_set_scale(0.5)  # Example: Scales to half size
        x_pos = (i % 2) * WIDTH
        y_pos = (i // 2) * HEIGHT

        # Muting audio (optional)
        if i > 0: # Mute all but the first video. Adjust as needed
            players[i].audio_set_mute(True)

    # Start Playing
    for idN, player in enumerate(players):
        print('play')
        player.play()
        time.sleep(1)  # A small delay to allow the output windows to initialize
        player.set_position(0.5)

        # print('file name {}'.format(media_files[idN]))
        # print('size {}'.format(player.video_get_width()))
        # print('Duration {}'.format(medias[idN].get_duration()))


    # players[0].audio_set_volume(100)

    playing = set([1,2,3,4])
    play = True

    while play:
        time.sleep(0.5)
        state = players[0].get_state()
        if state in playing:
            continue
        else:
            play = False

    # Keep the program running.  Replace with your actual loop/event handling.
    while any(player.is_playing() for player in players):
        time.sleep(20)  # Adjust sleep as needed