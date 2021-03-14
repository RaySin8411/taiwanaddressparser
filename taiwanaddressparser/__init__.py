import os
import pandas as pd

from .structures import AddrMap, Pca

__version__ = "0.0.1"
P = 0
pwd_path = os.path.abspath(os.path.dirname(__file__))
pca_path = os.path.join(pwd_path, 'pca.csv')


def _data_from_csv(pca_path: str):
    province_map = {}

    def _fill_province_map(province_map: dict, record_dict: dict):
        """
        填寫直轄市或省地名 - 第一級分類
        :param province_map:
        :param record_dict:
        :return: province_map
        """
        sheng = record_dict['sheng']
        if sheng not in province_map:
            province_map[sheng] = sheng
            # 省 和 直轄市
            if sheng.endswith('省') or sheng.endswith('市'):
                province_map[sheng[:-1]] = sheng

    with open(pca_path, encoding='utf-8')as f:
        import csv
        pca_csv = csv.DictReader(f)
        for record_dict in pca_csv:
            _fill_province_map(province_map, record_dict)

    return province_map


province_map = _data_from_csv(pca_path)

# 直轄市
munis = {'臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市'}


def is_munis(city_full_name: str):
    return city_full_name in munis


def transform(location_strs, index=None, cut=False, pos_sensitive=False):

    def _handle_one_record(addr, cut, pos_sensitive):

        def _extract_addr(addr, cut):
            return _jieba_extract(addr) if cut else _full_text_extract(addr)

        def _jieba_extract(addr):
            import jieba
            result = Pca()
            pos = 0
            truncate = 0

            def _set_pca(pca_property, name, full_name):
                if not getattr(result, pca_property):
                    setattr(result, pca_property, full_name)
                    setattr(result, pca_property + "_pos", pos)
                    if is_munis(full_name):
                        setattr(result, "province_pos", pos)
                    nonlocal truncate
                    if pos == truncate:
                        truncate += len(name)

            for word in jieba.cut(addr):
                if word in province_map:
                    _set_pca('province', word, province_map[word])

                pos += len(word)

            return result, addr[truncate:]

        if not isinstance(addr, str) or addr == '' or addr is None:
            empty = {'省': ''}
            if pos_sensitive:
                empty['省_pos'] = -1
            return empty

        pca, left_addr = _extract_addr(addr, cut)

        result = pca.propertys_dict(pos_sensitive)
        result["地址"] = left_addr
        return result

    if index is None:
        index = []
    result = pd.DataFrame(
        [_handle_one_record(addr, cut, pos_sensitive) for addr in location_strs], index=index) \
        if index else pd.DataFrame([_handle_one_record(addr, cut, pos_sensitive) for addr in location_strs])
    if pos_sensitive:
        return result.loc[:, ('省', '省_pos')]
    else:
        return result.loc[:, '省']
