import numpy as np
from netCDF4 import Dataset
import pywinter.winter as pyw
import glob

def generate_intermediate_files(input_file_name, output_file_name, output_dir):
    dataset = Dataset(input_file_name, 'r')

    print(dataset.variables.keys())

    lat = dataset.variables['latitude'][:]
    lon = dataset.variables['longitude'][:]

    dlat = lat[1] - lat[0]
    dlon = lon[1] - lon[0]

    sst = dataset.variables['sst'][:]

    winter_geo = pyw.Geo0(lat[0], lon[0], dlat, dlon)
    winter_t2m = pyw.V2d('SST', sst)

    total_fields = [
        winter_t2m,
    ]

    pyw.cinter('FILE', output_file_name, winter_geo, total_fields, output_dir)


root_dir = './data/window_sst'
output_dir = root_dir + '/intermediate2017/'

files = glob.glob(f'{root_dir}/*.nc4')

for file_dir_name in files:
    month_day = file_dir_name.rsplit('_', 1)[1].split('.')[0]

    output_name = f'2017-{month_day}_12'

    print(file_dir_name, output_name, output_dir)

    generate_intermediate_files(file_dir_name, output_name, output_dir)

