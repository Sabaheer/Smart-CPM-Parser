from Parser import Parser
from dashboard.EtihadDb import EtihadDb


class EtihadUtils:
    def __init__(self):
        pass

    def addFile(self, filename, content):
        source = ""

        tmp = filename.split("_")
        if len(tmp) > 1:
            source = tmp[0]

        EtihadDb().add_file(source, filename, content)
        self.log(source, filename, content)

    def build_line(self, backmatch):
        res = ""
        for b in backmatch:
            res += b["part"]

        return res


    def log(self, source, filename, content):
        EtihadDb().delete_errors(source, filename)
        print("-----")
        p = Parser()
        res = p.parse_text(content)
        for backmatch in p.backmatches:

            for bitem in backmatch:
                line = self.build_line(backmatch)
                if "wrong" in bitem:
                    EtihadDb().add_error(source, filename, line, bitem["field"], bitem["value"], "value_error")
            print(backmatch)


        print(res)

    def analyzeErrors(self):
        data = EtihadDb().get_errors()

        pass

    def analyze_common_mistake(self, all_errors):
        res = {}
        for error in all_errors:
            key = (error[0], error[3], error[4])
            if key in res:
                res[key] += 1
            else:
                res[key] = 1
            print(error)
        tmp = []
        for key in res:
            tmp += [(key, res[key])]
        tmp.sort(key=lambda tup: tup[1], reverse=True)
        print(tmp)

        return tmp