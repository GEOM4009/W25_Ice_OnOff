# Automated Ice On/Off monitoring
---

This tool is designed to automate the detection of ice on/off dates for waterbodies in the Ottawa River Watershed. Ice on refers to the state of total ice coverage, while ice off indicates open, ice free waters. 
Using Google Earth Engine, these tools leverage both Landsat 9 and Sentinel-1 data to estimate ice coverage within a user-defined waterbody and date range. The Landsat-based workflow uses a Normalized Difference Snow Index (NDSI) to detect ice, while the Sentinel-1 workflow applies speckle filtering and a dynamic threshold to extract ice cover from radar backscatter.

---
## The output includes: 
* Percent ice cover for each image
* A summary table and graph of freeze/thaw trends
* Optional CSV downloads

---
## Repository Contents
* IceOnOff_L9.py &rarr; Landsat 9 ice on/off analysis tool
* IceOnOff_SAR.py &rarr; Sentinel 1 ice on/off analysis tool
* IceOnOff_ORK.yml &rarr; python environment containing the required packages to run these tools
* IceOnOff_ProjectReport.pdf &rarr; Full project report
* LICENSE &rarr; MIT license covering the use and distribution of this project

---
## Environment Setup
1. Save the IceOnOff_ORK.yml file to an accessible directory
2. Download [Anaconda] (https://www.anaconda.com/download)
3. Open the Anaconda Prompt (included in Anaconda installation)
4. Navigate to the file containing IceOnOff_ORK.yml
```
cd [path to your directory]
```
---
## Using the tools 

---
## Troubleshooting / FAQ

Q: “Where should I save the scripts?”
*	You can save them anywhere, but it’s recommended to use a simple path with no special characters. 
*	For example, “C: /OttawaRiverkeeper/IceOnOff”

Q: “ModuleNotFoundError: No module named [module name]”
*	This error means the required packages are not installed in the current environment. 
*	Ensure that the correct environment has been activated. 
*	To verify which packages are installed in the current environment type “conda list” in the command-line. 
*	To install packages, type “conda install [package name]”

Q: “python can’t open file [file path]: [Errno 2] No such file or directory”
*	This error means python can’t find the file you are trying to access. 
*	Check the file name for any typos.
*	Make sure you’re in the correct directory.
*	You can type “dir” (windows) or “ls” (Mac/Linux) in the command line to list files in the current directory.

Q: “How do I know the HYDROUID of the lake I want to analyze?”
*	When prompted you can open the interactive map (linked in the tool) to browse the IDs of each waterbody. 
*	Map: benschellenberg.github.io/OttawaRiverWatershed/ORW_Feature_Names.html

Q: “No imagery found for this date range”
* This can happen for several reasons: 
  	 * Too much cloud cover over the selected waterbody between selected dates.
   	 * Imagery does not fully cover the waterbody between selected dates.
	 * There is no satellite pass over for the waterbody between selected dates.
* Try widening the date range or selecting a different waterbody. 

---
## Acknowledgments
