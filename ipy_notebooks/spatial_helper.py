import pandas as pd
import geopandas as gpd
from faker import Factory

fake = Factory.create()

# Function to Buffer the points
def buffering(data, distance=2500, resolution=10):
    """
    Buffer points to return polygons of spatially distinct data sets.

    params:
        data: GeoDataFrame
    returns:
        buffer_union: GeoDataFrame of buffers
    """

    buffers = data.buffer(distance, resolution)
    buffer_union = buffers.unary_union
    return buffer_union


# Function to join the points to the buffers
def spatial_join(points, buffers):
    """
    Spatially join points to buffers

    params:
        points: GeoDataFrame containing Points
        buffers: GeoDataFrame containing Points
    returns:
        Combined GeoDataFrame of points and buffers
    """
    points_buffered = gpd.sjoin(points, buffers, how="inner", op='intersects')
    points_buffered.drop(['index_right'], axis=1)
    return points_buffered


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
    sb_attributes_gdf.crs = {'init' :'epsg:3112'}
    
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
        mb_attributes_gdf.crs = {'init' :'epsg:3112'}
        
        return mb_attributes_gdf


# Function to join the points to the buffers
def samples_buffered(points, buffers):
    """
    Spatially join points to buffers

    params:
        points: GeoDataFrame containing Points
        buffers: GeoDataFrame containing Points
    returns:
        Combined GeoDataFrame of points and buffers
    """
    points_buffered = gpd.sjoin(points, buffers, how="inner", op='intersects')
    points_buffered.drop(['index_right'], axis=1)
    return points_buffered


# Generator function to subdivide the samples according to rin and sampletype
def data_divisions(rins):
    """Divide the data
    
    params:
        Groupby object of samples grouped by rin
    returns:
        yields a tuple (rin, sampleType, sampleData)"""
    # For each rin...
    for rin, rindata in rins:
        stypes = rindata.groupby(['SAMPCODE'])
        
        # For each sample type...
        for stype, rin_stype_data in stypes:
            yield (rin, stype, rin_stype_data)