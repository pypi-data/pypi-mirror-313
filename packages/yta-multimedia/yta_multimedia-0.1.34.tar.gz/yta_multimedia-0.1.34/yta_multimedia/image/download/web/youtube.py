from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from yta_general_utils.temp import create_temp_filename
from PIL import Image

def download_youtube_video_comments(url: str, comments_number: int = 5):
    """
    This method downloads the 'comments_number' first comments (if
    available) of Youtube video of the provided 'url'. It will 
    scrap the web page and will screenshot those comments. The 
    amount of available comments in that video could be lower than
    the requested 'comments_number' or even zero.

    This method will return an array containing the images opened.
    If there are no comments in the provided video, the array will
    be empty.
    """
    if not url:
        raise Exception('No "url" provided.')
    
    # TODO: Check if url is a valid Youtube url

    if not comments_number:
        comments_number = 5

    scrapper = ChromeScrapper(False)
    # Example of url: 'https://www.youtube.com/watch?v=OvUj2WsADjI'
    scrapper.go_to_web_and_wait_util_loaded(url)
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

    if len(comments) >= comments_number:
        comments[:5]

    # We remove the header bar to avoid being over our comments in some cases
    youtube_top_bar = scrapper.find_element_by_id_waiting('masthead-container')
    scrapper.remove_element(youtube_top_bar)

    screenshots = []
    for comment in comments:
        # TODO: I need to close the 'No, gracias' 'Probar 1 mes' popup
        scrapper.scroll_to_element(comment)
        style = 'width: 500px; padding: 10px;'
        scrapper.set_element_style(comment, style)
        filename = create_temp_filename('tmp_comment_screenshot.png')
        scrapper.screenshot_element(comment, filename)
        screenshots.append(Image.open(filename))

    # TODO: Maybe I need to return the filenames instead (?)
    return screenshots


"""
    When I get the 'innerText' attribute from a comment,
    I receive it with a specific structure:

    print(comment.get_attribute('innerText'))
    # I can handle the information from this innertext
    # If I split by \n:

    # 1st is author (@pabloarielcorderovillacort2149)
    # 2nd is date (hace 6 meses)
    # 3rd and next ones are comment text
    # Penultimate is the number of likes (number)
    # Last one is 'Responder'
    #
    # This below is an example of a read comment:
    #
    # @pabloarielcorderovillacort2149
    # hace 6 meses
    # No puedo esperar tu siguiente vídeo.

    # Andy Serkis es una joya de actor, Gollum y Cesar son mis personajes favoritos de este actor.
    # 3
    # Responder
"""