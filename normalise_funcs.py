
import pandas as pd
from pysal.esda.mapclassify import Natural_Breaks as nb
from math import log10
    
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
    
    x = (x - min_value) / (threshold - min_value) # 'Max' value is the threshold 
    return x

def normalise(df, element):

    df[element].fillna(0, inplace=True)

    df[f'{element}_nn'] = pd.to_numeric(df[f'{element}'])

    df[f'{element}_fn'] = df[f'{element}_nn'].apply(lambda x: neg_conversions(x))

    df[f'{element}_log'] = df[f'{element}_fn'].apply(lambda x: log10(x))

    median = df[f'{element}_log'].median()

    # Mean Absolute Deviation: Tukey, J.W., 1977. Exploratory Data Analysis. Addison-Wesley, Reading, 688 pp
    mad = df[f'{element}_log'].mad()  

    # Set threshold: http://crcleme.org.au/Pubs/guides/gawler/a7_id_anomalies.pdf
    threshold = median + 2*mad
    min_value = df[f'{element}_log'].min()
    
    df['normalised'] = df[f'{element}_log'].apply(lambda x: scaling(x, min_value, threshold))

    classifier = nb(df[f'{element}_log'], 7)
    df['classifications'] = df[f'{element}_log'].apply(classifier)
    df.classifications.replace([1,2,3,4,5,6,7], ['#82817d','#55b1d9','#5bd955','#e6a94e','#e02d2d','#da2de0','#af00b5'], inplace=True)

    return df
