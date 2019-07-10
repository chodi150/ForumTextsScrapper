
Abstract of the thesis:
Despite immense amounts of data available in the Internet, the process of their extraction is often tedious and time-consuming. This thesis is devoted to automatization of the textual data extraction process from Internet forums and its transformation to vector representations. The automatization is fulfilled by an implemented, generic tool. Its requirements, assumptions and details were described. The tool serves for data downloading from the most popular forum engines and transforming the extracted texts to vector representations. Tests of extracting data from three most widely used forum platforms were presented. Exported vector representations of texts were analyzed with use of machine learning algorithms to demonstrate possible uses of extracted data. Possible applications of forum data as well as reasons that make forums interesting field for exploration in data analysis were also introduced.
 
 
This repository contains code aiming to automatize extraction of textual data from internet forums.

 
 1. Opis programu
Program jest implementacją zautomatyzowanego procesu ekstrakcji tekstów z forów internetowych.
Umożliwia pobieranie danych tekstowych z zadanego forum oraz eksport treści oraz ich reprezentacji wektorowych.
Możliwa jest obsługa następujących platform forów: phpBB, Invision oraz vBulletin.

2. Konfiguracja środowiska
Zalecanym jest korzystanie z wirtualnego środowiska Pythona. Wymagane biblioteki i paczki języka Python
wymienione są w pliku requirements.txt. Ich instalacji można dokonać poleceniem:
pip install -r requirements.txt

W przypadku niepowodzenia instalacji pakietu CyHunspell, należy na maszynie najpierw zainstalować Hunspell.

W razie braku listy "stopwords" dla języka polskiego, należy w lokalizacji:  {ścieżka do folderu z danymi biblioteki nltk}/nltk_data/corpora/stopwords/
utworzyć plik o nazwie "polish" z listą "stopwords" dla języka polskiego.
Przykładową listę można znaleźć na:
https://github.com/bieli/stopwords/blob/master/polish.stopwords.txt lub w folderze extras tego projektu.

Natomiast w przypadku braku słownika dla języka polskiego w lokalizacji hunspella, zawierającej inne słowniki,
należy dodać pliki: pl.aff oraz pl.dic, które można znaleźć na: https://sjp.pl/slownik/en/ lub w folderze extras.
Można również skorzystać z poleceń:
cp extras/pl.aff lib/python3.5/site-packages/dictionaries
cp extras/pl.dic lib/python3.5/site-packages/dictionaries

Ponadto niezbędne jest skonfigurowanie połączenia do bazy danych PostgreSQL w pliku config/database_config.py:
USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
DATABASE_NAME = "scrap2"

Baza danych powinna być uprzednio założona - schemat i tabele zostaną założone przy pierwszym uruchomieniu aplikacji

3. Instrukcja obsługi
a)starter.py  - umożliwia uruchamianie pająka Scrapy i pobieranie treści

Może być uruchamiany z parametrami:
-f -- który odpowiada linkowi forum
-m -- tryb ekstrakcji

Możliwe tryby ekstrakcji:
-full_scraping -- pobieranie wszystkich treści z danego forum
-only_categories -- pobieranie tylko kategorii z danego forum i ich wypisanie w pliku config/categories.csv
-chosen_categories -- pobieranie treści z kategorii wyszczególnionych w pliku config/categories.csv

Dla każdego z trybów możliwe jest przeprowadzenie dodatkowej filtracji z kryteriami zadanymi w pliku config/filtering_config.py.
Kryteria definiowane są w jezyku Python.
Typy poszczególnych kryteriów:
topics_date_from -- datetime.datetime
topics_date_to -- datetime.datetime
posts_date_from -- datetime.datetime
posts_date_to -- datetime.datetime
topic_authors -- list(str)
post_authors -- list(str)
topic_keywords -- list(str)
post_keywords -- list(str)


b)export_starter.py - eksport danych

Możliwe wywołanie w trybach (-m):
- glove -- eksport reprezentacji GloVe
- tfidf -- eksport reprezentacji TF-IDF
- posts -- eksport tekstów
- preprocess -- eksport wstępnie przetworzonych tekstów
- forums -- wypisanie dostępnych forów w bazie danych (wraz z ich id)

W celu eksportu danych, niezbędne jest w wywołaniu podanie argumentu -f wraz z id forum.

Ponadto możliwe jest podanie dodatkowych kryteriów filtrujących oraz parametrów pożądanej reprezentacji. Są to:
-df -- od kiedy napisane zostały posty, które chcemy wyeksportować, podane w formacie y-m-d; domyślna wartość: 1970-1-1
-dt -- do kiedy napisane zostały posty, które chcemy wyeksprotować, podane w formacie y-m-d; domyślna wartość: 2020-1-1
-fn -- nazwa pliku, który zostanie wyeksportowany
-gv -- wymiar wektora w reprezentacji GloVe, domyślna wartość: 100
-gw -- rozmiar okna kontekstu w reprezentacji GloVe, domyślna wartość: 5
-ni -- liczba iteracji treningowych dla wektorów słów w GloVe, domyślna wartość: 100
-mindf -- minimalna liczba wystąpień słowa w dokumentach, podawana jako procent dokumentów, w których słowo wystąpiło, domyślna wartość: 0.0025 (słowo wystąpiło w więcej niż 0,25% dokumentów)
-maxdf -- maksymalna liczba wystąpień słowa w dokumentach, podawana jako procent dokumentów, w których słowo wystąpiło, domyślna wartość: 0.5 (słowo wystąpiło w mniej niż 50% dokumentów)



Ponadto w ramach eksportu reprezentacji utworzone zostaną jeszcze pliki .CSV, które zawierają:
- wstępnie przetworzone teksty
- wektory słów (w przypadku reprezentacji GloVe)










