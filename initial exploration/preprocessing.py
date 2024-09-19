import os
import rasterio
import numpy as np
from scipy.ndimage import median_filter
import matplotlib.pyplot as plt

def preprocess_input_image(input_image_path):
    # Get the absolute path to the input image
    input_image_path = os.path.join(os.path.dirname(__file__), "dataset", input_image_path)

    # Open the input image file
    with rasterio.open(input_image_path) as src:
        # Read the image data (bands)
        bands = src.read()
        # Close the file (we have already read the data)
        src.close()

    # Apply median filter to each band of the image
    preprocessed_bands = []
    for band in bands:
        # Apply median filter with a window size of 3x3
        filtered_band = median_filter(band, size=3)
        preprocessed_bands.append(filtered_band)

    # Convert the preprocessed bands to a NumPy array
    preprocessed_image = np.stack(preprocessed_bands, axis=0)

    # Prepare metadata for the preprocessed image
    metadata = src.meta.copy()

    return preprocessed_image, metadata
def visualize_image(image, cmap='gray'):
    # Check if image has multiple bands
    if len(image.shape) == 3:
        # Plot each band separately
        fig, axes = plt.subplots(1, image.shape[0], figsize=(15, 5))
        for ax, band in zip(axes, image):
            ax.imshow(band, cmap=cmap)
            ax.axis('off')
        plt.show()
    else:
        # Plot single-band image
        plt.imshow(image, cmap=cmap)
        plt.axis('off')
        plt.show()


# Example usage:
input_image_filename = "beforeFlood.tif"  # Replace with the actual filename
preprocessed_image, metadata = preprocess_input_image(input_image_filename)

# Visualize the preprocessed image
visualize_image(preprocessed_image)
