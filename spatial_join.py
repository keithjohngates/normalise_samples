# Function to join the points to the buffers
import geopandas as gpd


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
