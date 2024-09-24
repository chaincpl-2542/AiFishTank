# Example file showing a basic pygame "game loop"
import pygame
import pygame_gui
import random

# Set up the screen dimensions and maximum speed for agents
WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 2
NUMBER_AGENT = 20  # Number of agents in the simulation

# Factors controlling the behavior of the agents
COHERENCE_FACTOR = 0.01 # Controls how strongly agents are attracted to the center of mass
ALIGNMENT_FACTOR = 0.1  # Controls how strongly agents align their direction with others
SEPARATION_FACTOR = 0.05  # Controls how strongly agents avoid each other
SEPARATION_DIST = 25  # Minimum distance to maintain between agents


# -----------------------------------------------------------------------
# Agent class represents each moving entity in the simulation
# -----------------------------------------------------------------------

class Agent:
    def __init__(self, x, y) -> None:
        # Initialize agent's position and velocity with random values
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(
            random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = 1  # Mass of the agent used in force calculation

        self.frame_size = 64
        self.fx = 0
        self.fy = 1
        self.agent_frame = agent_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, 
                                                        self.fy * self.frame_size,
                                                        self.frame_size,
                                                        self.frame_size       ))
        
        self.time = 0
        self.animation_frame_rate = 4


    def update_animation(self):
        if self.time > self.animation_frame_rate:
            self.fx = self.fx + 1
            self.fx = self.fx%4

            self.agent_frame = agent_sprite.subsurface(pygame.Rect( 
                                                    self.fx * self.frame_size, 
                                                    self.fy * self.frame_size,
                                                    self.frame_size,
                                                    self.frame_size       ))
            
            self.time = 0
        else:
            self.time = self.time + 1


    def update_physics(self):
        # Update velocity and position of the agent based on current acceleration
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            # Limit the speed to MAX_SPEED
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity
        # Reset acceleration after each update
        self.acceleration = pygame.Vector2(0, 0)

    def update(self):
        self.update_physics()
        self.update_animation()


    def apply_force(self, x, y):
        # Apply a force to the agent, adjusting acceleration based on mass
        force = pygame.Vector2(x, y)
        self.acceleration += force / self.mass


    def seek(self, x, y):
        # Calculate the direction towards a target point and apply a small force in that direction
        d = pygame.Vector2(x, y) - self.position
        d = d.normalize() * 0.1  # Adjust the force magnitude
        seeking_force = d
        self.apply_force(seeking_force.x, seeking_force.y)

    def coherence(self, agents):
        # Steer towards the average position (center of mass) of neighboring agents
        center_of_mass = pygame.Vector2(0, 0)
        agent_in_range_count = 0
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < 100:  # Only consider nearby agents within 100 units
                    center_of_mass += agent.position
                    agent_in_range_count += 1

        if agent_in_range_count > 0:
            center_of_mass /= agent_in_range_count  # Calculate average position
            d = center_of_mass - self.position
            f = d * COHERENCE_FACTOR  
            self.apply_force(f.x, f.y)  # Apply coherence force

    def separation(self, agents):
        # Steer to avoid crowding neighbors (separation behavior)
        d = pygame.Vector2(0, 0)
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < SEPARATION_DIST:  # Only consider agents within separation distance
                    d += self.position - agent.position

        separation_force = d * SEPARATION_FACTOR  
        # Apply separation force
        self.apply_force(separation_force.x, separation_force.y)

    def alignment(self, agents):
        # Steer towards the average heading (velocity) of nearby agents (alignment behavior)
        v = pygame.Vector2(0, 0)
        agent_in_range_count = 0
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < 100:  # Only consider nearby agents within 100 units
                    v += agent.velocity
                    agent_in_range_count += 1

        if agent_in_range_count > 0:
            v /= agent_in_range_count  # Calculate average velocity

            alignment_force = v * ALIGNMENT_FACTOR  # Apply alignment force
            if alignment_force:
                self.apply_force(alignment_force.x, alignment_force.y)

    def draw(self, screen):
        # Draw the agent as a red circle on the screen
        # pygame.draw.circle(screen, "red", self.position, 10)
        
        screen.blit(self.agent_frame, self.position - pygame.Vector2(32, 32)  )

        pygame.draw.line(screen, "red", self.position, self.position + self.velocity*10 )


# -----------------------------------------------------------------------
#  Begin 
# -----------------------------------------------------------------------
pygame.init()

##
# load assets
##
agent_sprite = pygame.image.load("./White Cow Walk.png")


# Create a window with the specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  # Initialize a clock to manage frame rate

# Set up font for displaying FPS (frames per second)
font = pygame.font.Font(None, 36)

# -----------------------------------------------------------------------
# setup GUI
# -----------------------------------------------------------------------
gui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
speed_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect = pygame.Rect((10, 10), (200, 20)),
    start_value = 3,
    value_range = (0.0, 10.0),
    manager = gui_manager
)
separation_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect = pygame.Rect((10, 30), (200, 20)),
    start_value = 25,
    value_range = (5.0, 100.0),
    manager = gui_manager
)


# Create a list of agents at random positions within the screen
agents = [Agent(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
          for _ in range(NUMBER_AGENT)]


# ----- GAME LOOP ------------
running = True  # Variable to control the main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user closed the window
            running = False

        gui_manager.process_events(event)

    # Fill the screen with gray color to clear the previous frame
    screen.fill("gray")

    # update GUI manager
    time_delta = clock.tick(60)/ 1000.0
    gui_manager.update(time_delta)

    # adjust setting 
    MAX_SPEED = speed_slider.get_current_value()
    SEPARATION_DIST = separation_slider.get_current_value()


    # Update and draw each agent on the screen
    for agent in agents:
        # Uncomment the next line to make agents seek towards a fixed point (e.g., the center of the screen)
        # agent.seek(400, 400)
        agent.coherence(agents)  # Apply coherence behavior
        agent.separation(agents)  # Apply separation behavior
        agent.alignment(agents)  # Apply alignment behavior
        agent.update()  # Update the agent's position
        agent.draw(screen)  # Draw the agent on the screen

    # Boundary wrapping: make agents appear on the opposite side when they move off the screen
    for agent in agents:
        if agent.position.x > WIDTH:
            agent.position.x = 0
        elif agent.position.x < 0:
            agent.position.x = WIDTH
        if agent.position.y > HEIGHT:
            agent.position.y = 0
        elif agent.position.y < 0:
            agent.position.y = HEIGHT


    # Calculate and display FPS (frames per second) in the top-right corner of the screen
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))


    gui_manager.draw_ui(screen)

    pygame.display.flip()  # Update the screen with the drawn frame
    clock.tick(60)  # Limit the frame rate to 60 frames per second


pygame.quit()  # Clean up and close the game window when the loop ends