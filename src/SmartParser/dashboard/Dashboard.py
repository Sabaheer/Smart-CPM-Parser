import json
import string

from flask import Flask, render_template, request, redirect, flash, jsonify

# import helper
from dashboard.EtihadDb import EtihadDb
from dashboard.GrammarDB import grammar_db  
from dashboard.EtihadUtils import EtihadUtils
from parser.Parser import Parser, helper
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from dashboard.GrammarDB import GrammarDB
from dashboard.AirportCodes import AirportCodes

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Etihadly():
    def suggestion(self, partDict):
        pass

    def decorate(self, partDict):
        if "allwrong" in partDict:
            return f"<span class='allwrong'>{partDict['part']}</span>"

        if "possible" in partDict:
            posibilities = str(", ".join(partDict["possible"]))

            return f"<div class='justdiv'><span class='error'>" \
                   f"{partDict['part']}" \
                   f"<p class='myTooltip'>" \
                   f"Did you mean? {posibilities}<br/>" \
                   f"<a href='#' onclick='alert(\"changed in this file\")' >This file...</a>: {posibilities}<br/>" \
                   f"<a href='#' onclick='window.open(\"/create_rule\")'>Create rule</a></p>" \
                   f"</span></div>"

        return partDict["part"]

    def build(self, backmatch, sis):
        res = ""
        for line in backmatch:
            for part in line:
                res += self.decorate(part)
            res += "\n"

        return res + sis


@app.route('/rules', methods=['GET']) # show rules page
def show_rules():
    return render_template("rules.html")




@app.route('/analysis', methods=['GET']) # view the monthly and daily analysis. 
def show_analysis():
    all_errors = EtihadDb().get_errors()
    print(all_errors)

    common = EtihadUtils().analyze_common_mistake(all_errors)

    return render_template("analysis.html",
                           all_errors=all_errors,
                           error_num=len(all_errors),
                           common_errors=common)


@app.route('/create_rule', methods=['GET']) # create rule page
def create_rule():
    return render_template("create_rule.html")




@app.route('/show_file', methods=['GET']) # show a file 
def show_file():
    filename = request.args.get('file', default=None, type=str)
    if filename == None:
        return render_template("index.html",
                               dbfiles=EtihadDb("db.db").get_file_list())

    source = ""

    tmp = filename.split("_")
    if len(tmp) > 1:
        source = tmp[0]

    content = EtihadDb().get_file_content(source, filename)
    if content:
        # print(content)
        p = Parser()
        res = p.parse_text(content)
        si = res.get("SI")
        sis = ""
        for l in si:
            sis += l + '\n'
        return render_template("index.html",
                               header=res.get("header"),
                               carrier=res.get("Carrier"),
                               ULDs=res.get("ULDs"),
                               Bulks = res.get("Bulks"),
                               SI = si,
                               etihadly=Etihadly().build(p.backmatches, sis),
                               dbfiles=EtihadDb("db.db").get_file_list(),
                               filename=filename,
                               json_result=json.dumps(res, indent=2))

    return render_template("index.html",
                           header=None,
                           carrier=None,
                           ULDs=None,
                           etihadly=None,
                           SI = None,
                           dbfiles=EtihadDb("db.db").get_file_list())


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        print("post")
        content = request.form.get("editor")
        content = content.replace("\\r\\n", "\n")
        filename = request.form.get("filename")
        EtihadUtils().addFile(filename, content)

    return redirect(f"show_file?file={filename}")


@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == "POST":
        files = request.files.getlist("file")
        db = EtihadDb()
        for file in files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            print("adding file", filename)

            EtihadUtils().addFile(file.filename, helper.load_file_simple(filename))
            # db.add_file(file.filename, helper.load_file_simple(filename))
        return redirect(f"show_file?file={file.filename}")

    return redirect("show_file")


@app.route('/', methods=['GET', 'POST']) # show the main page
def index():
    return render_template('index.html', dbfiles=EtihadDb("db.db").get_file_list())

@app.route('/grammar', methods=['GET']) # create grammar page
def show_grammar():
    return render_template("grammar.html", Gr_Rules = GrammarDB("grammar.db").get_all_rules())
@app.route('/airportcodes', methods=['GET', 'POST']) # show airport codes
def show_airports():
    return render_template("AirportCodes.html", aircodes = AirportCodes("airport.db").get_all_codes())

@app.route("/grammar_rules", methods=['GET'])
def grammar_rules():
    rules = grammar_db.get_all_rules()
    # separate out Header, Carrier, and ULD rules
    header_rules = []
    carrier_rules = []
    uld_rules = []
    blk_rule = []

    for rule in rules:
        if rule["Section"] == "Header":
            header_rules.append(rule)
        elif rule["Section"] == "Carrier":
            carrier_rules.append(rule)
        elif rule["Section"] == "ULDs":
            uld_rules.append(rule)
        elif rule["Section"] == "BLK":
            blk_rule.append(rule)
    return render_template("grammar.html", header_rules=header_rules, carrier_rules=carrier_rules, uld_rules=uld_rules,blk_rule=blk_rule)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)