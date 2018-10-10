# Entropy-Calculation
Entropy Calculation for a given dataset. Both discrete and continuous data are supported (using the approximation in case of continuous data)

## Requirements
Please install the required packages mentioned in the requirements.txt file. 
* `pip install -r requirements.txt`

* In addition, python-tk is required in case you want to plot the output of DBScan which may be the case for continuous data. To install, please run the following command `sudo apt-get install python-tk`

## Input Arguments
* `data-path`: data-path to the input data
* `data-type`: mode of the data (`continuous` or `discrete`)

## Entropy for Discrete Data
We use publicly available [ZipCode dataset](https://catalog.data.gov/dataset/zip-codes-zipcodes). The dataset contains two attributes for location information: (i) Zipcode, and (ii)Country. Entropy is evaluated for each of the attibutes.

### Running instructions
Arguments for Discrete Data are included in the driver script as default. Please run `python driver.py`.

## Entropy for Continuous Data
We use publicly available [Field Activity Data](https://cmgds.marine.usgs.gov/data/field-activity-data/2012-035-FA/). The dataset contains geo cordinates (latitudes and longitudes). Since the coordiates are continuous, there are a couple of ways to solve to determine the entropy

### Assuming a Gaussian Distribution
Following the central limit theorem, we can assume the geo cordinates to be distributed normally. In this case, we can estimate the mean vector <a href="https://www.codecogs.com/eqnedit.php?latex=$\in&space;R^2$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\in&space;R^2$" title="$\in R^2$" /></a>
