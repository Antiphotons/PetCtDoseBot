import telebot
from telebot import types
# from random import choice  # will part of later implementation

token = ''  # insert your token

bot = telebot.TeleBot(token)


# Check the string consist of float value or not

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# Check and replace if phantom 16 cm set for inappropriate anatomy in adults

def phantom_check():
    if age["years"] >= 18 \
    and ct["anatomy"] not in [['Head'], ['Neck'], ['Head', 'Neck']] \
    and ct['phantom'] == 16:
        ct['phantom'] = 32
        return f'''
        Фантом 32 см установлен в соответствии с возрастом {age["years"]}
        и зоной сканирования {ct["anatomy"]}.
        '''
    else: return ''


# Display parameters (change options will be implemented in later versions)

language = 'Russian'
activity_units = 'мКи'
dose_units = 'мЗв'

# Scan parameters
# Anatomical zones of CT scan: English – Russian

anatomy = {'Head': 'Голова', 'Neck': 'Шея', 'Thorax': 'Грудная клетка',
           'Abdomen': 'Брюшная полость', 'Pelvis': 'Малый таз', 'Legs': 'Ноги'}

residual_anatomy = anatomy.copy()  # variable for anatomy buttons generation


# Coefficients for DLP -> effective dose computation
# 16 cm phantom (head, neck and pediatric)

ct_coef_16_infant = {
    'Head': 0.0059, 'Neck': 0.022, 'Head, Neck': 0.0078, 'Thorax': 0.026,
    'Abdomen': 0.031, 'Pelvis': 0.034, 'Legs': 0.0015, 'Thorax, Abdomen': 0.028,
    'Abdomen, Pelvis': 0.032, 'Thorax, Abdomen, Pelvis': 0.03,
    'Whole body': 0.019
    }
ct_coef_16_2 = {
    'Head': 0.0048, 'Neck': 0.018, 'Head, Neck': 0.0066, 'Thorax': 0.02,
    'Abdomen': 0.024, 'Pelvis': 0.027, 'Legs': 0.00099,
    'Thorax, Abdomen': 0.022, 'Abdomen, Pelvis': 0.026,
    'Thorax, Abdomen, Pelvis': 0.024, 'Whole body': 0.016
    }
ct_coef_16_7 = {
    'Head': 0.0035, 'Neck': 0.013, 'Head, Neck': 0.0051, 'Thorax': 0.014,
    'Abdomen': 0.017, 'Pelvis': 0.019, 'Legs': 0.00055,
    'Thorax, Abdomen': 0.016, 'Abdomen, Pelvis': 0.018,
    'Thorax, Abdomen, Pelvis': 0.017, 'Whole body': 0.013
    }
ct_coef_16_12 = {
    'Head': 0.0027, 'Neck': 0.011, 'Head, Neck': 0.0043, 'Thorax': 0.011,
    'Abdomen': 0.013, 'Pelvis': 0.014, 'Legs': 0.00036,
    'Thorax, Abdomen': 0.012, 'Abdomen, Pelvis': 0.014,
    'Thorax, Abdomen, Pelvis': 0.013, 'Whole body': 0.012
    }
ct_coef_16_17 = {
    'Head': 0.0018, 'Neck': 0.0073, 'Head, Neck': 0.003, 'Thorax': 0.0069,
    'Abdomen': 0.0079, 'Pelvis': 0.0087, 'Legs': 0.00016,
    'Thorax, Abdomen': 0.0073, 'Abdomen, Pelvis': 0.0083,
    'Thorax, Abdomen, Pelvis': 0.0078, 'Whole body': 0.0087
    }
ct_coef_16_adult = {
    'Head': 0.0014, 'Neck': 0.006, 'Head, Neck': 0.0025
    }
ct_coefficients_16 = {
    'inf': ct_coef_16_infant, '0.6-2': ct_coef_16_2, '3-7': ct_coef_16_7,
    '8-12': ct_coef_16_12, '13-17': ct_coef_16_17, 'adult': ct_coef_16_adult
    }

# 32 cm phantom (body-only)

ct_coef_32_infant = {
    'Thorax': 0.059, 'Abdomen': 0.072, 'Pelvis': 0.077, 'Legs': 0.0027,
    'Thorax, Abdomen': 0.065, 'Abdomen, Pelvis': 0.075,
    'Thorax, Abdomen, Pelvis': 0.069, 'Whole body': 0.043
    }
ct_coef_32_2 = {
    'Thorax': 0.047, 'Abdomen': 0.056, 'Pelvis': 0.06, 'Legs': 0.0018,
    'Thorax, Abdomen': 0.051, 'Abdomen, Pelvis': 0.059,
    'Thorax, Abdomen, Pelvis': 0.054, 'Whole body': 0.038
    }
ct_coef_32_7 = {
    'Thorax': 0.033, 'Abdomen': 0.039, 'Pelvis': 0.042, 'Legs': 0.001,
    'Thorax, Abdomen': 0.036, 'Abdomen, Pelvis': 0.041,
    'Thorax, Abdomen, Pelvis': 0.038, 'Whole body': 0.031
    }
ct_coef_32_12 = {
    'Thorax': 0.026, 'Abdomen': 0.03, 'Pelvis': 0.033, 'Legs': 0.00068,
    'Thorax, Abdomen': 0.028, 'Abdomen, Pelvis': 0.031,
    'Thorax, Abdomen, Pelvis': 0.029, 'Whole body': 0.027
    }
ct_coef_32_17 = {
    'Thorax': 0.016, 'Abdomen': 0.018, 'Pelvis': 0.02, 'Legs': 0.0003,
    'Thorax, Abdomen': 0.017, 'Abdomen, Pelvis': 0.019,
    'Thorax, Abdomen, Pelvis': 0.018, 'Whole body': 0.02
    }
ct_coef_32_adult = {
    'Thorax': 0.012, 'Abdomen': 0.014, 'Pelvis': 0.015, 'Legs': 0.0002,
    'Thorax, Abdomen': 0.013, 'Abdomen, Pelvis': 0.015,
    'Thorax, Abdomen, Pelvis': 0.014, 'Whole body': 0.017
    }
ct_coefficients_32 = {
    'inf': ct_coef_32_infant, '0.6-2': ct_coef_32_2, '3-7': ct_coef_32_7,
    '8-12': ct_coef_32_12, '13-17': ct_coef_32_17, 'adult': ct_coef_32_adult
    }


# Tracers and dose coefficients
# Age-corrected coefficients for tracers

fdg = {'inf': 0.095, '3-7': 0.05, '8-12': 0.036, '13-17': 0.025, 'adult': 0.019}
methionine = {'inf': 0.047, '3-7': 0.026, '8-12': 0.017, '13-17': 0.011,
'adult': 0.0084}
fet = {'inf': 0.082, '3-7': 0.047, '8-12': 0.031, '13-17': 0.021,
'adult': 0.0165}
fdopa = {'inf': 0.1, '3-7': 0.07, '8-12': 0.049, '13-17': 0.032, 'adult': 0.025}
wather = {'inf': 0.0077, '3-7': 0.0038, '8-12': 0.0023, '13-17': 0.0014,
'adult': 0.0011}
ammonia = {'inf': 0.011, '3-7': 0.0067, '8-12': 0.0036, '13-17': 0.0024,
'adult': 0.002}
naf = {'inf': 0.11, '3-7': 0.056, '8-12': 0.033, '13-17': 0.02, 'adult': 0.017}
flucholine = {'inf': 0.1, '3-7': 0.057, '8-12': 0.037, '13-17': 0.024,
'adult': 0.02}

# Dictionary with coefficient dictionaries

tracers = {'18F-FDG': fdg, '11C-methionine': methionine, '18F-FET': fet,
'18F-FDOPA': fdopa, '18F-NaF': naf, '13N-NH3': ammonia, '15O-H2O': wather,
'18F-choline': flucholine}

# half life periods

halflife = {'18F-FDG': 6588, '11C-methionine': 1220, '18F-FET': 6588,
'18F-FDOPA': 6588, '18F-NaF': 6588, '13N-NH3': 598, '15O-H2O': 120,
'18F-choline': 6588}


# Baseline scan characteristics

age = {'years': 33}  # patient age

# CT scan parameters

ct = {
    'modality': True,  # CT scan presence
    'dlp': 1488,  # Dose-Length Product
    'phantom': 16,  # Protocol phantom settings for CTDI computation
    'anatomy': ['Head']  # Anatomical zones
}

# PET scan parameters

pet = {
    'modality': True,  # PET scan presence
    'tracer': '18F-FDG',  # radiotracer name
    'activity_full': 14.88,  # measured filled suringe radioactivity
    'time_full': '00 00',  # time of full surringe measurement
    'time_inject': '00 00',  # time of radioactivity administration
    'time_empty': '00 00',  # time of empty surringe measurement
    'activity_empty': 0.25 # measured empty suringe radioactivity
}


def scan_parameters():
    scan_report = 'ПАРАМЕТРЫ СКАНИРОВАНИЯ' + '\n' \
        + f'Возраст: {age["years"]}' + '\n' \
        + f'DLP: {ct["dlp"]} мГр x см' + '\n' \
        + f'Phantom: {ct["phantom"]} см' + '\n' \
        + f'Области обследования: {", ".join(ct["anatomy"])}' + '\n' \
        + f'РФП: {pet["tracer"]}' + '\n' \
        + f'Активность в полном шприце: {pet["activity_full"]} {activity_units}' + '\n' \
        + f'Время измерения: {pet["time_full"]}' + '\n' \
        + f'Время введения: {pet["time_inject"]}' + '\n' \
        + f'Время измерения пустого шприца: {pet["time_empty"]}' + '\n' \
        + f'Активность в пустом шприце {pet["activity_empty"]} {activity_units}'
    return scan_report


menu = '''
Список доступных команд:
/start – начать ввод параметров сканирования
/dose_report – вывести на экран текущую лучевую нагрузку пациента
/settings – настройки языка и единиц измерения
/help - справка и доступные команды
'''


# Settings command -> message

@bot.message_handler(commands=['settings'])
def settings(message):
    bot.send_message(message.chat.id, \
    '''
    Опция временно недоступна, приносим извинения.
    Бот развивается. Идут строительные работы
    ''')


# Menu command -> message

@bot.message_handler(commands=['menu', 'help'])
def help(message):
    bot.send_message(message.chat.id, menu)


# Start command -> message and keyboard display

@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Возраст', 'Параметры КТ', 'Параметры ПЭТ', 'Лучевая нагрузка')
    msg = bot.reply_to(message, \
    'Введите параметры сканирования или сгенерируйте отчет', \
    reply_markup=markup)
    bot.register_next_step_handler(msg, start_process)


# Start commands routing

def start_process(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    if message.text == 'Возраст':
        msg = bot.reply_to(message, 'Введите возраст пациента:')
        bot.register_next_step_handler(msg, set_age)
    elif message.text == 'Параметры КТ':
        markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
        msg = bot.reply_to(message, 'Выберите, какой параметр изменить', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, ct_select)
    elif message.text == 'Параметры ПЭТ':
        markup.add('ПЭТ-скан', 'РФП', 'Активность', 'Время измерения', 'Назад')
        msg = bot.reply_to(message, 'Выберите, какой параметр изменить', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, pet_select)
    elif message.text == 'Лучевая нагрузка':
        add_msg = phantom_check()  # auto-set 32 cm phantom for adults
        scan_report = scan_parameters()  # generate scan parameters report
        markup.add('Продолжить', 'Изменить параметры')
        msg = bot.reply_to(message, add_msg + '\n' + scan_report, \
        reply_markup=markup)
        bot.register_next_step_handler(msg, display_report)


# Age change, message display and return to start menu keyboard

def set_age(message):
    new_age = message.text
    if not is_float(new_age):
        msg = bot.reply_to(message, \
        'Возраст должен быть числом. Введите возраст:')
        bot.register_next_step_handler(msg, set_age)
    else:
        if float(new_age) < 1: age["years"] = round(float(new_age), 1)
        else: age["years"] = round(float(new_age) // 1)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Возраст', 'Параметры КТ', 'Параметры ПЭТ', 'Лучевая нагрузка')
        msg = bot.reply_to(message, f'Установлен возраст {age["years"]}', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, start_process)


# CT parameter selection process

def ct_select(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    if message.text == 'КТ-скан':
        markup.add('ВКЛЮЧИТЬ КТ', 'ВЫКЛЮЧИТЬ КТ')
        msg = bot.reply_to(message, 'Выполнялось ли КТ сканирование?', reply_markup=markup)
        bot.register_next_step_handler(msg, set_ct_scan)
    elif message.text == 'Фантом':
        markup.add('16 см', '32 см')
        msg = bot.reply_to(message, \
        'Выберите тип фантома, указанный в настройках протокола сканирования', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, set_phantom_scan)
    elif message.text == 'DLP':
        msg = bot.reply_to(message, 'Введите DLP:')
        bot.register_next_step_handler(msg, set_dlp)
    elif message.text == 'Анатомические зоны':
        markup.add('Голова', 'Все тело', 'Другие зоны')
        msg = bot.reply_to(message, 'Выберите область сканирования:', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, select_anatomy)
    elif message.text == 'Назад':

        # auto-set 16 cm phantom for head and neck
        add_msg = ''
        if ct['anatomy'] in [['Head'], ['Neck'], ['Head', 'Neck']] \
        and ct['phantom'] == 32:
            ct['phantom'] = 16
            add_msg = 'Фантом 16 см установлен в соответствии с зоной сканирования'

        markup.add('Возраст', 'Параметры КТ', 'Параметры ПЭТ', 'Лучевая нагрузка')
        msg = bot.reply_to(message, add_msg + '\n' + \
        'Введите параметры сканирования или сгенерируйте отчет', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, start_process)
    else:
        markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
        msg = bot.reply_to(message, \
        'Используйте предлагаемые варианты настроек', reply_markup=markup)
        bot.register_next_step_handler(msg, ct_select)


# Enable or disable CT modality

def set_ct_scan(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
    if message.text == 'ВЫКЛЮЧИТЬ КТ':
        ct['modality'] = False
        msg = bot.reply_to(message, 'Модальность КТ отключена', \
        reply_markup=markup)
    elif message.text == 'ВКЛЮЧИТЬ КТ':
        ct['modality'] = True
        msg = bot.reply_to(message, 'Модальность КТ включена', \
        reply_markup=markup)
    bot.register_next_step_handler(msg, ct_select)


# Switch the CTDI phantom type

def set_phantom_scan(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
    if message.text == '16 см':
        ct['phantom'] = 16
        msg = bot.reply_to(message, \
        'Установлен фантом 16 см (голова, шея и педиатрические исследования)', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, ct_select)
    elif message.text == '32 см':
        ct['phantom'] = 32
        msg = bot.reply_to(message, 'Установлен фантом 32 см', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, ct_select)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('16 см', '32 см')
        msg = bot.reply_to(message, \
        'Используйте предлагаемые варианты фантомов', reply_markup=markup)
        bot.register_next_step_handler(msg, set_phantom_scan)


# DLP change and message display

def set_dlp(message):
    new_dlp = message.text
    if not is_float(new_dlp):
        msg = bot.reply_to(message, 'DLP должен быть числом. Введите DLP:')
        bot.register_next_step_handler(msg, set_dlp)
    else:
        ct["dlp"] = round(float(new_dlp), 2)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
        msg = bot.reply_to(message, f'Установлен DLP {ct["dlp"]}', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, ct_select)


# Set Head or Whole body zones or display detalized variants

def select_anatomy(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    if message.text == 'Голова':
        ct['anatomy'] = ['Head']
        ct['phantom'] = 16
        markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
        msg = bot.reply_to(message, 'Выбрана анатомическая область "Голова"' \
        + '\n' + 'Установлен фантом 16 см', reply_markup=markup)
        bot.register_next_step_handler(msg, ct_select)
    elif message.text == 'Все тело':
        ct['anatomy'] = ['Whole body']
        ct['phantom'] = 32
        markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
        msg = bot.reply_to(message, 'Выбрана анатомическая область "Все тело"' \
        + '\n' + 'Установлен фантом 32 см (может быть изменено)', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, ct_select)
    elif message.text == 'Другие зоны':
        ct['anatomy'] = []
        global residual_anatomy
        residual_anatomy = anatomy.copy()
        for zone in residual_anatomy:
            markup.add(residual_anatomy[zone])
        markup.add('Выход')
        msg = bot.reply_to(message, \
        'Выберите интересущие анатомические области', reply_markup=markup)
        bot.register_next_step_handler(msg, select_special_anatomy)
    else:
        markup.add('Голова', 'Все тело', 'Другие зоны')
        msg = bot.reply_to(message, \
        'Используйте предлагаемые варианты областей', reply_markup=markup)
        bot.register_next_step_handler(msg, select_anatomy)


# Set and additionaly request detalized anatomy

def select_special_anatomy(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    if message.text == 'Выход':

        # Sort ct[anatomy]
        anat_templ = [z for z in anatomy]  # sorted template anatomy list
        anat_sort = sorted(ct['anatomy'], key=lambda x: anat_templ.index(x))
        ct['anatomy'] = anat_sort.copy()

        # Whole body auto-replacement
        if ct['anatomy'] == ['Head', 'Neck', 'Thorax', 'Abdomen', 'Pelvis']:
            ct['anatomy'] = ['Whole body']

        # Unsupported anatomy warning and return
        if ', '.join(ct['anatomy']) not in [z for z in ct_coef_16_infant]:
            markup.add('Голова', 'Все тело', 'Другие зоны')
            msg = bot.reply_to(message, \
            'Выбраны неподдерживаемые анатомические области.' + '\n' + \
            'Скорректируйте области. Подробнее: меню /help', \
            reply_markup=markup)
            bot.register_next_step_handler(msg, select_anatomy)
        else:
            markup.add('КТ-скан', 'Фантом', 'DLP', 'Анатомические зоны', 'Назад')
            msg = bot.reply_to(message, \
            f'Установлены области: {", ".join(ct["anatomy"])}', \
            reply_markup=markup)
            bot.register_next_step_handler(msg, ct_select)
    else:
        for zone in residual_anatomy:
            if message.text == residual_anatomy[zone]:
                ct['anatomy'].append(zone)
                residual_anatomy.pop(zone, None)
                for res_zone in residual_anatomy:
                    markup.add(residual_anatomy[res_zone])
                markup.add('Выход')
                msg = bot.reply_to(message, \
                f'Добавлена анатомическая область: {anatomy[zone]}', \
                reply_markup=markup)
                bot.register_next_step_handler(msg, select_special_anatomy)
                break
            elif message.text not in [residual_anatomy[z] for z in residual_anatomy]:
                for res_zone in residual_anatomy:
                    markup.add(residual_anatomy[res_zone])
                markup.add('Выход')
                msg = bot.reply_to(message, \
                f'Используйте предлагаемые варианты областей {residual_anatomy}', reply_markup=markup)
                bot.register_next_step_handler(msg, select_special_anatomy)


# PET parameter selection process

def pet_select(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    if message.text == 'ПЭТ-скан':
        markup.add('ВКЛЮЧИТЬ ПЭТ', 'ВЫКЛЮЧИТЬ ПЭТ')
        msg = bot.reply_to(message, 'Выполнялось ли ПЭТ сканирование?', reply_markup=markup)
        bot.register_next_step_handler(msg, set_pet_scan)
    elif message.text == 'Активность':
        markup.add('В полном шприце', 'В пустом шприце')
        msg = bot.reply_to(message, 'Выберите тип измерения', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, select_activity)
    elif message.text == 'Время измерения':
        markup.add('В полном шприце', 'Время введения', 'В пустом шприце', 'Назад')
        msg = bot.reply_to(message, 'Выберите время измерения', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, select_time)
    elif message.text == 'РФП':
        for tracer in tracers:
            markup.add(tracer)
        msg = bot.reply_to(message, 'Выберите РФП:', reply_markup=markup)
        bot.register_next_step_handler(msg, set_tracer)
    elif message.text == 'Назад':
        markup.add('Возраст', 'Параметры КТ', 'Параметры ПЭТ', 'Лучевая нагрузка')
        msg = bot.reply_to(message, \
        'Введите параметры сканирования или сгенерируйте отчет', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, start_process)
    else:
        markup.add('ПЭТ-скан', 'РФП', 'Активность', 'Время измерения', 'Назад')
        msg = bot.reply_to(message, \
        'Используйте предлагаемые варианты настроек', reply_markup=markup)
        bot.register_next_step_handler(msg, pet_select)


# Enable or disable PET modality

def set_pet_scan(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('ПЭТ-скан', 'РФП', 'Активность', 'Время измерения', 'Назад')
    if message.text == 'ВЫКЛЮЧИТЬ ПЭТ':
        pet['modality'] = False
        msg = bot.reply_to(message, 'Модальность ПЭТ отключена', \
        reply_markup=markup)
    elif message.text == 'ВКЛЮЧИТЬ ПЭТ':
        pet['modality'] = True
        msg = bot.reply_to(message, 'Модальность ПЭТ включена', \
        reply_markup=markup)
    bot.register_next_step_handler(msg, pet_select)


# Change radiopharmaceutical and message display

def set_tracer(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('ПЭТ-скан', 'РФП', 'Активность', 'Время измерения', 'Назад')
    if message.text in tracers:
        pet["tracer"] = message.text
        msg = bot.reply_to(message, f'Установлен РФП: {pet["tracer"]}', \
        reply_markup=markup)
    else:
        msg = bot.reply_to(message, 'Недопустимый РФП', reply_markup=markup)
    bot.register_next_step_handler(msg, pet_select)


# Select the Activity type

def select_activity(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Назад')
    if message.text == 'В полном шприце':
        msg = bot.reply_to(message, \
        'Введите значение радиоактивности в полном шприце', reply_markup=markup)
        bot.register_next_step_handler(msg, set_activity_full)
    elif message.text == 'В пустом шприце':
        msg = bot.reply_to(message, \
        'Введите значение радиоактивности в пустом шприце', reply_markup=markup)
        bot.register_next_step_handler(msg, set_activity_empty)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('В полном шприце', 'В пустом шприце')
        msg = bot.reply_to(message, \
        'Используйте предлагаемые варианты', reply_markup=markup)
        bot.register_next_step_handler(msg, select_activity)


# Full suringe activity change and message display

def set_activity_full(message):
    new_act = message.text
    if not is_float(new_act):
        msg = bot.reply_to(message, \
        'Активность должна быть числом. Введите активность:')
        bot.register_next_step_handler(msg, set_activity_full)
    else:
        pet["activity_full"] = round(float(new_act), 2)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('ПЭТ-скан', 'РФП', 'Активность', 'Время измерения', 'Назад')
        msg = bot.reply_to(message, \
        f'Установлена активность в полном шприце {pet["activity_full"]} {activity_units}', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, pet_select)


# Empty suringe activity change and message display

def set_activity_empty(message):
    new_act = message.text
    if not is_float(new_act):
        msg = bot.reply_to(message, \
        'Активность должна быть числом. Введите активность:')
        bot.register_next_step_handler(msg, set_activity_empty)
    else:
        pet["activity_empty"] = round(float(new_act), 2)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('ПЭТ-скан', 'РФП', 'Активность', 'Время измерения', 'Назад')
        msg = bot.reply_to(message, \
        f'Установлена активность в пустом шприце {pet["activity_empty"]} {activity_units}', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, pet_select)


# Select the time of measurement type

def select_time(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Назад')
    if message.text == 'В полном шприце':
        msg = bot.reply_to(message, \
        'Укажите время измерения активности в полном шприце – ' + '\n' + \
        'часы и минуты через пробел (чч мм):', reply_markup=markup)
        bot.register_next_step_handler(msg, set_time_full)
    elif message.text == 'Время введения':
        msg = bot.reply_to(message, \
        'Укажите время введения РФП – часы и минуты через пробел (чч мм):', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, set_time_inject)
    elif message.text == 'В пустом шприце':
        msg = bot.reply_to(message, \
        'Введите время измерения активности в пустом шприце – ' + '\n' + \
        'часы и минуты через пробел (чч мм):', reply_markup=markup)
        bot.register_next_step_handler(msg, set_time_empty)
    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('ПЭТ-скан', 'РФП', 'Активность', 'Время измерения', 'Назад')
        msg = bot.reply_to(message, 'Выберите, какой параметр изменить', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, pet_select)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('В полном шприце', 'Время введения', 'В пустом шприце', 'Назад')
        msg = bot.reply_to(message, \
        'Используйте предлагаемые варианты', reply_markup=markup)
        bot.register_next_step_handler(msg, select_activity)


# Full suringe measurement time change and message display

def set_time_full(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('В полном шприце', 'Время введения', 'В пустом шприце', 'Назад')
    if message.text == 'Назад':
        msg = bot.reply_to(message, 'Выберите время измерения', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, select_time)
    else:
        time = message.text.split(' ')
        flag = True
        for t in time:
            if not t.isdigit():
                flag = False
                break
        if flag:
            pet["time_full"] = message.text
            msg = bot.reply_to(message, \
            f'''Установлено время измерения активности в полном шприце:
            {pet["time_full"]}''', \
            reply_markup=markup)
            bot.register_next_step_handler(msg, select_time)
        else:
            msg = bot.reply_to(message, \
            'Недопустимый формат ввода. Попробуйте еще раз (чч мм):')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Назад')
            bot.register_next_step_handler(msg, set_time_full)


# Administration measurement time change and message display

def set_time_inject(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('В полном шприце', 'Время введения', 'В пустом шприце', 'Назад')
    if message.text == 'Назад':
        msg = bot.reply_to(message, 'Выберите время измерения', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, select_time)
    else:
        time = message.text.split(' ')
        flag = True
        for t in time:
            if not t.isdigit():
                flag = False
                break
        if flag:
            pet["time_inject"] = message.text
            msg = bot.reply_to(message, \
            f'''Установлено время введения:
            {pet["time_inject"]}''', \
            reply_markup=markup)
            bot.register_next_step_handler(msg, select_time)
        else:
            msg = bot.reply_to(message, \
            'Недопустимый формат ввода. Попробуйте еще раз (чч мм):')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Назад')
            bot.register_next_step_handler(msg, set_time_inject)


# Empty suringe measurement time change and message display

def set_time_empty(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('В полном шприце', 'Время введения', 'В пустом шприце', 'Назад')
    if message.text == 'Назад':
        msg = bot.reply_to(message, 'Выберите время измерения', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, select_time)
    else:
        time = message.text.split(' ')
        flag = True
        for t in time:
            if not t.isdigit():
                flag = False
                break
        if flag:
            pet["time_empty"] = message.text
            msg = bot.reply_to(message, \
            f'''Установлено время измерения активности в пустом шприце:
            {pet["time_empty"]}''', \
            reply_markup=markup)
            bot.register_next_step_handler(msg, select_time)
        else:
            msg = bot.reply_to(message, \
            'Недопустимый формат ввода. Попробуйте еще раз (чч мм):')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Назад')
            bot.register_next_step_handler(msg, set_time_empty)


# Compute doses, generate and print dose report

@bot.message_handler(commands=['dose_report'])
def display_scan_parameters(message):
    add_msg = phantom_check()  # auto-set 32 cm phantom for adults
    scan_report = scan_parameters()  # generate scan parameters report
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Продолжить', 'Изменить параметры')
    msg = bot.reply_to(message, add_msg + '\n' + scan_report, \
    reply_markup=markup)
    bot.register_next_step_handler(msg, display_report)


def display_report(message):
    if message.text == 'Изменить параметры':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Возраст', 'Параметры КТ', 'Параметры ПЭТ', 'Лучевая нагрузка')
        msg = bot.reply_to(message, \
        'Введите параметры сканирования или сгенерируйте отчет', \
        reply_markup=markup)
        bot.register_next_step_handler(msg, start_process)
    elif message.text == 'Продолжить':

        # Derive dose coefficients
        # Age category

        if age["years"] <= 0.5: ct_age_cat, pet_age_cat = 'inf', 'inf'
        elif age["years"] <= 2: ct_age_cat, pet_age_cat = '0.6-2', 'inf'
        elif age["years"] <= 7: ct_age_cat, pet_age_cat = '3-7', '3-7'
        elif age["years"] <= 12: ct_age_cat, pet_age_cat = '8-12', '8-12'
        elif age["years"] <= 17: ct_age_cat, pet_age_cat = '13-17', '13-17'
        else: ct_age_cat, pet_age_cat = 'adult', 'adult'

        # CT dose coefficient

        if ct['phantom'] == 16: ct_coefficients = ct_coefficients_16[ct_age_cat]
        elif ct['phantom'] == 32: ct_coefficients = ct_coefficients_32[ct_age_cat]
        ct_coeff = ct_coefficients[", ".join(ct['anatomy'])]

        # PET dose coefficient

        pet_coefficients = tracers[pet["tracer"]]
        pet_coeff = 37 * pet_coefficients[pet_age_cat]

        # PET decay correction

        time_full = pet['time_full'].split(' ')
        minutes_full = int(time_full[0]) * 60 + int(time_full[1])
        time_inject = pet['time_inject'].split(' ')
        minutes_inject = int(time_inject[0]) * 60 + int(time_inject[1])
        time_empty = pet['time_empty'].split(' ')
        minutes_empty = int(time_empty[0]) * 60 + int(time_empty[1])
        minutes_halflife = halflife[pet["tracer"]] / 60
        full_decay = 2 ** ((minutes_full - minutes_inject) / minutes_halflife)
        empty_decay = 2 ** ((minutes_empty - minutes_inject) / minutes_halflife)

        # Compute parameters for dose report

        if pet['modality']:
            injected_activity = round(pet["activity_full"] * full_decay \
            - pet["activity_empty"] * empty_decay, 2)
            pet_dose = round(injected_activity * pet_coeff, 2)
        else: injected_activity, pet_dose = 0, 0

        if ct['modality']: ct_dose = round(ct["dlp"] * ct_coeff, 2)
        else: ct_dose = 0

        full_dose = round(ct_dose + pet_dose, 2)  # compute summarize dose

        dose_report = 'РАСЧЕТНЫЕ ПАРАМЕТРЫ' + '\n' \
                + f'Введенная радиоактивность: {injected_activity} {activity_units}' \
                + '\n' \
                + f'Лучевая нагрузка КТ: {ct_dose} {dose_units}' + '\n' \
                + f'Лучевая нагрузка ПЭТ: {pet_dose} {dose_units}' + '\n' \
                + f'Общая лучевая нагрузка: {full_dose} {dose_units}'

        bot.send_message(message.chat.id, dose_report)


bot.polling(none_stop=True)