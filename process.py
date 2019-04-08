from normalise_funcs import *
import geopandas as gpd
import pandas as pd
import pickle
import pandas as pd
normalised = gpd.GeoDataFrame()

def calc_normalisation(group, f, normalised=normalised):
    
    for subset, samples in group.groupby(['RIN','index']):
        df = normalise(samples, 'Au_ppm')
        normalised = gpd.GeoDataFrame(pd.concat([normalised, df], ignore_index=True))

    with open(fr"E:\sunset\broken_hill_surface_samples_normalised_{f}.pickle", 'wb') as fout:
            pickle.dump(normalised, fout, pickle.HIGHEST_PROTOCOL)

    return len(normalised)
