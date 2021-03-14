from collections import defaultdict


class AddrMap(defaultdict):
    def __init__(self):
        super().__init__(lambda: [[], None])

    def get_full_name(self, key):
        return self[key][1]

    def is_unique_value(self, key):
        if key not in self.keys():
            return False
        return len(self.get_relational_addrs(key)) == 1

    def get_relational_addrs(self, key):
        return self[key][0]

    def get_value(self, key, pos):
        return self.get_relational_addrs(key)[0][pos]

    def append_relational_addr(self, key, p_tuple, full_name_pos):
        self[key][0].append(p_tuple)
        if not self[key][1]:
            self[key][1] = p_tuple[full_name_pos]