

import pygame

class Mouse:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        cursor_org_1 = pygame.image.load("hand.png")
        self.cursor_org = pygame.transform.scale(cursor_org_1, (30, 30))
        cursor_org_2 = pygame.image.load("click.png")
        self.cursor_light = pygame.transform.scale(cursor_org_2, (30, 30))
        pygame.display.set_caption("Mouse Touch 2.0")
        self.font = pygame.font.SysFont("Arial", 30)
        self.MAIN = (0, 0, 200)
        self.LEFT_CLICK = (0, 0, 0)
        self.RIGHT_CLICK = (255, 165, 0)
        self.MOUSE_CLICK = (0, 200, 0)
        self.background_c = self.MAIN
        self.offset = 15
        self.RESET_COLOR_EVENT = pygame.USEREVENT +1
        self.clock = pygame.time.Clock()
        self.button_rect = pygame.Rect(350, 250, 100, 100)
        pygame.mouse.set_visible(False)


    def run(self):
        while True:
            events = self.check_events()
            if events is False:
                pygame.quit()
                #print("QUIT")
                return True
            elif events is not None:
                self.handle_mouse_click(events)

            self.screen.fill(self.background_c)
            pygame.draw.rect(self.screen, (0, 0, 0), (350, 250, 150, 100), border_radius = 20)
            #m_x, m_y = pygame.mouse.get_pos()
            #self.screen.blit(self.image, (m_x, m_y))
            text = self.font.render("Press : )", True, (255, 255, 255))
            self.screen.blit(text, (350, 275))
            self.handle_custom_mouse()


            pygame.display.flip()
            self.clock.tick(60)
    def handle_custom_mouse(self):
        m_x, m_y = pygame.mouse.get_pos()
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.cursor_light, (m_x + self.offset, m_y + self.offset))
            return True
        else:
            self.screen.blit(self.cursor_org, (m_x + self.offset, m_y + self.offset))
            return True

    def handle_mouse_click(self, value):
        if value == 0:
            self.background_c = self.LEFT_CLICK
            pygame.time.set_timer(self.RESET_COLOR_EVENT, 5000)
        elif value == 1:
            self.background_c = self.RIGHT_CLICK
            pygame.time.set_timer(self.RESET_COLOR_EVENT, 5000)
        else:
            self.background_c = self.MOUSE_CLICK
            pygame.time.set_timer(self.RESET_COLOR_EVENT, 5000)
        return True



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == self.RESET_COLOR_EVENT:
                self.background_c = self.MAIN
        #return True
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        if self.button_rect.collidepoint(mouse_pos):
            for point in range(3):
                print(point)
                if mouse_press[point]:
                    return point
            return None
        else:
            print("Not high enough")
            return None

mouse = Mouse()
mouse.run()

