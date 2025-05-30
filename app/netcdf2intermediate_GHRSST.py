import os
import numpy as np
from netCDF4 import Dataset
import pywinter.winter as pyw
import glob

def generate_intermediate_files(input_file_name, output_file_name, output_dir):
    dataset = Dataset(input_file_name, 'r')

    print(dataset.variables.keys())

    lat = dataset.variables['lat'][:]
    lon = dataset.variables['lon'][:]

    dlat = dataset.geospatial_lat_resolution
    dlon = dataset.geospatial_lon_resolution

    sst = dataset.variables['analysed_sst'][:].data[0]
    #fill value seems to be -32768
    mask = dataset.variables['mask'][:].data[0].astype(np.float32)

    winter_geo = pyw.Geo0(lat[0], lon[0], dlat, dlon)
    winter_t2m = pyw.V2d('SST', sst)
    #the mask is a bit mask where 0 is water, 1 is land
    #2 is optional lake, 3 is sea ice
    #4 is optional river and 5-7 are spare
    #from looking at the mask, they only use 0/1 in our area
    #from their default LANDSEA variable: uni="fraction", lev="200100"
    winter_land_mask = pyw.V2d('SST_mask', mask, 'Mask for SST data', 'fraction', '200100')

    total_fields = [
        winter_t2m,
        winter_land_mask,
    ]

    #technically you want the prefix to be SST here but because I am on a
    #windows machine it doesn't like the colon, so it is easier to change the
    #prefix using a separate code once I transfer the files to the Linus machine
    pyw.cinter('FILE', output_file_name, winter_geo, total_fields, output_dir)


root_dir = './data'
output_dir = root_dir + '/intermediate2017_from16/'

if not os.path.exists(output_dir):
    # Create the directory
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created.")
else:
    print(f"Directory '{output_dir}' already exists.")

files = glob.glob(f'{root_dir}/*.nc')

for file_dir_name in files:
    #this is specific to 2016 GHRSST file names
    month_day = file_dir_name.split('120000', 1)[0].split('16')[1]
    ref_month_day = month_day[0:2] + '-' + month_day[2:4]

    output_name = f'2017-{ref_month_day}_12'

    print('\n', file_dir_name, output_name, output_dir)

    generate_intermediate_files(file_dir_name, output_name, output_dir)
