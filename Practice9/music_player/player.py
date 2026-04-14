# player
import pygame
import os

# Define the custom event for when a song ends
SONG_END = pygame.USEREVENT + 1

class MusicController:
    def __init__(self):
        # Set up paths relative to this file
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.music_dir = os.path.join(self.base_dir, "music", "sample_tracks")
        
        # Automatically grab all .mp3 files in the folder
        self.songs = [os.path.join(self.music_dir, f) for f in os.listdir(self.music_dir) if f.endswith('.mp3')]
        self.current_index = 0
        self.is_playing = False

        if self.songs:
            pygame.mixer.music.load(self.songs[self.current_index])
            pygame.mixer.music.set_endevent(SONG_END)

    def toggle_play(self):
        """Toggles between play and pause states."""
        if not self.is_playing:
            pygame.mixer.music.play() if pygame.mixer.music.get_pos() == -1 else pygame.mixer.music.unpause()
            self.is_playing = True
        else:
            pygame.mixer.music.pause()
            self.is_playing = False
        return self.is_playing

    def play_next(self):
        """Moves to the next song in the list."""
        if self.songs:
            self.current_index = (self.current_index + 1) % len(self.songs)
            self._load_and_start()

    def play_prev(self):
        """Moves to the previous song in the list."""
        if self.songs:
            self.current_index = (self.current_index - 1) % len(self.songs)
            self._load_and_start()

    def _load_and_start(self):
        """Helper to load and play the current index."""
        pygame.mixer.music.load(self.songs[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True