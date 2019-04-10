import pickle
import os
import geopandas as gpd
from shapely.geometry import Point

def coordinate_conversion_4283(df_pickle, index):
	data_fout = os.path.join(os.path.dirname(os.getcwd()), 'data_out')
    
	with open(os.path.join(data_fout, 'samples_buffered_normalised_%d.pickle' % index), 'rb') as f:
		print(index)
		samples = pickle.load(f)
		
		# Make geometry field wkt (Well Known Text)
		samples['Coordinates_4283'] = list(zip(samples.LNG94.round(6), samples.LAT94.round(6))) # Round to 6dp
		samples['Coordinates_4283'] = samples['Coordinates_4283'].apply(Point)
		samples = gpd.GeoDataFrame(samples, geometry='Coordinates_4283', crs={'init' :'epsg:4283'})

	with open(os.path.join(data_fout, 'samples_buffered_normalised_4283_%d.pickle' % index), 'wb') as f:
		pickle.dump(samples, f, pickle.HIGHEST_PROTOCOL)


def coordinate_conversion_3112(df_pickle, index):
	data_fout = os.path.join(os.path.dirname(os.getcwd()), 'data_out')
    
	with open(os.path.join(data_fout, 'samples_buffered_normalised_%d.pickle' % index), 'rb') as f:
		print(index)
		samples = pickle.load(f)
		
		# Make geometry field wkt (Well Known Text)
		samples['Coordinates_3112'] = list(zip(samples.EASTING, samples.NORTHING)) # Round to 6dp
		samples['Coordinates_3112'] = samples['Coordinates_3112'].apply(Point)
		samples = gpd.GeoDataFrame(samples, geometry='Coordinates_3112', crs={'init' :'epsg:3112'})
		
	with open(os.path.join(data_fout, 'samples_buffered_normalised_3112_%d.pickle' % index), 'wb') as f:
		pickle.dump(samples, f, pickle.HIGHEST_PROTOCOL)




