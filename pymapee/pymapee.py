"""Main module."""
















































































def download_ee(ds,aoi,folder_name="GEE_Data",res=1000):
    """ Export an image from GEE with a given scale and area of interest
    to the Google Drive.

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