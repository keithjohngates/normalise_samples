​def grid_samples(samples, grid_gdf):
    
    grid_with_samples = gpd.sjoin(samples, grid_gdf, how="inner", op='intersects')
    
    max_vals = grid_with_samples.groupby(['index_right']).agg({'normalised': max})
        
    max_values_grids = grid.boxes_gdf.merge(max_vals, on='index_right')
    
    return max_values_grids

def grid_geojson(max_values_grids, name):
    max_values_grids.to_file(f'{name}.geojson', driver = 'GeoJSON')
    print('Exported')