import html2text, itertools, logging, math, os, tempfile, webbrowser, spacy, ctypes, mouse
import phonenumbers, re, requests, traceback, usaddress, shutil, subprocess, random
from typing import Dict, List, Union
from datetime import datetime, timedelta
from urllib.parse import quote
from urllib.parse import urlparse
import dateutil.parser
import numpy as np
from PIL import Image
from pytesseract import pytesseract
from Levenshtein import distance as levenshtein_distance
from scrapy.selector import Selector

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

##### Functions Date ######
def difference_between_two_dates(date1: str, date2: str, format: str='%Y-%m-%d') -> int:
    """
    Calculates the absolute difference in days between two dates.

    Args:
        date1 (str): The first date as a string, to be parsed using the given format.
        date2 (str): The second date as a string, to be parsed using the given format.
        format (str): The format in which the dates are provided. Example: '%Y-%m-%d'.

    Returns:
        int: The absolute difference in days between the two dates. Returns 0 if an error occurs.

    # Example usage:
    count_days = difference_between_two_dates(date1="2024-11-01", date2="2024-11-19", format="%Y-%m-%d")
    print(count_days)  # Output: 18
    """

    count_days = 0
    try:
        # Parse the date strings into datetime objects
        date1 = datetime.strptime(date1, format)
        date2 = datetime.strptime(date2, format)

        # Calculate the absolute difference in days
        count_days = abs((date2 - date1).days)
    except:
        logging.error(traceback.format_exc())

    return count_days


def current_date(format: str = '%Y-%m-%d') -> str:
    """
    Retrieves the current date in the specified format.

    Args:
        format (str, optional): The format in which to return the current date.

    Returns:
        str: The current date formatted according to the specified format. Returns None if an error occurs.

    # Example usage:
    date = current_date('%Y-%m-%d')
    print(date)  # Output: 2024-11-19
    """

    current_date = None
    try:
        # Get the current date and time
        now = datetime.now()

        # Format the current date according to the specified format
        current_date = now.strftime(format)
    except:
        logging.error(traceback.format_exc())

    return current_date



def yesterday_date(format: str = '%Y-%m-%d') -> str:
    """
    Retrieves the date for the previous day in the specified format.

    Args:
        format (str, optional): The format in which to return the date for yesterday.

    Returns:
        str: The date for the previous day, formatted according to the specified format. Returns None if an error occurs.

    # Example usage:
    date = yesterday_date('%Y-%m-%d')
    print(date)  # Output: 2024-11-18
    """

    yesterday_date = None
    try:
        # Get the current date and subtract one day
        yesterday_date = datetime.strftime(datetime.now() - timedelta(1), format)
    except:
        logging.error(traceback.format_exc())

    return yesterday_date


def get_offset_date(days: int = 1, direction: str = '-', format: str = '%Y-%m-%d') -> str:
    """
    Retrieves a date offset by a specified number of days in the past or future.

    Args:
        days (int, optional): The number of days to offset. Defaults to 1.
        direction (str, optional): The direction of offset, either '-' for past or '+' for future. Defaults to '-'.
        format (str, optional): The format in which to return the date. Defaults to '%Y-%m-%d'.

    Returns:
        str: The offset date formatted according to the specified format. Returns None if an error occurs.

    # Example usage:
    past_date = get_offset_date(days=2, direction='-', format='%Y-%m-%d')
    print(past_date)  # Output: 2024-11-18 (if today is 2024-11-20)

    future_date = get_offset_date(days=3, direction='+', format='%Y-%m-%d')
    print(future_date)  # Output: 2024-11-23 (if today is 2024-11-20)
    """
    offset_date = None
    try:
        # Calculate the offset based on direction
        if direction == '-':
            offset_date = datetime.now() - timedelta(days=days)
        elif direction == '+':
            offset_date = datetime.now() + timedelta(days=days)
        else:
            raise ValueError("Invalid direction. Use '-' for past or '+' for future.")

        # Format the date
        offset_date = offset_date.strftime(format)
    except:
        logging.error(traceback.format_exc())

    return offset_date


def convert_ago_to_date(date_ago: str, format: str = '%Y-%m-%d') -> str:
    """
    Converts a relative time (e.g., '3 days ago', '2 hours ago') into a specific date format.

    Args:
        date_ago (str): A string representing the relative time, e.g., "3 days ago", "1 hour ago".
        format (str, optional): The desired date format for the output (default is '%Y-%m-%d').

    Returns:
        str: The calculated date in the specified format. Returns the current date if the input is invalid.

    # Example usage:
    date_converted = convert_ago_to_date(date_ago="3 days ago")
    print(date_converted)  # Output: '2024-11-16'
    """

    date_converted = datetime.now()
    try:
        time_parts = date_ago.split(" ")
        num = int(time_parts[0])  # Convert the number to an integer
        unit = time_parts[1]  # Get the unit of time (e.g., "hours", "days", etc.)

        # Get the current date and time
        now = datetime.now()

        # Subtract the specified amount of time from the current date and time
        if "second" in unit:
            date_converted = now - timedelta(seconds=num)
        elif "minute" in unit:
            date_converted = now - timedelta(minutes=num)
        elif "hour" in unit:
            date_converted = now - timedelta(hours=num)
        elif "day" in unit:
            date_converted = now - timedelta(days=num)
        elif "week" in unit:
            date_converted = now - timedelta(weeks=num)
        elif "month" in unit:
            date_converted = now - timedelta(days=num * 30)  # Assuming a month has 30 days
        elif "year" in unit:
            date_converted = now - timedelta(days=num * 365)  # Assuming a year has 365 days

        # Convert the final calculated date into the requested format
        date_converted = date_converted.strftime(format)
    except:
        logging.error(traceback.format_exc())

    return date_converted



def get_current_timestamp() -> int:
    """
    Returns the current timestamp (seconds since the Unix epoch).

    Returns:
        int: The current timestamp as an integer.

    # Example usage:
    timestamp = get_current_timestamp()
    print(timestamp)  # Output: 1699812345
    """

    now = datetime.now()
    timestamp = int(now.timestamp())
    return timestamp



def convert_string_to_date_format(date_str: str, date_format: str = '%Y-%m-%d') -> str:
    """
    Converts a date string into a specific date format.

    Args:
        date_str (str): The date string to be converted (e.g., "2024-11-19").
        date_format (str, optional): The desired format for the output date (default is '%Y-%m-%d').

    Returns:
        str: The date in the specified format.

    # Example usage:
    date_str = "2024-11-19T15:30:00Z"
    date_converted = convert_string_to_date_format(date_str, date_format='%Y-%m-%d')
    print(date_converted)  # Output: '2024-11-19'
    """

    return dateutil.parser.parse(date_str).strftime(date_format)


def split_date_range_by_number_of_days(start_date: str, end_date: str, date_format: str, chunk_days: int):
    """
    Splits a date range into smaller chunks based on a specified number of days.

    Args:
        start_date (str): The start date in string format (e.g., '2024-01-01').
        end_date (str): The end date in string format (e.g., '2024-01-10').
        date_format (str): The format string for parsing and formatting the dates (e.g., '%Y-%m-%d').
        chunk_days (int): The number of days each chunk should span.

    Returns:
        list: A list of lists, where each inner list contains the start and end dates of each chunk.

    # Example usage
    result = split_date_range_by_number_of_days(start_date="2024-01-01", end_date="2024-01-10", date_format="%Y-%m-%d", chunk_days=3)
    print(result)  # Output: [['2024-01-01', '2024-01-03'], ['2024-01-04', '2024-01-06'], ['2024-01-07', '2024-01-09'], ['2024-01-10', '2024-01-10']]
    """

    date_list = []
    try:
        # Parse start and end dates
        first_date = datetime.strptime(start_date, date_format)
        last_date = datetime.strptime(end_date, date_format)
        current_date = first_date

        # Lists to store the start and end dates of each chunk
        start_dates = []
        end_dates = []

        while current_date <= last_date:
            # Calculate the end date for the current chunk
            chunk_end_date = current_date + timedelta(days=chunk_days - 1)

            # Append the start and end dates to their respective lists
            start_dates.append(current_date.strftime(date_format))
            if chunk_end_date > last_date:
                end_dates.append(last_date.strftime(date_format))
            else:
                end_dates.append(chunk_end_date.strftime(date_format))

            # Move to the next chunk
            current_date = chunk_end_date + timedelta(days=1)

        # Combine start and end dates into pairs
        for start, end in zip(start_dates, end_dates):
            date_list.append([start, end])

    except:
        logging.error(traceback.format_exc())

    return date_list


def format_seconds(seconds: int) -> str:
    """
    Converts a given number of seconds into a readable format
    including days, hours, minutes, and seconds.

    Args:
        seconds (int): The total number of seconds to format.

    Returns:
        str: A formatted string that breaks down the time into days, hours, minutes, and seconds.
             Returns "0 sec" if the input is 0.

    # Example usage
    seconds = 90061  # 1 day, 1 hour, 1 minute, and 1 second
    print(format_seconds(seconds))  # Output: "1 day 1 hour 1 min 1 sec"
    """

    days = seconds // 86400  # 86400 seconds in a day
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    time_parts = []

    if days:
        time_parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes:
        time_parts.append(f"{minutes} min{'s' if minutes > 1 else ''}")
    if seconds or not time_parts:  # Include "0 sec" if no other time parts exist
        time_parts.append(f"{seconds} sec{'s' if seconds > 1 else ''}")

    return ' '.join(time_parts)

##### Functions Date ######


def read_txt_file_to_list(file_path: str) -> list:
    """
    Reads a text file and returns a list of unique, non-empty lines.

    Args:
        file_path (str): The path to the text file to read.

    Returns:
        list: A list of unique, stripped, and non-empty lines from the file.

    # Example usage
    file_path = "example.txt"  # A file containing some lines of text
    lines = read_txt_file_to_list(file_path)
    print(lines)  # Output: A list of unique, non-empty lines from the file
    """

    with open(file_path, 'r') as file:
        lines_txt = file.readlines()

    line_pre = [line.strip() for line in lines_txt if line.strip()]

    line_set = set()
    unique_lines = [line for line in line_pre if line not in line_set and not line_set.add(line)]
    return unique_lines



def generate_combinations(length: int = 1, use_char: bool = False, use_number: bool = False, use_special_char: bool = False) -> list:
    """
    Generates all possible combinations of characters based on specified options.

    Args:
        length (int): The length of each combination. Default is 1.
        use_char (bool): Whether to include alphabetic characters (a-z). Default is False.
        use_number (bool): Whether to include numeric characters (0-9). Default is False.
        use_special_char (bool): Whether to include special characters (-+*_). Default is False.

    Returns:
        list: A list of all possible combinations as strings.

    # Example usage
    # Generate combinations of length 2 using letters and numbers
    combinations = generate_combinations(length=2, use_char=True, use_number=False, use_special_char=False)
    print(combinations)  # Output: ['aa', 'ab', ..., 'a0', ..., 'z9']
    """

    characters = ''
    if use_char:
        characters += 'abcdefghijklmnopqrstuvwxyz'

    if use_number:
        characters += '0123456789'

    if use_special_char:
        characters += '-+*_'

    combinations = [''.join(combination) for combination in itertools.product(characters, repeat=length)]
    return combinations



def exit(status_code: int = 1):
    """
    Terminates the program with a specified exit status code.

    Args:
        status_code (int): The exit status code. Default is 1, indicating an error or abnormal termination.

    Returns:
        None: This function will terminate the program and will not return any value.

    # Example usage
    exit(0)  # Normal exit with status 0
    exit(1)  # Exit with error status code 1
    """

    os._exit(status_code)



def open_html_in_browser(html_content: str) -> bool:
    """
    Creates a temporary HTML file with the provided content and opens it in the default web browser.

    Args:
        html_content (str): The HTML content to be written to the temporary file.

    Returns:
        bool: True if the browser was successfully opened, False otherwise.

    # Example usage
    html_content = "<html><body><h1>Hello, World!</h1></body></html>"
    open_html_in_browser(html_content)  # Opens the HTML content in the browser
    """

    # Create a temporary file with an HTML extension
    fd, fname = tempfile.mkstemp('.html')

    # Write the HTML content to the temporary file
    with open(fname, 'w', encoding="utf-8") as f:
        f.write(str(html_content))

    # Close the file descriptor
    os.close(fd)

    # Open the temporary file in the default web browser
    return webbrowser.open(f"file://{fname}")


def preg_repace(patt: str, repl: str, subj: str) -> str:
    """
    Replaces occurrences of a pattern in a string with a specified replacement, using regular expressions.

    Args:
        patt (str): The regular expression pattern to search for.
        repl (str): The replacement string to substitute for the matched pattern.
        subj (str): The input string to search and replace the pattern in.

    Returns:
        str: The modified string with the pattern replaced, or the original string if an error occurs.

    # Example usage
    text = "Hello, World!"
    modified_text = preg_repace(patt="World", repl="Universe", subj=text)
    print(modified_text)  # Output: "Hello, Universe! Universe!"
    """

    output = ''
    try:
        # Compile the regular expression with case-insensitive matching
        output = re.compile(patt, re.IGNORECASE)

        # Perform the substitution
        output = output.sub(repl, str(subj)).strip()
    except:
        logging.error(traceback.format_exc())

    return output



def preg_match(patt: str, subj: str):
    """
    Checks if a given pattern exists in a string and returns the matched string, or False if no match is found.

    Args:
        patt (str): The regular expression pattern to search for.
        subj (str): The string to search the pattern in.

    Returns:
        str or bool: The matched string if found, or False if no match is found.

    # Example usage
    text = "Hello, World!"
    match = preg_match(patt="World", subj=text)
    print(match)  # Output: "World"
    """

    try:
        # Perform the regex search with case-insensitive matching
        output = re.search(patt, str(subj), re.IGNORECASE)
        if output and output.group(0):
            return output.group(0)  # Return the matched string
    except:
        logging.error(traceback.format_exc())

    return False  # Return False if no match is found or an error occurs



def preg_split(patt: str, subj: str):
    """
    Splits a string into a list of substrings based on a regular expression pattern.

    Args:
        patt (str): The regular expression pattern to split the string by.
        subj (str): The string to split.

    Returns:
        list: A list of substrings split by the given pattern.

    # Example usage
    text = "apple,banana,orange"
    result = preg_split(patt=",", subj=text)
    print(result)  # Output: ['apple', 'banana', 'orange']
    """

    output = []
    try:
        # Compile the regular expression and split the string
        output = re.compile(patt, re.IGNORECASE).split(str(subj))
    except:
        logging.error(traceback.format_exc())

    return output



def convert_html_to_plain_text(html: str, ignore_links: bool = True, ignore_images: bool = True, ignore_anchors: bool = True) -> str:
    """
    Converts an HTML string into plain text, with options to ignore links, images, and anchors.

    Args:
        html (str): The HTML string to convert to plain text.
        ignore_links (bool): Whether to ignore links in the HTML content. Default is True.
        ignore_images (bool): Whether to ignore images in the HTML content. Default is True.
        ignore_anchors (bool): Whether to ignore anchor tags in the HTML content. Default is True.

    Returns:
        str: The plain text representation of the HTML content.

    # Example usage
    html_content = "<html><body><h1>Hello, World!</h1><a href='#'>Link</a></body></html>"
    plain_text = convert_html_to_plain_text(html_content, ignore_links=True, ignore_images=True, ignore_anchors=True)
    print(plain_text)  # Output: "Hello, World!"
    """

    md = ''
    try:
        # Initialize HTML2Text parser
        parser = html2text.HTML2Text()
        parser.ignore_links = ignore_links    # Set based on parameter
        parser.ignore_images = ignore_images  # Set based on parameter
        parser.ignore_anchors = ignore_anchors # Set based on parameter
        parser.body_width = 0                  # No wrapping for lines

        # Convert HTML to plain text
        md = parser.handle(str(html))

        # Clean up leading and trailing newlines
        md = preg_repace(patt='^\n+|\n+$', repl=' ', subj=md).strip()

    except:
        logging.error(traceback.format_exc())

    return md



def verify_is_person(name: str) -> bool:
    """
    Verifies whether the given name is recognized as a person using SpaCy's named entity recognition.

    Args:
        name (str): The name to be verified.

    Returns:
        bool: True if the name is recognized as a person, False otherwise.

    # Example usage
    name = "John Doe"
    result = verify_is_person(name)
    print(result)  # Output: True

    # Ref:
    pip install spacy
    python -m spacy download en_core_web_sm
    """

    try:
        # Load the SpaCy model for named entity recognition
        nlp = spacy.load("en_core_web_sm")

        # Process the input name with SpaCy
        doc = nlp(name.lower())

        # Check if any recognized entity is labeled as a person
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return True
    except:
        logging.error(traceback.format_exc())

    return False



def convert_letters_to_numbers(text: str) -> str:
    """
    Converts letters in a string to their corresponding positions in the alphabet (a=1, b=2, ..., z=26).
    Non-alphabetic characters are left unchanged.

    Args:
        text (str): The input string to convert.

    Returns:
        str: A new string where alphabetic characters are replaced by their corresponding number, and other characters remain unchanged.

    # Example usage
    text = "abc 123"
    result = convert_letters_to_numbers(text)
    print(result)  # Output: "1 2 3 123"
    """

    return ''.join([(str(ord(x.lower()) - 96) if x.isalpha() else x) for x in text])



def format_size_in_bytes(size_bytes: int) -> str:
    """
    Converts a size in bytes to a human-readable format (e.g., KB, MB, GB).

    Args:
        size_bytes (int): The size in bytes.

    Returns:
        str: The size formatted as a human-readable string with an appropriate unit (e.g., "1.23 MB").

    # Example usage
    result = format_size_in_bytes(size_bytes=1048576)
    print(result)  # Output: "1.0 MB"
    """

    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return f"{s} {size_name[i]}"



def extract_urls_from_text(text: str) -> list:
    """
    Extracts unique URLs from a given text string.

    Args:
        text (str): The input text from which to extract URLs.

    Returns:
        list: A list of unique URLs found in the input text. Returns an empty list if no URLs are found or if an error occurs.

    # Example usage
    text = "Check out https://example.com and http://test.com!"
    result = extract_urls_from_text(text)
    print(result)  # Output: ['https://example.com', 'http://test.com']
    """

    urls = []
    try:
        if text:
            # extractor = URLExtract()
            # urls_pre = extractor.find_urls(text)
            re_equ = r"http[s]?://\S+"
            urls_pre = re.findall(re_equ, text)
            urls_set = set()
            urls = [url for url in urls_pre if url not in urls_set and not urls_set.add(url)]
    except:
        logging.error(traceback.format_exc())

    return urls



def extract_emails_from_text(text: str) -> list:
    """
    Extracts unique email addresses from a given text string.

    Args:
        text (str): The input text from which to extract email addresses.

    Returns:
        list: A list of unique email addresses found in the input text. Returns an empty list if no emails are found or if an error occurs.

    # Example usage
    text = "Contact us at support@example.com or info@domain.com!"
    result = extract_emails_from_text(text)
    print(result)  # Output: ['support@example.com', 'info@domain.com']
    """

    emails = []
    try:
        if text:
            # Regular expression to match email addresses
            emails_pre = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            # Remove duplicates
            emails_set = set()
            emails = [email for email in emails_pre if email not in emails_set and not emails_set.add(email)]
    except:
        logging.error(traceback.format_exc())

    return emails



def extract_phones_from_text(text: str) -> list:
    """
    Extracts unique phone numbers from a given text string.

    Args:
        text (str): The input text from which to extract phone numbers.

    Returns:
        list: A list of unique phone numbers in national format. Returns an empty list if no phone numbers are found or if an error occurs.

    # Example usage
    text = "Call us at (555) 123-4567 or 555-987-6543!"
    result = extract_phones_from_text(text)
    print(result)  # Output: ['(555) 123-4567', '555-987-6543']
    """

    phones = []
    try:
        if text:
            # Use regex to find possible phone number patterns
            phone_pattern = r'(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})'
            matches = re.findall(phone_pattern, text)

            # For each match, use phonenumbers to validate and format
            phones_pre = []
            for match in matches:
                try:
                    # Clean the phone number and parse it
                    phone_number = phonenumbers.parse(match, "US")
                    formatted_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
                    phones_pre.append(formatted_number)
                except:
                    logging.error(traceback.format_exc())

            # Remove duplicates
            phones_set = set()
            phones = [phone for phone in phones_pre if phone not in phones_set and not phones_set.add(phone)]
    except:
        logging.error(traceback.format_exc())

    return phones



def format_phone_number(phone_number: str) -> str:
    """
    Formats a phone number to the national format for the US.

    Args:
        phone_number (str): The phone number to be formatted.

    Returns:
        str: The phone number in national format if valid, or the original input if not valid.

    # Example usage:
    phone = "5551234567"
    formatted_phone = format_phone_number(phone)
    print(formatted_phone)  # Output: (555) 123-4567
    """
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, "US")

        # Format the number in national format
        phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        logging.error(traceback.format_exc())
        return phone_number

    return phone_number



def get_text_from_image(image_path: str, path_to_tesseract: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe") -> str:
    """
    Extracts text from an image using Optical Character Recognition (OCR).

    Args:
        image_path (str): The path to the image from which to extract text.
        path_to_tesseract (str, optional): The file path to the Tesseract executable. Defaults to
                                           'C:\Program Files\Tesseract-OCR\tesseract.exe'.

    Returns:
        str: The text extracted from the image. If an error occurs, returns an empty string.

    # Example usage:
    image_path = "path_to_image.jpg"
    extracted_text = get_text_from_image(image_path)
    print(extracted_text)  # Output: Extracted text from the image
    """

    extracted_text = ''
    try:
        # Open the image using PIL
        image = Image.open(image_path)

        # Set Tesseract command path
        pytesseract.tesseract_cmd = path_to_tesseract

        # Use Tesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    except:
        logging.error(traceback.format_exc())

    return extracted_text



def parse_field(selector: str, html_content) -> str:
    """
    Extracts the value from an HTML element using an XPath selector.

    Args:
        selector (str): The XPath selector to locate the element from which to extract the value.
        html_content: The HTML content to parse (e.g., an HTML element or document).

    Returns:
        str: The extracted value from the element. Returns an empty string if no value is found or an error occurs.

    # Example usage:
    selector = "//div[@class='example-class']/text()"
    html_content = response.html  # Assuming response.html is a parsed HTML document
    print(parse_field(selector, html_content))  # Output: Extracted text or empty string
    """

    value = ''
    try:
        value = html_content.xpath(f'normalize-space({selector})').get()
    except:
        logging.error(traceback.format_exc())
        value = ''

    return value


class NameSwapper:
    """
    A class to handle splitting and swapping first, middle, and last names.

    Methods:
        split_name(key, name_parts): Returns the part of the name from the given index.
        split_and_swap_names(first_name, second_name): Splits the first and second names into parts,
                                                      and swaps them if necessary based on common names.


    # Example usage:
    first_name = "John Michael Doe"
    second_name = "John M. Doe"
    name_swapper = NameSwapper()
    modified_first_name, modified_second_name = name_swapper.split_and_swap_names(first_name, second_name)
    print(modified_first_name)  # Output: 'John M. Doe'
    print(modified_second_name)  # Output: 'John M. Doe'
    """

    def __init__(self):
        pass

    def split_name(self, key, name_parts):
        """
        Returns the name part at the specified index.

        Args:
            key (int): The index of the name part to return.
            name_parts (list): A list containing the split name parts.

        Returns:
            str: The name part at the specified index, or an empty string if the index is out of bounds.

        Example:
            name_parts = ['john', 'doe']
            split_name(0, name_parts)  # Returns 'john'
            split_name(1, name_parts)  # Returns 'doe'
        """
        try:
            return name_parts[key]
        except IndexError:
            return ''

    def split_and_swap_names(self, first_name, second_name):
        """
        Splits the first and second names into their respective parts (first, middle, last names),
        and swaps them if they share a common first name.

        Args:
            first_name (str): The first full name.
            second_name (str): The second full name.

        Returns:
            tuple: A tuple containing the modified first and second names after swapping parts.

        Example:
            first_name = "John Michael Doe"
            second_name = "John M. Doe"
            split_and_swap_names(first_name, second_name)
            # Returns ('John M. Doe', 'John M. Doe')
        """
        fname1 = fname2 = mname1 = mname2 = lname1 = lname2 = ''

        try:
            if first_name and second_name:
                first_name_parts = first_name.lower().split()
                second_name_parts = second_name.lower().split()

                first_name_0 = self.split_name(0, first_name_parts)
                first_name_1 = self.split_name(1, first_name_parts)
                first_name_2 = self.split_name(2, first_name_parts)

                second_name_0 = self.split_name(0, second_name_parts)
                second_name_1 = self.split_name(1, second_name_parts)
                second_name_2 = self.split_name(2, second_name_parts)

                # Check if first name parts match and adjust accordingly
                if first_name_0 == second_name_0:
                    lname1 = lname2 = first_name_0
                    fname1, mname1 = self._assign_names(first_name_1, first_name_2)
                    fname2, mname2 = self._assign_names(second_name_1, second_name_2)

                elif first_name_0 == second_name_1:
                    lname1 = lname2 = first_name_0
                    fname1, mname1 = self._assign_names(first_name_1, first_name_2)
                    fname2, mname2 = self._assign_names(second_name_0, second_name_2)

                elif first_name_0 == second_name_2:
                    lname1 = lname2 = first_name_0
                    fname1, mname1 = self._assign_names(first_name_1, first_name_2)
                    fname2, mname2 = self._assign_names(second_name_0, second_name_1)

                # Rebuild names in proper format
                first_name = self._format_name(fname1, mname1, lname1)
                second_name = self._format_name(fname2, mname2, lname2)

        except Exception:
            logging.error(traceback.format_exc())

        return first_name, second_name

    def _assign_names(self, part1, part2):
        """
        Assigns first name and middle name based on the available parts.

        Args:
            part1 (str): First name or middle name.
            part2 (str): The other name part (either first or middle).

        Returns:
            tuple: First name and middle name after assignment.

        Example:
            _assign_names('john', 'michael')  # Returns ('john', 'michael')
            _assign_names('john', '')  # Returns ('john', '')
        """
        fname = mname = ''
        if len(part1) == 1:
            mname = part1
            fname = part2
        elif len(part2) == 1:
            mname = part2
            fname = part1
        else:
            fname = part1
        return fname, mname

    def _format_name(self, fname, mname, lname):
        """
        Formats the name with first, middle, and last names.

        Args:
            fname (str): First name.
            mname (str): Middle name.
            lname (str): Last name.

        Returns:
            str: A formatted name with first, middle, and last names.

        Example:
            _format_name('John', 'Michael', 'Doe')  # Returns 'John Michael Doe'
            _format_name('John', '', 'Doe')  # Returns 'John Doe'
        """
        return f'{fname} {mname} {lname}'.replace('  ', ' ').strip().title()



def decode_cloudflare_encoded_email(fp):
    """
    Decodes a Cloudflare encoded email string.

    Args:
        fp (str): The encoded email string in hexadecimal format, typically encoded by Cloudflare.

    Returns:
        str: The decoded email address or None if decoding fails.

    Example:
        encoded_email = "d4d8d4e4e5d8d8e5d9d7d9e6d0"  # encoded email address
        decoded_email = decode_cloudflare_encoded_email(encoded_email)
        print(decoded_email)  # Output: 'example@example.com'
    """
    try:
        r = int(fp[:2], 16)  # Get the first two hex digits as a number
        # Decode the rest of the hex string
        email = ''.join([chr(int(fp[i:i + 2], 16) ^ r) for i in range(2, len(fp), 2)])
        return email
    except:
        logging.error(traceback.format_exc())



def parse_address_from_input(address: str) -> Dict[str, str]:
    """
    Parses a given address and returns the formatted address, street names, city, state, and zip code in a dictionary.

    Args:
        address (str): The address to be searched using Google Maps.

    Returns:
        dict: A dictionary containing the address, street1, street2, city, state, and zip code.

    Example:
        address = "2964 Cottage Grove Ct #170, Orlando, FL 32822"
        result = parse_address_from_input(address=address)
        print(result) #{'address': '2964 Cottage Grove Ct, # 170, Orlando, FL 32822', 'street1': '2964 Cottage Grove Ct', 'street2': '# 170', 'city': 'Orlando', 'state': 'FL', 'zip': '32822'}
    """

    result = {
        'address': '',
        'street1': '',
        'street2': '',
        'city': '',
        'state': '',
        'zip': ''
    }
    try:
        try:
            data, address_type = usaddress.tag(address)
            result['street1'] = f"{data.get('AddressNumber', '')} {data.get('StreetName', '')} {data.get('StreetNamePostType', '')} {data.get('StreetNamePostDirectional', '')}".strip()
            result['street2'] = f"{data.get('OccupancyType', '')} {data.get('OccupancyIdentifier', '')}".strip()
            result['city'] = data.get('PlaceName', '')
            result['state'] = data.get('StateName', '')
            result['zip'] = data.get('ZipCode', '')
        except:
            logging.error("Error parsing address with usaddress")

        # Fallback if street1 and street2 are empty
        if not result['street1'] and not result['street2']:
            tab_location = address.split(',')
            if len(tab_location) == 3:
                try:
                    result['street1'] = tab_location[0].strip()
                    result['city'] = tab_location[1].strip()
                    result['state'] = tab_location[2].strip().split()[0].strip()
                    result['zip'] = tab_location[2].strip().split()[1].strip()
                except:
                    logging.error("Error parsing fallback address format")

            elif len(tab_location) == 4:
                try:
                    result['street1'] = tab_location[0].strip()
                    result['street2'] = tab_location[1].strip()
                    result['city'] = tab_location[2].strip()
                    result['state'] = tab_location[3].strip().split()[0].strip()
                    result['zip'] = tab_location[3].strip().split()[1].strip()
                except:
                    logging.error("Error parsing fallback address format")

        # Build the formatted address, handling empty values
        formatted_address = ''
        if result.get('street1'):
            formatted_address += result['street1']
        if result.get('street2'):
            formatted_address += f", {result['street2']}"
        if result.get('city'):
            formatted_address += f", {result['city']}"
        if result.get('state'):
            formatted_address += f", {result['state']}"
        if result.get('zip'):
            formatted_address += f" {result['zip']}"

        # Join the address parts with commas and spaces
        result['address'] = formatted_address

    except:
        logging.error(traceback.format_exc())

    return result



def parse_address_with_google_map(address: str, google_map_key: str, proxies: List[str], use_proxy: bool = False) -> Dict[str, str]:
    """
    Parses a given address using the Google Maps API and returns the formatted address, street names,
    city, state, and zip code in a dictionary.

    Args:
        address (str): The address to be searched using Google Maps.
        google_map_key (str): A Google Maps API key to be used for the request.
        proxies (list): A list of proxies to be used in the request.
        use_proxy (bool): If True, will use the provided proxies for the API request. Defaults to False.

    Returns:
        dict: A dictionary containing the address, street1, street2, city, state, and zip code.

    Example:
        address = "2964 Cottage Grove Ct #170, Orlando, FL 32822"
        proxies = ['your_proxy_here']
        google_map_key = 'YOUR_GOOGLE_MAPS_API_KEY'
        result = parse_address_with_google_map(address=address, google_map_key=google_map_key, proxies=proxies, use_proxy=True)
        print(result) #{'address': '2964 Cottage Grove Ct, # 170, Orlando, FL 32822', 'street1': '2964 Cottage Grove Ct', 'street2': '# 170', 'city': 'Orlando', 'state': 'FL', 'zip': '32822', 'google_address': '2964 Cottage Grove Ct #170, Orlando, FL 32822'}
    """

    result = {
        'address': '',
        'street1': '',
        'street2': '',
        'city': '',
        'state': '',
        'zip': ''
    }
    try:
        base_link = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}&language=en'
        index_url = base_link.format(quote(address.encode('utf8')), quote(google_map_key.encode('utf8')))

        try:
            proxy = {}
            if use_proxy:
                proxy = random.choice(proxies)
                proxy = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

            response = requests.get(index_url, proxies=proxy)
            results1 = response.json()

            if results1.get('results'):
                formatted_address = results1['results'][0]['formatted_address'].replace(', USA', '').strip()
                result = parse_address_from_input(address=formatted_address)
                result['google_address'] = formatted_address

        except:
            logging.error(traceback.format_exc())

    except:
        logging.error(traceback.format_exc())

    return result



def extract_domain(url: str, remove_www: bool = True, with_scheme: bool = False) -> str:
    """
    Extracts the domain from a URL.

    Args:
        url (str): The URL from which the domain will be extracted.
        remove_www (bool): If True, removes the 'www.' prefix from the domain. Default is True.
        with_scheme (bool): If True, includes the scheme (e.g., 'http://') in the returned domain. Default is False.

    Returns:
        str: The extracted domain.

    Example:
        url = "https://www.example.com/path/to/page"
        result = extract_domain(url)
        print(result)  # Output: "example.com"
    """

    # Parse the URL
    parsed_url = urlparse(url)

    # If the scheme is not present in the URL, add a default scheme (http://)
    if not parsed_url.scheme:
        url = "http://" + url
        parsed_url = urlparse(url)

    domain = parsed_url.netloc

    # Include the scheme (e.g., 'http://') if requested
    if with_scheme:
        domain = parsed_url.scheme + "://" + domain

    # Remove the 'www.' prefix if requested
    if remove_www:
        domain = domain.replace('www.', '').strip()

    return domain



def number_to_excel_column(num: int) -> str:
    """
    Converts a given column number to its corresponding Excel column label.

    Args:
        num (int): The column number to be converted (e.g., 1, 2, 26, 27, ...).

    Returns:
        str: The corresponding Excel column label (e.g., 'A', 'B', 'Z', 'AA', ...).

    Example:
        num = 28
        result = number_to_excel_column(num)
        print(result)  # Output: "AB"
    """
    if num <= 26:
        return chr(64 + num)
    else:
        first_char = chr(64 + (num - 1) // 26)
        second_char = chr(64 + (num - 1) % 26 + 1)
        return f"{first_char}{second_char}"



def get_first_node(json_data: List[Dict]) -> Union[str, None]:
    """
    Extracts the first value found in the JSON-like structure (list of dictionaries).
    It assumes the input is a list of dictionaries and returns the first value it encounters.

    Args:
        json_data (List[Dict]): The list of dictionaries to search through.

    Returns:
        Union[str, None]: The first value found in the JSON structure, or None if no values are found.

    Example:
    result = get_first_node(json_data)
    """

    result = None
    if json_data:
        try:
            result = list(json_data[0].values())[0]
            # for i in json_data:
            #     for node in i.values():
            #         result = node
            #         break
            #     break
        except:
            logging.error(traceback.format_exc())

    return result



def extract_nodes_under_key(json_data: Union[Dict, List], target_key: str) -> List[Dict[str, str]]:
    """
    Recursively searches through a JSON-like structure (dict or list) to extract all nodes under the specified key.
    It returns a list of dictionaries containing the paths and values of the key.

    Args:
        json_data (dict or list): The JSON object to search through. It can be a dictionary, list, or a combination of both.
        target_key (str): The key for which you want to extract values and their respective paths.

    Returns:
        list: A list of dictionaries, each containing the path (as a string) and the value of the target key.
              The path is constructed as a forward-slash-separated string.

    Example:
        json_data = {
            "user": {
                "name": "John",
                "address": {
                    "city": "New York",
                    "zip": "10001"
                },
                "contacts": [
                    {"type": "email", "value": "john.doe@example.com"},
                    {"type": "phone", "value": "123-456-7890"}
                ]
            },
            "company": {
                "name": "ExampleCorp",
                "contacts": [
                    {"type": "email", "value": "contact@company.com"},
                    {"type": "phone", "value": "987-654-3210"}
                ]
            }
        }

        target_key = "contacts"
        nodes_data = extract_nodes_under_key(json_data, target_key)
        print(nodes_data)
        result = get_first_node(nodes_data)
        print(result)

        # Output:
        # [{'user/contacts/0/type': 'email'}, {'user/contacts/0/value': 'john.doe@example.com'},
        #  {'user/contacts/1/type': 'phone'}, {'user/contacts/1/value': '123-456-7890'},
        #  {'company/contacts/0/type': 'email'}, {'company/contacts/0/value': 'contact@company.com'},
        #  {'company/contacts/1/type': 'phone'}, {'company/contacts/1/value': '987-654-3210'}]
    """

    nodes = []
    def traverse(node, path=[]):
        """Recursively traverses the JSON structure."""
        if isinstance(node, dict):
            for key, value in node.items():
                new_path = path + [key]
                if key == target_key:
                    nodes.append({"/".join(new_path): value})
                traverse(value, new_path)
        elif isinstance(node, list):
            for i, item in enumerate(node):
                new_path = path + [str(i)]
                traverse(item, new_path)

    traverse(json_data)
    return nodes



def convert_to_full_number(value_str: str):
    """
    Convert a string representation of a number with a suffix ('K', 'M', 'B') to its full numerical form.
    - 'K' represents thousands
    - 'M' represents millions
    - 'B' represents billions

    Args:
        value_str (str): The string containing the number with an optional suffix ('K', 'M', or 'B').

    Returns:
        int: The converted full numerical value.

    Example:
    result1 = convert_to_full_number("2.90K")
    print(result1)  # Output: 2900
    """

    try:
        # Remove commas if present (in case of thousands separators)
        value_str = value_str.replace(',', '')

        # Check if the string ends with a suffix and perform the conversion accordingly
        if value_str.endswith('K'):
            return int(float(value_str[:-1]) * 1_000)  # K for thousand
        elif value_str.endswith('M'):
            return int(float(value_str[:-1]) * 1_000_000)  # M for million
        elif value_str.endswith('B'):
            return int(float(value_str[:-1]) * 1_000_000_000)  # B for billion
        else:
            return int(float(value_str))  # No suffix, just return the integer value

    except:
        logging.error(traceback.format_exc())
        return value_str



def similarity_calculate(string1: str, string2: str) -> float:
    """
    Calculate the similarity between two strings based on their Levenshtein distance.
    The similarity is computed as 1 - (Levenshtein distance / max(length of string1, length of string2)).

    Args:
        string1 (str): The first string to compare.
        string2 (str): The second string to compare.

    Returns:
        float: A similarity score between 0 and 1, rounded to two decimal places.

    Example:
        similarity = similarity_calculate("hello", "helo")
        print(similarity)  # Output: 0.8
    """

    # Convert both strings to lowercase
    string1 = str(string1).lower()
    string2 = str(string2).lower()

    # Calculate the Levenshtein distance
    try:
        levenshtein_dist = levenshtein_distance(string1, string2)
        # Calculate similarity as 1 - (Levenshtein distance / max length of the two strings)
        similarity = 1 - levenshtein_dist / max(len(string1), len(string2))
        return round(similarity, 2)
    except:
        logging.error(traceback.format_exc())
        return 0.0



def replace_invalid_chars(name: str, replace_with_char: str = '_') -> str:
    """
    Replace invalid characters in a string with a specified replacement character.
    Invalid characters typically include those that are not allowed in file names
    such as: \ / : * ? " < > |

    Args:
        name (str): The string to clean by replacing invalid characters.
        replace_with_char (str): The character to replace invalid characters with (default is '_').

    Returns:
        str: The cleaned string with invalid characters replaced by the specified character.

    Example:
        cleaned_name = replace_invalid_chars('hello:world*', replace_with_char='-')
        print(cleaned_name)  # Output: hello-world-
    """

    # List of invalid characters that are not allowed in filenames
    invalid_characters = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    # Replace each invalid character with the specified replacement character
    for invalid_character in invalid_characters:
        name = name.replace(invalid_character, replace_with_char)

    # Strip any leading/trailing whitespace from the name
    return name.strip()



def search_exa(query: str, fctrequest, proxies: List[str], search_company: bool = False, num_results: int = 30) -> List[Dict[str, str]]:
    """
    Search for companies or general keywords on exa.ai and return a list of results.

    Args:
        query (str): The search query string.
        fctrequest: The request handler to execute the search query.
        proxies (List, optional): A list of proxies to use.
        search_company (bool, optional): Whether to search for companies (True) or general keywords (False). Defaults to False.
        num_results (int, optional): The number of results to retrieve. Defaults to 30.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with 'title' and 'link' for each result.

    Example:
        query_exa = 'total.com zoominfo'
        results_exa = search_exa(query=query_exa, fctrequest=self.fctrequest, proxies=self.proxies, search_company=True, num_results=30)
        print(results_exa)
    """

    results = []
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
            'baggage': 'sentry-environment=production,sentry-release=ad867f430125dd89da1afe192e45096ba362b170,sentry-public_key=3a600f26c57ebafc07ac5690da6e4199,sentry-trace_id=0535660e24c24fd4b919bd6a097e68ec,sentry-sample_rate=1,sentry-sampled=true',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://exa.ai',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        }
        logging.info(f'exa_query: {query}')

        if search_company:
            data = '{"numResults":'+str(num_results)+',"category":"company","domainFilterType":"include","type":"auto","query":"' + str(query) + '","useAutoprompt":true,"resolvedSearchType":"keyword"}'
        else:
            data = '{"numResults":'+str(num_results)+',"domainFilterType":"include","type":"auto","query":"' + str(query) + '","useAutoprompt":true,"resolvedSearchType":"keyword"}'

        index_link = 'https://exa.ai/search/api/search'
        response1 = fctrequest.request(method='POST', link=index_link, data=data, headers=headers, proxies=proxies, tries=10)
        if response1.status_code in range(200, 300):
            data = []
            try:
                results1 = response1.json()
                data = results1['results']
            except:
                ''

            if data:
                exa_title = ''
                exa_url = ''
                for result in data:
                    try:
                        exa_title = result['title']
                    except:
                        ''
                    try:
                        exa_url = result['url']
                    except:
                        ''

                    results.append({'title': exa_title, 'link': exa_url})

    except:
        logging.error(traceback.format_exc())

    return results



def search_google(query: str, fctrequest, proxies: List[str], keyword_in_title: str = '', page: int = 1) -> List[Dict[str, str]]:
    """
    Perform a Google search and extract relevant results based on the query.

    Args:
        query (str): The search query to be executed.
        fctrequest: The request handler to execute the search.
        proxies (List[str]): A list of proxies to use for the request.
        keyword_in_title (str): A keyword that should appear in the result titles (optional).
        page (int): The page number to retrieve from Google search results (default is 1).

    Returns:
        List[Dict[str, str]]: A list of dictionaries with 'title' and 'link' for each result.

    Example:
        query_google = 'intitle:"devops member" site:linkedin.com'
        results_google = search_google(query=query_google, fctrequest=self.fctrequest, proxies=self.proxies, keyword_in_title='linkedin.com')
        print(results_google)
    """

    results = []
    try:
        headers = {
            'accept': '*/*',
            'accept-language': '*/*',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        logging.info(f'Google search query: {query} | page: {page}')

        # Construct the Google search URL
        index_link = f'https://www.google.com/search?q={quote(query.encode("utf8")).lower()}&start={page * 10}'
        response = fctrequest.request(method='GET', link=index_link, headers=headers, proxies=proxies, tries=10)

        if response.status_code in range(200, 300):
            html = Selector(text=response.text)

            try:
                # Define the XPath for extracting the search results
                search_xpath = f'//a[contains(@href, "{keyword_in_title}") and h3]'

                for result in html.xpath(search_xpath):
                    google_title = result.xpath('normalize-space(./h3)').get() or ''
                    google_url = result.xpath('./@href').get() or ''

                    # Only add results if both title and URL are found
                    if google_title and google_url:
                        results.append({'title': google_title, 'link': google_url})

            except:
                logging.error(traceback.format_exc())

    except:
        logging.error(traceback.format_exc())

    return results


def get_screen_resolution() -> tuple:
    """
    Get the screen resolution of the primary monitor, accounting for high DPI scaling.

    Returns:
        tuple: A tuple containing the screen width and height in pixels.

    # Example:
        width, height = get_screen_resolution()
        print(f"Screen resolution: {width}x{height}")
    """

    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()  # Ensures proper scaling on high-DPI displays

        work_area = ctypes.wintypes.RECT()
        # 48 is the SPI_GETWORKAREA constant, used to get the work area (usable screen area excluding taskbars)
        user32.SystemParametersInfoW(48, 0, ctypes.byref(work_area), 0)

        usable_width = work_area.right - work_area.left
        usable_height = work_area.bottom - work_area.top

        return usable_width, usable_height

    except:
        logging.error(traceback.format_exc())
        return 0, 0  # Returning a default value if there is an error



def get_section_coordinates(application_number: int, max_workers: int) -> tuple:
    """
    Calculate the position and size of a section on the screen for a given application number,
    based on dividing the screen into a grid.

    Args:
        application_number (int): The 1-based index of the application.
        max_workers (int): The total number of workers (sections) to divide the screen into.

    Returns:
        tuple: A tuple containing two strings:
            - window_position: A string in the format "x,y" (the top-left corner coordinates).
            - window_size: A string in the format "width,height" (the dimensions of the section).

    Raises:
        ValueError: If application_number is not within the valid range (1 to max_workers).

    # Example:
        window_position, window_size = get_section_coordinates(application_number=2, max_workers=4)
        print(f"Window Position: {window_position}, Window Size: {window_size}")
    """

    if application_number < 1 or application_number > max_workers:
        raise ValueError(f"application_number must be between 1 and {max_workers}, inclusive.")

    # Get screen resolution
    screen_width, screen_height = get_screen_resolution()
    # logging.info(f"Screen resolution: width={screen_width}, height={screen_height}")

    # Calculate the grid dimensions
    columns = math.ceil(math.sqrt(max_workers))
    rows = math.ceil(max_workers / columns)

    # Calculate width and height of each section
    section_width = screen_width // columns
    section_height = screen_height // rows

    # Calculate the row and column for the application
    row = (application_number - 1) // columns
    col = (application_number - 1) % columns

    # Calculate the x and y position
    x = col * section_width
    y = row * section_height

    window_position = f"{x},{y}"
    window_size = f"{section_width},{section_height}"
    logging.info(f"application_number: {application_number}, window_position: {window_position}, window_size: {window_size}")

    return window_position, window_size


def kill_python_processes(exclude_pid: int):
    """
    Kill all python.exe processes except for the current running script.

    Args:
        exclude_pid (int): The PID of the current process to exclude from termination.

    Example:
        current_pid = os.getpid()
        kill_python_processes(exclude_pid=current_pid)
    """

    try:
        result = subprocess.check_output('tasklist /FI "IMAGENAME eq python.exe"', shell=True, text=True)
        lines = result.strip().split("\n")[3:]  # Skip the header lines
        for line in lines:
            parts = line.split()
            if len(parts) > 1:
                pid = int(parts[1])
                if pid != exclude_pid:
                    subprocess.call(f"TASKKILL /f /PID {pid}")
        logging.info("All Python processes except the current one have been terminated.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while fetching Python processes: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def kill_specified_processes(processes):
    """
    Kill the specified processes.

    Args:
        processes (list): A list of process names (e.g., 'chrome.exe', 'chromedriver.exe') to terminate.

    Example:
        kill_specified_processes(['chrome.exe', 'chromedriver.exe'])
    """

    for process in processes:
        try:
            logging.info(f"Attempting to stop: {process}")
            subprocess.call(f"TASKKILL /f /IM {process}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error while stopping {process}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while stopping {process}: {e}")


def kill_processes(processes=None, kill_python=False):
    """
    Kill specified processes and optionally terminate all python processes except the current one.

    Args:
        processes (list): A list of process names to terminate (default is Chrome-related processes).
        kill_python (bool): If True, all Python processes except the current one will be terminated.

    Example:
        # To kill default processes and Python processes:
        kill_processes(kill_python=True)

        # To kill specific processes (e.g., 'firefox.exe' and 'chromedriver.exe'):
        kill_processes(processes=['firefox.exe', 'chromedriver.exe'], kill_python=False)
    """

    if processes is None:
        processes = ['chrome.exe', 'chromedriver.exe', 'uc_driver.exe']

    if kill_python:
        current_pid = os.getpid()
        kill_python_processes(exclude_pid=current_pid)

    kill_specified_processes(processes)



def delete_browser_data():
    """
    Deletes the browser data folder located at a specific path relative to the script's location.

    This function checks if the folder exists and is a directory, and if so, deletes it using `shutil.rmtree`.

    Example:
        delete_browser_data()  # Deletes the browser data folder if it exists
    """
    try:
        path_browser_data = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'requests', 'browser_data')
        logging.info(f'Path to browser data: {path_browser_data}')

        if os.path.exists(path_browser_data) and os.path.isdir(path_browser_data):
            shutil.rmtree(path_browser_data)
            logging.warning(f'Successfully deleted browser data at {path_browser_data}')
        else:
            logging.warning(f'Browser data path does not exist or is not a directory: {path_browser_data}')

    except Exception as e:
        logging.error(f"Error deleting browser data: {e}")
        logging.error("Traceback:", exc_info=True)



def split_total_items_to_ranges(total_items: int, max_workers: int) -> list:
    """
    Divide a total range into chunks and return the start and end values for all chunks.

    Args:
        total_items (int): The total number of items to divide into chunks.
        max_workers (int): The total number of chunks.

    Returns:
        list: A list of lists, each containing the start and end values for each chunk.
              If any of the inputs are invalid, prints an error and returns None.

    Example:
    ranges = chunk_total_items_to_ranges(total_items=52142, max_workers=4)
    print(f"ranges: {ranges}")
    # Output: ranges: [[1, 13036], [13037, 26072], [26073, 39108], [39109, 52142]]
    """

    if max_workers <= 0 or total_items <= 0:
        print("Both max_workers and total_items must be greater than 0.")
        return None

    # Split the total_items into 'max_workers' chunks
    ranges = list(np.array_split(range(total_items), max_workers))

    chunk_ranges = []
    for chunk in ranges:
        start = chunk[0] + 1
        end = chunk[-1] + 2
        chunk_ranges.append([int(start), int(end)])

    return chunk_ranges



def split_list_into_chunks(lst: list, max_workers: int) -> iter:
    """
    Splits a list into chunks based on the number of workers.

    Args:
        max_workers (int): The number of chunks to split the list into. Must be greater than 0.
        lst (list): The list (e.g., list) to be split into chunks.

    Returns:
        iter: A generator that yields each chunk as a list.

    # Example usage
    lst = [1, 2, 3, 4, 5, 6, 7, 8]
    max_workers = 3

    chunks = split_list_into_chunks(lst, max_workers)
    for chunk in chunks:
        print(chunk)

    # Output:
    # [1, 2, 3]
    # [4, 5, 6]
    # [7, 8]
    """

    if max_workers > 0:
        return (list(x) for x in np.array_split(lst, max_workers))



def split_list_into_sized_chunks(lst: list, chunk_size: int) -> iter:
    """
    Splits a list into sized chunks based on specified size.

    Args:
        lst (list): The list to be split into chunks.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        iter: A generator that yields chunks of the specified size.

    # Example usage
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    chunk_size = 3

    chunks = split_list_into_sized_chunks(lst, chunk_size)
    for chunk in chunks:
        print(chunk)

    # Output:
    # [1, 2, 3]
    # [4, 5, 6]
    # [7, 8, 9]

    # Ref:
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks

    """

    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]



def split_range_to_chunks(range_bounds, max_workers):
    """
    Splits a range_bounds into chunks and returns all chunks.

    Args:
        range_bounds (list): A list containing the start and end of the range (e.g., [1, 5000]).
        max_workers (int): The number of chunks to split the range_bounds into.

    Returns:
        list: A list of chunks, where each chunk is a list of range_bounds.

    Example Usage:
        range_bounds = [1, 5000]  # Start and end of the range
        max_workers = 5

        chunks = split_range_to_chunks(range_bounds, max_workers)
        print(chunks)  # Output: [[1, 2, ...], [...], ..., [4999, 5000]]
    """

    # Generate the range of range_bounds from start to end
    start, end = range_bounds[0], range_bounds[1]
    full_range = list(range(start, end + 1))

    # Split the range into chunks
    chunks = list(np.array_split(full_range, max_workers))

    # Return all chunks as a list of lists
    return [chunk.tolist() for chunk in chunks]



def move_mouse_randomly(window_position, window_size, duration=0.5):
    """
    Moves the mouse to a random point within a given window area.

    Args:
        window_position (str): Top-left corner of the window as a string (e.g., "0, 0").
        window_size (str): Dimensions of the window as a string (e.g., "960, 516").
        duration (float): Time in seconds for the mouse to move to the target position.

    Example Usage:
        window_position = '960,1020'
        window_size = '960,0'
        move_mouse_randomly(window_position, window_size, duration=0.2)
    """

    # Parse the position and size strings
    window_x, window_y = map(int, window_position.split(","))
    window_width, window_height = map(int, window_size.split(","))

    # Generate random coordinates within the window
    random_x = random.randint(0, window_width - 1)
    random_y = random.randint(0, window_height - 1)

    # Calculate the absolute position on the screen
    absolute_x = window_x + random_x
    absolute_y = window_y + random_y

    # Move the mouse
    mouse.move(absolute_x, absolute_y, duration=duration)
    logging.info(f"Mouse moved to random point: ({absolute_x}, {absolute_y})")