import pandas as pd
import time
import requests
import xmltodict
from anime_info import AnimeInfo
import matplotlib.pyplot as plt

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

                if "info" in anime:
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

    write_data_to_file(animes)

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


def create_plot_rating(df):
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    covid_filter_df = df[df["release_date"].dt.year.between(2020, 2022)]
    covid_filter_df.loc[:, "rating"] = pd.to_numeric(covid_filter_df["rating"], errors="coerce")
    covid_avarage = covid_filter_df["rating"].mean()
    print("COVID átlag:", covid_avarage)

    pre_covid_filter_df = df[df["release_date"].dt.year.lt(2020)]
    pre_covid_filter_df.loc[:, "rating"] = pd.to_numeric(pre_covid_filter_df["rating"], errors="coerce")
    pre_covid_avarage = pre_covid_filter_df["rating"].mean()
    print("Pre-COVID átlag:", pre_covid_avarage)

    post_covid_filter_df = df[df["release_date"].dt.year.gt(2022)]
    post_covid_filter_df.loc[:, "rating"] = pd.to_numeric(post_covid_filter_df["rating"], errors="coerce")
    post_covid_avarage = post_covid_filter_df["rating"].mean()
    print("Post-COVID átlag:", post_covid_avarage)

    average_ratings = [pre_covid_avarage, covid_avarage, post_covid_avarage]
    periods = ['Pre-COVID', 'COVID', 'Post-COVID']

    bars = plt.bar(periods, average_ratings, color=['blue', 'orange', 'green'])

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, round(yval, 2), ha='center', va='bottom')  # Új sor

    plt.title('Átlagos értékelés COVID előtt, alatt és után')
    plt.xlabel('Időszak')
    plt.ylabel('Átlagos értékelés')
    plt.ylim(5, 7)
    plt.show()
