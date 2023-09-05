import numpy as np
from Keyboard import Keyboard

class Matcher:
    def __init__(self, kb, dl):
        self.keyboard = kb
        self.data_list = dl

    def edit_dist(self, s1, s2):
        table = np.zeros((len(s1)+1, len(s2)+1))
        u = self.keyboard.std_key_diff
        for i in range(len(s1)):
            table[i+1][0] = table[i][0]+u
        for j in range(len(s2)):
            table[0][j+1] = table[0][j]+u

        for i in range(len(s1)):
            for j in range(len(s2)):
                table[i+1][j+1] = min(table[i][j]+self.keyboard.key_distance(s1[i], s2[j]), table[i+1][j]+u, table[i][j+1]+u)
        #print(table)
        return table[len(s1)][len(s2)]

    def str_dist(self, s1, s2):
        if len(s1) == len(s2):
            if s1 == s2:
                return 0
            for i in range(len(s1)-1):
                if s1 == s2[:i]+s2[i+1]+s2[i]+s2[i+2:]:
                    return self.keyboard.std_key_diff

        return self.edit_dist(s1,s2)

    def k_match(self, ips, k):
        min_k = [self.data_list[0]]
        min_dist = [self.str_dist(ips, min_k[0])]
        for data in self.data_list[1:]:
            d = self.str_dist(ips, data)
            if d < min_dist[0]:
                min_k = [data] + min_k
                min_dist = [d] + min_dist
            elif d < min_dist[-1]:
                for i in range(len(min_k)):
                    if d > min_dist[i]:
                        min_dist = min_dist[:i+1] + [d] + min_dist[i+1:]
                        min_k = min_k[:i+1] + [data] + min_k[i+1:]
                        break
            else:
                min_k.append(data)
                min_dist.append(d)
            if len(min_k) > k:
                min_k = min_k[:k]
                min_dist = min_dist[:k]
        return min_k, min_dist

'''m = Matcher(Keyboard(1,1), ["JFK","ABC","QWE"])
print(m.k_match("WE",2))
print(m.edit_dist("QWE","QQ"))'''
