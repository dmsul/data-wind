import os
import urllib

import xarray as xr

from winddata.util.env import data_path


def merge_direction_year(year):
    dfv = load_winddata('v', year)
    dfu = load_winddata('u', year)
    df = dfv.join(dfu, how='outer')

    # Check that there are no missings after merge/join
    # Add columsn for magnitude and direction
    # Remove `download_data.py` that's now redundant

    return df


def load_winddata(direction, year):
    filepath = data_path(f'{direction}wnd.sig995.{year}.nc')

    if not os.path.isfile(filepath):
        download_file(direction, year)

    netcdf = xr.open_dataset(filepath)

    df = netcdf.to_dataframe()
    df = df.drop(['time_bnds'], axis=1)

    df1 = df.loc(axis=0)[:, :, 0, :]
    df2 = df.loc(axis=0)[:, :, 1, :]

    df1 = df1.reset_index('nbnds', drop=True)
    df2 = df2.reset_index('nbnds', drop=True)

    assert df1.equals(df2)

    return df1


def download_file(direction, year):
    file = urllib.request.URLopener()
    filepath = data_path(f'{direction}wnd.sig995.{year}.nc')

    try:
        file.retrieve(
            'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/surface'
            f'/{direction}wnd.sig995.{year}.nc', filepath
        )

    except urllib.error.URLError as e:
        print(f'Failed to make request: {e.reason}')

    file.close()

    return


if __name__ == '__main__':
    df = merge_direction_year(2015)
    print(df.head())
