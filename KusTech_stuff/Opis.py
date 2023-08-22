
import requests
from PIL import Image
import os

import streamlit as st
from streamlit_lottie import st_lottie

#Dodajemy Icone
file_path = os.path.join("images", "Icon_webpage.png")
ikonka = Image.open(file_path)

st.set_page_config(
    page_title='KusTech Stuff',
    page_icon=ikonka,
    layout='wide',
    
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding_man = load_lottieurl('https://lottie.host/9b55db92-7224-48f5-892b-2a8321313727/7g7Lud3A0r.json')


# ---- HEADER SECTION --------
with st.container():
    st.subheader('KusTech Stuff presents')
    st.title('Witamy w naszym warsztacie! 👨‍🔧')
    st.write('Ta strona służy do głębszej demonstracji naszej działalności - zamiast czytania standartowych haseł zawsze ciekawiej jest zobaczyć w praktyce na co nasze rozwiązania się nadają. ')
    # st.sidebar.success('Opis')

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header('Na czym się skupiamy?')
        st.write('##')
        st.write(
            '''
            Dla celów demonstracyjnych skupimy się tutaj na konkretnym przykładzie - na przyśpieszeniu działalności pewnej firmy produkcyjnej z branży elektroniki. 
            
            Stworzyliśmy oraz wdrożyliśmy do procesów biznesowych:

            - System analizy oraz zamówień komponentów elektronicznych (rezystory, kondensatory, tranzystory, układy scalone itp.) od polskich oraz zagranicznych kontrahentów.
            - Algorytm automatycznej obsługi kalkulatora cen produkcji płyt PCB (płytki dla elektroniki) na stronie JLCPCB.com.
            - Customowy algorytm obsługi drukarki GoDEX z poziomu Excela "w jednym kliknięciu".
            - Różne małe skrypty umożliwiające szybszą analizę danych oraz ich przenoszenie pomiędzy arkuszami Excela.

            Nie martw się! Do każdego klienta podchodimy indywidualnie - dla ciebie również coś dobierzemy. 
            '''
        )
    
    with right_column:
        # st.write('##')
        st_lottie(lottie_coding_man, height=400, key='coding')