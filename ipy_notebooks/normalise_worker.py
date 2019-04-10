import pandas as pd
from pysal.viz.mapclassify import Natural_Breaks as nb
# from math import log10
import pickle
import os
import pandas as pd
import geopandas as gpd
import numpy as np

def calc_normalisation(group, f, elements):
	data_out = os.path.join(os.path.dirname(os.getcwd()), 'data_out')
	
	normalised = gpd.GeoDataFrame()
    
	for subset, samples in group.groupby(['RIN', 'index']):
	
		print(subset)
		
		df = normalise(samples, elements)
		normalised = gpd.GeoDataFrame(pd.concat([normalised, df], ignore_index=True))

	with open(os.path.join(data_out, "samples_buffered_normalised_%s.pickle" % f), 'wb') as fout:
		pickle.dump(normalised, fout, pickle.HIGHEST_PROTOCOL)

def normalise(df, elements):

	for element in elements:
	
		df[element].fillna(np.nan, inplace=True)
		
		df['%s_nn' % element] = pd.to_numeric(df['%s' % element])
		
		df['%s_nn' % element].fillna(np.nan, inplace=True)

		df['%s_fn' % element] = df['%s_nn' % element].apply(lambda x: neg_conversions(x))
		
		df['%s_fn' % element].fillna(np.nan, inplace=True)

		df['%s_log' % element] = df['%s_fn' % element].apply(lambda x: np.log10(x))

		median = df['%s_log' % element].median()
		
		# Mean Absolute Deviation: Tukey, J.W., 1977. Exploratory Data Analysis. Addison-Wesley, Reading, 688 pp
		mad = df['%s_log' % element].mad()
		
		# Set threshold: http://crcleme.org.au/Pubs/guides/gawler/a7_id_anomalies.pdf
		threshold = median + (mad+mad)
		
		min_value = df['%s_log' % element].min()
		max_value = df['%s_log' % element].max()
		
		df['%s_nml' % element] = df['%s_log' % element].apply(lambda x: scaling(x, min_value, max_value))
		
		# histogram = df['%s_nml' % element].hist()
		

		# classifier = nb(df['%s_log' % element], 7)
		# df['classifications'] = df['%s_log' % element].apply(classifier)
		# df.classifications.replace([1, 2, 3, 4, 5, 6, 7], ['#82817d', '#55b1d9', '#5bd955', '#e6a94e', '#e02d2d', '#da2de0', '#af00b5'], inplace=True)
	print('Normalised')
	return df

def neg_conversions(x):
	# Define the negative conversions
	if x < -1:
		return np.nan
	if x < 0:
		return abs(x)/2
	if x == 0:
		return np.nan
	if x > 0:
		return x


def scaling(x, min_value, max_value): # tried the threshold didn't work
	# Normalisation of values between 0 and 1
	
	x = (x - min_value) / (max_value - min_value)  # 'Max' value is the threshold
	return x
