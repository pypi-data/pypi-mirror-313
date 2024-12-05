from PIL import Image
import re
from datetime import datetime
import io
from deep_translator import GoogleTranslator
import pycountry
from rapidfuzz import process, fuzz
from idvpackage.common import extract_text_from_image_data
from io import BytesIO
import google.generativeai as genai
import os

def crop_second_part(img):
    width, height = img.size
    half_width = width // 2
    second_part = img.crop((half_width, 0, width, height))
    return second_part


def crop_third_part(img):
    width, height = img.size
    part_height = height // 6
    third_part = img.crop((0, 3.7 * part_height, width, height))
    return third_part


def detect_id_card(client, image_data, id_text, part=None):

    if id_text:
        vertices = id_text[0].bounding_poly.vertices
        left = vertices[0].x
        top = vertices[0].y
        right = vertices[2].x
        bottom = vertices[2].y

        padding = 40
        left -= padding
        top -= padding
        right += padding
        bottom += padding

        # img = image_data
        # with Image.open(io.BytesIO(image_data)) as img:
        #     id_card = img.crop((max(0, left), max(0, top), right, bottom))

        pil_image = Image.open(BytesIO(image_data))
        compressed_image = BytesIO()
        pil_image.save(compressed_image, format="JPEG", quality=50, optimize=True)
        compressed_image_data = compressed_image.getvalue()
        compressed_pil_image = Image.open(BytesIO(compressed_image_data))
        id_card = compressed_pil_image.crop((max(0, left), max(0, top), right, bottom))

        width, height = id_card.size
        if width < height:
            id_card = id_card.rotate(90, expand=True)
            
        if part=='second':
            part_img = crop_second_part(id_card)
        if part=='third':
            part_img = crop_third_part(id_card)
        
        # 2nd call to vision AI
        part_text = extract_text_from_image_data(client, part_img)

        return id_card, part_img, part_text
    else:
        print('No text found in the image.')

def is_arabic(word):
    return re.search(r'[\u0600-\u06FF]', word) is not None

def extract_name_ar(text):
    # patterns = [
    #     r"(?:الاسم|الإسم):\s*([^\n]+)",  
    #     r"الاسم\s+([^\n]+)"  
    # ]

    patterns = [
        r"(?:الإسم|الاسم):\s*([^\n]+)",
        r"(?:الإسم|الاسم)\s+([^\n]+)",
    ]

    for pattern in patterns:
        regex = re.compile(pattern, re.MULTILINE)
        match = regex.search(text)
        if match:
            return match.group(1).strip()

    return None

def extract_name_fields_from_cropped_part(text):

    pattern = r"Name:\s*([A-Z\s-]+)"
    name_dict = {}
    match = re.search(pattern, text)
    
    if match:
        extracted_name = match.group(1).strip()
        extracted_name = extracted_name.replace("\n", " ")
        unnecessary_words = ['OF', 'THE']
        extracted_name = [word for word in extracted_name.split() if word.upper() not in unnecessary_words]
        if len(extracted_name[-1]) <= 2:
            extracted_name = extracted_name[:-1]
        
        extracted_name = ' '.join(extracted_name)

        name_dict["name"] = extracted_name.strip()
        name_parts = extracted_name.split()

        first_name = name_parts[0].upper()
        last_name = name_parts[-1].upper()

        name_dict["first_name"] = first_name
        name_dict["last_name"] = last_name
    return name_dict

def identify_front(text):
    front_id_keywords = ["State of Qatar"]
    pattern = '|'.join(map(re.escape, front_id_keywords))
    
    try:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        else:
            return False
    except:
        return 'error'

def sort_dates_by_datetime(dates):
    return sorted(dates, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))

def extract_and_check_country(words):
    for word in words:
        try:
            country = pycountry.countries.lookup(word)
            if country:
                return country.name.upper()
        except LookupError:
            pass

    return ''

def extract_and_check_country_normalized(words):
    normalized_words = [re.sub(r'\s+|-', '', word).lower() for word in words]
    
    for country in pycountry.countries:
        common_name_normalized = re.sub(r'\s+|-', '', country.name).lower()
        official_name_normalized = re.sub(r'\s+|-', '', getattr(country, 'official_name', '')).lower()

        if common_name_normalized in normalized_words or official_name_normalized in normalized_words:
            return country.name.upper()

    return ''

def extract_name_after_nationality(word_list, nationality):
    nationality_index = word_list.index(nationality) if nationality in word_list else -1

    if nationality_index != -1 and nationality_index < len(word_list) - 1:
        words_after_nationality = word_list[nationality_index + 1:]
        return words_after_nationality
    else:
        return []

def get_fuzzy_match_score(line, patterns, threshold=80):
    result = process.extractOne(line, patterns, scorer=fuzz.WRatio)
    if result and result[1] > threshold:
        return result[1]
    return None

def extract_occupation_in_empty_case(text):
    pattern = re.compile(r'المهنة\s*[:]*\s*(\S*)', re.IGNORECASE)
    lines = text.split('\n')

    for i, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            if match.group(1):
                return match.group(1).strip()
            if i + 1 < len(lines):
                return lines[i + 1].strip()

    return ''

def extract_occupation_in_empty_case_v2(text):
    pattern = re.compile(r'occupation\s*[:]*\s*(\S*)', re.IGNORECASE)
    lines = text.split('\n')

    for i, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            if match.group(1):
                return match.group(1).strip()
            if i + 1 < len(lines):
                return lines[i + 1].strip()

    return ''

def genAI(ar_front_data, model):
    query = f"Please extract the nationality from the following text and provide the corresponding ISO 3166-1 alpha-3 country code for that nationality: {ar_front_data}"
    response = model.generate_content(query)
    nationality_ai = re.findall(r'\*\*(.*?)\*\*', response.text)[1]
    return  nationality_ai

def genAI_for_occupation(dct, model):
    query = f"""
    You are provided with the following front_data: {dct}. 

    Check if  'occupation_en' information is valid and correct. Please review this broadly without focusing on the specifics.
    for example if (doctor teacher employee and etc it is occupation as well)
    If 'occupation_en' match the expected values, respond with 'correct'. 
    If it is incorrect, respond with 'not_correct', if you are not able to determine then respond with 'undetermined'.
    as a response give me 'not_correct','undetermined' or 'correct' nothing else 
    """
    response = model.generate_content(query)
    value = response.candidates[0].content.parts[0].text.strip()

    return value


def genAI_for_occupation_correct(passport_details, model):
    query = f"""
    Please extract the occupation from the following text and provide it in this format:
    - English: **occupation**
    - Arabic: **occupation** return only these 2 nothing else.
    So you will get occupation in arabic and translate it into english and send it
      if no info about occupation then 'not_provided', for both English and Arabic: {passport_details}
    """
    response = model.generate_content(query)
    occupation_ai = re.findall(r'\*\*(.*?)\*\*', response.text)

    return occupation_ai

def genAI_for_expiry_date(ar_front_data, model):
    query = f"""
    Please extract the expiry date from the following text and provide it in this format(dd/mm/yyyy):
    - expiry_date, return only this 1 variable, nothing else.
      if no info about expiry_date found then return 'expiry_date': 'not_provided': {ar_front_data}
    """
    response = model.generate_content(query)
    expiry_ai = re.findall(r'\*\*(.*?)\*\*', response.text)[1]

    return expiry_ai

def extract_numeric_fields_from_raw(ar_front_data, third_part_text, name_extracted, model):
    front_data = GoogleTranslator(dest = 'en').translate(ar_front_data)
    id_number_pattern = r"\b\d{11}\b"
    
    words = re.findall(r'\b[A-Z]{4,}\b', ar_front_data)
    nationality = extract_and_check_country(words)
    
    nationality_iso = ''
    if not nationality:
        nationality = extract_and_check_country_normalized(words)
    
    if nationality:
        country = pycountry.countries.lookup(nationality)
        nationality_iso =  country.alpha_3

    ###############################################################
    if nationality_iso == '':
        try:
            pattern = r"(state[\s]*of[\s]*qatar|دولة[\s]*قطر)"
            ar_front_data = re.sub(pattern, "",ar_front_data, flags=re.IGNORECASE)
            nationality_iso = genAI(ar_front_data, model)
        except Exception as e:
            nationality_iso = ''  
    ################################################################
    
    names_list = extract_name_after_nationality(words, nationality)
    name = ' '.join(names_list)
    if not name:
        name = name_extracted

    id_number_match = re.search(id_number_pattern, ar_front_data, re.IGNORECASE)
    if id_number_match:
        id_number = id_number_match.group(0)
    else:
        try:
            id_number_match = re.search(id_number_pattern, ar_front_data, re.IGNORECASE)
            id_number = id_number_match.group(0)
        except:
            id_number = ''
    
    dates = sort_dates_by_datetime(re.findall(r'\d{2}/\d{2}/\d{4}', ar_front_data))
    combined_back_pattern = r'(Director General of the General Department|Directorate of Passports|Passport Number|Passport Expiry)'
    back_match = re.search(combined_back_pattern, ar_front_data, re.IGNORECASE)

    try:
        if back_match:
            if 'Passport' in ar_front_data:
                ar_front_data = ar_front_data.split("Name")[0]
            
            dates = sort_dates_by_datetime(re.findall(r'\d{2}/\d{2}/\d{4}', ar_front_data))

            if len(dates) > 2:
                # expiry = genAI_for_expiry_date(ar_front_data, model)
                dob = dates[0]
                expiry = dates[1]
            elif len(dates) <= 2:
                dob = dates[0]
                expiry = dates[-1]
        else:
            dob = dates[0]
            expiry = dates[-1]
    except:
        try:
            dob = dates[0]
            expiry = dates[-1]
        except:
            dob = ''
            expiry = ''
    
    if 'Passport' in ar_front_data:
        ar_front_data = ar_front_data.split("Name")[0]

    ar_front_data_filtered = [
            re.sub(r'\b[a-zA-Z0-9]+\b', '', line.replace(':', '').replace('/', '').replace('.', '').replace('المهنة', '').replace('تاريخ الميلاد', '').replace('دولة قطر', '').replace('الرقم الشخصي', '').replace('الصلاحية', '').replace('الجنسية', '').replace('رخصة إقامة', '').replace('الرقم', '').replace('اللى', '').replace('طو', '').replace('دولة', '').replace('الهند', '').replace('بطاقة', '').replace('إثبات', '').replace('شخصية', '').replace('ہے', '').replace('۔', '')) 
            for line in ar_front_data.split('\n')
        ]

    cleaned_lines = [line for line in ar_front_data_filtered if line.strip()]

    patterns_to_remove = [
        r"State Of Qatar", r"Residency Permit", r"ID\.No:", r"D\.O\.B\.:", r"D\.O\.B:",
        r"Expiry:", r"Nationality:", r"\d{9}", r"\d{2}/\d{2}/\d{4}", r"بنغلاديش", r"الهند",
        r"on", r"الرقم الشخصي:", r"تاريخ الميلاد:", r"الصلاحية:",
        r"الجنسية:", r"دولة قطر", r"رخصة إقامة", r"المهنة:", r"الاسم:", r"Name:"
        ]
    
    if nationality:
        patterns_to_remove.append(re.escape(nationality))
    
    if name:
        patterns_to_remove.append(re.escape(name))

    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns_to_remove]

    # lines = ar_front_data.split("\n")

    # filtered_lines = [line for line in lines if not any(pattern.search(line) for pattern in compiled_patterns)]
    countries_list = ['أفغانستان', 'جزر أولاند', 'ألبانيا', 'یمنی', 'الجزائر', 'ساموا الأمريكية', 'مغربي', 'أندورا', 'أنغولا', 'أنغويلا', 'القارة القطبية الجنوبية', 'أنتيغوا وبربودا', 'الأرجنتين', 'أرمينيا', 'أروبا', 'أستراليا', 'النمسا', 'أذربيجان', 'باهاماس', 'البحرين', 'بنغلاديش', 'بربادوس', 'بيلاروسيا', 'بلجيكا', 'بليز', 'بنين', 'برمودا', 'بوتان', 'بوليفيا', 'البوسنة والهرسك', 'بوتسوانا', 'جزيرة بوفيه', 'البرازيل', 'إقليم المحيط الهندي البريطاني', 'جزر العذراء البريطانية', 'بروناي', 'بلغاريا', 'بوركينا فاسو', 'بوروندي', 'كابو فيردي', 'كمبوديا', 'الكاميرون', 'كندا', 'الجزر الكاريبية الهولندية', 'جزر كايمان', 'جمهورية أفريقيا الوسطى', 'تشاد', 'تشيلي', 'الصين', 'جزيرة الكريسماس', 'جزر كوكوس', 'كولومبيا', 'جزر القمر', 'جمهورية الكونغو', 'جزر كوك', 'كوستاريكا', 'كرواتيا', 'كوبا', 'كوراساو', 'قبرص', 'التشيك', 'الدنمارك', 'جيبوتي', 'دومينيكا', 'جمهورية الدومينيكان', 'جمهورية الكونغو الديمقراطية', 'الاكوادور', 'السلفادور', 'غينيا الاستوائية', 'إريتريا', 'إستونيا', 'إسواتيني', 'إثيوبيا', 'جزر فوكلاند', 'جزر فارو', 'فيجي', 'فنلندا', 'فرنسا', 'غويانا الفرنسية', 'بولينزيا الفرنسية', 'أراض فرنسية جنوبية', 'الجابون', 'غامبيا', '\u202bجورجيا', 'ألمانيا', 'غانا', 'جبل طارق', 'اليونان', 'جرينلاند', 'غرينادا', 'غوادلوب', 'غوام', 'غواتيمالا', 'غيرنزي', 'غينيا', 'غينيا بيساو', 'غيانا', 'هايتي', 'جزيرة هيرد وجزر ماكدونالد', 'هندوراس', 'هونج كونج', 'هنجاريا', 'آيسلندا', 'الهند', 'أندونيسيا', 'إيران', 'العراق', 'أيرلندا', 'جزيرة مان', 'إيطاليا', 'ساحل العاج', 'جامايكا', 'اليابان', 'جيرسي', 'الأردن', 'كازاخستان', 'كينيا', 'كيريباتي', 'كوسوفو', 'الكويت', 'قيرغيزستان', 'لاوس', 'لاتفيا', 'لبنان', 'ليسوتو', 'ليبيريا', 'ليبيا', 'ليختنشتاين', 'ليتوانيا', 'لوكسمبورغ', 'ماكاو', 'مدغشقر', 'مالاوي', 'ماليزيا', 'المالديف', 'مالي', 'مالطا', 'جزر مارشال', 'مارتينيك', 'موريتانيا', 'موريشيوس', 'مايوت', 'المكسيك', 'ولايات ميكرونيسيا المتحدة', 'مولدوفا', 'موناكو', 'منغوليا', 'مونتينيغرو', 'مونتسرات', 'المغرب', 'موزمبيق', 'ميانمار', 'ناميبيا', 'ناورو', 'نيبال', 'هولندا', 'جزر الأنتيل الهولندية', 'كاليدونيا الجديدة', 'نيوزيلندا', 'نيكاراغوا', 'النيجر', 'نيجيريا', 'نييوي', 'جزيرة نورفولك', 'كوريا الشمالية', 'مقدونيا الشمالية', 'جزر ماريانا الشمالية', 'النرويج', 'سلطنة عمان', 'باكستان', 'بالاو', 'فلسطين', 'بنما', 'بابوا غينيا الجديدة', 'باراغواي', 'بيرو', 'الفلبين', 'جزر بيتكيرن', 'بولندا', 'البرتغال', 'بورتوريكو', 'قطر', 'ريونيون', 'رومانيا', 'روسيا', 'رواندا', 'سان بارتيلمي', 'سانت هيلينا', 'سانت كيتس ونيفيس', 'سانت لوسيا', 'سانت مارتن', 'سان بيير وميكلون', 'سانت فينسنت والغرينادين', 'ساموا', 'سان مارينو', 'ساو تومي وبرينسيب', 'السعودية', 'السنغال', 'صربيا', 'سيشل', 'سيراليون', 'سنغافورة', 'سانت مارتن', 'سلوفاكيا', 'سلوفينيا', 'جزر سليمان', 'الصومال', 'جنوب أفريقيا', 'جورجيا الجنوبية وجزر ساندويتش الجنوبية', 'كوريا الجنوبية', 'جنوب السودان', 'إسبانيا', 'سريلانكا', 'السودان', 'سورينام', 'سفالبارد ويان ماين', 'السويد', 'سويسرا', 'سوريا', 'تايوان', 'طاجيكستان', 'تنزانيا', 'تايلاند', 'تيمور الشرقية', 'توجو', 'توكيلاو', 'تونغا', 'ترينيداد وتوباغو', 'تونس', 'تركيا', 'تركمانستان', 'جزر توركس وكايكوس', 'توفالو', 'جزر الولايات المتحدة الصغيرة النائية', 'جزر العذراء الأمريكية', 'أوغندا', 'أوكرانيا', 'الإمارات العربية المتحدة', 'المملكة المتحدة', 'الولايات المتحدة الأمريكية', 'أوروغواي', 'أوزبكستان', 'فانواتو', 'مدينة الفاتيكان', 'فنزويلا', 'فيتنام', 'واليس وفوتونا', 'الصحراء الغربية', 'اليمن', 'زامبيا', 'زيمبابوي', 'اردني', 'اردنی', 'سریلانکا', 'پاکستان', 'بيكور', 'ایران', 'المهلة']
    
    arabic_keywords_to_remove = [
        "الرقم الشخصي", "تاريخ الميلاد", "الصلاحية", "لدولة", "الجنسية", "دولة قطر", "رخصة إقامة", "المهنة", "الإسم", "بطاقة", "إثبات", "شخصية", "ـلـة قـ", "ـة", "سلاحية"
    ]

    filtered_lines = []
    for line in cleaned_lines:
        match_score = get_fuzzy_match_score(line, arabic_keywords_to_remove)
        match_score1 = get_fuzzy_match_score(line, countries_list)

        if match_score or match_score1:
            score = match_score if match_score else match_score1
        elif not any(pattern.search(line) for pattern in compiled_patterns):
            filtered_lines.append(line)

    filtered_lines = [i for i in filtered_lines if i != 'در']
    arabic_list = []
    occupation = ''
    try:
        arabic_words = [word for word in filtered_lines if is_arabic(word) and ('الإسم' not in word and 'الاسم' not in word)]
        occupation = max(arabic_words, key=len)
        # occupation = arabic_words[0]
        
    except:
        try:
            occupation = extract_occupation_in_empty_case(ar_front_data)

            if len(occupation.split(' ')) > 3:
                occupation = ''

            if not is_arabic(occupation):
                occupation = extract_occupation_in_empty_case_v2(ar_front_data)
                
                if len(occupation.split(' ')) > 2:
                    occupation = ''
                
                if occupation:
                    occupation_en = GoogleTranslator(dest = 'en').translate(occupation)
                    if nationality.lower() in occupation_en.lower():
                        occupation = ''
                        try:
                            if 'المهنة' in third_part_text:
                                third_part_list = third_part_text.split('\n')
                                occupation = third_part_list[third_part_list.index('المهنة') - 1]
                                if occupation:
                                    occupation_en = GoogleTranslator(dest = 'en').translate(occupation)
                                    if nationality.lower() in occupation.lower() or nationality.lower() in occupation_en.lower():
                                        occupation = ''
                        except:
                            occupation = ''

        except Exception as e:
            try:
                ar_front_data_lines = ar_front_data.split('\n')
                occupation_line = next((line for line in ar_front_data_lines if 'المهنة' in line), None)
                occupation_index = ar_front_data_lines.index(occupation_line) + 1 if occupation_line else None
                occupation = ar_front_data_lines[occupation_index] if occupation_index and occupation_index < len(ar_front_data_lines) else ""
            except:
                occupation = ''

    if occupation:
        try:
            occupation_en = GoogleTranslator(dest = 'en').translate(occupation)
            if occupation_en and (occupation_en.startswith('Name') or occupation_en.startswith('Address') or occupation_en.lower().__contains__('e-wallet')):
                occupation, occupation_en = '', ''
                                  
        except:
            occupation_en = ''
    else:
        occupation, occupation_en = '', ''
    
    if extract_occupation_in_empty_case(ar_front_data) == '':
        occupation = ''
        occupation_en = ''

    # if 'Occupation' in ar_front_data or 'occupation' in ar_front_data:
    #      occupation = ''
    #      occupation_en = ''

    front_data = {
        # "name_raw": name,
        "nationality": nationality_iso,
        "id_number": id_number,
        "dob": dob,
        "expiry_date": expiry,
        # "occupation_ar": occupation,
        "occupation": occupation,
        "occupation_en": occupation_en
    }

    try:
        response_GenAI = genAI_for_occupation(front_data, model)
        if response_GenAI in( 'undetermined' , 'not_correct' , "'undetermined'", "'not_correct'"):
            english, arabic  = genAI_for_occupation_correct(ar_front_data, model)

            front_data = {
            # "name_raw": name,
            "nationality": nationality_iso,
            "id_number": id_number,
            "dob": dob,
            "expiry_date": expiry,
            #"occupation_ar": occupation,
            "occupation": arabic,
            "occupation_en": english
        }
            if (front_data['occupation_en'] == 'not_provided'):
                if front_data['occupation']:
                    occupation_en = GoogleTranslator(dest = 'en').translate(occupation)
                    front_data['occupation_en'] = occupation_en
                else:
                    front_data['occupation_en'] = ''

            if (front_data['occupation'] == 'not_provided'):
                front_data['occupation'] = ''
                
    except Exception as e:
        print(f"Error in GenAI: {e}")
        
    return front_data

def qatar_front_id_extraction(client, image_data, front_id_text, front_id_text_description, api_key):

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    except:
        model = None

    cropped_id_card, third_part, third_part_text = detect_id_card(client, image_data, front_id_text, part='third')
    front_data = extract_name_fields_from_cropped_part(third_part_text.replace("\n", ""))

    if not front_data.get('name', '') or not front_data.get('first_name', '') or not front_data.get('last_name', '') or len(front_data.get('name', '').split(' ')) <= 2:
        front_data_temp = extract_name_fields_from_cropped_part(front_id_text_description)
        front_data['name'] = front_data_temp.get('name', '')
        front_data['first_name'] = front_data_temp.get('first_name', '')
        front_data['last_name'] = front_data_temp.get('last_name', '') if len(front_data_temp.get('last_name', ''))>1 else ''

    name_ar = extract_name_ar(front_id_text_description)
    if name_ar:
        front_data["name_ar"] = name_ar
    else:
        front_data["name_ar"] = ''

    numeric_fields = extract_numeric_fields_from_raw(front_id_text_description, third_part_text, front_data.get('name', ''), model)

    front_data.update(numeric_fields)
    
    return front_data

def extract_employer_from_back(data, passport_number, passport_date, serial_no):
    patterns_to_remove = [r"\b[a-zA-Z0-9]+\b",
                          r"توقع حامل البطاقة",
                          r"مدير عام الجنسية والمنافذ وشؤون الوالدين",
                          r"المستقدم", r"توقع", r"حامل", r"البطاقة", r"مدير", r"عام", r"الإدارة", 
                          r"الجوازات", r"مدير عام الجنسية والمناقة وشؤون الوافدين",
                          r"صل", r"تاريخ النهاء الجواز", r"تاريخ", r"الجواز", r"البطاقة", r"توقع حامل البطاقة",
                          r"رق[ـم]* ج[ـوا]*ز السفر", r"تاريخ انتهاء ?الجواز", r"الرقم المسلسل", 
                          r"ن[ـو]*ع الرخص[ـة]*", r"مدير عام الإدارة العامة( للجوازات| الجورت)?", 
                          r"عمل",
                          r"الارة البا",
                          r"وزارة الله",
                          r"مدير عام الجنسية والمنافذ وشؤون الوافدين",
                          r"مدير إدارة الجنسية و وثائق السفر",
                          r"العنوان منطقة",
                          r"General Director of Nationality",
                          r"Borders & Expatriates Affairs",
                          r"Passport expiry date",
                           r"تاریخ انتهاء الجواز",
                          r"Drectorate of Passports",
                          r"Directorate of Passports",
                          r"Holder's Signature",
                          r"Authority's signature",
                          r"Residericy Type",
                          r"ترفيع حامل البطاقة", r"توقيع حامل البطاقة", r"passport_number|passport_date|serial_no", 
                          r"Holder's signature", r"Passport Number", r"Passport Expiry",
                          r"Serial No", r"Residency Type", r"Employer", r"Directorate of Passports",
                          r"General Director of the General", re.escape(passport_number), 
                          re.escape(passport_date), re.escape(serial_no), r":",
                        ]

    if 'employer' not in data.lower() or 'passport' not in data.lower():
        employer = ''
        return employer

    # compiled_patterns = [re.compile(pattern) for pattern in patterns_to_remove]
    compiled_patterns = [re.compile(pattern) for pattern in patterns_to_remove if pattern.strip()]
    data = data.replace("Employer", "").replace("Employe", "").replace("المستقدم :", "").replace("المستقدم", "")

    address_keywords = ["العنوان", "منطقة", "شارع"]
    lines = [
        line.strip() for line in data.split("\n")
        if line.strip() and not any(keyword in line for keyword in address_keywords)
    ]


    filtered_lines = []
    for line in lines:
        matched = False
        for pattern in compiled_patterns:
            if pattern.search(line):
                # print(f'Pattern: {pattern.pattern} matched line: {line}')
                matched = True
                break
        
        if not matched:
            filtered_lines.append(line)

    # print(f'FILTERED LINES: {filtered_lines}\n')
    
    lines = [re.sub(r'[A-Za-z0-9]', '', i) for i in filtered_lines]

    # print(f'FILTERED LINES 2: {lines}\n')

    try:
        employer = max(lines, key=len)
    except:
        employer = ''

    if employer:
        employer.strip().replace("'", '')
    else:
        employer = ''

    return employer


def qatar_back_id_extraction(back_id_text_description):
    serial_no_pattern = r"\b\d{14}\b|\b[A-Za-z0-9]{13,16}\b"
    passport_no_pattern = r"([A-Za-z]\d{8}|[A-Za-z]{2}\d{7}|[A-Za-z]\d{7}|[A-Za-z]\d{6})"
    # emp_pattern = r'Employer:\s*([\w\s.]+.)\n\b'

    serial_no_match = re.search(serial_no_pattern, back_id_text_description, re.IGNORECASE)
    
    try:
        if serial_no_match:
            serial_no = serial_no_match.group(0)
        else:
            serial_no = serial_no_match.group(1)
    except:
        serial_no = ''

    passport_no_match = re.search(passport_no_pattern, back_id_text_description, re.IGNORECASE)
    if passport_no_match:
        passport_no = passport_no_match.group(0)
    else:
        passport_no = ''

    dates = sort_dates_by_datetime(re.findall(r'\d{2}/\d{2}/\d{4}', back_id_text_description))
    passport_expiry = dates[0] if dates else ''

    try:
        back_id_text_description_original = back_id_text_description
        if 'Name' in back_id_text_description:
            back_id_text_description = back_id_text_description.split("Serial")[1]

        employer = extract_employer_from_back(back_id_text_description, passport_no, passport_expiry, serial_no)
        # print(f'Employer here 1: {employer}\n')

        if employer is None or employer == '':
            back_id_text_description_splitted_2 = back_id_text_description_original.split("Name")[1]
            employer = extract_employer_from_back(back_id_text_description_splitted_2, passport_no, passport_expiry, serial_no)
            # print(f'Employer here 2: {employer}\n')

        if not is_arabic(employer):
            employer = extract_employer_from_back(back_id_text_description, passport_no, passport_expiry, serial_no)
            # print(f'Employer here 3: {employer}\n')
    except:
        try:
            employer = extract_employer_from_back(back_id_text_description, passport_no, passport_expiry, serial_no)
            # print(f'Employer here 4: {employer}\n')
        except:
            employer = ''

    employer_en = ''
    if employer:
        try:
            employer_en = GoogleTranslator(dest = 'en').translate(employer)
            if employer_en and (employer_en.startswith('Director of the Nationality') or employer_en.startswith('Director of Nationality') or employer_en.startswith('Director General')) or employer_en == None:
                employer, employer_en = '', ''
        except:
            pass

    back_data = {
        "passport_number": passport_no,
        "passport_expiry": passport_expiry,
        "card_number": serial_no,
        "employer": str(employer),
        "employer_en": employer_en,
        "issuing_country": "QAT"
    }

    return back_data
