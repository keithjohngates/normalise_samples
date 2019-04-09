import pandas as pd
from pysal.viz.mapclassify import Natural_Breaks as nb
from math import log10
import pickle
import os

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


def normalise(df, index, element):
	dsfolder = os.path.join(os.path.dirname(os.getcwd()), 'data_src')

	df[element].fillna(0, inplace=True)
	
	df['%s_nn' % element] = pd.to_numeric(df['%s' % element])

	df['%s_fn' % element] = df['%s_nn' % element].apply(lambda x: neg_conversions(x))

	df['%s_log' % element] = df['%s_fn' % element].apply(lambda x: log10(x))

	median = df['%s_log' % element].median()

	# Mean Absolute Deviation: Tukey, J.W., 1977. Exploratory Data Analysis. Addison-Wesley, Reading, 688 pp
	mad = df['%s_log' % element].mad()

	# Set threshold: http://crcleme.org.au/Pubs/guides/gawler/a7_id_anomalies.pdf
	threshold = median + 2*mad
	min_value = df['%s_log' % element].min()
	
	df['normalised'] = df['%s_log' % element].apply(lambda x: scaling(x, min_value, threshold))
	classifier = nb(df['%s_log' % element], 7)
	df['classifications'] = df['%s_log' % element].apply(classifier)
	df.classifications.replace([1, 2, 3, 4, 5, 6, 7], ['#82817d', '#55b1d9', '#5bd955', '#e6a94e', '#e02d2d', '#da2de0', '#af00b5'], inplace=True)

	with open(os.path.join(dsfolder, 'rpt_spatial_sub_normalised_%s.pickle' % index), 'wb') as f:
		pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
