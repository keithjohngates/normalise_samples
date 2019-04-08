# Function to join the points to the buffers
def rin_stype_buffered(points, buffers):
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