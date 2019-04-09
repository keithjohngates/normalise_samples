import pandas as pd
from pysal.viz.mapclassify import Natural_Breaks as nb
from math import log10
import pickle
import os
import pandas as pd
import geopandas as gpd

def calc_normalisation(group, f, element):
	dsfolder = os.path.join(os.path.dirname(os.getcwd()), 'data_src')
	
	normalised = gpd.GeoDataFrame()
    
	for subset, samples in group.groupby(['RIN', 'index']):
		df = normalise(samples, element)
		normalised = gpd.GeoDataFrame(pd.concat([normalised, df], ignore_index=True))

	with open(os.path.join(dsfolder, "samples_normalised_%s.pickle" % f), 'wb') as fout:
		pickle.dump(normalised, fout, pickle.HIGHEST_PROTOCOL)

def normalise(df, element):
	df[element].fillna(0, inplace=True)
	
	df['%s_nn' % element] = pd.to_numeric(df['%s' % element])

	df['%s_fn' % element] = df['%s_nn' % element].apply(lambda x: neg_conversions(x))

	df['%s_log' % element] = df['%s_fn' % element].apply(lambda x: log10(x))

	median = df['%s_log' % element].median()
	
	print('median %s' % median)
	
	# Mean Absolute Deviation: Tukey, J.W., 1977. Exploratory Data Analysis. Addison-Wesley, Reading, 688 pp
	mad = df['%s_log' % element].mad()
	
	print('mad %s' % mad)
	
	# Set threshold: http://crcleme.org.au/Pubs/guides/gawler/a7_id_anomalies.pdf
	threshold = median + 2*mad
	
	print('threshold %s' % threshold)
	
	min_value = df['%s_log' % element].min()
	
	print('min_value %s' % min_value)
	
	df['normalised'] = df['%s_log' % element].apply(lambda x: scaling(x, min_value, threshold))
	
	print('normalised')
	# classifier = nb(df['%s_log' % element], 7)
	# df['classifications'] = df['%s_log' % element].apply(classifier)
	# df.classifications.replace([1, 2, 3, 4, 5, 6, 7], ['#82817d', '#55b1d9', '#5bd955', '#e6a94e', '#e02d2d', '#da2de0', '#af00b5'], inplace=True)
	return df

def neg_conversions(x):
	# Define the negative conversions
	if x < -5:
		return 0.0005
	if x < 0:
		return abs(x)/2
	if x == 0:
		return 0.0005
	if x > 0:
		return x


def scaling(x, min_value, threshold):
	# Normalisation of values between 0 and 1
	
	x = (x - min_value) / (threshold - min_value)  # 'Max' value is the threshold
	return x
