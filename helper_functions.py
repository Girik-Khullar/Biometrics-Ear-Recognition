from pyunpack import Archive
import os
import shutil
from sklearn.model_selection import train_test_split

def extract_rar(rar_path, extract_to):
    """
    Extracts a RAR file to a specified directory.

    Args:
    - rar_path (str): The path to the RAR file.
    - extract_to (str): The directory where the contents should be extracted.

    Ensures the output directory exists, creates it if not, and then
    uses pyunpack to extract the RAR file's contents into this directory.

    Example usage:
    --------------
    rar_file_path = 'path/to/your/file.rar'  # Change this to the path of your RAR file
    output_directory = 'path/to/extract'     # Change this to your desired output directory
    extract_rar(rar_file_path, output_directory)
    """
    # Ensure the output directory exists
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    # Use pyunpack to extract the RAR file
    Archive(rar_path).extractall(extract_to)
    print(f"Extracted: {rar_path} to {extract_to}")

def split_dataset(image_path, train_path, test_path, valid_path):
    """
    Split dataset into training, testing, and validation sets.

    This function takes the path to a directory containing class subdirectories,
    each filled with images, and splits these images into training, validation,
    and testing sets according to specified ratios. The images are then copied
    into corresponding directories for each set.

    Args:
    - image_path (str): Path to the directory containing the class subdirectories.
    - train_path (str): Path where the training set images will be stored.
    - test_path (str): Path where the testing set images will be stored.
    - valid_path (str): Path where the validation set images will be stored.

    Example usage:
    --------------
    ```python
    image_path = 'path/to/your/dataset'  # Adjust to your dataset's path
    train_path = 'path/to/train_set'
    test_path = 'path/to/test_set'
    valid_path = 'path/to/valid_set'

    split_dataset(image_path, train_path, test_path, valid_path)
    ```
    """

    # Create directories for the split if they do not exist
    for dir in [train_path, test_path, valid_path]:
        os.makedirs(dir, exist_ok=True)

    # Process each class directory
    for class_name in os.listdir(image_path):
        class_dir = os.path.join(image_path, class_name)

        # Ensure we're dealing with a directory
        if not os.path.isdir(class_dir):
            continue

        images = [os.path.join(class_dir, f) for f in os.listdir(class_dir) if os.path.isfile(os.path.join(class_dir, f))]
        train_imgs, test_imgs = train_test_split(images, test_size=20, random_state=42)  # Split into train and temp (test+val)
        val_imgs, test_imgs = train_test_split(test_imgs, test_size=10, random_state=42)  # Split temp into val and test

        # Function to copy files to their new location
        def copy_files(files, dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
            for f in files:
                shutil.copy(f, dest_dir)

        # Copy the files to their new directories
        copy_files(train_imgs, os.path.join(train_path, class_name))
        copy_files(val_imgs, os.path.join(valid_path, class_name))
        copy_files(test_imgs, os.path.join(test_path, class_name))

    print("Dataset split complete.")

def walk_through_dir(dir_path):
    """
    Walks through dir_path returning its contents.
    Args:
    dir_path (str): target directory

    Returns:
    A print out of:
      number of subdiretories in dir_path
      number of images (files) in each subdirectory
      name of each subdirectory
    
    Example usage:
    --------------
    dir_path = "/path/of/your/directory"
    walk_through_dir(dir_path)
    """
    for dirpath, dirnames, filenames in os.walk(dir_path):
        print(f"There are {len(dirnames)} directories and {len(filenames)} images in '{dirpath}'.")