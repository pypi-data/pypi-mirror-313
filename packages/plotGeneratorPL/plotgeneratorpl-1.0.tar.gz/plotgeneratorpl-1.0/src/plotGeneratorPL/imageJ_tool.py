import os
import cv2
import numpy as np
import pandas as pd
from .utils import (get_user_input, get_directory, get_filename)


__all__ = [
    "color_change",
    "batch_process_images",
    "divide_and_measure_intensity",
    "process_images_and_save_intensity",
    "image_processing"
    ]


def color_change(input_path: str, output_path: str, color: str,
                 threshold: int = 150):
    """
    Processes a single TIFF image by changing the bright parts to the specified
    color and
    saving the result.
    Args:
        input_path (str): Path to the input TIFF image.
        output_path (str): Path to save the processed image.
        color (str): The target color for bright areas.
        threshold (int): The brightness threshold to determine bright areas.
    """
    try:
        # Load the image in grayscale
        img_gray = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        if img_gray is None:
            print(f"Error: Could not open image at path: {input_path}")
            return

        # Create a mask for bright regions
        _, mask = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)

        # Create an empty RGB image with the same height and width as the
        # original grayscale image
        height, width = img_gray.shape
        img_rgb = np.zeros((height, width, 3), dtype=np.uint8)

        # Define the color mapping
        color_map = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0)
        }
        # Default to green if invalid
        target_color = color_map.get(color.lower(), (0, 255, 0))

        # Apply the color to the bright areas using the mask
        img_rgb[mask > 0] = target_color

        # Save the resulting image
        cv2.imwrite(output_path, img_rgb)
        print(f"Processed image saved to: {output_path}")

    except Exception as e:
        print(f"Failed to process the image: {input_path}")
        print(f"Error: {e}")


def batch_process_images(input_dir: str, output_dir: str, color: str,
                         threshold: int = 150):
    """
    Batch processes TIFF images in the input directory by changing bright
    parts to the specified color and saves the results.
    Args:
        input_dir (str): Directory containing the input images.
        output_dir (str): Directory to save the processed images.
        color (str): The target color for all images.
        threshold (int): The brightness threshold to determine bright areas.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.tiff', '.tif')):
            input_path = os.path.join(input_dir, filename)
            base_name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir,
                                       f"{base_name}_{color.lower()}{ext}")
            color_change(input_path, output_path, color, threshold)


def divide_and_measure_intensity(image_path: str):
    """
    Divides the image into three equal vertical parts and calculates the
    average intensity for each part.
    Args:
        image_path (str): Path to the input image.
    Returns:
        list: A list containing average intensities of the top, middle, and
        bottom parts.
    """
    # Load the image in grayscale
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        print(f"Error: Could not open image at path: {image_path}")
        return [None, None, None]

    # Get the dimensions of the image
    height, width = img_gray.shape

    # Divide the image into three equal vertical parts
    part_height = height // 3

    # Calculate the average intensity for each part
    top_intensity = np.mean(img_gray[0:part_height, :])
    middle_intensity = np.mean(img_gray[part_height:2*part_height, :])
    bottom_intensity = np.mean(img_gray[2*part_height:height, :])

    return [top_intensity, middle_intensity, bottom_intensity]


def process_images_and_save_intensity(input_dir: str, output_excel_path: str):
    """
    Processes all TIFF images in a directory, calculates the average intensity
    of three equal parts, and saves results to an Excel file.
    Args:
        input_dir (str): Directory containing the input images.
        output_excel_path (str): Path to save the Excel file with intensity
        measurements.
    """
    # Initialize a dictionary to store intensity data
    intensity_data = {}

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.tiff', '.tif')):
            image_path = os.path.join(input_dir, filename)
            intensities = divide_and_measure_intensity(image_path)

            # Store the intensity values in the dictionary
            intensity_data[filename.rsplit('.', 1)[0]] = intensities

    # Convert dictionary to a DataFrame
    df = pd.DataFrame(intensity_data, index=["Top Part Intensity",
                                             "Middle Part Intensity",
                                             "Bottom Part Intensity"])

    # Save the DataFrame to an Excel file
    df.to_excel(output_excel_path, index=True)
    print(f"Saved intensity data to: {output_excel_path}")


def image_processing():
    """
    Allows the user to choose between changing the color of images or
    calculating intensity deviations.
    """
    print("\nChoose the image processing method:")
    print("1. Change color of fluorescence images")
    print("2. Get intensity standard deviation of images")

    choice = get_user_input("Enter the number corresponding to your choice: ",
                            int)

    # Get the directory containing images
    input_dir = "Directory containing the images to process: "
    input_dir = get_directory(input_dir)

    if choice == 1:
        # Change color of images
        output_dir = get_directory("Directory to save the processed images: ")

        # Ask for the color change option
        print("\nChoose a target color:")
        print("1. Red")
        print("2. Green")
        print("3. Blue")
        color = get_user_input("Enter the number of your choice:",
                               int)
        color_map = {1: "red", 2: "green", 3: "blue"}
        color = color_map.get(color, "green")  # Default to green if invalid

        # Ask for the threshold value
        threshold = get_user_input("Enter the brightness threshold: ", int)

        # Confirm action
        print("\nSummary of Inputs:")
        print(f"Input Directory: {input_dir}")
        print(f"Output Directory: {output_dir}")
        print(f"Target Color: {color.capitalize()}")
        print(f"Brightness Threshold: {threshold}")

        confirm = get_user_input("Proceed? (yes/no): ").strip().lower()
        if confirm == "yes":
            batch_process_images(input_dir, output_dir, color, threshold)
            print("\nImage processing completed successfully!")
        else:
            print("\nOperation cancelled.")

    elif choice == 2:
        # Get intensity measurements and save to Excel
        output_excel = "Enter file name to save results (e.g., results.xlsx): "
        output_excel = get_filename(output_excel)
        saveDir = get_directory("Enter the directory to save the file: ")
        savePath = os.path.join(saveDir, output_excel)
        # Confirm action
        print("\nSummary of Inputs:")
        print(f"Input Directory: {input_dir}")
        print(f"Output Excel File: {output_excel}")

        confirm = get_user_input("Proceed? (yes/no): ").strip().lower()
        if confirm == "yes":
            process_images_and_save_intensity(input_dir, savePath)
            print("\nIntensity calculation completed successfully!")
        else:
            print("\nOperation cancelled.")

    else:
        print("Invalid choice. Please enter 1 or 2.")
