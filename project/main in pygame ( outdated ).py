import pygame 
import subprocess
import sys
from pathlib import Path
pygame.init()






class Connection:
    def __init__(self):
        pass

class Images:
    def __init__(self):
        BASE_DIR = Path(__file__).parent
        # mouse
        mouse = pygame.image.load(BASE_DIR / "images" /"hand.png").convert_alpha()
        self.mouse = pygame.transform.scale(mouse, (32, 32))
        self.mouse_rect = self.mouse.get_rect()
        self.mouse_size = self.mouse.get_size()
        self.mouse_surf = pygame.mask.from_surface(self.mouse)

        # logo
        logo = pygame.image.load(BASE_DIR / "images" / "Space_logo.png").convert_alpha()
        self.logo = pygame.transform.scale(logo, (500, 500))
        self.logo_rect = self.logo.get_rect()
        self.logo_size = self.logo.get_size()
        self.logo_surf = pygame.mask.from_surface(self.logo)
        


class Main:
    def __init__(self):
    
        
        screen_info = pygame.display.Info()
        self.SCREEN_WIDTH = screen_info.current_w
        self.SCREEN_HEIGHT = screen_info.current_h
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.images = Images()
    

        pygame.display.set_caption("Space clock UI")
        pygame.mouse.set_visible(False)
        self.images.logo_rect.topleft = ((self.SCREEN_WIDTH - self.images.logo_size[0]) // 2, 0)
        
    def draw_main_screen(self):
        self.screen.fill((0, 0, 100))
        self.screen.blit(self.images.logo, ((self.SCREEN_WIDTH-self.images.logo_size[0])/ 2, 0))

    def handle_events(self):
        quiting = False
        left_click = False
        right_click = False
        middle_click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quiting = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: left_click = True
                if event.button == 2: middle_click = True
                if event.button == 3: right_click = True

        return [quiting, left_click, right_click, middle_click]


    def mouse_traker(self):
        self.screen.blit(self.images.mouse, pygame.mouse.get_pos())
        mouse_pos = pygame.mouse.get_pos()
        self.images.mouse_rect.topleft = mouse_pos
        return True

    def collide(self):
        offset = (self.images.logo_rect.left - self.images.mouse_rect.left, 
                    self.images.logo_rect.top - self.images.mouse_rect.top)
        collide = self.images.mouse_surf.overlap(self.images.logo_surf, offset)
        if collide:
            return True
        else:
            return False
    def main(self):
        while True:
            events = self.handle_events()
            if events[0]:
                pygame.quit()
                return True
            if events[1]:
                if self.collide():
                    print("Pressed and touched the logo")
                    
            self.draw_main_screen()
            self.mouse_traker()
            pygame.display.flip()
main = Main()
main.main()