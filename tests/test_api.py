from app import app
import json

def test_main_route_status_code():
    '''
        Test main route status code.
        Should be 200 - OK.
    '''
    with app.test_client() as c:
        rv = c.get('/')
        assert rv.status_code == 200

def test_main_route_data():
    '''
        Test main route data for GET mothod.
        Should be b'API running!'.
    '''
    with app.test_client() as c:
        rv = c.get('/')
        assert rv.data == b'API running!'

def test_cep_route_get_status_code():
    '''
        Test cep route status code for GET method.
        Should be 405 - Method not allowed.
    '''
    with app.test_client() as c:
        rv = c.get('/cpp_cep_validation/')
        assert rv.status_code == 405

def test_cep_route_post_status_code_wout_data():
    '''
        Test cep route status code for POST method without data.
        Should be 400 - Bad Request.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/')
        assert rv.status_code == 400

def test_cep_route_post_status_code_w_data():
    '''
        Test cep route status code for POST method with data.
        Should be 200 - OK.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/', data=json.dumps({}))
        assert rv.status_code == 200

def test_cep_route_post_empty_json():
    '''
        Test cep route response for POST method with an empty json.
        Should be {'error': {'message': 'Input json empty or invalid.', 'exception': ''}}.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/', data=json.dumps({}))
        assert rv.get_json().get('error').get('message') == 'Input json empty or invalid.'

def test_cep_route_post_json_without_cep_key():
    '''
        Test cep route response for POST method with a json input without 'cep' key.
        Should be {'error': {'message': 'Json input does not have the key 'cep'.', 'exception': ''}}.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"another_key": 123}))
        assert rv.get_json().get('error').get('message') == "Json input does not have the key 'cep'."

def test_cep_route_post_json_with_cep_key_empty():
    '''
        Test cep route response for POST method with a json input with cep key empty.
        Should be {'error': {'message': "Data in 'cep' key is empty.", 'exception': ''}}.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": ""}))
        assert rv.get_json().get('error').get('message') == "Data in 'cep' key is empty."

def test_cep_route_post_json_with_cep_key_less_5_digits():
    '''
        Test cep route response for POST method with a json input with cep key data less than 5 digits.
        Should be {'error': {'message': "CEP data has less than 5 digits, more than 8 digits or is not numeric.", 'exception': ''}}.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": "3543"}))
        assert rv.get_json().get('error').get('message') == "CEP data has less than 5 digits, more than 8 digits or is not numeric."

def test_cep_route_post_json_with_cep_key_more_8_digits():
    '''
        Test cep route response for POST method with a json input with cep key data more than 8 digits.
        Should be {'error': {'message': "CEP data has less than 5 digits, more than 8 digits or is not numeric.", 'exception': ''}}.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": "3543356477234"}))
        assert rv.get_json().get('error').get('message') == "CEP data has less than 5 digits, more than 8 digits or is not numeric."

def test_cep_route_post_json_with_cep_key_not_numeric():
    '''
        Test cep route response for POST method with a json input with cep key data not numeric.
        Should be {'error': {'message': "CEP data has less than 5 digits, more than 8 digits or is not numeric.", 'exception': ''}}.
    '''
    with app.test_client() as c:
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": "SDGE3543"}))
        assert rv.get_json().get('error').get('message') == "CEP data has less than 5 digits, more than 8 digits or is not numeric."
    
def test_cep_route_post_negative_01():
    '''
        Test cep route response for POST method with a CEP data negative.
        Should be {'cep_validation': False, 'cep_data': '{first 5 digits}'}.
    '''
    with app.test_client() as c:
        cep = "00000000"
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": cep}))
        assert rv.get_json().get('cep_validation') == False
        assert rv.get_json().get('cep_data') == cep[:5]

def test_cep_route_post_negative_02():
    '''
        Test cep route response for POST method with a CEP data negative.
        Should be {'cep_validation': False, 'cep_data': '{first 5 digits}'}.
    '''
    with app.test_client() as c:
        cep = "69345000"
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": cep})) # Roraima
        assert rv.get_json().get('cep_validation') == False
        assert rv.get_json().get('cep_data') == cep[:5]

def test_cep_route_post_positive_01():
    '''
        Test cep route response for POST method with a CEP data positive.
        Should be {'cep_validation': True, 'cep_data': '{first 5 digits}'}.
    '''
    with app.test_client() as c:
        cep = "09290000"
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": cep})) # Santo André
        assert rv.get_json().get('cep_validation') == True
        assert rv.get_json().get('cep_data') == cep[:5]

def test_cep_route_post_positive_02():
    '''
        Test cep route response for POST method with a CEP data positive.
        Should be {'cep_validation': True, 'cep_data': '{first 5 digits}'}.
    '''
    with app.test_client() as c:
        cep = "81630000"
        rv = c.post('/cpp_cep_validation/', data=json.dumps({"cep": cep})) # Curitiba
        assert rv.get_json().get('cep_validation') == True
        assert rv.get_json().get('cep_data') == cep[:5]