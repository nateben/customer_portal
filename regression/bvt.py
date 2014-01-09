'''
Created on Jan 6, 2014

@author: nbensimon
'''
import unittest
import requests
import json
from configparser import ConfigParser


class BVT(unittest.TestCase):

   
    ###################
    #Move these values#
    ###################
    config = ConfigParser()
    config.read('regression.cfg')
    base_url = config['connection']['URL']
    username = config['authentication']['username']
    password = config['authentication']['password']
    headers = {'Connection': 'close'}
    ###################

    def setUp(self):
        
        #Clear the cache first...for each request.
        requests.get(self.base_url + "ClearCache", headers=self.headers)
               
        r = requests.get(self.base_url + "Login/" + self.username + "/" + self.password, headers=self.headers)
        self.assertEqual(200, r.status_code)
        response_data = r.text
        #print (response_data)
        auth_dict = json.loads(response_data)
        #print ("Token ID is: ", auth_dict["TokenID"])
        self.token_id = auth_dict['payload']['TokenID']

    def tearDown(self):
        pass

    
    def test_get_pv_production_data(self):        
        r = requests.get(self.base_url + "getPVProductionData?id=" + self.token_id, 
                         headers=self.headers)
        self.assertEqual(200, r.status_code)
        response_data = r.text
        #print (response_data)
        pv_prod_data_dict = json.loads(response_data)
        self.assertEqual(200, int(pv_prod_data_dict['statusCode']))
        payload = pv_prod_data_dict['payload']
        curr_prod_value = payload['CurrentProduction']['value']
        self.assertGreater(float(curr_prod_value), 0, "Expected Greater than 0, Actual " + curr_prod_value)

    def test_get_real_time_net_display(self):
        r = requests.get(self.base_url + "getRealTimeNetDisplay?id=" + self.token_id, 
                         headers=self.headers)
        self.assertEqual(200, r.status_code)
        response_data = r.text
        #print (response_data)
        pv_prod_data = json.loads(response_data)
        self.assertEqual(200, int(pv_prod_data['statusCode']))
        payload = pv_prod_data['payload']
        curr_prod_value = payload['currentProduction']['value']
        self.assertGreater(float(curr_prod_value), 0, "Expected Greater than 0, Actual " + curr_prod_value)

    
    def test_utlity_rates(self):
        postal_code = "78681"
        r = requests.get(self.base_url + "UtilityRates?id=" + self.token_id + "&postalCode=" + postal_code, 
                         headers=self.headers)
        self.assertEqual(200, r.status_code)
        response_data = r.text
        #print (response_data)
        utility_rates = json.loads(response_data)
        self.assertEqual(200, int(utility_rates['statusCode']))
        utils = utility_rates['payload']['Utilities']
        util_id = utils[0]['ID']
        self.assertGreater(util_id, 0, "Expected Greater than 0, Actual " + str(util_id))

        #Get the Synthesized Bill
        three_day_value_id = "4"
        r1 = requests.get(self.base_url + 
                          "SynthesizedBill?id=" + self.token_id + 
                          "&RateId=2206" +
                          "&value=" + three_day_value_id, 
                          headers=self.headers)
        self.assertEqual(200, r1.status_code)
        response_data = r1.text
        synthesized_bill = json.loads(response_data)
        self.assertEqual(200, int(synthesized_bill['statusCode']))
    
    def test_get_solar_today(self):
        r = requests.get(self.base_url + "getSolarToday?id=" + self.token_id, 
                         headers=self.headers)
        self.assertEqual(200, r.status_code)
        response_data = r.text
        solar_today = json.loads(response_data)
        self.assertEqual(200, int(solar_today['statusCode']))
        solar_today_payload = solar_today['payload']
        total_consumption = float(solar_today_payload['hourlyData'][0]['consumption'])
        self.assertGreater(total_consumption,
                           0, 
                           "Actual = " + str(total_consumption) +
                           "Expected > 0")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(verbosity=2)