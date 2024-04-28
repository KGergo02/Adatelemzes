from functions_for_animes import *
import matplotlib.pyplot as plt


if __name__ == '__main__':

    # ids = get_anime_ids()
    #
    # anime_infos = get_new_data_from_api(ids)

    # noinspection PyRedeclaration
    anime_infos = get_data_from_file()

    df = create_dataframe_from_model(anime_infos)

    df = df.sort_values(by="news_sum", ascending=False)

    print(df)


    
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    news_per_year = df.groupby('year')['news_sum'].sum()

    df.dropna(inplace=True)
    highest_rated_anime = df[df['rating'] == df['rating'].max()]
    

    plt.figure(figsize=(10, 6))
    news_per_year.plot(kind='line', marker='o')
    plt.title('Évenkénti hírek száma')
    plt.xlabel('Év')
    plt.ylabel('Hírek száma')
    plt.grid(True)
    plt.show()	
    


    



    
    df.sort_values(by='release_date', inplace=True)

    plt.figure(figsize=(10, 6))
    plt.plot(df['release_date'], df['rating'], marker='o', label='Értékelés')
    plt.plot(df['release_date'], df['news_sum'], marker='o', label='Hírek száma')
    plt.title('Animek értékelése és hírek száma az idő múlásával')
    plt.xlabel('Megjelenés dátuma')
    plt.ylabel('Értékelés / Hírek száma')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45) 
    plt.tight_layout()
    plt.show()
    
    
     
    df['anime_age'] = 2024 - df['release_date'].dt.year

    plt.figure(figsize=(10, 6))
    plt.scatter(df['anime_age'], df['news_sum'], color='b', alpha=0.5)
    plt.title('Anime korának és kapott hírek számának összefüggése')
    plt.xlabel('Anime kora (év)')
    plt.ylabel('Kapott hírek száma')
    plt.grid(True)

    plt.tight_layout()
    plt.show()  

    

    
    # create_plot_rating(df)
