import cv2
import time
import torch
import numpy as np
import open3d as o3d
from PIL import Image
import pyrealsense2 as rs
from transformers import pipeline
from transformers import AutoImageProcessor, DPTForDepthEstimation


#MARK: Funckaje REALSENSE

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
                # Wait for a coherent pair of frames: depth and color
                frames = pipeline.wait_for_frames()
                aligned_frames = align.process(frames)
                colorized = colorizer.process(frames)

                depth_frame = aligned_frames.get_depth_frame()
                color_frame = aligned_frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue
                depth_image = np.asanyarray(frames.get_depth_frame().get_data())
                # Convert images to numpy arrays
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
    """Function is looking for RealSense camera and saves point cloud to .ply file.

    Args:
        filename: string: name (or path) of point clode to save.
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
    """
    Function is looking for RealSense camera and returns its configuration.

    Returns:
        config: (rs.intrinsics), that contains height, width, fx, fy etc.
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
    
def create_semantic_3D_map(segmented_color_image, depth_image, fx: float, fy: float, z_scale = 0.001, print_logs = False, save_ply = False) -> o3d.geometry.PointCloud: #MARK: 3D semantic map
    """
    Create a 3D semantic map from the segmented color image and the depth image.


    :param segmented_color_image (numpy.ndarray): Segmented RGB image.
    :param depth_image (numpy.ndarray): Depth image corresponding to the segmented RGB image.
    :param fx
    :param fy
    :param z_scale
    :param print_logs: True or False
    :param save_ply: True or False

    Returns:
        open3d.geometry.PointCloud: A 3D point cloud representing the semantic map.
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
                 
            #x = (u - cx)# * z / fx
            #y = -(v - cy)# * z / fy

            x = u /fx
            y = -v /fy

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
    '''
    # Function reads and displays .ply file by Open3D.

    :param filename (str): name or path to a file.
    '''
    pcd = o3d.io.read_point_cloud(filename)
    o3d.visualization.draw_geometries([pcd])

def view_cloude_point(cloude_point) -> None:
    """
    Function displays cloude point

    :param cloude_point
    """
    o3d.visualization.draw_geometries([cloude_point])

#MARK: Funkcje segmentacji

def knn(photo, centroids_number: int):
    '''
        Function takes a photo and returns segmented photo using knn algorythm.
    '''
    # Convert the image to RGB
    #photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    # Reshape the image to be a list of pixels
    pixels = photo.reshape(-1, 3)
    # Convert to float
    pixels = np.float32(pixels)
    # Define criteria, number of clusters and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = centroids_number
    _, labels, (centers) = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Convert back to 8 bit values
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    # Reshape back to the original image dimension
    segmented_image = segmented_data.reshape((photo.shape))
    return segmented_image, labels, centers

def threshold(photo, threshold: int):
    '''
        Function takes a photo and returns segmented photo using thresholding algorythm.
    '''
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    _, segmented_image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return segmented_image

def local_threshold(photo):
    '''
        Function takes a photo and returns segmented photo using local thresholding algorythm.
    '''
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    segmented_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return segmented_image

def canny(photo, lower_boundry=100, upper_boundry=200):
    '''
        Function takes a photo and returns segmented photo using canny algorythm.
    '''
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    segmented_image = cv2.Canny(gray, lower_boundry, upper_boundry)
    return segmented_image
    
def sobel(photo, kernel_size=3, gray=True):
    '''
        Function takes a photo and returns segmented photo using sobel algorythm.
    '''
    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be odd")
    
    if gray:
        gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
        segmented_image = cv2.addWeighted(cv2.convertScaleAbs(sobelx), 0.5, cv2.convertScaleAbs(sobely), 0.5, 0)
    else:
        sobelx = cv2.Sobel(photo, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobely = cv2.Sobel(photo, cv2.CV_64F, 0, 1, ksize=kernel_size)
        segmented_image = cv2.addWeighted(cv2.convertScaleAbs(sobelx), 0.5, cv2.convertScaleAbs(sobely), 0.5, 0)
    return segmented_image

def region_growing(image):

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

def watershed(image): 

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

#MARK: Funkcje modeli głebi

def use_MiDaS(image, model = "MiDaS_small"): #DONE
    '''
        https://pytorch.org/hub/intelisl_midas_v2/

        :param image: image to estimate depth
        :param model: model to use (MiDaS_small, DPT_Large, DPT_Hybrid)
    '''

    if model not in ["MiDaS_small", "DPT_Large", "DPT_Hybrid"]:
        raise ValueError("Model must be 'MiDaS_small', 'DPT_Large' or 'DPT_Hybrid'")

    model_type = model
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

def use_MiDaS_Hybrid(image):
    """
    Estimate the depth of an image using the MiDaS Hybrid model.
    This function uses the Intel DPT-Hybrid-MiDaS model to perform depth estimation on the given image.
    Args:
        image: The input image for which depth estimation is to be performed. The image should be in a format compatible with the pipeline.
    Returns:
        tuple: A tuple containing:
            - depth: The estimated depth map of the input image.
            - results: The full results dictionary from the depth estimation pipeline.
    """

    device = "cuda" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model="Intel/dpt-hybrid-midas", device=device)

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    results = depth_estimation(image)
    depth = results['depth']
    # depth = np.array(depth)
    # depth = depth * 255 /depth.max()

    return depth, results

def use_EVP(image): #FIXME:  nie działa???
    """
    Estimate the depth of an image using the EVP depth estimation model.
    Parameters:
    image (PIL.Image): The input image for depth estimation.
    Returns:
    tuple: A tuple containing:
        - depth (numpy.ndarray): The estimated depth map of the input image.
        - results (dict): The full results dictionary from the depth estimation pipeline.
    """

    device = "cuda" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model="MykolaL/evp_depth", trust_remote_code=True, device = device)

    results = depth_estimation(image)

    return results['depth'], results

def use_BEiT_depth(image):
    """
    Estimate the depth of an image using the BEiT model.
    This function uses the "depth-estimation" pipeline from the Hugging Face 
    Transformers library with the "Intel/dpt-beit-large-512" model to estimate 
    the depth of the given image.
    Args:
        image (PIL.Image or numpy.ndarray): The input image for which depth 
        estimation is to be performed.
    Returns:
        tuple: A tuple containing:
            - depth (numpy.ndarray): The estimated depth map of the input image.
            - results (dict): The full results from the depth estimation pipeline.
    """

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    device = "CUDA" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model="Intel/dpt-beit-large-512", device=device)

    results = depth_estimation(image)
    depth = results['depth']
    # depth = np.array(depth)
    # depth = depth * 255 /depth.max()
    #depth = Image.fromarray(depth.astype("uint8"))

    return depth, results

def use_Depth_Anything(image, model: str = "small"):

    if model not in ["small","base", "large"]:
        raise ValueError("Model must be 'small', 'base' or 'large'")

    if not isinstance(image, Image.Image):
        image = _cv2_to_pil(image)

    device = "CUDA" if torch.cuda.is_available() else -1

    depth_estimation = pipeline("depth-estimation", model=f"LiheYoung/depth-anything-{model}-hf", device=device)

    results = depth_estimation(image)

    depth = results['depth']
    # depth = np.array(depth)
    # depth = depth * 255 /torch.max(results['predicted_depth']).item()
    #depth = Image.fromarray(depth.astype("uint8"))

    return depth, results

#MARK: Funkcje segmentacji semantycznej obrazu

def use_DeepLabV3(image, add_legend = False, model = 'apple', test_colors: bool = False): #DONE

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
    #print(colors)

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
    
def use_OneFormer(image, _task = 'semantic', model = 'large', dataset = 'ade20k', add_legend = False, test_colors = False): #DONE
    '''
        Function takes an image and returns segmented image using OneFormer model.
        :param image: image to segment
        :param dataset: dataset to use (ade20k, coco, cityscapes)
        :param model: model to use (large, tiny - only for ade20k)
        :return: segmented image, labels, masks
    '''

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
       
def use_BEiT_semantic(image, add_legend = False, model = 'base', test_colors = False): #FIXME

    '''
    [link](https://huggingface.co/docs/transformers/main/en/model_doc/beit#transformers.BeitForImageClassification)
    
    model = 'base'

    model = 'large' - realy large, over 2.2GB of size
    '''
    if model not in ['base', 'large']:
        raise ValueError("Model must be 'base' or 'large'")
        return None, None, None
    
    model = f"microsoft/beit-{model}-finetuned-ade-640-640" 

    device = "CUDA" if torch.cuda.is_available() else -1

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
    
def use_SegFormer(image, add_legend = False, dataset = 'ade20k', test_colors = False): #DONE
    #https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512

    if dataset not in ['ade20k', 'cityscapes']:
        raise ValueError("Dataset must be 'ade20k' or 'cityscapes'")
        return None, None, None

    if dataset == 'ade20k': model = "nvidia/segformer-b0-finetuned-ade-512-512"
    elif dataset == 'cityscapes': model = "nvidia/segformer-b1-finetuned-cityscapes-1024-1024"
    
    device = "CUDA" if torch.cuda.is_available() else -1

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

def use_MaskFormer(image, add_legend = False, model = 'base', dataset = 'coco', test_colors= False):

    """
    Apply MaskFormer model for semantic segmentation on the given image.
    Parameters:
    image (numpy.ndarray): The input image on which segmentation is to be performed.
    add_legend (bool, optional): If True, adds a legend next to the segmented image. Default is False.
    model (str, optional): The model variant to use. Must be one of 'tiny', 'small', 'base', or 'large'. Default is 'base'.
    dataset (str, optional): The dataset on which the model was trained. Must be 'coco' or 'ade'. Default is 'coco'.
    Returns:
    tuple: A tuple containing:
        - masked_image (numpy.ndarray): The image with applied segmentation masks.
        - labels (list of str): List of labels for each segmented region.
        - masks (list of numpy.ndarray): List of masks for each segmented region.
    Raises:
    ValueError: If the model is not one of 'tiny', 'small', 'base', or 'large'.
    ValueError: If the dataset is not 'coco' or 'ade'.
    """


    if model not in ['tiny', 'small', 'base', 'large']:
        raise ValueError("Model must be 'tiny', 'small', 'base' or 'large'")
    
    if dataset not in ['coco', 'ade']:
        raise ValueError("Dataset must be 'coco' or 'ade'")

    model = f"facebook/maskformer-swin-{model}-{dataset}"

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

#MARK: Funkcje segmentacji panopticon
def use_mask2former(image, add_legend=False, model = 'base', test_colors = False): #DONE

    if model not in ['base', 'large']:
        raise ValueError("Model must be 'base' or 'large'")
        return None, None, None

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
        
def use_ResNet_panoptic(image, add_legend = False, model = '50', test_colors = False):

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
        #color = None
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
         
#MARK: Funkcje pomocnicze

def _add_legend_next_to_segmented_imega(segmented_image, labels: list, colors: list):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    # Tworzenie obrazu legendy z białym tłem
    image = np.array(segmented_image)
    legend_width = 400 # Szerokość legendy
    legend_image = np.ones((image.shape[0], legend_width, 3), dtype=np.uint8) * 255

    label_height = image.shape[0] // len(labels)

    # Dodawanie każdego elementu legendy
    for i, label in enumerate(labels):
        x_position = 10
        y_position = (i % len(labels)) * label_height + 40
        color_box_start = (x_position, y_position - 20)
        color_box_end = (x_position + 20, y_position)

        color = colors[i]
        color = (255 - color[0], 255 - color[1], 255 - color[2])

        # Rysowanie prostokąta z kolorem odpowiadającym etykiecie
        cv2.rectangle(legend_image, color_box_start, color_box_end, color, -1)

        # Dodawanie nazwy etykiety obok prostokąta
        cv2.putText(legend_image, label, (x_position + 30, y_position), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

    # Łączenie segmentowanego obrazu z legendą
    masked_image_with_legend = np.hstack((segmented_image, legend_image))

    return masked_image_with_legend

def _check_results_pipeline(results):
    for i in range(len(results)):
        label = results[i]['label']
        print(f"Label: {label}")
    for i in range(len(results)):
        mask = results[i]['mask']
        print(f"Mask: {mask}")

def _cv2_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def generate_color_palette(n: int):

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
    #execution_time = time.time() - start_time
    execution_time = time
    if print_log: print(f"Execution time of {function_name}: {execution_time:.2f} seconds")

    with open("execution_time_log.txt", "a") as file:
        file.write(f"{function_name} {execution_time:.4f} \n")

def rs_log_execution_time(time, function_name: str, print_log = False) -> None:
    '''
        Function logs the execution time of a function.
    '''
    #execution_time = time.time() - start_time
    execution_time = time
    if print_log: print(f"Execution time of {function_name}: {execution_time:.2f} seconds")

    with open("./testy/rs_time.txt", "a") as file:
        file.write(f"{execution_time:.4f} \n")


def _generate_color_palette_for_testy(n: int = 20):
    """
    Generate a color palette with n colors.
    Parameters:
    n (int): The number of colors to generate.
    Returns:
    list: A list of n colors in RGB format.
    """
    # colors = [
        # (255, 1, 1),    # Czerwony
        # (1, 255, 1),    # Zielony
        # (1, 1, 255),    # Niebieski
        # (255, 255, 1),  # Żółty
        # (1, 255, 255),  # Cyjan
        # (255, 1, 255),  # Magenta
        # (192, 192, 192),# Srebrny
        # (128, 128, 128),# Szary
        # (128, 1, 1),    # Bordowy
        # (128, 128, 1),  # Oliwkowy
        # (1, 128, 1),    # Ciemnozielony
        # (128, 1, 128),  # Purpurowy
        # (1, 128, 128),  # Teal
        # (1, 1, 128),    # Granatowy
        # (255, 165, 1),  # Pomarańczowy
        # (255, 192, 203),# Różowy
        # (75, 1, 130),   # Indygo
        # (240, 230, 140),# Khaki
        # (173, 216, 230),# Jasnoniebieski
        # (139, 69, 19)   # Brązowy
    # ]

    colors = [
        (255, 1, 1),    # Czerwony
        (1, 255, 1),    # Zielony
        (1, 1, 255),    # Niebieski
        (255, 255, 1),  # Żółty
        (1, 255, 255),  # Cyjan
        (255, 1, 255),  # Magenta
        (192, 192, 192),# Srebrny
        (128, 128, 128),# Szary
        (128, 1, 1),    # Bordowy
        (128, 128, 1),  # Oliwkowy
        (1, 128, 1),    # Ciemnozielony
        (128, 1, 128),  # Purpurowy
        (1, 128, 128),  # Teal
        (1, 1, 128),    # Granatowy
        (255, 165, 1),  # Pomarańczowy
        (255, 192, 203),# Różowy
        (75, 1, 130),   # Indygo
        (240, 230, 140),# Khaki
        (173, 216, 230),# Jasnoniebieski
        (139, 69, 19)   # Brązowy
    ]

    if n > len(colors):
        colors.extend(generate_color_palette(n - len(colors)))

    return colors[:n]

