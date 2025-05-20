import pygame

pygame.init()
screen = pygame.display.set_mode((500, 400))

player = pygame.Surface((100, 100))
player.fill((255, 255, 255))

running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(player, (100, 100))  # Draw the red player square
    pygame.display.update()  # Update the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()