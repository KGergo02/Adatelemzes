from functions_for_animes import *
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


if __name__ == '__main__':

    # ids = get_anime_ids()
    #
    # anime_infos = get_new_data_from_api(ids)

    # noinspection PyRedeclaration
    anime_infos = get_data_from_file()

    df = create_dataframe_from_model(anime_infos)

    df = df.sort_values(by="news_sum", ascending=False)

    print(df)

    


    font = {'family': 'sans-serif',
            'weight': 'bold',
            'size': 12}

    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df.dropna(subset=['rating'], inplace=True)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df.dropna(subset=['release_date'], inplace=True)

    
    
    
    
    df['anime_age'] = 2024 - df['release_date'].dt.year
    
    plt.rc('font', **font) 
    plt.figure(figsize=(8, 12),)
    plt.scatter(df['anime_age'], df['news_sum'], color='red', edgecolors='red', linewidths=5, alpha=0.7)
    plt.title('ANIME KORÁNAK ÉS A KAPOTT HÍREK SZÁMÁNAK ÖSSZEFÜGGÉSE', fontweight = 'bold', fontsize = 15)
    plt.xlabel('ANIME KORA', fontweight = 'bold')
    plt.ylabel('HÍREK SZÁMA', fontweight = 'bold')
    plt.grid(True)
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
    
    plt.rc('font', **font)
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
    
    

    






    



    


    
    
    # create_plot_rating(df)
