# main
import pygame as pg
from ball import Ball

def main():
    # Initialize Pygame and the clock
    pg.init()
    clock = pg.time.Clock()

    # Screen setup
    width, height = 700, 700
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Moving Ball Task")

    # Create the ball instance
    my_ball = Ball(x=25, y=25, radius=25, color='Red')

    done = False
    while not done:
        # 1. Event Handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        # 2. Logic and Movement
        keys = pg.key.get_pressed()
        my_ball.update(keys, width, height)

        # 3. Rendering
        screen.fill((255, 255, 255)) # Background color
        my_ball.draw(screen)
        
        pg.display.flip()

        # 4. Maintain frame rate
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()