import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mimicry_analyser import MimiAnalyser

ma = MimiAnalyser('data/test_data_filtered.csv')
ma.plotTalkError(3, 'text')
ma.plotTalkError(3, 'Fumoji')