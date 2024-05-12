from functions_for_animes import *
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud
from bs4 import BeautifulSoup

if __name__ == '__main__':

    # ids = get_anime_ids()
    #
    # anime_infos = get_new_data_from_api(ids)

    # noinspection PyRedeclaration
    anime_infos = get_data_from_file()

    df = create_dataframe_from_model(anime_infos)

    df = df.sort_values(by="news_sum", ascending=False)

    #print(df)

    
    
    #font preset ha szükséges
    font = {'family': 'sans-serif',
            'weight': 'bold',
            'size': 12}

    #Ha véletlen valami rossz adat lenne a ratingbe, átalakítjuk számokká és ha hiba lépne fel a folyamatban, azt helyettesítjük NaN-rel, amiket később kidobunk
    #A release_date oszlopot dátum - idő objektumokká konvertáljuk, hasonlóan a ratinghez, itt is a hibás konverziót NaN-rel helyettesítjük, majd azokat kidobjuk
    #Ez azért kell, hogy birjunk jó típusú adatokkal dolgozni az elemzés közben   
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df.dropna(subset=['rating'], inplace=True)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df.dropna(subset=['release_date'], inplace=True)

    
    
    
    #kiszámoljuk, hogy hány éves az animé
    df['anime_age'] = 2024 - df['release_date'].dt.year
    

    #Szórásdiagramot hozunk létre, ami az animé korának és a kapott hírek számának összefüggését ábrázolja
    #Különböző paramétereket állítunk be, a vizualizálás érdekében, ami minden további plotra is igaz.
    plt.rc('font', **font) 
    plt.figure(figsize=(8, 12),)
    plt.scatter(df['anime_age'], df['news_sum'], color='red', edgecolors='red', linewidths=5, alpha=0.7)
    plt.title('ANIME KORÁNAK ÉS A KAPOTT HÍREK SZÁMÁNAK ÖSSZEFÜGGÉSE', fontweight = 'bold', fontsize = 15)
    plt.xlabel('ANIME KORA', fontweight = 'bold')
    plt.ylabel('HÍREK SZÁMA', fontweight = 'bold')
    plt.grid(True)
    plt.grid(color = 'red', alpha = 0.2)
    plt.show()
    



    
    
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    top_10_rating = df.nlargest(10, 'rating')

    plt.rc('font', **font) 
    plt.figure(figsize=(10, 10))
    plt.bar(top_10_rating['name'], top_10_rating['rating'], color='purple', edgecolor='black', linewidth=1)
    plt.title('TOP 10 LEGJOBB ÉRTÉKELÉSŰ ANIMÉK', fontweight = 'bold', fontsize = 15)
    
    plt.xticks(rotation=45, ha='right') 
    plt.yticks(range(1, 11)) 
    plt.grid(False)
    plt.tight_layout()
    plt.show()
    
    
    
    
    
    top_10_news = df.nlargest(10, 'news_sum')
    
    
    plt.figure(figsize=(10, 12))
    plt.bar(top_10_news['name'], top_10_news['news_sum'], color='skyblue',  edgecolor='black', linewidth=1)
    
    plt.ylabel('Hírek száma', fontweight = 'bold')
    plt.title('TOP 10 ANIME A LEGTÖBB HÍRREL', fontweight = 'bold', fontsize = 15)
    plt.xticks(rotation=45, ha='right', fontweight = 'bold')
    plt.tight_layout()
    plt.show()
    


    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    news_per_year = df.groupby('year')['news_sum'].sum()
    

    
    
    highest_rated_anime = df[df['rating'] == df['rating'].max()]
    
    
    
    
    df['year'] = df['release_date'].dt.year
    df_10_years = df.groupby('year')['news_sum'].sum().tail(10)
    
    plt.figure(figsize=(10, 6))
    df_10_years.plot(kind='bar', color='green', edgecolor='black', linewidth=1)
    plt.title('HÍREK SZÁMA AZ ELMÚLT 10 ÉVBEN', fontweight = 'bold', fontsize = 15)
    plt.grid(False)
    plt.show()
    

    
    theme_counts = df['themes'].explode().value_counts()
    top_10_themes = theme_counts.head(10)
    plt.figure(figsize=(10, 6))
    plt.scatter(top_10_themes.index, top_10_themes.values, s=100, color='green')
    plt.title('LEGGYAKORIBB TÉMÁK', fontweight='bold', fontsize=15)
    plt.yticks(range(0, max(top_10_themes.values) + 5, 5))
    plt.grid(True)
    plt.grid(color = 'green', alpha = 0.3)
    plt.tight_layout()
    plt.show()

    
    genre_counts = df['genres'].explode().value_counts()
    top_10_genres = genre_counts.head(10)
    plt.figure(figsize=(10, 6))
    plt.scatter( top_10_genres.index,  top_10_genres.values, s=100, color='blue')    
    plt.title('LEGGYAKORIBB MŰFAJOK', fontweight='bold', fontsize=15)
    plt.yticks(range(0, max(top_10_genres.values) +50, 50))
    plt.grid(True)
    plt.grid(color = 'blue', alpha = 0.3)
    plt.tight_layout()
    plt.show()
    
    
    all_news = ' '.join(str(news) for news in df['news']) 
    stopwords = ['cite', 'Cite']  
    wordcloud = WordCloud(max_words=50, max_font_size=100, min_font_size=10, prefer_horizontal=0.8, background_color='black', stopwords=stopwords).generate(all_news)
    plt.figure(figsize=(12, 6), facecolor='black')
    plt.imshow(wordcloud, interpolation='bilinear')
    
    plt.axis('off')
    plt.show()
    






    # create_plot_rating(df)
