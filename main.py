import requests
from functions_for_animes import *


anime_titles = get_anime_titles()

# anime_infos = get_new_data_from_api(anime_titles)

anime_infos = get_data_from_file()

df = create_dataframe_from_animeinfo(anime_infos)

create_plot_rating(df)

# bearer_token = "AAAAAAAAAAAAAAAAAAAAALm%2FtAEAAAAAZgtGWTGCIdIEVYicpCWj2v47ghI%3DU8W5eoR2qbnzPf6gQSWOdkPx6T9ox6TRVuRrGrus4aUXSiOyX2"
#
# hashtag = "#anime"
#
# url = "https://api.twitter.com/2/tweets/search/recent"
#
# params = {
#     'query': hashtag,
#     'tweet.fields': 'created_at'
# }
#
# headers = {
#     "Authorization": f"Bearer {bearer_token}",
#     "User-Agent": "v2FilteredStreamPython"
# }
#
# response = requests.request("GET", url, headers=headers, params=params)
#
# if response.status_code != 200:
#     raise Exception(response.status_code, response.text)
#
# print(response.json())

