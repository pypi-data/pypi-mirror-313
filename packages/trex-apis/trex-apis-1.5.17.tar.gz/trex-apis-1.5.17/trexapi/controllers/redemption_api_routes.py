'''
Created on 14 Dec 2023

@author: jacklok
'''
from flask import Blueprint, request
import logging
from trexlib.utils.log_util import get_tracelog
from trexmodel.utils.model.model_util import create_db_client
from trexapi.utils.api_helpers import StatusCode, create_api_message
from trexmodel.models.datastore.customer_models import Customer
from trexapi.decorators.api_decorators import customer_key_required
from flask_babel import gettext
from datetime import datetime
from trexmodel.models.datastore.redemption_catalogue_models import RedemptionCatalogue
    
from trexapi.utils.redemption_catalogue_helper import giveaway_redeem_catalogue_item

redemption_api_bp = Blueprint('redemption_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/redemption')

logger = logging.getLogger('api')


@redemption_api_bp.route('/list-redemption-catalogue', methods=['GET'])
@customer_key_required
def list_redemption_catalogue(customer_key):
    logger.info('customer_key=%s', customer_key)
    db_client = create_db_client(caller_info="list_redemption_catalogue")
    filtered_catalogues_list = []
    
    with db_client.context():
        customer   = Customer.fetch(customer_key)
        
        merchant_acct = customer.registered_merchant_acct
        
        published_redemption_catalogue_configuration = merchant_acct.published_redemption_catalogue_configuration
        if published_redemption_catalogue_configuration:
            catalogues_list = published_redemption_catalogue_configuration.get('catalogues')
            
            if len(catalogues_list)>0:
                for catalogue in catalogues_list:
                    if __check_is_still_active(catalogue):
                        if __check_is_eligible(customer, catalogue.get('exclusivity')):
                            catalogue['items'] = __resolve_catalogue_items_details(catalogue.get('items'), merchant_acct.published_voucher_configuration.get('vouchers'))
                            filtered_catalogues_list.append(catalogue)
    
    logger.debug('filtered_catalogues_list=%s', filtered_catalogues_list)
                
    return create_api_message(status_code=StatusCode.OK, catalogues_list=filtered_catalogues_list) 

@redemption_api_bp.route('/list-redemption-catalogue/reward-type/<reward_type>', methods=['GET'])
@customer_key_required
def list_redemption_catalogue_by_reward_type(customer_key, reward_type):
    logger.info('customer_key=%s', customer_key)
    logger.info('reward_type=%s', reward_type)
    db_client = create_db_client(caller_info="list_redemption_catalogue_by_reward_type")
    filtered_catalogues_list = []
    
    with db_client.context():
        customer   = Customer.fetch(customer_key)
        
        merchant_acct = customer.registered_merchant_acct
        
        published_redemption_catalogue_configuration = merchant_acct.published_redemption_catalogue_configuration
        if published_redemption_catalogue_configuration:
            catalogues_list = published_redemption_catalogue_configuration.get('catalogues')
            
            if len(catalogues_list)>0:
                for catalogue in catalogues_list:
                    if catalogue.get('redeem_reward_format')==reward_type:
                        if __check_is_still_active(catalogue):
                            if __check_is_eligible(customer, catalogue.get('exclusivity')):
                                catalogue['items'] = __resolve_catalogue_items_details(catalogue.get('items'), merchant_acct.published_voucher_configuration.get('vouchers'))
                                filtered_catalogues_list.append(catalogue)
    
    logger.debug('filtered_catalogues_list=%s', filtered_catalogues_list)
                
    return create_api_message(status_code=StatusCode.OK, catalogues_list=filtered_catalogues_list)    

def __resolve_catalogue_items_details(catalogue_items_list, vouchers_list):
    resolved_items_list = []
    voucher_dict = __convert_vouchers_list_to_dict(vouchers_list)
    for item in catalogue_items_list:
        voucher = voucher_dict.get(item.get('voucher_key'))
        if voucher:
            resolved_items_list.append(
                    {
                        'voucher_key'           : item.get('voucher_key'),
                        'amount'                : item.get('voucher_amount'),
                        'label'                 : voucher.get('label'),
                        'image_url'             : voucher.get('image_url'),
                        'terms_and_conditions'  : voucher.get('terms_and_conditions'),
                        'redeem_reward_amount'  : item.get('redeem_reward_amount'),
                    }
                
                )
        else:
            resolved_items_list.append(item)
        
    return resolved_items_list
        

def __convert_vouchers_list_to_dict(vouchers_list):
    voucher_dict = {}
    for voucher in vouchers_list:
        voucher_dict[voucher.get('voucher_key')] = voucher
    
    return voucher_dict

def __check_is_still_active(catalogue):
    today = datetime.utcnow().date()
    start_date  = datetime.strptime(catalogue.get('start_date'), '%d-%m-%Y').date()
    end_date    = datetime.strptime(catalogue.get('end_date'), '%d-%m-%Y').date()
    
    if today>=start_date and today<=end_date:
        logger.info('catalogue is still valid')
        return True
    else:
        logger.info('catalogue is expired')
        return False

def __check_is_eligible(customer, catalogue_exclusivity):
    
    catalogue_tags_list                 = catalogue_exclusivity.get('tags',[])
    catalogue_memberships_list          = catalogue_exclusivity.get('memberships',[])
    catalogue_tier_memberships_list     = catalogue_exclusivity.get('tier_memberships',[])
    
    is_eligiable = False
    
    if len(catalogue_tags_list)==0 and len(catalogue_memberships_list)==0 and len(catalogue_tier_memberships_list)==0:
        logger.info('catalogue no exclusivity')
        is_eligiable = True
    else:
        if len(catalogue_tags_list)>0:
            logger.info('Going to check member tagging')
            tags_list = customer.tags_list
            for tag in catalogue_tags_list:
                if tag in tags_list:
                    is_eligiable = True
                    logger.info('Found member tagging match with catalogue exclusivity')
                    break
        
        
        if is_eligiable==False and len(catalogue_memberships_list)>0:
            logger.info('Going to check member basic membership')
            memberships_list_list = customer.memberships_list
            for membership in catalogue_memberships_list:
                if membership in memberships_list_list:
                    is_eligiable = True
                    logger.info('Found basic membership match with catalogue exclusivity')
                    break
        
        if is_eligiable==False and len(catalogue_tier_memberships_list)>0:
            logger.info('Going to check member tier membership')
            tier_membership_key = customer.tier_membership_key
            logger.info('customer tier_membership_key=%s', tier_membership_key)
            logger.info('catalogue tier_membership=%s', catalogue_tier_memberships_list)
            if tier_membership_key in catalogue_tier_memberships_list:
                is_eligiable = True
                logger.info('Found tier membership match with catalogue exclusivity')
    
    
    return is_eligiable

@redemption_api_bp.route('/redeem-redemption-catalogue-item', methods=['POST'])
@customer_key_required
def redeem_redemption_catalogue_item(customer_key):
    
    redeem_data_in_json         = request.get_json()
    redemption_catalogue_key    = redeem_data_in_json.get('redemption_catalogue_key')
    voucher_key                 = redeem_data_in_json.get('voucher_key')
    
    customer            = None
    redeem_item_details = None
    
    
    logger.info('customer_key=%s', customer_key)
    logger.info('voucher_key=%s', voucher_key)
    
    
    try:
        db_client = create_db_client(caller_info="redeem_redemption_catalogue_item")
        with db_client.context():
            redemption_catalogue    = RedemptionCatalogue.fetch(redemption_catalogue_key)
            if redemption_catalogue:
                redeem_item_details     = next(filter(lambda x: x['voucher_key'] == voucher_key, redemption_catalogue.catalogue_settings.get('items')), None)
                
                if redeem_item_details:
                    customer = Customer.fetch(customer_key)
                    if customer:
                        reward_summary_before     = customer.reward_summary
                        logger.debug('reward_summary_before=%s', reward_summary_before)
                        giveaway_redeem_catalogue_item(customer, redemption_catalogue, voucher_key)
                        reward_summary_after      = customer.reward_summary
                        logger.debug('reward_summary_after=%s', reward_summary_after)
                        
                    
    except:
        logger.error('Failed to redeem due to %s', get_tracelog())
        return create_api_message(gettext('Failed to redeem'), status_code=StatusCode.BAD_REQUEST)            
            
    if redeem_item_details is None:
        return create_api_message(gettext('Invalid redeem item'), status_code=StatusCode.BAD_REQUEST)    
    elif customer is None:    
        return create_api_message(gettext('Invalid customer profile'), status_code=StatusCode.BAD_REQUEST)
    
    with db_client.context():
        customer_details_dict = customer.to_dict(date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S")
            
    #customer_details_json =  jsonify(customer_details_dict)
    
    return create_api_message(customer_latest_reward=customer_details_dict, status_code=StatusCode.OK)
         