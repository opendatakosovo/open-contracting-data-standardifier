# -*- coding: utf-8 -*-
import csv
import os
import glob
import utils
import doc_utils


def process_data(buyer_data_file_path, data_file_path, date_format):

    ocds_planning = doc_utils.create_ocds_planning_doc('http://data.opendatakosovo.org/procurements/2016/gjilan-planning.json')
    ocds_contract = doc_utils.create_ocds_contract_doc('http://data.opendatakosovo.org/procurements/2016/gjilan-contract.json')

    with open(buyer_data_file_path, 'rb') as mdf:
        buyer_data_reader = csv.reader(mdf)

        # skip header line
        next(buyer_data_reader)

        for buyer_data_row in buyer_data_reader:

            # Data dictionary
            buyer_data_dict = utils.create_buyer_data_dict(1, buyer_data_row, date_format)

            # Buyer
            buyer = doc_utils.create_buyer(buyer_data_dict)

            # Releases
            release_planning = doc_utils.create_release_for_contract(buyer)
            release_contract = doc_utils.create_release_for_contract(buyer)

    with open(data_file_path, 'rb') as df:
        data_reader = csv.reader(df)

        # skip header line
        next(data_reader)

        index = 1
        for data_row in data_reader:

            data_dict = utils.create_data_dict(index, data_row, date_format)

            '''
                Create Planning Document
            '''
            planning = doc_utils.create_planning(data_dict)
            release_planning['planning'] = planning
            release_planning['tender'] = {}  # TODO: create tender document

            ocds_planning['releases'].append(release_planning)

            # Output to JSON file
            doc_utils.write_planning(ocds_planning, index)

            ocds_planning['releases'] = []
            release_planning['planning'] = {}
            release_planning['tender'] = {}

            '''
                Create Tender Document
            '''
            # TODO: Create document and write it to JSON file

            '''
                Create Tender Amendment Document
            '''
            # TODO: Create document and write it to JSON file

            '''
                Create Award Document
            '''
            # TODO: Create document and write it to JSON file

            '''
                Create Contract Document
            '''
            # Supplier
            supplier = doc_utils.create_supplier(data_dict)

            # Award
            award = doc_utils.create_award(data_dict, index)

            # Push supplier into supplier list.
            award['suppliers'].append(supplier)

            # Push award into award list.
            release_contract['awards'].append(award)

            # Contract
            contract = doc_utils.create_contract(data_dict, index)

            # Push award into award list.
            release_contract['contracts'].append(contract)

            # Push release into release list
            ocds_contract['releases'].append(release_contract)

            # Output to JSON file
            doc_utils.write_contract(ocds_contract, index)

            # Reset release values in preparation of next contract.
            ocds_contract['releases'] = []
            release_contract['awards'] = []
            release_contract['contracts'] = []
            award['suppliers'] = []

            '''
                Create Award Document
            '''
            # TODO: Create document and write it to JSON file

            index += 1


# Create output folder if it doesn't exist already
if not os.path.exists('output'):
    os.makedirs('output')

# Delete all previously created files
json_file_list = glob.glob('output/*.json')
for f in json_file_list:
    os.remove(f)

# Create OCDS contract JSON files.
process_data('sample-csv/gjilan-2015-buyer-data.csv', 'sample-csv/gjilan-2015-contract-data.csv', '%d.%m.%Y')
