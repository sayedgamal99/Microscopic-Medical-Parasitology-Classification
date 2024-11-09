import os
import subprocess
import zipfile
import sys
import json
import time

def print_colored(text, color="green"):
    """Print colored text for better visibility."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def check_kaggle_json():
    """Check if kaggle.json exists in the current directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    kaggle_json_path = os.path.join(current_dir, "kaggle.json")
    
    if not os.path.exists(kaggle_json_path):
        print_colored("\nERROR: kaggle.json not found in the current directory!", "red")
        print_colored("\nPlease follow these steps:", "yellow")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Scroll down to 'API' section")
        print("3. Click 'Create New API Token' to download kaggle.json")
        print(f"4. Place kaggle.json in this directory: {current_dir}")
        print("\nAfter placing the file, run this script again.")
        return False
    
    # Verify kaggle.json format
    try:
        with open(kaggle_json_path) as f:
            credentials = json.load(f)
            if 'username' not in credentials or 'key' not in credentials:
                raise ValueError("Invalid kaggle.json format")
            
            # Set environment variables for Kaggle
            os.environ['KAGGLE_USERNAME'] = credentials['username']
            os.environ['KAGGLE_KEY'] = credentials['key']
        return True
    except Exception as e:
        print_colored("\nERROR: Your kaggle.json file appears to be invalid!", "red")
        print("Please download a new copy from https://www.kaggle.com/account")
        return False

def setup_environment():
    """Setup the environment and install required packages."""
    try:
        print_colored("Installing kaggle package...", "blue")
        
        # Try installing without --user flag since we're in a virtual environment
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print_colored("Regular install failed, trying with --user flag...", "yellow")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "kaggle"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        # Verify installation
        try:
            import kaggle
            print_colored("Kaggle package installed successfully!", "green")
            return True
        except ImportError:
            print_colored("ERROR: Kaggle package installation verified failed.", "red")
            return False
            
    except Exception as e:
        print_colored(f"\nERROR: Failed to install Kaggle package. Try installing manually:", "red")
        print("Run: pip install kaggle")
        print(f"Error details: {str(e)}")
        return False

def download_dataset():
    """Download and extract the dataset."""
    # Configuration
    DATASET_OWNER = "sayedgamal99"
    DATASET_NAME = "microscopic-parasite-classifier"
    MODELS_DIR = "models"
    
    try:
        # Create models directory
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        print_colored("\nDownloading dataset...", "blue")
        # Download using kaggle API
        result = subprocess.run([
            "kaggle", "datasets", "download",
            "-d", f"{DATASET_OWNER}/{DATASET_NAME}",
            "-p", MODELS_DIR
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print_colored(f"Download failed: {result.stderr}", "red")
            print_colored("\nTrying alternative download method...", "yellow")
            
            # Alternative download method using Python API
            try:
                from kaggle.api.kaggle_api_extended import KaggleApi
                api = KaggleApi()
                api.authenticate()
                api.dataset_download_files(
                    f"{DATASET_OWNER}/{DATASET_NAME}",
                    path=MODELS_DIR,
                    unzip=True
                )
                print_colored("Download successful using Python API!", "green")
                return True
            except Exception as e:
                print_colored(f"Alternative download method failed: {str(e)}", "red")
                return False
            
        # Extract the dataset
        zip_path = os.path.join(MODELS_DIR, f"{DATASET_NAME}.zip")
        if os.path.exists(zip_path):
            print_colored("Extracting files...", "blue")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(MODELS_DIR)
            
            # Clean up
            os.remove(zip_path)
            return True
        else:
            print_colored("ERROR: Downloaded file not found!", "red")
            return False
            
    except Exception as e:
        print_colored(f"ERROR: {str(e)}", "red")
        return False

def main():
    print_colored("\n=== Kaggle Dataset Downloader ===\n", "blue")
    
    # Step 1: Check for kaggle.json
    print_colored("Step 1: Checking for kaggle.json...", "yellow")
    if not check_kaggle_json():
        return
    print_colored("✓ kaggle.json found and verified!", "green")
    
    # Step 2: Setup environment
    print_colored("\nStep 2: Setting up environment...", "yellow")
    if not setup_environment():
        return
    print_colored("✓ Environment setup complete!", "green")
    
    # Step 3: Download and extract dataset
    print_colored("\nStep 3: Downloading and extracting dataset...", "yellow")
    if not download_dataset():
        return
    print_colored("✓ Dataset downloaded and extracted successfully!", "green")
    
    print_colored("\n=== Download Complete! ===", "blue")
    print_colored("The model files are now available in the 'models' directory.", "green")

if __name__ == "__main__":
    main()