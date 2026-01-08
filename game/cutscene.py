from typing import Any
from pygame.event import Event
from engine.scene import Scene
from engine.game import Game
import cv2
import pygame

class Cutscene (Scene):
    
    def __init__(self, mp4path: str, frate: int) :
        self.video = cv2.VideoCapture(mp4path)
        self.fps = frate
        self.clock = pygame.time.Clock()
        self.gameobj : Game
        
    def setGameobj(self, gameobj: Any) -> None:
        self.gameobj = gameobj
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    def handle_event(self, event: Event):
        return
    
    def update(self, dt: int):
        return
    
    def render(self, surface: pygame.Surface):
        frame = self.get_frame()
        if frame is None:
            self.gameobj.pop_scene()
        surface.blit(frame, (0, 0)) # type: ignore
        
    def get_frame(self) -> pygame.Surface | None:
        ret, frame = self.video.read()
        if ret is not True:
            return None
            
        frame = cv2.resize(frame, (1024, 768))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
            
        surf = pygame.surfarray.make_surface(frame) # type: ignore
        return surf
            