# encoding=utf8
__author__ = "Rahul Soni"
__email__ = "sn.rahul99@gmail.com"

import argparse
import fiona
import sys, os
import math
from collections import defaultdict
from collections import Counter

def get_args():
    parser = argparse.ArgumentParser(description='Location Entropy Test')
    parser.add_argument('--data-path', default="./data/ZipCodes/ZipCodes.shp", type=str,
                        help='one of `mnist` or `fmnist` or `pmnist` or `cifar10` or `cptb` or `wptb`')
    parser.add_argument('--data-type', default="discrete", type=str,
                        help='one of `mnist` or `fmnist` or `pmnist` or `cifar10` or `cptb` or `wptb`')
    args = parser.parse_args()
    return (args)

###############################################
#               Entropy Function              #
###############################################
def get_entropy(data):
    return(-sum([p * math.log(p,2) for p in data]))

###############################################
#        Entropy for discrete values          #
###############################################
def entropy_for_descrete_data(data_path):
    data = fiona.open(data_path)
    data_count = len(data)
    print("Dataset Schema:\n{}\n".format(data.schema))
    # We learn that the ZipCode dataset contains two attributes that give location information:
    # These are: (i) ZipCode, and (ii) Country Number
    # We calculate the location entropy for each of two location attributes

    zip_code = defaultdict(int)
    country_code = defaultdict(int)
    for item in data:
        code_i = int(item['properties']['ZIP5'])
        country_i = int(item['properties']['COUNTYNBR'])
        zip_code[code_i] += 1.0
        country_code[country_i] += 1.0

    zip_code_prob = [zipcode_freq / data_count for zipcode_freq in zip_code.values()]
    country_code_prob = [cntrycode_freq / data_count for cntrycode_freq in country_code.values()]

    zip_code_entropy = get_entropy(zip_code_prob)
    country_code_entropy = get_entropy(country_code_prob)
    print("Location entropy of Dataset given Zip Code as location is: {}".format(zip_code_entropy))
    print("Location entropy of Dataset given Country Code as location is: {}".format(country_code_entropy))

###############################################
# Entropy Approximation for continuous values #
###############################################
def entropy_for_continuous_data(data_path, plot_dbscan=False):
    df = pd.read_csv(data_path, index_col=0)
    location_data = np.array(df[['LATITUDE', 'LONGITUDE']])
    data_count = location_data.shape[0]

    db = dbscan.dbscan(location_data, 0.015, 3)
    location_cluster_ids = db[0]
    location_freq = Counter(location_cluster_ids)
    location_prob = [float(item_freq) / data_count for item_freq in location_freq.values()]
    location_entropy = get_entropy(location_prob)
    print("Location entropy of Dataset given geo coordinates is: {}".format(location_entropy))

    if(plot_dbscan):
        # optional: plot dbscan for geo cordinates
        dbscan.plot_dbscan(location_data, db)

if __name__ == "__main__":
    args = get_args()
    proj_path = os.path.dirname(os.path.realpath(__file__))
    #data_path = os.path.join(proj_path, 'data/' + args.data)
    data_path = args.data_path
    data_type = args.data_type

    if(data_type == 'continuous' and 'zipcode' in args.data_path.lower()):
        raise ValueError('Incompatible data_type: `{}` | Zipcode data '
                         'contains descrete location values\n'
                         'Please pass `--data-type discrete as argument`'.format(args.data_type))

    if(data_type == 'discrete' and 'fa_samples' in args.data_path.lower()):
        raise ValueError('Incompatible data_type: `{}` | FA data '
                         'contains continuous location values\n'
                         'Please pass `--data-type continuous` as argument'.format(args.data_type))


    if(data_type == 'discrete'):
        entropy_for_descrete_data(data_path)
    elif(data_type == 'continuous'):
        import dbscan
        import pandas as pd
        import numpy as np
        entropy_for_continuous_data(data_path)
    print("execution complete")













