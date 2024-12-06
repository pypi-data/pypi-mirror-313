from dnalib.utils import TableUtils, Utils
from dnalib.log import *

class DDL:    
    """ """    
    def __init__(self, layer):
        self.layer = layer.strip().lower()    

class TableDDL(DDL):
    """ """
    def __init__(self, layer, table_name):
        super().__init__(layer)          
        self.table_name = table_name.strip().lower()

    def describe(self):
        raise NotImplementedError("Method describe() must be implemented.")    

    def create_table(self):
        raise NotImplementedError("Method create_table() must be implemented.")    

    def create_view(self):
        raise NotImplementedError("Method create_view() must be implemented.")    
        
    def drop_table(self):
        raise NotImplementedError("Method drop_table() must be implemented.")        

    def drop_view(self):
        raise NotImplementedError("Method drop_view() must be implemented.")      

    def table_exists(self):
        raise NotImplementedError("Method table_exists() must be implemented.")        

    def view_exists(self):
        raise NotImplementedError("Method view_exists() must be implemented.")        
