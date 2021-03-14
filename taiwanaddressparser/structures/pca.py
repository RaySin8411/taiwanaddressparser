class Pca(object):
    def __init__(self, province='', city='', area='', province_pos=-1, city_pos=-1, area_pos=-1):
        self.province = province
        self.city = city
        self.area = area
        self.province_pos = province_pos
        self.city_pos = city_pos
        self.area_pos = area_pos

    def propertys_dict(self, pos_sensitive):
        result = {
            "省": self.province,
            "市": self.city,
            "區": self.area
        }

        if pos_sensitive:
            result["省_pos"] = self.province_pos
            result["市_pos"] = self.city_pos
            result["區_pos"] = self.area_pos

        return result

    def __repr__(self):
        return str(self.propertys_dict(pos_sensitive=False))