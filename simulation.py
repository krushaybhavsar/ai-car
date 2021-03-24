import pygame, sys, neat
from main import *

def run_simulation(genomes, config):

    hide_road = False
    
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    road = pygame.image.load(r'C:\Users\krush\OneDrive\Desktop\Side Projects\ai-car\imgs\road2.png')
    
    step = 0
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Racecar(10, step))
        step += 0.1
    
    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_distance())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 12 # Left
            elif choice == 1:
                car.angle -= 12 # Right
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2 # Slow Down
            else:
                car.speed += 2 # Speed Up
        
        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
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

        # Draw Map And All Cars That Are 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            hide_road = True
        else:
            hide_road = False
        screen.blit(road, (0, 0))
        if hide_road:
            screen.fill((0, 0, 0))
        for car in cars:
            if car.get_state():
                car.draw_screen(screen, road)
        
        # Display Info
        # all_fonts = pygame.font.get_fonts()
        # print(all_fonts)
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
    
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)