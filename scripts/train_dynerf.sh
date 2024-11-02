#!/bin/bash

run_commands() {
    local scene=$1
    local gpu=$2

    export CUDA_VISIBLE_DEVICES=$gpu
    python train.py --config configs/dynerf/${scene}.yaml
}

# Start initial trainings and store their process ids
run_commands "cook_spinach" 0 &
pid_gpu0=$!  
run_commands "flame_steak" 1 &
pid_gpu1=$!

# Function to wait for the first job to finish
wait_for_first_to_finish() {
    while true; do
        if ! kill -0 $pid_gpu0 2>/dev/null; then
            # GPU 0 finished first
            echo 0 
            return
        elif ! kill -0 $pid_gpu1 2>/dev/null; then
            # GPU 1 finished first
            echo 1
            return
        fi
        sleep 5
    done
}

# Wait for the first job to finish
free_gpu=$(wait_for_first_to_finish)
echo "GPU ${free_gpu} is now free, starting another training"

run_commands "cut_roasted_beef" $free_gpu &

wait