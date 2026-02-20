import os
import tkinter as tk
import customtkinter as ctk
import pygame
import pygame.mixer
import random
import json
from tkinter import filedialog
from listbox.CTkListbox import 
from messagebox.CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from SUT_error import EmptyFileError

existing_songs = []
folder_path = ""
selected_song = ""
last_played_song = ""


data = {
    'folder_path': '',
    'songs': []
}


def save_data():
    """Save the song's in folder in json file"""
    songs = [listbox.get(idx) for idx in range(listbox.size())]
    songs = [song for song in songs if song is not None]
    data['songs'] = songs
    with open("data/data.json", "w") as file:
        json.dump(data, file)


def load_data():
    """Return the songs that saved in json file"""
    global data, folder_path, existing_songs
    try:
        with open("data/data.json", "r") as file:
            data = json.load(file)
            folder_path = data.get('folder_path', '')
            songs = data.get('songs', [])
            existing_songs = songs
            for song in songs:
                listbox.insert(tk.END, song)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle case when the file doesn't exist or is empty
        pass


def file_path_error():
    """Error to call it anywhere we want"""
    CTkMessagebox(title="Error", message="Please select folder path first", icon="cancel")


def select_folder():
    """Return's the song in the folder that you select"""
    global folder_path

    try:
        # Get folder path and song files
        folder_path = filedialog.askdirectory()
        file_names = os.listdir(folder_path)

        if file_names and folder_path:
            # Check if a song is new and not already in the listbox
            new_songs = [song for song in file_names if song not in existing_songs]

            data['folder_path'] = folder_path

            # Add the new songs to the listbox
            for song in new_songs:
                # Limit the length of the song name to 20 characters
                truncated_song = (song[:60] + '...') if len(song) > 60 else song

                listbox.insert(ctk.END, truncated_song)

            # Update the existing songs list
            existing_songs.extend(new_songs)

            save_data()

        else:
            # Check if file is empty, hit the retry button and try again
            msg = CTkMessagebox(
                title="Warning",
                message="Your file is empty, do you want try another time?",
                icon="warning",
                option_1="Cancel",
                option_2="Retry"
            )

            if msg.get() == "Retry":
                select_folder()

    except EmptyFileError:
        print('Empty file')


def add_one_song():
    """Add a single song to the listbox"""

    CTkMessagebox(title="Info", message="This part will come soon")


def show_error(folder):
    """function to don't write error every time"""
    if folder:
        return True
    file_path_error()


def remove_songs():
    """Remove song's from the listbox"""
    global existing_songs

    if folder_path:
        msg = CTkMessagebox(title="Delete", message="Are you sure you want to delete the songs?",
                            icon="question", option_1="Cancel", option_3="Yes")
        response = msg.get()

        # check the user choice
        if response == "Yes":
            listbox.delete(0, tk.END)
            existing_songs = []  # Clear the existing_songs list

            # Clear the data dictionary and save it to the JSON file
            data['songs'] = []
            with open("data/data.json", "w") as file:
                json.dump(data, file)

        else:
            return
    else:
        file_path_error()


def play_song(selected_option):
    """Play the song"""
    global folder_path, selected_song, last_played_song

    if folder_path:
        # Check if selected_option is None or empty
        if selected_option in existing_songs:
            # Retrieve the full song path based on the selected option
            full_song_path = os.path.join(folder_path, selected_option)

            # Initialize pygame mixer if not already initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Check if selected song is already playing
            if selected_song == selected_option:
                # If already playing, pause the song
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    play_button.configure(image=play_image)  # Change play button image to 'play' icon
                else:
                    pygame.mixer.music.unpause()
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

            # Play the selected song
            pygame.mixer.music.load(full_song_path)
            pygame.mixer.music.play()

            clear_position_label()

            # Update the selected song variable
            selected_song = selected_option

            song_name_label.configure(text="Now playing: " + selected_option)  # Update "Now playing" label

            # Change play button image to 'pause' icon
            play_button.configure(image=pause_image)

            # Update the position bar and position label
            song_length = pygame.mixer.Sound(full_song_path).get_length()
            update_position(song_length)

            # Clear the current selection in the listbox
            listbox.selection_clear()

            # Find the index of the selected song in the listbox
            selected_song_index = existing_songs.index(selected_song)

            # Highlight the selected song in the listbox
            listbox.selection_set(selected_song_index)

        else:
            # Shuffle and play a new song
            play_random_song()
    else:
        file_path_error()


def play_pause_with_space(event):
    """Play or pause the song with the space key"""
    if event.keysym == 'space':
        play_song(listbox.get_selected_song())


def play_next_song():
    """Play the next song in the list"""
    global existing_songs, selected_song

    if existing_songs:
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

    else:
        CTkMessagebox(
            title="Error",
            message="No songs available",
            icon="cancel"
        )
        return


def play_next_song_with_button(event):
    """Return's the next song with right arrow"""
    if event.keysym == 'Right':
        play_next_song()


def play_last_song():
    """Play the previous song in the list"""
    global existing_songs, selected_song

    if existing_songs:
        # Get the index of the currently selected song
        current_index = existing_songs.index(selected_song)

        # Calculate the index of the previous song
        previous_index = (current_index - 1) % len(existing_songs)

        # Get the previous song from the existing songs list
        previous_song = existing_songs[previous_index]

        # Highlight the previous song in the listbox
        listbox.select_item(previous_song)

        # Play the selected previous song
        play_selected_song(previous_song)
        return

    CTkMessagebox(
        title="Error",
        message="No songs available",
        icon="cancel"
    )
    return


def play_last_song_with_button(event):
    """Return's the last song with left arrow"""
    if event.keysym == 'Left':
        play_last_song()


def fade_effect():
    """Return's a fade out effect on songs when they change"""
    if pygame.mixer.music.get_busy():
        # Stop the currently playing song
        pygame.mixer.music.fadeout(200)  # Fade out the song over 1 second

        # Wait for the fade-out effect to complete before loading and playing the next song
        pygame.time.wait(200)

    else:
        clear_position_label()  # Add this line to clear the position label


def clear_position_label():
    """Clear the position_label"""
    position_label.configure(text='00:00 / 00:00')


def play_random_song():
    """Shuffle and play a random song"""
    global folder_path, selected_song

    if not existing_songs:
        CTkMessagebox(
            title="Error",
            message="No songs available to shuffle",
            icon="cancel"
        )
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

        # Get the length of the random song
        song_path = os.path.join(folder_path, selected_song)
        song_length = pygame.mixer.Sound(song_path).get_length()

        # Update the position label for the random song
        update_position(song_length)


def play_selected_song(song):
    """Play the selected song"""
    song_path = os.path.join(folder_path, song)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()


def update_volume(value):
    """Update the volume sound"""
    if existing_songs:
        pygame.init()
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)
    else:
        CTkMessagebox(
            title="Error",
            message="No songs available",
            icon="cancel"
        )


def update_position(song_length):
    """Update the position of the song"""
    global selected_song

    if pygame.mixer.music.get_busy() and selected_song == listbox.get_selected_song():
        current_position = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
        formatted_current_position = format_time(current_position)
        formatted_song_length = format_time(song_length)
        position_label.configure(text=f"{formatted_current_position} / {formatted_song_length}")

    select_form.after(1000, update_position, song_length)  # Update every 1 second


def format_time(seconds):
    """Format the time in seconds to HH:MM:SS"""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def split_label(frame):
    """This function adds a line for split widgets"""
    label = ctk.CTkLabel(frame, text='-' * 600)
    label.pack(anchor=tk.W, padx=10)


# ________________________________________________UI________________________________________________


select_form = ctk.CTk()
select_form.config(background='#252525')
select_form.title('SUT')

icon_path = ImageTk.PhotoImage(file=(os.path.join("R.ico")))
select_form.wm_iconbitmap()
select_form.iconphoto(False, icon_path)

window_width = 1320
window_height = 720

screen_width = select_form.winfo_screenwidth()
screen_height = select_form.winfo_screenheight()

x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

select_form.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

frame_left2 = ctk.CTkFrame(select_form, corner_radius=20)
frame_left2.pack(fill=tk.X, padx=10, pady=10, ipadx=0, ipady=0)

frame_left = ctk.CTkFrame(select_form, corner_radius=20)
frame_left.pack(side=tk.LEFT, padx=10)

frame_song_label = ctk.CTkFrame(frame_left2, corner_radius=17)
frame_song_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 10))

frame_list_box = ctk.CTkFrame(frame_left, corner_radius=20)
frame_list_box.pack(padx=10, pady=10)

frame_file_buttons = ctk.CTkFrame(frame_left, corner_radius=20)
frame_file_buttons.pack(side=tk.BOTTOM, pady=10)

frame_right = ctk.CTkFrame(select_form, corner_radius=20)
frame_right.pack(side=tk.RIGHT, padx=200)

frame_buttons = ctk.CTkFrame(frame_right, corner_radius=20)
frame_buttons.pack(side=tk.RIGHT, padx=50, pady=50, expand=True)

# ________________________________________________images________________________________________________

folder_image = ctk.CTkImage(light_image=Image.open("icons/folder.png"), size=(30, 30))
song_image = ctk.CTkImage(light_image=Image.open("icons/song.png"), size=(30, 30))
remove_image = ctk.CTkImage(light_image=Image.open("icons/remove.png"), size=(30, 30))
play_image = ctk.CTkImage(light_image=Image.open("icons/play.png"), size=(30, 30))
pause_image = ctk.CTkImage(light_image=Image.open("icons/pause.png"), size=(30, 30))
next_image = ctk.CTkImage(light_image=Image.open("icons/next.png"), size=(30, 30))
last_image = ctk.CTkImage(light_image=Image.open("icons/last.png"), size=(30, 30))

# ________________________________________________Widgets________________________________________________

split_label(frame_song_label)

song_name_label = ctk.CTkLabel(frame_song_label, text='Now playing: ', font=("fonts/MonoLisa-Bold.ttf", 15))
song_name_label.pack(anchor=tk.W, padx=12)

split_label(frame_song_label)

volume_slide_bar = ctk.CTkSlider(frame_list_box, from_=0, to=100, fg_color='#696969', button_color='#696969',
                                 button_hover_color='#707070', width=100, command=update_volume)
volume_slide_bar.pack(anchor=tk.W, padx=10, pady=10)

listbox = CTkListbox(frame_list_box, width=520, height=400, font=("fonts/MonoLisa-Bold.ttf", 15), command=play_song)
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

position_label = ctk.CTkLabel(frame_buttons, text='00:00 / 00:00', font=("fonts/MonoLisa-Bold.ttf", 17))
position_label.pack(side=tk.TOP, pady=10)

last_button = ctk.CTkButton(frame_buttons, text='', image=last_image, font=('Arial', 15), width=5, fg_color='#696969',
                            corner_radius=8, hover_color='#707070', command=play_last_song)
last_button.pack(side=tk.LEFT, padx=10)

play_button = ctk.CTkButton(frame_buttons, text='', image=play_image, font=('Arial', 15), width=5, fg_color='#696969',
                            corner_radius=8, hover_color='#707070',
                            command=lambda: play_song(listbox.get_selected_song()))
play_button.pack(side=tk.LEFT, padx=10, pady=20)

next_button = ctk.CTkButton(frame_buttons, text='', image=next_image, font=('Arial', 15), width=5, fg_color='#696969',
                            corner_radius=8, hover_color='#707070', command=play_next_song)
next_button.pack(side=tk.LEFT, padx=10)

select_form.bind('<space>', play_pause_with_space)
select_form.bind('<Right>', play_next_song_with_button)
select_form.bind('<Left>', play_last_song_with_button)

load_data()

select_form.mainloop()
