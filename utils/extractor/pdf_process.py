from utils.extractor.pdf_convert_with_url import PDFProcessor
from utils.extractor.pdf_section_extractor import extract_methods_section,extract_discussion_section,remove_references_section
import os

def process_single_pdf_text(pdf_file):
    """Process a single PDF file and return the text content."""
    try:
        output_txt_path = pdf_file.replace('.pdf', '.txt')
        processor = PDFProcessor("tmp", "tmp")
        processor.extract_pdf_text(pdf_file, output_txt_path)
        
        # Read the extracted text for display in the textbox
        with open(output_txt_path, 'r') as file:
            extracted_text = file.read()
        
        # Clean up temporary text file
        os.remove(output_txt_path)

        print(extracted_text)
        
        return extracted_text  # Return both text and path to the text file
        
    except Exception as e:
        return f"Error converting the PDF file: {str(e)}"

def extract_methods_and_discussion(pdf_file, section):
    """Extract Methods and Discussion sections from the PDF text."""
    try:
        text = process_single_pdf_text(pdf_file)
        text_without_ref = remove_references_section(text)

        if section == 'methods':
            return extract_methods_section(text_without_ref)
        elif section == 'discussion':
            return extract_discussion_section(text_without_ref)
        elif section == 'all':
            return text
    except Exception as e:
        return f"Error extracting sections: {str(e)}"
    
def extract_methods_and_discussion_from_txt(text, section):
    """Extract Methods and Discussion sections from the PDF text."""
    try:
        text_without_ref = remove_references_section(text)

        if section == 'methods':
            return extract_methods_section(text_without_ref)
        elif section == 'discussion':
            return extract_discussion_section(text_without_ref)
        elif section == 'all':
            return text
    except Exception as e:
        return f"Error extracting sections: {str(e)}"


# print(process_single_pdf_text('PDFs_ARRIVE/10.3389+fphar.2020.596539.pdf'))
# print(extract_methods_and_discussion('../../../PDFs_test/10.1002+14651858.cd001218.pub3.pdf','methods'))
