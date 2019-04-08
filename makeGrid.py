​class makeGrid(object):
    def __init__(self, samples, gorigin: tuple, cellsize: float, nrows_ncols: tuple, Box, gridname = ''):
        
        self.samples = samples
        assert isinstance(self.samples, gpd.GeoDataFrame)
        self.nrows = nrows_ncols[0]
        self.ncols = nrows_ncols[1]
        
        self.cellsize = cellsize
        
        self.gridname = gridname
        self.gorigin = gorigin
        self.gorigin_x = self.gorigin[0]
        self.gorigin_y = self.gorigin[1]
        
        self.gorigin_x = self.gorigin_x - self.cellsize
        self.gorigin_y = self.gorigin_y - self.cellsize
        
        print(f'Grid cellsize: {self.cellsize}, rows: {self.nrows}, cols: {self.ncols}, Origin: {self.gorigin_x} / {self.gorigin_y}')

    def make_rows(self):
        self.rows = []
        for row in range(0, self.nrows):
            self.gorigin_x = self.gorigin_x + self.cellsize
            self.rows.append(self.gorigin_x)
    
    def make_cols(self):
        self.cols = []
        for row in range(0, self.ncols):
            self.gorigin_y = self.gorigin_y + self.cellsize
            self.cols.append(self.gorigin_y)
            
    def make_grid(self):
        
        self.make_rows()
        self.make_cols()
        
        grid_origins = list(itertools.product(self.rows, self.cols))
        
        boxes = []
        colours = []
        
        for i in grid_origins:
            colour = fake.hex_color()
            x = Box(i, self.cellsize)
            x.makebox()
            boxes.append(x.boxgeom)
            colours.append(colour)
        
        grid_origins_dict = {'geometry':  boxes, 'colour': colours}
        
        self.boxes_gdf = gpd.GeoDataFrame(grid_origins_dict, crs={'init' :'epsg:4283'})
        self.boxes_gdf = self.boxes_gdf.set_geometry('geometry')
        
    def export_geojson(self):
        self.boxes_gdf.to_file(f'{self.gridname}_boxes.geojson', driver = 'GeoJSON')