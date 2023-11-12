import os
import pygame
import textwrap
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from listbox.CTkListbox import *
from messagebox.CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk


class MusicPlayer:
    """Class to make the main root"""
    def __init__(self):
        """Initialize the app"""

        # root variables
        self.folder_path = None
        self.paused = False
        self.playback_position = 0
        self.song_positions = {}
        self.current_song_index = -1

        pygame.init()

        # Make the terminal to be clean
        os.system('cls')
        self.setup_gui()
        self.setup_event_handlers()

    def setup_gui(self):
        """Start to making the root"""
        self.root = ctk.CTk()
        self.root.config(background='#252525')
        self.root.title('SUT')

        # Make root to start at the center of the screen
        window_width = 900
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        self.root.title('SUT')

        # All the widgets of the root
        self.frame_list_box = tk.Frame(self.root, background='#252525')
        self.frame_list_box.pack(side=tk.RIGHT, padx=70, pady=10)

        self.frame_buttons = tk.Frame(self.root, background='#252525')
        self.frame_buttons.pack(side=tk.LEFT, padx=150, pady=10)

        self.listbox = CTkListbox(self.frame_list_box, width=300, command=self.play_song)
        self.listbox.pack(padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_song)

        # Image's for buttons
        self.play_image = Image.open("icons/Play.png")
        resize_play_image = self.play_image.resize((20, 20))
        self.play_image = ImageTk.PhotoImage(resize_play_image)

        self.pause_image = Image.open("icons/Pause.png")
        resize_pause_image = self.pause_image.resize((20, 20))
        self.pause_image = ImageTk.PhotoImage(resize_pause_image)

        self.last_image = Image.open("icons/last.png")
        resize_last_image = self.last_image.resize((20, 20))
        self.last_image = ImageTk.PhotoImage(resize_last_image)

        self.next_image = Image.open("icons/next.png")
        resize_next_image = self.next_image.resize((20, 20))
        self.next_image = ImageTk.PhotoImage(resize_next_image)

        # Root button's
        self.select_button = ctk.CTkButton(
            self.frame_list_box,
            text="Add Music",
            font=('Arial', 15),
            width=10,
            fg_color='#696969',
            hover_color='#707070',
            command=self.open_folder_dialog
        )
        self.select_button.pack(pady=10)

        self.last_button = ctk.CTkButton(
            self.frame_buttons,
            text='',
            image=self.last_image,
            font=('Arial', 15),
            width=7,
            fg_color='#696969',
            hover_color='#707070',
            command=self.play_last_song
        )
        self.last_button.pack(side=tk.LEFT, padx=10)

        self.play_button = ctk.CTkButton(
            self.frame_buttons,
            text='',
            image=self.play_image,
            font=('Arial', 15),
            width=7,
            fg_color='#696969',
            hover_color='#707070',
            command=lambda: self.play_song(self.listbox.get(self.listbox.curselection()))
        )
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.next_button = ctk.CTkButton(
            self.frame_buttons,
            text='',
            image=self.next_image,
            font=('Arial', 15),
            width=7,
            fg_color='#696969',
            hover_color='#707070',
            command=self.play_next_song
        )
        self.next_button.pack(side=tk.LEFT, padx=10)

        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def setup_event_handlers(self):
        self.root.bind("<Double-Button-1>", self.on_double_click)  # Make you to click two times in listbox
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.root.after(1000, self.check_song_finish)  # Start checking if song finished every second

    def open_folder_dialog(self):
        """Select folder and add song's"""
        if not self.folder_path:
            self.folder_path = filedialog.askdirectory()
        if self.folder_path and self.listbox.get() != '':
            files = os.listdir(self.folder_path)
            for file in files:
                if file.endswith((".mp3" or ".mp4")):
                    truncated_name = textwrap.shorten(file, width=40, placeholder="...")
                    self.listbox.insert(tk.END, truncated_name)
            if self.listbox.size() == 0:
                # if folder was empty it shows the error
                msg = CTkMessagebox(
                    title="Error",
                    message="No music files found in the selected folder.",
                    icon="error",
                    option_1="OK"
                )
                response = msg.get()
        else:
            # returns if you didnt select folder
            msg = CTkMessagebox(
                title="Reminding",
                message="Do you want leave without select??",
                icon="question",
                option_1="Cancel",
                option_2="No",
                option_3="Yes"
            )
            response = msg.get()

            if response == "Yes" or response == 'Cancel':
                self.root.destroy()
            else:
                self.open_folder_dialog()

    def play_song(self, selected_song):
        """Play's the song and, show images"""
        if self.listbox.size() == 0:
            CTkMessagebox(title="Error", message="Please select a folder first", icon="cancel")
        else:
            song_path = os.path.join(self.folder_path.replace("\\", "/"), selected_song)
            if not pygame.mixer.music.get_busy():
                if selected_song in self.song_positions:
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play(start=self.song_positions[selected_song] / 1000)  # in seconds
                else:
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()
                    self.song_positions[selected_song] = 0
                selection = self.listbox.curselection()
                if isinstance(selection, list) and selection:
                    self.current_song_index = selection[0]
                self.is_playing = True
            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.play_button_image = self.pause_image
                self.play_button.configure(image=self.play_button_image)
                self.is_playing = True
            else:
                self.song_positions[selected_song] = pygame.mixer.music.get_pos()
                pygame.mixer.music.pause()
                self.paused = True
                self.play_button_image = self.play_image
                self.play_button.configure(image=self.play_button_image)
                self.is_playing = False

            if self.is_playing:
                self.play_button_image = self.pause_image
            else:
                self.play_button_image = self.play_image
            self.play_button.configure(image=self.play_button_image)

    def on_double_click(self, event):
        """Can select in listbox with double click"""
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            selected_song = widget.get(index)
            self.play_song(selected_song)

    def on_select_song(self, event):
        """Update the song index"""
        selection = event.widget.curselection()
        if selection:
            self.current_song_index = selection[0]

    def play_next_song(self):
        """Return's next song in listbox"""
        if self.current_song_index < self.listbox.size() - 1:
            self.current_song_index += 1
        else:
            self.current_song_index = 0
        selected_song = self.listbox.get(self.current_song_index)
        self.play_song(selected_song)
        self.listbox.selection_clear()
        self.listbox.selection_set(self.current_song_index)
        self.listbox.activate(self.current_song_index)

    def play_last_song(self):
        """Return's last song in listbox """
        if self.current_song_index > 0:
            self.current_song_index -= 1
        else:
            self.current_song_index = self.listbox.size() - 1
        selected_song = self.listbox.get(self.current_song_index)
        self.play_song(selected_song)
        self.listbox.selection_clear()
        self.listbox.selection_set(self.current_song_index)
        self.listbox.activate(self.current_song_index)

    def check_song_finish(self):
        """Check if the current song has finished playing"""
        if not pygame.mixer.music.get_busy():
            # Play the next song
            self.play_next_song()
        self.root.after(1000, self.check_song_finish)  # Schedule the next check after 1 second

    def on_window_close(self):
        self.root.quit()

    def run(self):
        """Make the loop of the app"""
        self.root.mainloop()


if __name__ == "__main__":
    player = MusicPlayer()
    player.run()