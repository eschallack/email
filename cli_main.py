import os
import argparse
from cli_v1.models import OutlookSender, SMTPSender
from cli_v1.df_utils import EmailTable, get_all_files, pw_protect_pdf, parse_file_list
import settings
from datetime import datetime, timedelta
import pandas as pd
    
if __name__ == "__main__":
    email_method = settings.email_method
    default_from_address = settings.default_from_address
    default_message_subject = settings.default_message_subject
    default_message_body = settings.default_message_body
    default_attachment_filepaths = settings.default_attachment_filepaths
    input_spreadsheet = settings.input_spreadsheet
    output_spreadsheet = settings.output_spreadsheet
    processed_spreadsheet = settings.processed_spreadsheet
    attachment_lookup_folder = settings.attachment_lookup_folder
    output_folder = settings.output_folder
    parser = argparse.ArgumentParser(description="Send emails to clients")
    
    parser.add_argument("--find_pdfs", action="store_true", help="find pdf paths")
    parser.add_argument("--pw_protect", action="store_true", help="password protect pdfs")
    parser.add_argument("--schedule_emails", action="store_true", help="schedule emails")
    parser.add_argument("--test_email", action="store_true", help="send all the processed info, just to yourself")
    parser.add_argument("--send_emails", action="store_true", help="go go go go go")
    
    args = parser.parse_args()
    if args.find_pdfs:
        em_tbl = EmailTable(csv_path=input_spreadsheet,
                         input_folder=attachment_lookup_folder,
                         output_folder=output_folder,
                         global_attachment=default_attachment_filepaths)
        df = em_tbl.find_matching_files()
        df.to_csv(output_spreadsheet)
    if args.pw_protect:
        # if the output folder doesn't exist, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        em_tbl = EmailTable(csv_path=output_spreadsheet,
                            output_spreadsheet=output_spreadsheet,
                         input_folder=attachment_lookup_folder,
                         output_folder=output_folder,
                         global_attachment=default_attachment_filepaths)
        df = em_tbl.prep_df()
        df.to_csv(output_spreadsheet)
        for index, row in em_tbl.df_processed.iterrows():
            for file in row['path_to_file']:
                pw_protect_pdf(file, "password")
    if args.schedule_emails:
        em_tbl = EmailTable(csv_path=output_spreadsheet,
                        input_folder=attachment_lookup_folder,
                        output_folder=output_folder,
                        global_attachment=default_attachment_filepaths)
        
        # Define the start time as 10 minutes from now
        start_time = datetime.now() + timedelta(minutes=10)
        min_increment = 60  # 1 minute
        max_increment = 120  # 2 minutes

        # Call the create_scheduling function with the new arguments
        df = em_tbl.create_scheduling(start_time, min_increment, max_increment)
        
        df.to_csv(processed_spreadsheet)
    if args.send_emails:
        df = pd.read_csv(processed_spreadsheet)
        for index, row in df.iterrows():
            if row['ready_to_send'] == False:
                print('did not send')
            elif row['ready_to_send'] == True:
                # each row is an email argument
                ssn = row['ssn']
                message_to = row['email']
                message_from = default_from_address
                message_subject = f"{default_message_subject} ({row['name']})"
                message_body = default_message_body
                attachment_filepath = row['attachment_filepaths']
                outlook = OutlookSender(
                     message_to, message_from, message_subject, message_body, attachment_filepath=attachment_filepath
                )
                for file in default_attachment_filepaths:
                    file_name = os.path.basename(file)
                    output_pdf_path = f"{output_folder}/{file_name}"
                    default_pdf = pw_protect_pdf(file, ssn, output_pdf_path)
                outlook.send_mail_outlook(schedule_send_time=row['datetime'], default_attachments=default_attachment_filepaths)
            

        
