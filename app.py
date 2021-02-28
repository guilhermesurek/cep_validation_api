# -*- coding: utf-8 -*-
# endpoint.py
from flask import Flask
from flask import request
import json

from cep_validation import CEP, CEPError

app = Flask(__name__)

# Simple endpoint to check if api is running
@app.route('/')
def test():
    '''
        Simple function to check if the api is running.
    '''
    return 'API running!'

# Principal endpoint to post cep validation
@app.route('/cpp_cep_validation/',methods=['POST'])
def cpp_cep_validation():
    '''
        This function will parse the input as a json recieved in the POST method by the endpoint.
        Then will validate the cep data and return to the caller.
    '''
    # Force input as json
    post_params = request.get_json(force=True, cache=False)
    
    if post_params:
        # Check if the key 'cep' was send
        if ('cep' in post_params):

            try:
                # Validate the cep data
                answer = CEP(cep=post_params.get('cep'),
                             data_local=1).output()

                # Create api response
                response = app.response_class(
                        response=json.dumps(answer),
                        status=200,
                        mimetype='application/json')

                return response

            except CEPError as error:
                # Prepare error format response
                answer =  {
                    "error": {
                        "message": error,
                        "exception": "CEPError"
                    }
                }
                # CEP Error, create api response
                response = app.response_class(
                        response=json.dumps(answer),
                        status=200,
                        mimetype='application/json')

                return response
                
            except AssertionError as error:
                # Prepare error format response
                answer =  {
                    "error": {
                        "message": error,
                        "exception": "AssertionError"
                    }
                }
                # Assertion Error, create api response
                response = app.response_class(
                        response=json.dumps(answer),
                        status=200,
                        mimetype='application/json')

                return response

        else:
            # Json input does not have the key 'cep'
            # Prepare return message
            msg = "Json input does not have the key 'cep'."
            # Prepare error format response
            answer =  {
                "error": {
                    "message": msg,
                    "exception": ""
                }
            }
            # Create api response
            response = app.response_class(
                response=json.dumps(answer),
                status=200,
                mimetype='application/json')
            return response
    else:
        # Json input empty or invalid
        # Prepare return message
        answer =  {
            "error": {
                "message": "Input json empty or invalid.", 
                "exception": ""
            }
        }
        # Create api response
        response = app.response_class(
                response=json.dumps(answer),
                status=200,
                mimetype='application/json')
        return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
