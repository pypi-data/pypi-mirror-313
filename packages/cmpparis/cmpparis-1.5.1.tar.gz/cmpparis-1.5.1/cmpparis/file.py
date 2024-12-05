import pandas as pd

from cmpparis.ses_utils import *

supported_extensions = ['csv', 'xlsx']

class File:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"File({self.name})"

    def get_extension(self):
        return self.name.split(".")[-1]

    def get_name(self):
        return self.name

    def csv_to_dataframe(self):
        try:
            #read the file and convert it to a DataFrame
            with open(self.name, 'r', errors="ignore") as csv_file:
                csv_reader = pd.read_csv(filepath_or_buffer=csv_file, delimiter=';', dtype=object)

            return csv_reader
        except FileNotFoundError as e:
            raise Exception(f"The CSV file was not found : {e}")
        except Exception as e:
            raise Exception(f"Error while reading the CSV file : {e}")

    def excel_to_dataframe(self, sheet_name=None):
        try:
            if (sheet_name != None):
                excel_reader = pd.read_excel(io=self.name, sheet_name=sheet_name)
            else:
                excel_reader = pd.read_excel(io=self.name)

            return excel_reader
        except FileNotFoundError as e:
            raise Exception(f"The Excel file was not found : {e}")
        except Exception as e:
            raise Exception(f"Error while reading the Excel file : {e}")

    def extract_message_from_code(self, code):
        msg_list = self.excel_to_dataframe('MESSAGES')

        message = msg_list.loc[msg_list['code'] == code]

        return message['message'].values[0]

    #function that reads the file and sets the content inside a DataFrame according to its extension
    #supported extensions are : csv, xlsx
    #handle exceptions
    def read_file_to_dataframe(self, sheet=None):
        if (self.get_extension() not in supported_extensions):
            raise Exception("Unsupported file extension")

        file_extension = self.get_extension()

        match file_extension:
            case "csv":
                df = self.csv_to_dataframe()

                if (df.size == 0):
                    raise Exception("The dataframe is empty")

                return df
            case _:
                df = self.excel_to_dataframe(sheet)

                if (df.size == 0):
                    raise Exception("The dataframe is empty")

                return df