import os
import subprocess

# Step 1: Process all TIFF files in the input directory and apply gdaldem slope
def generate_slope(input_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop over each file in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".tif"):  # Only process TIFF files
            input_file = os.path.join(input_directory, file_name)  # Full path to the input file
            output_file = os.path.join(output_directory, f"{os.path.splitext(file_name)[0]}_slope.tif")  # Output path

            # Construct the gdaldem slope command
            command = ["gdaldem", "slope", input_file, output_file, "-s", "111120"]

            try:
                # Run the command using subprocess
                subprocess.run(command, check=True)
                print(f"Slope generated: {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_file}: {e}")

# Step 2: Specify the directories and call the function
input_directory = "./converted"  # Directory containing the .tif files (input)
output_directory = "./sloped"  # Directory where slope results will be saved

# Ensure the output directory exists
if not os.path.exists(output_directory):
    print(f"Creating output directory: {output_directory}")
    os.makedirs(output_directory)

# Call the function to process files
generate_slope(input_directory, output_directory)
