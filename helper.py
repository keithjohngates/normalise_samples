# Function to Buffer the points
def buffer(data, distance=0.0075, resolution=10):
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
