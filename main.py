import pandas as pd
from functions_for_animes import *

anime_titles = get_anime_titles()

# anime_infos = get_new_data_from_api(anime_titles)
#
# write_data_to_file(anime_infos)

anime_infos = get_data_from_file()

df = create_dataframe_from_animeinfo(anime_infos)

print(df)
