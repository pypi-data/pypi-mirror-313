import os
import json
import math
import copy
import logging

from .thread_process import *
from analytics_sdk.utilities import (
    BASE_API_URL,
    NO_OF_API_THREADS,
    DISABLE_API_THREADS,
    API_PAGE_SIZE
)

logger = logging.getLogger(__name__)

class ApiTask:
    def __init__(self, api_client, form):
        self.results = []
        self.api_client = api_client,
        self.form = form


    def get_opsql_results_with_threads_by_tenant(self, api_client, method='POST'):
        if self.form is not None and self.form.query_builder is not None:
            # Multi thread / Parallel processing
            if DISABLE_API_THREADS == 'false':
                pool = ThreadPool(int(NO_OF_API_THREADS))
                for query in self.form.query_builder:
                    pool.add_task(self.fetch_opsql_results_with_all_pages, api_client, query, method)
                pool.wait_completion()
                self.results = [item for sublist in self.results for item in sublist]
            else: # Sequential processing
                for query in self.form.query_builder:
                    url = BASE_API_URL + f'/opsql/api/v7/tenants/{query.tenant_id}/queries'
                    data = query.get_query()
                    result = api_client.get_paginated_api_results(method, url, json.dumps(data), f'V7 {data["objectType"]} OpsQL, tenant id is : {query.tenant_id} , run id is : {self.form.get_run_id()}')
                    if not result:
                        continue
                    self.results.append(result)
                self.results = [item for sublist in self.results for item in sublist]
        return self.results
    

    def get_opsql_results_with_threads_by_tenant_page(self, api_client, method='POST'):
        if self.form is not None and self.form.query_builder is not None:
            # Multi thread / Parallel processing
            if DISABLE_API_THREADS == 'false':
                pool = ThreadPool(int(NO_OF_API_THREADS))
                for query in self.form.query_builder:
                    page_size = query.get_opsql_page_size()
                    total_results_count = self.get_opsql_total_results(api_client, query)
                    if total_results_count > 0:
                        total_pages = self.get_no_of_pages(total_results_count, page_size)
                        if total_pages > 0:
                            t_resp = []
                            page_no = 1
                            while(page_no <= total_pages):
                                q_builder = copy.copy(query)
                                q_builder.page_no = page_no
                                q_builder.page_size = page_size
                                pool.add_task(self.fetch_opsql_results, api_client, q_builder, method)
                                page_no += 1
                pool.wait_completion()
                self.results = [item for sublist in self.results for item in sublist]
            else: # Sequential processing
                for query in self.form.query_builder:
                    url = BASE_API_URL + f'/opsql/api/v7/tenants/{query.tenant_id}/queries'
                    data = query.get_query()
                    result = api_client.get_paginated_api_results(method, url, json.dumps(data), f'V7 {data["objectType"]} OpsQL, tenant id is : {query.tenant_id} , run id is : {self.form.get_run_id()}')
                    if not result:
                        continue
                    self.results.append(result)
                self.results = [item for sublist in self.results for item in sublist]
        return self.results
    
    
    def get_opsql_total_results(self, api_client, query):
        count = 0
        if query is not None:
            url = BASE_API_URL + f'/opsql/api/v7/tenants/{query.tenant_id}/queries/count'
            data = query.get_count_query()
            count_result = api_client.get_post_opsql_count_results(url, json.dumps(data), f'V7 {data["objectType"]} OpsQL, tenant id is : {query.tenant_id}')
            if count_result and count_result is not None and 'count' in count_result:
                count = count_result['count']
        return count
    

    def fetch_opsql_results_with_all_pages(self, api_client, query, method):
        url = BASE_API_URL + f'/opsql/api/v7/tenants/{query.tenant_id}/queries'
        data = query.get_query()
        result = api_client.get_paginated_api_results(method, url, json.dumps(data), f'V7 {query.object_type} OpsQL, tenant id is : {query.tenant_id}')
        if result:
            self.results.append(result)


    def fetch_opsql_results(self, api_client, query, method):
        url = BASE_API_URL + f'/opsql/api/v7/tenants/{query.tenant_id}/queries'
        data = query.get_query()
        if method == 'POST':
            res = api_client.get_post_request_results(url, json.dumps(data), f'V7 {query.object_type} OpsQL, tenant id is : {query.tenant_id}')
        else:
            res = api_client.get_response(url, f'V7 {query.object_type} OpsQL, tenant id is : {query.tenant_id}')
            
        result = None
        if res == None or not res.ok:
            logger.error('Get %s API is failed, url %s', f'V7 {query.object_type} OpsQL, tenant id is : {query.tenant_id}', url)
            return result
        elif "results" not in res.json() or len(res.json()['results'])==0 :
            logger.error('Get %s API results are empty, url is %s', f'V7 {query.object_type} OpsQL, tenant id is : {query.tenant_id}', url)
            return result
        else:
            if 'results' in res.json():
                result = res.json()['results']
        
        if result:
            self.results.append(result)


    def get_no_of_pages(self, count, page_size):
        total_pages = 0
        if count > 0:
            total_pages = math.ceil(count / page_size)
        return total_pages
    

    def get_results_with_all_pages(self, api_client, url, type):
        url = BASE_API_URL + url
        result = api_client.get_response(url, type)
        if result:
            self.results.append(result)
    

    def get_results_by_threads(self, api_client, url_list, type):
        self.results = []
        if url_list is not None and len(url_list) > 0:
            if DISABLE_API_THREADS == 'false':
                pool = ThreadPool(int(NO_OF_API_THREADS))
                for url in url_list:
                    pool.add_task(self.get_results_with_all_pages, api_client, url, type)
                pool.wait_completion()
            else:
                for url in url_list:
                    result = api_client.get_response(url, type)
                    if result:
                        self.results.append(result)
                    else:
                        continue
        return self.results


    def get_results_json_map_with_all_pages(self, api_client, url, key, type):
        url = BASE_API_URL + url
        type = type + f' key : {key}'
        # result = api_client.get_response(url, type)
        data = {}
        result = api_client.get_paginated_api_results('GET', url, json.dumps(data), f'{type} V2 tenant id is : {self.form.get_tenant_id()} , run id is : {self.form.get_run_id()}')
        if result:
            res = {}
            res[key] = result
            self.results.append(res)
    

    def get_results_json_map_by_threads(self, api_client, url_map, type):
        self.results = []
        if url_map is not None and len(url_map) > 0:
            if DISABLE_API_THREADS == 'false':
                pool = ThreadPool(int(NO_OF_API_THREADS))
                for key in url_map:
                    pool.add_task(self.get_results_json_map_with_all_pages, api_client, url_map[key], key, type)
                pool.wait_completion()
            else:
                for key in url_map:
                    result = api_client.get_response(url_map[key], type)
                    if result:
                        res = {}
                        res[key] = result
                        self.results.append(res)
                    else:
                        continue
        return self.results
    
    
    def get_results_map_with_all_pages(self, api_client, url, key, type):
        url = BASE_API_URL + url
        type = type + f' key : {key}'
        result = api_client.get_response(url, type)
        if result:
            res = {}
            res[key] = result
            self.results.append(res)
    

    def get_results_map_by_threads(self, api_client, url_map, type):
        self.results = []
        if url_map is not None and len(url_map) > 0:
            if DISABLE_API_THREADS == 'false':
                pool = ThreadPool(int(NO_OF_API_THREADS))
                for key in url_map:
                    pool.add_task(self.get_results_map_with_all_pages, api_client, url_map[key], key, type)
                pool.wait_completion()
            else:
                for key in url_map:
                    url = BASE_API_URL + url_map[key]
                    result = api_client.get_response(url, type)
                    if result:
                        res = {}
                        res[key] = result
                        self.results.append(res)
                    else:
                        continue
        return self.results