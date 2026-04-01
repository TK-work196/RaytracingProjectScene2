import taichi as ti

ti.init(arch=ti.gpu)

aspect_ratio = 16.0 / 9.0
width = 3840
height = int(width / aspect_ratio)

samples_per_pixel = 1024
max_depth = 3

vec3 = ti.types.vector(3, ti.f32)