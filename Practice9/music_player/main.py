# main
import pygame
import sys
import os
from player import MusicController, SONG_END

def main():
    pygame.init()
    pygame.mixer.init()

    # Window and Layout
    window = pygame.display.set_mode((600, 300))
    pygame.display.set_caption("Python Music Player")
    
    # Path setup for images
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, "images")

    # Load UI Assets using relative paths
    img_play = pygame.image.load(os.path.join(img_dir, 'play.png')).convert_alpha()
    img_stop = pygame.image.load(os.path.join(img_dir, 'stop.png')).convert_alpha()
    img_next = pygame.image.load(os.path.join(img_dir, 'next.png')).convert_alpha()
    img_prev = pygame.image.load(os.path.join(img_dir, 'prev.png')).convert_alpha()

    # Define Button Rectangles
    prev_rect = pygame.Rect(100, 50, 173, 173)
    play_rect = pygame.Rect(300, 50, 173, 173)
    next_rect = pygame.Rect(500, 50, 173, 173)

    player = MusicController()
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_pos):
                    player.toggle_play()
                elif next_rect.collidepoint(mouse_pos):
                    player.play_next()
                elif prev_rect.collidepoint(mouse_pos):
                    player.play_prev()

            # Handle auto-advance when song ends
            if event.type == SONG_END:
                player.play_next()

        # Rendering
        window.fill((255, 255, 255))
        window.blit(img_prev, prev_rect.topleft)
        window.blit(img_next, next_rect.topleft)

        # Draw either Play or Stop depending on state
        current_play_img = img_stop if player.is_playing else img_play
        window.blit(current_play_img, play_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()