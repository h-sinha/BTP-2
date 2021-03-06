# Backend Setup
* Install conda. Follow the instructions given [here](https://docs.anaconda.com/anaconda/install/linux/).
* Navigate to backend directory using command line.
* Run ```conda env create -f environment.yml```.
* Run ```conda activate btp-2```
* Start the backend server using ```python main.py```

# API endpoints
* /get_map - Performs hydrology mapping for city and returns a plot for overlaying on the Google Map interface.

  **Request Method** - GET,POST

  #### Request Parameters
  * **city** - Name of city for which flood inundation has to be done
  * **date** - Date for which prediction needs to be done.

  #### Response
  * **url** * - Denotes the url where generated plot is stored
  * **bbox** - Coordinates of the bounding box corresponding to the returned matrix.
  * **centre** - Coordinate of centre of the city in parameter. Google map is centred at this coordinate for display.
  * **rainfall** - Predicted rainfall for the given date.
* /custom_data - Takes custom data for catchment and performs hydrology mapping.

  **Request Method** - GET,POST

  #### Request Parameters
  * **infil** - Infiltration data in map format
  * **soil** - Soil data in map format
  * **dem** - Dem data in map/tiff format
  * **rain** - Rainfall in mm

  #### Response
  * **url** * - Denotes the url where generated plot is stored
* /rain_pred

  **Request Method** - GET,POST

  #### Request Parameters
  * **rain** - Rainfall time series in csv format.

  #### Response
  * **url** - Denotes the url where generated plot is stored

# Files
* **main.py** - Contains all the API endpoints and handle all requests and responses.
* **rain_pred.py** - Contains functions for runnning ARIMA model for rainfall prediction.
* **hydrology.py** - Contains functions for performing hydrology mapping and processing dem data.
* **rainfall.py** - Contains functions for scraping rainfall data from Weather Underground.
* **bhuvan-downloader.py** - Automates the process of downloading data from Bhuvan. Gets bounding box for city using Google Map's geocoding API and then downloads the  data.


