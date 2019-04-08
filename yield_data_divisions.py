# Generator function to subdivide the samples according to rin and sample types


def yield_data_divisions(rins):
    """Divide the data
    
    params:
        Group by object of samples grouped by rin
    returns:
        yields a tuple (rin, sampleType, sampleData)"""
    # For each rin...
    for rin, rindata in rins:
        stypes = rindata.groupby(['SAMPCODE'])
        
        # For each sample type...
        for stype, rin_stype_data in stypes:
            yield (rin, stype, rin_stype_data)
