#!/bin/bash

set -e

# Check if required arguments are provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <experiment_name> <scene1> [scene2 scene3 ...]"
    echo "Example: $0 ablation1 scene1 scene2"
    exit 1
fi

experiment_name="$1"
shift # Remove first argument, leaving only scene names

echo "Experiment: $experiment_name"

output_folder="output/WAT/$experiment_name"

# Check if output folder exists
if [ ! -d "$output_folder" ]; then
    echo "Error: Output folder '$output_folder' does not exist"
    exit 1
fi

# If no scenes specified, process all scenes in the output folder
if [ "$#" -eq 0 ]; then
    echo "No specific scenes provided. Processing all scenes in $output_folder"
    scenes=("$output_folder"/*)  # Get all directories in output folder
    scenes=("${scenes[@]##*/}")  # Extract just the scene names from the full paths
else
    echo "Scenes to process: $@"
    scenes=("$@")
fi

# Process each scene
for scene in "${scenes[@]}"
do
    # Set the paths
    scene_output_path=$output_folder/$scene
    ckpt_best_path=$scene_output_path/chkpnt_best.pth
    modified_config_path=$scene_output_path/config.yaml
    
    # Check if the scene folder exists
    if [ ! -d "$scene_output_path" ]; then
        echo "Error: Scene output '$scene_output_path' does not exist"
        continue
    
    elif [ ! -f "$ckpt_best_path" ]; then
        echo "Scene $scene doesn't not have a chkpnt_best.pth file"
        continue
    else
        echo "Rendering and calculating metrics for scene $scene, output written to $scene_output_path"

        python render.py -m $scene_output_path --loaded_pth $ckpt_best_path
        python metrics.py -m $scene_output_path
    fi
done

echo "Done processing all WAT scenes"