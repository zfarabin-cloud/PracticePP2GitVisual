# main.py
import pygame
from clock import get_image, blitRotate, get_clock_angles

def main():
    pygame.init()

    # Screen setup
    screen_width, screen_height = 1200, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mickey's Clock")

    # Load and scale the background image
    bg_img = get_image("images/mainclock.png")
    bg = pygame.transform.scale(bg_img, (screen_width, screen_height))

    # Calculate the center position for the clock hands
    center_pos = (screen_width / 2, screen_height / 2)

    # Use Pygame's clock to manage frame rate
    fps_clock = pygame.time.Clock()
    done = False

    # Main application loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # 1. Get the current angles from our logic module
        angle_min, angle_sec = get_clock_angles()

        # 2. Draw the background
        screen.blit(bg, (0, 0))

        # 3. Draw the rotated arms (Using 1.py mapping: left=sec, right=min)
        blitRotate(screen, get_image("images/leftarm.png"), center_pos, angle_sec)
        blitRotate(screen, get_image("images/rightarm.png"), center_pos, angle_min)

        # 4. Update the display
        pygame.display.flip()

        # 5. Maintain consistent frame rate (60 FPS)
        fps_clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()