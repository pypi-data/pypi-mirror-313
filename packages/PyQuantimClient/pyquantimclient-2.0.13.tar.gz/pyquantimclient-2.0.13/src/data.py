# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from .api import quantim

class time_series(quantim):
    def __init__(self, username, password, secretpool, env="pdn", api_url=None):
        super().__init__(username, password, secretpool, env, api_url)

    def get_series(self, tks, ref_curr='Origen', join='outer', since_date='2008-01-01', verify=False):
        '''
        Get series
        '''
        data = {'tks':list(tks), 'ref_curr':ref_curr, 'join':join, 'since_date':since_date}
        resp = self.api_call('get_series', method="post", data=data, verify=verify)
        ts, summ, tks_invalid = pd.DataFrame(resp['ts']).set_index("Date"), pd.DataFrame(resp['summ']), resp['tks_invalid']
        return ts, summ, tks_invalid

    def clustering(self, tks, ref_curr='USD', ini_date=None, ncluster=None, cluster_method='graph', factor_tickers=None, verify=False):
        '''
        Clustering
        '''
        if cluster_method.lower()[:3]!='gra' and ncluster is None:
            raise ValueError('Please provide number of clusters (ncluster)')

        data = {'ref_curr':ref_curr, 'ini_date':ini_date, 'ncluster':ncluster, 'tickers':tks, 'factor_tickers':factor_tickers, 'cluster_method':cluster_method}
        resp = self.api_call('clustering', method="post", data=data, verify=verify)
        clusters, rets_summ, invalid_tickers, valid_dates, factors = pd.Series(resp['clusters']), pd.DataFrame(resp['rets_summ']), resp['invalid_tickers'], resp['valid_dates'], pd.DataFrame(resp['factors']) if resp['factors'] is not None else None
        return clusters, rets_summ, invalid_tickers, valid_dates, factors

class s3(quantim):
    def __init__(self, username, password, secretpool, env="pdn", api_url=None):
        super().__init__(username, password, secretpool, env, api_url)

    def read_file(self, bucket, key, sep=',', verify=False, res_url=False):
        '''
        Get series
        ''' 
        data = {'bucket':bucket, 'key':key, 'sep':sep, 'res_url':res_url}
        resp = self.api_call('retrieve_data_s3', method="post", data=data, verify=verify)

        if res_url:
            output = resp
        else:
            output = pd.DataFrame(resp)
        return output