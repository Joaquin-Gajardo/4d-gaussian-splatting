#set -e 
echo "Processing all WAT scenes"
base_folder="/workspace/4d-gaussian-splatting"
dataset_folder="$base_folder/data/WAT"
#export CUDA_VISIBLE_DEVICES=0
for input_folder in "$dataset_folder"/*
do
    scene=$(basename $input_folder)
    output_path="$base_folder/output/WAT-fullres/$scene"
    # Check if the date has already been processed
    if [ ! -d $output_path ]; then
        echo "Processing scene $scene, output written to $output_path"
        python train.py --config configs/WAT/$scene.yaml
        python render.py -m $output_path --loaded_pth $output_path/chkpnt_best.pth --skip_train
        python metrics.py -m $output_path
    else
        echo "Scene $scene is already processed on $output_path"
    fi
done
echo "Done processing all WAT scenes"