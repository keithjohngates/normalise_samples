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