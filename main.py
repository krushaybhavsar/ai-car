import pygame, sys, math

pygame.init()

# Screen Settings
WIDTH = 800
HEIGHT = 600
FPS = 60

CAR_SIZE = 35

# Gameplay Settings
STEERING = 5
INITIAL_SPEED = 1
COLLISION_COLOR = (90, 189, 66, 255)

# Collision and Lidar Vision 
POINT_SIZE = 5
CIRCLE_SIZE = 5

class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.road = pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\road.png')
        self.car = pygame.transform.scale(pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\car.png'), (CAR_SIZE, CAR_SIZE))
        self.rotated_sprite = self.car
        self.position = [320, 480]
        self.alive = True
        self.distance_driven = 0
        self.time_driven = 0
        self.speed = INITIAL_SPEED
        self.angle = 0
        self.center_point = [self.position[0] + CAR_SIZE / 2, self.position[1] + CAR_SIZE / 2]

        # Lidars and Collision Points
        self.points = [[[0, 0], (0, 255, 0)], [[0, 0], (0, 255, 0)], [[0, 0], (0, 255, 0)], [[0, 0], (0, 255, 0)]]
        self.lidar_rays = []
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw_screen()
            self.move()
            self.check_collision()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def move(self):
        ######## User Movement ########
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: 
            self.angle += STEERING
        if keys[pygame.K_RIGHT]: 
            self.angle -= STEERING
        ######## User Movement ########

        self.rotated_sprite = self.rotate_center(self.car, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 5)
        self.position[0] = min(self.position[0], WIDTH - 35)

        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 5)
        self.position[1] = min(self.position[1], HEIGHT - 35)

        self.center = [self.position[0] + CAR_SIZE / 2, self.position[1] + CAR_SIZE / 2]

        length = CAR_SIZE / 2
        self.points[0][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        self.points[1][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.points[2][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        self.points[3][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]

        self.distance_driven += self.speed
        self.time_driven += 1

        self.lidar_rays.clear()
        self.update_rays()
        

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def update_rays(self):
        for degree in range(-90, 90, 15):
            length = 0
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
            while not self.road.get_at((x, y)) == COLLISION_COLOR:
                length = length + 1
                x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
                y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
            distance = math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))
            self.lidar_rays.append([(x, y), distance])

    def check_collision(self):
        for point in self.points:
            if self.road.get_at((int(point[0][0]), int(point[0][1]))) == COLLISION_COLOR:
                point[1] = (255, 0, 0)
            else:
                point[1] = (0, 255, 0)

    def draw_screen(self):
        self.screen.blit(self.road, (0,0))
        #self.screen.fill((0, 0, 0))
        self.screen.blit(self.rotated_sprite, self.position)
        for point in self.points:
            pygame.draw.circle(self.screen, point[1], (point[0][0], point[0][1]), POINT_SIZE)
        for ray in self.lidar_rays:
            pygame.draw.line(self.screen, (255, 255, 0), self.center, ray[0])
            pygame.draw.circle(self.screen, (255, 255, 0), ray[0], CIRCLE_SIZE)
        pygame.display.update()

def run_game():
    app = App()
    app.run()

if __name__ == "__main__":
    run_game()