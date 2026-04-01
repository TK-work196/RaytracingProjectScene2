import numpy as np
from PIL import Image
from rt_config import width, height
from rt_classes import pixels
from rt_scene import init_scene
from rt_renderer import render

if __name__ == "__main__":
    init_scene()
    print(f"Rendering {width}x{height} image on GPU...")
    
    render()
    
    print("Saving image...")
    img = pixels.to_numpy()
    
    img = np.power(np.clip(img, 0.0, 1.0), 1.0/2.2) * 255 
    img = np.rot90(img)
    
    Image.fromarray(img.astype(np.uint8)).save('ball_scatter_scene.png')
    print("Done! Image saved as ball_scatter_scene.png")