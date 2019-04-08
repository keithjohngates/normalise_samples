​def cell_rows_cols(samples, cellsize):

    samples.total_bounds
    
    minx, miny, maxx, maxy = sample_locs.total_bounds
    
    xmin = minx - (0.5*cellsize)
    ymin = miny - (0.5*cellsize)
    
    width = maxx - minx
    height = maxy - miny

    nrows = abs(width) / cellsize
    ncols = abs(height) / cellsize

    nrows = int(nrows.round()) 
    ncols = int(ncols.round())
    
    return [(xmin, ymin), (nrows +1, ncols +1)]