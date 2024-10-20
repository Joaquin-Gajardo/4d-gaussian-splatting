#!/bin/bash

set -e

# Check if required arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <experiment_name> <mod_args>"
    echo "Example: $0 ablation1 \"gaussian_dim=8 OptimizationParams.iterations=50000\""
    exit 1
fi

experiment_name="$1"
mod_args="$2"

echo $experiment_name
echo $mod_args

echo "Processing all WAT scenes"
dataset_folder="../../data/WAT"
output_folder="output/WAT/$experiment_name"

for input_folder in "$dataset_folder"/*
do
    scene=$(basename "$input_folder")

    # Set the paths
    scene_output_path=$output_folder/$scene
    modified_config_path=$scene_output_path/config.yaml
    
    mkdir -p $scene_output_path
    
    ckpt_best_path=$scene_output_path/chkpnt_best.pth
    if [ ! -d $ckpt_best_path ]; then
        echo "Processing scene $scene, output written to $scene_output_path"

        # Append the input folder to mod_args (if we have the dataset somewhere else)
        scene_mod_args="$mod_args ModelParams.source_path=$input_folder"

        # Modify the YAML config
        python scripts/modify_yaml_configs.py --input "configs/WAT/$scene.yaml" \
                                              --output "$modified_config_path" \
                                              --mod "$scene_mod_args"

        #Use the modified config
        python train.py --config $modified_config_path
        python render.py -m $scene_output_path --loaded_pth $ckpt_best_path
        python metrics.py -m $scene_output_path
    else
        echo "Scene $scene is already processed in $scene_output_path"
    fi
done

echo "Done processing all WAT scenes"