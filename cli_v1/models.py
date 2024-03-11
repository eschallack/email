import os
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime
import pytz
import win32com.client
from typing import Any, Optional

from cli_v1.df_utils import EmailTable

import sys

# Get the directory where the data has been extracted
data_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

class OutlookSender:
    def __init__(self, message_to, message_from, message_subject, message_body, attachment_filepath:list[Any]=None):
        self.message_to = message_to
        self.message_from = message_from
        self.message_subject = message_subject
        self.message_body = message_body
        self.attachment_filepaths = attachment_filepath
   
    def send_mail_outlook(self, schedule_send_time: Optional[datetime] = None, default_attachments=None):

        outlook = win32com.client.gencache.EnsureDispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.Subject = self.message_subject
        mail.Body = self.message_body
        mail.To = self.message_to
        if isinstance(self.attachment_filepaths, list):
            for attachment in self.attachment_filepaths:
                absolute_path = os.path.abspath(attachment)
                mail.Attachments.Add(absolute_path)
        if isinstance(default_attachments, list):
            for attachment in default_attachments:
                absolute_path = os.path.abspath(attachment)
                mail.Attachments.Add(absolute_path)
        if schedule_send_time:
            aware_schedule_send_time = schedule_send_time.astimezone(pytz.timezone('US/Eastern'))
            mail.DeferredDeliveryTime = aware_schedule_send_time
        print(f"Sending email to {self.message_to}...")
        mail.Send()
        print(f"Email sent to {self.message_to}...")

        
    def get_most_recent_email(self):
        try:
            outlook = win32com.client.gencache.EnsureDispatch("Outlook.Application")
            inbox = outlook.GetNamespace("MAPI").GetDefaultFolder(6)
            messages = inbox.Items
            message = messages.GetLast()
            print(message.Subject)
            print(message.Body)
            print(message.To)
            print(message.SentOn)
            return message
        except Exception as e:
            print(f"Error: {e}")

class SMTPSender:
    def __init__(self, message_to, message_from, message_subject, message_body, attachment_filepaths=None):
        self.message_to = message_to
        self.message_from = message_from
        self.message_subject = message_subject
        self.message_body = message_body
        self.attachment_filepath = attachment_filepaths
        
    def construct_email(self) -> MIMEMultipart:
        message = MIMEMultipart()
        message['To'] = self.message_to
        message['From'] = self.message_from
        message['Subject'] = self.message_subject
        body = MIMEText(self.message_body)
        message.attach(body)
        if isinstance(self.attachment_filepaths, list):
            for attachment in self.attachment_filepaths:
                with open(attachment, "rb") as f:
                    attach = MIMEApplication(f.read(), _subtype="pdf")
                file_name = os.path.basename(attachment)
                attach.add_header('Content-Disposition', 'attachment', filename=file_name)
                message.attach(attach)
        
        elif self.attachment_filepaths is None:
            pass
        else:
            raise ValueError(f"you did something wacky. {type(self.attachment_filepaths)} is not supported")
        return message

    def send_mail_smtp(self, server:smtplib.SMTP, login_email=None, password=None, host='smtp.gmail.com', port=587):
        try:
            server.send_message(self.construct_email())
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

def login_smtp(login_email:str, password:str, host:str='smtp.gmail.com', port:int=587) -> smtplib.SMTP:
    server = smtplib.SMTP(host=host, port=port)
    server.starttls()
    server.debuglevel = 1
    print(f"logging in with {login_email} and {password}")
    server.login(login_email, password)
    return server



def spreadsheet_to_mail(df:pd.DataFrame, message_from, message_subject_prefix, messgae_body, method='smtp',global_attachment=None, output_spreadsheet:str=None, processed_spreadsheet:str=None):
    df_completed = pd.DataFrame(columns=df.columns)

    num_rows_skipped = 0
    num_rows_completed = 0
    for index, row in df.iterrows():
        if row['ready_to_send'] == False:
            num_rows_skipped += 1
            print(f"skipping {row['name']}...")
        elif row['ready_to_send'] == True:
            client_name = row['name']
            attachment_filepath = row['attachment_filepaths']
            message_to = row['email']
            message_subject = f"{message_subject_prefix}({client_name})"
            if method == 'smtp':
                print(f"Sending Email via smtp to {client_name}...")
                arg_list = [message_to, message_from, message_subject, messgae_body]
                for arg in arg_list:
                    print(arg)
                isSent = SMTPSender(message_to, message_from, message_subject, messgae_body,password=None, attachment_filepath=attachment_filepath, global_attachment=global_attachment)
            elif method == 'outlook':
                schedule_send_time = None
                if row['datetime']:
                    schedule_send_time = row['datetime']
                print(f"Sending Email via outlook to {client_name}...")
                isSent = OutlookSender(message_to, message_from, message_subject, messgae_body, attachment_filepath=attachment_filepath,global_attachment=global_attachment, schedule_send_time=schedule_send_time)
            else:
                raise ValueError(f"you did something wacky. {method} is not a valid email method")
            num_rows_completed += 1
            # add the row to a new dataframe
            df_completed = pd.concat([df_completed, row], axis=0)
            df.drop(index, inplace=True)
        print(f"Emails Sent: {num_rows_completed}")
        print(f"Emails Skipped: {num_rows_skipped}")
    
    df_completed.to_csv(processed_spreadsheet, index=False)

