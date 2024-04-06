import pandas as pd
from functions_for_animes import *
import matplotlib.pyplot as plt

anime_titles = get_anime_titles()

# anime_infos = get_new_data_from_api(anime_titles)

anime_infos = get_data_from_file()

df = create_dataframe_from_animeinfo(anime_infos)
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

covid_filter_df = df[df["release_date"].dt.year.between(2020, 2022)]
covid_filter_df.loc[:, "rating"] = pd.to_numeric(covid_filter_df["rating"], errors="coerce")
covid_avarage = covid_filter_df["rating"].mean()
print("COVID átlag:", covid_avarage)

pre_covid_filter_df = df[df["release_date"].dt.year.lt(2020)]
pre_covid_filter_df.loc[:, "rating"] = pd.to_numeric(pre_covid_filter_df["rating"], errors = "coerce")
pre_covid_avarage = pre_covid_filter_df["rating"].mean()
print("Pre-COVID átlag:", pre_covid_avarage)

post_covid_filter_df = df[df["release_date"].dt.year.gt(2022)]
post_covid_filter_df.loc[:, "rating"] = pd.to_numeric(post_covid_filter_df["rating"], errors = "coerce")
post_covid_avarage = post_covid_filter_df["rating"].mean()
print("Post-COVID átlag:", post_covid_avarage)




average_ratings = [pre_covid_avarage, covid_avarage, post_covid_avarage]
periods = ['Pre-COVID', 'COVID', 'Post-COVID']


plt.bar(periods, average_ratings, color=['blue', 'orange', 'green'])
plt.title('Átlagos értékelés COVID előtt, alatt és után')
plt.xlabel('Időszak')
plt.ylabel('Átlagos értékelés')
plt.show()
  
         



                           

