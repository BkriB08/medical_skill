import random


GlobalDict = {}

# GlobalDict['вопрос, слышат ли нас'] = [
#     {'text':'Вы меня слышите? Мы можем поговорить?', 
#      'tts':'Вы меня слышите? Мы можем поговорить?'},

#     {'text':'Вы здесь? Уделите мне минуту?', 
#      'tts':'Вы здесь? Уделите мне минуту?'},

#     {'text':'Могу я ейчас задать Вам несколько вопросов?', 
#      'tts':'Могу я ейчас задать Вам несколько вопросов?'},
# ]

# GlobalDict['Сообщаем, что переходим к следующему пользователю'] = [
#     {'text':'Чтож, дайте мне еще попытку', 
#      'tts':'Чтож, дайте мне еще попытку'},
#     {'text':'Давайте попробуем еще раз', 
#      'tts':'Давайте попробуем еще раз'},
# ]



GlobalDict['название'] = [
    {'text':'сообщение', 
     'tts':'сообщение'},
]


GlobalDict['название'] = [
    {'text':'сообщение', 
     'tts':'сообщение'},
]


GlobalDict['название'] = [
    {'text':'сообщение', 
     'tts':'сообщение'},
]


GlobalDict['название'] = [
    {'text':'сообщение', 
     'tts':'сообщение'},
]


GlobalDict['название'] = [
    {'text':'сообщение', 
     'tts':'сообщение'},
]


GlobalDict['название'] = [
    {'text':'сообщение', 
     'tts':'сообщение'},
]


GlobalDict['название'] = [
    {'text':'сообщение', 
     'tts':'сообщение'},
]


def text_generation(key, incoming_text):
    text = incoming_text
    tts = incoming_text   


    if key in GlobalDict:
        count = len(GlobalDict[key])
        tec = random.randint(0, count - 1)
        if 'text' in GlobalDict[key][tec]:
            text = GlobalDict[key][tec]['text']
            if 'tts' in GlobalDict[key][tec]:
                tts = GlobalDict[key][tec]['tts']
            else:
                tts = text

        # print (f'********генерируем фразу')
        # print (f'поступил ключ {key} и фраза по умолчанию {incoming_text}')
        # print (f'для такого ключа у нас заготовлены фразы {GlobalDict[key]}. Всего количество {count}, мы выбираем номер {tec}')
        print (f'итого возвращаем  text = {text}.  tts=  {tts}')
    
 
    return text, tts









    #val_enegry_received = request.body_energy ["kkal"]
    '''
    if 'breakfast' in request.body_energy:
        print(f'Готовимся спросить Гигачат о количестве калориев за завтрак')
        val_enegry_received += service_library.get_kkal_from_gigachat(request.body_energy['breakfast'])
        print(f'Получили количество калориев за завтрак =  { val_enegry_received}')

    if 'lunch' in request.body_energy:
        val_enegry_received += service_library.get_kkal_from_gigachat(request.body_energy['lunch'])

    if 'dinner' in request.body_energy:
        val_enegry_received += service_library.get_kkal_from_gigachat(request.body_energy['dinner'])
    
    
    #Для мужчин основной обмен = 88.362 + (13.397 x вес в кг) + (4.799 x рост в сантиметрах) - (5.677 x возраст в годах).

    #Для женщин основной обмен = 447.593 + (9.247 x вес в кг) + (3.098 x рост в сантиметрах) - (4.330 x возраст в годах).

    energy_spent = 1200
    
    if 'steps' in request.body_energy:
        energy_spent += request.body_energy ["steps"] * 0.04

    if 'sport' in request.body_energy:
        if request.body_energy ["sport"]:
            energy_spent += 500
    '''


    text = f'Вы потребили около {val_enegry_received} калорий. С учетом Вашей подвижности потрачено {energy_spent} калорий. '
    if val_enegry_received - energy_spent > 0:
        text += f'Избыток потребленной энергии составил { val_enegry_received - energy_spent} калорий'
    else:
        text += f'Дефицит энергии составил { val_enegry_received - energy_spent} калорий'
        
    return text, text