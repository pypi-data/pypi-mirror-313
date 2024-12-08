"""
MODIS Data Reprojection Tool

This module provides utility functions for processing MODIS satellite data,
converting HDF format MODIS data to GeoTIFF format, with support for
projection transformation, resolution adjustment, and other features.

Main features:
- Batch conversion from HDF to GeoTIFF
- Projection system transformation
- Resolution adjustment
- Band selection
"""

import os
from osgeo import gdal
from osgeo import osr
from glob import glob

def modis_to_tif_batch(input_dir, output_dir, target_epsg=None, selected_bands=None, 
                       target_resolution=None, file_pattern="*.hdf"):
    """
    Batch convert MODIS HDF files to GeoTIFF format.
    
    Parameters:
        input_dir (str): Input directory path containing MODIS HDF files
        output_dir (str): Output directory path for saving converted GeoTIFF files
        target_epsg (int, optional): Target projection EPSG code. If specified, will perform projection transformation
        selected_bands (list, optional): List of band indices to process. If None, process all bands
        target_resolution (tuple, optional): Target resolution in format (x_res, y_res)
        file_pattern (str, optional): HDF file matching pattern, defaults to "*.hdf"
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all matching HDF files
    hdf_files = glob(os.path.join(input_dir, file_pattern))
    
    if not hdf_files:
        print(f"No matching HDF files found in {input_dir}")
        return
    
    total_files = len(hdf_files)
    print(f"Found {total_files} HDF files to process")
    
    for index, hdf_file in enumerate(hdf_files, 1):
        try:
            print(f"Processing file {index}/{total_files}: {os.path.basename(hdf_file)}")
            
            # Extract base filename (without extension)
            base_name = os.path.splitext(os.path.basename(hdf_file))[0]
            hdf_ds = gdal.Open(hdf_file)
            
            if hdf_ds is None:
                print(f"Cannot open file: {hdf_file}")
                continue
            
            # Get subdatasets (bands)
            subdatasets = hdf_ds.GetSubDatasets()
            
            # If no bands specified, process all bands
            if selected_bands is None:
                selected_bands = range(len(subdatasets))
            
            for band_index in selected_bands:
                if band_index >= len(subdatasets):
                    print(f"Band {band_index} is out of range")
                    continue
                
                # Read band data and metadata
                subdataset = gdal.Open(subdatasets[band_index][0])
                proj = subdataset.GetProjection()
                geotransform = subdataset.GetGeoTransform()
                data = subdataset.ReadAsArray()
                
                # Construct output file path
                output_file = os.path.join(output_dir, f"{base_name}_band_{band_index}.tif")
                
                # Create GeoTIFF file and write data
                driver = gdal.GetDriverByName('GTiff')
                out_ds = driver.Create(output_file, 
                                     subdataset.RasterXSize, 
                                     subdataset.RasterYSize, 
                                     1, 
                                     gdal.GDT_Float32)
                
                out_ds.SetProjection(proj)
                out_ds.SetGeoTransform(geotransform)
                out_ds.GetRasterBand(1).WriteArray(data)
                
                # If projection transformation or resolution adjustment is needed
                if target_epsg or target_resolution:
                    temp_file = os.path.join(output_dir, f"{base_name}_temp.tif")
                    warp_options = gdal.WarpOptions(
                        resampleAlg=gdal.GRA_Bilinear,  # Use bilinear resampling
                        xRes=target_resolution[0] if target_resolution else None,
                        yRes=target_resolution[1] if target_resolution else None
                    )
                    
                    # If target projection is specified
                    if target_epsg:
                        target_srs = osr.SpatialReference()
                        target_srs.ImportFromEPSG(target_epsg)
                        warp_options = gdal.WarpOptions(
                            resampleAlg=gdal.GRA_Bilinear,
                            dstSRS=target_srs.ExportToWkt(),
                            xRes=target_resolution[0] if target_resolution else None,
                            yRes=target_resolution[1] if target_resolution else None
                        )
                    
                    # Perform projection transformation and resampling
                    gdal.Warp(temp_file, out_ds, options=warp_options)
                    
                    # Cleanup and rename files
                    out_ds = None
                    os.remove(output_file)
                    os.rename(temp_file, output_file)
                
                # Cleanup resources
                out_ds = None
                subdataset = None
            
            hdf_ds = None
            print(f"Completed file {index}/{total_files}")
            
        except Exception as e:
            print(f"Error processing file {hdf_file}: {str(e)}")
            continue
    
    print("All files processed!")

def modis_batch_projection(input_dir, output_dir, target_epsg=None, selected_bands=None, 
                              target_resolution=None):
    """
    Convenience function for batch projection transformation of MODIS data.
    
    Parameters:
        input_dir (str): Input directory path containing MODIS HDF files
        output_dir (str): Output directory path for saving converted files
        target_epsg (int, optional): Target projection EPSG code
        selected_bands (list, optional): List of band indices to process
        target_resolution (tuple, optional): Target resolution (x_res, y_res)
    
    Raises:
        ValueError: When input directory doesn't exist or is not a valid directory
    """
    try:
        if not os.path.exists(input_dir):
            raise ValueError(f"Input directory does not exist: {input_dir}")
        
        if not os.path.isdir(input_dir):
            raise ValueError(f"Input path is not a directory: {input_dir}")
        
        modis_to_tif_batch(input_dir, output_dir, target_epsg, selected_bands, target_resolution)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise