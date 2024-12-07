
Initialise the IndianPincodeFinder as below
IndianPincodeFinderObj = IndianPincodeFinder()

These are the methods we can look for
print(IndianPincodeFinderObj.get_all_states())
print(IndianPincodeFinderObj.get_districts_by_states('Delhi'))
print(IndianPincodeFinderObj.get_all_districts())
print(IndianPincodeFinderObj.get_all_cities())
print(IndianPincodeFinderObj.get_all_zipcodes())
print(IndianPincodeFinderObj.get_cities_by_district('Patna'))
print(IndianPincodeFinderObj.get_cities_by_state('Bihar'))
print(IndianPincodeFinderObj.get_zipcodes_by_state('Bihar'))
print(IndianPincodeFinderObj.get_zipcodes_by_district('Patna'))
print(IndianPincodeFinderObj.get_zipcodes_by_city('Bikram'))
print(IndianPincodeFinderObj.get_zipcode_detail(801104))