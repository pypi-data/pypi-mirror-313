import cv2
import torch
import numpy as np
import open3d as o3d
from PIL import Image
import pyrealsense2 as rs
from transformers import pipeline


#MARK:  REALSENSE

def check_if_realsense_is_present(print_logs = False) -> bool:
    """ 
    Function checks if RealSense camera is present.
        
    Args:
        bool: print_logs
        - if True then there are communicats printed in terminal
            
    Returns:
        bool: 
            - True if camera is present
            - False if camera is missing
    """
    try:
        pipeline = rs.pipeline()
        config = rs.config()
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        if print_logs:print(device.sensors)

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                if print_logs: print("Camera found")
                return True
        if not found_rgb:
            print("No RGB camera found")
            return False
    
    except Exception as e:
        if print_logs: print(e)
        return False

def get_rgb_and_depth_image_from_realsense(print_logs = False, height = 480, width = 640) -> tuple[np.array, np.array]:

    """ 
    Function is looking for RealSense camera. If camera is present, returns color and depth image. If camera is not found, function returns None, None


    Args:
        print_logs: bool: If True, function prints logs.
        height: int: Amount of height pixels of both images.
        width: int: Ammount of width pixels of both images.
            

    Returns:
        colorimage: array: Containing color image.

        depthimage: array: Containing depth image.
        
    """

    try:
        pipeline = rs.pipeline()
        config = rs.config()

        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                if print_logs: print("Camera found")
                break
        if not found_rgb:
            print("No RGB camera found")
            return None, None
        
        config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 30)
        pipeline.start(config)
        colorizer = rs.colorizer()
        align_to = rs.stream.color
        align = rs.align(align_to)


        color_image = None
        depth_image = None
        if print_logs: print("Getting data...")

        while True:
            
            for i in range(100):
                pipeline.wait_for_frames()
                frames = pipeline.wait_for_frames()
                aligned_frames = align.process(frames)
                colorized = colorizer.process(frames)

                depth_frame = aligned_frames.get_depth_frame()
                color_frame = aligned_frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue
                depth_image = np.asanyarray(frames.get_depth_frame().get_data())
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            break

        pipeline.stop()
        if print_logs: print("Data acquired")
        return color_image, depth_image

    except Exception as e:
        print(e)
        return None, None
    
        
def save_ply_file_from_realsense(filename: str) -> None:
    """Save raw point cloude directly from Intel RealSense camera

    Args:
        filename (str): name or path of a point cloude camera file
    """
    pc = rs.pointcloud()
    points = rs.points()
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth)

    pipeline.start(config)

    colorizer = rs.colorizer()

    try:
        frames = pipeline.wait_for_frames()
        colorized = colorizer.process(frames)

        ply = rs.save_to_ply(f"{filename}.ply")
        ply.set_option(rs.save_to_ply.option_ply_binary, False)
        ply.set_option(rs.save_to_ply.option_ply_normals, True)

        print(f"Saving to {filename}.ply...")
        ply.process(colorized)
        print("Done")
    except Exception as e:
        print(e)

    finally:
        pipeline.stop()

def get_realsense_camera_config() -> rs.intrinsics:
    """Function that returne Intel RealSense Camera config

    Returns:
        rs.intrinsics: config on a camera
    """
    pipeline = rs.pipeline()
    config = rs.config()

    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("No RGB camera found")
        return None
    
    pipeline.start(config)
    profile = pipeline.get_active_profile()
    depth_intrinsics = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
    pipeline.stop()
    
    return depth_intrinsics

#MARK: 3D semantic map
    
def create_semantic_3D_map(segmented_color_image, depth_image, fx: float, fy: float, z_scale = 0.001, print_logs = False, save_ply = False) -> o3d.geometry.PointCloud: 
    """Function that process image with its depth into 3D semantic map

    Args:
        segmented_color_image (image): input, segmented image
        depth_image (image): depth image of the segmented image
        fx (float): focal length in x axis
        fy (float): focal length in y axis
        z_scale (float, optional): Defaults to 0.001.
        print_logs (bool, optional): Flag that will show logs. Defaults to False.
        save_ply (bool, optional): Option to sav esemantic map into .ply file. Defaults to False.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        o3d.geometry.PointCloud: _description_
    """

    if isinstance(segmented_color_image,Image.Image):
        segmented_color_image = np.array(segmented_color_image)

    if isinstance(depth_image,Image.Image):
        depth_image = np.array(depth_image)



    if segmented_color_image.shape[:2] != depth_image.shape:
        raise ValueError("The segmented color image and the depth image must have the same dimensions.")

    if len(depth_image.shape) ==3 and depth_image.shape[3] !=1:
        raise ValueError("The depth image must be a single-channel image.")
    
    points = []
    colors = []

    cx = segmented_color_image.shape[1] // 2
    cy = segmented_color_image.shape[0] // 2

    if print_logs: print(f"cx: {cx}, cy: {cy}")



    for v in range(depth_image.shape[0]):
        for u in range(depth_image.shape[1]):
            z = depth_image[v, u] * z_scale
            if z <=0: continue 
                 
            x = (u - cx) * z / fx
            y = -(v - cy) * z / fy

            points.append([x, y, z])
            color = segmented_color_image[v, u, :3] / 255.0  
            colors.append(color)

    if print_logs: 
        print("Przeanalizowano piksele i naniesiono na chmurę głębi")
        print(f"points len: {len(points)}")
        print(f"colors len: {len(colors)}")

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(np.array(points, dtype=np.float32))
    point_cloud.colors = o3d.utility.Vector3dVector(np.array(colors, dtype=np.float32))


    if save_ply: 
        o3d.io.write_point_cloud("semantic_map.ply", point_cloud)
        if print_logs: print("Ply file saved")

    return point_cloud

def view_cloude_point_from_ply(filename: str) -> None:
    """Function to view point cloude from pointed file

    Args:
        filename (str)
    """
    pcd = o3d.io.read_point_cloud(filename)
    o3d.visualization.draw_geometries([pcd])

def view_cloude_point(point_cloude) -> None:
    """Function to view point cloude

    Args:
        cloude_point (array of points): Input cloude to view
    """
    o3d.visualization.draw_geometries([point_cloude])

def photo_from_webcam() -> np.array:
    """Capture image form PC webcam

    Raises:
        ValueError: Error if there is no image form camera

    Returns:
        np.array: image form camera
    """

    cam = cv2.VideoCapture(0)
    result, image = cam.read()

    if result: return image
    else: raise ValueError("No image form webcam")


#MARK: Funkcje segmentacji

def knn(image, centroids_number: int) -> np.array:
    """Uses knn algoryth on a given image

    Args:
        image (cv2 image): Input image
        centroids_number (int): Number of centroids

    Returns:
        np.array: Image after processing
    """
    pixels = image.reshape(-1, 3)
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = centroids_number
    _, labels, (centers) = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape((image.shape))
    return segmented_image, labels, centers

def threshold(image, threshold: int) -> np.array:
    """Uses thresholding on a given image

    Args:
        image (cv2. image): Input image
        threshold (int): threshold value

    Returns:
        np.array: Image after proecssing
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, segmented_image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return segmented_image

def local_threshold(image):
    """Uses local thresholding on a given image

    Args:
        imafe (cv2 image): Input image

    Returns:
        np.array: Image after processing
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    segmented_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return segmented_image

def canny(image, lower_boundry=100, upper_boundry=200) -> np.array:
    """Uses canny edge detection on a given image.

    Args:
        photo (cv2 image): _description_
        lower_boundry (int, optional) Defaults to 100.
        upper_boundry (int, optional): Defaults to 200.

    Returns:
        np.array: Processed image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    segmented_image = cv2.Canny(gray, lower_boundry, upper_boundry)
    return segmented_image
    
def sobel(image, kernel_size=3, gray=True) -> np.array:
    """Uses Sobels operator on a given image

    Args:
        image (cv2 image): input image
        kernel_size (int, optional): Defaults to 3.
        gray (bool, optional): Flage, that indicate if image should be process as grayscale. Defaults to True.

    Raises:
        ValueError: Kernel size value should be odd

    Returns:
        np.array: Image after processing
    """
    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be odd")
    
    if gray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
        segmented_image = cv2.addWeighted(cv2.convertScaleAbs(sobelx), 0.5, cv2.convertScaleAbs(sobely), 0.5, 0)
    else:
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)
        segmented_image = cv2.addWeighted(cv2.convertScaleAbs(sobelx), 0.5, cv2.convertScaleAbs(sobely), 0.5, 0)
    return segmented_image

def region_growing(image) -> np.array:
    """Uses region growing algoryth on a given image

    Args:
        image (cv2 image): input image

    Returns:
        np.array: image after usage of region growing algorythm
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret,thershold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thershold, cv2.MORPH_OPEN, kernel, iterations=2)  
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    distance = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(distance, 0.7 * distance.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(image, markers)
    image[markers ==-1] = [255,0,0]  
    return markers

def watershed(image) -> np.array: 
    """Uses watershed algoryth on a given image

    Args:
        image (cv2 image): input image

    Returns:
        NDarray: image after wathershed
    """

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    sure_bg = cv2.dilate(binary, kernel, iterations=3)
    
    dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    cv2.watershed(image, markers)
    image[markers == -1] = [0, 0, 255]

    return image

#MARK: Depth estimation Models

def use_MiDaS(image, model = "MiDaS_small") -> np.array:
    """Use MiDaS model form PyTorch hub to estimate depth of the given image.

    Args:
        image (cv2 image): input image to estimate its depth.
        model (str, optional): Model type to chose. Options: 'small', 'large', 'hybrid'. Defaults to "MiDaS_small".

    Raises:
        ValueError: _description_

    Returns:
        image: estimated depth image
    """
    if model not in ['small', 'large','hybrid']: raise ValueError("Model must be 'small', 'large' or 'hybrid'")

    if model == 'small': model_type = "MiDaS_small"
    elif model == 'large': model_type = "DPT_Large"
    elif model == 'hybrid': model_type = "DPT_Hybrid"

    midas = torch.hub.load("intel-isl/MiDaS", model_type)

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()

    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

    if model_type == "DPT_Large" or model_type == "DPT_Hybrid": transform = midas_transforms.dpt_transform
    else: transform = midas_transforms.small_transform

    image = np.array(image)
    input_batch = transform(image).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=image.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    return prediction.cpu().numpy(), prediction

def use_MiDaS_Hybrid(image) -> list:
    """Use MiDaS Hybrid model form Hugging face to estimate depth of the given image.

    Args:
        image (_type_): _description_

    Returns:
        _type_: _description_
    """

    device = "CUDA" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model="Intel/dpt-hybrid-midas", device=device)

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    results = depth_estimation(image)
    depth = results['depth']

    return depth, results

def use_EVP(image) -> list: 
    """Use EVP model form Hugging face to estimate depth of the given image.
        IMPORTANT: right now model has a bug and cannot be used.

    Args:
        image (PIL Image or cv2 image): input image to estimate its depth

    Returns:
        list: estimated depth image and dict with all estimation result information.
    """

    device = "CUDA" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model="MykolaL/evp_depth", trust_remote_code=True, device = device)

    results = depth_estimation(image)

    return results['depth'], results

def use_BEiT_depth(image) -> list:
    """Use BEiT depth model form Hugging face to estimate depth of the given image.


    Args:
        image (PIL Image or cv2 image): input image to estimate its depth.

    Returns:
        list: estimated depth image and dict with all estimation result information.
    """

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    device = "CUDA" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model="Intel/dpt-beit-large-512", device=device)

    results = depth_estimation(image)
    depth = results['depth']

    return depth, results

def use_Depth_Anything(image, model: str = 'small') -> list:
    """Use Depth Anything model form Hugging face to estimate depth of the given image.

    Args:
        image (PIL Image or cv2 image): input image to estimate its depth.
        model (str, optional): model size to chose. Options: 'small', 'base', 'large' Defaults to 'small'.

    Raises:
        ValueError: Raise when models size is incorrect.

    Returns:
        list: estimated depth image and dict with all estimation result information.
    """


    if model not in ['small','base', 'large']:
        raise ValueError("Model must be 'small', 'base' or 'large'")

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    device = "CUDA" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model=f"LiheYoung/depth-anything-{model}-hf", device=device)

    results = depth_estimation(image)

    depth = results['depth']

    return depth, results

#MARK: Segmentation models

def use_DeepLabV3(image, add_legend = False, model = 'apple', test_colors: bool = False) -> list:
    """Function uses DeepLabV3 model to segment image form Hugging face.


    Args:
        image (PIL Image or cv2 image): input image that will be segmented        
        add_legend (bool, optional): Flag that indicates to add legend into segemnted image with label. Defaults to False.        
        model (str, optional): Model to choose. Options: 'apple', 'apple-xx', 'google'. Defaults to 'apple'.
        test_colors (bool, optional): Flag that trigger usage of constant color pallete for segmentation masks. Defaults to False.
    Raises:
        ValueError: Raise when models name is incorrect.

    Returns:
        list: segmented image as PIL Image, list of labels and list of masks.
    """

    if model not in ['apple', 'apple-xx', 'google']:
        raise ValueError("Model must be 'apple', 'apple-xx' or 'google'")

    if model == 'apple': model="apple/deeplabv3-mobilevit-small"
    elif model == 'apple-xx': model="apple/deeplabv3-mobilevit-xx-small"
    elif model == 'google': model="google/deeplabv3_mobilenet_v2_1.0_513"

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    device = "CUDA" if torch.cuda.is_available() else -1

    semantic_segmentation = pipeline("image-segmentation", model=model, device=device)   

    results = semantic_segmentation(image)
    
    colors = _generate_color_palette_for_testy(len(results)) if test_colors else generate_color_palette(len(results))

    for i in range(len(results)):
        results[i]['color'] = colors[i]
    
    masked_image = np.zeros_like(image)

    for result in results:
        mask = np.array(result['mask'])
        colored_mask = np.zeros_like(image)
        color = np.array(result['color'])

        for j in range(3):
            colored_mask[:,:,j] = mask * color[j]
        masked_image += colored_mask
    
    if add_legend:
        labels = [result['label'] for result in results]
        colors = [result['color'] for result in results]
        masked_image = _add_legend_next_to_segmented_imega(masked_image, labels, colors)

    return masked_image, [result['label'] for result in results], [result['mask'] for result in results]
    
def use_OneFormer(image, model = 'large', dataset = 'ade20k', add_legend = False, test_colors = False) -> list: 
    """Function uses OneFormer model to segment image form Hugging face.

    Args:
        image (PIL Image or cv2 image): input image that will be segmented.
        model (str, optional): Model size to choose. Options: 'tiny', 'large'. Defaults to 'large'. IMPORTATN: 'tiny' model can be used only with 'ade20k' dataset.
        dataset (str, optional): Specyfic training dataset. Options: 'ade20k', 'coco', 'cityscapes' Defaults to 'ade20k'.
        add_legend (bool, optional): Flag that indicates to add legend into segemnted image with label. Defaults to False.
        test_colors (bool, optional): Flag that trigger usage of constant color pallete for segmentation masks. Defaults to False.
    Raises:
        ValueError: Raise when models size is incorrect.
        ValueError: Raise when dataset name is incorrect.
        ValueError: Raise when 'tiny' model is used without 'ade20k' dataset.

    Returns:
        list: _description_
    """

    if model not in ['large', 'tiny']:
        raise ValueError("Model must be 'large' or 'tiny'")

    if dataset not in ['ade20k', 'coco', 'cityscapes']:
        raise ValueError("Dataset must be 'ade20k', 'cityscapes' or 'coco'")

    if model == 'tiny' and dataset != "ade20k":
        raise ValueError("Tiny model is available only for ADE20K dataset")

    model = f"shi-labs/oneformer_{dataset}_swin_{model}"

    device = "CUDA" if torch.cuda.is_available() else -1

    semantic_segmentation = pipeline("image-segmentation", model="shi-labs/oneformer_ade20k_swin_large",device = device)   

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    results = semantic_segmentation(image)
    
    colors = _generate_color_palette_for_testy(len(results)) if test_colors else generate_color_palette(len(results))

    for i in range(len(results)):
        results[i]['color'] = colors[i]
    
    masked_image = np.zeros_like(image)

    for result in results:
        mask = np.array(result['mask'])
        colored_mask = np.zeros_like(image)
        color = np.array(result['color'])

        for j in range(3):
            colored_mask[:,:,j] = mask * color[j]
        masked_image += colored_mask
    
    if add_legend:
        labels = [result['label'] for result in results]
        colors = [result['color'] for result in results]
        masked_image = _add_legend_next_to_segmented_imega(masked_image, labels, colors)

    return masked_image, [result['label'] for result in results], [result['mask'] for result in results]
       
def use_BEiT_semantic(image, add_legend = False, model = 'base', test_colors = False) -> list: 
    """Function uses BEiT model to segment image form Hugging face.

    Args:
        image (PIL Image or cv2 image): input image that will be segmented
        add_legend (bool, optional): Flag that indicates to add legend into segemnted image with label. Defaults to False.        
        model (str, optional): Model size to choose. Options: 'base', 'large' Defaults to 'base'.
        test_colors (bool, optional): Flag that trigger usage of constant color pallete for segmentation masks. Defaults to False.
    Raises:
        ValueError: Raise when models size is incorrect
    Returns:
        list: segmented image as PIL Image, list of labels and list of masks
    """

    if model not in ['base', 'large']:
        raise ValueError("Model must be 'base' or 'large'")
    
    model = f"microsoft/beit-{model}-finetuned-ade-640-640" 

    device = "CUDA" if torch.cuda.is_available() else -1

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    semantic_segmentation = pipeline("image-segmentation", model=model, device=device)

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    results = semantic_segmentation(image)
    
    colors = _generate_color_palette_for_testy(len(results)) if test_colors else generate_color_palette(len(results))

    for i in range(len(results)):
        results[i]['color'] = colors[i]
    
    masked_image = np.zeros_like(image)

    for result in results:
        mask = np.array(result['mask'])
        colored_mask = np.zeros_like(image)
        color = np.array(result['color'])

        for j in range(3):
            colored_mask[:,:,j] = mask * color[j]
        masked_image += colored_mask
    
    if add_legend:
        labels = [result['label'] for result in results]
        colors = [result['color'] for result in results]
        masked_image = _add_legend_next_to_segmented_imega(masked_image, labels, colors)

    return masked_image, [result['label'] for result in results], [result['mask'] for result in results]
    
def use_SegFormer(image, add_legend = False, dataset = 'ade20k', test_colors = False) -> list:
    """Function uses SegFormer model to segment image form Hugging face.

    Args:
        image (PIL Image or cv2 image): input image that will be segmented
        add_legend (bool, optional): Flag that indicates to add legend into segemnted image with label. Defaults to False.        
        dataset (str, optional): Specyfic training dataset. Options: 'ade20k', 'cityscapes' Defaults to 'ade20k'.
        test_colors (bool, optional): Flag that trigger usage of constant color pallete for segmentation masks. Defaults to False.
    Raises:
        ValueError: Raise when models size is incorrect
        ValueError: Raise when dataset name is incorrect

    Returns:
        list: segmented image as PIL Image, list of labels and list of masks    
    """

    if dataset not in ['ade20k', 'cityscapes']:
        raise ValueError("Dataset must be 'ade20k' or 'cityscapes'")

    if dataset == 'ade20k': model = "nvidia/segformer-b0-finetuned-ade-512-512"
    elif dataset == 'cityscapes': model = "nvidia/segformer-b1-finetuned-cityscapes-1024-1024"
    
    device = "CUDA" if torch.cuda.is_available() else -1

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    semantic_segmentation = pipeline("image-segmentation",  model=model, device=device)   

    results = semantic_segmentation(image)
    
    colors = _generate_color_palette_for_testy(len(results)) if test_colors else generate_color_palette(len(results))

    for i in range(len(results)):
        results[i]['color'] = colors[i]
    
    masked_image = np.zeros_like(image)

    for result in results:
        mask = np.array(result['mask'])
        colored_mask = np.zeros_like(image)
        color = np.array(result['color'])

        for j in range(3):
            colored_mask[:,:,j] = mask * color[j]
        masked_image += colored_mask
    
    if add_legend:
        labels = [result['label'] for result in results]
        colors = [result['color'] for result in results]
        masked_image = _add_legend_next_to_segmented_imega(masked_image, labels, colors)

    return masked_image, [result['label'] for result in results], [result['mask'] for result in results]

def use_MaskFormer(image, add_legend = False, model = 'base', dataset = 'coco', test_colors= False) -> list:
    """Function uses mMaskFormer model to segment image form Hugging face.

    Args:
        image (PIL Image or cv2 image): input image that will be segmented
        add_legend (bool, optional): Flag that indicates to add legend into segemnted image with label. Defaults to False.        model (str, optional): _description_. Defaults to 'base'.
        model (str, optional): Model size to choose. Options: 'tiny', 'small', 'base', 'large'. Defaults to 'base'.
        dataset (str, optional): Specyfic training dataset. Options: 'coco', 'ade' Defaults to 'coco'.
        test_colors (bool, optional): Flag that trigger usage of constant color pallete for segmentation masks. Defaults to False.
    
    Raises:
        ValueError: Raise when models size is incorrect.
        ValueError: Raise when dataset name is incorrect.

    Returns:
        list: segmented image as PIL Image, list of labels and list of masks
    """

    if model not in ['tiny', 'small', 'base', 'large']:
        raise ValueError("Model must be 'tiny', 'small', 'base' or 'large'")
    
    if dataset not in ['coco', 'ade']:
        raise ValueError("Dataset must be 'coco' or 'ade'")

    model = f"facebook/maskformer-swin-{model}-{dataset}"

    device = "CUDA" if torch.cuda.is_available() else -1

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    semantic_segmentation = pipeline("image-segmentation", model=model, device=device)   

    results = semantic_segmentation(image)
    
    colors = _generate_color_palette_for_testy(len(results)) if test_colors else generate_color_palette(len(results))

    for i in range(len(results)):
        results[i]['color'] = colors[i]
    
    masked_image = np.zeros_like(image)

    for result in results:
        mask = np.array(result['mask'])
        colored_mask = np.zeros_like(image)
        color = np.array(result['color'])

        for j in range(3):
            colored_mask[:,:,j] = mask * color[j]
        masked_image += colored_mask
    
    if add_legend:
        labels = [result['label'] for result in results]
        colors = [result['color'] for result in results]
        masked_image = _add_legend_next_to_segmented_imega(masked_image, labels, colors)

    return masked_image, [result['label'] for result in results], [result['mask'] for result in results]

def use_mask2former(image, add_legend=False, model = 'base', test_colors = False) ->list:
    """Function uses mask2former model to segment image form Hugging face.

    Args:
        image (PIL Image or cv2 image): input image that will be segmented
        add_legend (bool, optional): Flag that indicates to add legend into segemnted image with label. Defaults to False.
        model (str, optional): Model size to choose. Options: 'base', 'large' Defaults to 'base'.
        test_colors (bool, optional): Flag that trigger usage of constant color pallete for segmentation masks. Defaults to False.

    Raises:
        ValueError: Raise when models size is incorrect

    Returns:
        list: segmented image as PIL Image, list of labels and list of masks
    """

    if model not in ['base', 'large']:
        raise ValueError("Model must be 'base' or 'large'")

    model = f"facebook/mask2former-swin-{model}-coco-panoptic"

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    device = "CUDA" if torch.cuda.is_available() else -1

    paoptic_segmentation = pipeline("image-segmentation", model=model, device=device)   

    results = paoptic_segmentation(image)
    
    colors = _generate_color_palette_for_testy(len(results)) if test_colors else generate_color_palette(len(results))

    for i in range(len(results)):
        results[i]['color'] = colors[i]
    
    masked_image = np.zeros_like(image)

    for result in results:
        mask = np.array(result['mask'])
        colored_mask = np.zeros_like(image)
        color = np.array(result['color'])

        for j in range(3):
            colored_mask[:,:,j] = mask * color[j]
        masked_image += colored_mask
    
    if add_legend:
        labels = [result['label'] for result in results]
        colors = [result['color'] for result in results]
        masked_image = _add_legend_next_to_segmented_imega(masked_image, labels, colors)

    

    return masked_image, [result['label'] for result in results], [result['mask'] for result in results]
        
def use_ResNet_panoptic(image, add_legend = False, model = '50', test_colors = False) -> list:
    """Function uses ResNet model to segment image form Hugging face.

    Args:
        image (PIL Image or cv2 image): input image that will be segmented.
        model (str, optional): Model size to choose. Options: '50','101' Defaults to '50'.
        test_colors (bool, optional): Flag that trigger usage of constant color pallete for segmentation masks. Defaults to False.
    Raises:
        ValueError: Raise when models size is incorrect.

    Returns:
        list: segmented image as PIL image, list of labels and list of masks
    """

    if model not in ['50', '101']:
        raise ValueError("Model must be '50' or '101'")
    
    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)
    
    device = "CUDA" if torch.cuda.is_available() else -1

    paoptic_segmentation = pipeline("image-segmentation", model=f"facebook/detr-resnet-{model}-panoptic", device=device)   

    results = paoptic_segmentation(image)
    
    colors = _generate_color_palette_for_testy(len(results)) if test_colors else generate_color_palette(len(results))

    for i in range(len(results)):
        results[i]['color'] = colors[i]
    
    masked_image = np.zeros_like(image)

    for result in results:
        mask = np.array(result['mask'])
        colored_mask = np.zeros_like(image)
        color = np.array(result['color'])

        for j in range(3):
            colored_mask[:,:,j] = mask * color[j]
        masked_image += colored_mask
    
    if add_legend:
        labels = [result['label'] for result in results]
        colors = [result['color'] for result in results]
        masked_image = _add_legend_next_to_segmented_imega(masked_image, labels, colors)

    return masked_image, [result['label'] for result in results], [result['mask'] for result in results]
         
#MARK: Additional functions

def _add_legend_next_to_segmented_imega(segmented_image, labels: list, colors: list) -> Image:
    """Hided function. It adds legend to a segmentes image.

    Args:
        segmented_image (PIL image): Input, already segmented image.
        labels (list): List of segmentation labels.
        colors (list): Colors of segmentation masks.

    Returns:
        Image: Segmented image with color legend on its right side.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    image = np.array(segmented_image)
    legend_width = 400 #
    legend_image = np.ones((image.shape[0], legend_width, 3), dtype=np.uint8) * 255

    label_height = image.shape[0] // len(labels)

    for i, label in enumerate(labels):
        x_position = 10
        y_position = (i % len(labels)) * label_height + 40
        color_box_start = (x_position, y_position - 20)
        color_box_end = (x_position + 20, y_position)

        color = colors[i]
        color = (255 - color[0], 255 - color[1], 255 - color[2])

        cv2.rectangle(legend_image, color_box_start, color_box_end, color, -1)

        cv2.putText(legend_image, label, (x_position + 30, y_position), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

    masked_image_with_legend = np.hstack((segmented_image, legend_image))

    return masked_image_with_legend

def _cv2_to_pil(image) -> Image:
    """Quick function that converts OpenCV image into PIL image

    Args:
        image (cv2 image): input image

    Returns:
        PIL image: Converted image.
    """
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def generate_color_palette(n: int) -> list:

    '''
        Function generates a color palette with n colors.
    '''
    palette = []
    for i in range(n):
        palette.append((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)))
    return palette

def log_execution_time(time, function_name: str, print_log = False) -> None:
    '''
        Function logs the execution time of a function.
    '''
    execution_time = time
    if print_log: print(f"Execution time of {function_name}: {execution_time:.2f} seconds")

    with open("execution_time_log.txt", "a") as file:
        file.write(f"{function_name} {execution_time:.4f} \n")

def rs_log_execution_time(time, function_name: str, print_log = False) -> None:
    '''
        Function logs the execution time of a function.
    '''
    execution_time = time
    if print_log: print(f"Execution time of {function_name}: {execution_time:.2f} seconds")

    with open("./testy/rs_time.txt", "a") as file:
        file.write(f"{execution_time:.4f} \n")


def _generate_color_palette_for_testy(n: int = 20) -> list:
    """
    Generate a color palette with n colors.
    Parameters:
    n (int): The number of colors to generate.
    Returns:
    list: A list of n colors in RGB format.
    """

    colors = [
        (255, 1, 1),    
        (1, 255, 1),    
        (1, 1, 255),    
        (255, 255, 1),  
        (1, 255, 255),  
        (255, 1, 255),  
        (192, 192, 192),
        (128, 128, 128),
        (128, 1, 1),    
        (128, 128, 1),  
        (1, 128, 1),    
        (128, 1, 128),  
        (1, 128, 128),  
        (1, 1, 128),    
        (255, 165, 1),  
        (255, 192, 203),
        (75, 1, 130),   
        (240, 230, 140),
        (173, 216, 230),
        (139, 69, 19)   
    ]

    if n > len(colors):
        colors.extend(generate_color_palette(n - len(colors)))

    return colors[:n]
