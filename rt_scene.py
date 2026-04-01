import random
from rt_classes import spheres, quads

def add_building(q_idx, x, z, w, h, d, color, mat_type):
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [x, 0, z], [w, 0, 0], [0, h, 0], color, mat_type; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [x+w, 0, z+d], [-w, 0, 0], [0, h, 0], color, mat_type; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [x, 0, z+d], [0, 0, -d], [0, h, 0], color, mat_type; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [x+w, 0, z], [0, 0, d], [0, h, 0], color, mat_type; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [x, h, z], [w, 0, 0], [0, 0, d], color, mat_type; q_idx+=1
    return q_idx

def add_lamp(q_idx, bx, bz, dir_x, dir_z):
    pole_h = 16.0
    pw, pd = 0.6, 0.6
    px, pz = bx - pw/2, bz - pd/2
    c_pole = [0.05, 0.05, 0.05]
    
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [px, 0, pz], [pw, 0, 0], [0, pole_h, 0], c_pole, 0; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [px+pw, 0, pz+pd], [-pw, 0, 0], [0, pole_h, 0], c_pole, 0; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [px, 0, pz+pd], [0, 0, -pd], [0, pole_h, 0], c_pole, 0; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [px+pw, 0, pz], [0, 0, pd], [0, pole_h, 0], c_pole, 0; q_idx+=1
    
    lx, lz = bx + dir_x * 3.0, bz + dir_z * 3.0
    lw, ld = 4.0, 4.0
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [lx-lw/2, pole_h, lz-ld/2], [lw, 0, 0], [0, 0, ld], [0,0,0], 0
    quads[q_idx].emission = [50.0, 40.0, 25.0] 
    q_idx+=1
    
    return q_idx

def init_scene():
    print("Loading Scene Data to GPU...")
def init_scene():
    print("Loading Scene Data to GPU...")
    
    # --- BALL ---
    spheres[0].center, spheres[0].radius, spheres[0].color = [0, 1.0, 0], 1.0, [0.9, 0.9, 0.9]
    spheres[1].center, spheres[1].radius, spheres[1].emission = [0, -100, 0], 0.0, [0.0, 0.0, 0.0]

    q_idx = 0
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-100, 0, -100], [200, 0, 0], [0, 0, 200], [0,0,0], 2; q_idx+=1
    
    mat_post = [0.9, 0.9, 0.9]
    mat_net = [0.8, 0.8, 0.8]
    
    gw, gh, gd = 24.0, 10.0, 8.0
    z_pos = 37.0
    
    # GOAL 1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-(gw/2+0.2), 0, -z_pos], [0.4, 0, 0], [0, gh, 0], mat_post, 0; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [(gw/2-0.2), 0, -z_pos], [0.4, 0, 0], [0, gh, 0], mat_post, 0; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-(gw/2+0.2), gh, -z_pos], [gw+0.4, 0, 0], [0, 0.4, 0], mat_post, 0; q_idx+=1 
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-gw/2, 0, -z_pos-gd], [gw, 0, 0], [0, gh, 0], mat_net, 1; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-gw/2, 0, -z_pos-gd], [0, 0, gd], [0, gh, 0], mat_net, 1; q_idx+=1
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [gw/2, 0, -z_pos-gd], [0, 0, gd], [0, gh, 0], mat_net, 1; q_idx+=1

    # GOAL 2
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-(gw/2+0.2), 0, z_pos], [0.4, 0, 0], [0, gh, 0], mat_post, 0; q_idx+=1  
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [(gw/2-0.2), 0, z_pos], [0.4, 0, 0], [0, gh, 0], mat_post, 0; q_idx+=1   
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-(gw/2+0.2), gh, z_pos], [gw+0.4, 0, 0], [0, 0.4, 0], mat_post, 0; q_idx+=1  
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-gw/2, 0, z_pos+gd], [gw, 0, 0], [0, gh, 0], mat_net, 1; q_idx+=1   
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [-gw/2, 0, z_pos], [0, 0, gd], [0, gh, 0], mat_net, 1; q_idx+=1   
    quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [gw/2, 0, z_pos], [0, 0, gd], [0, gh, 0], mat_net, 1; q_idx+=1

    step_w, step_h, z_start, z_len = 1.5, 0.8, -15.0, 30.0
    c_red, c_blue, c_riser = [0.8, 0.15, 0.15], [0.15, 0.25, 0.8], [0.6, 0.6, 0.6]
    
    # --- STANDS ---
    left_x = -22.0
    for i in range(6):
        quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [left_x - i*step_w, i*step_h, z_start], [-step_w, 0, 0], [0, 0, z_len], c_red, 0; q_idx+=1
        quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [left_x - (i+1)*step_w, i*step_h, z_start], [0, step_h, 0], [0, 0, z_len], c_riser, 0; q_idx+=1

    right_x = 22.0
    for i in range(6):
        quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [right_x + i*step_w, i*step_h, z_start], [0, 0, z_len], [step_w, 0, 0], c_blue, 0; q_idx+=1
        quads[q_idx].Q, quads[q_idx].u, quads[q_idx].v, quads[q_idx].color, quads[q_idx].mat_type = [right_x + (i+1)*step_w, i*step_h, z_start], [0, 0, z_len], [0, step_h, 0], c_riser, 0; q_idx+=1
    
    # --- PROCEDURAL BUILDING GENERATION ---
    random.seed(42) 
    gap = 1.5 
    
    for i in range(8):
        bx, bz = -32.0 + i * 8.0, -52.0
        bw, bd = 8.0 - gap, 10.0
        bh = random.uniform(15.0, 45.0)
        q_idx = add_building(q_idx, bx, bz, bw, bh, bd, [0.5, 0.5, 0.5], 3)
        
    for i in range(8):
        bx, bz = -32.0 + i * 8.0, 42.0
        bw, bd = 8.0 - gap, 10.0
        bh = random.uniform(25.0, 45.0)
        q_idx = add_building(q_idx, bx, bz, bw, bh, bd, [0.5, 0.5, 0.5], 3)

    for i in range(7):
        bx, bz = -42.0, -42.0 + i * 12.0
        bw, bd = 10.0, 12.0 - gap
        bh = random.uniform(20.0, 50.0)
        q_idx = add_building(q_idx, bx, bz, bw, bh, bd, [0.5, 0.5, 0.5], 3)
        
    for i in range(7):
        bx, bz = 32.0, -42.0 + i * 12.0
        bw, bd = 10.0, 12.0 - gap
        bh = random.uniform(20.0, 50.0)
        q_idx = add_building(q_idx, bx, bz, bw, bh, bd, [0.5, 0.5, 0.5], 3)

    # --- 4 CORNER STREET LAMPS ---
    q_idx = add_lamp(q_idx, -29.0, -39.0, dir_x= 1.0, dir_z= 1.0)
    q_idx = add_lamp(q_idx,  29.0, -39.0, dir_x=-1.0, dir_z= 1.0)
    q_idx = add_lamp(q_idx, -29.0,  39.0, dir_x= 1.0, dir_z=-1.0)
    q_idx = add_lamp(q_idx,  29.0,  39.0, dir_x=-1.0, dir_z=-1.0)