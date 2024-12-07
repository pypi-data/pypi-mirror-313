import json
import re
import traceback
from urllib.parse import unquote

import pandas as pd
from tqdm import tqdm



def handle_uri(data):
    tqdm.pandas()
    print(f"处理URI:{len(data)}")
    # 定义正则表达式，确保精确匹配各种攻击特征
    regex_patterns = {
        "sql": re.compile(
            r"\b(select|union|insert|update|delete|drop|--|#| or |' or '|information_schema|database\(\)|version\(\))\b",
            re.IGNORECASE),
        "xss": re.compile(r"(<script\b|javascript:|onload=|onclick=|<iframe\b|src=)", re.IGNORECASE),
        "cmd": re.compile(
            r"(/etc/passwd\b|/etc/shadow\b|;|&&|\||\$\(.+\)|\bcurl\b|\bwget\b|\bexec\b|\bsystem\b|cmd=|proc/self/environ)",
            re.IGNORECASE),
        "path": re.compile(r"(\.\./|\.\.%2f|\.\.%5c|\.\.\\|\.\.;|%2f%2e%2e%2f)", re.IGNORECASE),
        "redirect": re.compile(r"(redirect=|url=|next=|redirect_uri=|redirect:|RedirectTo=)", re.IGNORECASE),
        "danger": re.compile(
            r"(%3C|%3E|%27|%22|%00|%2F|%5C|%3B|%7C|%28|%29|%20|%3D|%3A|%3F|%26|%23|%2B|%25|file://|<foo|xmlns:|/etc/passwd|windows/win\.ini)",
            re.IGNORECASE),
        "suspicious_ext": re.compile(
            r"\.(exe|sh|py|pl|bak|php5|jspx|bat|cmd|pif|js|vbs|vbe|sct|ini|inf|tmp|swp|jar|java|class|ps1)\b",
            re.IGNORECASE)
    }

    # 定义多层解码函数，确保完全解码 URI
    def fully_decode_uri(uri):
        try:
            decoded_uri = str(uri)
            for _ in range(3):  # 尝试多次解码嵌套的编码
                decoded_uri = unquote(decoded_uri)
            return decoded_uri
        except Exception as e:
            return uri

    def process_row(row):
        uris = row['http.uri']
        if not isinstance(uris, list):
            try:
                uris = json.loads(uris)
                if not isinstance(uris, list):
                    uris = [str(uris)]
            except Exception:
                uris = [str(uris)]
        try:
            decoded_uris = [fully_decode_uri(uri) for uri in uris]
        except Exception as e:
            traceback.print_exc()
            exit(0)


        # 初始化统计变量
        param_count = 0
        path_depth = 0
        param_lengths = []
        feature_flags = {key: False for key in regex_patterns.keys()}

        # 遍历解码后的 URI
        for uri in decoded_uris:
            param_count += uri.count('&') + 1
            path_depth += uri.count('/')

            # 提取参数长度
            if '?' in uri:
                params = uri.split('?', 1)[-1].split('&')
                for param in params:
                    if '=' in param:
                        _, value = param.split('=', 1)
                        param_lengths.append(len(value))

            # 检查正则匹配特征
            for key, pattern in regex_patterns.items():
                if pattern.search(uri):
                    feature_flags[key] = True

        # 计算参数长度的统计值
        avg_length = sum(param_lengths) / len(param_lengths) if param_lengths else 0
        max_length = max(param_lengths) if param_lengths else 0

        # 创建返回结果字典
        result = {
            "URI_FEATURES_EXTRA_param_count": param_count,
            "URI_FEATURES_EXTRA_path_depth": path_depth,
            "URI_FEATURES_EXTRA_param_length_avg": avg_length,
            "URI_FEATURES_EXTRA_param_length_max": max_length,
        }

        # 添加特征标志到结果
        for key, value in feature_flags.items():
            result[f"URI_FEATURES_EXTRA_contains_{key}"] = value

        return result
    feature_data = data.progress_apply(process_row, axis=1, result_type="expand")
    data = pd.concat([data, feature_data], axis=1)
    return data


def handle_ua(data):
    tqdm.pandas()
    print("处理UA")
    data['http.useragent'] = data['http.useragent'].fillna('').astype(str)
    # 处理换行符及多余空格
    data['http.useragent'] = data['http.useragent'].str.replace(r'\s+', ' ', regex=True)
    # 常见攻击的 User-Agent 字符串匹配模式，忽略大小写
    attack_patterns = '|'.join([
        r"\bselect\b", r"\bunion\b", r"\binsert\b", r"\bupdate\b", r"\bdelete\b", r"\bdrop\b", r"--", r"#", r" or ",
        r"' or '",
        r"information_schema", r"database\(\)", r"version\(\)",  # SQL注入相关
        r"<script>", r"javascript:", r"onload=", r"onclick=", r"<iframe>", r"src=",  # XSS相关
        r"/etc/passwd", r"/etc/shadow", r"\&\&", r"\|", r"\$\(\)", r"exec", r"system",  # 命令执行相关
        r"\.\./", r"\.\.%2f", r"\.\.%5c", r"%c0%af", r"%252e%252e%252f",  # 路径遍历
        r"\.php", r"\.asp", r"\.jsp", r"\.exe", r"\.sh", r"\.py", r"\.pl",  # 文件扩展名
        r"redirect=", r"url=", r"next=",  # 重定向
        r"%3C", r"%3E", r"%27", r"%22", r"%00", r"%2F", r"%5C", r"%3B", r"%7C", r"%2E", r"%28", r"%29",  # 编码
        r'Googlebot', r'Bingbot', r'Slurp', r'curl', r'wget', r'Nmap',
        r'SQLMap', r'Nikto', r'Dirbuster', r'python-requests', r'Apache-HttpClient',
        r'Postman', r'Burp Suite', r'Fuzzing', r'nessus'
    ])
    # 企业客户端 User-Agent 模式
    enterprise_patterns = '|'.join([
        r'MicroMessenger', r'wxwork', r'QQ/', r'QQBrowser', r'Alipay', r'UCWEB'
    ])
    # 批量检查是否为攻击的 User-Agent，忽略大小写
    data['UserAgent_is_attack'] = data['http.useragent'].str.contains(attack_patterns, case=False, regex=True)
    # 批量检查是否为企业客户端，忽略大小写
    data['UserAgent_is_enterprise'] = data['http.useragent'].str.contains(enterprise_patterns, case=False)
    # 提取浏览器和版本
    data['UserAgent_browser'] = data['http.useragent'].str.extract(r'(Chrome|Firefox|Safari|MSIE|Edge|Opera|Trident)',
                                                                   expand=False, flags=re.IGNORECASE).fillna("Unknown")
    data['UserAgent_browser_version'] = data['http.useragent'].str.extract(
        r'Chrome/([\d\.]+)|Firefox/([\d\.]+)|Version/([\d\.]+).*Safari|MSIE ([\d\.]+)|Edge/([\d\.]+)|Opera/([\d\.]+)|Trident/([\d\.]+)',
        expand=False, flags=re.IGNORECASE).bfill(axis=1).fillna("Unknown").iloc[:, 0]
    # 提取操作系统和版本
    os_info = data['http.useragent'].str.extract(
        r'(Windows NT [\d\.]+|Mac OS X [\d_\.]+|Linux|Android [\d\.]+|iOS [\d_\.]+|Ubuntu|Debian|CentOS|Red Hat)',
        expand=False, flags=re.IGNORECASE)
    data['UserAgent_os'] = os_info.str.extract(r'(Windows|Mac OS X|Linux|Android|iOS|Ubuntu|Debian|CentOS|Red Hat)',
                                               expand=False, flags=re.IGNORECASE).fillna("Unknown")
    data['UserAgent_os_version'] = os_info.str.extract(r'([\d\._]+)', expand=False).fillna("Unknown")
    # 提取设备类型，忽略大小写
    data['UserAgent_device_type'] = data['http.useragent'].str.contains('mobile|android|iphone', case=False).map(
        {True: 'Mobile', False: 'Desktop'})
    # 提取硬件平台，增加对 x64 的匹配
    data['UserAgent_platform'] = data['http.useragent'].str.extract(r'(x86|x86_64|arm|arm64|x64)', expand=False,
                                                                    flags=re.IGNORECASE).fillna('Unknown')
    # 判断是否为爬虫，忽略大小写
    data['UserAgent_is_bot'] = data['http.useragent'].str.contains('bot|crawler|spider|slurp|curl|wget|httpclient',
                                                                   case=False)
    # 提取语言偏好（如果存在），忽略大小写
    data['UserAgent_language'] = data['http.useragent'].str.extract(r'\b([a-z]{2}-[A-Z]{2})\b', expand=False,
                                                                    flags=re.IGNORECASE).fillna("Unknown")
    # 统计 User-Agent 中的特殊字符个数
    data['UserAgent_special_char_count'] = data['http.useragent'].progress_apply(
        lambda x: len(re.findall(r'[!@#$%^&*\'=:|{}]', x, flags=re.IGNORECASE)))
    # 更新 UserAgent_is_unknown 的计算逻辑
    data['UserAgent_is_unknown'] = data[['UserAgent_browser', 'UserAgent_os', 'UserAgent_platform']].isna().any(
        axis=1).fillna("Unknown")
    return data
