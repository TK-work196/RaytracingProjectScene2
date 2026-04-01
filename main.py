import numpy as np
from PIL import Image
from rt_config import width, height
from rt_classes import pixels, ball_texture, building_texture
from rt_scene import init_scene
from rt_renderer import render

def load_texture(filename, field):
    try:
        img = Image.open(filename).convert('RGB')
        arr = np.array(img.transpose(Image.ROTATE_90)).astype(np.float32) / 255.0
        field.from_numpy(arr)
        print(f"Successfully loaded {filename}")
    except:
        print(f"FAILED to load {filename}. Field remains black!")

if __name__ == "__main__":
    init_scene()
    load_texture('textures/ball_map.jpg', ball_texture)
    load_texture('textures/building_facade.jpg', building_texture)
    print(f"Rendering {width}x{height} image on GPU...")
    
    render()
    
    print("Saving image...")
    img = pixels.to_numpy()
    exposure = 0.4  # Lower this (e.g., 0.3) for a darker night, raise it for more detail
    img *= exposure
    img = np.power(np.clip(img, 0.0, 1.0), 1.0/2.2) * 255 
    img = np.rot90(img)
    
    Image.fromarray(img.astype(np.uint8)).save('football_court_final.png')
    print("Done! Image saved as football_court_final.png")