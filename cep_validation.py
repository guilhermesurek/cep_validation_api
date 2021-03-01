# cep_validation.py
import pandas as pd
import db_manager as db

class CEPError(Exception):
    pass

class CEP():
    def __init__(self, cep, data_local=0) -> None:
        '''
            Instance of cep class. It will load internal or external data, preprocess cep data, cleaning it,
                then validate. To read the results call the output function.
            Input
                - cep: expected 8 lenght numeric value
                - data_local: 1 - for local data loading and; 0 - for database connection. Debuging and testing purposes.
            Output()
                - output_message: dict containing the keys 'cep_validation' and 'cep_data'.
        '''
        # Save input
        self.cep = cep
        self.data_local = data_local
        # Initialize error
        self.error = None
        # Load databases
        self._load_databases()
        # Preprocess CEP data
        self._preprocess()
        # Validate CEP data
        self._validate()

    def _load_databases(self):
        '''
            Function to load the data from external or internal sources.
            Generally, internal sources must be used only for testing purpouse. Additionally,
            the loaded files should be outdated by this time.
        '''
        ## ---- paths to local files ------
        l_path_cep = 'files/CEPs.csv' 
        ## ---- external table names ------
        cep_table_name = 'CPP_API_CEP'
        ## ---- load data table -----------
        try:
            if self.data_local == 0:
                # From external sources
                self.cep_table = db.get_df_table(cep_table_name)
            else:
                # From local sources
                self.cep_table = pd.read_csv(l_path_cep, converters={"CEP_Root5": str}) # CEP must be load as str, loading as number should exclude left zeros.
        except:
            raise CEPError("Fail to load data sources.")

    def _preprocess(self):
        '''
            Function to pre process the cep data. Cleaning.
        '''
        # check if cep is not None
        if self.cep:
            # Remove special chars
            self.cep = self.cep.replace('.', '').replace('-', '').replace('/', '').replace('*', '').replace('_', '').replace('|', '')
            # Remove spaces
            self.cep = self.cep.replace(' ', '')
            # Check if it is 8 lenght numeric
            if len(self.cep) <= 8 and len(self.cep) >= 5 and self.cep.isnumeric():
                # Valid
                # Get the 5 first numbers. I.e. from '81070100' get '81070'
                self.cep_root5 = self.cep[:5]
            else:
                # Invalid
                # Set cep_root5 to None
                self.cep_root5 = None
                # Set error message
                self.error = {"error": {"message": "CEP data has less than 5 digits, more than 8 digits or is not numeric.", "exception": ""}}
        else:
            # cep is None
            self.cep_root5 = None
            # Set error message
            self.error = {"error": {"message": "Data in 'cep' key is empty.", "exception": ""}}

    def _validate(self):
        '''
            Function to validate the cep data. It checks if the cep_root5 preprocessed before is in cep_table field CEP_Root5.
            If true set valid to True, otherwise set valid to False.
        '''
        # validate the cep_root5
        if self.cep_root5:
            if self.cep_root5 in self.cep_table['CEP_Root5'].values:
                # If cep_root5 is in the table content
                self.valid = True
            else:
                # If cep_root5 is not in the table content
                self.valid = False
        else:
            # If cep_root5 is None
            self.valid = False
    
    def output(self):
        '''
            Function to generate the output.
        '''
        if self.error:
            output = self.error
        else:
            output = {'cep_validation': self.valid,
                    'cep_data': self.cep_root5}
        return output