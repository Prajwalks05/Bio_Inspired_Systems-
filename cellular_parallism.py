from google.colab import files
import cv2
import numpy as np
from collections import Counter
from google.colab.patches import cv2_imshow

# Step 1: Upload image
uploaded = files.upload()  # This will open a file picker
image_path = list(uploaded.keys())[0]  # Get the uploaded filename

# Read the uploaded image in color
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Failed to load image. Make sure the file is an image.")

# Noise reduction functions
def get_neighborhood(grid, x, y):
    neighbors = []
    rows, cols = grid.shape
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = (x + dx) % rows
            ny = (y + dy) % cols
            neighbors.append(grid[nx, ny])
    return neighbors

def noise_reduction_update(pixel, neighbors):
    from collections import Counter
    counts = Counter(neighbors)
    majority_value = counts.most_common(1)[0][0]
    return majority_value

def run_pca_noise_reduction_color(color_image, steps=3):
    """
    Denoises a color image by applying single-channel noise reduction to each channel.

    Args:
        color_image: A NumPy array representing the color image (height, width, 3).
        steps: The number of noise reduction steps to apply to each channel.

    Returns:
        A NumPy array representing the denoised color image.
    """
    if color_image.shape[-1] != 3:
        raise ValueError("Input image must be a 3-channel color image.")

    # Split the color image into individual channels
    channels = cv2.split(color_image)
    denoised_channels = []

    # Apply noise reduction to each channel
    for channel in channels:
        # The original run_pca_noise_reduction function is applied to each channel
        denoised_channel = run_pca_noise_reduction(channel, steps=steps)
        denoised_channels.append(denoised_channel)

    # Merge the denoised channels back into a color image
    denoised_color = cv2.merge(denoised_channels)

    return denoised_color

# Apply noise reduction to the color image with 100 iterations
denoised_color_image = run_pca_noise_reduction_color(image, steps=10)

# Display images
print("Original Color Image:")
cv2_imshow(image) # Display the original color image
print("Denoised Color Image:")
cv2_imshow(denoised_color_image) # Display the denoised color image
