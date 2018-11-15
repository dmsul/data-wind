import os
import urllib
import numpy as np
import xarray as xr

from winddata.util.env import data_path


@load_or_build(data_path('{direction}wnd.sig995.{year}.nc'))
def dir_speed_year(year):
    '''
    Direction of 'uwnd' and 'vwnd':
        positive value: west and south winds
        negative value: east and north winds

    Wind direction: 0/360-degree is North, 90-degree is East, 180-degree is South, 270-degree is West

    Unit of 'speed'/'vwnd'/'uwnd': m/s (meters per second)

    '''

    dfv = load_winddata('v', year)
    dfu = load_winddata('u', year)
    df = dfv.join(dfu, how='outer')

    assert df.notnull().values.any()  # Check that there are no missings after join

    df['dir'] = 180 + np.arctan2(df['uwnd'], df['vwnd']) * 180 / np.pi
    df['speed'] = np.sqrt(df['vwnd']**2 + df['uwnd']**2)

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
    df = dir_speed_year(2015)
    print(df.head())
