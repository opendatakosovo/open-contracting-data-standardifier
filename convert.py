# -*- coding: utf-8 -*-
import csv
import json
import os
import glob
import utils

ODK_OCID = 'ocds-3n5h6d'
LANG = 'sq'


def process_data(buyer_data_file_path, contract_data_file_path, date_format):

    ocds_contract_doc = {
        'uri': 'http://data.opendatakosovo.org/procurements/2016/gjilan-contract.json',
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

    with open(buyer_data_file_path, 'rb') as mdf:
        buyer_data_reader = csv.reader(mdf)

        # skip header line
        next(buyer_data_reader)

        for buyer_data_row in buyer_data_reader:
            '''
            unused_data = {
                'report_date': buyer_data_row[0].strip(),
                'report_fiscal_year': int(buyer_data_row[1].strip()),
                'buyer_type': buyer_data_row[3].strip(),
                'budget_code':  buyer_data_row[4].strip(),
                'buyer_address': buyer_data_row[5].strip(),
            }
            '''

            # Buyer:
            buyer = {
                'identifier': {
                    'scheme': '',
                    'id': '',
                    'legalName': buyer_data_row[2].strip(),
                    'uri': buyer_data_row[10].strip()  # To be fetched from data source
                },
                'name': buyer_data_row[2].strip(),
                'address': {
                    'streetAddress': buyer_data_row[5].strip(),  # To be fetched from data source
                    'locality': 'Gjilan',  # FIXME: Don't hardcode this.
                    'region': 'Gjilan',  # FIXME: Don't hardcode this.
                    'postalCode': buyer_data_row[6].strip(),
                    'countryName': 'Kosovo'
                },
                'contactPoint': {
                    'name': buyer_data_row[8].strip(),
                    'email': buyer_data_row[9].strip(),
                    'telephone': buyer_data_row[7].strip(),
                    'faxNumber': "",
                    'url': buyer_data_row[10].strip()
                }
            }

            # Release:
            release = {
                'language': 'sq',
                'ocid': ODK_OCID + '-000-00001',  # FIXME: Figure out proper way of generating an id.
                'id': ODK_OCID + '-000-00001-05-contract',
                'date': utils.get_now_date(),  # FIXME: What should go here?
                'tag': ['contract'],
                'initiationType': 'tender',
                'buyer': buyer,
                'awards': [],
                'contracts': []
            }

    with open(contract_data_file_path, 'rb') as cdf:
        contract_data_reader = csv.reader(cdf)

        # skip header line
        next(contract_data_reader)

        index = 1
        for contract_data_row in contract_data_reader:
            '''
            This comment block details the first row of data, for visual testing purposes.

            Budget type: 2
            Serial number of procurement: 017
            Type procurement: 5
            The value of procurement: 2
            Procurement procedures: 1
            Classification (2 first digits of CPV): 45

            Title of the procurement activity: "Mirembajtja teknike e objekteve komunale"

            The date of the initiation of the procurement activity: 02.03.2015
            Date of publication of the contract notice: 05.03.2015
            Date of publication of the notice of award of contract: 15.05.2015
            Date of signing the contract (in case of canceling the date of the cancellation notice): 02.06.2015
            Deadlines for implementation of the contract (write the date of commencement and completion): 3 vite
            Date of conclusion of the contract (date of receipt of interim / preliminary): 02.06.2018

            The estimated value of the contract: € 180,000.00
            The contract price, including all taxes etc.: € 1,135,550.25
            Annex contract price, including all taxes etc.: N/A
            Deductions from the contract due to restrictions: N/A
            The total price paid for the contract: € 340,665.08

            EO whose name was given contracts: "CDC"
            Domestic operators (1); Not local (2)
            Number of bids submitted:
            Number of bids rejected (write only those with the lowest price compared to the winner):
            Deadline for receiving tenders:
            Criteria for contract award:
            '''

            # keep this commented out logic as reference for now.
            '''
            contract_data_dict = {
                'budget_type': utils.budget_types.get(contract_data_row[0].strip(), empty_val)[LANG],
                'procurement_serial_number': contract_data_row[1].strip(),
                'procurement_type': utils.procurement_types.get(contract_data_row[2].strip(), empty_val)[LANG],
                'procurement_value_size': utils.procurement_value_sizes.get(contract_data_row[3].strip(), empty_val)[LANG],
                'procurement_procedure': utils.procurement_procedures.get(contract_data_row[4].strip(), empty_val)[LANG],
                'classification': contract_data_row[5].strip(),
                'activity_title': contract_data_row[6].strip(),
                'procurement_initiation_date': contract_data_row[7].strip(),
                'contract_notice_publication_date': contract_data_row[8].strip(),
                'contract_award_notice_publication_date': contract_data_row[9].strip(),
                'contract_signing_or_cancel_date': contract_data_row[10].strip(),
                'contract_length': contract_data_row[11].strip(),
                'contract_conclusion_date': contract_data_row[12].strip(),
                'estimated_contract_value': contract_data_row[13].strip(),
                'contract_price': contract_data_row[14].strip(),
                'contract_annex_price': contract_data_row[15].strip(),
                'deduction_from_contract': contract_data_row[16].strip(),
                'total_price_paid': contract_data_row[17].strip(),
                'awardee_name': contract_data_row[18].strip(),
                'awardee_is_domestic': contract_data_row[19].strip(),
                'total_bids_submitted': contract_data_row[20].strip(),
                'total_bids_rejected_with_lower_price_than_awardee': contract_data_row[21].strip(),
                'tender_application_deadline_type': utils.tender_application_deadline_types.get(contract_data_row[22].strip(), empty_val)[LANG],
                'award_criteria': utils.award_criteria.get(contract_data_row[23].strip(), empty_val)[LANG],
            }
            '''

            # Supplier:
            supplier = {
                'identifier': {
                    'scheme': '',
                    'id': '',
                    'legalName': contract_data_row[18].strip()
                },
                'name': contract_data_row[18].strip()
            }

            award = {
                'id': ODK_OCID + '-000-00001-award-' + str(index),
                'title': contract_data_row[6].strip(),
                'description': contract_data_row[6].strip(),
                'status': 'active',  # FIXME: That is the value for completed award?
                'date': utils.convert_to_ocds_date_format(index, contract_data_row[9].strip(), date_format),  # FIXME: Need to format date correctly.
                'value': {
                    'amount': utils.clean_price_value(index, contract_data_row[17].strip()),  # To be fetched from data source
                    'currency': 'EUR'
                },
                'suppliers': [],
                'contractPeriod': {
                    'endDate': utils.convert_to_ocds_date_format(index, contract_data_row[12].strip(), date_format) # FIXME: Need to format date correctly.
                }
            }

            # Push supplier into supplier list.
            award['suppliers'].append(supplier)

            # Push award into award list.
            release['awards'].append(award)

            # Contract:
            contract = {
                'id': ODK_OCID + '-000-00001-contract-' + str(index),  # FIXME: Figure out proper way of generating an id.
                'awardID': ODK_OCID + '-000-00001-award-' + str(index),  # FIXME: Figure out proper way of generating an id.
                'title': contract_data_row[6].strip(),
                'description': contract_data_row[6].strip(),
                'status': 'active',  # FIXME: Figure out what to put here.
                'period': {
                    'endDate': utils.convert_to_ocds_date_format(index, contract_data_row[12].strip(), date_format),  # FIXME: Need to format date correctly.
                },
                'value': {
                    'amount': utils.clean_price_value(index, contract_data_row[14].strip()),
                    'currency': "EUR"
                },
                'dateSigned': utils.convert_to_ocds_date_format(index, contract_data_row[10].strip(), date_format)  # FIXME: Need to format date correctly.
            }

            # Push award into award list.
            release['contracts'].append(contract)

            # Push release into release list
            ocds_contract_doc['releases'].append(release)

            # Write document into JSON file
            complete_contract_json_str = json.dumps(ocds_contract_doc, indent=4)

            with open('output/gjilan-2015-contract-' + str(index) + '.json', 'w') as json_file:
                json_file.write(complete_contract_json_str)

            # Reset release  values in preparation of next contract.
            ocds_contract_doc['releases'] = []
            release['awards'] = []
            release['contracts'] = []
            award['suppliers'] = []

            index += 1

# Delete all previously created files
json_file_list = glob.glob('output/*.json')
for f in json_file_list:
    os.remove(f)

# Create OCDS contract JSON files.
process_data('sample-csv/gjilan-2015-buyer-data.csv', 'sample-csv/gjilan-2015-contract-data.csv', '%d.%m.%Y')
