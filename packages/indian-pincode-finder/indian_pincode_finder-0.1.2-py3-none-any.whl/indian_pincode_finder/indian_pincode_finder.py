import pandas as pd
import importlib.resources


class IndianPincodeFinder:
    def __init__(self):
        self.dir = 'indian_pincode_finder.data'
        self.file = 'india_pincode_final.csv'
        try:
            self.df = self.__get_data_frame__()
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['pincode', 'Taluk', 'Districtname', 'statename'])
            print("Error while loading data...")

    def __get_data_frame__(self) -> pd.DataFrame:
        with importlib.resources.open_text(self.dir, self.file) as csv_file:
            return pd.read_csv(csv_file)

    def get_all_states(self) -> dict:
        try:
            return {"states": self.df['statename'].unique().tolist()}
        except Exception as ex:
            return {"error": ex}

    def get_districts_by_states(self, state_name: str) -> dict:
        try:
            return {
                "state": state_name,
                "districts": self.df[
                    self.df['statename'].str.lower().str.strip() == state_name.lower().strip()
                    ]['Districtname'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_all_districts(self) -> dict:
        try:
            return {
                "districts": self.df['Districtname'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_all_cities(self) -> dict:
        try:
            return {
                "cities": self.df['Taluk'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_all_zipcodes(self) -> dict:
        try:
            return {
                "pincodes": self.df['pincode'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_cities_by_state(self, state_name: str) -> dict:
        try:
            return {
                "state": state_name,
                "cities": self.df[
                    self.df['statename'].str.lower().str.strip() == state_name.lower().strip()
                    ]['Taluk'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_cities_by_district(self, district_name: str) -> dict:
        try:
            return {
                "district": district_name,
                "cities": self.df[
                    self.df['Districtname'].str.lower().str.strip() == district_name.lower().strip()
                    ]['Taluk'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_zipcodes_by_district(self, district_name: str) -> dict:
        try:
            return {
                "district": district_name,
                "pin_codes": self.df[
                    self.df['Districtname'].str.lower().str.strip() == district_name.lower().strip()
                    ]['pincode'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_zipcodes_by_state(self, state_name: str) -> dict:
        try:
            return {
                "state": state_name,
                "pin_codes": self.df[
                    self.df['statename'].str.lower().str.strip() == state_name.lower().strip()
                    ]['pincode'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_zipcodes_by_city(self, city_name: str) -> dict:
        try:
            return {
                "city": city_name,
                "pin_code(s)": self.df[
                    self.df['Taluk'].str.lower().str.strip() == city_name.lower().strip()
                    ]['pincode'].unique().tolist()
            }
        except Exception as ex:
            return {"error": ex}

    def get_zipcode_detail(self, pincode: int) -> dict:
        try:
            filtered_pincode = self.df[self.df['pincode'] == pincode]
            return {"pin_code": pincode, "city": filtered_pincode['Taluk'].tolist()[0],
                    "district": filtered_pincode['Districtname'].tolist()[0],
                    "state": filtered_pincode['statename'].tolist()[0]}
        except Exception as ex:
            return {"error": ex}
