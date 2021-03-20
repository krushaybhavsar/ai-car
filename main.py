import pygame, sys, math

# General Settings
WIDTH = 800
HEIGHT = 600
FPS = 60
CAR_SIZE = 35
STEERING = 5
INITIAL_SPEED = 1
COLLISION_COLOR = (90, 189, 66, 255)

# Collision and Lidar Vision Settings
POINT_SIZE = 5
CIRCLE_SIZE = 5

current_generation = 0

class Racecar:

    def __init__(self, set_speed_num):
        self.running = True
        self.car = pygame.transform.scale(pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\car.png'), (CAR_SIZE, CAR_SIZE))
        self.rotated_sprite = self.car
        self.position = [320, 480]
        self.alive = True
        self.distance_driven = 0
        self.time_driven = 0
        self.speed = 0
        self.set_speed_num = set_speed_num
        self.speed_set = False
        self.angle = 0
        self.center_point = [self.position[0] + CAR_SIZE / 2, self.position[1] + CAR_SIZE / 2]

        # Lidars and Collision Points
        self.points = [[[0, 0], (0, 255, 0)], [[0, 0], (0, 255, 0)], [[0, 0], (0, 255, 0)], [[0, 0], (0, 255, 0)]]
        self.lidar_rays = []

    def move(self, road):

        if not self.speed_set:
            self.speed = self.set_speed_num
            self.speed_set = True

        self.rotated_sprite = self.rotate_center(self.car, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 5)
        self.position[0] = min(self.position[0], WIDTH - 40)

        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 5)
        self.position[1] = min(self.position[1], HEIGHT - 40)

        self.center = [self.position[0] + CAR_SIZE / 2, self.position[1] + CAR_SIZE / 2]

        length = CAR_SIZE / 2
        self.points[0][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        self.points[1][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.points[2][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        self.points[3][0] = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]

        self.distance_driven += self.speed
        self.time_driven += 1

        self.check_collision(road)
        self.lidar_rays.clear()
        self.update_rays(road)
        

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def update_rays(self, road):
        # for degree in range(-90, 90, 30):
        for degree in range(-90, 120, 45):
            length = 0
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
            while not road.get_at((x, y)) == COLLISION_COLOR:
                length = length + 1
                x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
                y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
            distance = math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))
            self.lidar_rays.append([(x, y), distance])

    def check_collision(self, road):
        self.alive = True
        for point in self.points:
            if road.get_at((int(point[0][0]), int(point[0][1]))) == COLLISION_COLOR:
                self.alive = False
                break

    def get_distance(self):
        # Get Distances To Border
        radars = self.lidar_rays
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(self.lidar_rays[1][1] / 30)
        return return_values

    def get_state(self):
        return self.alive

    def calculate_reward(self):
        return self.distance_driven / 50.0 # You can change this number

    def draw_screen(self, screen, road):
        # screen.fill((0, 0, 0))
        screen.blit(self.rotated_sprite, self.position)
        for point in self.points:
            pygame.draw.circle(screen, point[1], (point[0][0], point[0][1]), POINT_SIZE)
        for ray in self.lidar_rays:
            pygame.draw.line(screen, (255, 255, 0), self.center, ray[0])
            pygame.draw.circle(screen, (255, 255, 0), ray[0], CIRCLE_SIZE)