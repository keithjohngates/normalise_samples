# Calculate the origin for the grid and the number of rows and columns based on the cell size


def cell_rows_cols(samples, cell_size):

    minx, miny, maxx, maxy = samples.total_bounds
    
    xmin = minx - (0.5*cell_size)
    ymin = miny - (0.5*cell_size)
    
    width = maxx - minx
    height = maxy - miny

    nrows = abs(width) / cell_size
    ncols = abs(height) / cell_size

    nrows = int(nrows.round()) 
    ncols = int(ncols.round())
    
    return [(xmin, ymin), (nrows + 1, ncols + 1)]
