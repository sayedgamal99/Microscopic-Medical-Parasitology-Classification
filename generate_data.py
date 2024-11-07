import os
import zipfile
import shutil
import random
from pathlib import Path
from PIL import Image

def sample_validation_data(zip_path='validation_data.zip', output_dir='data_samples', samples_per_class=5):
    """
    Extract samples from validation data, resize to 224x224, and save them with class names
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create temporary directory for extraction
    temp_dir = 'temp_extract'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    try:
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Process each class directory
        for class_dir in os.listdir(temp_dir):
            
            # Get all files in the class directory
            class_path = os.path.join(temp_dir, class_dir)
            files = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
            
            # Sample files
            if files:
                num_samples = min(samples_per_class, len(files))
                sampled_files = random.sample(files, num_samples)
                
                # Copy, resize, and rename files
                for i, file_name in enumerate(sampled_files):
                    # Get file extension
                    ext = os.path.splitext(file_name)[1]
                    
                    # Create new file name with class
                    new_name = f"{class_dir}_{i+1}{ext}"
                    
                    # Open, resize, and save image
                    src = os.path.join(class_path, file_name)
                    dst = os.path.join(output_dir, new_name)
                    
                    with Image.open(src) as img:
                        img_resized = img.resize((224, 224), Image.LANCZOS)
                        img_resized.save(dst)
                
                print(f"Sampled and resized {num_samples} images from {class_dir}")
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    sample_validation_data(samples_per_class=5)
    print("Sampling and resizing completed!")