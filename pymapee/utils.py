""" A helper module to support pymapee module"""
import datetime
import ee

##############################################################################
#                                 Cloud Mask                                 #
##############################################################################

def bitwise_extract(img, from_bit, to_bit):
    """ Extract cloud-related bits

        Args:
            img (ee.Image): The input image containing QA bands.
            from_bit (int): The starting bit.
            to_bit (int): The ending bit (inclusive).

        Returns:
            ee.Image: The output image with wanted bit extracts.
    """
    mask_size=ee.Number(to_bit).add(ee.Number(1)).subtract(from_bit)
    mask=ee.Number(1).leftShift(mask_size).subtract(1)
    out_img=img.rightShift(from_bit).bitwiseAnd(mask)
    return out_img

def cloud_mask(col, from_bit, to_bit, QA_band, threshold=1):
    """ Mask out cloud-related pixels from an ImageCollection.

        Args:
            col (ee.ImageCollection): The input image collection.
            from_bit (int): The starting bit to extract bitmask.
            to_bit (int): The ending bit value to extract bitmask.
            QA_band (str): The quality assurance band, which contains cloud-related information.
            threshold (int|optional): The threshold that retains cloud-free pixels.

        Returns:
            ee.ImageCollection: Cloud masked ImageCollection.
    """
    def img_mask(img):
        qa_band=img.select(QA_band)
        bitmask_band=bitwise_extract(qa_band, from_bit, to_bit)
        mask_threshold=bitmask_band.lte(threshold)
        masked_band=img.updateMask(mask_threshold)
        return masked_band
    cloudless_col=col.map(img_mask)
    return cloudless_col

##############################################################################
#                            Datetime Untilities                             #
##############################################################################

def time_convert(date_code):
    """ Convert GEE time code to Python datetime.

        Args:
            date_code (int): The GEE datetime code

        Returns:
            datetime.datetime: The Python datetime object.
    """
    # Initialize the start date since GEE started date from 1970-01-01
    start_date=datetime.datetime(1970,1,1,0,0,0)
    # Convert time code to number of hours
    hour_number=date_code/(60000*60)
    # Increase dates from an initial date by number of hours
    delta=datetime.timedelta(hours=hour_number)
    end_date=start_date+delta
    return end_date

def date_range_col(col):
    """ Return the first and latest datetimes of image acquision in the collection

        Args:
            col (ee.ImageCollection): The input image collection.

        Returns:
            tuple: The ee.Date object
    """
    first_date=ee.Date(col.first().get("system:time_start"))
    latest_date=ee.Date(col.limit(1, "system:time_start", False).first().get("system:time_start"))
    return first_date, latest_date

def monthly_datetime_list(first_date, latest_date):
    """ Return a list of monthly datetime objects.

        Args:
            first_date(ee.date): The first date of collection.
            latest_date(ee.Date): The latest date of collection.

        Returns:
            ee.List: The list of monthly datetime objects.
    """
    m=ee.Number.parse(first_date.format("MM"))
    y=ee.Number.parse(first_date.format("YYYY"))
    month_count=latest_date.difference(first_date,"month").round()
    month_list=ee.List.sequence(0, month_count)
    def month_step(month):
        first_month=ee.Date.fromYMD(y,m,1)
        next_month=first_month.advance(month,"month")
        return next_month.millis()
    monthly_list=month_list.map(month_step)
    return monthly_list

##############################################################################
#                                 Other Untilities                           #
##############################################################################

def is_package_install(pkg_name):
    """ Return True if the package is installed and False otherwise."""
    try:
        __import__(pkg_name)
        return True
    except:
        return False

def package_install(pkg_name):
    """ Install the package."""
    import subprocess
    if isinstance(pkg_name, str):
        pkg_name=pkg_name.strip()
    subprocess.check_call(["python","-m", "pip","install", pkg_name])

def scaling_data(col, scale_factor=None):
    """ Scale value of an image or collection

        Args:
            col (ee.ImageCollection|ee.Image): The input image or collection.
            scale_factor (int|float|optional): The scale given by scale information in image band. Default to None.

        Returns:
            ee.Image|ee.ImageCollection: The output image or collection with scaled values.

    """
    if scale_factor is None:
        scale_factor=1
    if isinstance(col, ee.Image):
        out_data=ee.Image(col.multiply(scale_factor).copyProperties(col, col.propertyNames()))
    if isinstance(col, ee.ImageCollection):
        out_data=col.map(lambda img: img.multiply(scale_factor).copyProperties(img, img.propertyNames()))
    return out_data

def kelvin_celsius(col):
    """ Convert temperature from Kelvin unit to celsius degree

        Args:
            col (ee.Image|ee.ImageCollection): The input image or collection for unit conversion.

        Returns:
            ee.Image|ee.ImageCollection: The converted output image or collection in celsius unit.
    """
    if isinstance(col, ee.Image):
        out_data=ee.Image(col.subtract(273.15).copyProperties(col, col.propertyNames()))
    if isinstance (col, ee.ImageCollection):
        out_data=col.map(lambda img: img.subtract(273.15).copyProperties(img, img.propertyNames()))
    return out_data

def data_format(input_data):
    """ Format data returned by reduceRegions"""
    if not is_package_install("pandas"):
        package_install("pandas")
    try:
        import pandas as pd
    except:
        print("Please install pandas. Here is the link https://pandas.pydata.org/docs/getting_started/install.html")

    data=input_data["features"]
    slist=[]
    for i in data:
        thuoctinh=i["properties"]
        slist.append(thuoctinh)
    df=pd.DataFrame(slist)
    return df

def col_timestamp_band(col):
    """ return a collection with a new band added called timestamp"""
    def time_band(img):
        _time_band=img.metadata("system:time_start").rename("timestamp")
        time_band_mask=_time_band.updateMask(img.mask().select(0))
        return img.addBands(time_band_mask)
    return col.map(time_band)
