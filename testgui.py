#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import commute
import threading

class Application(tk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill=tk.BOTH)
        self.create_widgets()
        self.skipper = None
        self.loaded = False

    def create_widgets(self):
        self.top_label = tk.Label(
                self, text="Internet Radio Commercial Mute Application")
        self.top_label.pack(padx=20, pady=20)

        self.top_frame = tk.Frame(self, borderwidth=1, relief="sunken")
        self.top_frame.pack(fill="x", expand=True, padx=10, pady=10)

        ############
        song_title_frame = tk.Frame(self.top_frame)
        song_title_frame.pack(fill="x", padx=20, pady=10)
        self.song_title_label = tk.Label(song_title_frame, text="Title: ")
        self.song_title_label.pack(side='left')
        self.song_title = tk.Label(song_title_frame, text="wating for title")
        self.song_title.pack(side='right')
        ############

        ############
        song_artist_frame = tk.Label(self.top_frame)
        song_artist_frame.pack(fill="x", padx=20, pady=10)
        self.song_artist_label = tk.Label(song_artist_frame, text="Artist: ")
        self.song_artist_label.pack(side='left')
        self.song_artist = tk.Label(song_artist_frame, text="wating for artist")
        self.song_artist.pack(side='right')
        ############

        ############
        play_status_frame = tk.Label(self.top_frame)
        play_status_frame.pack(fill="x", padx=20, pady=10)
        self.play_status_label = tk.Label(play_status_frame, text="Status: ")
        self.play_status_label.pack(side='left')
        self.play_status = tk.Label(play_status_frame, text="None")
        self.play_status.pack(side='right')
        ############

        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(fill=tk.BOTH, expand=True)


        self.lower_frame = tk.Frame(self)
        self.lower_frame.pack(fill="x", expand=False, padx=10, pady=10)

        self.button_device_loader = tk.Button(
                self.lower_frame, text="Load Devices",
                command=self.load_devices)
        self.button_device_loader.pack(side="left", fill="x", expand=True)

        self.quit = tk.Button(self.lower_frame, text="Quit", command=self.quit)
        self.quit.pack(side="right", fill="x", expand=True)

    def quit(self):

        if self.skipper:
            self.skipper.running = False
        self.master.destroy()

    def load_devices(self):
        n = tk.StringVar()

        self.skipper = commute.CommercialSkipper(self)
        self.skipper.load_device_list()

        if not self.loaded:
            self.box_device_selector = ttk.Combobox(
                    self.middle_frame, width=30, textvariable=n)
            self.box_device_selector.pack(expand=False, fill="x", padx="10")

            button_frame = tk.Frame(self.middle_frame)
            button_frame.pack(fill="x", expand=False, padx=10)

            self.run_button = tk.Button(button_frame, text="Run", command=self.run)
            self.run_button.pack(fill="x", expand=True, side="left", pady=5)
            self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop)
            self.stop_button.pack(fill="x", expand=True, side="right", pady=5)

            self.loaded = True

        self.box_device_selector['values'] = self.skipper.dev_list

    def run(self):

        idx = self.box_device_selector.current()
        if idx < 0:
            return

        if self.skipper.is_alive():
            return

        self.skipper.set_device(self.skipper.dev_list[idx])
        self.skipper.start()


    def stop(self):

        if self.skipper:
            self.skipper.running = False

    def update_status(self, status):

        self.song_title_label.configure(text="Title: ")
        self.song_title.configure(text=status['title'])
        self.song_artist_label.configure(text="Artist: ")
        self.song_artist.configure(text=status['artist'])
        self.play_status.configure(text="Status")
        self.play_status.configure(text=status['status'])


def main():
    root = tk.Tk()
    root.geometry("700x500")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
