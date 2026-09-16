from tkinter import image_types

import pygame

class Mouse:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        cursor_org_1 = pygame.image.load("hand.png")
        self.cursor = pygame.transform.scale(cursor_org_1, (30, 30))
        pygame.display.set_caption("Donut_click" )
        self.image_donut = pygame.image.load("donut.png")
        self.font = pygame.font.SysFont("Arial", 30)
        self.clock = pygame.time.Clock()
        self.cursor_surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.cursor_surf.fill((255, 255, 255))
        self.cursor_mask = pygame.mask.from_surface(self.cursor_surf)
        self.donut_mask = pygame.mask.from_surface(self.image_donut)
        self.image_donut_rect = self.image_donut.get_rect(center = (400, 300))
        self.cursor_rect = self.cursor_surf.get_rect()
    def run(self):
        while True:
            self.screen.fill((200, 100, 0))
            self.screen.blit(self.image_donut, (0, 0))
            pygame.display.flip()
            self.clock.tick(1)
            mouse_pos = pygame.mouse.get_pos()
            self.cursor_rect.topleft = mouse_pos
            offset_x = mouse_pos[0] - self.image_donut_rect.x
            offset_y = mouse_pos[1] - self.image_donut_rect.y

            if self.image_donut_rect.collidepoint(mouse_pos) and self.donut_mask.get_at((offset_x, offset_y)):
                print("TOUCHED MY DOUNOUT!!!!!")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True

mouse = Mouse()
mouse.run()
