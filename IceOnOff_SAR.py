# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 16:06:37 2025

@author: Caitlin
"""

import ee
import pandas as pd
import datetime
import argparse
import webbrowser
import numpy as np
import matplotlib.pyplot as plt


def gee_initialize():
    """
    Author: Ben Schellenberg

    Authenticates the user's Google account and initializes their Google Earth Engine project.

    The user will be prompted to enter their Google Earth Engine project (e.g. ee-username).
    If a valid project is not found, the user can either enter a new project name, or exit the program.

    Note, this function is designed to be executed at the command line. Otherwise, 'project' would be a direct parameter.

    Returns
    -------
    None.

    This function does not return a value. Rather, it sets up access to Google Earth Engine.

    """

    ee.Authenticate()
    # Authenticating once, outside of the while loop.
    # In GEE, authentication happens before initialization and doesn't require a project name.

    while True:
        # A continuous loop, only broken by 'return', 'exit()', or 'break'.
        # Allows the function to continue until a specific case (input) breaks it.
        # Source: https://stackoverflow.com/questions/3754620/what-does-while-true-mean-in-python

        project = input("\nEnter the name of your Google Earth Engine Project: ")
        try:
            ee.Initialize(project=project)
            print("\nInitialization Successful!")
            break
        except Exception:
            print("Failed to initialize Earth Engine with that project.")

            while True:
                # If initialization fails, the user can keep trying to re-enter a new project name.

                try_again = (
                    input(
                        "\nWould you like to try a different project name? (yes/no): "
                    )
                    .strip()
                    .lower()
                )

                if try_again in ["yes", "y"]:
                    break  # Back to input (i.e. outer loop)

                elif try_again in ["no", "n"]:
                    print("Ok. Exiting the program.")
                    exit()  # Quit program entirely
                else:
                    print(
                        "Please enter either 'yes' or 'no'."
                    )  # Handling invalid answer.


def get_lake(lake_id):
    """
    Authors: Ben Schellenberg, Caitlin McMann

    Selects a waterbody from "projects/ee-benschellenberg04/assets/ORW_WaterBodies" (Google Earth Engine asset) based on a unique HYDROUID.

    The selected waterbody is buffered 50 metres inwards to reduce edge-pixel contamination.

    The buffered waterbody is then projected to WGS 84 / UTM Zone 18N (EPSG: 32618), which covers 78°W to 72°W longitude.

    Parameters
    ----------
    lake_id : int
        The HYDROUID of the waterbody from "OWR_waterbodies" that the user would like to select.

        IMPORTANT: Input ID cannot contain commas. (e.g. 55,404 --> 55404)

    Returns
    -------
    final_lake : ee.FeatureCollection
        The selected waterbody, buffered and reprojected.

    """

    ORW_waterbodies = ee.FeatureCollection(
        "projects/ee-benschellenberg04/assets/ORW_WaterBodies"
    )

    lake = ORW_waterbodies.filter(ee.Filter.eq("HYDROUID", lake_id))  # Selecting ID
    if lake.size().getInfo() == 0:
        return None

    buff_lake = lake.map(lambda feature: feature.buffer(-50))  # Buffering waterbody

    final_lake = buff_lake.map(
        lambda feature: feature.setGeometry(
            feature.geometry().transform(
                ee.Projection("EPSG:32618"), maxError=1
            )  # Reprojection
        )
    )

    return final_lake


def validate_lake():
    """
    Author: Ben Schellenberg, Hao Fan

    This function is designed to be executed at the command line and handles the case where no AOI is found in the main() function (i.e. invalid HYDROUID).

    The user will be prompted to open a reference map showing the IDs of the waterbodies, followed by a prompt to enter an ID.

    If a valid ID is entered, 'get_lake()' will be called to define an AOI. If not, the user can either enter a new ID, or exit the program.

    Returns
    -------
    aoi : ee.FeatureCollection
        The output of 'get_lake()' if a valid HYDROUID is entered.

    lake_id : int
        The unique HYDROUID of the selected lake.

    """
    while True:
        # Outer loop that will continue until the user either finds a valid AOI or exits the program.

        while True:
            # Inner loop to handle whether or not the user wants to open the map.
            open_map = (
                input(
                    "\nYou'll need the HYDROUID of the waterbody you'd like to analyze. Would you like to open a reference map showing all waterbodies and their IDs? (yes/no): "
                )  # Prompting reference map
                .strip()
                .lower()
            )
            if open_map in ["yes", "y"]:
                webbrowser.open(
                    "https://ben-schellenberg.github.io/OttawaRiverWatershed/ORW_Feature_Names.html"
                )  # If user enters 'yes', the map will open in their browser
                break  # Back to outer loop (ID entry)

            elif open_map in ["no", "n"]:
                break  # If user enters 'no', they will continue to ID entry (outer loop).

            else:
                print("Please enter either 'yes' or 'no'.")  # Handling invalid answer.

        try:
            lake_id = int(
                input(
                    "\nEnter the HYDROUID of the lake you would like to analyze (ID cannot include commas): "
                )
            )  # Command line inputs are strings but the HYDROUIDs are integers.
            aoi = get_lake(lake_id)  # Try get_lake() with the entered ID

            if aoi:
                return aoi, lake_id  # AOI found -> Exits the loop
            else:
                print(
                    "Lake not found."
                )  # AOI not found -> User will be prompted to try again.

        except ValueError:
            print("Invalid HYDROUID.")
        # This excpetion will occur if the entered ID is non-numeric and can't be converted to int.

        while True:
            try_again = (
                input("\nWould you like to try again? (yes/no): ").strip().lower()
            )

            if try_again in ["yes", "y"]:
                break  # Back to outer loop (i.e. map prompt and ID entry)

            elif try_again in ["no", "n"]:
                print("Ok. Exiting the program.")
                exit()  # If user decides to quite program entirely.

            else:
                print("Please enter either 'yes' or 'no'.")  # Handling invalid answer.


def toNatural(img):
    """
    Author: From GEOM4003 Water and Ice Lab

    Converts dB values to natural units.

    Parameters
    ----------
    img : ee.Image
        The input image in dB to convert to natural units.

    Returns
    -------
    ee.Image
        The converted image in natural units.
    """
    return ee.Image(10.0).pow(img.select(0).divide(10.0))


def toDB(img):
    """
    Author: From GEOM4003 Water and Ice Lab

    Converts natural units to dB.

    Parameters
    ----------
    img : ee.Image
        The input image in natural units to convert to dB.

    Returns
    -------
    ee.Image
        The converted image in dB.
    """
    return ee.Image(img).log10().multiply(10.0)


def RefinedLee(img):
    """
    Author: Adapted from GEOM4003 Water and Ice Lab

    Applies the Refined Lee filter for noise reduction on the image.

    Parameters
    ----------
    img : ee.Image
        The input image to which the filter will be applied.

    Returns
    -------
    ee.Image
        The filtered image with reduced speckle noise.
    """
    img_natural_VV = toNatural(img.select("VV"))
    img_natural_VH = toNatural(img.select("VH"))

    kernel = ee.Kernel.fixed(3, 3, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1, 1, False)

    mean_VV = img_natural_VV.reduceNeighborhood(ee.Reducer.mean(), kernel)
    variance_VV = img_natural_VV.reduceNeighborhood(ee.Reducer.variance(), kernel)

    mean_VH = img_natural_VH.reduceNeighborhood(ee.Reducer.mean(), kernel)
    variance_VH = img_natural_VH.reduceNeighborhood(ee.Reducer.variance(), kernel)

    noise_var_VV = variance_VV.divide(mean_VV.multiply(mean_VV))
    b_VV = variance_VV.subtract(
        noise_var_VV.multiply(mean_VV.multiply(mean_VV))
    ).divide(variance_VV)
    filtered_VV = mean_VV.add(b_VV.multiply(img_natural_VV.subtract(mean_VV)))

    noise_var_VH = variance_VH.divide(mean_VH.multiply(mean_VH))
    b_VH = variance_VH.subtract(
        noise_var_VH.multiply(mean_VH.multiply(mean_VH))
    ).divide(variance_VH)
    filtered_VH = mean_VH.add(b_VH.multiply(img_natural_VH.subtract(mean_VH)))

    return ee.Image.cat(
        ee.Image(10.0).multiply(filtered_VV.log10()).rename("VV"),
        ee.Image(10.0).multiply(filtered_VH.log10()).rename("VH"),
    )


def dynamic_threshold(date, polarization="VV"):
    """
    Author: Caitlin McMann

    Applies dynamic thresholding based on the month and polarization (VV or VH).

    Parameters
    ----------
    date : ee.Date
        The date of the image to determine the month for dynamic thresholding.
    polarization : str, optional, default="VV"
        The polarization for which to apply the thresholding ("VV" or "VH").

    Returns
    -------
    float
        The threshold value to use for ice detection in dB.
    """
    month = date.get("month")
    if polarization == "VV":
        if month in [12, 1, 2]:
            return -12
        else:
            return -18
    elif polarization == "VH":
        if month in [12, 1, 2]:
            return -20
        else:
            return -25
    else:
        raise ValueError("Invalid polarization. Choose 'VV' or 'VH'")


def calculate_ice_coverage(aoi, image, date):
    """
    Author: Caitlin McMann

    Calculates the percentage of ice coverage for a given area of interest (AOI).

    Parameters
    ----------
    aoi : ee.FeatureCollection
        The area of interest (AOI) to calculate ice coverage for.
    image : ee.Image
        The Sentinel-1 image from which ice coverage will be calculated.
    date : ee.Date
        The date of the image to apply dynamic thresholding.

    Returns
    -------
    ee.Image
        The input image with added properties 'Ice_Coverage_Percent' and 'Date'.
    """
    image = ee.Image(image)

    image_filtered = RefinedLee(image)

    threshold_VV = dynamic_threshold(date, polarization="VV")
    threshold_VH = dynamic_threshold(date, polarization="VH")

    ice_mask_VV = image_filtered.select("VV").gt(threshold_VV)
    ice_mask_VH = image_filtered.select("VH").gt(threshold_VH)

    ice_mask = ice_mask_VV.Or(ice_mask_VH)

    aoi_area = aoi.geometry().area(1)

    pixel_area = ee.Image.pixelArea().updateMask(ice_mask)
    ice_area = pixel_area.reduceRegion(
        reducer=ee.Reducer.sum(), geometry=aoi, scale=30, maxPixels=1e9
    ).get("area")

    ice_area = ee.Number(ice_area).max(0)
    ice_coverage = ee.Number(ice_area).divide(aoi_area).multiply(100)

    return image.set(
        {
            "Ice_Coverage_Percent": ice_coverage,
            "Date": ee.Date(image.get("system:time_start")).format("YYYY-MM-dd"),
        }
    )


def plot_ice_coverage(df):
    """
    Author: Caitlin McMann

    Plots the ice coverage over time and shows the threshold values used.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the ice coverage data to be plotted.
    """
    df["Date"] = pd.to_datetime(df["Date"])

    plt.figure(figsize=(10, 6))
    plt.plot(
        df["Date"],
        df["Ice Coverage (%)"],
        marker="o",
        color="b",
        label="Ice Coverage (%)",
        zorder=1,
    )

    plt.xlabel("Date")
    plt.ylabel("Ice Coverage (%)")
    plt.title("Ice Coverage Change")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def process_image_collection(aoi, start_date, end_date):
    """
    Author: Caitlin McMann

    Processes each image in the image collection, calculates ice coverage, and detects outliers.

    Parameters
    ----------
    aoi : ee.FeatureCollection
        The area of interest (AOI) for which ice coverage is to be calculated.
    start_date : str
        The start date for the image collection in the format 'YYYY-MM-DD'.
    end_date : str
        The end date for the image collection in the format 'YYYY-MM-DD'.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the Date, Ice Coverage (%), and Outlier status for each image in the collection.
    """
    image_collection = (
        ee.ImageCollection("COPERNICUS/S1_GRD")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
        .filter(ee.Filter.eq("instrumentMode", "IW"))
        .select(["VV", "VH"])
    )

    processed = image_collection.map(
        lambda image: ee.Image(
            calculate_ice_coverage(
                aoi,
                RefinedLee(image).copyProperties(image, image.propertyNames()),
                ee.Date(image.get("system:time_start")),
            )
        )
    )

    dates = processed.aggregate_array("Date").getInfo()
    coverage = processed.aggregate_array("Ice_Coverage_Percent").getInfo()

    df = pd.DataFrame({"Date": dates, "Ice Coverage (%)": coverage})

    plot_ice_coverage(df)

    return df


def prompt_download(df, name, first_date, last_date):
    """
    Author: Ben Schellenberg

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the date, ice coverage (%), and sensor (i.e. Landsat 9).

    name : str
        Name of the selected waterbody.

    first_date : str
        Date of the first image collected within specified date range.

    last_date : str
        Date of the last image collected within specified date range.

    Returns
    -------
    None.

    This function does not return a value. Rather, it saves a CSV to the users directory, if they so choose.

    """
    answer = (
        input("\nWould you like to download these results to a CSV? (yes/no): ")
        .strip()
        .lower()
    )
    if answer in ["yes", "y"]:
        if first_date == last_date:
            filename = f"{name}_IceCoverage_{first_date}.csv"
            # If there is only one date, the filename will only include that date.
        else:
            filename = f"{name}_IceCoverage_{first_date}_to_{last_date}.csv"
            # If there is multiple dates, the filename will include the date range.

        df.to_csv(filename, index=False)  # Saving the csv
        print(f"OK! CSV saved as '{filename}' in your current directory.")

    elif answer in ["no", "n"]:
        print("Ok! No CSV file was saved")
        # Program ends

    else:
        print("Please enter 'yes' or 'no'.")
        prompt_download(df, name, first_date, last_date)
        # Reprompt user if they enter an invalid answer.


def main():

    gee_initialize()

    # Adding necessary arguments for the analysis
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "lake_id",
        help="Enter the HYDROUID of the lake you would like to analyze. The ID cannot contain commas.",
        nargs="?",
    )
    parser.add_argument(
        "start_date", help="Enter the start date in the format 'YYYY-MM-DD'", nargs="?"
    )
    parser.add_argument(
        "--end_date",
        help="Enter the end date (optional) in the format 'YYYY-MM-DD'. Leave blank for single day: ",
    )
    args = parser.parse_args()
    # Assigning arguments to a variable that can be used as input for the functions.

    # Validate or prompt for lake ID
    if args.lake_id:
        try:
            lake_id = int(args.lake_id)
            aoi = get_lake(lake_id)
            if not aoi:
                aoi, lake_id = validate_lake()
        except ValueError:
            print("Invalid HYDROUID.")
            aoi, lake_id = validate_lake()
    else:
        aoi, lake_id = validate_lake()

    # Prompt for dates if not provided
    start_date = args.start_date
    end_date = args.end_date

    if not start_date:
        start_date = input("\nEnter the start date in the format 'YYYY-MM-DD': ")

    if not end_date:
        end_date_input = input(
            "Enter the end date (optional) in the format 'YYYY-MM-DD'. Leave blank for single day: "
        ).strip()
        end_date = end_date_input if end_date_input else None

    # Run analysis
    df = None
    while df is None:
        df = process_image_collection(aoi, start_date, end_date)
        if df is None or df.empty:
            print(
                "\nNo valid SAR imagery or no ice coverage data found for this date range."
            )

            try_again = (
                input("\nWould you like to try a new date range? (yes/no): ")
                .strip()
                .lower()
            )
            if try_again in ["yes", "y"]:
                start_date = input("\nEnter the start date (YYYY-MM-DD): ")
                end_date = input(
                    "Enter the end date (optional, YYYY-MM-DD). Leave blank for single day: "
                ).strip()
                end_date = end_date if end_date else None
            else:
                print("Ok. Exiting the program.")
                return

    # Get lake name from AOI
    if aoi.name() == "FeatureCollection":
        name = aoi.first().get("NAME").getInfo()
    else:
        name = aoi.get("NAME").getInfo()

    # First and last date for filename
    first_date = df["date"].min().strftime("%Y-%m-%d")
    last_date = df["date"].max().strftime("%Y-%m-%d")

    print("\n", df)

    prompt_download(df, name, first_date, last_date)


if __name__ == "__main__":
    main()
