import pandas as pd
import time
import requests
import xmltodict
from anime_info import AnimeInfo


def get_new_data_from_api(items):
    """
    Feltölt, majd visszaad egy listát animék adataival. Az adatokat az Anime News Network API biztosítja.

    :param items: Lista animék neveivel

    :returns: Új lista, amiben AnimeInfo típusú objectek vannak
    """
    animes = []

    query_string = ""

    step = 50

    DELAY = 1.1

    ct = 1

    while len(items) > 0:

        if len(items) < 50:
            step = len(items)

        batch = items[:step]

        for item in batch:
            query_string += f"title=~{item}&"

        query_string = query_string[:len(query_string) - 1]

        current_res = requests.get(f"https://cdn.animenewsnetwork.com/encyclopedia/api.xml?{query_string}")

        anime_infos = xmltodict.parse(current_res.content)

        for anime in anime_infos["ann"]["anime"]:

            anime_name = "None"

            anime_ratings = "NaN"

            anime_release_date = "None"

            if "ratings" in anime:

                anime_name = anime["@name"]

                anime_ratings = anime["ratings"]["@weighted_score"]

                for info in anime["info"]:
                    if "@type" in info and info["@type"] == "Vintage":
                        anime_release_date = info["#text"]
                        break

                current_anime = AnimeInfo(anime_name, anime_ratings, anime_release_date)

                animes.append(current_anime)

        print(f"#### Batch #{ct} complete ####")

        ct += 1

        query_string = ""

        items = items[step:]

        time.sleep(DELAY)

    print("#### Batching completed ####")

    return animes


def get_anime_titles():
    """
    Visszaadja az összes animének a nevét, ami megtalálható a weboldalon (Anime News Network)

    :return: Új lista, amiben animék nevei szerepelnek
    """
    res = requests.get("https://cdn.animenewsnetwork.com/encyclopedia/reports.xml?id=155&type=anime&nlist=all")

    reports_dict = xmltodict.parse(res.content)

    anime_titles = []

    for report in reports_dict["report"]["item"]:
        if report["name"] not in anime_titles:
            anime_titles.append(report["name"])

    return anime_titles


def create_dataframe_from_animeinfo(items):

    names, release_dates, ratings = [], [], []

    for item in items:
        names.append(item.name)
        release_dates.append(item.release_date)
        ratings.append(item.rating)

    df = pd.DataFrame(list(zip(names, release_dates, ratings)), columns=["name", "release_date", "rating"])

    df["rating"] = df["rating"].str.replace('\n', '')

    return df

def write_data_to_file(items):
    with open("animeinfodata.csv", 'w', encoding="UTF-16") as file:
        for item in items:
            file.write(f"{item.name};{item.release_date};{item.rating}\n")


def get_data_from_file():

    animes = []

    with open("animeinfodata.csv", 'r', encoding="UTF-16") as file:

        for x in file:
            data = x.split(';')

            item = AnimeInfo(data[0], data[2], data[1])

            animes.append(item)

    return animes
