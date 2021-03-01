# API to validate CEP data

Recieve CEP data, clean it, validate it and return the validation.
The validation uses only the first 5 digits of the cep data.

## File Structure

├──files (csv files for local running)
   ├──CEPs.csv (csv file containing all first 5 digits CEPs)
├──tests (test package to test all the features)
   ├──test_api.py (test file based on pytest)
├──app.py (Main app file)
├──cep_validation.py (Validation routine)
├──db_manager.py (Database connection handler)
├──README.md (This file)
├──requirements.txt (All requirements needed to run application on production, not included testing/debuging libraries)
├──testing_notebook.ipynb (Notebook to fast testing/validating)
└──wsgi.py ()