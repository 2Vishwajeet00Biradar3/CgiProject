import pygame
import sys
import serial
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Cuboid Movement Example')

# Colors
ORANGE = (255, 165, 0)
BLACK = (128, 0, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Function to initialize serial connection
def initialize_serial(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate)
        print(f"Successfully connected to {port}")
        return ser
    except serial.SerialException as e:
        print(f"Error: {e}")
        return None

# Initialize Arduino serial connection
ser = initialize_serial('COM4', 9600)  # Adjust 'COM4' based on your Arduino serial port

# OpenGL initialization function
def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Function to draw a cuboid
def draw_cuboid():
    glBegin(GL_QUADS)
    # Front face
    glColor3fv(ORANGE)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    # Back face
    glColor3fv(WHITE)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    # Top face
    glColor3fv(BLACK)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    # Bottom face
    glColor3fv(BLUE)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    # Left face
    glColor3fv(GREEN)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    # Right face
    glColor3fv(RED)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    glEnd()

# Main loop
def main():
    init_opengl()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        # Read accelerometer and gyroscope data from Arduino
        if ser:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    data = list(map(int, line.split(',')))
                    if len(data) == 6:
                        ax, ay, az, gx, gy, gz = data

                        # Adjust cuboid rotation based on gyroscope data
                        glRotatef(gx / 100.0, 1, 0, 0)
                        glRotatef(gy / 100.0, 0, 1, 0)
                        glRotatef(gz / 100.0, 0, 0, 1)

                        # Draw the cuboid
                        draw_cuboid()
            except Exception as e:
                print(f"Error reading serial data: {e}")

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Cap the frame rate at 30 FPS

    if ser:
        ser.close()  # Close serial connection before exiting
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

