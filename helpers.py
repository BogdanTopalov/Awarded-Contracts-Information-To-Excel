from datetime import datetime


def convert_date(date_string):
    """ Convert a date to readable format. """
    if date_string[-1] == 'Z':
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        date = datetime.strptime(date_string, date_format)
    else:
        date = datetime.fromisoformat(date_string)

    return str(date.date())


def normalize_text(text):
    """ Remove text whitespaces and return the first sentence. """
    stripped_strings = [x.strip() for x in text.split('\n')]
    joined_strings = ' '.join(stripped_strings)
    first_sentence = joined_strings.split('.')[0] + '.'

    return first_sentence


def format_address(text):
    """ Remove address whitespaces and separate address details with ',' """
    stripped_input = [x.strip() for x in text.split('\n')]
    address = ', '.join(stripped_input)

    return address
