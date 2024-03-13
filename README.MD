TO INSTALL:

 - make sure you have installed python 3.11.7 (the python install should be relatively easy, but there is a very important screen where, in the bottom left hand corner, there is a checkbox that says something like "Add python to path". **MAKE SURE "Add python to path" IS CHECKED!** otherwise you will have to manually add python to your path, which is not fun and can cause many problems).
 - check if python is installed by running the following command in your terminal:
 ```bash
python --version
 ```
 - check if pip is installed correctly
    ```bash
    pip list
    ```
 - if you install vscode, go to the extensions panel (icon on the left side, 3 squares and 1 extra one floating in). install the python extension.

 - getting this repository on your local machine can be donne in 1 of 2 ways:
    - you can either clone this repository to your local machine (if you have git installed) by running the following command in your terminal:
    ```bash
    gh repo clone eschallack/em-log
    ```
    - or you can download the zipfile and extract it to your documents folder (or wherever you want to keep it)


 - run the following command to create a virtual enviroment:
 ```bash
 python3 -m venv venv
 ```
 - run the following command to activate the virtual enviroment:
 ```bash
    source venv/bin/activate
```
 - now run:
 ```bash
 pip install -r requirements.txt
 ```
 
 - navigate to settings.py. read the comments in that file for instructions.

 - once you have configured your settings, navigate to the directory that cli_main is located in and run:
      python cli_main.py --find_pdfs
      python cli_main.py --pw_protect
      python cli_main.py --schedule_emails
      python cli_main.py --send_emails (if you want to test this command before running it, make a backup copy of the spreadsheet and change all of the emails to your own email, then send. they should go to yourself. then, delete the testing version, and replace it with the old correct version.)
