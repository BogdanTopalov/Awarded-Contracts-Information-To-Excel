import xml.etree.ElementTree as ElementTree

from helpers import convert_date, normalize_text, format_address

import pandas


xml_file = 'notices.xml'

tree = ElementTree.parse(xml_file)
root = tree.getroot()

CONTRACT_URL = 'https://www.contractsfinder.service.gov.uk/notice/'

all_contracts = []

for full_notice in root:
    contract_info = {
        'PublishedDate': '',
        'AwardedDate': '',
        'Title': '',
        'Description': '',
        'SupplierName': '',
        'SupplierAddress': '',
        'Value': '',
        'url': ''
    }

    for element in full_notice:
        if element.tag == 'Notice':
            for field in element:
                if field.tag == 'Id':
                    contract_info['url'] = CONTRACT_URL + field.text

                if field.tag in contract_info:

                    if field.tag == 'PublishedDate':
                        contract_info['PublishedDate'] = convert_date(field.text)
                        continue

                    elif field.tag == 'Description':
                        contract_info['Description'] = normalize_text(field.text)
                        continue

                    contract_info[field.tag] = field.text

        if element.tag == 'Awards':
            for award in element:
                for award_details in award:
                    if award_details.tag in contract_info:

                        if award_details.tag == 'AwardedDate':
                            contract_info['AwardedDate'] = convert_date(award_details.text)
                            continue

                        if award_details.tag == 'SupplierAddress':
                            contract_info['SupplierAddress'] = format_address(award_details.text)
                            continue

                        contract_info[award_details.tag] = award_details.text

    all_contracts.append(contract_info)


data_frame = pandas.DataFrame(all_contracts)

# Save the output as Excel file.
with pandas.ExcelWriter('output.xlsx') as writer:

    # Convert prices from string to float.
    data_frame['Value'] = data_frame['Value'].astype(float)

    data_frame.to_excel(writer, sheet_name='Contracts Output', index=False)

    # Adjust column widths.
    writer.sheets['Contracts Output'].set_column('A:B', 15)
    writer.sheets['Contracts Output'].set_column('C:D', 100)
    writer.sheets['Contracts Output'].set_column('E:E', 65)
    writer.sheets['Contracts Output'].set_column('F:F', 90)
    writer.sheets['Contracts Output'].set_column('G:G', 15)
    writer.sheets['Contracts Output'].set_column('H:H', 85)

print('Output file created successfully.')
