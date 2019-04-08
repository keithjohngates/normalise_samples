import geopandas as gpd


def grid_samples(samples, grid):
    
    grid_with_samples = gpd.sjoin(samples, grid, how="inner", op='intersects')
    
    max_vals = grid_with_samples.groupby(['index_right']).agg({'normalised': max})
        
    max_values_grids = grid.boxes_gdf.merge(max_vals, on='index_right')
    
    return max_values_grids

def grid_geojson(max_values_grids, name):
    max_values_grids.to_file('%s.geojson' % name, driver='GeoJSON')
    print('Exported')
