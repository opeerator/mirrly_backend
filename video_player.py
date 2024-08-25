import vlc
import os

class Player:
    def __init__(self):
        # Initialize the VLC instance
        self.vlc_instance = vlc.Instance()
        # Create a media player
        self.mediaPlayer = vlc.MediaPlayer(self.vlc_instance)
        # Set the player to full screen
        #self.mediaPlayer.set_fullscreen(True)
        # Mute the media player
        self.mediaPlayer.audio_set_mute(True)
        self.background_media = None

    def play_background(self, localPath):
        path = os.path.join(os.getcwd(), localPath)
        self.background_media = vlc.Media(path)
        self.mediaPlayer.set_media(self.background_media)
        self.mediaPlayer.play()
        # Keep playing the background video in a loop
        self.mediaPlayer.set_playback_mode(vlc.PlaybackMode.loop)
        self._loop_background()

    def _loop_background(self):
        # Keep the background video playing continuously
        while True:
            if not self.mediaPlayer.is_playing():
                self.mediaPlayer.play()
                
    def play_overlay(self, localPath):
        path = os.path.join(os.getcwd(), localPath)
        overlay_media = vlc.Media(path)
        self.mediaPlayer.set_media(overlay_media)
        self.mediaPlayer.play()
    
    def stop(self):
        # Stop playback
        self.mediaPlayer.stop()

    def set_volume(self, volume):
        # Set the volume of the media player
        self.mediaPlayer.audio_set_volume(volume)
