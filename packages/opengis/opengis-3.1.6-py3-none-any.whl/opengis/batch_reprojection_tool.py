"""
Batch Reprojection Tool
This module provides functionality for batch reprojection of raster data.
It can convert all raster data in a directory to match the projection system of a reference image.
"""

import os
from osgeo import gdal

# Enable GDAL exception handling
gdal.UseExceptions()

def batch_reprojection(src_img_path, ref_img_path, output_dir, match_resolution=False, 
                   input_formats=('.tif','.tiff','.img','.dat','.hdf'),
                   output_format='GTiff'):
    """
    Batch reprojection function
    
    Parameters:
        src_img_path (str): Path to the directory containing source images
        ref_img_path (str): Path to the reference image used for target projection
        output_dir (str): Path to output directory
        match_resolution (bool): Whether to match the reference image resolution, defaults to False
        input_formats (tuple): Supported input file format extensions, defaults to .tif,.tiff,.img,.dat,.hdf
        output_format (str): Output file format, defaults to 'GTiff'
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open reference image and get its projection info and geotransform parameters
    ref_ds = gdal.Open(ref_img_path)
    ref_proj = ref_ds.GetProjection()
    ref_geotrans = ref_ds.GetGeoTransform()
    
    # Get pixel size from reference image
    ref_pixelWidth = ref_geotrans[1]
    ref_pixelHeight = ref_geotrans[5]
    
    # Convert input formats to lowercase for case-insensitive comparison
    input_formats = tuple(fmt.lower() for fmt in input_formats)
    
    # Iterate through all files in source directory
    for filename in os.listdir(src_img_path):
        if filename.lower().endswith(input_formats):
            src_file = os.path.join(src_img_path, filename)
            
            # Determine file extension based on output format
            output_ext = {
                'GTiff': '.tif',
                'HFA': '.img',
                'ENVI': '.dat'
            }.get(output_format, '.tif')
            
            # Construct output file path
            base_name = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, f"reprojected_{base_name}{output_ext}")
            
            try:
                # Open source file
                src_ds = gdal.Open(src_file)
                
                if src_ds is None:
                    print(f"Failed to open file: {filename}")
                    continue
                
                # Set reprojection options
                warp_options = gdal.WarpOptions(
                    dstSRS=ref_proj,  # Target spatial reference system
                    format=output_format,  # Output format
                    xRes=ref_pixelWidth if match_resolution else None,  # X resolution
                    yRes=-ref_pixelHeight if match_resolution else None  # Y resolution
                )
                
                # Perform reprojection
                gdal.Warp(output_file, src_ds, options=warp_options)
                
                # Close dataset
                src_ds = None
                
                print(f"Processed: {filename}")
                
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")
                continue
    
    # Close reference dataset
    ref_ds = None
    print("Batch reprojection completed!")