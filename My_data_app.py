#!/usr/bin/env python
# coding: utf-8

# In[235]:


# importer les packages
import streamlit as st
import pandas as pd
from requests import get # récupérer le contenu html de la page
from bs4 import BeautifulSoup as bs # d'avoir le contenu sparsé dans un objet beautifulSoup
import streamlit as st
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import streamlit.components.v1 as components


# In[236]:


st.markdown("<h1 style='text-align: center; color: black;'>MY DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
Cette application récupère des données du site coin Afrique sur plusieurs pages. 
Les données concernent les chaussures et vertements pour homme et enfants. 
Il est également possible de télécharger directement les données récupérées depuis 
l'application, sans avoir à les extraire à nouveau.
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Coin-Afrique](https://sn.coinafrique.com/) 
""")


# In[237]:


# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


# In[238]:


# Web scraping pour les données de vetements et chaussures. évite de refaire le calcul à chaque clic.
@st.cache_data
#fonction transforme un DataFrame en CSV téléchargeable
def convert_df(df):
    return df.to_csv().encode('utf-8')


# In[239]:


#fonction transforme n’importe quel DataFrame en un petit module interactif : Bouton.Voir les données et Télécharger les données
def load(dataframe, title, key, key1) :
    # Créer 3 colonnes avec celle du milieu plus large
    col1, col2, col3 = st.columns([1, 2, 1])
# Affiche le titre et les dimension du dataframe  
    with col2:
        if st.button(title, key1):
            st.subheader('Display data dimension')
#affiche nbre de ligne et nbre de colonne
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
#Affiche le DataFrame sous forme de tableau interactif dans l’app
            st.dataframe(dataframe) 
#Appelle la fonction convert_df qui transforme le DataFrame en fichier CSV téléchageable
            csv = convert_df(dataframe)
#télécharge le contenu de csv
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Data.csv',
                mime='text/csv',
                key = key)


# In[240]:


#fonction : pont entre ton fichier CSS et Streamlit : Elle lit ton fichier .css et l’injecte dans la page web Streamlit pour modifier le design.
#def local_css(file_name):
    #with open(file_name) as f:
        #st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# In[241]:


#Fonction pour web scraping vetement homme
def load_vetement_homme_data(mul_page):
    # create a dataframe vide df
    df = pd.DataFrame()
    # Parcourir les indexes des différents pages 
    for index_page in range(1,int(mul_page)+1):
        url = f"https://sn.coinafrique.com/categorie/vetements-homme?page={index_page}"
    # récupération du contenu de la page
        res =get(url)
    # Avoir le contenu dans un objet bs et sparsifier
        soup = bs(res.content, "html.parser")
    # récupération des conteneurs
        containers = soup.find_all("div", class_="col s6 m4 l3")
    #scraper les données de tous les conteneurs
        data= []
        for container in containers:
            #url_container =  'https://sn.coinafrique.com' + container.find('a')['href'] # Recuperer l'url du sous_container
            # contenu html de la sous page
            #res_container = get(url_container)
            #soup_container = bs(res_container.content, 'html.parser')
            try:
     # scrape les données sur le type d'habits
                type_habits = container.find('p', class_='ad__card-description').text.strip()
    # scrape les données sur le prix           
                prix = container.find('p', class_='ad__card-price').text.strip('CFA')
    # scrape les données sur l"adresse
                adresse11 = container.find("p", class_="ad__card-location").text.strip()
                #adresse = [
                 #   span['data-address']
                  #  for span in container.find_all('span', class_='valign-wrapper')
                   # if 'data-address' in span.attrs]
                #adresse1 = list(dict.fromkeys(adresse))
                #adresse11 = str(adresse1)
                
    # scrape les données sur image_lien
                image_full1 = container.find("img")["src"]
                #url_image = [
                 #   div['style'].split('url(')[1].split(')')[0]
                  #  for div in container.find_all('div', class_='swiper-slide')
                   # if 'style' in div.attrs
             #   ]      
               # url_image = list(dict.fromkeys(url_image))
               # image_full = [img for img in url_image if "thumb_" not in img]
               # image_full1 = str(image_full)
                
                dic = {"Type d'habits": type_habits, "Prix": prix,
                    "Adresse": adresse11,
                    "Lien des images":image_full1
                }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame( data)
        df = pd.concat([df,DF], axis = 0).reset_index(drop = True)
        
        #Remplacer les valeurs manquantes par la médiane dans df
        for col in df[:]:
            if df[col].dtype != "object":   # Si la colonne est numérique → remplacer NA par médiane
                df[col].fillna(df[col].median(), inplace = True)
            else:  # Si la colonne est une chaine de caractère → remplacer NA par "N/A"
                df[col] = df[col].fillna("N/A")
    return df


# In[242]:


#Fonction pour web scraping chaussure homme
def load_chaussure_homme_data(mul_page):
    # create a dataframe vide df
    df = pd.DataFrame()
    # Parcourir les indexes des différents pages 
    for index_page in range(1,int(mul_page)+1):
        url = f"https://sn.coinafrique.com/categorie/chaussures-homme?page={index_page}"
    # récupération du contenu de la page
        res =get(url)
    # Avoir le contenu dans un objet bs et sparsifier
        soup = bs(res.content, "html.parser")
    # récupération des conteneurs
        containers = soup.find_all("div", class_="col s6 m4 l3")
    #scraper les données de tous les conteneurs
        data= []
        for container in containers:
            #url_container =  'https://sn.coinafrique.com' + container.find('a')['href'] # Recuperer l'url du sous_container
            # contenu html de la sous page
            #res_container = get(url_container)
            #soup_container = bs(res_container.content, 'html.parser')
            try:
     # scrape les données sur le type de chaussures
                type_chaussures = container.find('p', class_='ad__card-description').text.strip()
    # scrape les données sur le prix           
                prix = container.find('p', class_='ad__card-price').text.strip('CFA')
    # scrape les données sur l"adresse
                adresse11 = container.find("p", class_="ad__card-location").text.strip()
                #adresse = [
                 #   span['data-address']
                  #  for span in soup_container.find_all('span', class_='valign-wrapper')
                   # if 'data-address' in span.attrs]
                #adresse1 = list(dict.fromkeys(adresse))
                #adresse11 = str(adresse1)
                
    # scrape les données sur image_lien
                image_full1 = container.find("img")["src"]
                #url_image = [
                 #   div['style'].split('url(')[1].split(')')[0]
                  #  for div in soup_container.find_all('div', class_='swiper-slide')
                   # if 'style' in div.attrs
                #]      
                #url_image = list(dict.fromkeys(url_image))
                #image_full = [img for img in url_image if "thumb_" not in img]
                #image_full1 = str(image_full)
                
                dic = {"Type de chaussures": type_chaussures, "Prix": prix,
                    "Adresse": adresse11,
                    "Lien des images":image_full1
                }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame( data)
        df = pd.concat([df,DF], axis = 0).reset_index(drop = True)
        
        #Remplacer les valeurs manquantes par la médiane dans df
        for col in df[:]:
            if df[col].dtype != "object":   # Si la colonne est numérique → remplacer NA par médiane
                df[col].fillna(df[col].median(), inplace = True)
            else:  # Si la colonne est une chaine de caractère → remplacer NA par "N/A"
                df[col] = df[col].fillna("N/A")
    return df


# In[243]:


#Fonction pour web scraping chaussure homme
def load_vetement_enfants_data(mul_page):
    # create a dataframe vide df
    df = pd.DataFrame()
    # Parcourir les indexes des différents pages 
    for index_page in range(1,int(mul_page)+1):
        url = f"https://sn.coinafrique.com/categorie/vetements-enfants?page={index_page}"
    # récupération du contenu de la page
        res =get(url)
    # Avoir le contenu dans un objet bs et sparsifier
        soup = bs(res.content, "html.parser")
    # récupération des conteneurs
        containers = soup.find_all("div", class_="col s6 m4 l3")
    #scraper les données de tous les conteneurs
        data= []
        for container in containers:
            #url_container =  'https://sn.coinafrique.com' + container.find('a')['href'] # Recuperer l'url du sous_container
            # contenu html de la sous page
            #res_container = get(url_container)
            #soup_container = bs(res_container.content, 'html.parser')
            try:
     # scrape les données sur le type de vetements
                type_vetements = container.find('p', class_='ad__card-description').text.strip()
    # scrape les données sur le prix           
                prix = container.find('p', class_='ad__card-price').text.strip('CFA')
    # scrape les données sur l"adresse
                adresse11 = container.find("p", class_="ad__card-location").text.strip()
                #adresse = [
                    #span['data-address']
                    #for span in soup_container.find_all('span', class_='valign-wrapper')
                    #if 'data-address' in span.attrs]
                #adresse1 = list(dict.fromkeys(adresse))
                #adresse11 = str(adresse1)
                
    # scrape les données sur image_lien
                image_full1 = container.find("img")["src"]

                #url_image = [
                 #   div['style'].split('url(')[1].split(')')[0]
                  #  for div in soup_container.find_all('div', class_='swiper-slide')
                   # if 'style' in div.attrs
                #]      
                #url_image = list(dict.fromkeys(url_image))
                #image_full = [img for img in url_image if "thumb_" not in img]
                #image_full1 = str(image_full)
                
                dic = {"Type de vetements": type_vetements, "Prix": prix,
                    "Adresse": adresse11,
                    "Lien des images":image_full1
                }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame( data)
        df = pd.concat([df,DF], axis = 0).reset_index(drop = True)
        
        #Remplacer les valeurs manquantes par la médiane dans df
        for col in df[:]:
            if df[col].dtype != "object":   # Si la colonne est numérique → remplacer NA par médiane
                df[col].fillna(df[col].median(), inplace = True)
            else:  # Si la colonne est une chaine de caractère → remplacer NA par "N/A"
                df[col] = df[col].fillna("N/A")
    return df


# In[244]:


#Fonction pour web scraping chaussure homme
def load_chaussure_enfants_data(mul_page):
    # create a dataframe vide df
    df = pd.DataFrame()
    # Parcourir les indexes des différents pages 
    for index_page in range(1,int(mul_page)+1):
        url = f"https://sn.coinafrique.com/categorie/chaussures-enfants?page={index_page}"
    # récupération du contenu de la page
        res =get(url)
    # Avoir le contenu dans un objet bs et sparsifier
        soup = bs(res.content, "html.parser")
    # récupération des conteneurs
        containers = soup.find_all("div", class_="col s6 m4 l3")
    #scraper les données de tous les conteneurs
        data= []
        for container in containers:
            #url_container =  'https://sn.coinafrique.com' + container.find('a')['href'] # Recuperer l'url du sous_container
            # contenu html de la sous page
            #res_container = get(url_container)
            #soup_container = bs(res_container.content, 'html.parser')
            try:
     # scrape les données sur le type de chaussures
                type_chaussures = container.find('p', class_='ad__card-description').text.strip()
    # scrape les données sur le prix           
                prix = container.find('p', class_='ad__card-price').text.strip('CFA')
    # scrape les données sur l"adresse
                adresse11 = container.find("p", class_="ad__card-location").text.strip()

                #adresse = [
                 #   span['data-address']
                  #  for span in soup_container.find_all('span', class_='valign-wrapper')
                   # if 'data-address' in span.attrs]
                #adresse1 = list(dict.fromkeys(adresse))
                #adresse11 = str(adresse1)
                
    # scrape les données sur image_lien
                image_full1 = container.find("img")["src"]

                #url_image = [
                 #   div['style'].split('url(')[1].split(')')[0]
                  #  for div in soup_container.find_all('div', class_='swiper-slide')
                   # if 'style' in div.attrs
                #]      
                #url_image = list(dict.fromkeys(url_image))
                #image_full = [img for img in url_image if "thumb_" not in img]
                #image_full1 = str(image_full)
                
                dic = {"Type de chaussures": type_chaussures, "Prix": prix, "Adresse": adresse11, "Lien des images":image_full1
                      }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame( data)
        df = pd.concat([df,DF], axis = 0).reset_index(drop = True)
        
        #Remplacer les valeurs manquantes par la médiane dans df
        for col in df[:]:
            if df[col].dtype != "object":   # Si la colonne est numérique → remplacer NA par médiane
                df[col].fillna(df[col].median(), inplace = True)
            else:  # Si la colonne est une chaine de caractère → remplacer NA par "N/A"
                df[col] = df[col].fillna("N/A")
    return df


# In[245]:


#titre dans la barre latérale gauche de l’application Streamlit
st.sidebar.header('User Input Features')
#selectionneur du nombre de page
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 600)]))
#selectionneur des fonctions d'application
Choices = st.sidebar.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data', 'Evaluate the App'])


#image de fond
add_bg_from_local('img_file3.jpg') 
#choix du fichier CSS
#local_css('style.css')  


# In[250]:


if Choices=='Scrape data using beautifulSoup':

    Vetement_homme_data_mul_pag = load_vetement_homme_data(Pages)
    Chaussure_homme_data_mul_pag = load_chaussure_homme_data(Pages)
    Vetement_enfants_data_mul_pag = load_vetement_enfants_data(Pages)
    Chaussure_enfants_data_mul_pag = load_chaussure_enfants_data(Pages)
    
    
    load(Vetement_homme_data_mul_pag, 'Vetement homme data', '1', '101')
    load(Chaussure_homme_data_mul_pag, 'Chaussure homme data', '2', '102')
    load(Vetement_enfants_data_mul_pag, 'Vetement enfants data', '3', '103')
    load(Chaussure_enfants_data_mul_pag, 'Chaussure enfants data', '4', '104')

elif Choices == 'Download scraped data': 
    
    Vetements_homme = pd.read_csv('vetements_homme_data.csv')
    Chaussures_homme = pd.read_csv('chaussures_homme_data.csv')
    Vetements_enfants = pd.read_csv('vetements_enfants_data.csv')
    Chaussures_enfants = pd.read_csv('chaussures_enfants_data.csv')
    

    load(Vetements_homme, 'vetements homme data', '1', '101')
    load(Chaussures_homme, 'chaussures homme data', '2', '102')
    load(Vetements_enfants, 'vetements enfants data', '3', '103')
    load(Chaussures_enfants, 'chaussures enfants data', '4', '104')

elif  Choices == 'Dashbord of the data': 
#chagement des 4 bases de données
    
    df1 = pd.read_csv('vetements_homme_data.csv')
    df2 = pd.read_csv('chaussures_homme_data.csv')
    df3 = pd.read_csv('vetements_enfants_data.csv')
    df4 = pd.read_csv('chaussures_enfants_data.csv')

#Uniformiser le nom de la colonne 'type'
    df1 = df1.rename(columns={"type habits": "type"})
    df2 = df2.rename(columns={"type chaussures": "type"})
    df3 = df3.rename(columns={"type habits": "type"})
    df4 = df4.rename(columns={"type chaussures": "type"})
    
# Netoyage de la colonne prix
    def clean_price(df):
        df["prix"] = df["prix"].replace(
            ["Prix sur demande", ""],
            pd.NA
        )
    
    
        df["prix_num"] = pd.to_numeric(
            df["prix"]
            .str.replace("CFA", "", regex=False)
            .str.replace(" ", "", regex=False),
            errors="coerce"
        )
        return df

    df1 = clean_price(df1)
    df2 = clean_price(df2)
    df3 = clean_price(df3)
    df4 = clean_price(df4)
        
# Fonction pour calculer le prix moyen
    def prix_moy(df):
        return (
            df
            .groupby("type")["prix_num"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        
    prix_moy1 = prix_moy(df1)
    prix_moy2 = prix_moy(df2)
    prix_moy3 = prix_moy(df3)
    prix_moy4 = prix_moy(df4)

#Affichage des 4 graphiques

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Vêtements Homme")
        fig1 = plt.figure(figsize=(8,5))
        prix_moy1.plot(kind="bar")
        plt.ylabel("Prix moyen (CFA)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig1)

    with col2:
        st.subheader("Chaussures Homme")
        fig2 = plt.figure(figsize=(8,5))
        prix_moy2.plot(kind="bar")
        plt.ylabel("Prix moyen (CFA)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig2)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Vêtements Enfants")
        fig3 = plt.figure(figsize=(8,5))
        prix_moy3.plot(kind="bar")
        plt.ylabel("Prix moyen (CFA)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig3)

    with col4:
        st.subheader("Chaussures Enfants")
        fig4 = plt.figure(figsize=(8,5))
        prix_moy4.plot(kind="bar")
        plt.ylabel("Prix moyen (CFA)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig4)

else :
    # components.html("""
    # <iframe src="https://ee.kobotoolbox.org/i/y3pfGxMz" width="800" height="1100"></iframe>
    # """,height=1100,width=800)
    st.markdown("<h3 style='text-align: center;'>Donner votre Feedback</h3>", unsafe_allow_html=True)

    # centrer les deux boutons
    col1, col2 = st.columns(2)
#ouverture formulaire kobocollect
    with col1:
        st.markdown(
            '<a href="https://ee.kobotoolbox.org/x/b8hnbb02" target="_blank">'
            '<button style="width:100%">Kobo Evaluation Form</button>'
            '</a>',
            unsafe_allow_html=True
        )
    
#ouverture formulaire google form
    with col2:
        st.markdown(
            '<a href="https://docs.google.com/forms/d/e/1FAIpQLSdmulYTWrXgeza6qtJrMZpr-qvJ_Na1v9JG2Tv0-6e0TK8l9Q/viewform" target="_blank">'
            '<button style="width:100%">Google Forms Evaluation</button>'
            '</a>',
            unsafe_allow_html=True
    )



# In[ ]:




