import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #set standard output default encoding


def isinpolygon(point, vertex_lst: list, contain_boundary=True):
    lngaxis, lataxis = zip(*vertex_lst)
    minlng, maxlng = min(lngaxis), max(lngaxis)
    minlat, maxlat = min(lataxis), max(lataxis)
    lng, lat = point
    if contain_boundary:
        isin = (minlng <= lng <= maxlng) & (minlat <= lat <= maxlat)
    else:
        isin = (minlng < lng < maxlng) & (minlat < lat < maxlat)
    return isin


def isintersect(poi, spoi, epoi):
    lng, lat = poi
    slng, slat = spoi
    elng, elat = epoi
    if poi == spoi:
        return None
    if slat == elat:
        return False
    if slat > lat and elat > lat:
        return False
    if slat < lat and elat < lat:
        return False
    if slat == lat and elat > lat:
        return False
    if elat == lat and slat > lat:
        return False
    if slng < lng and elat < lat:
        return False
    xseg = elng - (elng - slng) * (elat - lat) / (elat - slat)
    if xseg == lng:
        return None
    if xseg < lng:
        return False
    return True


def isin_multipolygon(poi, vertex_lst, contain_boundary=True):
    if not isinpolygon(poi, vertex_lst, contain_boundary):
        return False
    sinsc = 0
    for spoi, epoi in zip(vertex_lst[:-1], vertex_lst[1::]):
        intersect = isintersect(poi, spoi, epoi)
        if intersect is None:
            return (False, True)[contain_boundary]
        elif intersect:
            sinsc += 1
    return sinsc % 2 == 1


if __name__ == '__main__':
    vertex_lst = [[0, 0], [1, 1], [1, 2], [0, 2], [0, 0]]
    poi = [3, 4]
    print(isin_multipolygon(poi, vertex_lst, contain_boundary=True))
