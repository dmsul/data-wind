import pandas as pd
import xarray as xr

from winddata.util.env import data_path

def load_winddata(direction, year):
    filepath = data_path(f'{direction}wnd.sig995.{year}.nc')

    netcdf = xr.open_dataset(filepath)
    df = pd.DataFrame(netcdf['nbnds'].data)
    df.index = netcdf['lat'].data
    df.columns = netcdf['lon'].data

    return df

if __name__ == '__main__':
    print(load_winddata("v", 2015))
