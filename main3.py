from symptoms import symptoms
from disease import Disease, all_diseases
import lib_gpt
from symptoms import list_all_symptoms



def find_key_by_symptom(symptom):
    for key, value in symptoms.items():
        for symptom_data in value['symptoms']:
            if symptom_data['sp'] == symptom:
                return key
    return None


def calc_probability(diseases, global_true_symptoms):
    for disease in diseases:
        count = 0
        for symptom in disease.symptoms:
            if symptom in global_true_symptoms:
                count += 1
                
            disease.probability = round(count / len(disease.symptoms) * 100)
        print(f"\nВероятность заболевания '{disease.name}': {disease.probability }%")

    # Сортируем список по убыванию вероятности и возвращаем первые 3
    return sorted(diseases, key=lambda x: x.probability, reverse=True)[:3]

def process_symptoms(key):
    new_list = []
    # Получаем данные по ключу
    data = symptoms[key]
    
    # Список симптомов
    symptoms_list = data['symptoms']
    
    # Вопросы к пользователю
    questions = data['questions']
    
    for question in questions:
     
        if question['type'] == 'yesno':
            answer = input(f"{question['text']} (да/нет): ").lower()
            if answer == 'да':
                for symptom in symptoms_list:
                    if symptom['id'] == question['id']:
                        symptom['res'] = True
                        new_list.append(symptom['sp'])
            elif question['id'] == '0':
                break
                
            
        elif question['type'] == 'float':
            value = float(input(f"{question['text']}: "))
            for symptom in symptoms_list:
                if symptom['id'] == question['id']:
                    if symptom['min'] < value <= symptom['max']:
                        symptom['res'] = True
                        new_list.append(symptom['sp'])
                        
        elif question['type'] == 'int':
            value = int(input(f"{question['text']}: "))
            for symptom in symptoms_list:
                if symptom['id'] == question['id']:
                    if symptom['min'] <= value <= symptom['max']:
                        symptom['res'] = True
                        new_list.append(symptom['sp'])
                        
        elif question['type'] == 'case':
            answer = input(f"{question['text']}: ")
            for symptom in symptoms_list:
                if symptom['id'] == question['id'] and symptom['answer'] == answer:
                    symptom['res'] = True
                    new_list.append(symptom['sp'])
    # sym = 
    return symptoms_list, new_list



def diagnose():

    initial_symptom_name = lib_gpt.get_answer_to_question_yandexGPT("какой симптом вас беспокоит?", input("какой симптом вас беспокоит?"), list_all_symptoms)
    
    # Поиск всех заболеваний с данным симптомом
    diseases_with_symptom = []
    global global_true_symptoms
    global_true_symptoms = []
    symptom_key_list = []
    for disease in all_diseases:
        if initial_symptom_name in disease.symptoms:
            diseases_with_symptom.append(disease)

    if not diseases_with_symptom:
        print(f"Симптом '{initial_symptom_name}' не соответствует ни одному заболеванию в базе данных.")
        return

    print(f"Возможные заболевания с симптомом '{initial_symptom_name}':")
    for disease in diseases_with_symptom:
        print(f" - {disease.name}")

    symptom_list =[]#создаем список симптомов
    first_symptom_key = find_key_by_symptom(initial_symptom_name)
    # print(f'ключ первого симптома {first_symptom_key}')
    if first_symptom_key is None:
        return
    answers, list_true_symptoms = process_symptoms(first_symptom_key)
    global_true_symptoms.extend(list_true_symptoms)
    symptom_list.append(answers)
    symptom_key_list.append(first_symptom_key)
    # print(f'для ключа - {first_symptom_key} получили список подтвержденных симптомов {global_true_symptoms}')
    
    
    print(f'Начинаем формировать список ключей симптомов для проверки') 
    
    for disease in diseases_with_symptom:
        for _symptom in disease.symptoms:
            symptom_key = find_key_by_symptom(_symptom)
            # print(f"Диагноз - {disease.name}, симптом - {symptom_key}")
            if symptom_key not in symptom_key_list:
                symptom_key_list.append(symptom_key)
                
            
    # print (f'получился список симптомов для проверки - {symptom_key_list}')
    symptom_key_list.remove(first_symptom_key)
    # print (f'удалили ключ первого симптома - {first_symptom_key}, получился список симптомов для проверки - {symptom_key_list}')
    
    for symptom_key in symptom_key_list:
        answers, list_true_symptoms = process_symptoms(symptom_key)
        global_true_symptoms.extend(list_true_symptoms)
        symptom_list.append(answers)
        # print (f'Для симптома - {symptom_key}, получили список значений пользователя - {answers}, получили список имеющихся у пациентов симптомов - {global_true_symptoms}')
    
    
            


    # получаем 3 наиболее вероятных заболеванияслабость
    top_three_diseases = calc_probability(diseases_with_symptom, global_true_symptoms)   

    # Выводим результаты
    for disease in top_three_diseases:
        print(f'{disease.name}: {disease.probability}')

diagnose()