import math

def radian_to_degree(r):
    return r * 180 / math.pi

def degree_to_radian(degree):
    return (360 - degree)*math.pi / 180;

def inv_radian_to_degree(r):
    return 360 - radian_to_degree(r)

def angle(c, a, b, no_inv=True):
    if c[1] == b[1] and c[0] < b[0]:
        return 0
    elif c[1] == b[1] and c[0] > b[0] :
        return 180
    elif c[0] == b[0] and c[1] == b[1]:
        return 0
    else :
        ac = math.sqrt((c[0]-a[0])**2 + (c[1]-a[1])**2)
        bc = math.sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2)
        ab = math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)
        if no_inv:
            return radian_to_degree(math.acos((bc*bc + ac*ac - ab*ab)/(2*bc*ac)))
        else:
            return inv_radian_to_degree(math.acos((bc*bc + ac*ac - ab*ab)/(2*bc*ac)))
