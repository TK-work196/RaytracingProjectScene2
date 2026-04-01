import taichi as ti
from rt_config import width, height, vec3

@ti.dataclass
class Ray:
    ro: vec3
    rd: vec3

@ti.dataclass
class Sphere:
    center: vec3
    radius: ti.f32
    color: vec3
    emission: vec3
    mat_type: ti.i32

@ti.dataclass
class Quad:
    Q: vec3
    u: vec3
    v: vec3
    color: vec3
    emission: vec3
    mat_type: ti.i32  

pixels = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))

spheres = Sphere.field(shape=150)   
quads = Quad.field(shape=1)