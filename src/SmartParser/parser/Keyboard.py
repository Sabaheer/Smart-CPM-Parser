class Keyboard:
    
    '''
    layout:
    QWERTY = 1
    QWERTZ = 2
    AZERTY = 3
    QZERTY = 4
    
    distance type:
    MANHATTAN_DISTANCE = 1
    EUCLID_DISTANCE = 2
    '''
    scale = 3
    max_y = 4
    shift_vec = [0,5,6,8]
    
    def __init__(self,layout,dist_type):
        self.dist_type = dist_type
        match layout:
            case 1:
                self.keys = [
                    "`1234567890-=",
                    "QWERTYUIOP[]",
                    "ASDFGHJKL;'",
                    "ZXCVBNM,./"
                ]
            case 2:
                self.keys = [
                    "`1234567890-=",
                    "QWERTZUIOP[]",
                    "ASDFGHJKL;'",
                    "YXCVBNM,./"
                ]
            case 3:
                self.keys = [
                    "`1234567890-=",
                    "AZERTYUIOP[]",
                    "QSDFGHJKLM;'",
                    "WXCVBN,./"
                ]
            case 4:
                self.keys = [
                    "`1234567890-=",
                    "QZERTYUIOP[]",
                    "ASDFGHJKLM;'",
                    "WXCVBN,./"
                ]
        self.std_key_diff = 3*self.key_distance('H','U')

    
    def key_coord(self,key):
        for i in range(Keyboard.max_y):
            for j in range(len(self.keys[i])):
                if key == self.keys[i][j]:
                    return (Keyboard.scale*i, 
                        Keyboard.scale*j+Keyboard.shift_vec[i])
        return (-1,-1)

    def key_distance(self, key1, key2):
        if key2 == '?':
            return 1
        x1,y1 = self.key_coord(key1)
        x2,y2 = self.key_coord(key2)
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            return 100
        match self.dist_type:
            case 1:
                return abs(x1-x2)+abs(y1-y2)
            case 2:
                return pow(pow(x1-x2,2)+pow(y1-y2,2), 0.5)
        return -1
