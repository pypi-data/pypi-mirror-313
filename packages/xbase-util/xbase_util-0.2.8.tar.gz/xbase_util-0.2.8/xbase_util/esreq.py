import requests


class EsReq:
    def __init__(self, url, timeout=120):
        self.es_url = url
        self.timeout = timeout
        print("初始化自定义es请求类")

    def clear_all_scroll(self):
        return requests.delete(self.es_url + "/_search/scroll", timeout=self.timeout, json={'scroll_id': '_all'})

    def search(self, body, index=""):
        if not index.startswith("/"):
            index = "/" + index
        return requests.post(self.es_url + f"{index}/_search", timeout=self.timeout, json=body)

    def start_scroll(self, exp, scroll, index=""):
        if not index.startswith("/"):
            index = "/" + index
        return requests.post(self.es_url + f"{index}/_search?scroll={scroll}", timeout=self.timeout,
                             json=exp)

    def scroll_by_id(self, scroll_id, scroll):
        return requests.post(self.es_url + "/_search/scroll", timeout=self.timeout,
                             json={'scroll_id': scroll_id, 'scroll': scroll})

    def search_file(self, id):
        return requests.post(f"{self.es_url}/arkime_files_v30/_search", timeout=self.timeout,
                             json={"query": {"term": {"_id": id}}})
