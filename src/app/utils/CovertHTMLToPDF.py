#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : BOTIN POV                                      |
#  | EMAIL: botin.pov@gmail.com                            |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 23.02.2024                                   |
#  +-------------------------------------------------------+

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import render_to_string
from django.conf import settings
import os
import datetime
from django.utils import timezone


def htmlToPdf(context, pdf_path, pdf_name, template_path):
    try:
        # Check if required input parameters are provided
        if not pdf_path or not pdf_name or not template_path:
            raise ValueError("Invalid input parameters. Please provide all required inputs.")

        # pdf_path = f"loan_files/loan_contract/{id}/"
        # pdf_name = "generated_file.pdf"
        # template_path = os.path.join("loan_contract/template.html")
        current_datetime = datetime.datetime.now()
        pdf_name = pdf_name if ".pdf" in pdf_name else f"{pdf_name}.pdf"
        if template_path[-5:] != ".html":
            template_path += ".html"

        staticPath = "static/file_storage/"
        # Get absolute paths to generate PDF
        get_pdf_path = os.path.join(staticPath, f"{pdf_path}")
        pdf_file_path = os.path.join(get_pdf_path, f"{pdf_name}")

        # Ensure the directory exists
        os.makedirs(get_pdf_path, exist_ok=True)

        # Render the template with data
        html_content = render_to_string(template_path, context)
        html = HTML(string=html_content)
        font_config = FontConfiguration()
        css = CSS(string=''' ''', font_config=font_config)


        # Use WeasyPrint to convert HTML to PDF
        html.write_pdf(
            pdf_file_path,
            stylesheets=[css],
            font_config=font_config
        )
        # Construct PDF file URL
        base_url = settings.GET_MEDIA_URL
        pdf_file_url = f"{base_url}/{pdf_path}{pdf_name}"

        # Get information about the generated PDF file
        file_info = {
            "upload_file_name": pdf_name,
            "original_name": pdf_name,
            "file_type": "application/pdf",  # PDF files are typically of this type
            "extension": ".pdf",
            "file_size": os.path.getsize(pdf_file_path),
            "timestamp": int(current_datetime.timestamp()),
            "file_path": pdf_path,
            "url": pdf_file_url,
        }

        # Return the information about the generated PDF file
        return file_info

    except Exception as e:
        # Print the error and raise a ValueError with the same message
        raise ValueError(f"Error during PDF generation: {e}")


#--------------------------------------------------------------------------------------------------------------------------
# Note: Internal Functions and Third Party Required
# Used: pip install WeasyPrint or pip3 install WeasyPrint
# Used: render_to_string  django.template.loader
# USed: settings.GET_MEDIA_URL base on configuration setting base_url on setting.py
# Use case for generating a PDF from a Django template and context data  
#--------------------------------------------------------------------------------------------------------------------------
# # Example data with tables      
# tables_data = [
#     {
#         'table_name': 'Botin POV',
#         'rows': [
#             {'column1': 'Data1', 'column2': 'Data3'},
#             {'column1': 'Data2', 'column2': 'Data4'},
#             # Add more rows as needed
#         ],             
#        
#     },
#     {
#         'table_name': 'Dara Soy',
#         'rows': [
#             {'column1': 'Data1', 'column2': 'Data3'},
#             {'column1': 'Data2', 'column2': 'Data4'},
#             # Add more rows as needed
#         ]
#     },
#     # Add more tables as needed
# ]
#
# pdf_path = f"loan_files/loan_contract/{id}/"
# pdf_name = "generated_file.pdf"
# template_path = os.path.join("loan_contract/template.html")
#
# try:
#     result = htmlToPdf({'tables_data': tables_data}, pdf_path, pdf_name, template_path)
#     print("PDF generation successful!")
#     print(result)
# except ValueError as ve:
    


#--------------------------------------------------------------------------------------------------------------------------
# Folder Level folder: templates/loan_contract/template.html
# If you don't have template.html please create it    
#--------------------------------------------------------------------------------------------------------------------------
# <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
# <head>
#     <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <meta name="x-apple-disable-message-reformatting">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
#     <!-- Start stylesheet -->
#     <style type="text/css">
#     </style>
#     <!-- End stylesheet -->

# </head>
    
# <body>
#     <h1>Your PDF Report</h1>
#     <!-- Loop through tables and data -->
#     {% for table_data in tables_data %}
#         <h2>{{ table_data.table_name }}</h2>
#         <table>
#             <thead>
#                 <tr>
#                     <th>Header 1</th>
#                     <th>Header 2</th>
#                     <!-- Add more headers as needed -->
#                 </tr>
#             </thead>
#             <tbody>
#                 {% for row in table_data.rows %}
#                     <tr>
#                         <td>{{ row.column1 }}</td>
#                         <td>{{ row.column2 }}</td>
#                         <!-- Add more columns as needed -->
#                     </tr>
#                 {% endfor %}
#             </tbody>
#         </table>
#     {% endfor %}
#
# </body>
# </html>   
    

    
def calculate_age(dob):
    if dob:
        dob_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        today = datetime.datetime.now().date()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return age
    else:
        return None



def get_address(customer):
    contacts = customer.get("contacts", [])
    if not contacts:
        return ""

    first_contact = contacts[0]
    province = first_contact.get("province", {}).get("name_kh", None)
    district = first_contact.get("district", {}).get("name_kh", None)
    commune = first_contact.get("commune", {}).get("name_kh", None)
    village = first_contact.get("village", {}).get("name_kh", None)

    check_village = village if village and "ភូមិ" in village else f"ភូមិ{village}" if village else ""

    house_no = first_contact.get("house_no", None)
    street = first_contact.get("street", None)

    capital = "រាជធានី​ភ្នំពេញ" if province in ["ភ្នំពេញ"] else f"ខែត្ត/ក្រុង​{province}"

    the_house_no = f"ផ្ទះលេខ{house_no}," if house_no else ""
    the_street = f"ផ្លូវលេខ{street}" if street else ""

    commune_show = f"សង្កាត់​{commune}" if province in ["ភ្នំពេញ"] else f"ឃុំ{commune}"
    district_show = f"ខណ្ឌ{district}" if province in ["ភ្នំពេញ"] else f"ស្រុក{district}"

    address = f"{the_house_no} {the_street} {check_village} {commune_show} {district_show} {capital}"

    return address




def format_currency(amount):
    try:
        # Convert the amount to a float if it's not already
        amount = float(amount)
        # Format the amount with commas and two decimal places
        formatted_amount = "{:,.2f}".format(amount)
        # Replace the decimal separator with a comma
        formatted_amount = formatted_amount.replace('.', ',')
        return formatted_amount
    except (ValueError, TypeError):
        return "Invalid amount"

def convert_term(term):
    return int(float(term))



def convert_date_format(date_str):
    date_obj = datetime.datetime.fromisoformat(date_str.split('+')[0])
    formatted_date = date_obj.strftime("%Y/%m/%d")
    return formatted_date





def contractKey(contract):
    context = {}
    # Borrower data==========================================================
    created_at = contract.get("created_at", None)
    formatted_date = convert_date_format(created_at)
    borrower = contract.get("borrower", {})
    salutation_selected = borrower.get("salutation_selected", {})
    identifications = borrower.get("identifications", [])
    contacts = borrower.get("contacts", [])
    place_of_birth = borrower.get("place_of_birth", None)
    fullname_kh = borrower.get("fullname_kh", None)
    fullname_en = borrower.get("fullname_en", None)
    gender = borrower.get("gender", None)
    name_kh = salutation_selected.get("name_kh", None)
    legal_id = identifications[0].get("legal_id", None)
    identification_expiry_date = identifications[0].get("identification_expiry_date", None)
    identification_issue_date = identifications[0].get("identification_issue_date", None)
    dob = borrower.get("dob", None)
    phone1 = contacts[0].get("phone1")
    job = borrower.get("job", None)
    job_location = borrower.get("job_location", None)

    # Assign extracted fields to context dictionary
    context['CREATED_AT'] = formatted_date
    context['BO_PLACE_OF_BIRTH'] = place_of_birth
    context['BO_NAME_KH'] = fullname_kh
    context['BO_NAME_EN'] = fullname_en
    context['BO_SALUTATION'] = name_kh
    # If gender is "M" (Male), return Khmer data for "ប្រុស"; otherwise, return Khmer data for "ស្រី"
    context['BO_GENDER'] = "ប្រុស" if gender == "M" else "ស្រី"
    context["BO_SALU2"] = "ខ្ញុំបាទ" if gender == "M" else "នាងខ្ញុំ"
    context["BO_ID"] = legal_id
    context["BO_ID_DATE"] = identification_issue_date
    context["BO_DOB"] = dob
    context['BO_AGE'] = calculate_age(dob)
    context['BO_ADDRESS'] = get_address(borrower)
    context['BO_PHONE'] = phone1 
    context['BO_JOB'] = job 
    context['BO_JOBLOCATION'] = job_location 
    print(context['CREATED_AT'])
    # Co borrower data =================================================
    co_borrows = contract.get("co_borrows", [])
    salutation_selected = co_borrows[0].get("salutation_selected", {})
    relationship_bo_selected = co_borrows[0].get("relationship_bo_selected", {})
    relationship_co_selected = co_borrows[0].get("relationship_co_selected", {})
    co_identifications = co_borrows[0].get("identifications" , None)
    co_contacts = co_borrows[0].get("contacts", [])
    co_name_kh = salutation_selected.get("name_kh", None)
    place_of_birth = co_borrows[0].get("place_of_birth", None)
    co_fullname_kh = co_borrows[0].get("fullname_kh", None)
    co_fullname_en = co_borrows[0].get("fullname_en", None)
    co_gender = co_borrows[0].get("gender", None)
    co_legal_id = co_identifications[0].get("legal_id", None)
    co_identification_expiry_date = co_identifications[0].get("identification_expiry_date", None)
    co_identification_issue_date = co_identifications[0].get("identification_issue_date", None)
    dob = co_borrows[0].get("dob", None)
    co_phone1 = co_contacts[0].get("phone1")
    co_job = co_borrows[0].get("job", None) 
    co_job_location = co_borrows[0].get("job_location", None)
    name_bo_kh = relationship_bo_selected.get("name_kh", None)
    name_co_kh = relationship_co_selected.get("name_kh", None)

    context['CO_SALUTATION'] = co_name_kh
    context['CO_PLACE_OF_BIRTH'] = place_of_birth
    context['CO_NAME_KH'] = co_fullname_kh
    context['CO_NAME_EN'] = co_fullname_en
    # If gender is "M" (Male), return Khmer data for "ប្រុស"; otherwise, return Khmer data for "ស្រី"
    context['CO_GENDER'] = "ប្រុស" if co_gender == "M" else "ស្រី"
    context["CO_SALU2"] = "ខ្ញុំបាទ" if co_gender == "M" else "នាងខ្ញុំ"
    context["CO_ID"] = co_legal_id
    context["CO_ID_DATE"] = co_identification_issue_date
    context["CO_DOB"] = dob
    context['CO_AGE'] = calculate_age(dob)
    context['CO_ADDRESS'] = get_address(co_borrows[0])
    context['CO_PHONE'] = co_phone1 
    context['CO_JOB'] = co_job 
    context['CO_JOBLOCATION'] = co_job_location 
    context['RELATIONSHIP_BO'] = name_bo_kh
    context['RELATIONSHIP_CO'] = name_co_kh

    # contract data=========================================================
    request_type = contract.get("request_type", None)
    currency = contract.get("currency", None)
    currency_word = contract.get("currency_word", None)    
    amount = contract.get("amount", None)  
    formatted_amount = format_currency(amount)
    amount_in_form = formatted_amount
    amount_word = contract.get("amount_word", None)  
    loan_type = contract.get("loan_type", None)  
    term_m = contract.get("term_m", None)  
    interest_rate_m = contract.get("interest_rate_m", None)  
    interest_rate_y = contract.get("interest_rate_y", None)  
    fee = contract.get("fee", None)  
    purpose = contract.get("purpose", None)  
    repayment_method = contract.get("repayment_method", None) 

    context['REQUEST_TYPE'] = request_type
    context['CURRENCY'] = currency
    context['CURRENCY_WORD'] = currency_word
    context['AMOUNT'] = amount
    context['AMOUNT_IN_FORM'] = amount_in_form
    context['AMOUNT_WORD'] = amount_word
    context['LOAN_TYPE'] = loan_type
    context['TERM_M'] = convert_term(term_m) 
    context['INT_RATE_IN_Y'] = interest_rate_y
    context['INT_RATE_IN_M'] = interest_rate_m
    context['FEE'] = fee
    context['PURPOSE'] = purpose
    context['REPAYMENT_METHOD'] = repayment_method

    # guarantors data=========================================================
    guarantors = contract.get("guarantors", [])
    if guarantors:
        salutation_selected = guarantors[0].get("salutation_selected", {})
        gua_identifications = guarantors[0].get("identifications" , None)
        gua_name_kh = salutation_selected.get("name_kh", None)
        gua_fullname_kh = guarantors[0].get("fullname_kh", None)
        contacts = guarantors[0].get("contacts", [])
        gua_phone1 = contacts[0].get("phone1") if contacts else None
        gua_id = identifications[0].get("legal_id", None)
        context['GUA1_SALUTATION'] = gua_name_kh
        context['GUA1_NAME'] = gua_fullname_kh
        context['GUA1_ADDRESS'] = get_address(guarantors[0]) 
        context['GUA1_PHONE'] = gua_phone1 
        context['GUA1_ID'] = gua_id 
        
    else:
        context['GUA1_SALUTATION'] = None
        context['GUA1_NAME'] = None
        context['GUA1_ADDRESS'] = None
        context['GUA1_PHONE'] = None
        context['GUA1_ID'] = None

    # collaterals mortgagor1 data=========================================================
    collaterals = contract.get("collaterals", [])
    mortgagor1 = collaterals[0].get("mortgagor1", {})
    relationship_mortgagor1_selected = collaterals[0].get("relationship_mortgagor1_selected", {})
    salutation_selected = mortgagor1.get("salutation_selected", {})
    col1_contacts = mortgagor1.get("contacts", [])
    identifications = mortgagor1.get("identifications", [])
    col1_name_kh = salutation_selected.get("name_kh", None)
    col1_fullname_kh = mortgagor1.get("fullname_kh", None)
    col1_id = identifications[0].get("legal_id", None)
    col1_gender = mortgagor1.get("gender", None)
    dob = mortgagor1.get("dob", None)
    place_of_birth = mortgagor1.get("place_of_birth", None)
    col1_phone1 = col1_contacts[0].get("phone1", None)
    col1_father = mortgagor1.get("father_name", None)
    col1_mother = mortgagor1.get("mother_name", None)

    context['COLLATERAL1_SALU_MORTGAGOR1'] = col1_name_kh
    context['COLLATERAL1_MORTGAGOR1_NAME'] = col1_fullname_kh
    context['COLLATERAL1_MORTGAGOR1_ID'] = col1_id
    # If gender is "M" (Male), return Khmer data for "ប្រុស"; otherwise, return Khmer data for "ស្រី"
    context['COLLATERAL1_MORTGAGOR1_GENDER'] = "ប្រុស" if col1_gender == "M" else "ស្រី"
    context['COLLATERAL1_MORTGAGOR1_DATE_OF_BIRTH'] = dob
    context['COLLATERAL1_MORTGAGOR1_AGE'] = calculate_age(dob)
    context['COLLATERAL1_MORTGAGOR1_BIRTH_PLACE'] = place_of_birth
    context['COLLATERAL1_MORTGAGOR1_FATHER'] = col1_father
    context['COLLATERAL1_MORTGAGOR1_MOTHER'] = col1_mother
    context['COLLATERAL1_MORTGAGOR1_ADDRESS'] = get_address(mortgagor1)
    context['COLLATERAL1_MORTGAGOR1_PHONE'] = col1_phone1

    # collaterals mortgagor2 data=========================================================
    mortgagor2 = collaterals[0].get("mortgagor2", {})
    relationship_mortgagor2_selected = collaterals[0].get("relationship_mortgagor2_selected", {})
    salutation_selected = mortgagor2.get("salutation_selected", {})
    col2_contacts = mortgagor2.get("contacts", [])
    identifications = mortgagor2.get("identifications", [])
    col2_name_kh = salutation_selected.get("name_kh", None)
    col2_fullname_kh = mortgagor2.get("fullname_kh", None)
    col2_id = identifications[0].get("legal_id", None)
    col2_gender = mortgagor2.get("gender", None)
    dob = mortgagor2.get("dob", None)
    place_of_birth = mortgagor2.get("place_of_birth", None)
    col2_phone1 = col2_contacts[0].get("phone1", None)
    col2_father = mortgagor2.get("father_name", None)
    col2_mother = mortgagor2.get("mother_name", None)
    relation1_name_kh = relationship_mortgagor1_selected.get("name_kh", None)
    relation2_name_kh = relationship_mortgagor2_selected.get("name_kh", None)
    collateral_title_type = collaterals[0].get("collateral_title_type", None)
    collateral_id = collaterals[0].get("collateral_number", None)
    collateral_issue_date = collaterals[0].get("collateral_issue_date", None)
    collateral_description = collaterals[0].get("collateral_description", None)
    collateral_address = collaterals[0].get("collateral_address", None)
    collateral_commune = collaterals[0].get("collateral_commune", None)
    collateral_sangkat = collaterals[0].get("collateral_sangkat", None)
    collateral_commune_chief = collaterals[0].get("collateral_commune_chief", None)
    collateral_land_type = collaterals[0].get("collateral_land_type", None)
    collateral_issuer = collaterals[0].get("collateral_issuer", None)
    collateral_lot_number = collaterals[0].get("collateral_lot_number", None)

    context['COLLATERAL1_SALU_MORTGAGOR2'] = col2_name_kh
    context['COLLATERAL1_MORTGAGOR2_NAME'] = col2_fullname_kh
    context['COLLATERAL1_MORTGAGOR2_ID'] = col2_id
    # If gender is "M" (Male), return Khmer data for "ប្រុស"; otherwise, return Khmer data for "ស្រី"
    context['COLLATERAL1_MORTGAGOR2_GENDER'] = "ប្រុស" if col2_gender == "M" else "ស្រី"
    context['COLLATERAL1_MORTGAGOR2_DATE_OF_BIRTH'] = dob
    context['COLLATERAL1_MORTGAGOR2_AGE'] = calculate_age(dob)
    context['COLLATERAL1_MORTGAGOR2_BIRTH_PLACE'] = place_of_birth
    context['COLLATERAL1_MORTGAGOR2_FATHER'] = col2_father
    context['COLLATERAL1_MORTGAGOR2_MOTHER'] = col2_mother
    context['COLLATERAL1_MORTGAGOR2_ADDRESS'] = get_address(mortgagor2)
    context['COLLATERAL1_MORTGAGOR2_PHONE'] = col2_phone1
    context['COLLATERAL1_RELATIONSHIP_MORTGAGOR1'] = relation1_name_kh
    context['COLLATERAL1_RELATIONSHIP_MORTGAGOR2'] = relation2_name_kh
    context['COLLATERAL1_TITLE_TYPE'] = collateral_title_type
    context['COLLATERAL1_ID'] = collateral_id
    context['COLLATERAL1_ISSUE_DATE'] = collateral_issue_date
    context['COLLATERAL1_DESCRIPTION'] = collateral_description
    context['COLLATERAL1_ADDRESS'] = collateral_address
    context['COLLATERAL1_COMMUNE'] = collateral_commune
    context['COLLATERAL1_KHUM_IN_SANGKAT'] = collateral_sangkat
    context['COLLATERAL1_COMMUNE_CHIEF'] = collateral_commune_chief
    context['COLLATERAL1_LAND_TYPE'] = collateral_land_type
    context['COLLATERAL1_ISSUER'] = collateral_issuer
    context['COLLATERAL1_LOT_NUMBER'] = collateral_lot_number


    # print("Context:", context)
    return context

