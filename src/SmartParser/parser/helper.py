from pathlib import Path



def load_file_simple(filename):
    f = open(filename, "r")
    content = f.read()
    f.close()
    return content

def load_file(filename):

    content = Path(filename).read_text().splitlines()

    return content


def load_file_list(filename):

    content = None
    with open(filename) as f:
        res = []
        for line in f:
            res += [line.strip()]
        return res

    return []
