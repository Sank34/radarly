import pygame
import serial
import math
from collections import deque

# CONFIG
PORT = "/dev/cu.usbserial-120" # replace with your serial port (on windows it might be "COM...")
BAUD = 115200

WIDTH, HEIGHT = 900, 600
FPS = 60

MAX_CM = 100 # lung max ecran
SWEEP_WIDTH = 20
POINT_MEMORY = 100 


# convert from polar coords to screen coords
def polar(cx, cy, angle, r):
    a = math.radians(angle)
    x = cx + r * math.cos(a)
    y = cy - r * math.sin(a)
    return int(x), int(y)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultrasonic Radar")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

ser = serial.Serial(PORT, BAUD, timeout=0.05)

# centru radar
cx, cy = WIDTH // 2, HEIGHT - 40
radius = min(WIDTH // 2 - 40, HEIGHT - 80)

angle = 0
distance = -1

points = deque(maxlen=POINT_MEMORY)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # citire serial
    try:
        line = ser.readline().decode().strip()
        if "," in line:
            a, d = line.split(",")
            angle = int(a)
            distance = int(float(d))

            if 0 <= distance <= MAX_CM:
                r = (distance / MAX_CM) * radius
                x, y = polar(cx, cy, angle, r)
                points.append((x, y))
    except:
        pass

    # drawing!!!
    screen.fill((15, 15, 15))

    # grid
    grid_color = (0, 200, 0)
    thin = 1

    #semicercuri (10–40 cm)
    for cm in range(10, MAX_CM + 1, 10):
        r = int((cm / MAX_CM) * radius)
        pygame.draw.arc(
            screen, grid_color,
            (cx - r, cy - r, 2 * r, 2 * r),
            math.pi, 2 * math.pi, thin
        )
        label = font.render(f"{cm}cm", True, grid_color)
        screen.blit(label, (cx + r - 30, cy - 20))

    # raze unghi
    for a in range(0, 181, 30):
        x, y = polar(cx, cy, a, radius)
        pygame.draw.line(screen, grid_color, (cx, cy), (x, y), thin)
        txt = font.render(f"{a}°", True, grid_color)
        screen.blit(txt, (x - 10, y - 10))

    # linia de baza
    pygame.draw.line(screen, grid_color, (cx - radius, cy), (cx + radius, cy), thin)

    # SWEEP
    for i in range(SWEEP_WIDTH):
        alpha = max(0, 180 - i * 3)
        col = (0, 255, 0, alpha)
        surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        a1 = angle - i * 0.5
        a2 = angle - (i + 1) * 0.5

        p1 = polar(cx, cy, a1, radius)
        p2 = polar(cx, cy, a2, radius)

        pygame.draw.polygon(surf, col, [(cx, cy), p1, p2])
        screen.blit(surf, (0, 0))

    # linie scanare
    x, y = polar(cx, cy, angle, radius)
    pygame.draw.line(screen, (0, 255, 0), (cx, cy), (x, y), 2)

    # pct detectate
    for p in points:
        pygame.draw.circle(screen, (0, 255, 0), p, 4)

    #text
    info1 = font.render(f"Angle: {angle}", True, (0, 255, 0))
    info2 = font.render(f"Distance: {distance} cm", True, (0, 255, 0))
    screen.blit(info1, (WIDTH - 200, HEIGHT - 50))
    screen.blit(info2, (WIDTH - 200, HEIGHT - 30))

    pygame.display.flip()

ser.close()
pygame.quit()
