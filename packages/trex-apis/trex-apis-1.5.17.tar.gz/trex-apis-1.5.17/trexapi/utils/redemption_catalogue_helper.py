'''
Created on 17 Dec 2023

@author: jacklok
'''

from datetime import datetime, date
from trexmodel import program_conf
from dateutil.relativedelta import relativedelta
import logging
from trexprogram.reward_program.reward_program_base import EntitledVoucherSummary
from trexmodel.models.datastore.voucher_models import MerchantVoucher
from trexmodel.models.datastore.reward_models import CustomerEntitledVoucher
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.model_decorators import model_transactional
from trexmodel.utils.model.model_util import generate_transaction_id
from trexmodel.models.datastore.redeem_models import RedemptionCatalogueTransaction,\
    CustomerRedemption
from trexanalytics.bigquery_upstream_data_config import create_merchant_customer_redemption_upstream_for_merchant
from trexmodel.models.datastore.customer_model_helpers import update_customer_entiteld_voucher_summary_with_customer_new_voucher
from trexmodel.models.datastore.message_model_helper import create_redeem_catalogue_item_message
from trexprogram.utils.reward_program_helper import calculate_effective_date,\
    calculate_expiry_date
from trexconf.program_conf import REWARD_PROGRAM_DATE_FORMAT

logger = logging.getLogger('helper')

@model_transactional(desc='giveaway_redeem_catalogue_item')
def giveaway_redeem_catalogue_item(customer, redemption_catalogue, voucher_key):
    redeemed_datetime       = datetime.utcnow()
    redeem_reward_format    = redemption_catalogue.redeem_reward_format
    redeem_item_details     = next(filter(lambda x: x['voucher_key'] == voucher_key, redemption_catalogue.catalogue_settings.get('items')), None)
    redeem_reward_amount    = redeem_item_details.get('redeem_reward_amount')
    
    if redeem_reward_format in (program_conf.REWARD_FORMAT_POINT,program_conf.REWARD_FORMAT_STAMP) :
        reward_summary      = customer.reward_summary
        
        logger.debug('********************************')
        logger.debug('customer reward_summary=%s', reward_summary)
        logger.debug('********************************')
        
        if reward_summary.get(redeem_reward_format).get('amount') < redeem_reward_amount:
            raise Exception('Not sufficient reward amount to redeem')
    
        else:
            transaction_id = generate_transaction_id(prefix='r')
            redemption_catalogue_transction_summary = {
                                                        'redemption_catalogue_key'  : redemption_catalogue.key_in_str,
                                                        'voucher_key'               : voucher_key,
                                                        
                                                        }
            CustomerRedemption.create(customer, 
                                    reward_format                           = redeem_reward_format,
                                    redeemed_amount                         = redeem_reward_amount,
                                    redeemed_datetime                       = redeemed_datetime, 
                                    transaction_id                          = transaction_id,
                                    redemption_catalogue_transction_summary = redemption_catalogue_transction_summary,
                                    )
            
            redemption_catalogue_transaction = RedemptionCatalogueTransaction.create(redemption_catalogue,
                                                  voucher_key, 
                                                  customer,
                                                  transaction_id,
                                                  redeemed_datetime,
                                                  )
            
            reward_summary = __giveaway_voucher_from_redemption_catalogue_item(customer, redeem_item_details, transaction_id, redeemed_datetime)
            
            create_redeem_catalogue_item_message(customer, reward_summary.entitled_voucher_summary, redemption_catalogue_transaction)
            
            #if customer_redemption:
            #    logger.info('Going to create customer redemption upstream')
                #create_merchant_customer_redemption_upstream_for_merchant(customer_redemption, streamed_datetime=redeemed_datetime)
            
            return reward_summary    


def __giveaway_voucher_from_redemption_catalogue_item(customer, redeem_item_details, transaction_id, transact_datetime):
    logger.debug('---__giveaway_voucher_from_redemption_catalogue_item---')
    
    voucher_key             = redeem_item_details.get('voucher_key')
    effective_type          = redeem_item_details.get('effective_type')
    effective_value         = redeem_item_details.get('effective_value')
    effective_date_str      = redeem_item_details.get('effective_date')
    
    if effective_type == program_conf.REWARD_EFFECTIVE_TYPE_SPECIFIC_DATE:
        if is_not_empty(effective_date_str):
            effective_date = datetime.strptime(effective_date_str, REWARD_PROGRAM_DATE_FORMAT)
    else:
        effective_date = calculate_effective_date(effective_type, effective_value, start_date = transact_datetime)
    
    expiration_type         = redeem_item_details.get('expiration_type')
    expiration_value        = redeem_item_details.get('expiration_value')
     
    expiry_date             = calculate_expiry_date(expiration_type, expiration_value, start_date=effective_date)
    
    voucher_amount          = redeem_item_details.get('voucher_amount')
    
    merchant_voucher = MerchantVoucher.fetch(voucher_key)
    customer_entitled_voucher_list = []
    reward_summary = EntitledVoucherSummary()
    
    logger.debug('merchant_voucher=%s', merchant_voucher)
    logger.debug('voucher_amount=%s', voucher_amount)
    
    if merchant_voucher:
        entitled_voucher_summary = customer.entitled_voucher_summary
        for v in range(voucher_amount):
            customer_entitled_voucher = CustomerEntitledVoucher.create(
                                                            merchant_voucher,
                                                            customer, 
                                                            transaction_id      = transaction_id,
                                                            rewarded_datetime   = transact_datetime,
                                                            effective_date      = effective_date,
                                                            expiry_date         = expiry_date,
                                                            
                                                            )
            
            logger.debug('customer_entitled_voucher=%s', customer_entitled_voucher)
            
            update_customer_entiteld_voucher_summary_with_customer_new_voucher(entitled_voucher_summary, customer_entitled_voucher)
            customer_entitled_voucher_list.append(customer_entitled_voucher)
        
        customer.entitled_voucher_summary = entitled_voucher_summary    
        customer.put()
        
        reward_summary.add(merchant_voucher, 
                                   customer_entitled_voucher_list) 
        
    return reward_summary
