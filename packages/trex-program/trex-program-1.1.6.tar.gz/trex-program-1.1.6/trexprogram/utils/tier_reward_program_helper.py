'''
Created on 5 Oct 2021

@author: jacklok
'''
from trexmodel.models.datastore.transaction_models import CustomerTransaction
from trexmodel.models.datastore.reward_models import CustomerEntitledTierRewardSummary
from trexconf import program_conf 
import logging

#logger = logging.getLogger('helper')
logger = logging.getLogger('debug')

def update_and_get_unlock_tier_index_list(customer, tier_reward_program, transaction_details):
    logger.debug('---update_and_get_unlock_tier_index_list---, transaction_id=%s', transaction_details.transaction_id)
    
    customer_tier_reward_summary    = CustomerEntitledTierRewardSummary.get_customer_tier_reward_program_summary(customer, tier_reward_program)
    transact_datetime               = transaction_details.transact_datetime
    cycle_start_datetime            = None
    checking_transaction_list       = []
    unlock_reward_tier_index_list   = []
    is_new_cycle                    = False
    allow_recycle                   = False
    is_cycle_completed              = False
    
    logger.debug('customer_tier_reward_summary=%s', customer_tier_reward_summary)
    
    if customer_tier_reward_summary is None:
        logger.debug('no customer_tier_reward_summary yet')
        checking_transaction_list   = None
        is_new_cycle                = True
        cycle_start_datetime        = transact_datetime
        #cycle_start_datetime        = datetime.combine(tier_reward_program.start_date, time())
        
        customer_tier_reward_summary = CustomerEntitledTierRewardSummary.create(customer, 
                                                                                tier_reward_program, 
                                                                                cycle_start_datetime = cycle_start_datetime)
        logger.debug('Created csutomer entitled tier reward summary')
        
    else:
        logger.debug('found customer_tier_reward_summary')
        is_cycle_completed = customer_tier_reward_summary.is_cycle_completed 
        
        logger.debug('is_cycle_completed=%s', is_cycle_completed)
        
        if is_cycle_completed:
            logger.debug('cycle have completed, thus going to restart cycle')
            allow_recycle = tier_reward_program.is_tier_recycle
            if allow_recycle:
                #since cycle have been completed, thus restart the cycle and use latest transaction datetime as cycle start datetime
                is_cycle_completed      = False
                cycle_start_datetime    = transact_datetime
                
                CustomerEntitledTierRewardSummary.restart_cycle(customer_tier_reward_summary, cycle_start_datetime=cycle_start_datetime)
                logger.debug('Change is_cycle_completed to False after restart cycle')
                
        else:
            #follow existing cycle start datetime
            cycle_start_datetime        = customer_tier_reward_summary.cycle_start_datetime
            logger.debug('Follow existing cycle start datetime')
            
    customer_tier_summary_list  = customer_tier_reward_summary.tier_summary.get('tiers') or [] if customer_tier_reward_summary.tier_summary else []
    
    logger.debug('========================================================================')
    logger.debug('cycle_start_datetime=%s', cycle_start_datetime)
    logger.debug('transact_datetime=%s', transact_datetime)
    
    if is_cycle_completed == False:
        logger.debug('cycle is not yet completed')
        if is_new_cycle:
            logger.debug('it is new cycle')
            checking_transaction_list   = [transaction_details]
        else:
            logger.debug('it is existing cycle, cycle_start_datetime=%s, transact_datetime=%s', cycle_start_datetime, transact_datetime)
            checking_transaction_list = CustomerTransaction.list_customer_transaction_by_transact_datetime(customer, 
                                                                                                           transact_datetime_from   = cycle_start_datetime, 
                                                                                                           transact_datetime_to     = transact_datetime
                                                                                                           )
            
             
            if checking_transaction_list is None:
                checking_transaction_list = [transaction_details]
            else:
                checking_transaction_list.append(transaction_details)
        
        #process transaction history to accumulate by reward format
        accumulated_transaction_summary = {
                                            program_conf.SALES_AMOUNT : {
                                                                        'amount': .0,
                                                                        'sources':[],
                                                                        },
                                           }
        
        for _transaction_details in checking_transaction_list:
            if _transaction_details.is_revert == False:
                entitled_reward_summary = _transaction_details.entitled_reward_summary
                logger.debug('reading accumulated reward for transaction_id=%s', transaction_details.transaction_id)
                if entitled_reward_summary:
                    for reward_format, reward_summary in entitled_reward_summary.items():
                        if reward_format in program_conf.SUPPORT_TIER_REWARD_PROGRAM_CONDITION_REWARD_FORMAT:
                            accumualated_amount = .0
                            found_reward        = False
                            
                            if accumulated_transaction_summary.get(reward_format) is not None:
                                accumualated_amount    = accumulated_transaction_summary.get(reward_format).get('amount')
                                found_reward = True
                            
                            
                            transaction_reward_amount       = reward_summary.get('amount')
                            
                            if transaction_reward_amount>0:
                                accumualated_amount    += transaction_reward_amount
                                
                                transaction_source_details = {
                                                            'transaction_id': _transaction_details.transaction_id,
                                                            'amount':transaction_reward_amount,    
                                                            }
                                
                                if found_reward:
                                    reward_sources_list = accumulated_transaction_summary.get(reward_format).get('sources')
                                    reward_sources_list.append(transaction_source_details)
                                    accumulated_transaction_summary[reward_format] = {
                                                                                    'amount' : accumualated_amount,   
                                                                                    'sources': reward_sources_list,
                                                                                    }
                                else:
                                    accumulated_transaction_summary[reward_format] = {
                                                                                'amount' : accumualated_amount,
                                                                                'sources': [
                                                                                            transaction_source_details
                                                                                            ]
                                                                                        
                                                                                           
                                
                                                                            }
                
                
                if _transaction_details.transact_amount>0:
                    transaction_sales_details   = {
                                                            'transaction_id': _transaction_details.transaction_id,
                                                            'amount'        : _transaction_details.transact_amount,    
                                                            }
                    
                    sales_sources_list = accumulated_transaction_summary.get(program_conf.SALES_AMOUNT).get('sources')
                    sales_sources_list.append(transaction_sales_details)
                    sales_accumualated_amount   = accumulated_transaction_summary.get(program_conf.SALES_AMOUNT).get('amount')
                    sales_accumualated_amount   += _transaction_details.transact_amount
                    
                    accumulated_transaction_summary[program_conf.SALES_AMOUNT] = {
                                                                    'amount' : sales_accumualated_amount,   
                                                                    'sources': sales_sources_list,
                                                                    }
            
            
        logger.debug('accumulated_transaction_summary=%s', accumulated_transaction_summary)
        total_tier_count = len(customer_tier_summary_list)
        
        #continue_check_tier_reward      = True
        max_unlock_tier_count_per_trax  = tier_reward_program.max_unlock_tier_count_per_trax
        unlock_tier_count               = 0
        
        logger.debug('max_unlock_tier_count_per_trax=%s', max_unlock_tier_count_per_trax)
        
        #while continue_check_tier_reward:
        for tier_no, tier_summary in enumerate(customer_tier_summary_list, start=1):
            
            logger.debug('tier_no=%d, tier_summary=%s', tier_no, tier_summary)
            
            if tier_summary.get('unlock_status'):
                continue
            else:
                #checking for not unlock tier
                target_checking_format              = None
                accumualated_checking_amount        = .0
                unlock_condition_value              = float(tier_summary.get('unlock_condition_value'))
                unlock_value                        = float(tier_summary.get('unlock_value') or .0) 
                
                if tier_summary.get('unlock_condition') in program_conf.ENTITLE_REWARD_CONDITION_ACCUMULATE_TYPES: 
                    if program_conf.ENTITLE_REWARD_CONDITION_ACCUMULATE_POINT == tier_summary.get('unlock_condition'):
                        
                        if accumulated_transaction_summary.get(program_conf.REWARD_FORMAT_POINT) is not None:
                            reward_amount = accumulated_transaction_summary.get(program_conf.REWARD_FORMAT_POINT).get('amount')
                            accumualated_checking_amount    = reward_amount or .0
                        else:
                            accumualated_checking_amount = .0
                        
                        target_checking_format          = program_conf.REWARD_FORMAT_POINT
                        
                    elif program_conf.ENTITLE_REWARD_CONDITION_ACCUMULATE_STAMP == tier_summary.get('unlock_condition'):
                        
                        if accumulated_transaction_summary.get(program_conf.REWARD_FORMAT_STAMP) is not None:
                            reward_amount = accumulated_transaction_summary.get(program_conf.REWARD_FORMAT_STAMP).get('amount')
                            accumualated_checking_amount    = reward_amount or .0
                        else:
                            accumualated_checking_amount = .0
                        
                        target_checking_format          = program_conf.REWARD_FORMAT_STAMP
                        
                        
                    elif program_conf.ENTITLE_REWARD_CONDITION_ACCUMULATE_SALES_AMOUNT == tier_summary.get('unlock_condition'): 
                        
                        accumualated_checking_amount    = accumulated_transaction_summary.get(program_conf.SALES_AMOUNT).get('amount') or .0 
                        target_checking_format          = program_conf.SALES_AMOUNT
                    
                    logger.debug('tier_no=%s, unlock_tier_count=%s, accumualated_checking_amount=%s target_checking_format=%s', tier_no, unlock_tier_count, accumualated_checking_amount, target_checking_format)
                    logger.debug('accumualated_checking_amount=%d', accumualated_checking_amount)       
                    logger.debug('unlock_value=%d', unlock_value)
                    
                    is_condition_match = accumualated_checking_amount >= unlock_condition_value
                    
                    logger.debug('is_condition_match=%s', is_condition_match)
                        
                    if is_condition_match==True:
                        logger.debug('OKAY, found unlock matched condition tier no=%d', tier_no)
                        unlock_tier_count+=1
                        tier_summary['unlock_status']           = True
                        tier_summary['unlock_value']            = unlock_condition_value
                        tier_summary['unlock_datetime']         = transact_datetime.strftime('%d-%m-%Y %H:%M:%S')
                        tier_summary['unlock_source_details']   = accumulated_transaction_summary.get(target_checking_format).get('sources')
                         
                        unlock_reward_tier_index_list.append(tier_summary.get('tier_index'))
                        
                        if tier_no==total_tier_count:
                            #this is final tier
                            logger.debug('Unlock last tier')
                            
                    else:
                        logger.debug('tier condition not match, tier no=%d', tier_no)
                        tier_summary['unlock_value']    = accumualated_checking_amount  
                        if accumualated_checking_amount>0:
                            tier_summary['unlock_source_details'] = accumulated_transaction_summary.get(target_checking_format).get('sources')
                        
                          
                        break
                    
                    
                    
                logger.debug('unlock_tier_count=%s', unlock_tier_count)
                        
        logger.debug('-----> customer_tier_summary_list=%s', customer_tier_summary_list)
        
        
        CustomerEntitledTierRewardSummary.update(customer_tier_reward_summary, 
                                                 { 'tiers': customer_tier_summary_list })
        logger.debug('Updated customer entitled tier reward summary')
    
    logger.debug('unlock_reward_tier_index_list=%s', unlock_reward_tier_index_list)
    
    return unlock_reward_tier_index_list   
