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
    out_img=image.rightShift(from_bit).bitwiseAnd(mask)
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
#                                 Other Untilities                           #
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