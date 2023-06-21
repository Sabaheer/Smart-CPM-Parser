FIX_THRESHOLD = 2

def ajacent_dup(str):
    for i in range(len(str) - 1):
        if str[i] == str[i + 1]:
            return True
    return False


def long_match_unit(str1, str2):
    res = -1
    if ajacent_dup(str1):
        res = 2
    else:
        res = 5
    combs = []
    for i in range(len(str1)):
        combs.append(str1[:i] + str1[i + 1:])
    for co in combs:
        if co == str2:
            return res
    return -1


def short_match_unit(str1, str2):
    i = 0
    j = 0
    missing = 0
    while i < len(str1) and j < len(str2):
        if str1[i] == str2[j]:
            i += 1
        else:
            missing += 1
        j += 1
        if missing > 1:
            return False
    if len(str2) - j > 1:
        return False
    return missing == 0 or j == len(str2)


def k_nearest(distance_list, data_list, k):
    min_vals = [distance_list[0]]
    k_matches = [[data_list[0]]]
    for i in range(len(distance_list)):
        if min_vals[0] > distance_list[i]:
            min_vals[0] = distance_list[i]
            k_matches[0] = [data_list[i]]
        elif min_vals[0] == distance_list[i]:
            k_matches[0].append(data_list[i])
    if len(k_matches[0]) > k*2:
        return 'SUGGEST',min_vals,k_matches[0][:k*2]
    for j in range(1, k):
        min_vals.append(0)
        k_matches.append([data_list[0]])
        for d in distance_list:
            if d > min_vals[j - 1]:
                min_vals[j] = d
                break
        for i in range(len(distance_list)):
            if min_vals[j] > distance_list[i] > min_vals[j - 1]:
                min_vals[j] = distance_list[i]
                k_matches[j] = [data_list[i]]
            elif min_vals[j] == distance_list[i]:
                k_matches[j].append(data_list[i])
    warn_type = 'SUGGEST'
    if min_vals[1]/min_vals[0] > FIX_THRESHOLD:
        warn_type = 'REPLACE'
    return warn_type, min_vals, k_matches


def equal_match_unit(kb, str1, str2):
    swaps = []
    if len(str1) == 2:
        swaps.append(str1[1] + str1[0])
    else:
        for i in range(len(str1) - 1):
            swaps.append(str1[:i] + str1[i + 1] + str1[i] + str1[i + 2:])
    for sw in swaps:
        if sw == str2:
            return kb.std_key_diff
    return kb.direct_diff(str1, str2)


class Matcher:
    MATCH = 0
    SWAP_MATCH = 1
    SHORT_MATCH = 2
    LONG_MATCH = 3

    def __init__(self, kb, data_list, fixed_length):
        self.keyboard = kb
        self.data_list = data_list
        self.fixed_length = fixed_length

    def all_diff(self, input_str):
        distance_list = []

        if self.fixed_length:
            match len(input_str) - len(self.data_list[0]):
                case 0:
                    if len(input_str) > 1:
                        for data in self.data_list:
                            distance_list.append(equal_match_unit(self.keyboard, input_str, data))
                    else:
                        for data in self.data_list:
                            distance_list.append(self.keyboard.key_distance(input_str, data))
                case 1:
                    if len(input_str) > 2:
                        for data in self.data_list:
                            res = long_match_unit(input_str, data)
                            if res > 0:
                                distance_list.append(res * self.keyboard.std_key_diff)
                            else:
                                distance_list.append(self.keyboard.direct_diff(input_str, data)*5)
                    else:
                        for data in self.data_list:
                            distance_list.append(self.keyboard.key_distance(input_str, data))
                case -1:
                    if len(input_str) > 1:
                        for data in self.data_list:
                            if short_match_unit(input_str, data):
                                distance_list.append(self.keyboard.std_key_diff)
                            else:
                                distance_list.append(self.keyboard.direct_diff(input_str, data))
                    else:
                        for data in self.data_list:
                            distance_list.append(self.keyboard.key_distance(input_str, data))
                case _:
                    for data in self.data_list:
                        distance_list.append(self.keyboard.direct_diff(input_str, data)*5)

        elif len(input_str) == 1:
            for data in self.data_list:
                distance_list.append(self.keyboard.direct_diff(input_str, data))

        elif len(input_str) == 2:
            for data in self.data_list:
                match len(input_str) - len(data):
                    case 0:
                        distance_list.append(equal_match_unit(self.keyboard, input_str, data))
                    case -1:
                        if short_match_unit(input_str, data):
                            distance_list.append(self.keyboard.std_key_diff)
                        else:
                            distance_list.append(self.keyboard.direct_diff(input_str, data))
                    case _:
                        distance_list.append(self.keyboard.direct_diff(input_str, data))

        else:
            for data in self.data_list:
                match len(input_str) - len(data):
                    case 0:
                        distance_list.append(equal_match_unit(self.keyboard, input_str, data))
                    case -1:
                        if short_match_unit(input_str, data):
                            distance_list.append(self.keyboard.std_key_diff)
                        else:
                            distance_list.append(self.keyboard.direct_diff(input_str, data))
                    case 1:
                        res = long_match_unit(input_str, data)
                        if res > 0:
                            distance_list.append(res * self.keyboard.std_key_diff)
                        else:
                            distance_list.append(self.keyboard.direct_diff(input_str, data)*5)
                    case _:
                        distance_list.append(self.keyboard.direct_diff(input_str, data)*5)
        return distance_list

# mt = Matcher(Keyboard(1, 2), create_list("data/airline_codes.txt"), False)
# diffs = mt.all_diff('JL')
# print(k_nearest(diffs,mt.data_list,4))


