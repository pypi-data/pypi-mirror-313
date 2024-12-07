"""
Here we are using the https://message.style/app/editor
platform with a Web Scrapper to obtain the nice Discord
images they generate.
"""
from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from yta_general_utils.programming.singleton import SingletonMeta
from selenium.webdriver.common.keys import Keys
from PIL import Image
from time import sleep

import io
import json
import datetime


WEB_URL = 'https://message.style/app/editor'

class DiscordMessageImageGenerator(metaclass = SingletonMeta):
    """
    Singleton class to generate Discord Message images. I use it as a 
    singleton because if the scrapper is instantiated it only has to
    reload the web page and go to build the next message, and not 
    opening a new browser again.
    """
    def __init__(self):
        if not hasattr(self, 'scrapper'):
            self.scrapper = ChromeScrapper()

    def __build_string_json(self, username: str, user_avatar_url: str, message: str, image_url: str = None):
        """
        Returns the json that will create the message in the platform,
        but as a string.
        """
        # TODO: Sanitize this better, please
        # Check this: https://forum.uipath.com/t/how-to-remove-r-n-from-this-json/747396/11

        embeds = []
        if image_url:  # if image
            embeds.append({
                "id": 652627557,
                "color": 3289650,
                "fields": [],
                "image": {
                    "url": image_url
                }
            })

        json_content = {
            "content": message,
            "tts": False,
            "username": username,
            "avatar_url": user_avatar_url,
            "embeds": embeds,
            "components": [],
            "actions": {}
        }

        return json.dumps(json_content, ensure_ascii = False).encode('utf-8').decode('utf-8')

    def generate(self, username: str, user_avatar_url: str, message: str, badge_text: str = None, datetime_text: str = None, image_url: str = None, output_filename: str = None):
        """
        Generates a Discord message with the provided parameters and
        stores it locally as 'output_filename'.

        If you want to do a line break you must use "\\ \\n" but 
        toghether, without the blank space I left and without the
        quotes.

        If 'badge_text' is None the badge will be not shown. If 
        'datetime_text' is None, it will display the current datetime
        as 'Hoy a las XX:XX'.
        """
        if not username:
            raise Exception('No "username" provided')
        
        if not user_avatar_url:
            raise Exception('No "user_avatar_url" provided.')
        
        if not message:
            message = ''
        
        # We go to the main website
        self.scrapper.go_to_web_and_wait_util_loaded(WEB_URL)

        # TODO: Check if provided 'image_url' is a valid image
        json_string = self.__build_string_json(username, user_avatar_url, message, image_url)
        # We need to manually add the string to clipboard to 
        # be able to paste it
        self.scrapper.add_to_clipboard(json_string)

        # We will now change the JSON to format the message we want
        self.scrapper.go_to_web_and_wait_util_loaded(WEB_URL + '/json')
        
        # Focus the editor to be able to paste
        self.scrapper.press_key_x_times(Keys.TAB, 25) # Manually detected, to focus on json editor

        # Select the whole previous json, delete it and paste our own
        self.scrapper.press_ctrl_a()
        self.scrapper.press_key_x_times(Keys.DELETE, 1)
        active_element = self.scrapper.driver.switch_to.active_element
        active_element.click()
        self.scrapper.press_key_x_times(Keys.DELETE, 1)
        self.scrapper.press_ctrl_v_on_element(active_element)
        # Press the save button
        save_button = self.scrapper.find_element_by_text('button', 'Save')
        save_button.click()
        # TODO: This could be a 'wait-for-element-change' waiting,
        # by now the amount of seconds is manually chosen
        sleep(2)
        message_element = self.scrapper.find_element_by_class('div', 'discord-message')

        # Hide bot badge
        if not badge_text:
            self.scrapper.execute_script('document.getElementsByClassName("discord-application-tag")[0].style.display = "none";')
        else:
            self.scrapper.execute_script('document.getElementsByClassName("discord-application-tag")[0].innerHTML = "' + badge_text + '";')

        # Set datetime
        if not datetime_text:
            now = datetime.datetime.now().strftime("%H:%M")
            if now.startswith('0'):
                now = now[1:]
            datetime_text = 'hoy a las ' +  now
        self.scrapper.execute_script('document.getElementsByClassName("discord-message-timestamp pl-1")[0].innerHTML = "' + datetime_text + '";')
        
        # We return the screenshot or we store it and return the image filename
        screenshot = self.scrapper.screenshot_element(message_element, output_filename)

        if output_filename:
            return screenshot

        # TODO: Write this in docummentation
        # TODO: If unneeded, replace the dict in ChromeScrapper
        # for only the 'data' as we don't need to know the size
        return Image.open(io.BytesIO(screenshot))


"""
Useful discord messages below

{
  "content": "Welcome to **Embed Generator**! 🎉 Create stunning embed messages for your Discord server with ease!\n\nIf you're ready to start, simply click on the \"Clear\" button at the top of the editor and create your own message.\n\nShould you need any assistance or have questions, feel free to join our [support server](/discord) where you can connect with our helpful community members and get the support you need.\n\nWe also have a [complementary bot](/invite) that enhances the experience with Embed Generator. Check out our [Discord bot](/invite) which offers features like formatting for mentions, channels, and emoji, creating reaction roles, interactive components, and more.\n\nLet your creativity shine and make your server stand out with Embed Generator! ✨",
  "tts": false,
  "embeds": [
    {
      "id": 652627557,
      "title": "About Embed Generator",
      "description": "Embed Generator is a powerful tool that enables you to create visually appealing and interactive embed messages for your Discord server. With the use of webhooks, Embed Generator allows you to customize the appearance of your messages and make them more engaging.\n\nTo get started, all you need is a webhook URL, which can be obtained from the 'Integrations' tab in your server's settings. If you encounter any issues while setting up a webhook, our bot can assist you in creating one.\n\nInstead of using webhooks you can also select a server and channel directly here on the website. The bot will automatically create a webhook for you and use it to send the message.",
      "color": 2326507,
      "fields": []
    },
    {
      "id": 10674342,
      "title": "Discord Bot Integration",
      "description": "Embed Generator offers a Discord bot integration that can further enhance your the functionality. While it is not mandatory for sending messages, having the bot on your server gives you access to a lot more features!\n\nHere are some key features of our bot:",
      "color": 2326507,
      "fields": [
        {
          "id": 472281785,
          "name": "Interactive Components",
          "value": "With our bot on your server you can add interactive components like buttons and select menus to your messages. Just invite the bot to your server, select the right server here on the website and you are ready to go!"
        },
        {
          "id": 608893643,
          "name": "Special Formatting for Mentions, Channels, and Emoji",
          "value": "With the /format command, our bot provides special formatting options for mentions, channel tags, and ready-to-use emoji. No more manual formatting errors! Simply copy and paste the formatted text into the editor."
        },
        {
          "id": 724530251,
          "name": "Recover Embed Generator Messages",
          "value": "If you ever need to retrieve a previously sent message created with Embed Generator, our bot can assist you. Right-click or long-press any message in your server, navigate to the apps menu, and select Restore to Embed Generator. You'll receive a link that leads to the editor page with the selected message."
        },
        {
          "id": 927221233,
          "name": "Additional Features",
          "value": "Our bot also supports fetching images from profile pictures or emojis, webhook management, and more. Invite the bot to your server and use the /help command to explore all the available features!"
        }
      ]
    }
  ],
  "components": [],
  "actions": {}
}
"""