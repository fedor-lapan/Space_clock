import pygame

# ... rest of your code ...

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Clock")
print("Hello world")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)