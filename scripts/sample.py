import pandas as pd
import numpy as np

from sys import argv

# read file in
data = pd.read_hdf(argv[1])

# sample from data
sample_size = int(len(data)*20/100)

#seed here
sample = data.sample(sample_size, random_state=1)

# output the sample
sample.to_hdf(argv[2], 'sample')
