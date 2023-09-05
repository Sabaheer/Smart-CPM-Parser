from pathlib import Path


def load_file_simple(filename): # it importes a file to the parser.  
    f = open(filename, "r")
    content = f.read()
    f.close()
    return content

def load_file(filename): # it loads the file to the 

    content = Path(filename).read_text().splitlines()

    return content


def load_file_list(filename): # it loads all the files.

    content = None
    with open(filename) as f:
        res = []
        for line in f:
            res += [line.strip()]
        return res

    return []
