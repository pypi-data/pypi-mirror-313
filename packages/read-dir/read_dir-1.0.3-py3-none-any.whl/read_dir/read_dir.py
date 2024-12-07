# -*- coding: utf-8 -*-
# @Time    : 2024/12/5 4:41 下午
# @Author  : dubaichuan
# @File    :read_dir.py
# @Software: PyCharm

import os
import pandas as pd


class read_dir(object):
    def __init__(self, a):
        self.a = a

    def to_pd(self):
        text = []
        label = []
        for j in os.listdir(f'text classification/{self.a}')[1:]:
            for i in os.listdir(f'text classification/{self.a}/{j}'):
                try:
                    with open(f'text classification/{self.a}/{j}/{i}', 'r', encoding='gbk') as f:
                        text.append(f.read())
                        label.append(j)
                except:
                    continue
        return pd.DataFrame({'text': text, 'label': label})
