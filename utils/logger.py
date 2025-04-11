import logging


#  Настройка логирования
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='hh.log',
        filemode='w'
    )

    # Дополнительно выводим логи в консоль
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(console_formatter)

    #  logging.getLogger('').addHandler(console_handler)  # Добавляем вывод в консоль (раскомментировать при необх.)



