from scraper.vacancy_scraper import parse_vacancy
from scraper.vacancy_scraper import get_text_or_default


def test_get_text_or_default(driver):
    """Проверяет, что функция корректно получает текст элемента или возвращает значение по умолчанию."""
    existing_text = get_text_or_default(driver, '[data-qa="search-input"]', 'не найдено')
    assert existing_text != 'не найдено'  # Должен вернуть текст, а не значение по умолчанию

    missing_text = get_text_or_default(driver, '.non-existent-selector', 'не найдено')
    assert missing_text == 'не найдено'  # Должен вернуть значение по умолчанию


def test_parse_vacancy(driver):
    """Проверяет, что parse_vacancy корректно извлекает данные вакансии."""
    sample_url = "https://novosibirsk.hh.ru/vacancy/102422415"

    data = parse_vacancy(driver, sample_url)

    assert data is not None, 'Функция должна возвращать словарь'
    assert isinstance(data, dict), 'Результат должен быть словарем'

    expected_keys = {'title', 'salary', 'experience', 'date', 'url', 'description'}
    assert expected_keys.issubset(data.keys()), f'Отсутствуют ключи: {expected_keys - set(data.keys())}'

    # Дополнительные проверки на заполненность данных
    assert data['title'], 'Заголовок вакансии пуст'
    assert data['url'] == sample_url, 'URL вакансии некорректен'


