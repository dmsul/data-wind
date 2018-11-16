import os
import urllib
import numpy as np
import xarray as xr
from econtools import load_or_build

from winddata.util.env import data_path, src_path


@load_or_build(data_path('wnd_sig995_{year}.pkl'))
def dir_speed_year(year):
    '''
    Direction of 'uwnd' and 'vwnd':
        positive value: west and south winds
        negative value: east and north winds

    Wind direction: 0/360-degree is North, 90-degree is East, 180-degree is
    South, 270-degree is West

    Unit of 'speed'/'vwnd'/'uwnd': m/s (meters per second)
    '''

    dfv = load_winddata('v', year)
    dfu = load_winddata('u', year)
    df = dfv.join(dfu, how='outer')
    assert df.notnull().values.any()    # Check that there are
                                        # no missings after join

    df['dir'] = 180 + np.arctan2(df['uwnd'], df['vwnd']) * 180 / np.pi
    df['speed'] = np.sqrt(df['vwnd'] ** 2 + df['uwnd'] ** 2)

    return df


def load_winddata(direction, year):
    netcdf = raw_netcdf(direction, year)

    df = netcdf.to_dataframe()
    df = df.drop(['time_bnds'], axis=1)

    df1 = df.loc(axis=0)[:, :, 0, :]
    df2 = df.loc(axis=0)[:, :, 1, :]

    df1 = df1.reset_index('nbnds', drop=True)
    df2 = df2.reset_index('nbnds', drop=True)

    assert df1.equals(df2)

    return df1


def raw_netcdf(direction, year, _load=True, _rebuild=False):
    file = urllib.request.URLopener()
    filepath = src_path(f'{direction}wnd.sig995.{year}.nc')
    if _load and not _rebuild and os.path.isfile(filepath):
        pass
    else:
        url = ('ftp://ftp.cdc.noaa.gov/Datasets/'
               'ncep.reanalysis.dailyavgs/surface'
               f'/{direction}wnd.sig995.{year}.nc')
        print('---------- Downloading ------------')
        print(url)
        try:
            file.retrieve(url, filepath)
        except urllib.error.URLError as e:
            print(f'Failed to make request: {e.reason}')
            raise e

        print('------------- Done ----------------')
        file.close()

    return xr.open_dataset(filepath)


if __name__ == '__main__':
    df = dir_speed_year(2015)
    # nc = raw_netcdf('u', 2015)
