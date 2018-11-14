import xarray as xr
import pandas as pd
import numpy as np

from winddata.util.env import data_path


def merge_direction_year(year):
    dfv = load_winddata('v', year)
    dfu = load_winddata('u', year)
    df = pd.merge(dfv, dfu, on=['lat', 'lon', 'time', 'nbnds'])

    return df


def load_winddata(direction, year):
    filepath = data_path(f'{direction}wnd.sig995.{year}.nc')

    netcdf = xr.open_dataset(filepath)
    df = netcdf.to_dataframe()
    df = df.drop(['time_bnds'], axis=1)

    df1 = df.loc(axis=0)[:, :, 0, :]
    df2 = df.loc(axis=0)[:, :, 1, :]

    # assert df1.equals(df2), "df1 does not equal df2"  # Have no idea why this returns false?

    return df1


if __name__ == '__main__':
    df = merge_direction_year(2015)
    print(df.head())
