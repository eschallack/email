# ############################################################################ #
# CONFIGURATION SETTINGS                                                       #
# All variables uncommented are required for the program to run                #
# ############################################################################ #

email_method = "outlook" #smtp would go here but it doesnt work rn. just dont touch this.

# ##############################################  #
# uncomment below if using smtp, ignore if you're #
# using outlook                                   #
# ##############################################  #

# login_email = ""
# password = ""

# the default email adress to send from
default_from_address = ""

# subject line
default_message_subject = "Hi there!"

# body text:
default_message_body = """Dear Client,\n\n We are holding your taxes hostage.\nPlease send us $1,000,000 in unmarked bills. \n\n Sincerely, \n\n The IRS"""
# TODO: make sure you add newline breaks (like this: \n) when you want to add newlines. think of each as hitting the enter key once.

# global attachments. these wll be sent to all clients that have their corresponding pdf found.
default_attachment_filepaths = [
    # r"/Users/evanschallack/Downloads/mememme//attachment_awesome.txt",
    # ############################################ #
    # other items would go in the list like this:  #
    # "path/to/more/slop.pdf",                     #
    # "even/more/stupid/shit.jpg",                 #
    # ############################################ #
]

# input_spreadsheet: Must be a .csv file, and must include the following columns:
#       name
#       email
#       ssn
# if these are not present, the program will throw an error.

input_spreadsheet = r"C:\Users\Evan Schallack\Desktop\em-log-v2\src\data\input_data\emails.csv"

# this is where the spreadsheet will be output. these files SHOULD NOT EXIST, as the program will generate them,
# but the folders above them should:

output_spreadsheet = r"C:\Users\Evan Schallack\Desktop\em-log-v2\src\data\input_data\output.csv"
processed_spreadsheet = r"C:\Users\Evan Schallack\Desktop\em-log-v2\src\data\input_data\processed.csv"

# path to attachment folder
attachment_lookup_folder = r"C:\Users\Evan Schallack\Desktop\em-log-v2\src\pdfs\input_pdf"

# path to where the password protected pdfs will be exported to
output_folder = r"C:\Users\Evan Schallack\Desktop\em-log-v2\src\pdfs\input_pdf"