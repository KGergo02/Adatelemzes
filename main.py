import pandas as pd
from functions_for_animes import *

anime_titles = get_anime_titles()

anime_infos = get_new_data(anime_titles)

print(anime_infos)
