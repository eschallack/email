from PyPDF2 import PdfReader, PdfWriter

def pw_protect_pdf(path_to_pdf:str, search_id:int, output_file_path) -> str:
    out = PdfWriter() 
    file = PdfReader(path_to_pdf) 
    num = len(file.pages) 
    for idx in range(num): 
        page = file.pages[idx]
        out.add_page(page) 
    pw = str(search_id)
    out.encrypt(pw) 
    with open(output_file_path, "wb") as f: 
        out.write(f)
    return output_file_path