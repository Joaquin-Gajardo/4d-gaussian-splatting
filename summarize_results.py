import json
import os

import pandas as pd

def summarize_results(base_folder):
    # List to store results
    results = []

    # Iterate through each subfolder in the base folder
    for scene_folder in os.listdir(base_folder):
        scene_path = os.path.join(base_folder, scene_folder)

        # Skip if scene folder ends with a number (e.g. "scene2"), assumes final runs are without numbers
        if scene_path[-1].isdigit():
            continue
        
        # Check if it's a directory
        if os.path.isdir(scene_path):
            json_path = os.path.join(scene_path, 'results.json')
            
            # Check if the JSON file exists
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data = json.load(f)
                
                # Extract mean values
                data = data.get('ours_None', {})
                result = {
                    'Scene': scene_folder,
                    'PSNR': data.get('PSNR', 'N/A'),
                    'SSIM': data.get('SSIM', 'N/A'),
                    'LPIPS (vgg)': data.get('LPIPS', 'N/A')
                }
                results.append(result)
            else:
                print(f"Warning: No JSON file found for scene {scene_folder}")

    # Create a DataFrame
    df = pd.DataFrame(results).sort_values('Scene')

    # Calculate overall mean
    mean_row = pd.DataFrame({
        'Scene': ['Overall Mean'],
        'PSNR': [df['PSNR'].mean()],
        'SSIM': [df['SSIM'].mean()],
        'LPIPS (vgg)': [df['LPIPS (vgg)'].mean()]
    })

    # Concatenate the mean row to the original DataFrame
    df = pd.concat([df, mean_row], ignore_index=True)

    # Set 'Scene' as index for better display
    df.set_index('Scene', inplace=True)

    return df

#base_folder = "output/N3V"
base_folder = "output/WAT-fullres"
summary_table = summarize_results(base_folder)

print(summary_table.to_string())

#summary_table.to_csv("dynerf_realtime4DGS_results_summary.csv")
summary_table.to_csv("WAT_realtime4DGS-fullres_results_summary.csv")