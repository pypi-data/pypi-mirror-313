from datetime import datetime
import re
from google.cloud import vision_v1
from googletrans import Translator
from deep_translator import GoogleTranslator
import io
from PIL import Image
# import anthropic
import json

translator = Translator()

def find_gender_from_back(text):
    gender = ''
    gender_pattern = r'(\d)([A-Za-z])(\d)'
    gender_match = re.search(gender_pattern, text)
    if gender_match:
        gender = gender_match.group(2)
        
    if not gender:
        gender_pattern = r'(\d)([MFmf])(\d)'
        gender_match = re.search(gender_pattern, text)
        if gender_match:
            gender = gender_match.group(2)

    return gender

def func_common_dates(  extract_no_space):
    dob = ''
    expiry_date = ''
    try:
        matches = re.findall(r'\d{2}/\d{2}/\d{4}', extract_no_space)
        y1 = matches[0][-4:]
        y2 = matches[1][-4:]
        if int(y1) < int(y2):
            dob = matches[0]
            expiry_date = matches[1]
        else:
            dob = matches[1]
            expiry_date = matches[0]
    except:
        dob = ''
        expiry_date = ''

    return dob, expiry_date

def convert_dob(input_date):
    day = input_date[4:6]
    month = input_date[2:4]
    year = input_date[0:2]

    current_year = datetime.now().year
    current_century = current_year // 100
    current_year_last_two_digits = current_year % 100

    century = current_century
    # If the given year is greater than the last two digits of the current year, assume last century
    if int(year) > current_year_last_two_digits:
        century = current_century - 1

    final_date = f"{day}/{month}/{century}{year}"

    return final_date

def func_expiry_date(  extract):
    extract_no_space = extract.replace(' ','')
    dob, expiry_date = func_common_dates(extract_no_space)
    if expiry_date == '':
        match_doe = re.findall(r'\d{7}[A-Z]{2,3}', extract_no_space)
        for i in match_doe:
         
            raw_doe = i[0:6]
            print(raw_doe)
            expiry_date = raw_doe[4:6]+'/'+raw_doe[2:4]+'/20'+raw_doe[0:2]
            try:
                dt_obj = datetime.strptime(expiry_date, '%d/%m/%Y')
                break
            except:
   
                expiry_date = ''

    return expiry_date

def convert_expiry_date(input_date):
    day = input_date[4:6]
    month = input_date[2:4]
    year = input_date[0:2]

    current_year = datetime.now().year
    current_century = current_year // 100
    current_year_last_two_digits = current_year % 100
    century = current_century

    if int(year) <= current_year_last_two_digits:
        century = current_century
    else:
        century = current_century
    final_date = f"{day}/{month}/{century}{year}"

    return final_date

def func_dob(  extract):
    extract_no_space = extract.replace(' ','')
    dob, expiry_date = func_common_dates(extract_no_space)
    if dob == '':  
        match_dob = re.findall(r'\d{7}(?:M|F)\d', extract_no_space)
        for i in match_dob:
            # print(i)
            raw_dob = i[0:6]
            # print(raw_dob)
            year = str(datetime.today().year)[2:4]
            temp = '19'
            if int(raw_dob[0:2]) > int(year):
                temp = '19'
            else:
                temp = '20'      
            dob = raw_dob[4:6]+'/'+raw_dob[2:4]+'/'+temp+raw_dob[0:2]
            try:
                dt_obj = datetime.strptime(dob, '%d/%m/%Y')
                break
            except:
                # print(f'invalid date {dob}')
                dob = ''
        else:
            pattern = r"\b(\d{14}).*?\b"

            new_dob_match = re.search(pattern, extract_no_space)

            if new_dob_match:
                new_dob = new_dob_match.group(1)
                new_dob = new_dob[:7]
                dob = convert_dob(new_dob)

    return dob

def remove_special_characters_mrz2(string):
    # This pattern matches any character that is not a letter, digit, or space
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', string)

def count_digits(element):
    digits = [char for char in element if char.isdigit()]
    return len(digits)

# def get_front_id_response_from_genai(front_id_data):
#     message = claude_client.messages.create(
#     model="claude-3-5-sonnet-20240620",
#     max_tokens=2000,
#     temperature=0.3,
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": f"From the attached text, please extract the data in a structured format, the response should be a dictionary, having name, dob(dd/mm/yyyy), id_number(11 digits), place_of_birth, occupation. The extracted details should be in arabic and a transliterated version(for the values that are in arabic) as having key_name_en, including name, dob(dd/mm/yyyy), id_number, etc.. the structure should be 'name_ar', 'name_en', 'occupation_ar', 'occupation_en', etc. Make sure that the response should only contain a dictionary, and nothing else. Here's the text for your task: {front_id_data}"
#                 }
#             ]
#         }]
#     )

#     return message.content[0].text

# def get_back_id_response_from_genai(back_id_data):
#     message = claude_client.messages.create(
#     model="claude-3-5-sonnet-20240620",
#     max_tokens=2000,
#     temperature=0.3,
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": f"From the attached text, please extract the data in a structured format, the response should be a dictionary, having name, dob(dd/mm/yyyy), issue_date(dd/mm/yyyy), expiry_date(dd/mm/yyyy), name, gender(to be extracted from mrz), mrz1, mrz2, mrz3, nationality. Make sure that the response should only contain a dictionary, and nothing else. Here's the text for your task: {back_id_data}"
#                 }
#             ]
#         }]
#     )

#     return message.content[0].text

def sdn_back_id_extraction(back_id_data):
    mrz_pattern = r'(IDSDN.*\n*.*\n*.*\n*.*|IDSDN.*\n*.*\n*.*\n*.*|IDSDN.*\n*.*\n*.*\n*.*)'
    nationality_pattern = r'([A-Z]+)<<'

    mrz1, mrz2, mrz3 = '', '', ''

    try:
        mrz = re.findall(mrz_pattern, back_id_data.replace(" ","").strip(), re.MULTILINE)
        mrz_str = mrz[0].replace(" ", "")
    except:
        mrz_str = ''

    if mrz_str:
        mrz_list=mrz_str.replace(" ", "").split("\n")
        try: 
            mrz1=mrz_list[0]
            if len(mrz_list)==3:
                mrz1, mrz2, mrz3 = mrz_list[0], mrz_list[1], mrz_list[2]
        except:
            mrz1=''

        try:
            mrz2=[ele for ele in [ele for ele in mrz_list if ele not in [mrz1,mrz3] ] if remove_special_characters_mrz2(ele) !='']
            if len(mrz2)>1:
                mrz2=max(mrz2, key=count_digits)+[ele for ele in mrz2 if ele!=max(mrz2, key=count_digits)][0]

                pattern = r'\d{7}[MF]\d{7}[\S]{3}<+?\d'
                mrz2_temp = re.search(pattern, mrz2.replace(">", ""))
                if mrz2_temp:
                    mrz2 = mrz2_temp.group(0)

                mrz2=mrz2.split('<')[0]+'<<<<<<<<<<'+mrz2.split('<')[-1]

                # mrz2=mrz2[0].split('<')[0]+'<<<<<<<<<<'+mrz2[-1][-1]
            else :
                mrz2=mrz2[0].split('<')[0]+'<<<<<<<<<<'+mrz2[0][-1]
        except:
            mrz2=''

    ## condition to replace O with 0
    try:
        pattern = r'(IDSDN[A-Z]{1,2})O(?=[0-9])'
        replacement = lambda m: m.group(1) + '0'
        mrz1 = re.sub(pattern, replacement, mrz1)
    except:
        pass

    ## condition to replace '>' with 7
    if mrz2 and mrz2.endswith('>'):
        mrz2 = mrz2.split('<')[0]+'<<<<<<<<<<'+'7'

    if not mrz3 or (mrz3.startswith('>') or mrz3.startswith('<')):
        pattern = r'^[A-Za-z]+<+[A-Za-z]+.*$'
        matches = re.findall(pattern, mrz_str, re.MULTILINE)
        try:
            mrz3 = list(filter(None, matches))[0]
        except:
            try:
                matches = re.findall(pattern, back_id_data, re.MULTILINE)
                mrz3 = list(filter(None, matches))[0]
            except:
                mrz3 = ''

    ## condition to add filler to mrz3, making it total length of 30 chars
    if len(mrz3) < 30:
        mrz3 = mrz3.ljust(30, '<')

    try:
        dob = func_dob(mrz2)
    except:
        dob = ''

    if not dob:
        matches = re.findall(r'\d{4}/\d{2}/\d{2}', back_id_data)
        sorted_dates = sorted(matches)
        dob = sorted_dates[0]
    
    expiry = func_expiry_date(mrz_str)
    if not expiry:
        matches = re.findall(r'\d{4}/\d{2}/\d{2}', back_id_data)
        sorted_dates = sorted(matches)
        expiry = sorted_dates[-1]

    #issue date
    try:
        matches = re.findall(r'\d{4}/\d{2}/\d{2}', back_id_data)
        sorted_dates = sorted(matches)
        if len(sorted_dates) > 2:
            issue_date = sorted_dates[1]
    except:
        issue_date = ''
    
    try:
        nationality=mrz2.split('<')[0][-3:]
    except: 
        nationality=''
    
    if mrz3:
        full_name_mrz = mrz3.replace('<', ' ').replace('>', ' ').strip()
    
    else:
        full_name_mrz = ''
    
    try:
        pattern = r'(?<=Name: )\w+(?: \w+)*|(?<=Name )\w+(?: \w+)*'

        match = re.search(pattern, back_id_data, re.IGNORECASE)
        name = match.group(0) or match.group(1)
    except:
        try:
            pattern = r'(?<=NAME):*[ \n]*([A-Z ]+)'

            match = re.search(pattern, back_id_data, re.IGNORECASE)
            if match:
                name = match.group(1).strip().replace(':', '')
            else:
                name = ''
        except:
            name = ''
    
    if full_name_mrz and not name:
        name = ' '.join(full_name_mrz.split(' ')[1:]) + ' ' + full_name_mrz.split(' ')[0] if full_name_mrz else ''
        name = name.strip()
    
    # try:
    #     response_genai = get_back_id_response_from_genai(back_id_data)
    #     response_genai_json = json.loads(response_genai)
    # except:
    #     response_genai_json = {}

    if name:
        first_name = name.split(' ')[0]
        last_name = name.split(' ')[-1]
        middle_name = ' '.join(name.split(' ')[1:-1])
    else:
        # try:
        #     if response_genai_json:
        #         name = response_genai_json.get('name', '')
        #         if name:
        #             first_name = name.split(' ')[0]
        #             last_name = name.split(' ')[-1]
        #             middle_name = ' '.join(name.split(' ')[1:-1])
        # except:
            first_name, last_name, middle_name = '', '', ''

    # if not issue_date:
    #     try:
    #         issue_date = response_genai_json.get('issue_date', '')
    #     except:
    #         issue_date = ''

    try:
        dob_pattern = r'(\d+)[MF]'
        dob_match = re.search(dob_pattern, mrz2)
        dob_mrz = convert_dob(dob_match.group(1)) if dob_match else ''

        doe_pattern = r'[MF](\d+)'
        doe_match = re.search(doe_pattern, mrz2)
        expiry_date_mrz = convert_expiry_date(doe_match.group(1)) if doe_match else ''
    except:
        dob_mrz, expiry_date_mrz = '', ''

    gender = ''
    try:
        gender = find_gender_from_back(mrz2)
    except:
        gender = find_gender_from_back(back_id_data)

    mrz_str = f"{mrz1}\n{mrz2}\n{mrz3}"

    try:
        if expiry and not expiry_date_mrz:
            expiry_date_mrz = expiry

        if dob and not dob_mrz:
            dob_mrz = dob
    except:
        pass


    back_data_dict = {
        "mrz": [mrz_str],
        "mrz1": mrz1.replace('*', '<'),
        "mrz2": mrz2,
        "mrz3": mrz3,
        # "dob_generic": dob,
        # "full_name_mrz": full_name_mrz,
        "name": name,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "issuing_country": "SDN",
        # "expiry_date_generic": expiry,
        "nationality": nationality,
        "dob_back": dob_mrz,
        "issue_date": issue_date,
        "expiry_date": expiry_date_mrz,
        "gender": gender
    }
    
    return back_data_dict


def crop_second_part(img):
    width, height = img.size
    half_width = width // 2
    second_part = img.crop((half_width, 0, width, height))
    return second_part

def extract_text_from_image_data(client, image):
    """Detects text in the file."""

    with io.BytesIO() as output:
        image.save(output, format="PNG")
        content = output.getvalue()

    image = vision_v1.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    return texts[0].description

def detect_id_card(client, image_data, id_text, part=None):
    if id_text:
        vertices = id_text[0].bounding_poly.vertices
        left = vertices[0].x
        top = vertices[0].y
        right = vertices[2].x
        bottom = vertices[2].y

        padding = 30
        left -= padding
        top -= padding
        right += padding
        bottom += padding

        # img = image_data

        with Image.open(io.BytesIO(image_data)) as img:
            id_card = img.crop((max(0, left), max(0, top), right, bottom))
            width, height = id_card.size
            if width < height:
                id_card = id_card.rotate(90, expand=True)
            

            part_text = id_text[0].description
            part_img = crop_second_part(id_card)
            part_text = extract_text_from_image_data(client, part_img)

            return  part_text

def extract_occupation(text):
    match = re.search(r'المهنة\s*([^\n]+)', text)
    if match:
        return match.group(1).strip().replace(":", "")
    else:
        match = re.search(r'المهن[ةــ]*\s*\n\s*([^\n]+)', text)
        if match:
            return match.group(1).replace(":", "").replace("ــة","").replace("ة.","").replace("ة","").replace("العقــ","").replace("ـ","").strip()
        else:
            return None

def extract_occupation_from_text(part_text):
    lines = part_text.split('\n')

    arabic_number_pattern = re.compile(r'[\u0660-\u0669]+')
    final_occupation = ''

    for i in range(len(lines) - 1, 0, -1):
        if arabic_number_pattern.search(lines[i]):
            occupation = lines[i - 1].strip()
            occupation = re.sub(r'\d+', '', occupation)
            occupation = re.sub(r'[A-Za-z]+', '', occupation)
            if occupation and occupation in ['العنــ', 'الغد', 'المهنــ', 'العنوان', 'العلب', 'العنب', 'ـوان', 'العيد', 'العز', 'العن', 'العد']:
                search_key = lines.index(occupation)
                final_occupation = lines[search_key-1]
                break
            else:
                final_occupation = occupation

    return final_occupation.replace(":", "").replace("المهنة", "").replace("ــة","").replace("ة.","").replace("ة","").replace("العقــ","").replace("ـ","").strip() if final_occupation else ""

def extract_occupation_v2(client, image_data, texts):
    part_text = detect_id_card(client, image_data, texts)
    occupation_res = extract_occupation_from_text(part_text)
    if not occupation_res:
        occupation_res = extract_occupation_from_text(texts[0].description)
    
    if occupation_res in ['الرقم الوطني'] or not occupation_res:
        occupation_res = extract_occupation(part_text)
        if not occupation_res:
            occupation_res = extract_occupation(texts[0].description)

    return occupation_res

def extract_place_of_birth(text):
    match = re.search(r'مكان الميلاد\s*([^\n]+)|مكان الميادد\s*([^\n]+)', text)
    if match:
        return match.group(1).strip().replace(":", "") if match.group(1) is not None else match.group(2).strip().replace(":", "")
    return None

def extract_dob(text):
    dob = ''
    extract_no_space = text.replace(" ", "")
    try:
        matches = re.findall(r'\d{4}/\d{2}/\d{2}', extract_no_space)
        dob = matches[0]
    except:
        dob = ''
    return dob

def extract_name_from_front(text, dob):
    name = ''
    lines = text.split("\n")
    for line in lines:
        if dob in line:
            search_key = lines.index(line)
            part_name = lines[search_key-1]
            if part_name:
                part_name = re.sub(r'\d+', '', part_name)
                part_name = re.sub(r'[A-Za-z]+', '', part_name)
                name = part_name.replace("الإســــــــــــم", "").replace("الاسم", "").replace("الإسم", "").replace("ـم", "").replace(":", "").strip()
                if name in ['تاريخ الميلاد', 'الإســ', 'الإسـ', 'الإس', 'الإصـ', 'تاریخ', 'الرقم الوطني'] or len(name.split(' '))<=2:
                    name = lines[search_key-2]
                    if name:
                        name = name.replace("الإســــــــــــم", "").replace("الاسم", "").replace("الإسم", "").replace("ـم", "").replace(":", "").strip()
                        name = re.sub(r'\d+', '', name)
                        name = re.sub(r'[A-Za-z]+', '', name)
                break
    return name.strip()

def sdn_front_id_extraction(client, ar_front_id_data, image_data, texts):
    front_id_data = translator.translate(ar_front_id_data, src='ar', dest='en').text
    # print(f'\n\nTranslated front ID data: {front_id_data}\n')
    
    id_number_pattern = r"\b\d{11}\b"
    
    id_number_match = re.search(id_number_pattern, front_id_data.replace(" ",""), re.IGNORECASE)
    if id_number_match:
        id_number = id_number_match.group(0)
    else:
        try:
            id_number_match = re.search(id_number_pattern, ar_front_id_data.replace(" ",""), re.IGNORECASE)
            id_number = id_number_match.group(0)
        except:
            id_number = ''

    # genai_front_response = get_front_id_response_from_genai(ar_front_id_data)
    # genai_front_response_json = json.loads(genai_front_response)
    
    # if not id_number or len(id_number) < 11 or id_number.startswith('<') or id_number.endswith('>'):
    #     try:
    #         id_number = genai_front_response_json.get('id_number', '')
    #     except:
    #         id_number = ''    


    try:
        occupation = extract_occupation_v2(client, image_data, texts)
        if occupation:
            try:
                occupation_en = GoogleTranslator(dest = 'en').translate(occupation)
            except:
                occupation_en = ''
        else:
            occupation, occupation_en = '', ''
    except:
        occupation, occupation_en = '', ''

    try:
        place_of_birth = extract_place_of_birth(ar_front_id_data)
        if place_of_birth:
            try:
                place_of_birth_en = GoogleTranslator(dest = 'en').translate(place_of_birth)
            except:
                place_of_birth_en = ''
        else:
            place_of_birth, place_of_birth_en = '', ''
    except:
        place_of_birth, place_of_birth_en = '', ''

    try:
        dob = extract_dob(ar_front_id_data)
    except:
        dob = ''
    
    try:
        full_name = extract_name_from_front(ar_front_id_data, dob)
        if full_name:
            if 'مكان الميلاد' in full_name:
                lines = ar_front_id_data.split('\n')
                search_pos = lines.index(full_name)
                full_name = lines[search_pos-1]
        else:
            full_name
    except:
        full_name

    return {
        'id_number': id_number,
        'occupation': occupation,
        'occupation_en': occupation_en,
        'place_of_birth': place_of_birth,
        'place_of_birth_en': place_of_birth_en,
        'dob': dob,
        'name_ar': full_name
    }
