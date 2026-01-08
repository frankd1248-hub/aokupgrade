import pygame

class Camera:
    """
    A 2D camera which is essentially a wrapper for a pygame.Rect at this point
    """
    
    def __init__(self, width : int, height : int):
        """
        Initializes a camera with given bounds and top-left corner at (0, 0)

        Args:
            width (int): Width of the camera in pixels
            height (int): Height of the camera in pixels
        """
        self.width = width
        self.height = height
        self.viewport = pygame.Rect(0, 0, width, height)

    def update(self, target_pos : pygame.Vector2):
        """
        Updates the position of the camera to be centered at a given position

        Args:
            target_pos (pygame.Vector2): The target center
        """
        self.viewport.x = int(target_pos.x - self.width // 2)
        self.viewport.y = int(target_pos.y - self.height // 2)

    def get_viewport_rect(self):
        """
        Returns a rectangle representing the current position and bounds of the camera
        """
        return self.viewport
