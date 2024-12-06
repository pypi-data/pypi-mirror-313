# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from .api import quantim
from .utils import get_csv_separator

class risk_data(quantim):
    def __init__(self, username, password, secretpool, env="pdn", api_url=None):
        super().__init__(username, password, secretpool, env, api_url)

    def load_ports_alm_co(self, file_name, overwrite=False, sep='|'):
        '''
        Load portfolio file to s3.
        '''
        payload = pd.read_csv(file_name, sep=sep).to_dict(orient='records')
        data = {'bucket':'condor-sura-alm', 'file_name':'portfolios/co/'+file_name.split('/')[-1], 'payload':payload, 'sep':sep, 'overwrite':overwrite}
        try:
            resp = self.api_call('load_data_s3', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}
        return resp

    def load_master_limits(self, file_name, overwrite=True, sep=';'):
        '''
        Load portfolio file to s3.
        '''
        payload = pd.read_csv(file_name, sep=sep).to_dict(orient='records')
        data = {'bucket':'condor-sura', 'file_name':'inputs/risk/static/'+file_name.split('/')[-1], 'payload':payload, 'sep':sep, 'overwrite':overwrite}
        try:
            resp = self.api_call('load_data_s3', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}
        return resp

    def get_limits(self, portfolio):
        '''
        Get limits table.
        '''

        data = {'portfolio':portfolio.to_dict(orient="records")}
        resp = self.api_call('limits', method="post", data=data, verify=False)
        summ, detail = pd.DataFrame(resp['summ']), pd.DataFrame(resp['detail'])

        return port_date, summ, detail

    def run_limits(self, ref_date=None):
        '''
        Run limits table.
        ref_date: str (%Y-%m-%d)
        '''
        if ref_date is None:
            data = {'jobname':'job_limits_co'}
        else:
            data = {'jobname':'job_limits_co', "add_args":{"--ref_date":ref_date}}
        try:
            resp = self.api_call('run_glue_job', method="post", data=data, verify=False)
            msg = "La ejecucion de límites se ha activado exitosamente!" if resp=='RUNNING' else "Error. No se ha activado el proceso de límites."
            print(msg)
        except:
            raise ValueError("Error: No se ha podido iniciar el proceso de límites o ya existe una ejecución en curso. Intente de nuevo en algunos minutos.")
        return resp

    def get_portfolio(self, client_id=None, port_type=None, ref_date=None):
        '''
        Get portfolio
        
        '''
        data = {'client_id':client_id, 'port_type':port_type, 'ref_date':ref_date}
        resp = self.api_call('portfolio', method="post", data=data, verify=False)

        portfolio, port_dur, port_per_msg, limits = pd.DataFrame(resp['portfolio']), resp['port_dur'], resp['port_per_msg'], resp['limits']
        limits_summ =  pd.DataFrame(limits['summ'])
        return portfolio, port_dur, port_per_msg, limits_summ

    def get_cashflows(self, client_id=None, port_type=None):
        '''
        Get cashflows
        '''
        data = [{'key':'client_id', 'value':client_id}, {'key':'port_type', 'value':port_type}] if client_id is not None else None
        resp = self.api_call('port_cashflows', method="post", data=data, verify=False)
        port_cfs = pd.DataFrame(resp)
        return port_cfs

    def get_value_at_risk(self, bucket="condor-sura", prefix="output/fixed_income/co/var/", sep=',', ref_date=None):
        '''
        Get Value at Risk results and suport information.
        '''
        ref_date = (dt.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - rd(days=1)).strftime("%Y%m%d") if ref_date is None else ref_date
        files = ["var", "bond_cf", "exp_cps", "bond_float", "exp_cca", "exp_fx", "exp_eq"] 

        try:
            dfs = {}
            for file_i in files: 
                dfs[file_i] = self.retrieve_s3_df(bucket, f'{prefix}{ref_date}/{file_i}_{ref_date}.csv', sep=sep)
                print(f'{file_i} ready!')
            dfs = dfs.values()
        except:
            print(f"Files not available for {ref_date}!")
            dfs = None
        return dfs

    def load_limits_params(self, file_path, encoding='latin-1'):
        '''
        Load limits parameters file to s3.
        '''
        # Validate filename:
        sep=';'
        filename = file_path.split('/')[-1]
        if filename.split('.')[-1]!='csv':
            raise ValueError('Extension must be csv. Please check file.')
        if not np.any(np.in1d(filename.split('.')[-2], ['LIMITES_GEN', 'LIMITES_GEN_AGG', 'EMISIONES', 'Agregacion'])):
            raise ValueError('You can only load LIMITES_GEN.csv, LIMITES_GEN_AGG.csv, EMISIONES.csv or Agregacion.csv. Please check file name.')

        resp = self.upload_with_presigned_url(file_path, "condor-sura", f"inputs/risk/static/{filename}")
        return resp

    def get_irl(self, ref_date=None, return_cfs=False):
        '''
        Get cashflows
        '''
        data = {'ref_date':ref_date, 'return_cfs':return_cfs}
        resp = self.api_call('irl', method="post", data=data, verify=False)
        irl_report = pd.DataFrame(resp['irl'])
        cfs = pd.read_csv(resp['cf_url']) if return_cfs else None

        return irl_report, cfs

    def load_series_cl(self, file_path_performance=None, file_path_peers=None):
        '''
        Load series Chile to s3.
        '''
        # Load data
        if file_path_performance is not None:
            resp = self.upload_with_presigned_url(file_path_performance, "condor-sura", "inputs/benchmarks/performance/cl/performance.csv")
        if file_path_peers is not None:
            resp = self.upload_with_presigned_url(file_path_peers, "condor-sura", "inputs/benchmarks/peers/cl/peers.csv")
        return resp

    def load_pat_co(self, file_path, country="CO"):
        '''
        Load series Chile to s3.
        '''
        # Load data
        resp = self.upload_with_presigned_url(file_path, "condor-pat", f"inputs/portfolio_ledger/{country}/BD_Isin.csv")
        return resp

    def load_bs(self, file_path):
        '''
        Load buys and sells.
        '''
        # Load data
        filename = file_path.split("/")[-1]
        resp = self.upload_with_presigned_url(file_path, "condor-sura", f"inputs/portfolios/buy_sell/CO/{filename}")
        return resp

    def load_navs(self, file_path, country='CO'):
        '''
        Load fund series (NAVs).
        '''
        # Load data

        if country=='CO':
            filename = file_path.split("/")[-1]
            if filename not in ['BD_PAS.csv']:
                raise ValueError('file name not supported.')
            else:
                resp = self.upload_with_presigned_url(file_path, "condor-sura", f"inputs/portfolios/nav/CO/{filename}")
        else:
            raise ValueError("country not supported.")
        return resp

    def port_contrib(self, start_date, end_date, names, groupers=["secType"], subgroup=False):
        '''
        Portfolio risk an return ex-post contribution.
        '''
        hist_class = True
        return_all_dates = True
        data = {'start_date': start_date,'end_date':end_date,"groupers":groupers ,'portfolioNames':names, "hist_class":hist_class, "subgroup":subgroup, "return_all_dates":return_all_dates}
        resp = self.api_call('port_pat', method="post", data=data, verify=False)
        metrics = pd.DataFrame(resp['metrics'])
        ref_dates = resp['ref_dates']

        return metrics, ref_dates

    def port_alpha(self, start_date, end_date, name, groupers=["secType"], subgroup=False):
        '''
        Portfolio risk an return ex-post attribution.
        '''
        hist_class = True
        verbose = False
        return_all_dates = True

        data = {'start_date': start_date,'end_date':end_date,"groupers":groupers ,'portfolioName':name, 'benchmarkName':f"{name}_BMK", "verbose":verbose, "hist_class":hist_class, "subgroup":subgroup, "return_all_dates":return_all_dates}
        resp = self.api_call('port_alpha', method="post", data=data, verify=False)
        metrics = pd.DataFrame(resp['attribution'])
        ref_dates = resp['ref_dates']

        return metrics, ref_dates
