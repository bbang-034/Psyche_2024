import pygame
import sys
import math
from circular_queue import CircularQueue

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
RADIUS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circular Queue Visualization")

# Font setup
font = pygame.font.SysFont("hy궁서b", 20)


def draw_text(text, pos, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


def draw_queue(queue):
    screen.fill(WHITE)
    center_x = WIDTH // 2
    center_y = 260
    angle_step = 360 // queue.capacity


    draw_text("Enqueue by 'e'", (10, 200))
    draw_text("Dequeue by 'd'", (10, 250))

    for i in range(queue.capacity):
        angle = math.radians(i * angle_step)
        x = center_x + int(200 * math.cos(angle))
        y = center_y + int(200 * math.sin(angle))

        color = BLUE if queue.queue[i] is not None else BLACK
        pygame.draw.circle(screen, color, (x, y), RADIUS, 2)

        if queue.queue[i] is not None:
            text = font.render(str(queue.queue[i]), True, BLACK)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

    if not queue.is_empty():
        # Draw front indicator
        front_angle = math.radians(queue.front * angle_step)
        front_x = center_x + int(200 * math.cos(front_angle))
        front_y = center_y + int(200 * math.sin(front_angle))
        pygame.draw.circle(screen, RED, (front_x, front_y), RADIUS, 4)
        text = font.render("F", True, RED)
        text_rect = text.get_rect(center=(front_x, front_y - RADIUS - 20))
        screen.blit(text, text_rect)

        # Draw rear indicator
        rear_angle = math.radians(queue.rear * angle_step)
        rear_x = center_x + int(200 * math.cos(rear_angle))
        rear_y = center_y + int(200 * math.sin(rear_angle))
        pygame.draw.circle(screen, RED, (rear_x, rear_y), RADIUS, 4)
        text = font.render("R", True, RED)
        text_rect = text.get_rect(center=(rear_x, rear_y + RADIUS + 20))
        screen.blit(text, text_rect)

    pygame.display.flip()


def input_screen1():
    input_active = True
    user_text = ''
    clock = pygame.time.Clock()

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill(WHITE)
        draw_text("Enter the size of the queue:", (250, 200))
        draw_text(user_text, (575, 200))
        pygame.display.flip()
        clock.tick(30)

    return int(user_text)


def input_screen2():
    input_active = True
    user_text = ''
    clock = pygame.time.Clock()

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode.isdigit():  # Accept only digit input
                    user_text += event.unicode


        draw_text("Enter the number for enqueue:", (200, 540))
        draw_text(user_text, (575, 540))
        pygame.display.flip()
        clock.tick(30)

    return int(user_text)



def main():
    queue_size = input_screen1()
    queue = CircularQueue(queue_size)
    clock = pygame.time.Clock()



    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    try:
                        item = input_screen2()
                        if queue.is_full():
                            # Display queue full message for 2 seconds
                            screen.fill(WHITE)
                            draw_text("Queue is Full!", (250, 200))
                            pygame.display.flip()
                            pygame.time.delay(1000)  # 2000 milliseconds = 2 seconds
                        queue.enqueue(item)
                    except Exception as e:
                        print(e)
                elif event.key == pygame.K_d:
                    try:
                        if queue.is_empty():
                            # Display queue empty message for 2 seconds
                            screen.fill(WHITE)
                            draw_text("Queue is Empty!", (250, 200))
                            pygame.display.flip()
                            pygame.time.delay(1000)  # 2000 milliseconds = 2 seconds
                        queue.dequeue()
                    except Exception as e:
                        print(e)
        draw_queue(queue)
        clock.tick(30)


if __name__ == "__main__":
    main()
