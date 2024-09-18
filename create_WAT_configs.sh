# Path to the template file
TEMPLATE_FILE="breville.yaml"

# Directory containing the scene folders
DATA_DIR="data/WAT"

# Directory to store the output YAML files
OUTPUT_DIR="configs/WAT"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through each subdirectory in the data folder
for scene in "$DATA_DIR"/*; do
    if [ -d "$scene" ]; then
        scene_name=$(basename "$scene")
        if [ "$scene_name" = "breville" ]; then
            continue
        fi
        template_file="$OUTPUT_DIR/$TEMPLATE_FILE"
        output_file="$OUTPUT_DIR/${scene_name}.yaml"
        echo $output_file

        # Copy the template file
        cp "$template_file" "$output_file"

        # Modify the source_path and model_path
        sed -i "s|source_path: .*|source_path: \"data/WAT/$scene_name\"|" "$output_file"
        sed -i "s|model_path: .*|model_path: \"output/WAT/$scene_name\"|" "$output_file"

        echo "Created and modified $output_file"
    fi
done

echo "YAML file creation and modification complete."