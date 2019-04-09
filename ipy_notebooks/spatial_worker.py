import helper
import pandas as pd
import geopandas as gpd
import os
import pickle

# Counter to check the output is valid
def spatial_worker(rins_sub, index):
	all_buffers = gpd.GeoDataFrame()
	sbuffered_samples = gpd.GeoDataFrame()
	mbuffered_samples = gpd.GeoDataFrame()
	all_buffered_samples = gpd.GeoDataFrame()
	
	total_samples = 0
	
	dsfolder = os.path.join(os.path.dirname(os.getcwd()), 'data_src')
	
	for rin, stype, subsamples in helper.data_divisions(rins_sub):
		
		# We buffer all the samples
		buffers = helper.buffering(subsamples)
		
		print(rin, stype, len(subsamples), buffers.geom_type)
		
		total_samples = total_samples + len(subsamples)
		
		if buffers.geom_type == 'Polygon':
			
			# For each of the single wkt polygons convert to a dataframe (adding attributes)
			_df = helper.sb_attributes(buffers)
			assert isinstance(_df, gpd.GeoDataFrame)

			# Aggregate the buffers
			all_buffers = gpd.GeoDataFrame(pd.concat([all_buffers, _df], ignore_index=True))
			
			# Spatial join the samples to the buffer
			sbuffered_samples = gpd.sjoin(_df, subsamples, how="inner", op='intersects')
			
			# Aggregate the samples
			all_buffered_samples = gpd.GeoDataFrame(pd.concat([all_buffered_samples, sbuffered_samples], ignore_index=True))

		if buffers.geom_type == 'MultiPolygon':
			
			# Split the Multipolygon wkt to dataframe
			_mdf = helper.mb_attributes(buffers)

			# Set empty frames to collect the subdivided sets
			multisamples = gpd.GeoDataFrame()
			mbuffers = gpd.GeoDataFrame()
			
			# Iterate over the multi-buffer dataframe
			for row, mbuffer in _mdf.groupby('index'):
				assert isinstance(mbuffer, gpd.GeoDataFrame)

				# Aggregate the buffers
				mbuffers = gpd.GeoDataFrame(pd.concat([mbuffers, mbuffer], ignore_index=True))
				
				# Spatially join the samples to the buffers
				mbuffered_samples = gpd.sjoin(mbuffer, subsamples, how="inner", op='intersects')
				
				# Aggregate the samples
				multisamples = gpd.GeoDataFrame(pd.concat([multisamples, mbuffered_samples], ignore_index=True))
			
			# Aggregate the single and multipolygon buffers and samples
			all_buffers = gpd.GeoDataFrame(pd.concat([all_buffers, mbuffers], ignore_index=True))
			all_buffered_samples = gpd.GeoDataFrame(pd.concat([all_buffered_samples, multisamples], ignore_index=True))
			
			# Watch it grow
			print(f'\nCaptured samples: {total_samples} of {len(all_buffered_samples)}\n')
			
	with open(os.path.join(dsfolder, 'rpt_spatial_sub_%s.pickle' % index), 'wb') as f:
		pickle.dump(all_buffered_samples, f, pickle.HIGHEST_PROTOCOL)