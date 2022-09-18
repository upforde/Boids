from pyglet.gl import *
import ctypes
import pyrr
import time

class Triangle:
    def __init__(self):

        self.triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                          0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                          0.0,  0.5, 0.0, 0.0, 0.0, 1.0]

        self.vertex_shader_source = b"""
        #version 330
        in layout(location = 0) vec3 position;
        in layout(location = 1) vec3 color;
        out vec3 newColor;
        uniform mat4 transform;

        void main()
        {
            gl_Position = transform * vec4(position, 1.0f);
            newColor = color;
        }
        """

        self.fragment_shader_source = b"""
        #version 330
        in vec3 newColor;
        out vec4 outColor;
        void main()
        {
            outColor = vec4(newColor, 1.0f);
        }
        """

        vertex_buff = ctypes.create_string_buffer(self.vertex_shader_source)
        c_vertex = ctypes.cast(ctypes.pointer(ctypes.pointer(vertex_buff)), ctypes.POINTER(ctypes.POINTER(GLchar)))
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, 1, c_vertex, None)
        glCompileShader(vertex_shader)

        fragment_buff = ctypes.create_string_buffer(self.fragment_shader_source)
        c_fragment = ctypes.cast(ctypes.pointer(ctypes.pointer(fragment_buff)), ctypes.POINTER(ctypes.POINTER(GLchar)))
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, 1, c_fragment, None)
        glCompileShader(fragment_shader)

        shader = glCreateProgram()
        glAttachShader(shader, vertex_shader)
        glAttachShader(shader, fragment_shader)
        glLinkProgram(shader)

        glUseProgram(shader)

        vbo = GLuint(0)
        glGenBuffers(1, vbo)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, 72, (GLfloat * len(self.triangle))(*self.triangle), GL_STATIC_DRAW)

        #positions
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        #colors
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        self.transform_loc = glGetUniformLocation(shader, b'transform')

        self.rot_y = pyrr.Matrix44.identity()

    def rotate(self):
        self.rot_y = pyrr.Matrix44.from_y_rotation(time.perf_counter() * 2)

        self.rot_y = [y for x in self.rot_y for y in x]

        c_rotate_y = (GLfloat * len(self.rot_y))(*self.rot_y)

        glUniformMatrix4fv(self.transform_loc, 1, GL_FALSE, c_rotate_y)