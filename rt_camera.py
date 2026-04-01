import taichi as ti
import numpy as np
from rt_config import width, height, vec3

look_from = vec3(0.0, 15.0, 35.0)
look_at = vec3(0.0, 0.0, 0.0)
vup = vec3(0.0, 1.0, 0.0)
fov = 60.0

theta = fov * np.pi / 180.0
h = np.tan(theta / 2.0)
viewport_height = 2.0 * h
viewport_width = viewport_height * (width / height)
w = (look_from - look_at).normalized()
u = vup.cross(w).normalized()
v = w.cross(u)
horizontal = viewport_width * u
vertical = viewport_height * v
lower_left_corner = look_from - horizontal / 2.0 - vertical / 2.0 - w