import random
from rt_classes import spheres, quads

def init_scene():
    print("Loading Sphere Scene to GPU...")
    
    quads[0].Q, quads[0].u, quads[0].v = [-100, 0, -100], [200, 0, 0], [0, 0, 200]
    quads[0].color, quads[0].mat_type = [0.6, 0.6, 0.6], 0

    spheres[0].center, spheres[0].radius, spheres[0].emission = [50.0, 40.0, -30.0], 10.0, [50.0, 45.0, 40.0]
    spheres[0].color, spheres[0].mat_type = [0,0,0], 0


    spheres[1].center, spheres[1].radius, spheres[1].color, spheres[1].mat_type = [-3.0, 4.0, -5.0], 4.0, [0.9, 0.9, 0.9], 1
    spheres[1].emission = [0,0,0]
    
    spheres[2].center, spheres[2].radius, spheres[2].color, spheres[2].mat_type = [4.0, 4.0, -8.0], 4.0, [0.2, 0.4, 0.8], 0
    spheres[2].emission = [0,0,0]

    random.seed(42)
    for i in range(3, 150):
        radius = random.uniform(0.4, 1.2)
        
        x = random.uniform(-25.0, 25.0)
        z = random.uniform(-25.0, 10.0)
        
        if (x+3.0)**2 + (z+5.0)**2 < 30.0 or (x-4.0)**2 + (z+8.0)**2 < 30.0:
            x += 10.0
            
        y = radius 
        r, g, b = random.uniform(0.3, 0.9), random.uniform(0.3, 0.9), random.uniform(0.3, 0.9)
        
        emission = [0.0, 0.0, 0.0]
        
        rand_mat = random.random()
        if rand_mat < 0.25:
            mat_type = 0
        elif rand_mat < 0.50:
            mat_type = 1
        elif rand_mat < 0.65:
            mat_type = 2
        elif rand_mat < 0.80:
            mat_type = 3
        elif rand_mat < 0.90:
            mat_type = 4
            r, g, b = 1.0, 0.8, 0.2
        else:
            mat_type = 5
            r, g, b = 0.0, 0.0, 0.0
            
            color_choice = random.randint(1, 4)
            if color_choice == 1:
                emission = [0.0, 0.0, 35.0] 
            elif color_choice == 2:
                emission = [0.0, 35.0, 0.0]
            elif color_choice == 3:
                emission = [35.0, 2.0, 2.0]
            else:
                emission = [35.0, 15.0, 0.0] 
                
        spheres[i].center = [x, y, z]
        spheres[i].radius = radius
        spheres[i].color = [r, g, b]
        spheres[i].mat_type = mat_type
        spheres[i].emission = emission
        spheres[i].center = [x, y, z]
        spheres[i].radius = radius
        spheres[i].color = [r, g, b]
        spheres[i].mat_type = mat_type
        spheres[i].emission = emission