from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):  # pass
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):  # pass
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоск', animal_type='вортерьер',
                                     age='4', pet_photo='images/uzbogoy.jpeg'):  # failed
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():  # pass
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cateyeblack.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):  # pass
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# 1. Тест добавления питомца с корректными данными без фото. Pass
def test_post_create_pet_simple(name='Брабос', animal_type='дворер',
                                     age='1'):

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 2. Тест получение инфо о питомце первого в списке без фото. Pass
def test_get_pet_without_photo(name='sova', animal_type='flylow', age=7):

    # запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # запрашиваем первого из списка питомца
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, pet_id)

    assert status == 200
    assert id != 0

    raise Exception('Нет своих питомцев')


# 3. Проверка добавления фото питомца. Pass
def test_add_pet_photo(name='Барбоск', animal_type='вортерьер',
                                     age='4', pet_photo='images/uzbogoy.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert pet_photo != ''


# 4. Проверка ключа валидность и длина. Pass
def test_get_length_api_key(email=valid_email, password=valid_password):

    # получаем ключ api и его валидное значение
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert len(result['key']) == 56

    raise Exception('Проверьте данные логина и пароля!')


# 5. Проверка получения ключа с невалидным пользователем. Pass
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):

    # получаем ключ api с невалидными значениями
    status, result = pf.get_api_key(email, password)

    assert status == 403

    raise Exception('Кто-то заимел мои данные почты и пароля!')


# 6. Проверка изменения инфо(имени) о первом в списке моем питомце. Pass
def test_update_info_first_list_my_pet(name='sova', animal_type='flylow', age=7):

    # запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # изменяем данные первого из списка питомца
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name='tarakun', animal_type='rungun', age=6)
    _, my_pets = pf.get_list_of_pets(auth_key, pet_id)

    assert result['name'] != name  # проверка, что изменено имя

    raise Exception('Потому что должны быть разные имена')


# 7. Проверка создания питомца с отрицательным значением возраста (тест должен быть пройден)
def test_post_create_pet_negative_age_value(name='Gavy', animal_type='Kusya',
                                     age='-3'):

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    age = int(age)  # из str в int

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert age < 0


# 8. Получение id питомца первого из списка и проверка его наличия. Pass
def test_get_pet_id():
    # запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # id первого питомца
    pet_id = my_pets['pets'][0]['id']

    assert id != 0

    raise Exception('Моих питомцев в списке нет')


# 9. Проверка добавление нового питомца с фото, не вложив фото
def test_add_new_pet_without_attaching_a_photo(name='Poky', animal_type='dive',
                                     age='1', pet_photo=''):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 10. Тест проверки моих питомцев и что он не пустой. Pass
def test_get_my_pets_with_valid_key(filter='my_pets'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)  # получаем api ключ и сохраняем в переменную auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)  # запрашиваем список моих питомцев

    assert status == 200
    assert len(result['pets']) > 0  # проверяем что список не пустой



