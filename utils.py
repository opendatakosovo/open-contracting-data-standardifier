# -*- coding: utf-8 -*-
from datetime import datetime

budget_types = {
    '1': {'en': 'Municipal Revenue', 'sq': 'Të hyrat vetanake'},
    '2': {'en': 'Kosovo Budget', 'sq': 'Buxheti i Konsoliduar i Kosovës'},
    '3': {'en': 'Donation', 'sq': 'Donacion'}
}

procurement_types = {
    '1': {'en': 'supply', 'sq': 'Furnizim'},
    '2': {'en': 'services', 'sq': 'Sherbime'},
    '3': {'en': 'counseling services', 'sq': 'Sherbime Keshillimi'},
    '4': {'en': 'design competition', 'sq': 'Konkurs projektimi'},
    '5': {'en': 'work', 'sq': 'Punë'},
    '6': {'en': 'work concession', 'sq': 'Punë me koncesion'},
    '7': {'en': 'immovable property', 'sq': 'Pronë e palujtshme'}
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
        transformation_log += ' --> 0'
        print transformation_log + '. Unable to clean price!'
        return 0  # FIXME: Is this what we want?


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


def create_buyer_data_dict(index, row, date_format):
    data_dict = {
        'report_date': convert_to_ocds_date_format(index, row[0].strip(), date_format),
        'report_fiscal_year': int(row[1].strip()),
        'buyer_name': row[2].strip(),
        'buyer_type': row[3].strip(),
        'budget_code': row[4].strip(),
        'buyer_address': row[5].strip(),
        'buyer_postal_code': row[6].strip(),
        'contact_telephone': row[7].strip(),
        'contact_name': row[8].strip(),
        'contact_email': row[9].strip(),
        'contact_url': row[10].strip()
    }

    return data_dict


def create_data_dict(index, row, date_format, lang='sq'):
    data_dict = {
        'budget_type': budget_types.get(row[0].strip(), empty_val)[lang],
        'procurement_serial_number': row[1].strip(),
        'procurement_type': procurement_types.get(row[2].strip(), empty_val)[lang],
        'procurement_value_size': procurement_value_sizes.get(row[3].strip(), empty_val)[lang],
        'procurement_procedure': procurement_procedures.get(row[4].strip(), empty_val)[lang],
        'classification': row[5].strip(),
        'activity_title': row[6].strip(),
        'procurement_initiation_date': convert_to_ocds_date_format(index, row[7].strip(), date_format),
        'contract_notice_publication_date': convert_to_ocds_date_format(index, row[8].strip(), date_format),
        'contract_award_notice_publication_date': convert_to_ocds_date_format(index, row[9].strip(), date_format),
        'contract_signing_or_cancel_date': convert_to_ocds_date_format(index, row[10].strip(), date_format),
        'contract_length': row[11].strip(),
        'contract_conclusion_date': convert_to_ocds_date_format(index, row[12].strip(), date_format),
        'estimated_contract_value': clean_price_value(index, row[13].strip()),
        'contract_price': clean_price_value(index, row[14].strip()),
        'contract_annex_price': clean_price_value(index, row[15].strip()),
        'deduction_from_contract': clean_price_value(index, row[16].strip()),
        'total_price_paid': clean_price_value(index, row[17].strip()),
        'awardee_name': row[18].strip(),
        'awardee_is_domestic': row[19].strip(),
        'total_bids_submitted': row[20].strip(),
        'total_bids_rejected_with_lower_price_than_awardee': row[21].strip(),
        'tender_application_deadline_type':
            tender_application_deadline_types.get(row[22].strip(), empty_val)[lang],
        'award_criteria': award_criteria.get(row[23].strip(), empty_val)[lang],
    }

    return data_dict
