import glfw
from OpenGL.GL import *
import numpy as np
import noise

class NoiseField:
    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT = 480
        self.increment = 0.1

    def main(self):
        # Initialize GLFW
        if not glfw.init():
            return

        # Create a window
        window = glfw.create_window(self.WIDTH, self.HEIGHT, "My OpenGL Window", None, None)
        

        # Make the window the current context
        glfw.make_context_current(window)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Loop until the user closes the window
        while not glfw.window_should_close(window):
            glClearColor(0, 0, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT)

            self.generate_noise()

            glfw.swap_buffers(window)
            glfw.poll_events()

        # Destroy the window
        glfw.destroy_window(window)

        # Terminate GLFW
        glfw.terminate()

    def generate_noise(self):
        y_off = 0
        for y in range(self.HEIGHT):
            x_off = 0
            for x in range(self.WIDTH):
                r = (noise.pnoise2(x_off, y_off) + 1) / 2
                glColor4f(r, r, r, 1.0)
                glBegin(GL_POINTS)
                glVertex2f(x, y)
                glEnd()
                x_off += self.increment
            y_off += self.increment


if __name__ == "__main__":
    window = NoiseField()
    window.main()
