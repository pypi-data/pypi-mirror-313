# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests, json, mimetypes

mimetypes.add_type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','.xlsx')
mimetypes.add_type('application/vnd.ms-excel', '.xls')
mimetypes.add_type('application/vnd.ms-excel.sheet.macroEnabled.12', '.xlsm')
mimetypes.add_type('text/csv','.csv')
mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document','.docx')
mimetypes.add_type('application/msword', '.doc')
mimetypes.add_type('application/pdf', '.pdf')

class quantim:
    def __init__(self, username, password, secretpool, env="pdn", api_url=None):
        self.username = username
        self.password = password
        self.secretpool = secretpool
        self.env = env

        if api_url is None:
            self.api_url = "https://api-quantimqa.sura-im.com/" if env=="qa" else "https://api-quantim.sura-im.com/"
        else:
            self.api_url = api_url

    def get_token(self):
        if self.secretpool=='ALM':
            token_url = f"{self.api_url}token"
            data = {"username":self.username, "password":self.password}
        else:
            token_url = f"{self.api_url}tokendynamicpool"
            data = {"username":self.username, "password":self.password, "secretpool":self.secretpool}

        headers = {"Accept": "*/*",'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        access_token_response = requests.post(token_url, data=json.dumps(data), headers=headers, verify=False, allow_redirects=False)
        tokens = json.loads(access_token_response.text)
        access_token = tokens['id_token']

        return access_token

    def get_header(self):
        '''
        Build request header
        '''
        access_token = self.get_token()
        api_call_headers = {"Accept": "*/*", 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

        return api_call_headers

    def api_call(self, endpoint, method="post", data=None, verify=False):
        '''
        data: when method get, data is an array of key values.
        '''
        api_call_headers = self.get_header()
        api_url = f"{self.api_url}{endpoint}"
        if method.lower()=='post':
            api_call_response = requests.post(api_url, headers=api_call_headers, data=json.dumps(data), verify=verify)
        elif method.lower()=='get':
            if data is not None:
                api_url = api_url + '?'+'&'.join([f"{x['key']}={x['value']}" for x in data])
            api_call_response = requests.get(api_url, headers=api_call_headers, data=None, verify=verify)
        else:
            print("Method not supported!")
            return None
        
        try:
            resp = json.loads(api_call_response.text)
        except:
            resp = api_call_response.text
        return resp

    def retrieve_s3_df(self, bucket, key, sep=','):
        '''
        Get series
        '''
        data = {'bucket':bucket, 'key':key, 'sep':sep}
        resp = self.api_call('retrieve_data_s3', method="post", data=data, verify=False)
        df = pd.DataFrame(resp)
        return df

    def load_s3_df(self, df, bucket, key, sep=',', overwrite=True):
        '''
        Load file to s3.
        '''
        payload = df.to_dict(orient='records')
        data = {'bucket':bucket, 'file_name':key, 'payload':payload, 'sep':sep, 'overwrite':overwrite}
        try:
            resp = self.api_call('load_data_s3', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}
        return resp

    def load_portfolio(self, port_df, port_name, ref_date=None):
        '''
        Load portfolio to WM database.
        '''
        weights = port_df.to_dict(orient='records')
        data = {'port_name':port_name, 'ref_date':ref_date, 'weights':weights}
        try:
            resp = self.api_call('load_portfolio', method="post", data=data, verify=False)
        except:
            resp = {'msg':'Check permissions!'}
        return resp['msg']

    def upload_with_presigned_url(self, local_file_path, bucket, key):
        """
        Upload a local file to S3 using a presigned URL.
        """
        data = {'bucket':bucket, 'key':key}
        try:
            presigned_url = self.api_call('link_data_s3', method="post", data=data, verify=False)
        except Exception as e:
            print(f"Error with presigned url: {e}")
            return False

        content_type, _ = mimetypes.guess_type(local_file_path)
        put_headers = {'Content-Type':content_type}

        with open(local_file_path, 'rb') as file:
            try:
                response = requests.put(presigned_url, data=file, headers=put_headers, verify=False)
                if response.status_code == 200:
                    print("File uploaded successfully")
                    return True
                else:
                    print(f"Error uploading file. Status code: {response.status_code}")
                    return False
            except Exception as e:
                print(f"Error uploading file: {e}")
                return False
