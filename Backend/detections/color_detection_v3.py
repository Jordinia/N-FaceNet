import cv2
import numpy as np
from skimage import color

# Define the color names with their corresponding RGB values and IDs
colors = {
    'red': {'id': 0, 'rgb': (255, 0, 0)},
    'blue': {'id': 1, 'rgb': (0, 0, 255)},
    'green': {'id': 2, 'rgb': (0, 255, 0)},
    'yellow': {'id': 3, 'rgb': (255, 255, 0)},
    'black': {'id': 4, 'rgb': (0, 0, 0)},
    'white': {'id': 5, 'rgb': (255, 255, 255)},
    'gray': {'id': 6, 'rgb': (128, 128, 128)},
    'beige': {'id': 7, 'rgb': (245, 245, 220)},
    'brown': {'id': 8, 'rgb': (165, 42, 42)},
    'purple': {'id': 9, 'rgb': (128, 0, 128)},
    'orange': {'id': 10, 'rgb': (255, 165, 0)}
}

outfit = {
    'bottom': {'id': 0, 'rgb': (255, 0, 0)},
    'dress': {'id': 1, 'rgb': (0, 0, 255)},
    'top': {'id': 2, 'rgb': (0, 255, 0)}
}

def get_dominant_color(image, k=4):
    """
    Determines the dominant color in an image using K-means clustering and visualizes the result.

    Parameters:
        image (str or numpy.ndarray): Image file path or image array.
        k (int): Number of clusters for K-means clustering.

    Returns:
        tuple: (color_name, color_id, dominant_color_rgb)
    """
    def rgb_to_lab(rgb):
        """Convert RGB to LAB color space."""
        rgb = np.array(rgb, dtype=np.uint8).reshape(1, 1, 3)
        lab = color.rgb2lab(rgb / 255.0)
        return lab[0, 0]

    # Check if input is a file path or image array
    if isinstance(image, str):
        # Load and resize the image from file path
        image = cv2.imread(image)
    elif not isinstance(image, np.ndarray):
        raise ValueError("Input must be a file path or an image array.")

    # Resize the image for faster processing
    image = cv2.resize(image, (300, 300))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape image to a 2D array of pixels
    pixels = image_rgb.reshape(-1, 3)
    pixels = np.float32(pixels)

    # Define criteria and apply K-means clustering
    criteria = (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 100, 0.2)
    _, labels, palette = cv2.kmeans(
        pixels, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS
    )

    # Find the most frequent cluster
    counts = np.bincount(labels.flatten())
    dominant_color = palette[np.argmax(counts)].astype(int)

    # Convert dominant color to LAB
    dominant_color_lab = rgb_to_lab(dominant_color)

    # Find the closest predefined color using CIEDE2000
    min_distance = float('inf')
    closest_color_name = None
    closest_color_id = None
    for name, info in colors.items():
        color_lab = rgb_to_lab(info['rgb'])
        distance = color.deltaE_ciede2000(dominant_color_lab, color_lab)
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name
            closest_color_id = info['id']

    return closest_color_name, closest_color_id, dominant_color

# TESTING
# Example usage with image path
# image_path = input("Enter the path to the image file: ")
# color_name, color_id, rgb = get_dominant_color(image_path)
# print(f"Dominant Color: {color_name}, ID: {color_id}, RGB: {rgb}")

# Example usage with image array (e.g., outfit_crop from outfit_detection.py)
# Assuming 'outfit_crop' is a NumPy array of the cropped image
# color_name, color_id, rgb = get_dominant_color(outfit_crop)
# print(f"Dominant Color: {color_name}, ID: {color_id}")