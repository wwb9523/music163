# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import jieba





if __name__=='__main__':
    file='comment/Where Did You Sleep Last Night.txt'
    data = pd.read_table(file, header=None, encoding='utf-8', delim_whitespace=True, index_col=None)