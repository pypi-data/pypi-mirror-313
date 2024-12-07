import json
import os
import re
from urllib.parse import urlparse, parse_qs

import execjs
import numpy as np
import tldextract
from scapy.layers.dns import DNS

from xbase_util.xbase_constant import parse_path, dns_domain_list


def process_origin_pos(originPos):
    temres = (f"{originPos}"
              .replace("]", "")
              .replace("[", "")
              .replace("\\", "")
              .replace("\"", "")
              .replace(" ", "")
              .split(","))
    return [int(f"{i}") for i in temres]


def parse_expression(expression):
    if expression:
        with open(parse_path, "r") as f:
            ctx = execjs.compile(f.read())
            return eval(ctx.call("parse_exp", expression))
    else:
        return None


def get_cookie_end_with_semicolon_count(text_data):
    count = 0
    for text in text_data.replace("-", "_").lower().split("\n"):
        item_text = text.replace("\n", "").replace("\t", "").replace(" ", "")
        if "cookie:" in item_text and f"{item_text}".endswith(";"):
            count = count + 1
    if count == 0:
        return -1
    return len(count)


def get_ua_duplicate_count(text_data):
    ua_list = []
    for text in text_data.replace("-", "_").lower().split("\n"):
        item_text = text.replace("\n", "").replace("\t", "").replace(" ", "")
        if "user_agent:" in item_text and f"{item_text}".endswith(";"):
            ua_list.append(item_text.replace("user_agent:", ""))
    count = list(set(ua_list))
    if count == 0:
        return -1
    return sum(count)


def get_res_status_code_list(text_data):
    value_res = []
    res = []
    num_1 = 0
    num_2 = 0
    num_3 = 0
    num_4 = 0
    num_5 = 0

    res.extend([item for item in text_data.split("\n") if item.startswith("HTTP/")])
    for item in res:
        m = re.search(r"\b(\d{3})\b", item)
        if m:
            value_res.append(int(m.group(0)))
    for value in value_res:
        if 0 <= value < 200:
            num_1 = num_1 + 1
        if 200 <= value < 300:
            num_2 = num_2 + 1
        if 300 <= value < 400:
            num_3 = num_3 + 1
        if 400 <= value < 500:
            num_4 = num_4 + 1
        if 500 <= value < 600:
            num_5 = num_5 + 1
    return num_1, num_2, num_3, num_4, num_5


def get_packets_percentage(session, isReq):
    if "source.bytes" in session and "destination.bytes" in session:
        total_bytes = session["source.bytes"] + session["destination.bytes"]
        if total_bytes > 0:
            if isReq:
                return session["source.bytes"] / total_bytes
            else:
                return session["destination.bytes"] / total_bytes
        else:
            return 0.0  # 避免除以0的情况
    else:
        return 0.5


def split_samples(sample, per_subsection):
    num_subsections = len(sample) // per_subsection
    remainder = len(sample) % per_subsection
    subsection_sizes = [per_subsection] * num_subsections
    if remainder > 0:
        subsection_sizes.append(remainder)
        num_subsections += 1
    return num_subsections, subsection_sizes


def split_process(subsection, process_count):
    subsection_per_process = len(subsection) // process_count
    remainder = len(subsection) % process_count
    lengths = []
    start = 0
    for i in range(process_count):
        end = start + subsection_per_process + (1 if i < remainder else 0)
        lengths.append(end - start)
        start = end
    return lengths


def build_es_expression(size, start_time, end_time, arkime_expression):
    expression = {"query": {"bool": {"filter": []}}}
    try:
        if size:
            expression['size'] = size
        if start_time:
            expression['query']['bool']['filter'].append(
                {"range": {"firstPacket": {"gte": round(start_time.timestamp() * 1000)}}})
        if end_time:
            expression['query']['bool']['filter'].append(
                {"range": {"lastPacket": {"lte": round(end_time.timestamp() * 1000)}}})
        arkime_2_es = parse_expression(arkime_expression)
        if arkime_2_es:
            expression['query']['bool']['filter'].append(arkime_2_es)
        return expression
    except Exception as e:
        print(f"请安装nodejs{e}")
        print(arkime_expression)
        exit(1)


def get_uri_depth(url):
    match = re.match(r'^[^?]*', url)
    if match:
        path = match.group(0)
        # 去除协议和域名部分
        path = re.sub(r'^https?://[^/]+', '', path)
        segments = [segment for segment in path.split('/') if segment]
        return len(segments)
    return 0


def firstOrZero(param):
    if type(param).__name__ == 'list':
        if (len(param)) != 0:
            return param[0]
        else:
            return 0
    else:
        return 0


def get_statistic_fields(packets):
    length_ranges = {
        "0_19": (0, 19),
        "20_39": (20, 39),
        "40_79": (40, 79),
        "80_159": (80, 159),
        "160_319": (160, 319),
        "320_639": (320, 639),
        "640_1279": (640, 1279),
        "1280_2559": (1280, 2559),
        "2560_5119": (2560, 5119),
        "more_than_5120": (5120, float('inf'))
    }

    def get_length_range(le):
        for key, (min_len, max_len) in length_ranges.items():
            if min_len <= le <= max_len:
                return key
        return "more_than_5120"

    packet_lengths = {key: [] for key in length_ranges}
    total_length = 0
    packet_len_total_count = len(packets)
    for packet_item in packets:
        length = len(packet_item)
        length_range = get_length_range(length)
        packet_lengths[length_range].append(length)
        total_length += length
    total_time = packets[-1].time - packets[0].time if packet_len_total_count > 1 else 1
    packet_len_average = round(total_length / packet_len_total_count, 5) if packet_len_total_count > 0 else 0
    packet_len_min = min(len(packet_item) for packet_item in packets) if packets else 0
    packet_len_max = max(len(packet_item) for packet_item in packets) if packets else 0
    packet_len_rate = round((packet_len_total_count / total_time) / 1000, 5) if total_time > 0 else 0
    packet_size = [len(p) for p in packets]
    field_map = {
        "packet_size_mean": float(round(np.mean(packet_size), 5)),
        "packet_size_variance": float(round(np.var(packet_size), 5)),
        'packet_len_total_count': packet_len_total_count,
        'packet_len_total_average': packet_len_average,
        'packet_len_total_min': packet_len_min,
        'packet_len_total_max': packet_len_max,
        'packet_len_total_rate': float(packet_len_rate),
        'packet_len_total_percent': 1,
    }
    for length_range, lengths in packet_lengths.items():
        count = len(lengths)
        if count > 0:
            average = round(sum(lengths) / count, 5)
            min_val = min(lengths)
            max_val = max(lengths)
        else:
            average = min_val = max_val = 0
        packet_len_rate = round((count / total_time) / 1000, 5) if total_time > 0 else 0
        percent = round(count / packet_len_total_count, 5) if packet_len_total_count > 0 else 0
        field_map.update({
            f"packet_len_{length_range}_count": count,
            f"packet_len_{length_range}_average": average,
            f"packet_len_{length_range}_min": min_val,
            f"packet_len_{length_range}_max": max_val,
            f"packet_len_{length_range}_rate": float(packet_len_rate),
            f"packet_len_{length_range}_percent": percent
        })
    return field_map


def get_dns_domain(packets):
    domain_name = ""
    for packet_item in packets:
        if DNS in packet_item:
            dns_layer = packet_item[DNS]
            if dns_layer.qd:
                try:
                    domain_name = dns_layer.qd.qname.decode('utf-8')
                    # print(f"dns域名:{domain_name}")
                except Exception:
                    domain_name = str(dns_layer.qd.qname)
                    print(f"dns域名编码失败的字符串:{domain_name}")
                break
    if domain_name.endswith("."):
        domain_name = domain_name[:-1]
    return domain_name


def extract_session_fields(origin_list, geoUtil):
    res = []
    for item in origin_list:
        _source = item.get("_source", {})
        source = _source.get("source", {})
        tcpflags = _source.get("tcpflags", {})
        destination = _source.get("destination", {})
        http = _source.get("http", {})
        dns = _source.get("dns", {})
        tls = _source.get("tls", {})
        uri = http.get('uri', [])
        uri_length = [len(u) for u in uri]
        uri_depth = [get_uri_depth(u) for u in uri]
        uri_filename_length = [get_uri_filename_length(u) for u in uri]
        uri_params = [get_url_param_count(u) for u in uri]
        res.append(geoUtil.get_geo_by_ip({
            "id": item["_id"],
            "node": _source.get("node", ""),
            "segmentCnt": _source.get("segmentCnt", 0),
            "tcpflags.rst": tcpflags.get("rst", 0),
            "tcpflags.ack": tcpflags.get("ack", 0),
            "tcpflags.syn": tcpflags.get("syn", 0),
            "tcpflags.urg": tcpflags.get("urg", 0),
            "tcpflags.psh": tcpflags.get("psh", 0),
            "tcpflags.syn-ack": tcpflags.get("syn-ack", 0),
            "tcpflags.fin": tcpflags.get("fin", 0),
            "source.ip": source.get("ip", ""),
            "destination.ip": destination.get("ip", ""),
            "source.port": source.get("port", ""),
            "source.packets": source.get("packets", ""),
            "source.bytes": source.get("bytes", 0),
            "destination.port": destination.get("port", ""),
            "destination.bytes": destination.get("bytes", 0),
            "destination.packets": destination.get("packets", 0),
            "initRTT": _source.get("initRTT", ""),
            "firstPacket": _source.get("firstPacket", 0),
            "lastPacket": _source.get("lastPacket", 0),
            "ipProtocol": _source.get("ipProtocol", 0),
            "protocolCnt": _source.get("protocolCnt", 0),
            "protocol": _source.get("protocol", []),
            "server.bytes": _source.get("server", {}).get("bytes", 0),
            "totDataBytes": _source.get("totDataBytes", 0),
            "network.packets": _source.get("network", {}).get("packets", 0),
            "network.bytes": _source.get("network", {}).get("bytes", 0),
            "length": _source.get("length", 0),
            "client.bytes": _source.get("client", {}).get("bytes", 0),
            "http.uri": uri,
            "http.uri_length_mean": round(np.nan_to_num(np.mean(uri_length)), 5),
            "http.uri_length_var": round(np.nan_to_num(np.var(uri_length)), 5),
            "http.uri_param_count_mean": round(np.nan_to_num(np.mean(uri_params)), 5),
            "http.uri_param_count_var": round(np.nan_to_num(np.var(uri_params)), 5),
            "http.uri_depth_mean": round(np.nan_to_num(np.mean(uri_depth)), 5),
            "http.uri_depth_var": round(np.nan_to_num(np.var(uri_depth)), 5),
            "http.uri_filename_length_mean": round(np.nan_to_num(np.mean(uri_filename_length)), 5),
            "http.uri_filename_length_var": round(np.nan_to_num(np.var(uri_filename_length)), 5),

            "http.response-content-type": http.get("response-content-type", []),
            "http.bodyMagicCnt": http.get("bodyMagicCnt", 0),
            "http.statuscodeCnt": http.get("statusCodeCnt", 0),
            "http.clientVersionCnt": http.get("clientVersionCnt", 0),
            "http.response-content-typeCnt": http.get("response-content-typeCnt", 0),
            "http.xffIpCnt": http.get("xffIpCnt", 0),
            "http.requestHeaderCnt": http.get("requestHeaderCnt", 0),
            "http.serverVersion": http.get("serverVersion", []),
            "http.serverVersionCnt": http.get("serverVersionCnt", 0),
            "http.responseHeaderCnt": http.get("responseHeaderCnt", 0),
            "http.xffIp": http.get("xffIp", []),
            "http.clientVersion": http.get("clientVersion", []),
            "http.uriTokens": http.get("uriTokens", ""),
            "http.useragentCnt": http.get("useragentCnt", 0),
            "http.statuscode": http.get("statusCode", []),
            "http.bodyMagic": http.get("bodyMagic", []),
            "http.request-content-type": http.get("request-content-type", []),
            "http.uriCnt": http.get("uriCnt", 0),

            "http.useragent": http.get("useragent", ""),
            "http.keyCnt": http.get("keyCnt", 0),
            "http.request-referer": http.get("requestReferer", []),
            "http.request-refererCnt": http.get("requestRefererCnt", 0),
            "http.path": http.get("path", []),
            "http.hostCnt": http.get("hostCnt", 0),
            "http.response-server": http.get("response-server", []),
            "http.pathCnt": http.get("pathCnt", 0),
            "http.useragentTokens": http.get("useragentTokens", ""),
            "http.methodCnt": http.get("methodCnt", 0),
            "http.method": http.get("method", []),
            "http.method-GET": http.get("method-GET", 0),
            "http.method-POST": http.get("method-POST", 0),
            "http.key": http.get("key", []),
            "http.hostTokens": http.get("hostTokens", ""),
            "http.requestHeader": http.get("requestHeader", []),
            "http.responseHeader": http.get("responseHeader", []),

            "dns.ASN": dns.get("ASN", []),
            "dns.RIR": dns.get("RIR", []),
            "dns.GEO": dns.get("GEO", []),
            "dns.alpn": dns.get("https.alpn", []),
            "dns.alpnCnt": dns.get("https.alpnCnt", 0),
            "dns.ip": dns.get("ip", []),
            "dns.ipCnt": dns.get("ipCnt", 0),
            "dns.OpCode": dns.get("opcode", []),
            "dns.OpCodeCnt": dns.get("opcodeCnt", 0),
            "dns.Puny": dns.get("puny", []),
            "dns.PunyCnt": dns.get("puntCnt", 0),
            "dns.QueryClass": dns.get("qc", []),
            "dns.QueryClassCnt": dns.get("qcCnt", 0),
            "dns.QueryType": dns.get("qt", []),
            "dns.QueryTypeCnt": dns.get("qtCnt", 0),
            "dns.status": dns.get("status", []),
            "dns.hostCnt": json.dumps(dns.get("hostCnt", 0)),
            "dns.host": json.dumps(dns.get("host", [])),
            "dns.statusCnt": dns.get("statusCnt", 0),

            "tls.cipher": tls.get("cipher", []),
            "tls.cipherCnt": tls.get("cipherCnt", 0),
            "tls.dstSessionId": tls.get("dstSessionId", []),
            "tls.ja3": tls.get("ja3", []),
            "tls.ja3Cnt": tls.get("ja3Cnt", 0),
            "tls.ja3s": tls.get("ja3s", []),
            "tls.ja3sCnt": tls.get("ja3sCnt", 0),
            "tls.ja4": tls.get("ja4", []),
            "tls.ja4Cnt": tls.get("ja4Cnt", 0),
            "tls.srcSessionId": tls.get("srcSessionId", []),
            "tls.version": tls.get("version", []),
            "tls.versionCnt": tls.get("versionCnt", 0),
            "tls.ja4_r": tls.get("versionCnt", 0),
            "tls.ja4_rCnt": tls.get("versionCnt", 0),
            "packetPos": json.dumps(_source.get("packetPos", [])),
            "traffic_type": item.get("traffic_type", ""),
            "PROTOCOL": item.get("PROTOCOL", ""),
            "DENY_METHOD": item.get("DENY_METHOD", ""),
            "THREAT_SUMMARY": item.get("THREAT_SUMMARY", ""),
            "SEVERITY": item.get("SEVERITY", ""),
        }))
    return res


def get_url_param_count(url):
    query = urlparse(url).query  # 解析 URL 中的查询字符串
    params = parse_qs(query)  # 解析查询字符串为字典
    return len(params)


def get_uri_filename_length(uri):
    match = re.search(r'\.([^./?#]+)$', uri)
    if match:
        extension = match.group(0)
        return len(extension)
    return 0


def get_dns_domain_suffix(domain, dns_lock):
    with dns_lock:
        try:
            for tmp_suffix in dns_domain_list:
                if tmp_suffix in domain:
                    return tmp_suffix
            extracted = tldextract.extract(domain)
            return extracted.suffix
        except Exception as e:
            return ""


def check_path(file_path: str):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return file_path


def get_project_root(project_name):
    current_directory = os.getcwd()
    while current_directory != os.path.dirname(current_directory):
        if os.path.basename(current_directory) == project_name:
            return f"{current_directory}{os.sep}"
        current_directory = os.path.dirname(current_directory)
    return None
