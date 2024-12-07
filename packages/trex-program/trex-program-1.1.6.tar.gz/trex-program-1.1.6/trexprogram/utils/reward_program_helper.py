'''
Created on 2 May 2024

@author: jacklok
'''
import logging
from trexconf import program_conf
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from trexconf.program_conf import REWARD_PROGRAM_DATE_FORMAT

logger = logging.getLogger('reward-program-lib')

def calculate_expiry_date(expiration_type, expiration_value, start_date=None):
        expiry_date = None
        
        logger.debug('calculate_expiry_date: expiration_type=%s', expiration_type)
        logger.debug('calculate_expiry_date: expiration_value=%s', expiration_value)
        
        if start_date is None:
            start_date = datetime.utcnow().date()
        
        if expiration_type == program_conf.REWARD_EXPIRATION_TYPE_AFTER_YEAR:
            expiry_date = start_date + relativedelta(years=expiration_value)
        
        elif expiration_type == program_conf.REWARD_EXPIRATION_TYPE_AFTER_MONTH:
            expiry_date =  start_date + relativedelta(months=expiration_value)
        
        elif expiration_type == program_conf.REWARD_EXPIRATION_TYPE_AFTER_WEEK:
            expiry_date =  start_date + relativedelta(weeks=expiration_value)
        
        elif expiration_type == program_conf.REWARD_EXPIRATION_TYPE_AFTER_DAY:
            expiry_date =  start_date + relativedelta(days=expiration_value)
        
        elif expiration_type == program_conf.REWARD_EXPIRATION_TYPE_SPECIFIC_DATE:
            expiry_date =  datetime.strptime(expiration_value, REWARD_PROGRAM_DATE_FORMAT)
        
        if isinstance(expiry_date, date):
            return expiry_date
        else:
            return expiry_date.date()
        
def calculate_effective_date(effective_type, effective_value, start_date=None):
        if start_date is None:
            start_date = datetime.utcnow().date()
        
        if effective_type == program_conf.REWARD_EFFECTIVE_TYPE_AFTER_MONTH:
            return start_date + relativedelta(months=effective_value)
        
        elif effective_type == program_conf.REWARD_EFFECTIVE_TYPE_AFTER_WEEK:
            return start_date + relativedelta(weeks=effective_value)
        
        elif effective_type == program_conf.REWARD_EFFECTIVE_TYPE_AFTER_DAY:
            return start_date + relativedelta(days=effective_value)
        
        elif effective_type == program_conf.REWARD_EFFECTIVE_TYPE_IMMEDIATE:
            return start_date           
