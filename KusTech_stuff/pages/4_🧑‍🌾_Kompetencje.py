import requests
from PIL import Image
import os

import streamlit as st
from streamlit_lottie import st_lottie

#Dodajemy Icone
file_path = os.path.join("images", "Icon_webpage.png")
ikonka = Image.open(file_path)

st.set_page_config(
    page_title='Kompetencje',
    page_icon=ikonka,
    layout='wide',
    
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_inzynier = load_lottieurl('https://lottie.host/a494877e-4e8b-46a3-aff1-e5dd7f54ac89/BoFuCu7tVV.json')

with st.container():
    st.subheader('Wiedza się liczy')
    st.write('Posiadamy wiedzę głównie z branży produkcyjnej - częściowo znamy jej słabe strony i widzimy ogromne obszar do działań. ')
    st.write("---")

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.header('Kto w załodze?')
        st.write('##')
        st.write('''
                 Naszym głównym programmistem jest Konstantin Karavaev - inżynier po "Automatyzacji i robotyzacji procesów produkcyjnych" na Politechnice Warszawskiej.

                 Po studiach bywa różnie, natomiast zdobyte tam doświadczenie przy maszynach pozwala na skuteczniejsze napisanie algorytmów dla polepszenia procesów produkcyjnych.

                 ---

                 Poniżej załączamy pracę inżynierską do poglądu 👀
                 ''')
        
        file_pa = os.path.join("files", "Praca_Inżynierska_-_Konstantin_Karavaev_303144.pdf")
        with open(file_pa, "rb") as file:
            btn = st.download_button(
                    label="Pobierz pracę inżynierską",
                    data=file,
                    file_name="Praca_Inżynierska_-_Konstantin_Karavaev_303144.pdf",
                    mime="image/png"
                )

    with right_column:
        # st.write('##')
        st_lottie(lottie_inzynier, height=400, key='coding')