__author__ = 'jwely'

from dnppy import core
from list_http_e4ftl01 import list_http_e4ftl01
from download_url import download_url
import os

__all__ = ["fetch_Landsat_WELD"]


def fetch_Landsat_WELD(product, tiles, years, outdir):
    """
    Fetch WELD data from the server at [http://e4ftl01.cr.usgs.gov/WELD].
    Weld data is corrected and processed Landsat 5 and 7 data that is distributed in the
    MODIS sinusoidal projection and grid format. Read more about WELD data.
    https://landsat.usgs.gov/WELD.php
    http://globalmonitoring.sdstate.edu/projects/weldglobal/

    :param product:     WELD product to download such as 'USWK','USMO','USYR'
    :param tiles:       list of tiles to grab such as ['h11v12','h11v11']
    :param years:       list of years to grab such as range(2001,2014)
    :param outdir:      output directory to save downloaded files

    :return output_filelist: A list of full filepaths to files fetched be this function
    """

    output_filelist = []

    # check formats
    global dates
    tiles = core.enf_list(tiles)
    years = core.enf_list(years)
    years = [str(year) for year in years]

    # create output directories
    for tile in tiles:
        if not os.path.exists(os.path.join(outdir,tile)):
            os.makedirs(os.path.join(outdir,tile))

    print('Connecting to servers!')

    # Map the contents of the directory
    site= 'https://e4ftl01.cr.usgs.gov/WELD/WELD'+product+'.001'
    try:
        dates = list_http_e4ftl01(site)
    except:
        print('Could not connect to site! check inputs!')

    # find just the folders within the desired year range.
    good_dates=[]
    for date in dates:
        try:
            y, m, d = date.split(".")
            if y in years:
                good_dates.append(date)
        except: pass

    print("Found {0} days within year range".format(len(good_dates)))

    # for all folders within the desired date range,  map the subfolder contents.
    for good_date in good_dates:

        files = list_http_e4ftl01(site+'/'+good_date)

        for afile in files:
            # only list files with desired tilenames and not preview jpgs
            if not '.jpg' in afile:
                for tile in tiles:
                    if tile in afile:

                        # assemble the address
                        address = '/'.join([site,good_date,afile])
                        print("Downloading {0}".format(address))

                        #download the file.
                        outname = os.path.join(outdir,tile,afile)
                        output_filelist.append(outname)
                        download_url(address, outname)
    return
