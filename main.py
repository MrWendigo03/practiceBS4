# import requests
# from bs4 import BeautifulSoup
#
# TARGET_URL = "https://kinogo.biz"
# # print(requests.get(TARGET_URL).text)
# with open("kinogo.html", "w", encoding="utf-8") as file:
#     file.write(requests.get(TARGET_URL).text)
# content = requests.get(TARGET_URL).text
# page = BeautifulSoup(content, "html.parser")
# print(page.find("a"))
# first_film = page.get("a", attrs={"title": "Чёрный Адам (2022)"})
# print(first_film.get("href"))
#
# # def run(): #скачать с mover.uz
# #     commands = {
# #         "new_video_title": "Последние по видео",
# #         "all_categories": "Поиск по категории",
# #         "download_video": "Скачать"
# #     }-


import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://mover.uz/"

def get_and_convert_soup(url: str):
    return BeautifulSoup(requests.get(url).text, "html.parser")

def parse_video_page(page: BeautifulSoup):
    film_links = page.select(".video-list .video-item .item-info h5 a")
    films = []
    for film_obj in film_links:
        films.append({"name": film_obj.text, "link": film_obj["href"]})
    return films

def parse_categories(page: BeautifulSoup) -> dict:
    category_links = enumerate(
        page.select("#categories-menu ul.pure-menu-list li.pure-menu-item a"),
        start=1
    )
    categories = {}
    for index, category_obj in category_links:
        categories[index] = {"name": category_obj.text, "link": category_obj["href"]}
    return categories

def parse_video_link(page: BeautifulSoup):
    print(page.text)
    # print(page.select("#video-container #player pjsdiv pjsdiv video"))

def text_from_dict(source_dict: dict) -> str:
    return '\n'.join(map(
        lambda command: f"\t{command[0]}: {command[1]}",
        source_dict.items()
    ))

def validate_command(command: str):
    return command.isdigit() or len(command) == 1

def check_command(command_dict: dict, user_command) -> bool:
    return command_dict.get(int(user_command), False)

def run():
    commands = {
        1: "Скачать видеофайлы",
        2: "Информация о видео",
    }
    subcommand_text = text_from_dict(commands)
    user_command = input(f"Введите номер команды\n{subcommand_text}\nВвод: ")
    if not validate_command(user_command):
        print("Попробуй крч заново")
        return
    if not check_command(commands, user_command):
        print("Такой команды нет")
        return
    main_page = get_and_convert_soup(TARGET_URL)
    categories = parse_categories(main_page)
    text_list = []
    for key, category_dict in categories.items():
        text_list.append(f'\t{key}: {category_dict["name"]}')
    command_text = "\n".join(text_list)
    category_id = input(f"Выберите категорию видео:\n{command_text}\nВвод: ")
    if not validate_command(category_id):
        print("Попробуй крч заново")
        return
    if not check_command(categories, category_id):
        print("Такой категории нет")
        return
    category_page = get_and_convert_soup(categories[int(category_id)]["link"] + "/latest")
    page_videos = parse_video_page(category_page)
    film_names = "\n".join(map(
        lambda film: film["name"],
        page_videos
    ))
    input(f"Выберите фильм\n{film_names}")
    # for i in parse_video_page_links(page):
    #     print(i)
