"""Just a test to make sure pygame works"""
import pygame


# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

if __name__ == "__main__":
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Variable to keep the main loop running
    running = True

    # Main loop
    while running:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False

            # Fill the screen with white
        screen.fill((0,0,0))

        # Create a surface and pass in a tuple containing its length and width
        surf = pygame.Surface((50, 50))

        # Give the surface a color to separate it from the background
        surf.fill((255,255,255))
        rect = surf.get_rect()
        # Put the center of surf at the center of the display
        surf_center = (
            (SCREEN_WIDTH-surf.get_width())/2,
            (SCREEN_HEIGHT-surf.get_height())/2
        )

        # Draw surf at the new coordinates
        screen.blit(surf, surf_center)
        pygame.display.flip()