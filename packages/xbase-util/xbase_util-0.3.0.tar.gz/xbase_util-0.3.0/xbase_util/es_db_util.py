import os.path


class EsDb:
    def __init__(self, req, manager):
        self.req = req
        self.internals = manager.dict()
        print("初始化:Elasticsearch DB")

    def get_file_by_file_id(self, node, num, prefix=None):
        key = f'{node}!{num}'
        if key in self.internals:
            return self.internals[key]
        res = self.req.search_file(f"{node}-{num}")
        try:
            hits = res.json()['hits']['hits']
            if len(hits) > 0:
                file = hits[0]['_source']
                if prefix is None:
                    return file
                prefix_res = prefix
                if not prefix.endswith('/'):
                    prefix_res = f"{prefix}/"
                origin_path = file['name']
                basename = os.path.basename(origin_path)
                result_path = f"{prefix_res}{basename}"
                file['name'] = result_path
                self.internals[key] = file
                return file
        except Exception as e:
            print(f"获取es文件失败：{node}-{num}\n\n{res.text}")
        return None
