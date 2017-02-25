# -*- coding: utf-8 -*-
from datetime import datetime

budget_types = {
    '1': {'en': 'Municipal Revenue', 'sq': 'Të hyrat vetanake'},
    '2': {'en': 'Kosovo Budget', 'sq': 'Buxheti i Konsoliduar i Kosovës'},
    '3': {'en': 'Donation', 'sq': 'Donacion'}
}

procurement_types = {
    '1': {'en': '', 'sq': 'Furnizim'},
    '2': {'en': '', 'sq': 'Sherbime'},
    '3': {'en': '', 'sq': 'Sherbime Keshillimi'},
    '4': {'en': '', 'sq': 'Konkurs projektimi'},
    '5': {'en': '', 'sq': 'Punë'},
    '6': {'en': '', 'sq': 'Punë me koncesion'},
    '7': {'en': '', 'sq': 'Pronë e palujtshme'}
}

procurement_value_sizes = {
    '1': {'en': 'Large', 'sq': 'Vlerë e madhe'},
    '2': {'en': 'Medium', 'sq': 'Vlerë e mesme'},
    '3': {'en': 'Small', 'sq': 'Vlerë e vogël'},
    '4': {'en': 'Minimal', 'sq': 'Vlerë  minimale'}
}

procurement_procedures = {
    '1': {'en': '', 'sq': 'Procedura e prokurimit'},
    '2': {'en': '', 'sq': 'Procedura e hapur'},
    '3': {'en': '', 'sq': 'Procedura e kufizuar'},
    '4': {'en': '', 'sq': 'Procedura e negociuar pas publikimit te njoftimit te kontrates'},
    '5': {'en': '', 'sq': 'Procedura e negociuar pa publikimit te njoftimit te kontrates'},
    '6': {'en': '', 'sq': 'Procedura e kuotimit te Çmimeve'},
    '7': {'en': '', 'sq': 'Procedura e vleres minimale'}
}

tender_application_deadline_types = {
    '1': {'en': '', 'sq': 'Afati kohor normal'},
    '2': {'en': '', 'sq': 'Afati kohor i shkurtuar'}
}

award_criteria = {
    '1': {'en': '', 'sq': 'Çmimi më i ulët'},
    '2': {'en': '', 'sq': 'Tenderi ekonomikisht më i favorshëm'}
}

empty_val = {'en': 'N/A', 'sq': 'N/A'}


def clean_price_value(index, price, verbose=False):
    # Transforms amount values given in string format into a float

    # Track the transformation, for visual integrating checking.
    transformation_log = str(index) + ' - ' + price

    # e.g.: €10, 247.39 --> 10247.39
    clean_price = price.replace('€', '').replace(',', '').strip()

    if price != clean_price:
        transformation_log += ' --> ' + clean_price

    # e.g.: 55.700.00 --> 55700.00
    period_count = clean_price.count('.')
    if period_count > 1:
        cleaner_price = ''

        num_of_periods_removed = 0
        for char in clean_price:
            if char == '.' and num_of_periods_removed != period_count - 1:
                num_of_periods_removed += 1
            else:
                cleaner_price += char

        clean_price = cleaner_price
        transformation_log += ' --> ' + clean_price

    try:
        float_price = float(clean_price)

        if verbose:
            print transformation_log
        return float_price

    except ValueError:
        transformation_log += ' --> -1'
        print transformation_log + '. Unable to clean price!'
        return -1


def convert_to_ocds_date_format(index, date, given_date_format, verbose=False):
    # e.g. "31.07.2015" --> "2015-07-31T23:59:00Z"

    try:
        datetime_object = datetime.strptime(date, given_date_format)
        datetime_object = datetime_object.replace(hour=23, minute=59)

        ocds_date_str = datetime_object.strftime('%Y-%m-%dT%I:%M:00Z')

        if verbose:
            print '%s --> %s' % (date, ocds_date_str)

        return ocds_date_str

    except ValueError:
        print '%i - Invalid date provided: %s' % (index, date)
        return ''


def get_now_date():
    ocds_date_str = datetime.now().strftime('%Y-%m-%dT%I:%M:00Z')
    return ocds_date_str
