from pyglet.gl import *
from triangle import Triangle

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        glClearColor(0.2, 0.3, 0.2, 1.0)

        self.triangle = Triangle()


    def on_draw(self):
        self.clear()
        glDrawArrays(GL_TRIANGLES, 0, 3)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def update(self, dt):
        self.triangle.rotate()

if __name__ == "__main__":
    window = Window(1920, 1080, "Boids", resizable = True)
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()