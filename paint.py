import os
import subprocess


# Function to apply color relief using gdaldem
def apply_color_relief(input_path, output_path, color_table_path):
    # Construct the gdaldem color-relief command
    command = ["gdaldem", "color-relief", input_path, color_table_path, output_path]

    try:
        # Run the command using subprocess
        subprocess.run(command, check=True)
        print(f"Colorized slope saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_path}: {e}")


# Function to process all .tif files in the input directory
def process_all_slope_files(input_directory, output_directory, color_table_path):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process all .tif files in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".tif"):
            input_path = os.path.join(input_directory, file_name)
            output_file_name = f"{os.path.splitext(file_name)[0]}_painted.tif"
            output_path = os.path.join(output_directory, output_file_name)

            # Apply color relief using gdaldem and save the result
            apply_color_relief(input_path, output_path, color_table_path)


# Step 1: Specify directories and call the function to process all slope files
input_directory = "./sloped"  # Directory containing the slope .tif files
output_directory = "./painted"  # Directory to save the colorized .tif files
color_table_path = "color_table.txt"  # Path to the color table

# Process all slope files and apply color relief
process_all_slope_files(input_directory, output_directory, color_table_path)
