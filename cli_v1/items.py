from pydantic import BaseModel, Field
from typing import List
import json

class ConfigDataModel(BaseModel):
    email_method: str = Field(default="outlook", description="Email method (outlook/smtp)")
    
    login_email: str = Field(default="", description="Login email for SMTP")
    password: str = Field(default="", description="Password for SMTP")

    default_from_address: str = Field(default="", description="From address for email")
    default_message_subject: str = Field(default="", description="Default message subject")
    default_message_body: str = Field(default="", description="Default message body")
    default_attachment_filepaths: List[str] = Field(default=[], description="List of default attachment filepaths")

    input_spreadsheet: str = Field(default="", description="Path to input spreadsheet")
    output_spreadsheet: str = Field(default="", description="Path to output spreadsheet")
    processed_spreadsheet: str = Field(default="", description="Path to processed spreadsheet")
    attachment_lookup_folder: str = Field(default="", description="Path to the attachment lookup folder")
    output_folder: str = Field(default="", description="Path to the output folder")

    class Config:
        schema_extra = {
            "example": {
                "email_method": "outlook",
                "login_email": "",
                "password": "",
                "input_spreadsheet": "src/data/input_data/emails.csv",
                "global_attachments": [],
                "attachment_lookup_folder": "src/pdfs/input_pdf",
                "output_folder": "src/pdfs/output_pdf"
            }
        }
def load_config(config_path: str) -> ConfigDataModel:
    with open(config_path, 'r') as f:
        config_dict = json.load(f)
    return ConfigDataModel(**config_dict)