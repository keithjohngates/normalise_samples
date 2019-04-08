# Function to convert the single buffer polygons to a GeoDataFrame
def sb_attributes(singlebuffer):
    """
    Converts wkt polygon to GeoDataFrame
    
    params:
        wkt: Polygon
    returns:
        GeoDataFrame
    """
    colour = fake.hex_color()
    
    # Set a dictonary to build the attributes for the polygon
    sb_attributes = dict()
    sb_attributes['geometry'] = singlebuffer
    sb_attributes['index'] = [0]
    sb_attributes['stroke'] = [colour]
    # TODO add the RIN as a tooltip
    
    # Covert the dictionary into the GeoDataFrame 
    sb_attributes_df = pd.DataFrame(sb_attributes)
    sb_attributes_gdf = gpd.GeoDataFrame(sb_attributes_df)
    sb_attributes_gdf.columns={'geometry': 'geometry', 'index': 'index', 'stroke': 'stroke'}
    sb_attributes_gdf.crs = {'init' :'epsg:4326'}
    
    return sb_attributes_gdf
	
# Function to convert the multi buffers polygons to a GeoDataFrame
def mb_attributes(multibuffer):
        """
        Converts wkt MultiPolygon to GeoDataFrame

        params:
            wkt: MultiPolygon
        returns:
            GeoDataFrame
        """
        # Set a dictonary to build the attributes for each polygon
        mb_attributes = dict()
        geometry = []
        index = []
        stroke = []
    
        # Loop over each polygon in the MultiPolygon
        for idx, b in enumerate(multibuffer):
            colour = fake.hex_color()
            stroke.append(colour)
            geometry.append(b)
            index.append(idx)
            # TODO add the RIN as a tooltip

            # Populate the dictionary
            mb_attributes['geometry'] = geometry
            mb_attributes['index'] = index
            mb_attributes['stroke'] = stroke
            
        # Covert the dictionary into the GeoDataFrame 
        mb_attributes_df = pd.DataFrame(mb_attributes)
        mb_attributes_gdf = gpd.GeoDataFrame(mb_attributes_df)
        mb_attributes_gdf.columns={'geometry': 'geometry', 'index': 'index', 'stroke': 'stroke'}
        mb_attributes_gdf.crs = {'init' :'epsg:4326'}
        
        return mb_attributes_gdf