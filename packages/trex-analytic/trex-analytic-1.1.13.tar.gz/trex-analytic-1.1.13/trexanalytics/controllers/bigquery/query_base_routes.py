'''
Created on 19 Jan 2021

@author: jacklok
'''

from flask import request
from flask_restful import Resource
from trexconf import conf
import logging
from trexlib.utils.log_util import get_tracelog

from trexlib.utils.google.bigquery_util import execute_query, process_job_result_into_category_and_count, create_bigquery_client

logger = logging.getLogger('analytics')

class BaseResource(Resource):
    
    def post(self):
        return self.get()
    
    def get(self):
        logger.info('base resource')
        
        return 'Base'
        

class QueryBaseResource(Resource):
    
    def post(self):
        return self.get()
    
    def get(self):
        logger.info('query base resource from QueryBaseResource') 
        content         = {}
        try:
            content         = request.args or request.args.to_dict() or request.json or {}
        except:
            logger.warn('failed to get content where %s', get_tracelog())
        
        logger.info('content=%s', content)
        
        #if is_not_empty(content):
        query           = self.prepare_query(**content)
        
        logger.info('query=%s', query)
        
        bg_client       = create_bigquery_client(
                            credential_filepath=conf.BIGQUERY_SERVICE_CREDENTIAL_PATH,
                            project_id=conf.BIGQUERY_GCLOUD_PROJECT_ID,
                            )
        
        if bg_client is not None:
            logger.info('BigQuery Client is not none, thus going to execute query')
        
            try:
                job_result_rows = execute_query(bg_client, query)
                
                bg_client.close()
            except:
                job_result_rows = []
                logger.error('Failed to execute query due to %s', get_tracelog())
        else:
            job_result_rows = []
            
        query_result    = self.process_query_result(job_result_rows)
        
        logger.info('query_result=%s', query_result)
        
        return query_result
        #else:
        #    return {}
        
    def prepare_query(self, **kwrgs):
        pass
    
    def process_query_result(self, job_result_rows):
        pass
    
class CategoryAndCountQueryBaseResource(QueryBaseResource):
    
    def process_query_result(self, job_result_rows):
        return process_job_result_into_category_and_count(job_result_rows)
    
class FieldnameAndValueQueryBaseResource(QueryBaseResource):
    
    def process_query_result(self, job_result_rows):
        return process_job_result_into_category_and_count(job_result_rows)    
    
    
        