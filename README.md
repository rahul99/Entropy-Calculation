# Entropy-Calculation
Entropy Calculation for a given attribute of a dataset.

<a href="https://www.codecogs.com/eqnedit.php?latex=E&space;=&space;-&space;\sum_{i=1}^{n}&space;\left(&space;p_i&space;*&space;log_2(p_i)&space;\right)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E&space;=&space;-&space;\sum_{i=1}^{n}&space;\left(&space;p_i&space;*&space;log_2(p_i)&space;\right)" title="E = - \sum_{i=1}^{n} \left( p_i * log_2(p_i) \right)" /></a>

Both discrete and continuous data are supported (using the approximation in case of continuous data)

## Requirements
Please install the required packages mentioned in the requirements.txt file. 
* `pip install -r requirements.txt`

* In addition, python-tk is required in case you want to plot the output of DBScan which may be the case for continuous data. To install, please run the following command `sudo apt-get install python-tk`

## Input Arguments
* `data-path`: path to the input data
* `data-type`: mode of the data (`continuous` or `discrete`)

## Entropy for Discrete Data
We use publicly available [ZipCode dataset](https://catalog.data.gov/dataset/zip-codes-zipcodes). The dataset contains two attributes for location information: (i) Zipcode, and (ii)Country. Entropy is evaluated for each of the attibutes.

### Running instructions
* `cd` to the project directory
* Run `python driver.py`. Arguments for Discrete Data are included in the driver script as default.

## Entropy for Continuous Data
We use publicly available [Field Activity Data](https://cmgds.marine.usgs.gov/data/field-activity-data/2012-035-FA/). The dataset contains geo cordinates (latitudes and longitudes). Since the coordiates are continuous, there are a couple of ways to solve to determine the entropy

### Assuming a Gaussian Distribution
Following the central limit theorem, we can assume the geo cordinates to be distributed normally. In this case, we can estimate the mean vector, <a href="https://www.codecogs.com/eqnedit.php?latex=\pmb{\mu}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\pmb{\mu}" title="\pmb{\mu}" /></a> <a href="https://www.codecogs.com/eqnedit.php?latex=$\in&space;R^2$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\in&space;R^2$" title="$\in R^2$" /></a> and the covariance matrix, <a href="https://www.codecogs.com/eqnedit.php?latex=\pmb{\Sigma}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\pmb{\Sigma}" title="\pmb{\Sigma}" /></a> <a href="https://www.codecogs.com/eqnedit.php?latex=$\in&space;R^2&space;\times&space;R^2$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\in&space;R^2&space;\times&space;R^2$" title="$\in R^2 \times R^2$" /></a> to determine the join Gaussian distribution <a href="https://www.codecogs.com/eqnedit.php?latex=\[&space;X&space;\sim&space;\mathcal{N}(\pmb{\mu},\,\pmb{\Sigma})\,&space;\]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\[&space;X&space;\sim&space;\mathcal{N}(\pmb{\mu},\,\pmb{\Sigma})\,&space;\]" title="\[ X \sim \mathcal{N}(\pmb{\mu},\,\pmb{\Sigma})\, \]" /></a> of the location X:

### Assuming a Discrete Approximation
We can use clustering based methods of discretize the continuous location values. Choosing a suitable clustering method is important, for example for K-means, there is an unknown parameter k to estimate. For location attributes, DBScan seems to be an appropriate choice. My implementation of DBScan is available in `dbscan.py`. Note that there might more sophisticated implementations available on the web.

### Running Instructions
* `cd` to the project directory
* `python driver.py --data-path ./data/2012-035-FA_samples/2012-035-FA_samples.csv --data-type continuous`

Above implementation supports approximation based entropy. Gaussian based entropy is also straightforward and therefore not implemented in the current setting
