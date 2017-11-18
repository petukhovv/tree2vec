import json


class AstReader:
    @staticmethod
    def read(filename):
        f = open(filename, 'r')
        nodes = f.read()
        f.close()
        return json.loads(nodes)
