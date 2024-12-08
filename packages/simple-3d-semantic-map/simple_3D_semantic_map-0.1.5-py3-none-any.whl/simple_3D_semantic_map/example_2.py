# This example demonstrates how to integrate images from RealSense camera with semantic segmentation and depth estimation models.

import simple_3D_semantic_map as lib
import numpy as np
import matplotlib.pyplot as plt

def example_2():

    # Check if RealSense camera is present
    camera_presense = lib.check_if_realsense_is_present(print_logs= False)

    if not camera_presense:
        print("Realsense camera is not present")
        return
    
    # get color image from RealSense camera
    color_image, _ = lib.get_rgb_and_depth_image_from_realsense()

    # get semantic segmentation and depth estimation
    segmented_image,labels,masks  = lib.use_mask2former(color_image, add_legend=True) # here can by used any other semantic segmentation model aviable in library
    depth_image_AI,depth_dict = lib.use_Depth_Anything(color_image) # here can by used any other depth estimation model aviable in library

    print(f"Amount of predicted labels: {len(labels)}")
    print(f"Labels: {labels}")

    # Display the images
    fig = plt.figure(figsize=(18,7))
    fig.add_subplot(1,2,1)
    plt.imshow(segmented_image)
    fig.add_subplot(1,2,2)
    plt.imshow(depth_image_AI, cmap='gray')
    plt.show()


if __name__ == "__main__":
    example_2()