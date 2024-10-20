import yaml
import argparse
import os
import shutil

def modify_yaml_config(input_path, output_path, modifications):
    # First, copy the original config file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    shutil.copy2(input_path, output_path)
    
    # Read the copied YAML file
    with open(output_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Apply modifications
    changes_made = False
    for mod in modifications.split():
        key, value = mod.split('=')
        keys = key.split('.')
        current = config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        # Try to convert value to appropriate type
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        else:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
        if current[keys[-1]] != value:
            current[keys[-1]] = value
            changes_made = True
    
    # Update the output path in the YAML config
    if 'ModelParams' in config and 'model_path' in config['ModelParams']:
        new_path = os.path.dirname(output_path)
        if config['ModelParams']['model_path'] != new_path:
            config['ModelParams']['model_path'] = new_path
            changes_made = True
    
    # If changes were made, write the modified config back to the file
    if changes_made:
        with open(output_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False, sort_keys=False)
        print(f"Modified config saved to {output_path}")
    else:
        print(f"No changes were necessary. Original config copied to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Modify YAML config for ablation experiments")
    parser.add_argument("--input", required=True, help="Path to the original YAML config")
    parser.add_argument("--output", required=True, help="Path to save the modified YAML config")
    parser.add_argument("--mod", required=True, help="Modifications as a space-separated string of key=value pairs")
    
    args = parser.parse_args()
    
    modify_yaml_config(args.input, args.output, args.mod)

if __name__ == "__main__":
    main()