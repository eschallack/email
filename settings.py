# ############################################################################ #
# CONFIGURATION SETTINGS                                                       #
# All variables uncommented are required for the program to run                #
# ############################################################################ #

email_method = "outlook" #outlook or smtp

# #############################################################  #
# uncomment below if using smtp, ignore if using outlook locally #
# #############################################################  #

# login_email = ""
# password = ""

# the default email adress to send from
default_from_address = ""

# subject line
default_message_subject = "Hi there!"

# body text:
default_message_body = """Dear Client,\n\n \\n\n Sincerely, \n\n """

# global attachments. these wll be sent to all clients that have their corresponding pdf found.
default_attachment_filepaths = [
    # "my_attachment.txt",
    # other items would go in the list like this:  #
    # "path/to/file.pdf",                     #
    # "path/to/image.jpg",                 #
    # ############################################ #
]

# input_spreadsheet: Must be a .csv file, and must include the following columns:
#       name
#       email
#       search_value
# if these are not present, the program will throw an error.

input_spreadsheet = "emails.csv"

# this is where the spreadsheet will be output. these files SHOULD NOT EXIST, as the program will generate them,
# but the folders above them should:

output_spreadsheet = "output.csv"
processed_spreadsheet = "processed.csv"

# path to attachment folder
attachment_lookup_folder = "input_pdfs"

# path to where the password protected pdfs will be exported to
output_folder = "input_pdf"

protect_pdf_mode = True # if true, the program will password protect the pdfs. if false, it will not.
