# Automated Ice On/Off monitoring
---

This tool is designed to automate the detection of ice on/off dates for waterbodies in the Ottawa River Watershed. Ice on refers to the state of full ice coverage, while ice off indicates open, ice free waters. 
Using Google Earth Engine, the tools leverage both Landsat 9 and Sentinel-1 data to estimate ice coverage on a user-defined waterbody and date range. The Landsat-based workflow uses a spectral index (NDSI) and cloud filtering to detect open water and ice, while the Sentinel-1 workflow applies speckle filtering and a dynamic threshold to extract ice cover from radar backscatter.

---
The output includes: 
* Percent ice cover for each image
* A summary table and graph of freeze/thaw trends
* Optional CSV downloads
