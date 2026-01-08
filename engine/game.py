import pygame
from collections import deque as stack
from engine.scene import Scene
from engine.hud import HUD

class Game:
    """
    The main Game class for the engine.
    Handles the game loop.
    """
    
    def __init__(self, scene : Scene, frm : int = 60):
        """
        Initializer for a game with a starting scene and a framerate (optional)

        Args:
            scene (Scene): The scene that should be displayed when the game opens.
            frm (int, optional): The refresh rate for the game. Defaults to 60.
        """
        pygame.init()
        pygame.display.set_caption("Advenchers of Kowawa")

        self.surface = pygame.display.set_mode((1024, 768))
        self.clock = pygame.time.Clock()
        self.running = True
        self.framerate = frm
        
        self.scenestack = stack([scene])
        self.scenestack[-1].setGameobj(self)
        
        self.HUDlist : list[HUD] = []
        
    def add_hud(self, hud: HUD):
        """
        Add a HUD to be displayed every frame.

        Args:
            hud (HUD): The HUD to be added.
        """
        self.HUDlist.append(hud)
        
    def peek_scene(self):
        """
        A method for manipulating the scene stack.
        Returns the scene on the top of the stack, without removing it.
        """
        return self.scenestack[-1]

    def pop_scene(self):
        """
        A method for manipulating the scene stack.
        Removes the scene on the top of the stack and returns it.
        """
        return self.scenestack.pop()
        
    def push_scene(self, scene: Scene):
        """
        A method for manipulating the scene stack.
        Adds a scene to the top of the stack, meaning it will be displayed starting next frame.

        Args:
            scene (Scene): The scene to be added
        """
        self.scenestack.append(scene)
        self.scenestack[-1].setGameobj(self)

    def run(self):
        """
        Begins running the game.
        Enters the game loop and lets go only when the window is closed.
        """
        while self.running:
            dt = self.clock.tick(self.framerate)                # Get dt
            self.handle_events()                                # Let current scene handle events
            self.scenestack[-1].update(dt)                      # Update the current scene
            self.scenestack[-1].render(self.surface)            # Render the current scene
            for hud in self.HUDlist:
                hud.render(self.surface)                        # Render all relevant HUDs
            pygame.display.flip()                               # Update display

    def handle_events(self):
        """
        Distributes every event other than pygame.QUIT to the scene currently displayed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.scenestack[-1].handle_event(event)
