import pymupdf
import re
import os
from multiprocessing import Pool, cpu_count, freeze_support
from tqdm import tqdm
class PDFProcessor:
    """
    A class for processing PDF files, extracting and cleaning text, handling URLs,
    and saving the cleaned text to files. Uses multiprocessing for batch processing
    of multiple PDFs in a folder or a specified list.

    Attributes:
        input_folder (str): Path to the folder containing input PDFs.
        output_folder (str): Path to the folder where output text files will be saved.
    """

    def __init__(self, input_folder, output_folder):
        """
        Initializes the PDFProcessor with input and output folder paths.

        Args:
            input_folder (str): Path to the folder with PDF files to process.
            output_folder (str): Path to save the output text files.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.create_output_folder()

    def create_output_folder(self):
        """
        Creates the output folder if it doesn't already exist.
        """
        os.makedirs(self.output_folder, exist_ok=True)

    @staticmethod
    def clean_string(text):
        """
        Cleans non-breaking spaces and removes non-ASCII characters.

        Args:
            text (str): The text to clean.

        Returns:
            str: Cleaned text with non-breaking spaces removed and non-ASCII
                 characters stripped.
        """
        
        text =  text.replace('\xa0', ' ').strip().encode('ascii', 'ignore').decode("iso-8859-8")
        text = text.replace("Conicts of Interest", "Conflict of Interest")
        text = text.replace("condential","confidential")
        text = text.replace("supplement le","supplement file")
        text = text.replace("Charit ", "Charité ")
        text = text.replace("Charite ", "Charité ")
        text = text.replace("Charite ","Charité ")
        text = text.replace("nngen./","finngen.fi/")
        text = text.replace("Source Data le","Source Data file")
        text = text.replace("the ndings","the findings")
        text = text.replace("Data and code availability d","Data and code availability")
        text = text.replace(".gshare",".figshare")
        text = text.replace("/gshare","/figshare")
        text = text.replace("num ber","number")
        text = text.replace("Pzer","Pfizer")
        text = text.replace("(ttps","(https")
        text = text.replace("data les","data files")
        text = text.replace("data_les","data_files")
        text = text.replace("additional le","additional file")
        text = text.replace("data le","data file")
        text = text.replace("da ta","data")
        text = text.replace("/ m9","/m9")
        text = text.replace("Conict of Interest","Conflict of Interest")
        text = text.replace("pub licly","publicly")
        text = text.replace("comprise","compromise")
        text = text.replace("sensi ble","sensible")
        text = re.sub(r'www\.\s+', 'www.', text)

        return text

    @staticmethod
    def replace_exact_word(text, old_word, new_word):
        """
        Replaces exact occurrences of a specified word with a new word in the text.

        Args:
            text (str): The text to modify.
            old_word (str): The word to replace.
            new_word (str): The word to replace with.

        Returns:
            str: Text with the specified word replaced.
        """
        pattern = r'\b' + re.escape(old_word) + r'\b'
        return re.sub(pattern, new_word, text)

    @staticmethod
    def extract_links(link_data):
        """
        Extracts unique URLs from a list of link data dictionaries.

        Args:
            link_data (list): A list of dictionaries containing link information.

        Returns:
            list: A list of unique URLs found in the link data.
        """
        links = [link['uri'] for link in link_data if 'uri' in link]
        return list(set(links))  # Remove duplicates

    @staticmethod
    def join_text(text):
        """
        Joins text by removing line breaks, special characters, and unnecessary whitespace.

        Args:
            text (str): The text to join.

        Returns:
            str: Joined and cleaned text.
        """
        text = text.replace("¼", "=")
        text = " ".join(text.split("\n"))
        text = text.replace("- ","").replace("  "," ")
        return text
    
    @staticmethod
    def format_url_string_pattern(input_string):
        """
        Formats a URL string into a regex pattern that allows for flexible matching
        by handling whitespace and newline characters, as well as special characters.

        Args:
            input_string (str): The URL string to format.

        Returns:
            str: A regex pattern for flexible matching of the URL.
        """
        join_non_special_char = r"(\s*|\\n*)"
        join_special_char = r"(\s*|\\n*)" + "\\"
        
        result = []
        
        def is_special_char(char):
            special_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
            return char in special_chars
        
        for char in input_string:
            if is_special_char(char):
                result.append(join_special_char + char)
            else:
                result.append(join_non_special_char + char)
        
        return ''.join(result)

    def replace_text_with_links(self, text, links):
        """
        Replaces occurrences of links in the text with the actual link values.

        Args:
            text (str): The text to search and replace links in.
            links (list): A list of link strings to replace in the text.

        Returns:
            str: Text with links replaced by their actual values.
        """
        for link in links:
            if "penalty" in link or "ignorespaces" in link:
                continue
            try:
                link = link.replace("%20\\l%20", "#")
                pattern = PDFProcessor.format_url_string_pattern(str(link))
                text = re.sub(pattern, f" {link} ", text, flags=re.IGNORECASE)
            except re.error:
                print(f"Error with link: {link}")
        return text
        
    def extract_pdf_text(self, pdf_path, output_txt_path):
        """
        Extracts and cleans text and URLs from a PDF file, then saves the output
        to a text file.

        Args:
            pdf_path (str): Path to the PDF file to process.
            output_txt_path (str): Path to save the output text file.
        """
        doc = pymupdf.open(pdf_path)

        with open(output_txt_path, 'w', encoding='utf-8') as f:
            for page in doc:
                page.wrap_contents()
                text = page.get_text("text")
                text = self.clean_string(text)
                links = self.extract_links(page.get_links())

                if links:
                    text = self.replace_text_with_links(text, links)
                f.write(self.join_text(text) + "\n")

        doc.close()

    def extract_pdf_text_to_memory(self, pdf_path):
        """
        Extracts and cleans text and URLs from a PDF file, storing the output in memory.

        Args:
            pdf_path (str): Path to the PDF file to process.

        Returns:
            str: The combined and cleaned text of all pages in the PDF.
        """
        
        doc = pymupdf.open(pdf_path)
        extracted_texts = []

        for page in doc:
            page.wrap_contents()
            text = page.get_text("text")
            text = self.clean_string(text)
            links = self.extract_links(page.get_links())

            if links:
                text = self.replace_text_with_links(text, links)
            extracted_texts.append(self.join_text(text)+ "\n")

        doc.close()
        result = " ".join(extracted_texts)
        result = self.clean_string(result)
        return result
    
    def process_pdf_wrapper(self, args):
        """Wrapper function to handle arguments for extracting PDF info."""
        pdf_path, output_txt_path = args
        self.extract_pdf_text(pdf_path, output_txt_path)

    def process_pdf_folder(self):
        """Process all PDF files in the given folder using multiprocessing."""
        pdf_files = [f for f in os.listdir(self.input_folder) if f.endswith('.pdf')]
        pdf_file_paths = [os.path.join(self.input_folder, f) for f in pdf_files]
        output_txt_paths = [os.path.join(self.output_folder, f"{os.path.splitext(f)[0]}.txt") for f in pdf_files]

        args = zip(pdf_file_paths, output_txt_paths)
        with Pool(processes=cpu_count()) as pool:
            results = list(tqdm(pool.imap(self.process_pdf_wrapper, args),
                                total=len(pdf_files), desc="Converting PDFs", unit="file"))

        print("All PDFs processed with URLs fixed")
        return results
    
    def process_pdf_list(self):
        """Process the given list of PDF file paths using multiprocessing."""

        # Filter to include only PDF files
        pdf_files = [f for f in self.input_folder if f.lower().endswith('.pdf')]
        
        # Generate corresponding output .txt paths
        output_txt_paths = [os.path.join(self.output_folder, f"{os.path.splitext(os.path.basename(f))[0]}.txt") for f in pdf_files]

        # Prepare arguments for processing
        args = zip(pdf_files, output_txt_paths)
        
        # Use multiprocessing to process PDFs
        with Pool(processes=cpu_count()) as pool:
            results = list(tqdm(pool.imap(self.process_pdf_wrapper, args),
                                total=len(pdf_files), desc="Converting PDFs", unit="file"))

        print("All PDFs processed with URLs fixed")
        return results

if __name__ == '__main__':
    freeze_support()
