import vlc
import os
import keyboard

class Player:

    def __init__(self):
        # Initialize the VLC instance
        self.vlc_instance = vlc.Instance()
        # Create a media list player
        self.listPlayer = self.vlc_instance.media_list_player_new()
        # Create a regular media player
        self.mediaPlayer = self.listPlayer.get_media_player()

    def addPlayList(self, localPath):
        # Create a new media list
        self.mediaList = self.vlc_instance.media_list_new()
        path = os.path.join(os.getcwd(), localPath)
        # Add the media to the list
        self.mediaList.add_media(path)
        # Attach the media list to the list player
        self.listPlayer.set_media_list(self.mediaList)
        # Set the media player to full screen
        #self.mediaPlayer.set_fullscreen(True)
        # Mute the media player
        self.mediaPlayer.audio_set_mute(True)
        # Set the playback mode to loop
        #self.listPlayer.set_playback_mode(vlc.PlaybackMode.loop)

    def play(self):
        # Start playback
        self.listPlayer.play()

    def stop(self):
        # Stop playback
        self.listPlayer.stop()

# Usage
play = Player()
play.addPlayList("logo_intro.mp4")
play.play()

while True:
    if keyboard.is_pressed('q'):
        play.stop()  # Use the correct player instance
        break
