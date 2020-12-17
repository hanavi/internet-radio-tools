#!/usr/bin/env python
# coding: utf-8
#
# Author: James Casey
# Date: 2020-12-16

import pychromecast as cc
from time import sleep
import sys
import click
import threading
import tkinter as tk

class CommercialSkipper(threading.Thread):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.running = False

    def run(self):
        self.skip_commercials()

    def load_device_list(self):

        self.devices = cc.get_chromecasts()[0]
        self.dev_list = []
        for dev in self.devices:
            self.dev_list.append(dev.device.friendly_name)

    def set_device(self, name):

        for dev in self.devices:
            if dev.device.friendly_name == name:
                self.device = dev
                self.device.wait()
                sleep(1)
                return

    def skip_commercials(self):

        print("connected to device")
        mc = self.device.media_controller

        if mc.is_playing:
            self.main_window.play_status.configure(text="Playing")

        default_delay = 5
        delay = default_delay
        muted = False
        self.running = True
        volume = self.device.status.volume_level

        while self.running:

            if not mc.is_playing:
                sleep(delay)
                continue

            status =  mc.status

            time_remaining = status.duration - status.adjusted_current_time

            if time_remaining < 1:
                delay = .1
            elif time_remaining < 5:
                delay = .5
            else:
                delay = default_delay

            title = status.title
            if not title or title == "Advertisement":
                if not muted:
                    volume = self.device.status.volume_level
                    self.device.set_volume(0)
                    self.main_window.play_status.configure(text="Muted")
                    muted = True
                if delay > 1:
                    self.main_window.song_title.configure(text="Advertisement")
                    self.main_window.song_artist.configure(text="None")
            else:
                if muted:
                    self.device.set_volume(volume)
                    self.main_window.play_status.configure(text="Playing")
                    muted = False
                if delay > 1:
                    artist = status.artist
                    if len(title) > 35:
                        title = title[:35] + "..."
                    if len(artist) > 35:
                        artist = artist[:35] + "..."
                    self.main_window.song_title.configure(text=title)
                    self.main_window.song_artist.configure(text=artist)

            sleep(delay)

