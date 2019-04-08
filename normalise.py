import pandas as pd
from math import log10
from pysal.esda.mapclassify import Natural_Breaks as nb


class FixData(object):
    """"""
    def __init__(self, df, element):
        self.df = df
        self.element = element
    
    def force_numeric(self):
        # Coerce element to numeric values
        self.df[self.element].fillna(0, inplace=True)
        # Coerce element to numeric values
        self.df['%s_nn' % self.element] = pd.to_numeric(self.df[self.element])

    def neg_conversions(self, x):
        # Define the negative conversions
        if x < -5:
            return 0.0005
        if x < 0:
            return abs(x)/2
        if x == 0:
            return 0.0005
        if x > 0:
            return x
        
    def fix_neg(self):
        self.df['%s_fn' % self.element] = self.df[self.element].apply(lambda x: self.neg_conversions(x))

    def log(self):
        self.df['%s_log' % self.element] = self.df['%s_fn' % self.element].apply(lambda x: log10(x))
        
    def threshold(self):
        median = self.df['%s_log' % self.element].median()
        # Mean Absolute Deviation: Tukey, J.W., 1977. Exploratory Data Analysis. Addison-Wesley, Reading, 688 pp
        mad = self.df['%s_log' % self.element].mad()
        # Set threshold: http://crcleme.org.au/Pubs/guides/gawler/a7_id_anomalies.pdf
        self.threshold = median + 2*mad 
        
    def scaling(self, x):
        # Normalisation of values between 0 and 1
        min_value = self.df['%s_log' % self.element].min()
        x = (x - min_value) / (self.threshold - min_value)  # 'Max' value is the threshold
        return x
        
    def apply_scaling(self):
        self.df['normalised'] = self.df['%s_log' % self.element].apply(lambda x: self.scaling(x))

    def natural_breaks(self):
        # Apply hex colours to natural breaks
        classifier = nb(self.df[self.element], 7)  # nb are natural breaks
        self.df['classifications'] = self.df[self.element].apply(classifier)
        self.df.classifications.replace([1, 2, 3, 4, 5, 6, 7], ['#82817d', '#55b1d9', '#5bd955', '#e6a94e', '#e02d2d', '#da2de0', '#af00b5'], inplace=True)
