'''
Created on 29 Nov 2023

@author: jacklok
'''
from flask import Blueprint, request
import logging
from trexmodel.utils.model.model_util import create_db_client
from datetime import datetime
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet
from trexapi.utils.api_helpers import StatusCode,\
    create_api_message
from trexapi.decorators.api_decorators import user_auth_token_required,\
    user_auth_token_required_pass_reference_code
from flask.json import jsonify
from trexmodel.models.datastore.rating_models import OutletRating,\
    OutletRatingResult, MerchantRatingResult

rating_api_bp = Blueprint('rating_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/rating')

logger = logging.getLogger('api')

@rating_api_bp.route('/outlet/<outlet_key>/review', methods=['POST'])
@user_auth_token_required_pass_reference_code
def give_outlet_rating(reference_code, outlet_key):
    logger.debug('---give_outlet_rating---')
    
    rating_in_json              = request.get_json()
    service_rating              = rating_in_json.get('service_rating')
    ambience_rating             = rating_in_json.get('ambience_rating')
    food_rating                 = rating_in_json.get('food_rating')
    value_rating                = rating_in_json.get('value_rating')
    
    
    db_client = create_db_client(caller_info="give_outlet_rating")
    
    logger.debug('give_outlet_rating: user account by reference code=%s', reference_code)
    logger.debug('give_outlet_rating: outlet_key=%s', outlet_key)
    
    with db_client.context():
        user_acct       = User.get_by_reference_code(reference_code)
        outlet          = Outlet.fetch(outlet_key)
        merchant_acct   = outlet.merchant_acct_entity
    
    if user_acct and outlet:
        with db_client.context():
            OutletRating.create(user_acct, outlet, 
                                    service_rating  = service_rating, 
                                    ambience_rating = ambience_rating, 
                                    food_rating     = food_rating, 
                                    value_rating    = value_rating,
                                    )
            MerchantRatingResult.update(merchant_acct)
        
        return create_api_message(status_code=StatusCode.OK)
    else:
        return create_api_message(status_code=StatusCode.BAD_REQUEST)

@rating_api_bp.route('/outlet/<outlet_key>/review', methods=['GET'])
def read_outlet_rating(outlet_key):   
    logger.debug('give_outlet_rating: outlet_key=%s', outlet_key)
    
    db_client = create_db_client(caller_info="read_outlet_rating")
    
    with db_client.context():
        outlet      = Outlet.fetch(outlet_key) 
        outlet_rating_result = OutletRatingResult.get_by_outlet(outlet)
    
    
    if outlet_rating_result:
        return jsonify(outlet_rating_result.rating_result)
    else:
        return create_api_message(status_code=StatusCode.BAD_REQUEST)
    
@rating_api_bp.route('/merchant/<merchant_acct_key>/review', methods=['GET'])
def read_merchant_rating(merchant_acct_key):   
    logger.debug('read_merchant_rating: merchant_acct_key=%s', merchant_acct_key)
    
    db_client = create_db_client(caller_info="read_merchant_rating")
    
    with db_client.context():
        merchant_acct           = MerchantAcct.fetch(merchant_acct_key) 
        merchant_rating_result  = MerchantRatingResult.get_by_merchant_acct(merchant_acct)
    
    
    if merchant_rating_result:
        return jsonify(merchant_rating_result.rating_result)
    else:
        return create_api_message(status_code=StatusCode.BAD_REQUEST)    
    
@rating_api_bp.route('/outlet/<outlet_key>/update', methods=['POST'])
def update_outlet_rating(outlet_key):   
    logger.debug('update_outlet_rating: outlet_key=%s', outlet_key)
    update_rating_in_json       = request.get_json()
    updated_datetime_from       = update_rating_in_json.get('updated_datetime_from')
    
    db_client = create_db_client(caller_info="update_outlet_rating")
    
    if is_not_empty(updated_datetime_from):
        updated_datetime_from = datetime.strptime(updated_datetime_from, '%d-%m-%Y %H:%M')
    
    with db_client.context():
        outlet      = Outlet.fetch(outlet_key) 
        OutletRatingResult.update(outlet, updated_datetime_from)
    
    
    return create_api_message(triggered_datetime=datetime.now(), status_code=StatusCode.OK)

@rating_api_bp.route('/merchant/<merchant_acct_key>/update', methods=['POST'])
def update_merchant_rating(merchant_acct_key):   
    logger.debug('update_merchant_rating: merchant_acct_key=%s', merchant_acct_key)
    update_rating_in_json       = request.get_json()
    updated_datetime_from       = update_rating_in_json.get('updated_datetime_from')
    
    db_client = create_db_client(caller_info="update_merchant_rating")
    
    if is_not_empty(updated_datetime_from):
        updated_datetime_from = datetime.strptime(updated_datetime_from, '%d-%m-%Y %H:%M')
    
    with db_client.context():
        merchant_acct      = MerchantAcct.fetch(merchant_acct_key) 
        MerchantRatingResult.update(merchant_acct, updated_datetime_from)
    
    
    return create_api_message(triggered_datetime=datetime.now(), status_code=StatusCode.OK)    
    
