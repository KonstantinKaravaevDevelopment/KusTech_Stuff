#Biblioteki ogólne
import requests
import os
import tmeapi
import json
import urllib.error   
from PIL import Image

#Biblioteki streamlit
import streamlit as st
from streamlit_lottie import st_lottie


### POCZĄKOWA KONFIGURACJA
#Definiujemy zmienne początkowe
TME_wynik = ''
TME_duzy_wynik = ''

# Definiujemy potrzebne funkcje
def get_component_from_TME_API(component, typ):
    client = tmeapi.Client('f9bad40438faa66696f92a567ac7d94a2de8cdbccc678', '6031de0c307964d2ddf6')
    parameters = { 'Country': 'PL', 'Language': 'PL', 'SearchPlain' : component, 'SearchOrder' : 'PRICE_FIRST_QUANTITY' }
    try:
        #Pobieramy informację ogólną
        response = urllib.request.urlopen(client.request('/Products/Search.json', parameters))    
        data_Search = response.read()    
        obj_Search = json.loads(data_Search) 
        Symbol_TME = obj_Search['Data']['ProductList'][0]['Symbol']
        Symbol_Producenta = obj_Search['Data']['ProductList'][0]['OriginalSymbol']
        Producent = obj_Search['Data']['ProductList'][0]['Producer']
        Opis = obj_Search['Data']['ProductList'][0]['Description']
        #Pobieramy dostępność i ceny
        parameters2 = {'Country': 'PL', 'Language': 'PL', 'Currency' : 'PLN','SymbolList[0]' : Symbol_TME}
        response = urllib.request.urlopen(client.request('/Products/GetPricesAndStocks.json', parameters2))    #Wysyłamy zapytanie do TME
        data_GetPricesAndStocks = response.read()
        obj_GetPricesAndStocks = json.loads(data_GetPricesAndStocks)
        Ilosc_na_magazynie = obj_GetPricesAndStocks['Data']['ProductList'][0]['Amount']

        if typ == 'raport':
            #Tworzymy listę cen
            lista_cen = []
            for el in obj_GetPricesAndStocks['Data']['ProductList'][0]['PriceList']:
                lista_cen.append(f"\n           * Zapłacisz **{el['PriceValue']}zł** za sztukę przy zakupie **{el['Amount']}+** sztuk")

            raport_TME = f'''
            - Nazwa komponentu na TME: **{Symbol_TME}**
            - Nazwa komponentu według producenta: **{Symbol_Producenta}**
            - Prodeucent: **{Producent}**
            - Opis: **{Opis}**
            - Ilość sztuk na magazynie **{Ilosc_na_magazynie}**
            - Ceny dla różnych ilości hurtowych: 
            '''
            for elem in lista_cen:
                raport_TME = raport_TME + elem

            return raport_TME    
        elif typ == 'pojedynczy':
            return [Symbol_TME, Ilosc_na_magazynie,  obj_GetPricesAndStocks['Data']['ProductList'][0]['PriceList']]                                                     
    except: 
        if typ == 'raport':
            raport_TME = '''
            **Brak elementu w bazie TME.**

            **Spróbuj poszukać inny komponent**
            '''
            return raport_TME
        
        elif typ == 'pojedynczy':
            return ['Brak elementu w bazie']

def get_price_of_multiple_PCB(components, ilosci):

    spisok = []
    # a = 0
    # a = 0
    for el in components:

        info_komponent = get_component_from_TME_API(el[0], 'pojedynczy')
        pozycja = []
        
        # odpowiedz = f'Dla ilosci {ilosci[a]} trzeba będzie kupić {ilosci[a] * int(el[1])} i ich cena wyniesie '
        # odpowiedz = f'Przy ilości produkcji '

        spisok.append(info_komponent)
        # print(odpowiedz)

        # if el[1] == '1':
        #     pozycja = [info_komponent[0], info_komponent[1], info_komponent[2][] ]

    
        # a = a+1
    
    odpowiedz = f'''
        Dla produkcji 10 płytek trzeba kupić:
        - {ilosci[0]*int(components[0][1])} szt RF-40HA50DS-EE-Y ({spisok[0][1]} szt na magazynie TME), za co zapłacisz **{round(40 * spisok[0][2][1]["PriceValue"], 2)} Zł**
        - {ilosci[0]*int(components[1][1])} szt SMD0805-100R-1% ({spisok[1][1]} szt na magazynie TME), za co zapłacisz **{round(100 * spisok[1][2][0]["PriceValue"], 2)} Zł**
        - {ilosci[0]*int(components[2][1])} szt BAT54W-DIO ({spisok[2][1]} szt na magazynie TME), za co zapłacisz **{round(25 * spisok[2][2][0]["PriceValue"], 2)} Zł**
        
        Razem wychodzi **{round(round(40 * spisok[0][2][1]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(25 * spisok[2][2][0]["PriceValue"], 2),2)} Zł** (**{round((round(40 * spisok[0][2][1]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(25 * spisok[2][2][0]["PriceValue"], 2))/10, 2)} Zł** za płytkę)

        Dla produkcji 30 płytek trzeba kupić:
        - {ilosci[1]*int(components[0][1])} szt RF-40HA50DS-EE-Y ({spisok[0][1]} szt na magazynie TME), za co zapłacisz {round(120 * spisok[0][2][2]["PriceValue"], 2)} Zł
        - {ilosci[1]*int(components[1][1])} szt SMD0805-100R-1% ({spisok[1][1]} szt na magazynie TME), za co zapłacisz {round(100 * spisok[1][2][0]["PriceValue"], 2)} Zł
        - {ilosci[1]*int(components[2][1])} szt BAT54W-DIO ({spisok[2][1]} szt na magazynie TME), za co zapłacisz {round(60 * spisok[2][2][0]["PriceValue"], 2)} Zł
        
        Razem wychodzi **{round(round(120 * spisok[0][2][2]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(60 * spisok[2][2][0]["PriceValue"], 2),2)} Zł** (**{round((round(120 * spisok[0][2][2]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(60 * spisok[2][2][0]["PriceValue"], 2))/30, 2)} Zł** za płytkę)

        Dla produkcji 50 płytek trzeba kupić:
        - {ilosci[2]*int(components[0][1])} szt RF-40HA50DS-EE-Y ({spisok[0][1]} szt na magazynie TME), za co zapłacisz {round(200 * spisok[0][2][2]["PriceValue"], 2)} Zł
        - {ilosci[2]*int(components[1][1])} szt SMD0805-100R-1% ({spisok[1][1]} szt na magazynie TME), za co zapłacisz {round(100 * spisok[1][2][0]["PriceValue"], 2)} Zł
        - {ilosci[2]*int(components[2][1])} szt BAT54W-DIO ({spisok[2][1]} szt na magazynie TME), za co zapłacisz {round(100 * spisok[2][2][1]["PriceValue"], 2)} Zł
        
        Razem wychodzi **{round(round(200 * spisok[0][2][2]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(100 * spisok[2][2][1]["PriceValue"], 2),2)} Zł** (**{round((round(200 * spisok[0][2][2]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(100 * spisok[2][2][1]["PriceValue"], 2))/50, 2)} Zł** za płytkę)

        Dla produkcji 100 płytek trzeba kupić:
        - {ilosci[3]*int(components[0][1])} szt RF-40HA50DS-EE-Y ({spisok[0][1]} szt na magazynie TME), za co zapłacisz {round(500 * spisok[0][2][3]["PriceValue"], 2)} Zł
        - {ilosci[3]*int(components[1][1])} szt SMD0805-100R-1% ({spisok[1][1]} szt na magazynie TME), za co zapłacisz {round(100 * spisok[1][2][0]["PriceValue"], 2)} Zł
        - {ilosci[3]*int(components[2][1])} szt BAT54W-DIO ({spisok[2][1]} szt na magazynie TME), za co zapłacisz {round(200 * spisok[2][2][1]["PriceValue"], 2)} Zł
        
        Razem wychodzi **{round(round(500 * spisok[0][2][3]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(200 * spisok[2][2][1]["PriceValue"], 2),2)} Zł** (**{round((round(500 * spisok[0][2][3]["PriceValue"], 2) + round(100 * spisok[1][2][0]["PriceValue"], 2) + round(200 * spisok[2][2][1]["PriceValue"], 2))/100, 2)} Zł** za płytkę)

        Dla produkcji 500 płytek trzeba kupić:
        - {ilosci[4]*int(components[0][1])} szt RF-40HA50DS-EE-Y ({spisok[0][1]} szt na magazynie TME), za co zapłacisz {round(2000 * spisok[0][2][3]["PriceValue"], 2)} Zł
        - {ilosci[4]*int(components[1][1])} szt SMD0805-100R-1% ({spisok[1][1]} szt na magazynie TME), za co zapłacisz {round(1000 * spisok[1][2][1]["PriceValue"], 2)} Zł
        - {ilosci[4]*int(components[2][1])} szt BAT54W-DIO ({spisok[2][1]} szt na magazynie TME), za co zapłacisz {round(1000 * spisok[2][2][2]["PriceValue"], 2)} Zł
        
        Razem wychodzi **{round(round(2000 * spisok[0][2][3]["PriceValue"], 2) + round(1000 * spisok[1][2][1]["PriceValue"], 2) + round(1000 * spisok[2][2][2]["PriceValue"], 2),2)} Zł** (**{round((round(2000 * spisok[0][2][3]["PriceValue"], 2) + round(1000 * spisok[1][2][1]["PriceValue"], 2) + round(1000 * spisok[2][2][2]["PriceValue"], 2))/500, 2)} Zł** za płytkę)

        '''



    return odpowiedz
    



### PARAMETRY STRONKI 
#Dodajemy Icone
ikonka_path = os.path.join("images", "Icon_webpage.png")
ikonka = Image.open(ikonka_path)
# ikonka = Image.open(r"images\Icon_webpage.png")

st.set_page_config(
    page_title='🪩 Komunikacja API',
    page_icon=ikonka,
    layout='wide',
    
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_rocket = load_lottieurl('https://lottie.host/c6a39c47-7387-4b0b-b7a3-1b2e9c4d9f13/8mLeR8dPTh.json')
piesek_zdjecie_path = os.path.join("images", "question_image.png")
piesek_zdjecie = Image.open(piesek_zdjecie_path)
# piesek_zdjecie = Image.open(r"images\question_image.png")

LED_USB_path = os.path.join("images", "LED_USB.png")
LED_USB = Image.open(LED_USB_path)
# LED_USB = Image.open(r"images\LED_USB.png")


with st.container():

    ##Bloczek z ogolnym info
    st.header('API dla automatyzacji zakupów 🪩')
    st.subheader('Projekt służący pomocą działowi logistycznemu.')
    st.write("---")
    st.write('##')
    st.write(
        '''

        API (Interfejs Programowania Aplikacji) jest protokolem, umożliwiającym dwóm różnym aplikacją "rozmawianie" ze sobą poprzez wysyłanie specjalnych komend do siebie na wzajem.
        
        Dzięki temu protokołowi aplikacje stworzone różnymi programmistami mogą wymieniać się informacjami oraz skutecznie współpracować bez konieczności interwencji człowieka.
        '''
    )

    ##Bloczek z pieskami
    left_column_1, right_column_1 = st.columns(2)
    with left_column_1:
        st.write('##')
        st.write('##')
        st.subheader('Na przykład')
        st.write('##')
        st.write(
            '''
            Dzięki technologii API możemy wysyłać zapytania na stronę https://dog.ceo/dog-api/ aby otrzymywać randomowe zdjęcia piesków, umieszczone w ich bazie dannych:
            
            '''
        )
        st.write('##')
        piesek = st.button('Pokaż pieska', type='secondary')
        if piesek:
            piesek_zdjecie_internet = requests.get('https://dog.ceo/api/breeds/image/random')
            piesek_zdjecie_dict = piesek_zdjecie_internet.json()
            piesek_zdjecie = piesek_zdjecie_dict['message']

    with right_column_1:
        # st.image('https://images.dog.ceo/breeds/labrador/n02099712_5263.jpg', caption='Otrzymany piesek')
        st.image(piesek_zdjecie, caption='Otrzymany piesek', width= 300)
    
    ##Bloczek o API
    st.write('##')
    st.write('##')
    st.write(
        '''
        Poza ładowaniem zdjęć z internetu ten protokół może posłużyć również dla szybkiego pobierania wszelakich informacji,
        odpowiednia analiza któwych może zwiększyć konkurencyjność Pańskiej firmy. Mogą to być między innymi dostępność pewnych
         artykółów na magazynach, ceny tego samego towaru w różnych sklepach internetowych itp. \n
        Trzeba też wziąć pod uwagę, że nie każda strona internetowa posiada API, natomiast nektóre strony mają i my jako przedsiębiorcy korzystając z niego zwięszamy effektywność naszych procesów biznesowych. 
        ''')
    st.write("---")
    
    ##Bloczek z API TME
    left_column_2, right_column_2 = st.columns(2)
    with left_column_2:
        st.write('##')
        # st.subheader('Przychodząc do rzeczy praktycznych')
        st.subheader('A w praktyce?')

        st.write(
        '''
        Jako przykład użytecznego wykorzystania API zobaczmy jaką informację się uda wyciągnąć z polskiego sklepu internetowego https://www.tme.eu, zajmującego się sprzedażą komponentów elektronicznych.\n
        Posiada on swoją dokumentację API (https://developers.tme.eu/), opowiadającą w jakim formacie i gdzie należy wysłać zapytanie, aby otrzymać interesującą nas informacje. \n
        Będziemy wyciągali: 
        - Nazwę komponentu 
        - Nazwę produkcyjną komponentu
        - Producenta
        - Opis
        - Dostępność na magazynie
        - Ceny dla różnych ilości
        
        Skopiuj jedną z nazw komponentów ('**0105WHF1000TDE**', '**0201B102K500CT**', '**1N4148-0805**', '**2N7002-DIO**', '**68001-102HLF**') lub wejść na stronę https://www.tme.eu/pl/katalog/rezystory-smd_100300/?onlyInStock=1 i skopiuj dowolny komponent ze sklepu, po czym wstaw go do pola roboczego. 
        Następnie naciśnij przycisk "Szukaj!". Po prawej stronie powinna się pojawić informacja dotycząca wybranego komponentu. 
        ''')

    with right_column_2:
        st.write('##')
        st.subheader('Wyniki zapytania API')
        st.write('##')
        nazwa_komponentu = st.text_input('Podaj nazwę komponentu', '0105WHF1000TDE')
        TME_API_button = st.button('Pobierz informacje z TME', type='secondary')
        
        if TME_API_button:
            raport_TME = get_component_from_TME_API(nazwa_komponentu, 'raport')
            TME_wynik = raport_TME

        
        st.write(TME_wynik)
    st.write("---")

    ##Bloczek o porównywaniu 
    left_column_3, right_column_3 = st.columns(2)
    with left_column_3:
        st.write('##')
        st.subheader('Jak to może pomóc twojemu biznesowi?')
        st.write(
        '''
        Pozwoli to przede wszystkim otrzymywać informację bez zbędnych ruchów i w tej formie, która będzie najbardziej optymalna dla dalszej analizy. \n
        Zobaczmy na przykładzie latarki USB, odnalezionej na Allegro:
        ''')
        st.image(LED_USB, caption='Latarka USB z Allegro', width= 450)
        st.write(
        '''
        Składa się ona z PCB płytki, 4 diodów LED (np **RF-40HA50DS-EE-Y**), jednego rezystora o wartości 100 Ohm (np **SMD0805-100R-1%**) oraz dwóch diodów Schottkiego (np **BAT54W-DIO**).\n 
        Dzięki dobrze skonfigorowanemu algorytmowi i danych z API będziemy mogli policzyć koszt komponenów dla produkcji kilku przykładowych partii tej płytki przy zakupie na TME w czasie rzeczewistym. 
        ''')
        USB_LED_koszty_button = st.button('Policz wydatki na komponenty z TME', type='secondary')
        if USB_LED_koszty_button:
            raport_ceny_TME = get_price_of_multiple_PCB([['RF-40HA50DS-EE-Y', '4'], ['SMD0805-100R-1%', '1'], ['BAT54W-DIO', '2']], [10,30,50,100,500])
            TME_duzy_wynik = raport_ceny_TME
            # print(raport_ceny_TME)
    
    with right_column_3:
        st.write('##')
        st.subheader('Wyniki obliczeń ')
        # st.write('##')

        st.write(TME_duzy_wynik)
    
    st.write("---")
    ##Bloczek z podsumowaniem
    st.write('##')
    st.subheader('Napisz do nas!')
    st.write('##')
    st.write(
    '''
    Wszelakie pytanie prosimy kierować na adres mailowy **KusTech@proton.me**. 

    **Zróbmy Pańskie obliczenia szybciej!**
    ''')

