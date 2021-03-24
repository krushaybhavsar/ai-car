import pygame, sys, neat
from main import *

def run_simulation(genomes, config):

    hide_road = False
    
    nets = []
    cars = []

    car_imgs = [pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\car1.png'),
                pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\car2.png'),
                pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\car3.png'),
                pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\car4.png'),
                pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\car5.png')]

    # Initialize PyGame and display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    road = pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\road2.png')
    
    step = 0
    img_num = 0
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Racecar(5, step, car_imgs[img_num]))
        img_num += 1
        if img_num == 5:
            img_num = 0
        step += 10
        if step > 50:
            step = 0
    
    global current_generation
    current_generation += 1

    counter = 0

    while True:
        # Exit on quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For each car check the option it chooses
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_distance())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 12 # Left
            elif choice == 1:
                car.angle -= 12 # Right
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 3 # Slow Down
            else:
                car.speed += 3 # Speed Up
        
        # Check if car Is still alive
        # Tncrease fitness if yes and break loop if not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.get_state():
                still_alive += 1
                car.move(road)
                genomes[i][1].fitness += car.calculate_reward()
        if still_alive == 0:
            break

        counter += 1
        if counter == 40 * 50: # Stop After About 30 Seconds
            break

        # Draw map and all cars that are still alive
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            hide_road = True
        elif not keys[pygame.K_SPACE]:
            hide_road = False
        screen.blit(road, (0, 0))
        if hide_road:
            screen.fill((0, 0, 0))
        for car in cars:
            if car.get_state():
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    car.draw_screen(screen, road, True)
                elif not keys[pygame.K_LSHIFT] or not keys[pygame.K_RSHIFT]:
                    car.draw_screen(screen, road, False)
        
        # Display info
        font = pygame.font.SysFont('roboto', 23)

        text = font.render("Generation: " + str(current_generation), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (100, 570)
        screen.blit(text, text_rect)

        text = font.render("Current Population: " + str(still_alive), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (650, 570)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60) # 60 FPS

# app = Racecar()
# app.run(screen, clock, road)

if __name__ == "__main__":
    
    # Load config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create population and add reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run simulation for a maximum of 1000 generations
    population.run(run_simulation, 1000)