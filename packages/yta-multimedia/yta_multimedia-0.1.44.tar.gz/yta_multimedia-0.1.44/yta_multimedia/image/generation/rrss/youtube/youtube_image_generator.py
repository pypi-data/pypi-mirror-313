from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.temp import create_temp_filename
from yta_multimedia.resources import Resource
from selenium.webdriver.common.by import By
from PIL import Image
from random import randrange
from typing import Union
from time import strftime, gmtime


class YoutubeImageGenerator:
    @staticmethod
    def generate_comment(author: str = None, avatar_url: str = None, time: str = None, message: str = None, likes_number: int = None, output_filename: Union[str, None] = None):
        """
        This method generates a Youtube comment image with the provided
        information. It will return the image read with PIL, but will
        also store the screenshot (as this is necessary while processing)
        with the provided 'output_filename' if provided, or with as a
        temporary file if not.
        """
        if not author:
            # TODO: Fake author name (start with @)
            author = 'Juanillo'

        if not avatar_url:
            # TODO: Fake avatar_url or just let the one existing
            avatar_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmIVOqsYK3t8HxkQ_WjwPoP2cwJiV1xDyWIw&s'

        if not time:
            # TODO: Fake time ('hace X años,meses,dias,horas')
            time = 'hace 3 horas'

        if not message:
            # TODO: Fake a message with AI
            message = 'Esto es un mensaje de ejemplo, fakeado, pasa el tuyo propio por favor.'

        if not likes_number:
            likes_number = randrange(50)

        scrapper = ChromeScrapper(False)
        # We go to this specific video with comments available
        scrapper.go_to_web_and_wait_util_loaded('https://www.youtube.com/watch?v=OvUj2WsADjI')
        # We need to scroll down to let the comments load
        # TODO: This can be better, think about a more specific strategy
        # about scrolling
        scrapper.scroll_down(1000)
        scrapper.wait(1)
        scrapper.scroll_down(1000)
        scrapper.wait(1)

        # We need to make sure the comments are load
        scrapper.find_element_by_element_type_waiting('ytd-comment-thread-renderer')
        comments = scrapper.find_elements_by_element_type('ytd-comment-thread-renderer')

        comment = comments[2]
        body = comment.find_element(By.ID, 'body')

        # Change user (avatar) image
        image = body.find_element(By.ID, 'img')
        scrapper.set_element_attribute(image, 'src', avatar_url)
        # TODO: Check that Image actually changes in the view
        # maybe with this: https://stackoverflow.com/questions/44286061/how-to-check-that-the-image-was-changed-if-therere-no-changes-in-html-code

        # Change date
        time_element = body.find_element(By.ID, 'published-time-text')
        time_element = scrapper.find_element_by_element_type('a', time_element)
        scrapper.set_element_inner_text(time_element, time)

        # Change user name
        author_element = body.find_element(By.ID, 'header-author')
        author_element = scrapper.find_element_by_element_type('h3', author_element)
        author_element = scrapper.find_element_by_element_type('a', author_element)
        author_element = scrapper.find_element_by_element_type('span', author_element)
        scrapper.set_element_inner_text(author_element, author)

        # Change message
        message_element = scrapper.find_element_by_id('content-text', comment)
        message_element = scrapper.find_element_by_element_type('span', message_element)
        scrapper.set_element_inner_text(message_element, message)

        # Change number of likes
        likes_element = scrapper.find_element_by_id('vote-count-middle', comment)
        scrapper.set_element_inner_text(likes_element, str(likes_number))
        
        scrapper.scroll_to_element(comment)
        
        filename = output_filename
        if not filename:
            filename = create_temp_filename('tmp_comment_screenshot.png')
        
        style = 'width: 500px; padding: 10px;'
        scrapper.set_element_style(comment, style)
        scrapper.screenshot_element(comment, filename)

        return Image.open(filename)

    @staticmethod
    def generate_thumbnail(title: str = None, image_url: str = None, channel_name: str = None, channel_image_url: str = None, duration_in_seconds: int = None, views: str = None, time_since_publication: str = None, output_filename: Union[str, None] = None):
        if not title:
            # TODO: Fake it
            title = 'Título de la miniatura'

        if not image_url:
            # TODO: Fake it
            image_url = 'https://static-cse.canva.com/blob/1697393/1600w-wK95f3XNRaM.jpg'

        if not channel_name:
            # TODO: Fake it
            channel_name = 'Youtube Autónomo'

        if not channel_image_url:
            # TODO: Fake it
            channel_image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmIVOqsYK3t8HxkQ_WjwPoP2cwJiV1xDyWIw&s'

        if not duration_in_seconds:
            duration_in_seconds = randrange(300, 700)

        if not views:
            # TODO: Fake it
            views = '2.3M visitas'

        if not time_since_publication:
            # TODO: Fake it
            time_since_publication = 'hace 2 horas'

        scrapper = ChromeScrapper()
        # Go to https://thumbnailchecker.com/es
        scrapper.go_to_web_and_wait_util_loaded('https://thumbnailchecker.com/es')

        # Fill info (we need it to be able to see the modal)
        title_input = scrapper.find_element_by_class('input', 'form_input')
        title_input.send_keys('Título de prueba')
        upload_input = scrapper.find_element_by_id('upload')
        # This is just an Image to set it, but then we change
        # it for the real one
        filename = Resource.get('https://drive.google.com/file/d/1rcowE61X8c832ynh0xOt60TH1rJfcJ6z/view?usp=drive_link', 'base_thumbnail.png')
        scrapper.set_file_input(upload_input, f'{get_project_abspath()}{filename}')

        button = scrapper.find_element_by_text_waiting('button', 'Revisa tu miniatura')
        scrapper.scroll_to_element(button)
        button.click()

        thumbnail_container_element = scrapper.find_element_by_class_waiting('div', 'yt_main_box')

        # Image
        image = scrapper.find_element_by_class('div', 'yt_box_thumbnail', thumbnail_container_element)
        image = scrapper.find_element_by_element_type('div', image)
        image = scrapper.find_element_by_element_type('img', image)
        scrapper.set_element_attribute(image, 'src', image_url)
        # TODO: Wait loading (?)

        # Avatar image
        avatar_image = scrapper.find_element_by_class('div', 'yt_box_info_avatar', thumbnail_container_element)
        avatar_image = scrapper.find_element_by_element_type('img', avatar_image)
        scrapper.set_element_attribute(avatar_image, 'src', channel_image_url)
        # TODO: Wait loading (?)

        # Video duration (in 'MM:SS' format)
        video_duration_element = scrapper.find_element_by_class('span', 'yt_time_status')
        duration_str = strftime('%M:%S', gmtime(duration_in_seconds))
        if duration_in_seconds >= 3600:
            duration_str = strftime('%H:%M:%S', gmtime(duration_in_seconds))
            if duration_in_seconds < 36000:
                # We need to set hour as one only digit
                duration_str = duration_str[1:]
        scrapper.set_element_inner_text(video_duration_element, duration_str)

        # Title
        description = scrapper.find_element_by_class('div', 'yt_box_info_content', thumbnail_container_element)
        title_element = scrapper.find_element_by_element_type('h4', description)
        scrapper.set_element_inner_text(title_element, title)

        # Author
        user = scrapper.find_element_by_element_type('p', description)
        scrapper.set_element_inner_text(user, channel_name)

        # Views
        views_element = scrapper.find_element_by_class('div', 'yt_box_info_meta', thumbnail_container_element)
        ul = scrapper.find_element_by_element_type('ul', views_element)
        listed_items = scrapper.find_elements_by_element_type('li', ul)
        # TODO: Handle 'views' and 'time_since_publication' with int
        # and format it manually here
        scrapper.set_element_inner_text(listed_items[1], views)
        scrapper.set_element_inner_text(listed_items[2], time_since_publication)

        style = 'width: 500px; padding: 10px;'
        scrapper.set_element_style(thumbnail_container_element, style)

        if not output_filename:
            output_filename = create_temp_filename('tmp_youtube_thumbnail.png')

        scrapper.screenshot_element(thumbnail_container_element, output_filename)

        return Image.open(output_filename)