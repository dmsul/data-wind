import xarray as xr

from winddata.util.env import data_path


def load_winddata(direction, year):
    filepath = data_path(f'{direction}wnd.sig995.{year}.nc')

    netcdf = xr.open_dataset(filepath)
    df = netcdf.to_dataframe()
    df = df.reset_index()

    return df


if __name__ == '__main__':
    df = load_winddata("v", 2015)
    print(df.head())
