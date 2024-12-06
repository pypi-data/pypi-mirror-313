import os
import pandas as pd
import pyarrow as pa
import lance
import time
from tqdm import tqdm
from PIL import Image
import io

# Function to process images with or without splits
def process_images(images_folder, schema, splits=None, resize=None):
    # If splits are defined, process them accordingly
    if splits:
        for split in splits:
            split_folder = os.path.join(images_folder, split)
            
            # Check if the split folder exists
            if not os.path.exists(split_folder):
                print(f"Warning: The {split} folder does not exist. Skipping...")
                continue
            
            # Iterate over the categories (subfolders) within each split
            for label in os.listdir(split_folder):
                label_folder = os.path.join(split_folder, label)
                
                # Ensure it's a directory (i.e., category)
                if not os.path.isdir(label_folder):
                    continue
                
                # Iterate over the images within each label
                for filename in tqdm(os.listdir(label_folder), desc=f"Processing {split} - {label}"):
                    image_path = os.path.join(label_folder, filename)

                    # Read and convert the image to a binary format
                    with open(image_path, 'rb') as f:
                        binary_data = f.read()

                    # Optional resizing or preprocessing
                    if resize:
                        image = Image.open(io.BytesIO(binary_data))
                        image = image.resize(resize)
                        with io.BytesIO() as img_byte_arr:
                            image.save(img_byte_arr, format="JPEG")
                            binary_data = img_byte_arr.getvalue()

                    image_array = pa.array([binary_data], type=pa.binary())
                    filename_array = pa.array([filename], type=pa.string())
                    label_array = pa.array([label], type=pa.string())
                    split_array = pa.array([split], type=pa.string())

                    # Yield RecordBatch for each image
                    yield pa.RecordBatch.from_arrays(
                        [image_array, filename_array, label_array, split_array],
                        schema=schema
                    )
    else:
        # No splits, process all images together
        all_images = []
        for label in os.listdir(images_folder):
            label_folder = os.path.join(images_folder, label)
            
            # Ensure it's a directory (i.e., category)
            if not os.path.isdir(label_folder):
                continue

            # Iterate over the images within each label
            for filename in tqdm(os.listdir(label_folder), desc=f"Processing {label}"):
                image_path = os.path.join(label_folder, filename)

                # Read and convert the image to a binary format
                with open(image_path, 'rb') as f:
                    binary_data = f.read()

                # Optional resizing or preprocessing
                if resize:
                    image = Image.open(io.BytesIO(binary_data))
                    image = image.resize(resize)
                    with io.BytesIO() as img_byte_arr:
                        image.save(img_byte_arr, format="JPEG")
                        binary_data = img_byte_arr.getvalue()

                image_array = pa.array([binary_data], type=pa.binary())
                filename_array = pa.array([filename], type=pa.string())
                label_array = pa.array([label], type=pa.string())

                # No split column for datasets without splits
                all_images.append(pa.RecordBatch.from_arrays(
                    [image_array, filename_array, label_array],
                    schema=schema
                ))

        # Yield all images as a single batch (no split column)
        yield from all_images


# Function to write images to Lance dataset
def write_to_lance(images_folder, dataset_name, schema, splits=None, resize=None):
    if splits:
        for split in splits:
            # Construct the lance file path based on the split
            lance_file_path = os.path.join(images_folder, f"{dataset_name}_{split}.lance")
            print(f"Writing Lance dataset to: {lance_file_path}")
            
            # Process images and write to Lance
            reader = pa.RecordBatchReader.from_batches(schema, process_images(images_folder, schema, splits=[split], resize=resize))
            lance.write_dataset(
                reader,
                lance_file_path,
                schema,
            )
    else:
        # If no splits, create a single lance file
        lance_file_path = os.path.join(images_folder, f"{dataset_name}.lance")
        print(f"Writing single Lance dataset to: {lance_file_path}")

        reader = pa.RecordBatchReader.from_batches(schema, process_images(images_folder, schema, splits=None, resize=resize))
        lance.write_dataset(
            reader,
            lance_file_path,
            schema,
        )


# Function to load the dataset into pandas DataFrame
def loading_into_pandas(images_folder, dataset_name, splits=None, batch_size=10):
    data_frames = {}  # Dictionary to store DataFrames for each split

    if splits:
        for split in splits:
            uri = os.path.join(images_folder, f"{dataset_name}_{split}.lance")
            ds = lance.dataset(uri)
            
            # Accumulate data from batches into a list
            data = []
            for batch in tqdm(ds.to_batches(columns=["image", "filename", "label", "split"], batch_size=batch_size), desc=f"Loading {split} batches"):
                tbl = batch.to_pandas()
                data.append(tbl)

            # Concatenate all DataFrames into a single DataFrame
            df = pd.concat(data, ignore_index=True)
            
            # Store the DataFrame in the dictionary
            data_frames[split] = df
            print(f"Pandas DataFrame for {split} is ready")
            print("Total Rows: ", df.shape[0])
    
    else:
        # Load all images into one DataFrame (no split column)
        uri = os.path.join(images_folder, f"{dataset_name}.lance")
        ds = lance.dataset(uri)
        
        # Accumulate data from batches into a list
        data = []
        for batch in tqdm(ds.to_batches(columns=["image", "filename", "label"], batch_size=batch_size), desc="Loading all batches"):
            tbl = batch.to_pandas()
            data.append(tbl)

        # Concatenate all DataFrames into a single DataFrame
        df = pd.concat(data, ignore_index=True)
        data_frames["all"] = df
        print(f"Pandas DataFrame for all data is ready")
        print("Total Rows: ", df.shape[0])
    
    return data_frames

def convert_dataset(dataset_path, batch_size=10, splits=None, resize=None):
    # Validate dataset path
    if not os.path.exists(dataset_path):
        raise ValueError(f"The dataset folder '{dataset_path}' does not exist.")

    # Extract dataset name
    dataset_name = os.path.basename(dataset_path)

    # Define schema for the dataset
    schema = pa.schema([
        pa.field("image", pa.binary()),
        pa.field("filename", pa.string()),
        pa.field("label", pa.string())
    ])
    if splits:
        schema = schema.append(pa.field("split", pa.string()))

    # Start processing and converting to Lance format
    start = time.time()
    write_to_lance(dataset_path, dataset_name, schema, splits=splits, resize=resize)
    data_frames = loading_into_pandas(dataset_path, dataset_name, splits=splits, batch_size=batch_size)
    end = time.time()
    print(f"Time(sec): {end - start:.2f}")

    return data_frames

# Main function to process the arguments and run the pipeline
def main():
    print("Welcome to the Image Dataset to Lance Converter!")

    # Prompt user for input
    dataset_path = input("Enter the path to the image dataset folder: ").strip()
    
    # Validate dataset path
    if not os.path.exists(dataset_path):
        print(f"Error: The dataset folder '{dataset_path}' does not exist.")
        return

    batch_size = int(input("Enter the batch size for processing images (default is 10): ") or 10)
    
    # Ask if there are splits
    splits_input = input("Does your dataset have splits (train, val, test)? (yes/no): ").strip().lower()
    splits = None
    if splits_input == 'yes':
        splits_input = input("Enter the splits (comma-separated, e.g., 'train,test,val'): ").strip()
        splits = [split.strip() for split in splits_input.split(',')]

    # Get optional resize dimensions from the user (e.g., '256,256')
    resize_input = input("Enter image resize dimensions (width,height), or press Enter to skip: ").strip()
    resize = None
    if resize_input:
        resize = tuple(map(int, resize_input.split(',')))

    convert_dataset(dataset_path, batch_size, splits, resize)