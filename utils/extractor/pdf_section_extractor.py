import  re

# Define regex patterns
alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He|She|It|They|Their|Our|We|But|However|That|This|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = r"([A-Za-z0-9._%+-]+(?:\.[A-Za-z]{2,})+)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

def split_into_sentences(text):
    """
    Split the text into sentences without adding any tags.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    # Surround text with spaces for easier matching
    text = " " + text + " "
    
    # Replace newlines with spaces
    text = text.replace("\n", " ")

    # Replace periods for starters and endings while handling acronyms and decimals
    text = re.sub(prefixes, "\\1.", text)  # Handle prefixes
    text = re.sub(digits + "[.]" + digits, "\\1.\\2", text)  # Handle decimal numbers
    text = re.sub(multiple_dots, lambda match: '.' * len(match.group(0)), text)  # Handle multiple dots

    # Handle special cases like Ph.D.
    text = text.replace("Ph.D.", "Ph.D.")  # Special case for "Ph.D."

    # Replace abbreviations with periods
    text = re.sub(r"\s" + alphabets + r"[.] ", r" \1. ", text)  # Handle abbreviation followed by space
    text = re.sub(acronyms + " " + starters, r"\1 \2", text)  # Handle acronyms followed by sentence starters
    text = re.sub(alphabets + r"[.]" + alphabets + r"[.]" + alphabets + r"[.]", r"\1.\2.\3.", text)  # Handle multiple acronyms
    text = re.sub(alphabets + r"[.]" + alphabets + r"[.]", r"\1.\2.", text)  # Handle pairs of acronyms
    text = re.sub(" " + suffixes + "[.] " + starters, r" \1 \2", text)  # Handle suffixes followed by starters
    text = re.sub(" " + suffixes + "[.]", r" \1.", text)  # Handle suffixes
    text = re.sub(" " + alphabets + "[.]", r" \1.", text)  # Handle single alphabets followed by a period

    # Replace punctuation marks with their variations
    text = text.replace(".”", ".”")
    text = text.replace(".\"", "\".")
    text = text.replace("!\"", "\"!")
    text = text.replace("?\"", "\"?")
    
    # Split sentences by common sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split at end of sentence punctuation
    
    # Handle any remaining spaces and empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty sentences
    return sentences

REFERENCES_TERMS = ['Citations', 'References', 'Bibliography', 'Works Cited']
DISCUSSION_TERMS = ['Results and discussion','Discussion','Discussions', 'Discussion and conclusion', 'Discussion and Conclusions','Lessons learned','General discussion']
METHODS_TERMS = ['STAR+METHODS','Method details','System and methods','Methods and results',"Methods and results:",'Experimental','Method','Methodology', 'Methods','Protocol', 'Intervention Description', 'Materials and Methods','Methods and materials', 'Materials and methods','Materials and method',  'Material and Method', 'Material and methods','Experimental methods', 'Materials and Methods', 'Materials and methods', 'Material & Method', 'Material & method',  'Materials & Methods', 'Materials & methods',  'Online Methods', 'Online methods', 'Online method', 'Online Method','Experimental procedures','Study population and procedures','Patients and methods']
DISCUSSION_END_TERMS = METHODS_TERMS + ['Citations', 'References',  'Bibliography',  'Works Cited',  'Acknowledgements',  'Author contribution', 'Author contributions', 'Contributions',  'Conflicts of interest', 'Conflict of interest', 'Data availability',  'Code availability','Data accessibility' , 'Conclusion',  'Conclusions','Funding','acknowledgments','acknowledgment','Supplementary Materials']
METHODS_END_TERMS = REFERENCES_TERMS + DISCUSSION_TERMS + ['Conclusion:','Conclusions:','Citations', 'References',  'Bibliography',  'Works Cited',  'Acknowledgements',  'Author contribution', 'Author contributions', 'Contributions',  'Conflicts of interest', 'Conflict of interest', 'Data availability',  'Code availability','DATA AND CODE AVAILABILITY' ,'DATA AND SOFTWARE AVAILABILITY', 'Conclusion',  'Conclusions','Funding'] + ['Results', 'Result', 'Experiments','acknowledgments','Perspective','Case reports','Outcome']
REFERENCES_END_TERMS = METHODS_TERMS
REFERENCES_END_TERMS_APX = ['STAR+METHODS','Citations', 'References',  'Bibliography',  'Works Cited',  'Acknowledgements',  'Author contribution', 'Author contributions', 'Contributions',  'Conflicts of interest', 'Conflict of interest', 'Data availability',  'Code availability','Data accessibility' , 'Conclusion',  'Conclusions','Funding','acknowledgments','acknowledgment','Supplementary Materials', 'Publishers note']
# should we add method terms like : Experimental Section


def generate_case_regex(strings, is_uppercase=False):
    patterns = []

    for s in strings:
        words = s.split()
        if not words:
            continue
        
        # Escape the first word and create a case-sensitive pattern
        first_word = re.escape(words[0])
        
        if is_uppercase:
            # Only match uppercase for the first word
            first_word_pattern = f'{first_word.upper()}'
        else:
            # Case-insensitive matching for the first word
            first_word_pattern = f'({first_word.capitalize()}|{first_word.upper()})'
        
        # Prepare to build the case-sensitive or case-insensitive pattern for the rest of the words
        rest_words = []
        for word in words[1:]:
            escaped_word = re.escape(word)
            if is_uppercase:
                # Only uppercase letters
                case_sensitive = ''.join(f'{c.upper()}' if c.isalpha() else c for c in escaped_word)
                rest_words.append(case_sensitive)
            else:
                # Case-insensitive matching for letters
                case_insensitive = ''.join(f'[{c.upper()}{c.lower()}]' if c.isalpha() else c for c in escaped_word)
                rest_words.append(case_insensitive)
        
        # Combine the first word with the rest to form a full pattern
        full_pattern = r'\b' + first_word_pattern + r'\s+' + r'\s+'.join(rest_words) 
        
        # Add the condition for the following word (digit or capital letter) before the word boundary
        full_pattern += r'\s*(?=\d+|[A-Z]\w*)\b'
        
        # Add the full pattern (for longer matches)
        patterns.append(full_pattern)
        
        # Now, handle the uppercase letter sequences separated by spaces (e.g., M E T H O D S)
        # If the string contains more than one word, add space between spaced-uppercase patterns for each word
        spaced_uppercase_words = []
        for word in words:
            spaced_uppercase = r'\b' + r'\s*'.join(list(word.upper())) + r'\b'
            spaced_uppercase_words.append(spaced_uppercase)
            
        # Join spaced-uppercase patterns with space between them if there are multiple words
        spaced_full_pattern = r'\s+'.join(spaced_uppercase_words)
        spaced_full_pattern = spaced_full_pattern.replace('*+','*\+')
        
        # Add this spaced-uppercase pattern
        patterns.append(spaced_full_pattern)
    
    # Sort patterns to ensure longer matches are prioritized
    patterns.sort(key=len, reverse=True)
    
    # Join all patterns with OR |
    return '|'.join(patterns)

# ex = ['Experimental','Experimental methods']
# print(generate_case_regex(ex))
# print(generate_case_regex(METHODS_TERMS))
# print(generate_case_regex(REFERENCES_TERMS))

def extract_section(text, start_terms, end_terms):
    """
    Extracts the longest section of the text between start_terms and end_terms.
    Excludes sections where "cf" or "cf." appears immediately before the start term.
    
    :param text: The raw text from which to extract the section.
    :param start_terms: The regex pattern indicating the start of the section.
    :param end_terms: The regex pattern indicating the end of the section.
    
    :return: The longest extracted section text, or an empty string if not found.
    """
    # Compile case-insensitive regex patterns for start and end terms
    start_terms = generate_case_regex(start_terms)
    end_terms = generate_case_regex(end_terms)
    
    # Pattern to exclude 'cf' or 'cf.' before the start_terms
    cf_exclude_pattern = rf"(?:cf|cf\.)\s*"

    longest_section = ""
    matched_start_term = ""

    # Find all start terms in the text
    for match in re.finditer(start_terms, text):
        # Get the start index of the current match
        start_index = match.start()

        # Check if the start term is preceded by 'cf' or 'cf.'
        if start_index > 0:
            preceding_text = text[start_index - 4:start_index].strip()
            # Check if 'cf' or 'cf.' appears at the end of the preceding text
            if re.search(cf_exclude_pattern, preceding_text, re.IGNORECASE):
                continue  # Skip this match if 'cf' is found before it
        
        # Check if the next word starts with a capital letter
        # Extract the text after the start match to find the first word
        post_match_text = text[match.end():].strip()
        next_word_match = re.match(r"\b[A-Z\d]\w*\b", post_match_text)
        # print("nextword",next_word_match)
        if not next_word_match:
            continue  # Skip if the next word doesn't start with a capital letter
        
        # Now find the end term after the current start term
        end_search = re.search(end_terms, text[match.end():])
        # print("endserach",end_search)
        if end_search:
            # Get the end index of the match
            end_index = match.end() + end_search.start()
            
            # Check if the word following the end term starts with a capital letter
            after_end_text = text[end_index:].strip()
            next_word_after_end = re.match(r"\b[A-Z][a-zA-Z]*\b", after_end_text)

            if next_word_after_end:
                # Extract the section between the start and end points
                section = text[match.end():end_index].strip()
            else:
                continue  # Skip this end match if the next word after it doesn't start with a capital letter
        else:
            # If no end marker is found, return everything after the start
            section = text[match.end():].strip()
        
        # Update if the current section is longer than the previously found one
        if len(section) > len(longest_section):
            longest_section = section
            matched_start_term = match.group()

    if longest_section:
        return f"{matched_start_term} {longest_section}"
    else:
        return ""

def extract_methods_section(text):
    """
    Extracts the methods section from the given text.

    :param text: The raw text from which to extract the methods section.
    :return: The methods section text.
    """
    return extract_section(text, METHODS_TERMS, METHODS_END_TERMS)

def extract_discussion_section(text):
    """
    Extracts the discussion section from the given text.

    :param text: The raw text from which to extract the discussion section.
    :return: The discussion section text.
    """
    return extract_section(text, DISCUSSION_TERMS, DISCUSSION_END_TERMS)

def remove_references_section(text):
    """
    Removes the 'References' section and everything that follows in the given text.
    The removal considers end terms, such as methods and discussion markers,
    to ensure it properly captures the references section.
    Also checks for the word 'TABLE' in the two preceding sentences to avoid false matches.
    
    :param text: The raw text from which to remove the references section.
    :return: The text without the references section.
    """
    
    # ijra2 7tirazi
    text = text.replace("Animal Experiments Committee","Animal experiments Committee").replace("Experimental Therapeutics","experimental Therapeutics")
    text = text.replace("Experimental Ophthalmology","experimental Ophthalmology").replace("Experimental Medicine", "experimental Medicine")
    text = text.replace('Experimental Approach','experimentals approach').replace("EXPERIMENTAL AND THERAPEUTIC","experimental AND THERAPEUTIC")
    text = text.replace("Experimental Procedures)","experimental procedures)").replace("described in Protocol","described in protocol")
    text = text.replace("In Vitro Experiments","In Vitro experiments").replace("In Vivo Experiments","In Vivo experiments")
    text = text.replace("Experimental TBI", "Experimental tBI").replace("Experimental Traumatic","experimental Traumatic")
    text = text.replace("AcknowledgmentsWe","Acknowledgments We")
    
   # Create regex patterns for detecting the start and end of the references section
    references_pattern = generate_case_regex(REFERENCES_TERMS)
    references_end_pattern = generate_case_regex(REFERENCES_END_TERMS, is_uppercase=True)   
    references_end_pattern_apx = generate_case_regex(REFERENCES_END_TERMS_APX)
    re.compile(references_pattern)
    re.compile(references_end_pattern)
    re.compile(references_end_pattern_apx)
    
    # Search for matches
    matches = list(re.finditer(references_pattern, text))

    for match in matches:
        # Get the text before the match
        pre_match_text = text[:match.start()]
        
        # Split into sentences (simple split by period, exclamation, question mark)
        sentences = re.split('[.!?]+', pre_match_text)
        
        # Get the last two sentences if they exist
        last_two_sentences = sentences[-2:] if len(sentences) >= 2 else sentences
        combined_sentences = ' '.join(last_two_sentences)
        
        # Check if 'TABLE' (case insensitive) is in the last two sentences
        if not re.search(r'table', combined_sentences, re.IGNORECASE):
            # This is a valid reference section match
            # Look for the end of the references section
            end_match = re.search(references_end_pattern, text[match.end():])
            end_match_2 = re.search(references_end_pattern_apx, text[match.end():])
            
            if end_match_2:
                return text[:match.start()].strip() + " " + text[match.end() + end_match_2.start():].strip()
            
            if end_match:
                # Slice the text, excluding the references section up to the end term
                return text[:match.start()].strip() + " " + text[match.end() + end_match.start():].strip()
            else:
                # If no end marker is found, remove everything after the references section
                return text[:match.start()].strip()

    return text

def process_text(text):
    """
    Removes the references section, and then extracts the methods and discussion sections.
    
    :param text: The raw text to process.
    :return: A tuple containing the methods and discussion sections.
    """
    text_without_references = remove_references_section(text)
    # print(text_without_references)
    # print(text)
    # Extract the methods and discussion sections
    methods_section = extract_methods_section(text_without_references)
    discussion_section = extract_discussion_section(text_without_references)
    
    return methods_section, discussion_section




# references_end_pattern = generate_case_regex(list(set([x.upper() for x in REFERENCES_END_TERMS])), is_uppercase=True)   
# print(references_end_pattern)
# re.compile(references_end_pattern)
# # load text from txt file 
# with open('PDFs_ARRIVE/10.1021+acschemneuro.7b00260.txt', 'r',encoding='ISO-8859-1') as file:
#     text = file.read()

# Extract methods and discussion sections
# print(text,"="*200)
# methods,discussion= process_text(text)

# discussion = extract_discussion_section(text)

# print("Methods Section:")
# print(methods)
# print("\nDiscussion Section:")
# print(discussion)


