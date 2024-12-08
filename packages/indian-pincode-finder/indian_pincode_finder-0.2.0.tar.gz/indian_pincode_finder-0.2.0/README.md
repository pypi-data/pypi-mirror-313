## Indian Pincode FInder
### This module is written to help those developers who needs to deal with PINCODE offline.
### Here we have collected some methods in simple way to retrive all states, districts and cities of India. Here we are providing methids to fetch the collective data related to states, districts, cities and pincodes.
#### Below we can find the implementation of the code.

##### Import 

from indian_pincode_finder import IndianPincodeFinder

##### Implementation 
Initialise the IndianPincodeFinder as below
IndianPincodeFinderObj = IndianPincodeFinder()

These are the methods we can look for. all the method names are self-explanatory.


- IndianPincodeFinderObj.get_all_states()
- IndianPincodeFinderObj.get_districts_by_states('Delhi')
- IndianPincodeFinderObj.get_all_districts()
- IndianPincodeFinderObj.get_all_cities()
- IndianPincodeFinderObj.get_all_zipcodes()
- IndianPincodeFinderObj.get_cities_by_district('Patna')
- IndianPincodeFinderObj.get_cities_by_state('Bihar')
- IndianPincodeFinderObj.get_zipcodes_by_state('Bihar')
- IndianPincodeFinderObj.get_zipcodes_by_district('Patna')
- IndianPincodeFinderObj.get_zipcodes_by_city('Bikram')
- IndianPincodeFinderObj.get_zipcode_detail(801104)
