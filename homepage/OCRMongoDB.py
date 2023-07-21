import pymongo
from pymongo import MongoClient

def get_database():    
    CONNECTION_STRING = "mongodb+srv://root:SalmonRES@whatsappresbot.9dsq1g0.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    return client['OCRDatabase']
    #print(client) 
    
def get_database_new():    
    CONNECTION_STRING = "mongodb+srv://root:SalmonRES@whatsappresbot.9dsq1g0.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    return client['OCRDatabase']
    #print(client) 

def document_info(file_name):    
    page_id = 0 
    spreadsheet_id = ''
    dbname = get_database()
    dbOCRDocument = dbname["MeggitInvoice"]
    agents_details = dbOCRDocument.find()

    for agent in agents_details:        
        # while spreadsheet_id == '':
        if file_name == agent['filename']:
            spreadsheet_id = agent['spreadsheet_id']
            print(spreadsheet_id)
            page_id = agent['page_id']
            # break
        else:
            continue
    return spreadsheet_id, page_id
    

def document_info_new(file_name):    
    page_id = 0 
    spreadsheet_id = ''
    dbname = get_database_new()
    dbOCRDocument = dbname["GeneralInvoice"]
    agents_details = dbOCRDocument.find()

    for agent in agents_details:        
        # while spreadsheet_id == '':
        if file_name == agent['filename']:
            spreadsheet_id = agent['spreadsheet_id']
            print(spreadsheet_id)
            page_id = agent['page_id']
            # break
        else:
            continue
    return spreadsheet_id, page_id