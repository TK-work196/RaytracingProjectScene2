import taichi as ti

ti.init(arch=ti.gpu)

width = 3840
height = 1440
samples_per_pixel = 1024
max_depth = 3

vec3 = ti.types.vector(3, ti.f32)