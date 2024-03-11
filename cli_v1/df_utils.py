import os
import pandas as pd
from pathlib import Path
import pytz
from cli_v1.pdf_utils import pw_protect_pdf
from cli_v1.utils import parse_file_list, get_all_files
import random
from datetime import datetime, timedelta

class EmailTable:
    def __init__(self, csv_path:str=None,output_spreadsheet=None, input_folder:str=None, output_folder:str=None, global_attachment:str=None):
        self.df = pd.read_csv(csv_path)
        self.output_spreadsheet = output_spreadsheet
        self.pdf_input_folder = input_folder
        self.pdf_output_folder = output_folder
        self.df_processed = pd.DataFrame(columns=['name', 'email', 'ssn', 'path_to_file', 'attachment_filepaths', 'ready_to_send'])
        self.global_attachment = global_attachment
    # @property
    # def ready_to_send(self) -> pd.DataFrame:
    #     rows_ready_to_send:pd.DataFrame = self.df[self.df['ready_to_send'] == True]
    #     return rows_ready_to_send
    
    # @property
    # def not_ready_to_send(self) -> pd.DataFrame:
    #     rows_not_ready_to_send:pd.DataFrame = self.df[self.df['ready_to_send'] == False]
    #     return rows_not_ready_to_send
    def find_matching_files(self,see_result=True) -> pd.DataFrame:
        pdf_paths:list[str] = get_all_files(self.pdf_input_folder)
        self.df['path_to_file'] = [[] for _ in range(len(self.df))]
        self.df['ready_to_send'] = [False for _ in range(len(self.df))]
        # itterating (looping) through the spreadsheet
        found_paths = []
        for index, row in self.df.iterrows():
            # grab the data from the row, and store it into variables
            client_name = row['name']

            files_found = parse_file_list(client_name, pdf_paths)
            if len(files_found) > 0:
                found_paths.append(files_found)
            self.df.loc[index, 'path_to_file'] = str(files_found)  # Convert list to string
        if see_result:
            self.df.to_csv('matching_files.csv')
            path_to_csv = self.df.to_csv('matching_files.csv')
            found_len = len(self.df[self.df['path_to_file'].apply(lambda x: len(x) > 2)])
            total_len = len(self.df)
            unfound_len = total_len - found_len
            
            print(f"""
                  Okay, I found {found_len} out of {total_len} files. That means there are {unfound_len} left. \n\n
                  Your file has been saved to: {path_to_csv}""")
        return self.df
    
    def prep_df(self) -> pd.DataFrame:
        # create the column names that we expect to have after processing
        
        pdf_paths:list[str] = get_all_files(self.pdf_input_folder)
        # itterating (looping) through the spreadsheet
        
        

        
        df = pd.DataFrame(columns=['name', 'email', 'ssn', 'path_to_file', 'attachment_filepaths', 'ready_to_send'])
        for index, row in self.df.iterrows():
        # grab the data from the row, and store it into variables
            attachment_output_file_paths = []
            client_name = row['name']
            message_to = row['email']
            ssn = row['ssn']
            row['path_to_file'] = parse_file_list(client_name, pdf_paths)
            if len(row['path_to_file']) > 0:
            # use the path_to_pdf and ssn to password protect the pdf. save it to a new location, and return the new filepath
                for path in row['path_to_file']:
                    file_name = os.path.basename(path)
                    output_pdf_path = f"{self.pdf_output_folder}/{file_name}"
                    if not Path(output_pdf_path).exists():
                        attachment_output_file_paths.append(pw_protect_pdf(path, ssn, output_pdf_path))
                    elif Path(output_pdf_path).exists():
                        attachment_output_file_paths.append(output_pdf_path)
            
                row['ready_to_send'] = True
            else:
                row['ready_to_send'] = False
            row['attachment_filepaths'] = attachment_output_file_paths
            # add the row to df_processed
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            self.df = df
            print(df)
        return self.df

    def add_global_attachment(self) -> pd.DataFrame:
        # if the attachment_filepaths column is not in the dataframe, create it
        if 'attachment_filepaths' not in self.df.columns:
            self.df['attachment_filepaths'] = []
        # now for each row in the dataframe, append the global attachment to each attachment_filepaths list in the column
        for index, row in self.df.iterrows():
            row['attachment_filepaths'].append(self.global_attachment)
        return self.df
    
    def create_scheduling(self, start_time:datetime, min_increment:int, max_increment:int) -> pd.DataFrame:
        current_time = start_time
        datetime_list = []
        
        for _ in self.df.index:
            datetime_list.append(current_time)
            increment = random.randint(min_increment, max_increment)
            current_time += timedelta(seconds=increment)
            
        self.df['datetime'] = datetime_list
        
        return self.df

    def validate_csv(self) -> pd.DataFrame:
        input_df_col_list = self.df.columns.tolist()
        # the columns that we expect to have before processing
        unprocessed_col_list = ['name', 'email', 'ssn']
        # the columns that we expect to have after processing
        processed_col_list = ['name', 'email', 'ssn', 'path_to_file', 'attachment_filepaths', 'ready_to_send']
        
        #  if not all the columns that we expect to have before processing are in the input spreadsheet, raise a ValueError 
        if not all(x in input_df_col_list for x in unprocessed_col_list):
            raise ValueError(f"Your spreadsheet is missing one of the following columns: {unprocessed_col_list}")
        
        # otherwise, if all the columns are there, and the processed columns are there, this means the spreadsheet has already been processed
        elif all(x in input_df_col_list for x in processed_col_list):
            print("Your spreadsheet has already been processed")
            return self.df
        
        # otherwise, if all the unprocessed columns are there, but the processed columns are not there, this means the
        # columns are ready to be processed.
        if not all(x in input_df_col_list for x in processed_col_list):
            print("Your spreadsheet is ready to be processed")
            return self.df
def init_email_table(input_spreadsheet_path:str, input_folder:str, output_folder:str) -> EmailTable:
    df = pd.read_csv(input_spreadsheet_path)
    return EmailTable(df, input_folder, output_folder)
def import_csv(path_to_csv:str) -> pd.DataFrame:
    df = pd.read_csv(path_to_csv)
    return df