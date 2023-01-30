# -*- coding: utf-8 -*-

"""
Created on Sat Jul 17 16:09:52 2021
"""

# Your name: Michaela Ianaki
# Your student id: 39084442
# Your email: mianaki@umich.edu
# List who you have worked with on this project: Tessa Voytovich, Miles Sheffler

import io
import sys
import csv
import unittest


def load_csv(file):
    data_dict = {}
    with open(file) as csv_file:
        for row in csv.DictReader(csv_file):
            data_dict[row['Region']] = row
        for key in data_dict:
            del(data_dict[key]['Region'])
    return(data_dict)


def get_perc(data_dict):
    pct_dict = {}
    region_dict = {}
    for dic in data_dict:
        for demographic in data_dict[dic]:
            num = int(data_dict[dic][demographic])
            total = int(data_dict[dic]['Region Totals'])
            avg = (num/total)*100
            region_dict[demographic] = avg
        pct_dict[dic] = region_dict
    return pct_dict
   

def get_diff(ap_data, census_data):
    pct_dif_dict = {}
    for region in ap_data: 
        pct_dif_dict.setdefault(region, {})
        for category in ap_data[region]:
            if category in census_data[region]:
                census = census_data[region][category]
                ap = ap_data[region][category]
                diff = abs(float(ap) - float(census))
                rounded_diff = round(diff, 2)
                pct_dif_dict[region][category] = rounded_diff
    return pct_dif_dict

def write_csv(data_dict, file_name):
    with open(file_name, 'w', newline = "") as out_file:
        writer = csv.writer(out_file)
        header = ['Region']
        header.extend(list(data_dict['west'].keys())) 
        writer.writerow(header)
        for dic in data_dict:
            for demographic in data_dict[dic]:
                writer.writerow(data_dict[dic])
        out_file.close()


def max_min_mutate(data_dict, col_list):
    # Do not change the code in this function
    # edit this code
    '''
    Mutates the data to simplify sorting

    Parameters
    ----------
    data_dict : dict
        dictionary of data passed in. In this case, it's the
    col_list : list
        list of columns to mutate to.

    Returns
    -------
    demo_vals: dict
    '''

    # Do not change the code in this function
    demo_vals = {}
    for demo in col_list:
        demo_vals.setdefault(demo, {})
        for region in data_dict:
            demo_vals[demo].setdefault(region, data_dict[region][demo])
    return demo_vals

def min_max(data_dict):
    min_max = {'max': {}, 'min': {}}
    holder = {}
    for demographic in data_dict:
        min_max['max'].setdefault(demographic, {})
        min_max['min'].setdefault(demographic, {})
        for region in data_dict[demographic]:
            holder[region] = data_dict[demographic][region]
            ascending = dict(sorted(holder.items(), key = lambda item: item[1]))
            descending = dict(sorted(holder.items(), key = lambda item: item[1], reverse = True))
        min_max["max"][demographic]= descending
        min_max['min'][demographic] = ascending
    return min_max

def nat_perc(data_dict, col_list):
    '''
    EXTRA CREDIT
    Uses either AP or Census data dictionaries
    to sum demographic values, calculating
    national demographic percentages from regional
    demographic percentages

    Parameters
    ----------
    data_dict: dict
        Either AP or Census data
    col_list: list
        list of the columns to loop through. helps filter out region totals cols

    Returns
    -------
    data_dict_totals: dict
        dictionary of the national demographic percentages

    '''
    data_dict = {}

def nat_diff(data_dict1, data_dict2):
    '''
    EXTRA CREDIT
    Calculates the difference between AP and Census
    data on a national scale

    Parameters
    ----------
    data_dict1: dict
        Either national AP or national Census data
    data_dict2: dict
        Either national AP or national Census data

    Returns
    nat_diff: dict
        the dictionary consisting of the demographic difference on natl. level
    '''
    nat_diff = {}

def main():
    # read in the data
    file1 = load_csv('region_ap_data.csv')
    file2 = load_csv('region_census_data.csv')
    # compute demographic percentages
    percentage1 = get_perc(file1)
    percentage2 = get_perc(file2)
    # computing the difference between test taker and state demographics
    pct_dif_dict = get_diff(percentage1, percentage2)
    # outputing the csv
    write_csv(pct_dif_dict, "proj1-voytovich.csv")

    # # creating a list from the keys of inner dict
    col_list = list(pct_dif_dict["west"].keys())

    # # mutating the data
    mutated = max_min_mutate(pct_dif_dict, col_list)

    # # calculating the max and mins
    min_max(mutated)

    # # extra credit
    # # providing a list of col vals to cycle through
    # col_list = census_data["west"].keys()

    # # computing the national percentages
    # ap_nat_perc = nat_perc(ap_data, col_list)
    # census_nat_perc = nat_perc(census_data, col_list)

    # # computing the difference between them
    # dif = nat_diff(ap_nat_perc, census_nat_perc)
    # print("Difference between AP Comp Sci A and national demographics:\n",
    #       dif)

main()

# unit testing
# Don't touch anything below here
# create 4 tests
class HWTest(unittest.TestCase):

    def setUp(self):
        # surpressing output on unit testing
        suppress_text = io.StringIO()
        sys.stdout = suppress_text

        # setting up the data we'll need here
        # basically, redoing all the stuff we did in the main function
        self.ap_data = load_csv("region_ap_data.csv")
        self.census_data = load_csv("region_census_data.csv")

        self.ap_pct = get_perc(self.ap_data)
        self.census_pct = get_perc(self.census_data)

        self.pct_dif_dict = get_diff(self.ap_pct, self.census_pct)

        self.col_list = list(self.pct_dif_dict["midwest"].keys())

        self.mutated = max_min_mutate(self.pct_dif_dict, self.col_list)

        self.max_min_val = min_max(self.mutated)

        # extra credit
        # providing a list of col vals to cycle through
        self.col_list = self.census_data["midwest"].keys()

        # computing the national percentages
        self.ap_nat_pct = nat_perc(self.ap_data, self.col_list)
        self.census_nat_pct = nat_perc(self.census_data, self.col_list)

        self.dif = nat_diff(self.ap_nat_pct, self.census_nat_pct)

    # testing the csv reading func is working properly
    def test_load_csv(self):
         test = load_csv("region_ap_data.csv")

         self.assertEqual(test["west"]["ASIAN"], 7477)

    # testing the get_perc function
    def test_get_perc(self):
        self.assertEqual(get_perc({"region":{"demo":5,"Region Totals":10}}),
                         {"region":{"demo": 50.0}})

    # second test on the get_perc function
    # fails because my value is wrong (doh!)
    def test2_get_perc(self):
        self.assertEqual(
            self.ap_pct["midwest"]['AMERICAN INDIAN/ALASKA NATIVE'],
            0.29)

    # testing the get_diff function
    def test_get_diff(self):
        self.assertEqual(
            get_diff({"region":{"demo":50.0}},{"region":{"demo":50.0}}),
            {'region': {'demo': 0.0}}
            )

    # second test on the get_diff function
    # needs a valid value though brah
    def test2_get_diff(self):
        self.assertEqual(
            self.pct_dif_dict["west"]["AMERICAN INDIAN/ALASKA NATIVE"],
            1.51)

    # testing the max_min function
    def test_min_max(self):
        self.assertEqual(
            min_max({"demo":{"a":1,"b":2,"c":3,"d":4,"e":5}})
            ,
            {'max': {'demo': {'e': 5, 'd': 4, 'c': 3, 'b': 2, 'a': 1}},
             'min': {'demo': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}}}
            )

    # second test on the max_min function
    def test2_min_max(self):
        self.assertEqual(
            self.max_min_val["max"]["BLACK"]["west"],
            3.47)

    # # testing the nat_pct extra credit function
    # def test_nat_perc(self):
    #    self.assertEqual(
    #    nat_perc({"region":{"demo":5,"Region Totals":10}},["demo", "Region Totals"]),
    #    {"demo":50.0, "Region Totals":10})

    # # second test for the nat_pct extra credit function
    # def test2_nat_perc(self):
    #     self.assertEqual(
    #         self.ap_nat_pct["AMERICAN INDIAN/ALASKA NATIVE"],
    #         0.3)

    # # testing the nat_dif extra credit function
    # def test_nat_diff(self):
    #     self.assertEqual(
    #         nat_diff({"demo":0.53, "Region Totals": 1},{"demo":0.5, "Region Totals": 1}),
    #         {"demo":0.03}
    #         )

    # # second test for the nat_diff extra credit function
    # def test2_nat_diff(self):
    #     self.assertEqual(
    #         self.dif["ASIAN"],
    #         28.2)

if __name__ == '__main__':
    unittest.main(verbosity=2)