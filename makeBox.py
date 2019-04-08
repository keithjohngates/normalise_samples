from shapely import geometry


class Box(object):
    def __init__(self, borigin: tuple, bsize: float):
        self.borigin = borigin
        self.bsize = bsize
        
        self.xmin = self.borigin[0]
        self.xmax = self.borigin[0] + self.bsize
        self.ymin = self.borigin[1]
        self.ymax = self.borigin[1] + self.bsize
        
    def makebox(self):
        self.boxgeom = geometry.box(self.xmin, self.ymin, self.xmax, self.ymax)
        self.boxgeom_wkt = self.boxgeom.wkt
        self.centroid_wkt = self.boxgeom.centroid.wkt
