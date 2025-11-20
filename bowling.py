import pygame
import pymunk
import pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
score = 0
attempts = 3
game_over = False

# Pymunk Setup
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Load Images
ball_image = pygame.image.load("bowling_ball.png")
pin_image = pygame.image.load("pin.png")
background_image = pygame.image.load("bowlingbg.jpg")

ball_image = pygame.transform.scale(ball_image, (70, 70))
pin_image = pygame.transform.scale(pin_image, (60, 90))
background_image = pygame.transform.scale(background_image, (800, 600))

# Sounds (REMOVED)
# hit_sound = pygame.mixer.Sound("bowling_ball.mp3")
# win_sound = pygame.mixer.Sound("win.mp3")
# lose_sound = pygame.mixer.Sound("lose.mp3")


# Ground
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, 580), (800, 580), 5)
ground_shape.friction = 1.0
space.add(ground_body, ground_shape)

# Create Bowling Ball
def create_ball(x, y):
    body = pymunk.Body(2, pymunk.moment_for_circle(2, 0, 25))
    body.position = x, y
    shape = pymunk.Circle(body, 25)
    shape.elasticity = 0.5
    shape.friction = 0.9
    space.add(body, shape)
    return body, shape

ball_body, ball_shape = create_ball(150, 500)

# Create Pins
def create_pin(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (20, 60)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (20, 60))
    shape.elasticity = 0.3
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

# Vertically arranged pins
pins = []
rows = [4, 3, 2, 1]  # Number of pins per row
start_x = 600
start_y = 520
dx = 30  # spacing
dy = 70

for row_index in range(len(rows)):
    num_pins = rows[row_index]
    row_y = start_y - row_index * dy
    row_start_x = start_x - ((num_pins - 1) * dx) / 2
    for i in range(num_pins):
        x = row_start_x + i * dx
        y = row_y
        pins.append(create_pin(x, y))

# Draw
def draw_game():
    screen.blit(background_image, (0, 0))

    # -------------- REMOVED WIN/LOSE CONDITIONS --------------
    # if len(pins) == 0 and not game_over:
    #     win_sound.play()
    #     font = pygame.font.SysFont(None, 72)
    #     win_text = font.render("STRIKE!", True, (0, 255, 0))
    #     screen.blit(win_text, (300, 250))
    #     return

    # if game_over:
    #     lose_sound.play()
    #     font = pygame.font.SysFont(None, 72)
    #     lose_text = font.render("GAME OVER", True, (255, 0, 0))
    #     screen.blit(lose_text, (280, 250))
    #     return
    # -----------------------------------------------------------

    # Draw Ball
    ball_pos = ball_body.position
    screen.blit(ball_image, (ball_pos.x - 25, ball_pos.y - 25))

    # Draw Pins
    global score
    for body, shape in pins[:]:
        pos = body.position
        if pos.x > 800 or pos.y > 600:
            pins.remove((body, shape))
            space.remove(body, shape)
            score += 500
            # hit_sound.play()  # removed
        else:
            screen.blit(pin_image, (pos.x - 15, pos.y - 30))

    # UI
    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Attempts: {attempts}", True, (255, 255, 255)), (10, 50))

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and attempts > 0:

            mouse_pos = pygame.mouse.get_pos()
            ball_body.position = (150, 500)
            ball_body.velocity = ((mouse_pos[0] - 150) * 4,
                                  (mouse_pos[1] - 500) * 4)

            # hit_sound.play()  # removed
            attempts -= 1

            # if attempts == 0 and len(pins) > 0:
            #     game_over = True
            #     pygame.mixer.music.stop()

    space.step(1 / 60.0)
    draw_game()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
