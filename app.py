import streamlit as st
import pandas as pd
from io import BytesIO
from functions import *

st.set_page_config(
    page_title='Scraping BDM',
    page_icon='🦆',
    layout='centered'
)

df = pd.read_json('data.json').T


# Title
st.title('My First App Streamlit - V1')

# CheckBox
if st.checkbox("Show information"):
    st.write(df)

# Formulaire 

articles = None
url = "https://www.blogdumoderateur.com"
with st.form("First form"):
    user_input = st.text_input("Votre recherche")
    submitted = st.form_submit_button('Send')
    if submitted:
        articles_page_1 = scraping_bdm(url + "?s=" + user_input.replace(' ', '+'))
        articles_page_2 = scraping_bdm(url + "/page/2/?s=" + user_input.replace(' ', '+'))
        st.session_state['articles'] = {**articles_page_1, **articles_page_2}

if 'articles' in st.session_state and st.session_state['articles']:
    articles = st.session_state['articles']
    df = pd.DataFrame.from_dict(articles, orient='index')
    towrite = BytesIO()
    df.to_excel(towrite, index=False, engine='openpyxl')
    towrite.seek(0)
    file_name = "article.xlsx"
    st.download_button(label="Télécharger les données en Excel",
                        data=towrite,
                        file_name=file_name,
                        mime="application/vnd.ms-excel")
    selected = st.selectbox('Choisissez votre article', [value['title'] for key, value in articles.items()])
    selected_article = next((item for key, item in articles.items() if item['title'] == selected), None)
    col1, col2 = st.columns(2)
    with col1:
        st.write("Titre:", selected_article['title'])
        st.write("Catégorie:", selected_article.get('label', 'Non spécifié'))
        st.write("Date de publication:", selected_article.get('time', 'Non spécifié'))
        st.write("Lien de l'article:", selected_article.get('link', 'Non spécifié'))

    with col2:
        image_url = selected_article.get('image')
        if image_url:
            st.image(image_url, caption="Image de l'article")
        else:
            st.write("Aucune image disponible")
    st.markdown("<hr>", unsafe_allow_html=True)

   
   
   

