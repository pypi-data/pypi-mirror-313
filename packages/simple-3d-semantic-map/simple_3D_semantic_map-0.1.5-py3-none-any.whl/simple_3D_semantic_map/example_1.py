# Example shows how to interuct with the realsense camera.

import simple_3D_semantic_map as lib
import matplotlib.pyplot as plt

def example_1(): 

    # Check if RealSense camera is present
    realsense_presence = lib.check_if_realsense_is_present(print_logs= True)

    if not realsense_presence:
        print("Realsense camera is not present")
        return
    
    print("Realsense camera is present")

    # get RealSense camera configuration
    realsense_config = lib.get_realsense_camera_config()
    
    print(f"model: {realsense_config.model}")
    print(f"fx: {realsense_config.fx}, fy:{realsense_config.fy}")
    print(f"{realsense_config.width}x{realsense_config.height}")

    #get color and depth image form camera
    color_image, depth_image = lib.get_rgb_and_depth_image_from_realsense()

    # Display the images
    fig = plt.figure(figsize=(14,7))
    fig.add_subplot(1,2,1)
    plt.imshow(color_image)
    fig.add_subplot(1,2,2)
    plt.imshow(depth_image)
    plt.show()

    #get depth point cloud
    lib.save_ply_file_from_realsense(filename="1")

    # view point cloud
    lib.view_cloude_point_from_ply("1.ply")   


if __name__ == "__main__":
    example_1()
