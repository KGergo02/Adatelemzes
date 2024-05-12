import json
from datetime import datetime
import pandas as pd
import time
import requests
import xmltodict
from anime_info import AnimeInfo
import matplotlib.pyplot as plt


def get_new_data_from_api(items):
    """
    Feltölt, majd visszaad egy listát animék adataival. Az adatokat az Anime News Network API biztosítja.

    :param items: Lista animék azonosítóival

    :returns: Új lista, amiben AnimeInfo típusú objectek vannak
    """

    animes = []

    query_string = ""

    step = 50

    DELAY = 1.1

    ct = 1

    open("animeinfodata.json", 'w', encoding="UTF-16").close()

    while len(items) > 0:

        if len(items) < 50:
            step = len(items)

        batch = items[:step]

        for item in batch:
            query_string += f"anime={item}&"

        query_string = query_string[:len(query_string) - 1]

        current_res = requests.get(f"https://cdn.animenewsnetwork.com/encyclopedia/api.xml?{query_string}")

        anime_infos = xmltodict.parse(current_res.content)

        for anime in anime_infos["ann"]["anime"]:

            anime_id = int(anime.get("@id"))

            anime_name = anime.get("@name")

            anime_rating = "NA"

            anime_release_date = "NA"

            anime_news = []

            anime_genres = []

            anime_themes = []

            related_animes = []

            # animék előző szezonjainak az azonosítóikat kigyűjtjük az alábbi kóddal

            if "related-prev" in anime:
                if isinstance(anime["related-prev"], dict):
                    rel = anime["related-prev"]["@rel"]

                    if rel == "remake of":
                        anime_id = int(anime["related-prev"]["@id"])
                    if rel != "adapted from":
                        if anime["related-prev"]["@id"] != anime_id:
                            related_animes.append(int(anime["related-prev"]["@id"]))
                else:
                    for rel in anime["related-prev"]:
                        if rel["@rel"] == "remake of":
                            anime_id = int(rel["@id"])
                        if rel["@rel"] != "adapted from":
                            if rel["@id"] != anime_id:
                                related_animes.append(int(rel["@id"]))

            # animék következő szezonjainak az azonosítóikat kigyűjtjük az alábbi kóddal

            if "related-next" in anime:
                if isinstance(anime["related-next"], dict):
                    related_animes.append(int(anime["related-next"]["@id"]))
                else:
                    for rel in anime["related-next"]:
                        related_animes.append(int(rel["@id"]))

            # értékelések kigyűjtése

            if "ratings" in anime:
                anime_rating = anime["ratings"]["@weighted_score"]

            # kiadási dátum, műfajok és témák kigyűjtése

            if 'info' in anime:
                if isinstance(anime["info"], list):
                    for info in anime["info"]:
                        if info["@type"] == "Vintage":
                            anime_release_date = info["#text"]
                        if info["@type"] == "Genres":
                            anime_genres.append(info["#text"])
                        if info["@type"] == "Themes":
                            anime_themes.append(info["#text"])
                else:
                    if anime["info"]["@type"] == "Vintage":
                        anime_release_date = anime["info"]["#text"]
                    if anime["info"]["@type"] == "Genres":
                        anime_genres.append(anime["info"]["#text"])
                    if anime["info"]["@type"] == "Themes":
                        anime_themes.append(anime["info"]["#text"])

            # konkrét hírek kigyűjtése

            if "news" in anime:
                if isinstance(anime["news"], list):
                    for news in anime["news"]:
                        anime_news.append(news["#text"])
                else:
                    anime_news.append(anime["news"]["#text"])

            # modellt készítünk belőle a könnyebb kezelhetőség érdekében

            current_anime = AnimeInfo(anime_id, anime_name, anime_rating, anime_release_date, anime_news, anime_genres,
                                      anime_themes, related_animes)

            animes.append(current_anime)

        print(f"#### Batch #{ct} complete ####")

        ct += 1

        query_string = ""

        items = items[step:]

        time.sleep(DELAY)

    print("#### Batching completed ####")

    write_data_to_file(animes)

    return animes


def get_anime_ids():
    """
    Visszaadja az összes animének az id-jét, ami megtalálható a weboldalon (Anime News Network)

    :return: Új lista, amiben animék azonosítói szerepelnek
    """

    res = requests.get("https://cdn.animenewsnetwork.com/encyclopedia/reports.xml?id=155&type=anime&nlist=all")

    reports_dict = xmltodict.parse(res.content)

    anime_ids = []

    for report in reports_dict["report"]["item"]:
        anime_ids.append(int(report["id"]))

    return anime_ids


def create_dataframe_from_model(items):
    """
    Dataframe-t készítünk az animék listájából. Az adatokat feldolgozzuk, megszámoljuk a hírek számát és az értékelésekből átlagot számolunk.
    :param items: Animék listája saját modellként
    :return: Dataframe
    """

    names, release_dates, ratings, related_news_appearances, news, genres, themes = [], [], [], [], [], [], []

    for item in items:
        news_sum, news_var, genres_var, themes_var, date = count_anime_related_news_appearances(item, items, item.related)
        news.append(news_var)
        genres.append(genres_var)
        themes.append(themes_var)
        related_news_appearances.append(item.get_news_count() + news_sum)
        names.append(item.name)
        release_dates.append(date)
        ratings.append(item.rating)

    df = pd.DataFrame(list(zip(names, release_dates, ratings, news, genres, themes, related_news_appearances)),
                      columns=["name",
                               "release_date",
                               "rating",
                               "news",
                               "genres",
                               "themes",
                               "news_sum",
                               ])

    # Ez az a beállítás, amivel az összes oszlop látszódik, ha kiírjuk a dataframet
    # pd.set_option('display.max_columns', None)

    # Ugyan az, csak sorokkal

    pd.set_option('display.max_rows', None)

    return df


def count_anime_related_news_appearances(anime, animes, ids):
    """
    :param anime: A jelenlegi anime
    :param animes: A teljes anime lista
    :param ids: Az összes olyan azonosító, ami tartozik a jelenlegi animéhez
    :return: Tuple-t ad vissza, ami a hírek számából, konkrét hírekből, műfajokból, témákból és dátumokból áll.
    """

    id_set = set(ids)

    replace_useless_date(anime)

    # Ha nincs az animéhez folytatás vagy multiple season
    if len(ids) == 0:
        if anime.release_date != "NA":
            return len(anime.news), set(anime.news), set(anime.genres), set(anime.themes), str(datetime.strptime(anime.release_date, determine_datetime_format(anime.release_date)))[0:10]
        else:
            return len(anime.news), set(anime.news), set(anime.genres), set(anime.themes), "NA"

    news = set(anime.news)

    genres = set(anime.genres)

    themes = set(anime.themes)

    current_animes = [item for item in animes if item.id in id_set]

    for item in current_animes:
        item_id_set = set(item.related)
        id_set = id_set | item_id_set

    # Szűrök az id_set alapján az animes listára.
    selected_animes = set([item for item in animes if item.id in id_set])

    selected_animes.add(anime)

    id_set.clear()

    title = anime.name

    min_id = min([int(item.id) for item in selected_animes])

    ratings = 0.0

    rating_counter = 0.0

    if anime.release_date != "NA":
        min_date = datetime.strptime(str(anime.release_date), determine_datetime_format(str(anime.release_date)))
    else:
        min_date = datetime.strptime("9999-12-31", "%Y-%m-%d")

    if anime.id < min_id:
        title = anime.name
    else:
        for item in selected_animes:
            replace_useless_date(item)
            if item.rating != "NA":
                ratings += float(item.rating)
                rating_counter += 1.0
            if item.id == min_id:
                title = item.name
            if item.release_date != "NA" and datetime.strptime(item.release_date, determine_datetime_format(str(item.release_date))) < min_date:
                min_date = datetime.strptime(item.release_date, determine_datetime_format(str(item.release_date)))

    anime.name = title

    if rating_counter != 0:
        anime.rating = str(float(ratings / rating_counter))
    else:
        anime.rating = "0.0"

    for anime in selected_animes:

        if len(anime.news) != 0:
            news = news.union(set(anime.news))

        if len(anime.genres) != 0:
            genres = genres.union(set(anime.genres))

        if len(anime.themes) != 0:
            themes = themes.union(set(anime.themes))

        animes.remove(anime)

    return len(news), news, genres, themes, str(min_date)[0:10]


def determine_datetime_format(date):
    """
    Eldönti, hogy melyik dátum formátumot kell használni a paraméterből kapott értékre.
    :param date: Dátum
    :return: Korrekt dátum formátum
    """

    if len(date.split("-")) == 3:
        return "%Y-%m-%d"
    elif len(date.split("-")) == 2:
        return "%Y-%m"
    elif len(date.split("-")) == 1:
        return "%Y"


def replace_useless_date(anime):
    """
    Kitörli a felesleges karaktereket a dátumokból
    :param anime: Anime modell
    :return: A módosított dátum
    """

    if "(" in anime.release_date:
        anime.release_date = str.strip(anime.release_date.split("(")[0])
    if "to" in anime.release_date:
        anime.release_date = str.strip(anime.release_date.split("to")[0])
    return anime.release_date


def write_data_to_file(items):
    """
    Json fileba elmenti az Anime modellt
    :param items: Anime lista
    :return:
    """

    with open("animeinfodata.json", 'w', encoding="UTF-16") as file:
        json.dump([anime.to_dict() for anime in items], file, ensure_ascii=False, indent=4)


def get_data_from_file():
    """
    Kiolvassa a json fileból az adatokat
    :return: Animék listája
    """

    animes = []

    with open("animeinfodata.json", 'r', encoding="UTF-16") as file:
        data = json.load(file)

        for anime in data:
            item = AnimeInfo(anime["id"], anime["name"], anime["rating"], anime["release_date"], anime["news"],
                             anime["genres"], anime["themes"], anime["related"])
            animes.append(item)

    return animes


def create_plot_rating(df):
    """
    Animék értékeléséhez készít egy plotot, amin COVID időszakot vizsgálunk
    :param df: Dataframe
    :return:
    """

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