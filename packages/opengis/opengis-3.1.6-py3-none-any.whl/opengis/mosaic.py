"""
This module provides functionality for mosaicking multiple GeoTIFF images.
It uses GDAL (Geospatial Data Abstraction Library) for processing geospatial data.
"""

import os
from osgeo import gdal

def mosaic(path_image, output_dir=None):
    """
    Create a mosaic from multiple GeoTIFF images in a directory.
    
    Args:
        path_image (str): Directory path containing the input GeoTIFF files
        output_dir (str, optional): Directory path for the output mosaic. If None, 
                                  the mosaic will be saved in the input directory
    
    Returns:
        None
    """
    path = path_image
    # Get all .tif files from the directory (case-insensitive)
    path_lists = [f for f in os.listdir(path) if f.lower().endswith('.tif')]
    
    if len(path_lists) < 2:
        print(f"Not enough tif images in folder {path} for mosaic.")
        return
        
    print(f"Processing {len(path_lists)} tif images......")

    # Open all images using GDAL
    images = [gdal.Open(os.path.join(path, img), gdal.GA_ReadOnly) for img in path_lists]

    # Get projection from the first image
    input_proj = images[0].GetProjection()

    # Extract date part from the first image's filename for naming the output
    first_image_name = os.path.basename(path_lists[0])
    date_part = first_image_name.split('_')[0]

    # Configure GDAL warp options for the mosaic
    options = gdal.WarpOptions(srcSRS=input_proj, dstSRS=input_proj, format='GTiff',
                             resampleAlg=gdal.GRA_NearestNeighbour)

    output_filename = f"{date_part}_Mosaic.tif"
    
    # Set up output path, create directory if it doesn't exist
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, output_filename)
    else:
        output_path = os.path.join(path, output_filename)
        
    # Create the mosaic using GDAL Warp
    gdal.Warp(output_path, images, options=options)

    # Clean up by closing all images
    for img in images:
        img = None
        del img

    print(f"Mosaic completed, processed {len(path_lists)} tif files")
    print(f"Output file: {output_path}")

def get_subfolder_paths(folder_path):
    """
    Get paths of all subfolders in the given directory.
    
    Args:
        folder_path (str): Path to the parent directory
    
    Returns:
        list: List of paths to all subfolders
    """
    subfolder_paths = []
    for root, dirs, _ in os.walk(folder_path):
        for dir_name in dirs:
            subfolder_paths.append(os.path.join(root, dir_name))
    return subfolder_paths

def batch_mosaic(folder_path, out_path):
    """
    Perform mosaic operation on all subfolders in the given directory.
    
    Args:
        folder_path (str): Path to the parent directory containing subfolders with GeoTIFF files
        out_path (str): Output directory path for all mosaics
    
    Returns:
        None
    """
    subfolders = get_subfolder_paths(folder_path)
    for path in subfolders:
        mosaic(path, out_path)
