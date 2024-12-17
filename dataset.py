import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

standing_url = "https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats"
data = requests.get(standing_url) # получает html-код главной дата страницы в скобках 
soup = BeautifulSoup(data.text) # создание объекта с html-кодом
standings_table = soup.select('table.stats_table')[0] # селектор css по классу в скобках - выбираем html только для нужной нам таблички
"""
links = standings_table.find_all('a') # ищем в файле все <а> теги
links = [l.get("href") for l in links] # получение в список на все ссылки в каждой строки таблицы
links = [l for l in links if '/squads/' in l] # получение ссылок только на команды рпл
team_urls = [f"https://fbref.com{l}" for l in links] # получение полных team_url """

# парсинг заданных таблиц
main_table_epl = pd.read_html(StringIO(str(data.text)), match="Premier League Table") # основная таблица турнира
squad_shooting = pd.read_html(StringIO(str(data.text)), match="Squad Shooting")
squad_standart = pd.read_html(StringIO(str(data.text)), match="Squad Standard Stats")
squad_goalkeeping = pd.read_html(StringIO(str(data.text)), match="Squad Goalkeeping")
squad_def = pd.read_html(StringIO(str(data.text)), match="Squad Defensive Actions")
squad_shoot_ag = pd.read_html(StringIO(str(soup.find('table', {'id': 'stats_squads_shooting_against'}))))
squad_pass = pd.read_html(StringIO(str(data.text)), match="Squad Pass Types ")
squad_possn = pd.read_html(StringIO(str(data.text)), match="Squad Possession ")

# создание моей итоговой таблицы XGdifference = 13 индекс
my_epl_dataframe = pd.DataFrame([], columns=['Team', 'All Sh', 'Sh OT', 'Goals', 'Sh OT Ag', 'Clean Perc', 'Goals Ag',
'xGD', 'Interc', 'YC', 'Crs', 'CK', 'Poss', 'Bls'])
dict_frame = {1: 'Team', 6: 'Goals', 7: 'Goals Ag', 13: 'xGD'} # создание словаря для столбцов с уже известными значениями

i_d = 0 # создание переменной индексации для функции loc
for data_ in main_table_epl[0].values: # пробегаемся по массивам значений 
    for x in (1, 6, 7, 13): # массив нужных индексов для записи из таблицы main_table_rpl
        my_epl_dataframe.loc[i_d, dict_frame[x]] = data_[x] # присвоение нужной ячейки своего значения
    i_d += 1

dict_squad_ag = {} # создание словаря команд со статистикой их ударов
for data_ in squad_shoot_ag[0].values: # пробегаемся по массивам значений 
    dict_squad_ag[data_[0][3:]] = (data_[5]) # наполнение словаря данными по командам

i_d = 0
for data_ in my_epl_dataframe.values:
    my_epl_dataframe.loc[i_d, 'Sh OT Ag'] = dict_squad_ag[data_[0]] # записываем данные из словаря в нужные места
    i_d += 1


def parsing(table, stats, index_list):
    """Функция, реализующая передачу данных из нужных столбцов заданной таблицы в локальную
    list[DataFrame]: table - фрейм данных заданной таблицы,
    list: stats - нужные стат. характеристики
    list: index_list - массив индексов"""

    if (len(index_list) == 2): # если количество передаваемых стат. характеристик == 2
        dict_squad_ = {} # создание словаря команд со статистикой характеристики, которую передают в качестве параметра
        for data_ in table[0].values: # пробегаемся по массивам значений 
            dict_squad_[data_[0]] = (data_[index_list[0]], data_[index_list[1]]) # наполнение словаря данными по командам
        print(dict_squad_)

        i_d = 0
        for data_ in my_epl_dataframe.values:
            my_epl_dataframe.loc[i_d, stats[0]] = dict_squad_[data_[0]][0] # записываем данные из словаря в нужные места
            my_epl_dataframe.loc[i_d, stats[1]] = dict_squad_[data_[0]][1]
            i_d += 1

    if (len(index_list) == 1): # если количество передаваемых стат. характеристик == 1
        dict_squad_ = {} # создание словаря команд со статистикой характеристики, которую передают в качестве параметра
        for data_ in table[0].values: # пробегаемся по массивам значений 
            dict_squad_[data_[0]] = (data_[index_list[0]]) # наполнение словаря данными по командам
        print(dict_squad_)

        i_d = 0
        for data_ in my_epl_dataframe.values:
            print(data_[0])
            my_epl_dataframe.loc[i_d, stats[0]] = dict_squad_[data_[0]] # записываем данные из словаря в нужные места
            i_d += 1

parsing(squad_goalkeeping, ["Clean Perc"], [15])
parsing(squad_shooting, ['All Sh', 'Sh OT'], [4, 5])
parsing(squad_standart, ['YC'], [14])
parsing(squad_def, ['Interc'], [15])
parsing(squad_pass, ['Crs', 'CK'], [9, 11])
parsing(squad_possn, ['Poss'], [2])
parsing(squad_def, ['Bls'], [12])



print(my_epl_dataframe)
"""
my_epl_dataframe.to_csv('data.csv')

with open("data.csv") as file:
    text = file.read().split("\n")
    new_ = []
    for i in text:
        new = i.replace(",", " ")
        new = new.replace(".", ",")
        new_.append(new)
    print(*new_)

    
"""