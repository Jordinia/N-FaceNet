import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

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

def get_dominant_color(image_path, k=3):
    """
    Determines the dominant color in an image using K-means clustering and finds the closest matching predefined color.
    Parameters:
    image_path (str): The file path to the image.
    k (int): The number of clusters to form in K-means clustering. Default is 3.
    Returns:
    tuple: A tuple containing the name of the closest matching predefined color (str), its ID (int), and the RGB values of the dominant color (numpy.ndarray).
    """
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize image to speed up processing
    image = cv2.resize(image, (100, 100))
    
    # Reshape the image to be a list of pixels
    pixels = image.reshape((-1, 3))
    
    # Perform K-means clustering
    clt = KMeans(n_clusters=k)
    clt.fit(pixels)
    
    # Find the most frequent cluster
    unique, counts = np.unique(clt.labels_, return_counts=True)
    dominant_cluster = unique[np.argmax(counts)]
    dominant_color = clt.cluster_centers_[dominant_cluster]
    
    # Find the closest predefined color
    min_distance = float('inf')
    closest_color_name = None
    closest_color_id = None
    for name, info in colors.items():
        distance = np.linalg.norm(dominant_color - np.array(info['rgb']))
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name
            closest_color_id = info['id']
    
    return closest_color_name, closest_color_id, dominant_color

# Example usage
color_name, color_id, rgb = get_dominant_color('outfit/contoh/Person_1_top.jpg')
print(f"Dominant Color: {color_name} ID: {color_id}")