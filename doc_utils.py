import utils
import json

ODK_OCID = 'ocds-3n5h6d'
LANG = 'sq'

PARENT_DOC = {
    'uri': '',
    'publishedDate': utils.get_now_date(),  # TODO: Is this the date of the data source publishDate or our publishDate?
    'publisher': {
        'scheme': '',
        'uid': '',
        'name': 'Open Data Kosovo',
        'uri': 'http://data.opendatakosovo.org/procurements/'
    },
    'license': 'http://opendatacommons.org/licenses/pddl/1.0/',
    'publicationPolicy': 'https://github.com/open-contracting/sample-data/',
    'releases': []
}


def create_buyer(data_dict):
    buyer = {
        'identifier': {
            'scheme': '',
            'id': '',
            'legalName': data_dict['buyer_name'],
            'uri': data_dict['contact_url']
        },
        'name': data_dict['buyer_name'],
        'address': {
            'streetAddress': data_dict['buyer_address'],
            'locality': 'Gjilan',  # FIXME: Don't hardcode this.
            'region': 'Gjilan',  # FIXME: Don't hardcode this.
            'postalCode': data_dict['buyer_postal_code'],
            'countryName': 'Kosovo'
        },
        'contactPoint': {
            'name': data_dict['buyer_name'],
            'email': data_dict['contact_email'],
            'telephone': data_dict['contact_telephone'],
            'faxNumber': '',
            'url': data_dict['contact_url']
        }
    }

    return buyer


def _create_base_release(step):
    release = {
        'language': 'sq',
        'ocid': ODK_OCID + '-000-00001',  # FIXME: Figure out proper way of generating an id.
        'id': ODK_OCID + '-000-00001-05-' + step,
        'date': utils.get_now_date(),  # FIXME: What should go here?
        'tag': [step],
        'initiationType': 'tender',
    }

    return release


def create_release_for_contract(buyer):
    release = _create_base_release('contract')

    release['buyer'] = buyer
    release['awards'] = []
    release['contracts'] = []

    return release


def create_release_for_planning(buyer):
    release = _create_base_release('planning')

    release['buyer'] = buyer
    release['planning'] = {}
    release['tender'] = {}

    return release


def create_supplier(data_dict):
    supplier = {
        'identifier': {
            'scheme': '',
            'id': '',
            'legalName': data_dict['awardee_name']
        },
        'name': data_dict['awardee_name']
    }

    return supplier


def create_award(data_dict, index):
    award = {
        'id': ODK_OCID + '-000-00001-award-' + str(index),
        'title': data_dict['activity_title'],
        'description': data_dict['activity_title'],
        'status': 'active',  # FIXME: That is the value for completed award?
        'date': data_dict['contract_award_notice_publication_date'],
        'value': {
            'amount': data_dict['total_price_paid'],
            'currency': 'EUR'
        },
        'suppliers': [],
        'contractPeriod': {
            'endDate': data_dict['contract_conclusion_date']
        }
    }

    return award


def create_planning(data_dict):
    planning = {
        'budget': {
            'source': '',  # TODO: Open Spending Link
            'id': '',
            'description': data_dict['activity_title'],
            'amount': {
                'amount': data_dict['estimated_contract_value'],
                'currency': 'EUR'
            },
            'project': data_dict['activity_title'],
            'projectID': data_dict['procurement_serial_number'],
            'uri': ''
        }
    }

    return planning

def create_tender(data_dict):
    tender = {
        'id':'',
        'title': data_dict['activity_title'],
        'description': data_dict['activity_title'],
        'value': data_dict['procurement_value_size'],
        'award_criteria': data_dict['award_criteria'],
        'numberOfTenderers': data_dict['total_bids_submitted'], 

def create_contract(data_dict, index):
    contract = {
        'id': ODK_OCID + '-000-00001-contract-' + str(index),  # FIXME: Figure out proper way of generating an id.
        'awardID': ODK_OCID + '-000-00001-award-' + str(index),  # FIXME: Figure out proper way of generating an id.
        'title': data_dict['activity_title'],
        'description': data_dict['activity_title'],
        'status': 'active',  # FIXME: Figure out what to put here.
        'period': {
            'endDate': data_dict['contract_conclusion_date'],
        },
        'value': {
            'amount': data_dict['contract_price'],
            'currency': "EUR"
        },
        'dateSigned': data_dict['contract_signing_or_cancel_date']
    }

    return contract


def create_ocds_planning_doc(uri):
    PARENT_DOC['uri'] = uri

    return PARENT_DOC


def create_ocds_contract_doc(uri):
    PARENT_DOC['uri'] = uri

    return PARENT_DOC


def _write_doc(file_path, ocds_doc):
    # Write document into JSON file
    json_str = json.dumps(ocds_doc, indent=4, sort_keys=True)

    with open(file_path, 'w') as json_file:
        json_file.write(json_str)


def write_contract(ocds_contract, index):
    file_path = 'output/gjilan-2015-contract-' + str(index) + '.json'
    _write_doc(file_path, ocds_contract)


def write_planning(ocds_planning, index):
    file_path = 'output/gjilan-2015-planning-' + str(index) + '.json'
    _write_doc(file_path, ocds_planning)
