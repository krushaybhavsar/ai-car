import pygame
from main import *

def run_game():
    road = pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\road.png')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    app = Racecar(1)
    run(app, screen, clock, road)

def run(app, screen, clock, road):
        while app.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app.running = False
            screen.blit(road, (0,0))
            app.draw_screen(screen, road)
            pygame.display.update()
            control(app)
            manual_check_collision(app, road)
            app.move(road)
            app.check_collision(road)
            clock.tick(FPS)
        pygame.quit()
        sys.exit()

def manual_check_collision(app, road):
    app.alive = True
    for point in app.points:
        if road.get_at((int(point[0][0]), int(point[0][1]))) == COLLISION_COLOR:
            point[1] = (255, 0, 0)
        else:
            point[1] = (0, 255, 0)

def control(app):
    ######## User Movement ########
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        app.angle += STEERING
    if keys[pygame.K_RIGHT]: 
        app.angle -= STEERING
    ######## User Movement ########

if __name__ == "__main__":
    run_game()