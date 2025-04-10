# Automated Ice On/Off monitoring
---

This tool is designed to automate the detection of ice on/off dates for waterbodies in the Ottawa River Watershed. Ice on refers to the state of total ice coverage, while ice off indicates open, ice-free waters. 
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
  
* IceOnOff_Presentation.pdf &rarr; A copy of the project presentation
  
* demo &rarr; Folder containing demo inputs and outputs, including a command line screenshot, output graph, and a sample CSV
  
* LICENSE &rarr; MIT license covering the use and distribution of this project
  
* README.md &rarr; Overview of the Ice On/Off analysis tools and usage instructions (you’re reading this now)

---
## Hardware Requirements
Since most of the image processing in these tools is handled on Google Earth Engine’s servers, they do not require intensive local memory. However, to ensure smooth performance when plotting results or managing CSV files, it’s recommended to use a computer with at least 8 GB of RAM.

Internet access is required for all Earth Engine operations.

**Note:** Processing speed may vary depending the complexity of the analysis (e.g., large waterbodies and/or wide date ranges), Google’s server load, and your internet connection.

---
## Environment Setup
1. Save the IceOnOff_ORK.yml file to an accessible directory

2. Download [Anaconda](https://www.anaconda.com/download)
   
3. Open the Anaconda Prompt (included in Anaconda installation)
   
4. Navigate to the file containing IceOnOff_ORK.yml. To do this, run the following:
```
cd [path to your directory]
```
5. Create an environment using the .yml file. To do this, run the following:
```
conda env create --file IceOnOff_ORK.yml
```
* If needed, replace 'IceOnOff_ORK' with an appropriate name
  
**Note:** The IceOnOff_ORK environment is not explicitly required. Other Environments will work, provided they contain the following packages: 
* earthengine-api

* pandas

* matplotlib

---
## Tool Setup & Usage

Before using these tools, ensure that: 
* Anaconda is installed on your computer

* You have access to an appropriate python environment

* The Ice On/Off analysis tool is saved on your computer
  
* You have a Google account and a registered [Google Earth Earth Engine project](https://console.cloud.google.com/earth-engine/welcome?pli=1&invt=AbuNfA)

### Step-by-step instructions
1. Open the command-line interface and select the directory where the .py files are stored.
```
cd [file path]
```
* cd &rarr; "change directory"
* Notice the prompt update to the selected directory

2. Activate your environment:
```
conda activate [environment name]
```
* Notice the prompt update from (base) to your environment. This means it worked!

3. Run the Ice On/Off analysis tool
```
python IceOnOff_L9.py
```
* If needed, replace IceOnOff_L9 with the proper file name

From here, the tool will provide prompts for the necessary input

4. Alternative execution
   
Use the same input as step 3, followed by the desired parameters:
```
python IceOnOff_L9.py [HYDROUID] [Start Date] --end_date [End Date]
```
* This method bypasses prompts, allowing for direct parameter input
* Make sure to include “--end_date” before entering the end date
* This approach will still prompt you to enter your earth engine project

---
## Script Documentation
* See the [Sphinx-generated documentation](https://ben-schellenberg.github.io/Ice_OnOff_Documentation/) for a description of each function used in the Ice On/Off analysis tools.

---
## Troubleshooting / FAQ

**Q:** “Where should I save the scripts?”
*	You can save them anywhere, but it’s recommended to use a simple path with no special characters. 
*	For example, “C: /OttawaRiverkeeper/IceOnOff”


**Q:** “ModuleNotFoundError: No module named [module name]”
*	This error means the required packages are not installed in the current environment. 
*	Ensure that the correct environment has been activated. 
*	To verify which packages are installed in the current environment run: 
```
conda list

# Make sure you're in the environment you want to check
```
*	To install packages, run:
```
conda install [package name]

# Make sure the correct environment is activated
```


**Q:** “python can’t open file [file path]: [Errno 2] No such file or directory”
*	This error means python can’t find the file you are trying to access. 
*	Check the file name for any typos.
*	Make sure you’re in the correct directory.
*	You can type “dir” (windows) or “ls” (Mac/Linux) in the command line to list files in the current directory.


**Q:** “How do I know the HYDROUID of the lake I want to analyze?”
*	When prompted you can open the [interactive map](https://ben-schellenberg.github.io/OttawaRiverWatershed/ORW_Feature_Names.html) (also linked in the tool) to browse the IDs of each waterbody. 


**Q:** “No imagery found for this date range”
* This can happen for several reasons: 
  	 * Too much cloud cover over the selected waterbody between selected dates.
   	 * Imagery does not fully cover the waterbody between selected dates.
	 * There is no satellite pass over for the waterbody between selected dates.
    
* Try widening the date range or selecting a different waterbody.
  
---
### For a more detailed overview of this project, see the included IceOnOff_ProjectReport.pdf

---
## Acknowledgments

We thank Dr. Derek Mueller for his ongoing support throughout this project, including feedback on intermediate deliverables and valuable insights during team discussions.

We would also like to acknowledge Liam Nguyen, who initially proposed this project and provided suggestions that helped ensure our efforts aligned with the project’s overarching goals.


### Frequently used online resources
* [Stack Overflow](https://stackoverflow.com/questions)

* Google Earth Engine [guides](https://developers.google.com/earth-engine/guides)

* [ChatGPT](https://chatgpt.com/)
