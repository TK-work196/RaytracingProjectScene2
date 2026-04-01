import taichi as ti
from rt_config import width, height, samples_per_pixel, max_depth, vec3
from rt_classes import Ray, pixels, spheres, quads, ball_texture, building_texture
from rt_camera import look_from, lower_left_corner, horizontal, vertical

@ti.func
def intersect_sphere(ray, s_idx):
    s = spheres[s_idx]
    oc = ray.ro - s.center
    a = ray.rd.dot(ray.rd)
    half_b = oc.dot(ray.rd)
    c = oc.dot(oc) - s.radius * s.radius
    discriminant = half_b * half_b - a * c
    
    hit_t = 1e20
    normal = vec3(0.0, 0.0, 0.0)
    if discriminant > 0:
        sqrtd = ti.sqrt(discriminant)
        root = (-half_b - sqrtd) / a
        if root > 0.001:
            hit_t = root
            normal = (ray.ro + ray.rd * hit_t - s.center) / s.radius
        else:
            root = (-half_b + sqrtd) / a
            if root > 0.001:
                hit_t = root
                normal = (ray.ro + ray.rd * hit_t - s.center) / s.radius
    return hit_t, normal

@ti.func
def intersect_quad(ray, q_idx):
    q = quads[q_idx]
    uxv = q.u.cross(q.v)
    normal = uxv.normalized()
    denom = normal.dot(ray.rd)
    
    hit_t = 1e20
    u_uv, v_uv = 0.0, 0.0 
    if ti.abs(denom) > 1e-8:
        t = (q.Q - ray.ro).dot(normal) / denom
        if t > 0.001:
            hit_point = ray.ro + ray.rd * t
            planar_hit = hit_point - q.Q
            w_vec = uxv / uxv.dot(uxv)
            alpha = w_vec.dot(planar_hit.cross(q.v))
            beta = w_vec.dot(q.u.cross(planar_hit))
            
            if 0.0 <= alpha <= 1.0 and 0.0 <= beta <= 1.0:
                is_hit = True
                if q.mat_type == 1:
                    a_val = alpha * 80.0
                    b_val = beta * 40.0
                    if (a_val - ti.floor(a_val)) > 0.12 and (b_val - ti.floor(b_val)) > 0.12:
                        is_hit = False 
                
                if is_hit:
                    hit_t = t
                    u_uv, v_uv = alpha, beta 
                    if denom > 0:
                        normal = -normal
    return hit_t, normal, u_uv, v_uv

@ti.kernel
def render():
    for i, j in pixels:
        pixel_color = vec3(0.0, 0.0, 0.0)
        
        for s in range(samples_per_pixel):
            u_coord = (i + ti.random()) / width
            v_coord = (j + ti.random()) / height
            
            ray_dir = (lower_left_corner + u_coord * horizontal + v_coord * vertical - look_from).normalized()
            ray = Ray(look_from, ray_dir)
            
            throughput = vec3(1.0, 1.0, 1.0)
            accumulated_color = vec3(0.0, 0.0, 0.0)
            is_active = True 
            
            for depth in range(max_depth):
                rx, ry, rz = ti.randn(), ti.randn(), ti.randn()
                random_vec = vec3(rx, ry, rz).normalized()
                
                if is_active:
                    closest_t = 1e20
                    hit_normal = vec3(0.0, 0.0, 0.0)
                    hit_color = vec3(0.5, 0.5, 0.5)
                    hit_emission = vec3(0.0, 0.0, 0.0)
                    hit_mat_type = 0
                    hit_u, hit_v = 0.0, 0.0
                    
                    for idx in range(2):
                        t, n = intersect_sphere(ray, idx)
                        if t < closest_t:
                            closest_t = t
                            hit_normal = n
                            hit_emission = spheres[idx].emission
                            hit_mat_type = 10
                            
                    for idx in range(207):
                        t, n, u_uv, v_uv = intersect_quad(ray, idx)
                        if t < closest_t:
                            closest_t = t
                            hit_normal = n
                            hit_color = quads[idx].color
                            hit_emission = quads[idx].emission
                            hit_mat_type = quads[idx].mat_type
                            hit_u, hit_v = u_uv, v_uv

                    if closest_t == 1e20:
                        a = 0.5 * (ray.rd.y + 1.0)
                        sky = (1.0 - a) * vec3(0.01, 0.01, 0.02) + a * vec3(0.02, 0.03, 0.08)
                        accumulated_color += throughput * sky
                        is_active = False
                    
                    elif hit_emission.sum() > 0.0:
                        accumulated_color += throughput * hit_emission
                        is_active = False
                        
                    else:
                        hit_point = ray.ro + ray.rd * closest_t
                        
                        if hit_mat_type == 10:
                            u_tex = 0.5 + ti.atan2(hit_normal.z, hit_normal.x) / (2 * 3.14159)
                            v_tex = 0.5 - ti.asin(hit_normal.y) / 3.14159
                            hit_color = ball_texture[ti.i32(u_tex * 511), ti.i32(v_tex * 511)]

                        if hit_mat_type == 2:
                            px = ti.abs(hit_point.x)
                            pz = ti.abs(hit_point.z)
                            is_line = False
                            
                            if (27.8 < px < 28.2 and pz < 38.2) or (37.8 < pz < 38.2 and px < 28.2): is_line = True
                            if pz < 0.2 and px < 28.2: is_line = True
                            
                            dist = ti.sqrt(px**2 + pz**2)
                            if 4.8 < dist < 5.2: is_line = True
                            
                            if px < 20.2 and 22.0 < pz < 38.2:
                                if (22.0 < pz < 22.4) or (20.0 < px < 20.2):
                                    is_line = True

                            if px < 14.2 and 32.0 < pz < 38.2:
                                if (32.0 < pz < 32.4) or (14.0 < px < 14.2):
                                    is_line = True

                            if is_line:
                                hit_color = vec3(0.9, 0.9, 0.9)
                            else:
                                cx = ti.cast(ti.floor(hit_point.x / 4.0), ti.i32)
                                cz = ti.cast(ti.floor(hit_point.z / 4.0), ti.i32)
                                if (cx + cz) % 2 == 0:
                                    hit_color = vec3(0.15, 0.40, 0.15)
                                else:
                                    hit_color = vec3(0.18, 0.45, 0.18)

                        elif hit_mat_type == 3:
                            tx = ti.i32(ti.math.fract(hit_u * 1.0) * 511)
                            ty = ti.i32(ti.math.fract(hit_v * 4.0) * 511)
                            hit_color = building_texture[tx, ty]
                            
                            u_mod, v_mod = ti.math.fract(hit_u * 8.0), ti.math.fract(hit_v * 16.0)
                            
                            if 0.35 < u_mod < 0.65 and 0.2 < v_mod < 0.8:
                                grid_u, grid_v = ti.floor(hit_u * 8.0), ti.floor(hit_v * 16.0)
                                if ti.abs(ti.sin(grid_u * 12.9 + grid_v * 78.2)) > 0.8:
                                    hit_emission = vec3(1.2, 1.0, 0.6) 
                                    accumulated_color += throughput * hit_emission
                                    is_active = False 
                                else:
                                    hit_color = vec3(0.01, 0.01, 0.02)

                        ray.ro = hit_point + hit_normal * 0.01
                        ray.rd = (hit_normal + random_vec).normalized()
                        throughput *= hit_color
            
            pixel_color += accumulated_color 
            
        pixels[i, j] = pixel_color / samples_per_pixel