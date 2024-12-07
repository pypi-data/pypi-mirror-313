from flask import Blueprint, request, url_for, jsonify
import logging, json
from trexapi.decorators.api_decorators import auth_token_required
from trexlib.utils.string_util import is_not_empty, is_empty
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.pos_models import POSSetting
from trexmodel.utils.model.model_util import create_db_client
from trexmodel.models import merchant_helpers
from trexlib.utils.common.common_util import sort_list
from firebase_admin import firestore
from datetime import datetime


#logger = logging.getLogger('api')
logger = logging.getLogger('debug')

transaction_api_bp = Blueprint('transaction_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/transaction')

@transaction_api_bp.route('/ping', methods=['GET'])
def ping():
    return 'pong',200