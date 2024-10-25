
import os
import yaml

# Attempt to use the faster CLoader for YAML loading; fall back to the safe Loader if not available.
try:
    from yaml import CLoader as Loader
    print("Using libyaml for faster YAML processing.")
except ImportError:
    from yaml import SafeLoader as Loader
    print("Falling back to pyyaml's SafeLoader.")

    
# Define the directory and file name
cwd = ""
filename = 'Configuration.yml'
config_path = os.path.join(cwd, filename)

# Function to load YAML configuration
def load_config(filepath):
    if not os.path.exists(filepath):
        print(f"Configuration file not found: {filepath}")
        return None
    
    try:
        with open(filepath, 'r') as file:
            return yaml.load(file, Loader=Loader)
    except yaml.YAMLError as exc:
        print(f"Error in configuration file: {exc}")
        return None
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        return None
    
# Load the configuration
config_data = load_config(config_path)

if config_data:
    try:
        # Extract configuration data
        alpha = config_data['Portfolio_Configuration']['Risk_Tolerance']
        historical_horizon = config_data['Portfolio_Configuration']['Historical_Days']
        start_day = config_data['Portfolio_Configuration']['Seed']
        capital = config_data['Portfolio_Configuration']['Capital']
        trade_horizon = config_data['Portfolio_Configuration']['Holding_Period']
        tickers = config_data['Portfolio_Configuration']['Inputs_Parameters']['Tickers']
        data_file = config_data['Portfolio_Configuration']['File path']

        # Print or use the extracted data
        print("Configuration loaded successfully.")
        print("Alpha:", alpha)
    except KeyError as e:
        print(f"Error reading config data: {e}")

else:
    print("Failed to load configuration.")




