import numpy as np
import pandas as pd
filepath = '/2015-raporti-vjetor-per-kontratat-e-nenshkruara-publike.xlsx'
df = pd.read_excel(filepath, skiprows=26, skip_footer=58, index_col=False)
# pull meta data
meta = pd.read_excel(filepath, skiprows=0, skip_footer=173, index=False, encoding='iso8859_2')
publishedDate = pd.Series(pd.to_datetime(meta.iat[5,6]))
publisher = pd.Series(meta.iloc[:,8].str.encode(encoding="utf-8", errors="strict"))
publisher_fields = pd.Series(meta.iloc[:,1]).str.encode(encoding="utf-8", errors="strict")

meta_info = pd.concat([publisher_fields, publisher], ignore_index=True, axis=1)
meta_info.iat[5,1] = publishedDate
meta_info.rename(columns={0:"publisher_fields",1:'publisher_info'}, inplace=True)
print meta_info


#rename columns to comply with OCDS
df.rename(index=str, columns={
    df.rename(index=str, columns={
    1:'releases/planning/budget/source', 
    2:'id', 
    3:'releases/tender/description', 
    4:'releases/tender/value/description', 
    5:'releases/tender/procurementMethod', 
    6:'releases/FPP', 
    7:'releases/tender/title', 
    8:'releases/planning/period/endDate', 
    9:'releases/tender/tenderPeriod/startDate',
    10:'releases/tender/tenderPeriod/endDate', 
    11: 'releases/contract/DateSigned',
    12:'releases/contract/contractPeriod/timeframe', 
    13:'releases/contract/contractPeriod/endDate', 
    14:'releases/contract/contractValue/amount/estimate', 
    15:'releases/contract price', 
    16:'releases/Annex/AnnexValue/amount',
    17:'releases/Contract/contractValue/amount/deductions', 
    18:'releases/contract/contractValue/amount', 
    19:'releases/Award/AwardSuppliers/name', 
    20: 'releases/Award/AwardSuppliers/local',
    21:'releases/Tender/numberOfEnquires', 
    21:'releases/Tender/numberOfRequests', 
    'Unnamed: 21': 'releases/Tender/numberOfTenderers',
    22: 'releases/Tender/numberOfTendersRejected', 
    23:'releases/Tender/details/expedited', 
    24:'releases/Tender/awardCriteria'}, inplace=True)

#add in currency information
df['Value.currency'] = 'EUR'
#add in language code
df['langauge'] = 'en'
#add OCID prefix
df['ocid'] = 'ocds-3n5h6d-'
df['id'] = df['id'].astype(str)
df['ocid'] = df[['ocid','id']].apply(lambda x: ''.join(x), axis=1)



###############################


#transform datetime formats

def to_date(series):
    ts = pd.to_datetime(series, yearfirst = True)
    return ts
    
startTime = str('00:00:00UTC+1h')
endTime= str('23:23:59UTC+1h')

df['planning/period/endDate'] = to_date(df['planning/period/endDate'])
df['tender/tenderPeriod/startDate' ] = to_date(df['tender/tenderPeriod/startDate' ])
df['tender/tenderPeriod/endDate'] = to_date(df['tender/tenderPeriod/endDate'])
df['contract/DateSigned'] = to_date(df['contract/DateSigned'])
df['contract/contractPeriod/endDate'] = to_date(df['contract/contractPeriod/endDate'])
    
#convert numerical variables back into string text

df['planning/budget/source'] = df['planning/budget/source'].replace([1,2,3],['local municipal funds', 'Kosovo Consolidated Budget', 'Donation' ])
df['tender/description'] = df['tender/description'].replace([1,2,3,4,5,6,7], ['supply', 'services', 'counseling services','design contest', 'jobs', 'concession jobs', 'immovable property'])
df['tender/value/description'] = df['tender/value/description'].replace([1,2,3,4], ['great','medium','small', 'minimal'])
df['tender/procurementMethod'] = df['tender/procurementMethod'].replace([1,2,3,4,5,6,7],['open procedure', 'restricted procedure', 'design contest', 'negotiated procedure after publication of a contract notice','negotiated procedure without publication of a contract notice', 'price quotation procedure', 'cheapest offer' ])
df['Award/AwardSuppliers/local'] = df['Award/AwardSuppliers/local'].replace([1,2],['domestic', 'international'])

# convert to machine readable - Award.contractPeriod
#split the column on white space into a new df
#x = df['contract/contractPeriod/timeframe'].str.split(expand=True)

#translate Albanian time expressions into an integer amount of days
#x[0] = x[0].replace(['një', 'tri', 'tre', 'dy', '12-', '90ditë', 'dhjetë'], [1,3,3,2,12,90,10])
#x[1] = x[1].replace(['ditë', 'vite', 'muaj', 'dite', 'vit', 'muj', '-muaj'], [1,365, 30,1, 365, 30,30 ])

#******issue: strings containing ë are not being replaced

# multiply x[0] and x[1] to create series showing contract length in days

#x[3] = x[0] * x[1]

# use contract length to fill in missing values in contractPeriod.endDate


df.to_csv('2016 Gjilan public works report-releases.csv')
meta_info.to_csv('2016 Gjilan public works report-meta info.csv')
#create csv to convert to json
csv_tojson = pd.concat([df,meta_info], axis=1)
csv_tojson.to_csv('/Users/coreyclip/Desktop/2016 Gjilan public work report/2016 Gjilan public works report-tojson.csv' ,encoding='utf-8')

# convert file to json
json = {}
json_list = []

import csv
file = '/2016 Gjilan public works report-tojson.csv'
with open('file', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
for row in csv_reader:
    json_list{
    "uri":"http://data.opendatakosovo.org/procurements/2016/gjilan-contract.json",
    "publishedDate":"2014-07-21T14:45:00Z",
    "publisher": {
        "scheme": "",
        "uid": "",
        "name": "Open Data Kosovo",
        "uri": "http://data.opendatakosovo.org/procurements/"
        },
    "license":"http://opendatacommons.org/licenses/pddl/1.0/",
    "publicationPolicy":"https://github.com/open-contracting/sample-data/",
    "buyer": {
        
    }
    "releases": {
        "ocid": row[27],
        "language": row[26],
        "date": "2014-07-21T14:45:00Z",
        "tag": ["contract"],
        "initiationType": "tender",
        "planning": {
            "period": {
                "endDate":row[7],
            }
            "budget": {
                "source": row[0],
        "local_id" : row[1],
        "tender": {
            "description": row[2],
            "value": {
                "description": row[3],
            "procurementMethod": row[4],
            "title": row[6],
            "tenderPeriod": {
                "startDate": row[8],
                "endDate": row[9],
        "contract": {
            "DateSigned": row[10],
            "contractPeriod": {
                "timeframe": row[11],
                "endDate":row[12],
            }
            "contractValue": {
                "amount": {
                    "estimate":row[13],
                    "deductions": row[16],
                    "amount": row[17],
                }
            }
            "numberOfRequests": row[20],
            "numberOfTenderers": row[21],
            "numberOfTenderersRejected": row[22],
            "details": { 
                "expedited": row[23],
            }
            "awardCriteria": row[24],
            
            }
        "Value": {
            "currency":row[25],
        }
        "FFP": row[5],
        "contract price": row[14],
        "Annex":{
            "AnnexValue":{
                "amount":row[15],
                
            }
        }
        "Award": {
            "AwardSuppliers": {
                "name":row[18],
                "local": row[19],
                
            }
        }
            }
        }
            
            }
    
            }
        
    }]
    
    

json_list.push(json)

print(json_list)



