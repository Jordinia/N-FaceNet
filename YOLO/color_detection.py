import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Define the color names and their corresponding RGB values
colors = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'beige': (245, 245, 220),
    'brown': (165, 42, 42),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0)
}

def get_dominant_color(image_path, k=3):
    """
    Determines the dominant color in an image using K-means clustering and finds the closest matching predefined color.
    Parameters:
    image_path (str): The file path to the image.
    k (int): The number of clusters to form in K-means clustering. Default is 3.
    Returns:
    tuple: A tuple containing the name of the closest matching predefined color (str) and the RGB values of the dominant color (numpy.ndarray).
    The function performs the following steps:
    1. Loads the image using OpenCV and converts it to RGB format.
    2. Optionally resizes the image to speed up processing.
    3. Reshapes the image to a list of pixels.
    4. Applies K-means clustering to the pixels.
    5. Identifies the dominant color as the largest cluster.
    6. Finds the closest matching predefined color to the dominant color.
    7. Displays the resized image and the dominant color.
    """
    # Load image using OpenCV (BGR format)
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Resize image to speed up the process (optional)
    image_rgb_resized = cv2.resize(image_rgb, (200, 200))

    # Step 1: Reshape the image to be a list of pixels
    pixels = image_rgb_resized.reshape(-1, 3)

    # Step 2: Apply K-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)

    # Step 3: Find the dominant color (largest cluster)
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_

    # Count the number of pixels in each cluster
    unique, counts = np.unique(labels, return_counts=True)
    dominant_cluster = unique[np.argmax(counts)]  # Cluster with the most pixels
    dominant_color = cluster_centers[dominant_cluster]

    print(f"Dominant RGB color: {dominant_color}")

    # Step 4: Find the closest matching predefined color
    closest_color_name = None
    min_distance = float('inf')
    for color_name, color_value in colors.items():
        distance = np.linalg.norm(np.array(dominant_color) - np.array(color_value))
        if distance < min_distance:
            min_distance = distance
            closest_color_name = color_name

    # Show the original image and the dominant color
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    axs[0].imshow(image_rgb_resized)
    axs[0].set_title("Resized Image")
    axs[0].axis('off')

    axs[1].imshow([[dominant_color.astype(int)]])
    axs[1].set_title(f"Dominant Color: {closest_color_name}")
    axs[1].axis('off')

    plt.show()

    return closest_color_name, dominant_color

# Example usage
image_path = 'input12.jpg'  # Replace with your image file
dominant_color_name, dominant_color_value = get_dominant_color(image_path)
print(f"The dominant color is {dominant_color_name} (RGB: {dominant_color_value})")
