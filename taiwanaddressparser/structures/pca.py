class Pca(object):
    def __init__(self, province='', province_pos=-1):
        self.province = province
        self.province_pos = province_pos

    def propertys_dict(self, pos_sensitive):
        result = {
            "省": self.province,
        }

        if pos_sensitive:
            result["省_pos"] = self.province_pos

        return result

    def __repr__(self):
        return str(self.propertys_dict(pos_sensitive=False))