import urllib

from winddata.util.env import data_path


def download_main(direction, year):
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
    download_main('v', 2015)
