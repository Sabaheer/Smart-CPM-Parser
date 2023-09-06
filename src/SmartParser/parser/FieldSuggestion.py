from Keyboard import Keyboard
import pandas as pd

from Matcher import Matcher

ULD_CHART = pd.read_excel("data/uld.xls")
ULD_LIST = ULD_CHART["CONCAT"]
ULD_INFO= [["APDMQR","IOT"],["KMPVAWLGQY","IOTCDU"],["EC","IOTQSR"]]
SEC_TOP_RATIO = 2

def create_list(file_path): # we have eliminated empty data lists. 
    f = open(file_path,"r")
    data_list = f.read().splitlines()
    i = 0
    while i < len(data_list):
        if data_list[i] == '0':
            data_list.pop(i)
        else:
            i += 1
    return data_list

def get_val(df,col1,val,col2): # we will use it to get values from columns and rows.
    row = df[df[col1] == val].index[0]
    return df[col2][row]

def airport_airline_registration_check(input_str,field_name,num_match,kb): # We check the registration and manipulate the data according to requirements. 
    path = ""
    match field_name:
        case 'Airport':
            path = "data/airports.txt"
        case 'Airline':
            path = "data/airline_codes.txt"
        case 'Registration':
            path = "data/aircraft registration country codes.txt"
    data_list = create_list(path)
    mc = Matcher(kb,data_list)
    reg_latter = ""
    if field_name == 'Registration':
        if len(input_str) < 5:
            input_str += "AAA"
        for i in range(1,5):
            for data in mc.data_list:
                if input_str[:i] == data:
                    return 'ACCEPT',[]
        reg_latter = input_str[2:] 
        input_str = input_str[:2]
    for data in mc.data_list:
        if input_str == data:
            return 'ACCEPT',[]
    min_k, min_dist = mc.k_match(input_str, num_match)
    if field_name == 'Registration':
        for sug in min_k:
            for j in range(len(sug)):
                sug[j] = sug[j] + reg_latter
    return 'REPLACE',min_k

def uld_check(uld_type,kb,num_match):
    if len(uld_type) != 3:
        return 'REJECT',[]
    valid = True
    for i in range(3):
        if uld_type[i] in ULD_INFO[i][1]:
            valid = False
            break
    if uld_type[0] not in ULD_INFO[0][0] and uld_type[1] not in ULD_INFO[1][0]:
        valid = False
    if not valid:
        distance_list = []
        for data in ULD_LIST:
            distance_list.append(kb.direct_diff(uld_type,data))
        warn_type,min_vals,suggestions = k_nearest(distance_list,ULD_LIST,num_match)
        for i in range(3):
            for sug in suggestions:
                for n in range(len(sug)):
                    if sug[n][i] == '?':
                        diffs = []
                        for c in ULD_INFO[i][0]:
                            diffs.append(kb.key_distance(uld_type[i],c))
                        min_dist = min(diffs)
                        for j in range(len(diffs)):
                            if diffs[j] == min_dist:
                                sug[n] = sug[n][:i]+ULD_INFO[i][0][j]+sug[n][i+1:]
        return warn_type,suggestions
    return 'ACCEPT',[]

def uld_position(uld_type,kb):
    diffs = []
    for data in ULD_LIST:
        diffs.append(kb.direct_diff(uld_type,data))
    min_vals,suggestions = Matcher.k_nearest(diffs,ULD_LIST,2)
    res = [get_val(ULD_CHART,'CONCAT',suggestions[0][0],'POS')]
    if min_vals[0] == 0:
        return res
    elif min_vals[1]/min_vals[0] < SEC_TOP_RATIO:
        res = ["UNKNOWN"]
    elif len(suggestions[0]) > 1:
        for i in range(1,len(suggestions[0])):
            dup = get_val(ULD_CHART,'CONCAT',suggestions[0][i],'POS')
            if dup != res[0]:
                res.append(dup)
    return res

def uld_bay_check(bay):
    suggestions = []
    if len(bay) >= 2:
        if bay[0] in "IO" or len(bay) > 3:
            if bay[len(bay)-1] in "LRP":
                for c in "KJLUP98":
                    suggestions.append(c+bay[len(bay)-1])
            else:
                cs = "JKU"
                if bay[0] == 'O':
                    cs = "KLP"
                for c in cs:
                    for d in "LRP":
                        suggestions.append(c+d)
        elif bay[1] in "IO":
            for d in "LRP":
                suggestions.append(bay[0]+d)
        elif bay[len(bay)-1] not in "LPR":
            for c in "LPR":
                suggestions.append(bay[:len(bay)-1]+c)
    elif bay[0] == 'I':
        for c in "JK89U":
            suggestions.append(c)
    elif bay[0] == 'O':
        for c in "KLP9":
            suggestions.append(c)
    if suggestions == []:
        return 'ACCEPT',suggestions
    return 'SUGGEST',suggestions

def weight_check(pos,w):
    weight_lim = get_val(ULD_CHART,'POS',pos,'Max gross weight')
    if weight_lim == 'NaN' or weight_lim <= weight_lim:
        return 'ACCEPT'
    return 'REJECT'

def date_check(d):
    if 1 <= d <= 31:
        return 'ACCEPT'
    return 'REJECT'

def contour_check(input_str):
    suggestions = []
    for c in "16":
        for d in ["Q7","Q6","X5"]:
            suggestions.append('P'+c+"P/"+d)
    if input_str not in suggestions:
        return 'SUGGEST',suggestions
    return 'ACCEPT',[]

#See performance
keyboard = Keyboard(1,2)
#Test example input
num_suggestions = 4
airports = ["JFL","JFJR","JEQ","DDD","AB","IEPWI","C"]
airlines = ["3E","CZ","JDP","C","JDOEP","AA","353"]
reg = ["A6DDD","J3BABC","DPRDC","KDPAAA","FCZZA","BCD","QQQAAD"]
uld_types = ["AKE","PWA","JEI","BBB","RERR","CD","P6P"]
uld_bays = ["11R","KL","IJO","22PL","JD","123"]
contours = ["P1P/Q5","POPEJ","P6P/AB"]
    
print("airport")
for ap in airports:
    print(airport_airline_registration_check(ap,'Airport',num_suggestions,keyboard))
print("airline")
for al in airlines:
     print(airport_airline_registration_check(al,'Airline',num_suggestions,keyboard))
# print("reg")
# for r in reg:
#     print(airport_airline_registration_check(r,'Registration',num_suggestions,keyboard))
# print("uld")
# for ut in uld_types:
#     print(uld_check(ut,keyboard,num_suggestions))
# print("bays")
# for ub in uld_bays:
#     print(uld_bay_check(ub))
# print("contours")
# for ct in contours:
#     print(contour_check(ct))
