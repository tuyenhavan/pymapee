"""Main module."""
import ee
from .utils import (date_range_col, monthly_datetime_list,
                    cloud_mask, scaling_data, data_format)

def modis_cloud_mask(col, from_bit, to_bit, QA_band="DetailedQA", threshold=1):
    """ Return a collection of MODIS cloud-free images

        Args:
            col (ee.ImageCollection): The input image collection.
            from_bit (int): The start bit to extract.
            to_bit (int): The last bit to extract.
            QA_band (str|optional): The quality band which contains cloud-related infor. Default to DetailedQA.
            threshold (int|optional): The threshold value to mask cloud-related pixels. Default to 1.

        Returns:
            ee.ImageCollection: The output collection with cloud-free pixels.
    """
    if not isinstance(col, ee.ImageCollection):
        raise TypeError ("Unsupported data type. It only supports ee.ImageCollection")
    out_col=cloud_mask(col, from_bit, to_bit, QA_band, threshold)
    return out_col

def landsat_cloud_mask(col, from_bit, to_bit, QA_band="QA_PIXEL ", threshold=1):
    """ Return a collection of Landsat cloud-free images

        Args:
            col (ee.ImageCollection): The input image collection.
            from_bit (int): The start bit to extract.
            to_bit (int): The last bit to extract.
            QA_band (str|optional): The quality band which contains cloud-related infor. Default to QA_PIXEL.
            threshold (int|optional): The threshold value to mask cloud-related pixels. Default to 1.

        Returns:
            ee.ImageCollection: The output collection with cloud-free pixels.
    """
    if not isinstance(col, ee.ImageCollection):
        raise TypeError ("Unsupported data type. It only supports ee.ImageCollection")
    out_col=cloud_mask(col, from_bit, to_bit, QA_band, threshold)
    return out_col

def sentinel2_cloud_mask(col, from_bit, to_bit, QA_band="QA60", threshold=0):
    """ Return a collection of Sentinel-2 cloud-free images

        Args:
            col (ee.ImageCollection): The input image collection.
            from_bit (int): The start bit to extract (e.g., 10)
            to_bit (int): The last bit to extract (e.g., 11)
            QA_band (str|optional): The quality band which contains cloud-related infor. Default to DetailedQA.
            threshold (int|optional): The threshold value to mask cloud-related pixels. Default to 1.

        Returns:
            ee.ImageCollection: The output collection with cloud-free pixels.
    """
    if not isinstance(col, ee.ImageCollection):
        raise TypeError ("Unsupported data type. It only supports ee.ImageCollection")
    out_col=cloud_mask(col, from_bit, to_bit, QA_band, threshold)
    return out_col


def monthly_composite(col, mode=None):
    """ Return a collection of monthly images

        Args:
            col (ee.ImageCollection): The input image collection.
            mode (str): The aggregated method. Supported modes 'max', 'min',
                        'median', 'mean', 'sum'. Default to None.

        Returns:
            ee.ImageCollection: A output image collection of monthly images.
   """
    if  not isinstance(col, ee.ImageCollection):
        raise TypeError ("Unsupported data type. Expected data is ee.ImageCollection")
    if not isinstance(mode, (str, type(None))):
        raise TypeError ("Unsupported data type. Mode should be string")
    if mode is None:
        mode="max"
    mode=mode.lower().strip()
    if mode not in ["max", "mean", "median", "mvc", "min", "sum"]:
        raise ValueError ("Unsupported methods. Please choose mean, max, min, sum, or median")

    first_date, latest_date=date_range_col(col)
    monthly_list=monthly_datetime_list(first_date, latest_date)
    def monthly_data(date):
        start_date=ee.Date(date)
        end_date=start_date.advance(1,"month")
        monthly_col=col.filterDate(start_date, end_date)
        size=monthly_col.size()

        if mode == "mean":
            img=monthly_col.mean().set({"system:time_start":start_date.millis()})
        elif mode == "max":
            img=monthly_col.max().set({"system:time_start":start_date.millis()})
        elif mode == "min":
            img=monthly_col.min().set({"system:time_start":start_date.millis()})
        elif mode in ["median", "mvc"]:
            img=monthly_col.median().set({"system:time_start":start_date.millis()})
        else:
            img=monthly_col.sum().set({"system:time_start":start_date.millis()})
        return ee.Algorithms.If(size.gt(0), img)
    composite_col = ee.ImageCollection.fromImages(monthly_list.map(monthly_data))
    return composite_col

def VAI(col, scale=1):
    """ Return a collection of monthly vegetation anomaly index.

        Args:
            col (ee.ImageCollection): The input image collection.
            scale (int|float|optional): Scaling factor

        Returns:
            ee.ImageCollection: The output collection with vegetation Anomaly Index (VAI).
    """
    if not isinstance(col, ee.ImageCollection):
        raise TypeError ("Unsupported data type. Please provide ee.ImageCollection.")
    col=scaling_data(col, scale)

    first_date, latest_date=date_range_col(col)
    monthly_list=monthly_datetime_list(first_date, latest_date)
    def ndvi_anomaly(date):
        start_time=ee.Date(date)
        set_month=ee.Number.parse(start_time.format("MM"))
        last_time=start_time.advance(1,"month")
        col_month=col.filter(ee.Filter.calendarRange(set_month,set_month,"month"))
        subcol=col.filterDate(start_time,last_time)
        size=col_month.size()
        mean=col_month.mean()
        anomaly=subcol.max().subtract(mean).set({"system:time_start":start_time.millis()})
        return ee.Algorithms.If(size.gt(0), anomaly.rename("VAI"))
    vai=ee.ImageCollection.fromImages(monthly_list.map(ndvi_anomaly))
    return vai

def VCI(col):
    """ Return a collection of vegetation condition index.

        Args:
            col (ee.ImageCollection): The input image collection.
            scale (int|float|optional): Scaling factor

        Returns:
            ee.ImageCollection: The output collection with vegetation Anomaly Index (VAI).
    """
    if not isinstance(col, ee.ImageCollection):
        raise TypeError ("Unsupported data type. Please provide ee.ImageCollection.")

    first_date, latest_date=date_range_col(col)
    monthly_list=monthly_datetime_list(first_date, latest_date)
    def vci(date):
        start_time=ee.Date(date)
        set_month=ee.Number.parse(start_time.format("MM"))
        last_time=start_time.advance(1,"month")
        col_month=col.filter(ee.Filter.calendarRange(set_month,set_month,"month"))
        subcol=col.filterDate(start_time,last_time)
        size=col_month.size()
        mean=col_month.mean()
        min_value=col_month.min()
        max_value=col_month.max()
        vci_img=subcol.max().subtract(min_value).divide(max_value.subtract(min_value)).multiply(100)
        vci_img=vci_img.set({"system:time_start":start_time.millis()}).rename("VCI")
        return ee.Algorithms.If(size.gt(0), vci_img)
    vci_col=ee.ImageCollection.fromImages(monthly_list.map(vci))
    return vci_col

def col_resample(col, resample_method=None, scale=None, crs=None):
    """ Return a collection of resampled images. Resampling methods include max, min,
        bilinear, bicubic, average, mode, and median.

        Args:
            col (ee.ImageCollection|ee.Image): The input image collection.
            resample_method (str|optional): The resampling method. Default to bilinear.
            crs (str|optional): The coordinate referenced system (reprojection) EPSG code. Default to None.
            scale (int|float|optional): The spatial resolution in meters. Default to None.

        Returns:
            ee.ImageCollection: The output of resampled collection.
    """
    if resample_method is None:
        resample_method="bilinear"
    if crs is None:
        if isinstance(col, ee.Image):
            crs=col.select(0).projection().getInfo()["crs"]
        elif isinstance(col, ee.ImageCollection):
            crs=col.first().select(0).projection().getInfo()["crs"]
    if scale is None:
        scale =1000
    if not (isinstance(resample_method, str) and isinstance(crs, str) and isinstance(scale, (int, float))):
        raise TypeError ("Unsupported data type!")
    if isinstance(col, ee.Image):
        data=ee.Image(col).resample(resample_method).reproject(crs=crs, scale=scale)
    if isinstance(col, ee.ImageCollection):
        data=col.map(lambda img: img.resample(resample_method).reproject(crs=crs, scale=scale))
    else:
        raise TypeError("Unsupported data type!")
    return data

def value_from_image(img, polygon, method=None, scale=None, keep_geometry=False):
    """ Extract values from an multi-band image using polygon (e.g., point, polygon).

        Args:
            img (ee.Image): The image that is used to extract values from.
            polygon (ee.FeatureCollection): The shapefile feature collection.
            method (str|optional): The method for extracting values using shapefile feature. Default to None.
            scale (int|float|optional): The scale value in meters.
            keep_geometry (bol|optional): If True, then keep the coordinate values. Default to False.

        Returns:
            pandas.DataFrame: The extracted dataframe.
    """
    if not isinstance(img, ee.Image):
        raise TypeError("Unsupported data type!")
    if not isinstance(polygon, ee.FeatureCollection):
        raise TypeError("Unsupported data type!")
    if method is None:
        method="median"
    if scale is None:
        scale =1000
    if not (isinstance(method, str) and isinstance(scale, (int, float))):
        raise TypeError("Unsupported data type!")
    value=img.reduceRegions(collection=polygon, reducer=method, scale=scale)
    dict_value=value.select(trend_band.bandNames().getInfo(), retainGeometry=keep_geometry).getInfo()
    df=data_format(dict_value)
    return df


def download_ee(ds,aoi,folder_name="GEE_Data",res=1000):
    """ Export an image from GEE with a given scale and area of interest
    to the Google Drive. If input data is an ImageCollection, it will convert it
    into an image and then export. The collection should contains only single data,
    for example NDVI bands or precipitation bands or LST bands.

        Args:
            ds (ee.Image|ee.ImageCollection): The input ee.Image or ee.ImageCollection
            aoi (FeatureCollection): The area of interest to clip the images.
            folder_name (str): An output file name. Default is GEE_Data
            res (int): A spatial resolution in meters. Default is 1km.

        Returns:
            ee.Image: the clipped image with crs: 4326
    """
    if isinstance(ds, ee.ImageCollection):
        # Convert it to an image
        img=ds.toBands()
        # get bands and rename
        oldband=img.bandNames().getInfo()
        newband=["_".join(i.split("_")[::-1]) for i in oldband]
        # Rename it
        new_img=img.select(oldband, newband).clip(aoi)
    elif isinstance(ds, ee.Image):
        new_img=ds.clip(aoi)
    else:
        raise TypeError("Unsupported data type!")

    # Initialize the task of downloading an image
    task = ee.batch.Export.image.toDrive(image=new_img,  # an ee.Image object.
                                     region=aoi.geometry().bounds().getInfo()["coordinates"],  # an ee.Geometry object.
                                     description=folder_name,
                                     folder=folder_name,
                                     crs="EPSG:4326",
                                     scale=res)
    task.start()