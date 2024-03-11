from PyPDF2 import PdfReader, PdfWriter

def pw_protect_pdf(path_to_pdf:str, ssn:int, output_file_path) -> str:
    out = PdfWriter() 
        # Open our PDF file with the PdfFileReader 
    file = PdfReader(path_to_pdf) 
    # Get number of pages in original file 
    num = len(file.pages) 
    # Iterate through every page of the original  
    # file and add it to our new file. 
    for idx in range(num): 
        # Get the page at index idx 
        page = file.pages[idx]
        # Add it to the output file 
        out.add_page(page) 
    # Encrypt the new file with the entered password 
    pw = str(ssn)
    out.encrypt(pw) 
    # Open a new file "myfile_encrypted.pdf" 
    with open(output_file_path, "wb") as f: 
        
        # Write our encrypted PDF to this file 
        out.write(f)
    return output_file_path