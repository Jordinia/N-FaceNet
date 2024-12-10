import cv2
import numpy as np
from skimage import color
from cuml.cluster import KMeans as cuKMeans

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

# Precompute LAB values for predefined colors
predefined_colors_lab = {}
for name, info in colors.items():
    rgb = np.array(info['rgb'], dtype=np.uint8).reshape(1, 1, 3)
    lab = color.rgb2lab(rgb / 255.0)
    predefined_colors_lab[name] = {
        'id': info['id'],
        'lab': lab[0, 0]
    }

def get_dominant_color(image, k=5):
    """
    Determines the dominant color in an image using GPU-accelerated K-Means clustering.

    Parameters:
        image (numpy.ndarray): Image array in BGR format.
        k (int): Number of clusters for K-Means clustering.

    Returns:
        tuple: (color_name, color_id, dominant_color_rgb)
    """

    # Resize the image for faster processing
    image = cv2.resize(image, (100, 100))  # Reduced size for performance
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape image to a 2D array of pixels
    pixels = image_rgb.reshape(-1, 3).astype(np.float32)

    # Use GPU-accelerated KMeans from RAPIDS cuML
    kmeans = cuKMeans(n_clusters=k, max_iter=100, init="k-means++", random_state=42)

    # Fit the model to the pixels
    kmeans.fit(pixels)

    # Get cluster centers and labels
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_

    # Find the most frequent cluster
    unique_labels, counts = np.unique(labels, return_counts=True)
    dominant_cluster = unique_labels[np.argmax(counts)]
    dominant_color = cluster_centers[dominant_cluster].astype(int)

    # Convert dominant color to LAB
    dominant_color_rgb = dominant_color.reshape(1, 1, 3).astype(np.uint8)
    dominant_color_lab = color.rgb2lab(dominant_color_rgb / 255.0)[0, 0]

    # Find the closest predefined color using CIEDE2000
    min_distance = float('inf')
    closest_color_name = None
    closest_color_id = None
    for name, info in predefined_colors_lab.items():
        color_lab = info['lab']
        distance = color.deltaE_ciede2000(dominant_color_lab, color_lab)
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name
            closest_color_id = info['id']

    return closest_color_name, closest_color_id, dominant_color_rgb[0, 0]

# # TESTING
# # Example usage with image path
# image = input("Enter the path to the image file: ")
# image = cv2.imread(image)
# color_name, color_id, rgb = get_dominant_color(image)
# print(f"Dominant Color: {color_name}, ID: {color_id}, RGB: {rgb}")

# Example usage with image array (e.g., outfit_crop from outfit_detection.py)
# Assuming 'outfit_crop' is a NumPy array of the cropped image
# color_name, color_id, rgb = get_dominant_color(outfit_crop)
# print(f"Dominant Color: {color_name}, ID: {color_id}")