import taichi as ti
from rt_config import width, height, samples_per_pixel, max_depth, vec3
from rt_classes import Ray, pixels, spheres, quads
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
        root1 = (-half_b - sqrtd) / a
        root2 = (-half_b + sqrtd) / a
        
        valid_root = -1.0
        is_inside = False
        
        if root1 > 0.001:
            p1 = ray.ro + ray.rd * root1
            if s.mat_type == 4 and is_hole(p1):
                pass
            else:
                valid_root = root1
                
        if valid_root < 0.0 and root2 > 0.001:
            p2 = ray.ro + ray.rd * root2
            if s.mat_type == 4 and is_hole(p2):
                pass
            else:
                valid_root = root2
                is_inside = True 
                
        if valid_root > 0.0:
            hit_t = valid_root
            normal = (ray.ro + ray.rd * hit_t - s.center) / s.radius
            if is_inside:
                normal = -normal
                
    return hit_t, normal

@ti.func
def intersect_quad(ray, q_idx):
    q = quads[q_idx]
    uxv = q.u.cross(q.v)
    normal = uxv.normalized()
    denom = normal.dot(ray.rd)
    hit_t = 1e20
    if ti.abs(denom) > 1e-8:
        t = (q.Q - ray.ro).dot(normal) / denom
        if t > 0.001:
            hit_point = ray.ro + ray.rd * t
            planar_hit = hit_point - q.Q
            w_vec = uxv / uxv.dot(uxv)
            alpha = w_vec.dot(planar_hit.cross(q.v))
            beta = w_vec.dot(q.u.cross(planar_hit))
            if 0.0 <= alpha <= 1.0 and 0.0 <= beta <= 1.0:
                hit_t = t
                if denom > 0:
                    normal = -normal
    return hit_t, normal

@ti.func
def is_hole(p):
    grid_scale = 5.0
    px = p.x * grid_scale
    py = p.y * grid_scale
    pz = p.z * grid_scale
    
    lx = px - ti.floor(px) - 0.5
    ly = py - ti.floor(py) - 0.5
    lz = pz - ti.floor(pz) - 0.5
    
    dist_sq = lx*lx + ly*ly + lz*lz
    return dist_sq < 0.12

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
                    hit_normal = vec3(0.0)
                    hit_color = vec3(0.0)
                    hit_emission = vec3(0.0)
                    hit_mat_type = 0
                    
                    for idx in range(150):
                        t, n = intersect_sphere(ray, idx)
                        if t < closest_t:
                            closest_t = t
                            hit_normal = n
                            hit_color = spheres[idx].color
                            hit_emission = spheres[idx].emission
                            hit_mat_type = spheres[idx].mat_type
                            
                    for idx in range(1):
                        t, n = intersect_quad(ray, idx)
                        if t < closest_t:
                            closest_t = t
                            hit_normal = n
                            hit_color = quads[idx].color
                            hit_emission = quads[idx].emission
                            hit_mat_type = quads[idx].mat_type

                    if closest_t == 1e20:
                        a = 0.5 * (ray.rd.y + 1.0)
                        sky = (1.0 - a) * vec3(1.0, 1.0, 1.0) + a * vec3(0.3, 0.5, 0.8)
                        accumulated_color += throughput * sky
                        is_active = False
                    
                    elif hit_emission.sum() > 0.0:
                        accumulated_color += throughput * hit_emission
                        is_active = False
                        
                    else:
                        hit_point = ray.ro + ray.rd * closest_t
                        
                        if hit_mat_type == 2 or hit_mat_type == 3:
                            u_tex = 0.5 + ti.atan2(hit_normal.z, hit_normal.x) / (2 * 3.14159)
                            safe_y = ti.max(-1.0, ti.min(1.0, hit_normal.y))
                            v_tex = 0.5 - ti.asin(safe_y) / 3.14159
                            
                            if hit_mat_type == 2: 
                                u_check = ti.floor(u_tex * 20.0)
                                v_check = ti.floor(v_tex * 10.0)
                                if (u_check + v_check) % 2 != 0:
                                    hit_color = vec3(0.05, 0.05, 0.05) 
                            elif hit_mat_type == 3: 
                                if ti.sin(v_tex * 60.0) > 0.0:
                                    hit_color = vec3(0.9, 0.9, 0.9) 

                        if hit_mat_type == 1:
                            reflection = ray.rd - 2.0 * ray.rd.dot(hit_normal) * hit_normal
                            ray.rd = reflection.normalized()
                            throughput *= hit_color 
                        else:
                            target = hit_normal + random_vec
                            ray.rd = target.normalized()
                            throughput *= hit_color
                            
                        ray.ro = hit_point + hit_normal * 0.01

            sun_pos = vec3(50.0, 40.0, -30.0)
            sun_dir = (sun_pos - look_from).normalized()
            sun_glow = ti.max(0.0, ray_dir.dot(sun_dir)) 
            base_glare = sun_glow ** 24.0
            
            god_ray_color = vec3(1.0, 0.9, 0.8) * base_glare
            pixel_color += accumulated_color + god_ray_color
            
        pixels[i, j] = pixel_color / samples_per_pixel