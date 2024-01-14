import os
import random
import tkinter as tk
import webbrowser
import customtkinter as ctk
import json
import pygame

from tkinter import filedialog as fd
from listbox.CTkListbox import *
from messagebox.CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from SUT_error import check_empty_file, extract_directory_path, extract_file_name
from IHL.hover import Hover

img = None
is_playing = True
existing_songs = []
directory = ""
selected_song = ""
last_played_song = ""
current_position = 0
new = 1
url = "https://github.com/Rexlep"

data = {
    'folder_path': '',
    'songs': []
}


def save_data():
    """
    Save the song's in folder in json file
    """
    songs = [listbox.get(idx) for idx in range(listbox.size())]
    songs = [song for song in songs if song is not None]
    data['songs'] = songs
    with open("data/data.json", "w") as file:
        json.dump(data, file)


def save_data_one_song():
    """
    This function use to write one song in JSON file
    """
    with open("data/data.json", "w") as file:
        json.dump(data, file)


def load_data():
    """
    Read datas in JSON file and return the songs that saved in json file
    """
    global data, directory, existing_songs
    try:
        with open("data/data.json", "r") as file:
            data = json.load(file)
            data.get('folder_path', '')
            songs = data.get('songs', [])
            existing_songs = songs
            for song in songs:
                listbox.insert(tk.END, song)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle case when the file doesn't exist or is empty
        pass


def check_the_format(filename):
    """
    This function checks the format of song
    """
    for song in filename:
        file_path = os.path.join(directory, song)
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.aiff', '.alac']:
            return True
        return False


def select_folder():
    """
    Return's the song in the folder that you select insert song in listbox
    """
    global directory

    try:
        # Ask directory from user
        directory = fd.askdirectory(title="Select folder song", initialdir='/')
        # Get the name if files in folder
        file_name = os.listdir(directory)

        # Check if empty file function is not true shows an error
        if not check_empty_file(file_name, directory):
            CTkMessagebox(title="Error", message="Your folder is empty", icon="cancel", fade_in_duration=0.2,
                          button_color='#696969', button_hover_color='#707070')
            return

        # Check if not selecting directory show warning with try option
        if not directory or not file_name:
            msg = CTkMessagebox(title="Warning", message="Please select a folder to continue", icon="warning",
                                fade_in_duration=0.2, button_color='#696969', button_hover_color='#707070',
                                option_1="Retry", option_2="Cancel")
            if msg.get() == "Retry":
                select_folder()

                # Check the format of files in the folder if it not song formats show an error with try option
        if not check_the_format(file_name):
            msg = CTkMessagebox(title="Error", message="Please select a valid song folder", icon="cancel",
                                fade_in_duration=0.2, button_color='#696969', button_hover_color='#707070',
                                option_1="Retry", option_2="Cancel")
            if msg.get() == "Retry":
                select_folder()
        # Check the songs in a variable list, and if there is a repetitious song, it will not add
        new_songs = [song for song in file_name if song not in existing_songs]
        data['folder_path'] = directory

        # Make a loop around all songs and new songs if the len be more than 60
        # its write 55 parts of name and put (...) for the next of it
        for song in new_songs:
            truncated_song = (song[:55] + '...') if len(song) > 60 else song
            listbox.insert(ctk.END, truncated_song)

        # Delete the repetitious song form list
        existing_songs.extend(new_songs)
        # Calling save data function to save the infos into json file
        save_data()
    except FileNotFoundError:
        CTkMessagebox(title="Error", message="Empty path", icon="cancel", fade_in_duration=0.2, button_color='#696969',
                      button_hover_color='#707070')


def add_one_song():
    """
    Add a single song to the listbox
    """
    global existing_songs, directory

    try:
        # Ask of r selecting song
        directory = fd.askopenfilename(title="Select songs you want")

        # Extract the file path for json file
        path = extract_directory_path(directory)
        song_name = extract_file_name(directory)

        # Check is any song did not select show an error
        if not directory:
            msg = CTkMessagebox(title="Warning", message="Please select song to continue", icon="warning",
                                fade_in_duration=0.2, button_color='#696969', button_hover_color='#707070',
                                option_1="Retry", option_2="Cancel")
            if msg.get() == "Retry":
                add_one_song()
            return

        # Write the path of folder in json
        data['folder_path'] = path
        # Get the existing songs list or create an empty list if it doesn't exist
        songs = data.get('songs')
        # Add the new song_name to the song list
        songs.append(song_name)
        # Update the 'songs' key in the data dictionary
        data['songs'] = songs

        # Add the new song_name to the existing songs list
        existing_songs.append(song_name)

        new_songs = [song for song in song_name if song not in existing_songs]

        # Delete the repetitious song form list
        existing_songs.extend(new_songs)

        # Insert the new song into the listbox
        listbox.insert(ctk.END, new_songs)

        # Calling save_data function to save the information into the JSON file
        save_data_one_song()

    except FileNotFoundError:
        CTkMessagebox(title="Error", message="Empty path", icon="cancel", fade_in_duration=0.2, button_color='#696969',
                      button_hover_color='#707070')


def remove_songs():
    """
    Remove songs from the listbox and JSON file
    """
    global data
    # Check if directory is empty show error
    file_path = data["folder_path"]
    song_name = data["songs"]
    if file_path == "" and song_name == "":
        CTkMessagebox(title="Error", message="Select song first", icon="cancel", fade_in_duration=0.2,
                      button_color='#696969', button_hover_color='#707070')
    # And when dir is not empty, let you delete songs
    else:
        CTkMessagebox(title="Info", message="Deleted!", icon="info", fade_in_duration=0.2,
                      button_color='#696969', button_hover_color='#707070')
        try:
            # Delete listbox items
            listbox.delete(0, ctk.END)
            # Load the json file to access to data in file
            file_data = json.load(open("data/data.json", "r"))
            # Set "" for folder path variable
            file_data["folder_path"] = ""
            # Set an empty list for songs when this two-parameter set file is empty
            file_data["songs"] = []
            json.dump(file_data, open("data/data.json", "w"), indent=4)
        except FileNotFoundError:
            CTkMessagebox(title="Error", message="Empty path", icon="cancel", fade_in_duration=0.2,
                          button_color='#696969', button_hover_color='#707070')


def fade_effect():
    """
    This function adds a fade-out effect when a song gets change
    """
    if pygame.mixer.music.get_busy():
        # Stop the currently playing song
        pygame.mixer.music.fadeout(200)  # Fade out the song over 1 second

        # Wait for the fade-out effect to complete before loading and playing the next song
        pygame.time.wait(200)


def get_song_length_and_remaining_time(full_song_path):
    import pygame.mixer

    # Get the duration of the selected song
    sound = pygame.mixer.Sound(full_song_path)
    song_length = sound.get_length() * 1000

    # Calculate the remaining time
    remaining_time = song_length
    remaining_minutes = int(remaining_time // 60000)
    remaining_seconds = int((remaining_time % 60000) // 1000)

    # Convert the duration to minutes and seconds
    minutes = int(song_length // 60000)
    seconds = int((song_length % 60000) // 1000)

    # Format minutes and seconds with leading zeros if necessary
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)
    remaining_minutes_str = str(remaining_minutes).zfill(2)
    remaining_seconds_str = str(remaining_seconds).zfill(2)

    # Update position label with current time and remaining time
    position_label.configure(text=f"{minutes_str}:{seconds_str} / Time")


def file_folder_error():
    """
    File or folder path error
    """
    msg = CTkMessagebox(title="Warning", message="Please select folder or file first", icon="warning",
                        fade_in_duration=0.2, button_color='#696969', button_hover_color='#707070',
                        option_3="Folder", option_2="File", option_1="Cancel")
    if msg.get() == "Folder":
        select_folder()
    if msg.get() == "File":
        add_one_song()


def play_selected_song(song):
    """
    Play the selected song
    """
    global data
    song_path = os.path.join(data["folder_path"], song)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()


def play_random_song():
    """
    This function play a random song if you tap play button
    """
    global data, selected_song
    if data["folder_path"] == "":
        CTkMessagebox(title="Error", message="Your path", icon="cancel", fade_in_duration=0.2,
                      button_color='#696969', button_hover_color='#707070')
        return
    else:
        # Initialize pygame.mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Select a random song from the existing songs list
        selected_song = random.choice(existing_songs)

        # Highlight the selected random song in the listbox
        listbox.select_item(selected_song)

        # Play the selected random song
        play_selected_song(selected_song)


def play_song(option):
    """
    Play selected song in listbox
    """
    global data, last_played_song, is_playing, current_position, selected_song

    file_path = data["folder_path"]

    try:
        if file_path != "":
            if option in existing_songs:
                full_song_path = os.path.join(file_path, option)  # Use the full file path

                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                # Check if selected song is already playing
                if selected_song == option:
                    # If already playing, pause the song
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                        state_label.configure(text="State: Pause  ")
                        play_button.configure(image=play_image)  # Change play button image to 'play' icon
                    else:
                        pygame.mixer.music.unpause()
                        state_label.configure(text="State: Play  ")
                        play_button.configure(image=pause_image)  # Change play button image to 'pause' icon
                    return

                fade_effect()

                if last_played_song != selected_song:
                    # Update the position bar and position label
                    song_length = pygame.mixer.Sound(full_song_path).get_length()

                    # Clear the current selection in the listbox
                    listbox.selection_clear()

                    # Find the index of the selected song in the listbox
                    selected_song_index = existing_songs.index(selected_song)

                    # Highlight the selected song in the listbox
                    listbox.selection_set(selected_song_index)

                    last_played_song = selected_song

                pygame.mixer.music.load(full_song_path)
                pygame.mixer.music.play()
                get_song_length_and_remaining_time(full_song_path)

                # Update the selected song variable
                selected_song = option

                truncated_song = option[:40] + '...' if len(option) > 30 else option
                # Showing song name on song name label
                song_name_label.configure(text=f"Now playing: {truncated_song}")

                # Change play button image to 'pause' icon
                play_button.configure(image=pause_image)

                # Clear the current selection in the listbox
                listbox.selection_clear()

                # Find the index of the selected song in the listbox
                selected_song_index = existing_songs.index(selected_song)

                # Highlight the selected song in the listbox
                listbox.selection_set(selected_song_index)
            else:
                play_random_song()
        else:
            file_folder_error()
    except pygame.error:
        CTkMessagebox(title="Error", message="File not founded in directory", icon="cancel", fade_in_duration=0.2,
                      button_color='#696969', button_hover_color='#707070')


def play_pause_with_space(event):
    """Play or pause the song with the space key"""
    if event.keysym == 'space':
        play_song(lambda: play_song(listbox.get_selected_song()))


def play_next_song():
    """Play the next song in the list"""
    global data, selected_song, existing_songs

    file_path = data["folder_path"]

    if file_path == "":
        msg = CTkMessagebox(title="Warning", message="Please select folder or file first", icon="warning",
                            fade_in_duration=0.2, button_color='#696969', button_hover_color='#707070',
                            option_3="Folder", option_2="File", option_1="Cancel")
        if msg.get() == "Folder":
            select_folder()
        if msg.get() == "File":
            add_one_song()

    else:
        # Get the index of the currently selected song
        current_index = existing_songs.index(selected_song)

        # Calculate the index of the next song
        next_index = (current_index + 1) % len(existing_songs)

        # Get the next song from the existing songs list
        next_song = existing_songs[next_index]

        # Highlight the next song in the listbox
        listbox.select_item(next_song)

        # Play the selected next song
        play_selected_song(next_song)


def play_next_song_with_button(event):
    """Return's the next song with right arrow"""
    if event.keysym == 'Right':
        play_next_song()


def play_last_song():
    """Play the previous song in the list"""
    global data, selected_song, existing_songs

    file_path = data["folder_path"]

    if file_path == "":
        msg = CTkMessagebox(title="Warning", message="Please select folder or file first", icon="warning",
                            fade_in_duration=0.2, button_color='#696969', button_hover_color='#707070',
                            option_3="Folder", option_2="File", option_1="Cancel")
        if msg.get() == "Folder":
            select_folder()
        if msg.get() == "File":
            add_one_song()

    else:
        # Get the index of the currently selected song
        current_index = existing_songs.index(selected_song)

        # Calculate the index of the next song
        next_index = (current_index - 1) % len(existing_songs)

        # Get the next song from the existing songs list
        next_song = existing_songs[next_index]

        # Highlight the next song in the listbox
        listbox.select_item(next_song)

        # Play the selected next song
        play_selected_song(next_song)


def play_last_song_with_button(event):
    """Return's the last song with left arrow"""
    if event.keysym == 'Left':
        play_last_song()


def split_label(frame, repeat, anchor, side=None):
    """This function adds a line for split widgets"""
    label = ctk.CTkLabel(frame, text='-' * repeat)
    label.pack(anchor=anchor, side=side, padx=10)


def split_label_stand_line(frame):
    """This function adds a | for split widgets"""
    label = ctk.CTkLabel(frame, text='|')
    label.pack(side=tk.LEFT, padx=10)


def info():
    """
    This function shows the info of creator
    """
    CTkMessagebox(title="Info", message="SUT-Music player\nAuthor: REXLEP\nv0.0.3", fade_in_duration=0.2)


def openweb():
    """
    This function open the creator GitHub page
    """
    webbrowser.open(url, new=new)


def update_volume(value):
    """
    This function can use it for slider and sound controlling
    """
    if existing_songs:
        pygame.init()
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)
    else:
        CTkMessagebox(title="Error", message="No songs available", icon="cancel")


# ________________________________________________UI________________________________________________

select_form = ctk.CTk()
select_form.config(background='#252525')
select_form.title('SUT')

icon_path = ImageTk.PhotoImage(file=(os.path.join("R.ico")))
select_form.wm_iconbitmap()
select_form.iconphoto(False, icon_path)

window_width = 1320
window_height = 630

screen_width = select_form.winfo_screenwidth()
screen_height = select_form.winfo_screenheight()

x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

select_form.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

frame_top = ctk.CTkFrame(select_form, corner_radius=20)
frame_top.pack(padx=10, pady=10, ipadx=0, ipady=0, anchor=ctk.W)

frame_song_label = ctk.CTkFrame(frame_top, corner_radius=10)
frame_song_label.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=(10, 10))

frame_right = ctk.CTkFrame(select_form, corner_radius=20)
frame_right.place(anchor='ne', relx=1, x=-10, y=10)

frame_list_box = ctk.CTkFrame(frame_right, corner_radius=10)
frame_list_box.pack(padx=10, pady=10)

frame_file_buttons = ctk.CTkFrame(frame_right, corner_radius=10)
frame_file_buttons.pack(side=tk.BOTTOM, pady=10)

frame_left = ctk.CTkFrame(frame_top, corner_radius=10)
frame_left.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=10, pady=10)

frame_buttons = ctk.CTkFrame(frame_left, corner_radius=10)
frame_buttons.pack(side=ctk.BOTTOM, padx=10, pady=30)

# ________________________________________________images________________________________________________

folder_image = ctk.CTkImage(light_image=Image.open("icons/folder.png"), size=(30, 30))
song_image = ctk.CTkImage(light_image=Image.open("icons/song.png"), size=(30, 30))
remove_image = ctk.CTkImage(light_image=Image.open("icons/remove.png"), size=(30, 30))
play_image = ctk.CTkImage(light_image=Image.open("icons/play.png"), size=(30, 30))
pause_image = ctk.CTkImage(light_image=Image.open("icons/pause.png"), size=(30, 30))
next_image = ctk.CTkImage(light_image=Image.open("icons/next.png"), size=(30, 30))
last_image = ctk.CTkImage(light_image=Image.open("icons/last.png"), size=(30, 30))
info_image = ctk.CTkImage(light_image=Image.open("icons/info.png"), size=(30, 30))
git_image = ctk.CTkImage(light_image=Image.open("icons/github.png"), size=(30, 30))

# ________________________________________________Widgets________________________________________________

split_label(frame_song_label, 138, anchor='nw')

song_name_label = ctk.CTkLabel(frame_song_label, text='Now playing: ', font=("fonts/MonoLisa-Bold.ttf", 15))
song_name_label.pack(anchor=tk.W, padx=12)

position_label = ctk.CTkLabel(frame_song_label, text='00:00 / Time', font=("fonts/MonoLisa-Bold.ttf", 17))
position_label.pack(anchor=tk.W, padx=10, pady=10)

split_label(frame_song_label, 138, anchor='nw')

volume_slide_bar = ctk.CTkSlider(frame_list_box, from_=0, to=100, fg_color='#696969', button_color='#696969',
                                 button_hover_color='#707070', width=100, command=update_volume)
volume_slide_bar.pack(anchor=tk.W, padx=10, pady=10)

listbox = CTkListbox(frame_list_box, width=730, height=400, font=("fonts/MonoLisa-Bold.ttf", 15), command=play_song)
listbox.pack(padx=10, pady=10)

remove_button = ctk.CTkButton(frame_file_buttons, text="", image=remove_image, font=('Arial', 15), width=7,
                              fg_color='#696969', corner_radius=10, hover_color='#707070', command=remove_songs)
remove_button.pack(side=tk.LEFT, padx=10)

add_one_song_button = ctk.CTkButton(frame_file_buttons, text="", image=song_image, font=('Arial', 15), width=7,
                                    fg_color='#696969', corner_radius=10, hover_color='#707070', command=add_one_song)
add_one_song_button.pack(side=tk.LEFT, padx=10)

select_button = ctk.CTkButton(frame_file_buttons, text="", image=folder_image, font=('Arial', 15), width=7,
                              fg_color='#696969', corner_radius=10, hover_color='#707070', command=select_folder)
select_button.pack(side=tk.LEFT, padx=10, pady=10)

last_button = ctk.CTkButton(frame_left, text='', image=last_image, font=('Arial', 15), width=5, fg_color='#696969',
                            corner_radius=8, hover_color='#707070', command=play_last_song)
last_button.pack(side=tk.LEFT, padx=10)

play_button = ctk.CTkButton(frame_left, text='', image=play_image, font=('Arial', 15), width=5, fg_color='#696969',
                            corner_radius=8, hover_color='#707070',
                            command=lambda: play_song(listbox.get_selected_song()))
play_button.pack(side=tk.LEFT, padx=10, pady=20)

next_button = ctk.CTkButton(frame_left, text='', image=next_image, font=('Arial', 15), width=5, fg_color='#696969',
                            corner_radius=8, hover_color='#707070', command=play_next_song)
next_button.pack(side=tk.LEFT, padx=10)

state_label = ctk.CTkLabel(frame_left, text='State: None', font=("fonts/MonoLisa-Bold.ttf", 17))
state_label.pack(side=tk.LEFT, padx=2, pady=10)

info_button = ctk.CTkButton(frame_buttons, text='', image=info_image, font=('Arial', 15), width=5, fg_color='#696969',
                            corner_radius=8, hover_color='#707070', command=info)
info_button.pack(side=tk.LEFT, padx=10, pady=20)

git_button = ctk.CTkButton(frame_buttons, text='', image=git_image, font=('Arial', 15), width=5, fg_color='#696969',
                           corner_radius=8, hover_color='#707070', command=openweb)
git_button.pack(side=tk.LEFT, padx=10, pady=20)

select_form.bind('<space>', play_pause_with_space)
select_form.bind('<Right>', play_next_song_with_button)
select_form.bind('<Left>', play_last_song_with_button)

# Hover option for buttons
Hover(volume_slide_bar, "Volume", duration=1)
Hover(remove_button, "Remove songs", duration=1)
Hover(add_one_song_button, "Add song", duration=1)
Hover(select_button, "Select folder", duration=1)
Hover(last_button, "Last song", duration=1)
Hover(play_button, "Play song", duration=1)
Hover(next_button, "Next song", duration=1)
Hover(info_button, "Info", duration=1)
Hover(git_button, "GitHub page", duration=1)

load_data()

select_form.mainloop()
