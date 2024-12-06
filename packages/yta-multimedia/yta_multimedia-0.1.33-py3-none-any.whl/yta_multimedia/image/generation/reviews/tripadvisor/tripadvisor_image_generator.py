from yta_general_utils.temp import create_temp_filename
from yta_general_utils.downloader import Downloader
from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from PIL import Image, ImageFont, ImageDraw, ImageOps
from random import randrange
from typing import Union

import textwrap
import numpy as np


# TODO: Maybe implement it as a Singleton like DiscordImageGenerator
# to be faster when reusing the scrapper for consecutive generations
class TripadvisorImageGenerator:
    def generate_review_manually(self, review: str = None, avatar_url: str = None, username: str = None, city: str = None, contributions_number: int = randrange(30), rating_stars: int = (randrange(5) + 1), title: str = None, output_filename: str = None):
        # TODO: This must be set by the user in .env I think
        __FONTS_PATH = 'C:/USERS/DANIA/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/'

        # TODO: Do more checkings please
        # TODO: Check contributions_number is in between 1 and 30 and is a number
        # TODO: Check rating_stars is a number between 1 and 5
        # TODO: Check title exists
        # TODO: Check review exists

        bold_font = ImageFont.truetype(__FONTS_PATH + 'HUMANIST_777_BOLD_BT.TTF', 22, encoding = 'unic')
        normal_font = ImageFont.truetype(__FONTS_PATH + 'HUMANIST-777-FONT.OTF', 16, encoding = 'unic')
        review_font = ImageFont.truetype(__FONTS_PATH + 'HUMANIST-777-FONT.OTF', 20, encoding = 'unic')

        # Create white review background (440 is h, 800 is w)
        img = np.zeros((440, 800, 3), dtype = np.uint8)
        img.fill(255)
        img = Image.fromarray(img).convert('RGBA')
        draw = ImageDraw.Draw(img)

        # Place avatar image circle at (24, 31)
        image_filename = create_temp_filename('tmp_avatar.png')
        if not avatar_url:
            avatar_url = 'https://avatar.iran.liara.run/public'
        Downloader.download_image(avatar_url, image_filename)
        avatar_image = Image.open(image_filename)

        # Make image fit and then mask with circle
        avatar_image = ImageOps.fit(avatar_image, (64, 64))
        mask = Image.new('L', avatar_image.size, 0)
        circle_draw = ImageDraw.Draw(mask)
        circle_draw.ellipse((0, 0, 64, 64), fill = 255)
        result = Image.new('RGBA', avatar_image.size, (255, 255, 255))
        result.paste(avatar_image, (0, 0), mask)

        img.paste(result, (24, 31))

        # I check if I need some fake information
        fake_data = None
        if not username or not city:
            # TODO: Move this below to a 'get_json_from_url' or similar
            # TODO: Create the new 'yta-data-provider' library and include this
            import requests
            response = requests.get('https://fakerapi.it/api/v1/persons?_locale=es_ES')
            data = response.json()
            fake_data = data['data'][0] # First person generated data

        # Put reviewer name at (103, 33)
        if not username:
            username = fake_data['firstname'] + ' ' + fake_data['lastname']
        draw.text((103, 33), username, font = bold_font, fill = (84, 84, 84), line_height = '19px', width = 700)
        
        # Write city and contributions at (103, 65)
        if not city:
            city = fake_data['address']['city']
        # TODO: Check contributions_number is a number
        draw.text((103, 65), city + ' · ' + str(contributions_number) + ' contribuciones', font = normal_font, fill = (84, 84, 84), line_height = '19px', width = 700)

        # Build the evaluation (in green circles) at (24, 126)
        def __draw_filled_ellipse(xy):
            return draw.ellipse(xy, fill = (0, 170, 108), outline = (0, 170, 108))
        def __draw_unfilled_ellipse(xy):
            return draw.ellipse(xy, fill = (255, 255, 255), outline = (0, 170, 108))
        
        x = 24
        for i in range(5):
            if i < rating_stars:
                __draw_filled_ellipse((x, 126, x + 24, 126 + 24))
            else:
                __draw_unfilled_ellipse((x, 126, x + 24, 126 + 24))
            x += 24 + 6

        # Place the review title at (24, 164)
        if not title:
            # TODO: Fake review title with AI
            title = 'Menuda pasada'
        draw.text((24, 164), title, font = bold_font, fill = (84, 84, 84), line_height = '19px')

        # Place the review date at (24, 199)
        # TODO: Implement 'date' parameter
        # TODO: Implement 'visit_type' options
        draw.text((24, 199), "jul 2019 · En pareja", font = normal_font, fill = (84, 84, 84), line_height = '19px')

        # Place the whole wrapped text starting at (24, 440 - 180)
        # See this: (https://gist.github.com/turicas/1455973) to wrap text
        if not review:
            # TODO: Fake review with AI
            review = 'Estuvimos todo el viaje pensando en que ibamos a poder visitar por fin este sitio, y la verdad es que no ha defraudado nada. Lo disfrutamos de principio a fin y la atención fue espectacular. Llevábamos unas espectativas bastante altas pero, sin lugar a dudas, las han superado. Encantados!!'
        lines = textwrap.wrap(review, width = 76)
        y_text = 440 - 180
        for line in lines:
            left, top, right, bottom = review_font.getbbox(line)
            height = bottom - top
            draw.text((24, y_text), line, font = review_font, fill = (84, 84, 84))
            y_text += height + 8

        # Place the number of likes: 700, 50
        #draw.text((700, 50), "3", font = normal_font, fill = (84, 84, 84), line_height = '19px')

        if not output_filename:
            output_filename = create_temp_filename('tmp_tripadvisor_review.png')
        img.save(output_filename, 'png')

        # TODO: Why not returning the image instead (?)
        return output_filename
    
    def generate_review(self, username: str = None, user_picture_url: str = None, title: str = None, message: str = None, rating: int = None, output_filename: Union[str, None] = None):
        if not username:
            # TODO: Fake it
            username = 'Gabriel de las Salinas'

        if not user_picture_url:
            # TODO: Fake it
            user_picture_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmIVOqsYK3t8HxkQ_WjwPoP2cwJiV1xDyWIw&s'

        if not title:
            # TODO: Fake it
            title = 'Estancia un poco aleatoria'

        if not message:
            # TODO: Fake it
            message = 'Este es un mensaje puesto a dedo en un comentario, que quiero que sea largo para que ocupe dos líneas a ser posible, y así lo veamos bien cómo quedaría.'

        if not rating:
            rating = randrange(1, 5)

        # TODO: Implement date
        # TODO: Implement review type ('Pareja', 'Solitario', 'Familia', etc.)

        if rating < 1:
            rating = 1
        elif rating > 5:
            rating = 5

        # I don't let manually handle this value (it is useless)
        contributions_number = randrange(1, 15)
        # TODO: Implement this in the future (maybe)
        # likes_number = 13

        # TODO: I don't know why this is not working without GUI
        scrapper = ChromeScrapper(True)
        scrapper.go_to_web_and_wait_util_loaded('https://www.tripadvisor.es/AttractionProductReview-g189180-d25382579-The_Unvanquished_Tour_in_Porto_City_Center-Porto_Porto_District_Northern_Portugal.html')
        # Get <div data-automation="reviewCard">
        review_element = scrapper.find_element_by_custom_tag_waiting('div', 'data-automation', 'reviewCard')
        review_card_divs = scrapper.find_elements_by_element_type('div', review_element, only_first_level = True)
        scrapper.scroll_to_element(review_element)
        scrapper.scroll_up(100)

        # User image url   divx8 > a > picture > img.src = new_url
        image_element = review_card_divs[0]
        for i in range(7):
            image_element = scrapper.find_element_by_element_type('div', image_element)
        image_element = scrapper.find_element_by_element_type('a', image_element)
        image_element = scrapper.find_element_by_element_type('div', image_element)
        image_element = scrapper.find_element_by_element_type('picture', image_element)
        image_element = scrapper.find_element_by_element_type('img', image_element)
        scrapper.set_element_attribute(image_element, 'src', user_picture_url)

        # Username   divx2 > div#1 (2o div) > span > a inner_text
        author_element = review_card_divs[0]
        author_element = scrapper.find_element_by_element_type('div', author_element)
        author_element = scrapper.find_elements_by_element_type('div', author_element, only_first_level = True)[1]
        # TODO: This [1] is doing div > div, not getting the second 
        # child in horizontal hierarchy
        author_element = scrapper.find_element_by_element_type('span', author_element)
        author_element = scrapper.find_element_by_element_type('a', author_element)
        scrapper.set_element_inner_text(author_element, username)

        # Contributions   divx2 > div#1 (2o div) > divx2 > span inner_text
        contributions_element = review_card_divs[0]
        contributions_element = scrapper.find_element_by_element_type('div', contributions_element)
        contributions_element = scrapper.find_elements_by_element_type('div', contributions_element, only_first_level = True)[1]
        contributions_element = scrapper.find_element_by_element_type('div', contributions_element)
        contributions_element = scrapper.find_element_by_element_type('div', contributions_element)
        contributions_element = scrapper.find_element_by_element_type('span', contributions_element)
        # 1 contribución, X contribuciones
        contributions_str = '1 contribución'
        if contributions_number > 1:
            contributions_str = str(contributions_number) + ' contribuciones'
        scrapper.set_element_inner_text(contributions_element, contributions_str)

        # Rating (starts alike)   div#1 (2o div) > svg > path (special)
        rating_element = review_card_divs[1]
        rating_element = scrapper.find_element_by_element_type('svg', rating_element)
        paths = scrapper.find_elements_by_element_type('path', rating_element)
        FILLED_CIRCLE_D_VALUE = 'M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z'
        UNFILLED_CIRCLE_D_VALUE = 'M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12zm0 2a9.983 9.983 0 019.995 10 10 10 0 01-10 10A10 10 0 012 12 10 10 0 0112 2z'
        for i in range(5):
            if rating > i:
                scrapper.set_element_attribute(paths[i], 'd', FILLED_CIRCLE_D_VALUE)
            else:
                scrapper.set_element_attribute(paths[i], 'd', UNFILLED_CIRCLE_D_VALUE)

        # Title   div#2 (3er div) > a > span inner_text
        title_element = review_card_divs[2]
        title_element = scrapper.find_element_by_element_type('a', title_element)
        title_element = scrapper.find_element_by_element_type('span', title_element)
        scrapper.set_element_inner_text(title_element, title)

        # Date and type of visit   div#3 (4o div) inner_text
        date_and_type_element = review_card_divs[3]
        # TODO: Work this below, please
        # Accepted values: Pareja, Familia
        # example: sept de 2024 • Familia
        date_and_type_str = 'sept de 2024 • Pareja'
        scrapper.set_element_inner_text(date_and_type_element, date_and_type_str)

        # Message (opinion)   div#4 (5o div) > div > div > span > span inner_text (with <br> please)
        message_element = review_card_divs[4]
        message_element = scrapper.find_element_by_element_type('div', message_element)
        message_element = scrapper.find_element_by_element_type('div', message_element)
        message_element = scrapper.find_element_by_element_type('span', message_element)
        message_element = scrapper.find_element_by_element_type('span', message_element)
        scrapper.set_element_inner_text(message_element, message)

        # Images is the div#4 (5o div) but it is empty if no pictures
        # and we don't care (by now) about this div, just to remove it
        scrapper.remove_element(review_card_divs[5])

        # Written date   div#5 (6o div) > div#0 inner_text
        written_date_element = review_card_divs[6]
        written_date_element = scrapper.find_element_by_element_type('div', written_date_element)
        # TODO: Handle this please
        written_date_str = 'Escrita el 2 de septiembre de 2024'
        scrapper.set_element_inner_text(written_date_element, written_date_str)

        # Tripadvisor disclaimer   div#5 (6o div) > div#1 inner_text
        tripadvisor_disclaimer_element = written_date_element = review_card_divs[len(review_card_divs) - 1]
        tripadvisor_disclaimer_element = scrapper.find_elements_by_element_type('div', written_date_element, only_first_level = True)[1]
        disclaimer_str = 'Esta es una opinión personal y no de la cuenta que publica este contenido.'
        scrapper.set_element_inner_text(tripadvisor_disclaimer_element, disclaimer_str)

        style = 'width: 500px; padding: 10px;'
        scrapper.set_element_style(review_element, style)

        if not output_filename:
            output_filename = create_temp_filename('tmp_youtube_thumbnail.png')

        scrapper.screenshot_element(review_element, output_filename)

        return Image.open(output_filename)
