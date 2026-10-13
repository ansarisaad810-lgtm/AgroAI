# DSA ALGORITHM: Hash Map Lookups (Python Dict abstraction)
# USED FOR: O(1) matching between Crop <-> Soil <-> Weather/Season.

class RecommendationHashMap:
    def __init__(self):
        self.crop_to_details = {}
        self.soil_to_crops = {}
        self.season_to_crops = {}

    def populate(self, crop_records):
        """Fills hash maps from database records."""
        for rec in crop_records:
            c_name, soil, season, technique, tools = rec["name"], rec["soil"], rec["season"], rec["technique"], rec["tools"]
            
            # Crop -> Details
            self.crop_to_details[c_name.lower()] = rec

            # Soil -> Crops list
            if soil.lower() not in self.soil_to_crops:
                self.soil_to_crops[soil.lower()] = []
            self.soil_to_crops[soil.lower()].append(rec)

            # Season -> Crops list
            if season.lower() not in self.season_to_crops:
                self.season_to_crops[season.lower()] = []
            self.season_to_crops[season.lower()].append(rec)

    def get_by_crop(self, crop_name):
        """O(1) lookup by Crop Name."""
        return self.crop_to_details.get(crop_name.lower())

    def get_by_soil(self, soil_type):
        """O(1) lookup by Soil Type."""
        return self.soil_to_crops.get(soil_type.lower(), [])

    def get_by_season(self, season_name):
        """O(1) lookup by Season/Weather."""
        return self.season_to_crops.get(season_name.lower(), [])
