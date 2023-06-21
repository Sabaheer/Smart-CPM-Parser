class Keyboard:
    QWERTY = 1
    QWERTZ = 2
    AZERTY = 3
    QZERTY = 4
    MANHATTAN_DISTANCE = 1
    EUCLID_DISTANCE = 2
    SCALE = 3
    MAX_Y = 4
    
    def __init__(self,layout,dist_type):
        self.keys = []
        self.shift_vec = [0,5,6,8]
        self.dist_type = dist_type
        match layout:
            case self.QWERTY:
                self.keys = [
                    "`1234567890-=",
                    "QWERTYUIOP[]",
                    "ASDFGHJKL;'",
                    "ZXCVBNM,./"
                ]
            case self.QWERTZ:
                self.keys = [
                    "`1234567890-=",
                    "QWERTZUIOP[]",
                    "ASDFGHJKL;'",
                    "YXCVBNM,./"
                ]
            case self.AZERTY:
                self.keys = [
                    "`1234567890-=",
                    "AZERTYUIOP[]",
                    "QSDFGHJKLM;'",
                    "WXCVBN,./"
                ]
            case self.QZERTY:
                self.keys = [
                    "`1234567890-=",
                    "QZERTYUIOP[]",
                    "ASDFGHJKLM;'",
                    "WXCVBN,./"
                ]
        self.std_key_diff = self.key_distance('H','U')

    
    def key_coord(self,key):
        for i in range(self.MAX_Y):
            MAX_X = len(self.keys[i])
            for j in range(MAX_X):
                if key == self.keys[i][j]:
                    return (self.SCALE*i, 
                        self.SCALE*j+self.shift_vec[i])
        return (-1,-1)

    def key_distance(self, key1, key2):
        if key2 == '?':
            return 1
        x1,y1 = self.key_coord(key1)
        x2,y2 = self.key_coord(key2)
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            return 100
        match self.dist_type:
            case self.MANHATTAN_DISTANCE:
                return abs(x1-x2)+abs(y1-y2)
            case self.EUCLID_DISTANCE:
                return pow(pow(x1-x2,2)+pow(y1-y2,2), 0.5)
        return -1

    def direct_diff(self, str1, str2):
        if str1 == "" and str2 == "":
            return 0
        if str1 == "":
            return self.std_key_diff * len(str2)
        if str2 == "":
            return self.std_key_diff * len(str1)
        return self.key_distance(str1[0], str2[0]) + self.direct_diff(str1[1:], str2[1:])

str = "qwer"
print(str[:0]+str[2])