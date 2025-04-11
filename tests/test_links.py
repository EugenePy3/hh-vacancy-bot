from scraper.parser import get_vacancy_links


def test_get_vacancy_links(driver):
    """Проверяет, что функция get_vacancy_links возвращает непустой список ссылок на вакансии."""
    driver.get('https://novosibirsk.hh.ru/search/vacancy?text=Python+разработчик')

    links = get_vacancy_links(driver)

    assert isinstance(links, list), 'Функция должна возвращать список'
    assert len(links) > 0, 'Список ссылок пуст, возможно, сайт изменил разметку или вакансий нет'


def test_vacancy_links_are_valid(driver):
    """Проверяет, что каждая собранная ссылка содержит 'vacancy', подтверждая корректность ссылок."""
    links = get_vacancy_links(driver)

    assert all("vacancy" in link for link in links), 'Некоторые ссылки не ведут на вакансии'
