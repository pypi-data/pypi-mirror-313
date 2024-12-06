import re

import geoip2.database

from xbase_util.xbase_constant import geo_path


class GeoUtil:
    def __init__(self):
        self.reader = geoip2.database.Reader(geo_path)
        print("初始化:GeoUtil")

    @staticmethod
    def is_stable_name(ip):
        ip_match = r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)\.)(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(?:25[0-4]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)$"
        if re.match(ip_match, ip):
            # 分割IP地址
            octets = ip.split('.')
            first_octet = int(octets[0])
            second_octet = int(octets[1])
            # 判断是否是本地地址
            if ip == "10.28.0.0" or ip.startswith("10.28.0.") or ip.startswith("10.28.0.0/16"):
                return "LOCAL_ADDRESS"
            # 判断是否是VPN地址
            if ip.startswith("10.28.15"):
                return "VPN_ADDRESS"
            # 判断是否是分支机构地址
            if (192 <= first_octet <= 195) or (first_octet == 192 and 144 <= second_octet <= 255):
                return "DEPARTMENT_ADDRESS"
        else:
            return False

    @staticmethod
    def fill_geo_empty(value):
        if value == "" or value is None:
            return "IP_GEO_EMPTY"
        else:
            return value

    def get_geo_by_ip(self, geo_map):
        source_ip = geo_map["source.ip"]
        source_ip_name = self.is_stable_name(source_ip)
        if source_ip_name is not False:
            try:
                response = self.reader.city(source_ip)
                geo_map["source.ip_Country_IsoCode"] = self.fill_geo_empty(response.country.iso_code)
                geo_map['source.ip_Country_Name'] = self.fill_geo_empty(response.country.name)
                geo_map["source.ip_Country_SpecificName"] = self.fill_geo_empty(
                    response.subdivisions.most_specific.name)
                geo_map['source.ip_Country_SpecificIsoCode'] = self.fill_geo_empty(
                    response.subdivisions.most_specific.iso_code)
                geo_map['source.ip_City_Name'] = self.fill_geo_empty(response.city.name)
                geo_map['source.ip_City_PostalCode'] = self.fill_geo_empty(response.postal.code)
                geo_map['source.ip_Location_Latitude'] = self.fill_geo_empty(response.location.latitude)
                geo_map["source.ip_Location_Longitude"] = self.fill_geo_empty(response.location.longitude)
            except Exception as e:
                geo_map["source.ip_Country_IsoCode"] = "IP_GEO_EMPTY"
                geo_map['source.ip_Country_Name'] = "IP_GEO_EMPTY"
                geo_map["source.ip_Country_SpecificName"] = "IP_GEO_EMPTY"
                geo_map['source.ip_Country_SpecificIsoCode'] = "IP_GEO_EMPTY"
                geo_map['source.ip_City_Name'] = "IP_GEO_EMPTY"
                geo_map['source.ip_City_PostalCode'] = "IP_GEO_EMPTY"
                geo_map['source.ip_Location_Latitude'] = "IP_GEO_EMPTY"
                geo_map["source.ip_Location_Longitude"] = "IP_GEO_EMPTY"
        else:
            geo_map["source.ip_Country_IsoCode"] = source_ip_name
            geo_map['source.ip_Country_Name'] = source_ip_name
            geo_map["source.ip_Country_SpecificName"] = source_ip_name
            geo_map['source.ip_Country_SpecificIsoCode'] = source_ip_name
            geo_map['source.ip_City_Name'] = source_ip_name
            geo_map['source.ip_City_PostalCode'] = source_ip_name
            geo_map['source.ip_Location_Latitude'] = source_ip_name
            geo_map["source.ip_Location_Longitude"] = source_ip_name
        destination_ip = geo_map["destination.ip"]
        destination_ip_name = self.is_stable_name(destination_ip)
        if destination_ip_name is not False:
            try:
                response = self.reader.city(destination_ip)
                geo_map["destination.ip_Country_IsoCode"] = self.fill_geo_empty(response.country.iso_code)
                geo_map['destination.ip_Country_Name'] = self.fill_geo_empty(response.country.name)
                geo_map["destination.ip_Country_SpecificName"] = self.fill_geo_empty(
                    response.subdivisions.most_specific.name)
                geo_map['destination.ip_Country_SpecificIsoCode'] = self.fill_geo_empty(
                    response.subdivisions.most_specific.iso_code)
                geo_map['destination.ip_City_Name'] = self.fill_geo_empty(response.city.name)
                geo_map['destination.ip_City_PostalCode'] = self.fill_geo_empty(response.postal.code)
                geo_map['destination.ip_Location_Latitude'] = self.fill_geo_empty(response.location.latitude)
                geo_map["destination.ip_Location_Longitude"] = self.fill_geo_empty(response.location.longitude)
            except Exception:
                geo_map["destination.ip_Country_IsoCode"] = "IP_GEO_EMPTY"
                geo_map['destination.ip_Country_Name'] = "IP_GEO_EMPTY"
                geo_map["destination.ip_Country_SpecificName"] = "IP_GEO_EMPTY"
                geo_map['destination.ip_Country_SpecificIsoCode'] = "IP_GEO_EMPTY"
                geo_map['destination.ip_City_Name'] = "IP_GEO_EMPTY"
                geo_map['destination.ip_City_PostalCode'] = "IP_GEO_EMPTY"
                geo_map['destination.ip_Location_Latitude'] = "IP_GEO_EMPTY"
                geo_map["destination.ip_Location_Longitude"] = "IP_GEO_EMPTY"
        else:
            geo_map["destination.ip_Country_IsoCode"] = destination_ip_name
            geo_map['destination.ip_Country_Name'] = destination_ip_name
            geo_map["destination.ip_Country_SpecificName"] = destination_ip_name
            geo_map['destination.ip_Country_SpecificIsoCode'] = destination_ip_name
            geo_map['destination.ip_City_Name'] = destination_ip_name
            geo_map['destination.ip_City_PostalCode'] = destination_ip_name
            geo_map['destination.ip_Location_Latitude'] = destination_ip_name
            geo_map["destination.ip_Location_Longitude"] = destination_ip_name
        return geo_map
