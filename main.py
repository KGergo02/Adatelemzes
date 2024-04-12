from functions_for_animes import *

if __name__ == '__main__':

    ids = get_anime_ids()

    #anime_infos = get_new_data_from_api(ids)

    # noinspection PyRedeclaration
    anime_infos = get_data_from_file()

    df = create_dataframe_from_model(anime_infos)

    # create_plot_rating(df)
