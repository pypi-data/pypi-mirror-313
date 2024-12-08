# Example shows how to create 3D semantic map from an loaded image

import simple_3D_semantic_map as lib
#import lib
import matplotlib.pyplot as plt
from PIL import Image


def example_3():

    #Load image
    image = Image.open("./example_3.jpg")
    plt.imshow(image)
    plt.show()


    #Segment image and get depth image
    segmented_image, _, _  = lib.use_mask2former(image,model = 'large',add_legend=False) # here can by used any other semantic segmentation model aviable in library
    depth_image, _ = lib.use_BEiT_depth(image) # here can by used any other depth estimation model aviable in library

    # create 3D semantic map
    semantic_3d_map = lib.create_semantic_3D_map(segmented_image, depth_image, fx = 385, fy = 385, print_logs=True, save_ply=True)

    # view 3D semantic map
    lib.view_cloude_point(semantic_3d_map)


if __name__ == "__main__":
    example_3()
