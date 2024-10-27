import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

def get_currency_data_cbr(target_currency, start_date, end_date):
    # Форматируем даты для запроса в формате ДД/ММ/ГГГГ
    formatted_start_date = start_date.strftime('%d/%m/%Y')
    formatted_end_date = end_date.strftime('%d/%m/%Y')

    url = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={formatted_start_date}&date_req2={formatted_end_date}&VAL_NM_RQ={target_currency}"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return None

    # Парсим XML
    try:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        data = []
        for record in root.findall('Record'):
            date_str = record.attrib['Date']
            date = datetime.strptime(date_str, '%d.%m.%Y')
            value = float(record.find('Value').text.replace(',', '.'))  # Парсим значение курса
            data.append((date, value))

        # Преобразуем в DataFrame
        df = pd.DataFrame(data, columns=['Date', 'Rate'])
        df.set_index('Date', inplace=True)
        return df

    except ET.ParseError:
        print("Ошибка парсинга XML.")
        return None

# Пример использования для курса USD к рублю
target_currency = "R01235"  # Код валюты для USD
end_date = datetime.today()
start_date = end_date - timedelta(days=90)

df = get_currency_data_cbr(target_currency, start_date, end_date)

if df is not None:  # Проверка, что DataFrame не пустой
    # Визуализация
    df.plot()
    plt.title(f"Exchange rate for USD to RUB")
    plt.xlabel("Date")
    plt.ylabel(f"Rate (RUB)")
    plt.grid(True)
    plt.show()