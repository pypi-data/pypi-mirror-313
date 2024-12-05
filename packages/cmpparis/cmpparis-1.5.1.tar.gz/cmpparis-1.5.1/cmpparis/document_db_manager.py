####################################################
# document_db_manager.py for the 'cmpparis' library
# Created by: Sofiane Charrad
####################################################

import os
import pymongo
import sys
import urllib

from bson import ObjectId
from datetime import datetime

class DocumentDBManager:
    def __init__(self, db_user="root", db_pwd="", db_host="localhost", database_name="my_database", collection_name="my_collection", pem_file_path=None):
        self.db_user = db_user
        self.db_pwd = db_pwd
        self.db_host = db_host
        self.database_name = database_name
        self.collection_name = collection_name
        self.pem_file_path = pem_file_path or '/opt/python/utils/global-bundle.pem'
        
        if not os.path.exists(self.pem_file_path):
            self.pem_file_path = os.path.join(os.path.dirname(__file__), 'global-bundle.pem')
        
        self.client = self.connect_to_documentdb()
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

    def connect_to_documentdb(self):
        try:
            client = pymongo.MongoClient(
                f"mongodb://{self.db_user}:{self.db_pwd}@{self.db_host}:27017/?tls=true&tlsCAFile={self.pem_file_path}&retryWrites=false&directConnection=true")
            print("Client ok :", client)
            return client
        except Exception as e:
            print("Error while connecting to DocumentDB : ", e)
            sys.exit(1)

    def insert_document(self, document):
        try:
            document['createdAt'] = datetime.now()
            document['lastModificationAt'] = datetime.now()

            result = self.collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            print(f"Error while inserting data into documentDB : {e}")

    def update_document(self, filter_criteria, update_data):
        try:
            result = self.collection.update_one(filter_criteria, {'$set': update_data})
            return result.modified_count
        except Exception as e:
            print(f"Error while updating data in documentDB : {e}")

    def get_document(self, column, value):
        try:
            return self.collection.find_one({column: value})
        except Exception as e:
            print(f"Error while getting data from documentDB : {e}")

    def get_documents(self, projection=None, filter=None):
        try:
            return self.collection.find(filter=filter, projection=projection)
        except Exception as e:
            print(f"Error while getting data from documentDB : {e}")

    def update_list_in_document(self, filter, list_name, list_value):
        try:
            self.collection.update_one(filter, {"$push": {list_name: list_value}})
        except Exception as e:
            print(f"Error while updating list in documentDB : {e}")

    def delete_document(self, id):
        try:
            self.collection.delete_one({"_id": id})
            print("Document successfully deleted")
        except Exception as e:
            print(f"Error while deleting data from documentDB : {e}")

    def delete_all_documents(self):
        try:
            self.collection.delete_many({})
            print("All documents are successfully deleted")
        except Exception as e:
            print(f"Error while deleting data from documentDB : {e}")