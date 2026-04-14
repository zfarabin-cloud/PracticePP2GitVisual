# clock
import pygame
import os
import datetime

# Get the absolute path of the directory containing this script (mickeys_clock/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dictionary to cache loaded images so we don't load them multiple times from the hard drive
_image_library = {}

def get_image(path):
    """
    Loads an image using a relative path, caches it, and returns the pygame surface.
    Paths should be passed as "images/filename.png"
    """
    global _image_library
    
    # Construct an absolute path based on the script's location
    abs_path = os.path.join(BASE_DIR, path).replace("/", os.sep).replace("\\", os.sep)
    
    image = _image_library.get(abs_path)
    if image is None:
        image = pygame.image.load(abs_path)
        _image_library[abs_path] = image
        
    return image

def blitRotate(screen, img, pos, angle):
    """
    Rotates an image around its center and draws it on the screen.
    """
    rotated_img = pygame.transform.rotate(img, angle)
    # Get a new rect that maintains the center position of the original image
    new_rect = rotated_img.get_rect(center=img.get_rect(center=pos).center)
    screen.blit(rotated_img, new_rect.topleft)

def get_clock_angles():
    """
    Gets the current real-world time and calculates the rotation angles 
    for the minute and second hands.
    """
    current_time = datetime.datetime.now()
    minutes = current_time.minute
    seconds = current_time.second

    # Calculate angles using the specific offsets from your original code
    angle_min = -6 * minutes + 53
    angle_sec = -6 * seconds - 60

    return angle_min, angle_sec