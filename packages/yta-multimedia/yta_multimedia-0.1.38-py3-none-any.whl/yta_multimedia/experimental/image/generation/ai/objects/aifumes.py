from yta_general_utils.experimental.chrome_scrapper import start_chrome, go_to_and_wait_loaded
from yta_general_utils.downloader import Downloader
from random import randint
from datetime import datetime

import requests
import time
import os


PROJECT_ABSOLUTE_PATH = os.getenv('PROJECT_ABSOLUTE_PATH')

class AIFumes():
    """
    They are implementing a lot of models in their webpage: https://fumesai.web.app/. They are also
    working on an API that I want to use :].
    """
    HUGGIN_FACE_IMAGE_MODELS_DEMO_HEADERS = {
        'authority': 'flask-hello-world-murex-sigma.vercel.app',
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://fumesai-text2image-models-demo.static.hf.space',
        'referer': 'https://fumesai-text2image-models-demo.static.hf.space/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    def generate(self, prompt, negative_prompt, output_filename):
        """
        This is the default generating method that will use the method I manually chose from
        code (maybe because someone is down due to external issues).
        """
        # I force this negative prompt by now
        negative_prompt = ',(bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3),poorly drawn,deformed hands,deformed fingers,deformed faces,deformed eyes,mutated fingers,deformedbody parts,mutated body parts,mutated hands, disfigured,oversaturated,bad anatom,cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, deformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck,deformed eyes'

        self.generate_leonardo(prompt, negative_prompt, output_filename)

    def __get_recaptcha_token(self):
        """
        TODO: This is not working. This pretends to get a reCAPTCHA token to be able to do other 
        requests in the webpage in which it is implemented.
        """
        
        # Open (https://huggingface.co/spaces/FumesAI/Leonardo-AI-image-Creator-UPDATED) with crome
        # Alternative page: https://fumesai-leonardo-ai-image-creator-updated.static.hf.space/index.html
        URL = 'https://fumesai-leonardo-ai-image-creator-updated.static.hf.space/index.html'
        chromedriver = start_chrome(False, False, False)
        go_to_and_wait_loaded(chromedriver, URL)
        time.sleep(10)

        # #time.sleep(10)
        # # Obtaining cookies
        # cookie_3PAPISID = chromedriver.get_cookie('__Secure-3PAPISID')
        # cookie_3PSID = chromedriver.get_cookie('__Secure-3PSID')
        # cookie_1P_JAR = chromedriver.get_cookie('1P_JAR')
        # cookie_NID = chromedriver.get_cookie('NID')
        # cookie_3PSIDTS = chromedriver.get_cookie('__Secure-3PSIDTS')
        # cookie_3PSIDCC = chromedriver.get_cookie('__Secure-3PSIDCC')
        # print(chromedriver.get_cookies())
        # #time.sleep(30)

        from selenium.webdriver.common.by import By

        
        # # Get iframe title='reCAPTCHA' information for the request
        recaptcha_iframe = chromedriver.find_element(By.XPATH, '//iframe[contains(@title, "reCAPTCHA")]')
        recaptcha_url = recaptcha_iframe.get_attribute('src')
        recaptcha_hidden_input = recaptcha_iframe.find_element(By.ID, 'recaptcha-token')
        recaptcha_token_value = recaptcha_hidden_input.get_attribute('value')
        # recaptcha_url = chromedriver.find_element(By.XPATH, '//iframe[contains(@title, "reCAPTCHA")]').get_attribute('src')
        # print(recaptcha_url)
        # chromedriver.switch_to.new_window()
        # go_to_and_wait_loaded(chromedriver, recaptcha_url)
        # #time.sleep(3)
        # recaptcha_token_value = chromedriver.find_element(By.ID, 'recaptcha-token').get_attribute('value')
        # #recaptcha_token_value = chromedriver.execute_script('document.getElementById("recaptcha-token").value')
        # chromedriver.close()
        # #recaptcha_token = chromedriver.find_element(By.ID, 'recaptcha-token').get_attribute('value')
        
        # #recaptcha_token_value = chromedriver.execute_script('document.getElementById("recaptcha-token").value')
        # print(recaptcha_token_value)
        elements = recaptcha_url.split('&')
        k = elements[1].split('=')[1]
        co = elements[2].split('=')[1]
        hl = elements[3].split('=')[1]
        v = elements[4].split('=')[1]
        size = elements[5].split('=')[1]
        cb = elements[6].split('=')[1]
        # # It is like 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Leqa5cpAAAAABVhh6FGouusHKaPjYz65-0Yy8kS&co=aHR0cHM6Ly9mdW1lc2FpLWxlb25hcmRvLWFpLWltYWdlLWNyZWF0b3ItdXBkYXRlZC5zdGF0aWMuaGYuc3BhY2U6NDQz&hl=es&v=QquE1_MNjnFHgZF4HPsEcf_2&size=invisible&cb=6beu3j2e4aw1'

        # cookies = {
        #     '__Secure-3PAPISID': cookie_3PAPISID,
        #     '__Secure-3PSID': cookie_3PSID,
        #     '1P_JAR': cookie_1P_JAR,
        #     'NID': cookie_NID,
        #     # These two bellow change
        #     '__Secure-3PSIDTS': cookie_3PSIDTS,
        #     '__Secure-3PSIDCC': cookie_3PSIDCC,
        # }

        # #print(cookies)
        # #chromedriver.close()

        # #exit()
        
        # cookies = {
        #     '__Secure-3PAPISID': '_WzuX9CrPc_FkcnN/AuyTLnEH9KU6HehCw',
        #     '__Secure-3PSID': 'g.a000gwihvpnyIXm_lkiIHWDAxR5zEc3nmpehpn5rkkF0Qi4iYBDKqylsZenvw3HYCckDh_9QcQACgYKAeYSAQASFQHGX2Mitln4s1aKi3-7FYEiC43LCRoVAUF8yKoWA4M9yXlK-ESydg8qZjEO0076',
        #     '1P_JAR': '2024-03-14-10',
        #     'NID': '512=LovqwJ2ZvqbyuntKUMl91ck_Hox3CiGtqz51sDb1BJzdsi9gzIROjfPd_jjylMiGBQyHX5NK3WWeFn2OwqwhSfu4Rto6N0A3f2kMx58bB9FEI1AyWSiEYvULI01XbicEt40gzY0W8I_6HmbMW6CgCh5qVqqD1lxsJbYhVIiceSFokaydCE2_ztwJNcF5i2_cOAUVwLtoPDPkQz076rYc4V3uN3gcgb0yaPg2IfbnKrNQv8PFgg015gi05QCXFM52uaq4M7hxWxDd932CT1d42Tf4FxI18Tgk2Pptz1pAUfdZO05GwrV2jltWAcah2eebT5E7g35arH1l',
        #     # These two bellow change but I can get from chromedriver
        #     '__Secure-3PSIDTS': 'sidts-CjIBYfD7Z5_Rcj0Q8U1RhodY_Sa-XvhygWai2kUJmcrP92A4ga6ffTrznuhYL4Dy0Ae4YhAA',
        #     '__Secure-3PSIDCC': 'AKEyXzWYLPS1hnmEdQBdi3nQf6B1XISaMGqbMQlde94fkLs-ttnr_fylRh76sYAQkwKX-GkzFOY',
        # }
        
        # headers = {
        #     'authority': 'www.google.com',
        #     'accept': '*/*',
        #     'accept-language': 'es-ES,es;q=0.9',
        #     'content-type': 'application/x-protobuffer',
        #     # 'cookie': '__Secure-3PAPISID=_WzuX9CrPc_FkcnN/AuyTLnEH9KU6HehCw; __Secure-3PSID=g.a000gwihvpnyIXm_lkiIHWDAxR5zEc3nmpehpn5rkkF0Qi4iYBDKqylsZenvw3HYCckDh_9QcQACgYKAeYSAQASFQHGX2Mitln4s1aKi3-7FYEiC43LCRoVAUF8yKoWA4M9yXlK-ESydg8qZjEO0076; 1P_JAR=2024-03-14-10; NID=512=LovqwJ2ZvqbyuntKUMl91ck_Hox3CiGtqz51sDb1BJzdsi9gzIROjfPd_jjylMiGBQyHX5NK3WWeFn2OwqwhSfu4Rto6N0A3f2kMx58bB9FEI1AyWSiEYvULI01XbicEt40gzY0W8I_6HmbMW6CgCh5qVqqD1lxsJbYhVIiceSFokaydCE2_ztwJNcF5i2_cOAUVwLtoPDPkQz076rYc4V3uN3gcgb0yaPg2IfbnKrNQv8PFgg015gi05QCXFM52uaq4M7hxWxDd932CT1d42Tf4FxI18Tgk2Pptz1pAUfdZO05GwrV2jltWAcah2eebT5E7g35arH1l; __Secure-3PSIDTS=sidts-CjIBYfD7Z5_Rcj0Q8U1RhodY_Sa-XvhygWai2kUJmcrP92A4ga6ffTrznuhYL4Dy0Ae4YhAA; __Secure-3PSIDCC=AKEyXzWYLPS1hnmEdQBdi3nQf6B1XISaMGqbMQlde94fkLs-ttnr_fylRh76sYAQkwKX-GkzFOY',
        #     'origin': 'https://www.google.com',
        #     'referer': 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=' + k + '&co=' + co + '&hl=es&v=' + v + '&size=invisible&cb=' + cb,
        #     'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-fetch-dest': 'empty',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-site': 'same-origin',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        #     'x-client-data': 'CJS2yQEIorbJAQipncoBCJzzygEIlqHLAQic/swBCIWgzQEY9cnNARjSgs4B',
        # }

        # params = {
        #     'k': k,
        # }

        # "03AFcWeA5iq5KRnX6G4cEa9vdSi7xmlnqnaN7eO0mfR-B3Py79GbkMepAVy01OF9PM0TYms1Ze00HVIiaDwBaTqYEQvHxy1Old1BhD2JBgK0eQh-S_AnscrLRCOv_003ceP-w3PlWdNF0MQA9FRjR0_qJrecpPbhfrDRsaxTFD3aJYeIAGsw7QabomNYWOdRTGfI1ALYB94YOdsV_fLbXG1sAgHgbuZrzGGSpm_qRb4U9DHQSSSdzX1bpMvMpNMrSAu8AacqZcYBuZtuqO8IFS2opknsZgrtiaHaS_5MNk94gI9bYQ1QMlXjksjaBwzZvGfl9MXLIGEtKk5MTMoje3pu9Ckg0ChL3YD1LHIMTTVWEBi1wNlQCOHfbkb3Zy2sIheZxA87UJaevv9fcQqIPM6A30sySsJ-dPLsmqC0t4K0V9RWBLzqgUadmO6Kwu2BgYML021ReKHq3BWJhhihhWxp0dqvvb2_95wRcKZ_mS4cyw5ygsdBwbjHUPmY68TLQ4ZPAH7b9WqbnhsrQLtlA_vcekuKVk6HUEH0gP_rbZ4GCu0ZaTNuHwf4vnXzgnzzbK_QkEuvqWem26tcRybwvIbYi9LYv6piES-Mk1rmk2eSbT9Pd53AgK_Blo99eiQW4aRfYZi7joU6ZoJPG7nvb9n5y0X_lvavNHv5JO1ZAQTW8eM6qFmcLBB1dOQ2GA0CfmjxkZaszoOiXap4TcCrcAYS_SHn5kbMnctyezzjdpkb5VbPOjO9Rrfu5n7tGSlyh8Qjsw1xTXH_r0wXCmZdWMRC10Lf7KvLLE58PCV9axAWKE8Xn3jiab694nw4srIPMCPIUXlOVXWk-YMdQkH8I3ZetzYUSmq4qPlVWN-lb4-r3nLWcKi6VGR2aI6WgTBUHTWY6HoNEOF8AJfGsXrvw-qMEBUWw9066bcD9ErG6Lk-cHzU7HsmhNvRvCS86WOgNHtwutWpurWRSXZ7W4W2Nkzyg7ypfExRXYE8HL0JVBP4OuWeIaeCVSzhENmoQnuMC8v3aru6j5Wur-73TTRorwfFQoEng-BE4T3vKzwQnirmPso8I7a7yZlNgERvgsO4kQoRSfZwy8ucq49HPhOKBMMasfmMP6FmIIlH-HiKiOLUFLO2iR7oPgkbCM5wOMROEDSGT1bRIpDN-bfE39wI_ypIUFJT0vhGlz7a89t_WmP06oEZW2pxAI_l9cDrTLQZvHYLfJ22ZG4s7EGKKGb3EB1mV2qOPM9xb0MwRthQaNDI2I-555cx2jfwe-0Qw2bl1myvLqL8-IIV0qh7rIApJSu1sf1oe7AvM3Tp6FbRGliWb08Ai2wkVc1AyY0N_yO0hHjtN6CsLMfayXzeBvon0xxi1_8ewTvZtg-svxTnmQDsJxolhp20UnA8xxPYg7vSToYO5dKIzOR0ntW_N_VGO_AkeZ_d1OIa-BKoguWPSgipusb2pcdMo6JOsUZqETmvJt_l-zzJT0sY2AhYHUf_nWZZ4CtQA2yG6CcxtLdOsH20KKyXmraiDlJkPbjyfUEtfUuwERwvTK5A4n5_Dx1FKTg6Feh_NXBut8m-YUzE5FAjJ4rCMK3VFw7ZIcxWsFHZtsMj5VYcZ4NxBVcWnNDeCthMeJ1VNDBwrkwhS6oIiwR_dZ4BKeKrxn4DDk_WQJE61YCK95sej5XtvTj0gOYkTiUEjzeQqi7n9w_DqAVwIiNguoIBCCc-Hs4gTMVj7J0ZgfkaZRA3S38AjqTlo5P-RVHbBpC5mElmGwtg"


        # # Where does this come from?
        # data = recaptcha_token_value

        # #response = requests.post('https://www.google.com/recaptcha/api2/reload', params = params, cookies = cookies, headers = headers, data = data)

        # #print(response.content)
        # #token = response.json()['1']

        token = chromedriver.execute_script('grecaptcha.execute("' + k + '");')
        print(token)

        #print(cookies)
        chromedriver.close()

        return token

    def generate_leonardo(self, prompt, negative_prompt = '', output_filename = 'tmp_fumes_leonardo.png'):
        #URL = 'https://fumesai-leonardo-ai-image-creator-updated.static.hf.space/index.html'
        URL = 'https://fumesai.web.app/img'
        chromedriver = start_chrome(True, False, False)
        go_to_and_wait_loaded(chromedriver, URL)

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from utils.autogui_utils import move_cursor_to
        from random import randint

        prompt_input = chromedriver.find_element(By.ID, 'inp')
        # Write input
        prompt_input.send_keys(prompt)
        time.sleep(1)
        move_cursor_to(randint(400, 1900), randint(100, 900))
        settings_button = chromedriver.find_element(By.XPATH, "//button[contains(text(), 'Setting')]")
        settings_button.click()
        time.sleep(1)
        move_cursor_to(randint(100, 1800), randint(50, 800))
        negative_prompt_input = chromedriver.find_element(By.ID, 'np')

        negative_prompt = ',(bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3),poorly drawn,deformed hands,deformed fingers,deformed faces,deformed eyes,mutated fingers,deformedbody parts,mutated body parts,mutated hands, disfigured,oversaturated,bad anatom,cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, deformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck,deformed eyes'
        
        if negative_prompt:
            negative_prompt_input.send_keys(negative_prompt)
        time.sleep(1)
        move_cursor_to(randint(100, 1700), randint(100, 800))
        photography_style_radio_button = chromedriver.find_element(By.XPATH, "//input[contains(@value, 'photo')]").click()
        time.sleep(1)
        move_cursor_to(randint(200, 1600), randint(200, 780))

        # Scroll down
        chromedriver.execute_script('window.scrollTo(' + str(0) + ', ' + str(999) + ')')

        landscape_radio_button = chromedriver.find_element(By.XPATH, "//input[contains(@value, '16:9')]").click()
        time.sleep(1)
        move_cursor_to(120, 550)
        close_button = chromedriver.find_element(By.ID, 'close').click()
        time.sleep(1)
        chromedriver.execute_script('window.scrollTo(' + str(0) + ', ' + str(0) + ')')
        move_cursor_to(randint(700, 1700), randint(250, 800))
        for i in range(3):
            move_cursor_to(randint(0, 1000), randint(0, 1000))
        create_button = chromedriver.find_element(By.ID, 'create').click()
        time.sleep(1)

        image_urls = []
        for i in range(100):
            print('Looking for images')
            try:
                images = chromedriver.find_elements(By.TAG_NAME, 'img')
                # Writing to sample.json
                if len(images) > 0:
                    for image in images:
                        image_url = image.get_attribute('src')
                        image_urls.append(image_url)
                    break
            except:
                pass
            time.sleep(1)
            if i % 10 == 0:
                chromedriver.execute_script('window.scrollTo(' + str(randint(0, 70)) + ', ' + str(999) + ')')

        if len(image_urls) > 0:
            print('Downloading ' + image_urls[0])
            # We secure the one we want
            Downloader.download_image(image_urls[0], output_filename)
            # But then we store all generated images
            for image_url in image_urls:
                print('Downloading ' + image_url)
                delta = (datetime.now() - datetime(1970, 1, 1))
                image_filename = 'leonardo_' + str(int(delta.total_seconds())) + str(randint(0, 10000)) + '_' + str(randint(0, 1000)) + '.png'
                print('Downloading to local leonardo images folder.')
                try:
                    Downloader.download_image(image_url, PROJECT_ABSOLUTE_PATH + 'leonardo_images/' + image_filename)
                    with open(PROJECT_ABSOLUTE_PATH + 'leonardo_images/leonardo_generated_images.txt', 'a') as outfile:
                        outfile.write(image_url + '\n')
                        outfile.close()
                except:
                    pass

        chromedriver.close()

    def __generate_leonardo_inactive(self, prompt, negative_prompt = '', output_filename = 'tmp_fumes_leonardo.png'):
        """
        This is a generation created in this HugginFace space: https://huggingface.co/spaces/FumesAI/Leonardo-AI-image-Creator-UPDATED

        [ ! ] TODO: This is not working due to reCAPTCHA token needed in AIFumes API request.
        I was not able to get it an doing a good request, so I decided to implement an scrapper
        to be able to get images.
        """
        HEADERS = {
            'authority': 'fumes-api.onrender.com',
            'accept': '*/*',
            'accept-language': 'es-ES,es;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://fumesai-leonardo-ai-image-creator-updated.static.hf.space',
            'referer': 'https://fumesai-leonardo-ai-image-creator-updated.static.hf.space/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        # TODO: Investigate all available 'styles' to integrate as parameter
        STYLES = [
            'PHOTOGRAPHY',
        ]

        negative_prompt = ',(bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3),poorly drawn,deformed hands,deformed fingers,deformed faces,deformed eyes,mutated fingers,deformedbody parts,mutated body parts,mutated hands, disfigured,oversaturated,bad anatom,cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, deformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck,deformed eyes'

        #token = '03AFcWeA7BkorgG3DLH8M7Kc7n_OR4_aIzjM29WDFbTTGug037ubLfdcCo6CsxtvEaJH16JaVpr2IS0k3QOvEYrJdfp4EISFt7la0vnb1DOfD6KYHvW7udVmBu6dv5b-7sCJ3LDln6dhf63mFD_x7NAdXiAogdNgimfW2hwkXBwNGyFGD-p2C-VILC1BcEa95EjXHlWwB4FhZyKQtJAAkov1hAiETLrUZ85TDYDjSfiCziimtXpDCzW2fZzjZW0p_4VtBNdDkbNLwZC2ixM-_XuxpXoInQ1GXe3iqr9mWnILqloRRl_tblhFUO613WLEKwLZxnpBSITOHrg_TmIGqaIpjpv8koUYU0rgimOb1QXdEiaMyStZv8FkNggfOs4oDv895pJ3cUNKn8rk25htgDdDaa2ij6vCgX7OwdrWqSoMKR9uhgwDnuyR-228uvx5FMeRCzana6QAAe9cYgR7HfmR0B5M2l8qSyroWfnVD0HtnHoaqj71NLWht4VmuzhM8MfiZof5zDouxoWEFXl10HMj8S4yuGOCJ_U2y63BB5n4r3MmKWWlXxxCD-hS_zLqirr2lXK-SdVdEZFdDKVTMT4OKKpy4gVla0fJXtUoSdr_XpS0XYA6pwqVx4CezppNnHwHS5CHAoa2PMDaZExKZxeY5ArP2A8UzDHE9l2zclNckEtligkofBCnF-z9lmcGsMLco6sS-CHsNOT60UF4IIzTQQ71H7HArQbJd2WsJoCncCiYdfOzBrQF3PuVUzFG1OZPYvirteabptInbCkg1Rd0jXzuCZi1smo2HTpZ6cCC3V_uKn8mdQrlRNo7BLHm0s16Wp_Y16I_m2znBdEGM3KDu378uaMWeGIxZ-a-pq69bmGynGi_ZBu-LZnVSpCZ3ZMXawMr0ilOijnjKD8FvZWy_KAj9gfGfGoQ8_grlsLNzEFMtqHgPSTzeYwX5URqs16y71ydYJtxVqI3uszuEZbFlpee5Sa1nfOd48RVA9XRsWsED1lEvQTyGd7oXSlXlDl0uGEcbaMGoGFU9QlbZTpn0CuxF-3rJsZWRw0c3lbGktM-3bOu76T06c1lT530uSFC9HCmxNRrXnXWi26ynAnaiRmDwXsfyHKzi8wA1TwR1no233dL06TwWeBtzrfvUCkc-4aAP41R3yUK6uGA4QCjr38_5b8frgkVwEu6ecMYd-DVQVFLpOQB1gVkVAR9GZPWEz8XTes-hhDCoMNloCV9Bhb3L26m5EizMh0CLMM5Efvdl0Yf4j4QSgfTEnuaHfvM24HEdGSFcCXgg6hYCfLyejEAR5hW1OXqQ6_WGBNTRosJ6XIeQv2mPaOCWjWPKwE5_JkjhQZr6wZVDF5Yg2fBV-uma0Oq2BeLUcma92xicr7-5kbChI1eNneYHBruAkEBiqW2ZTPjuiaGQEL8WLOaWWefPf7Uvs4xJVvBGi5sJQUyY_jDCXS__Kcvcm0ZaAIgct4AanL2Gvr_URHhWzJiPYwd0J_jy3M8rYsljgGkD8Yd929z3bSwwxjkrYnUwW76FcXM3wZsNOHbiEqx1uuwNDrmdnXdviNdqRyyLzLI0EKqDXaZLXaxgM2_fFJ-lZeHeDeeoDQ1jqIchCZSJPSeNL_rTTy8r8PtCRBrpahK9VgdqtIdXyL0zDvP2bveQIZHM9BmYcpvsMD5QK092gKaVCYqnAwzwDSSI0QFU7nSUFH6FlLGabj7fh8XEi9iflmid8C6SF4CS6'

        token = self.get_recaptcha_token()

        json_data = {
            'prompt': prompt,
            'nprompt': negative_prompt,
            'steps': 20,
            'guidenceScale': 7,
            'style': 'PHOTOGRAPHY',
            'width': 1024,
            'height': 576,
            'alchemy': True,
            'pr': True,
            'token': token,
        }

        # This could be slow, and thats why I use 500 of timeout
        response = requests.post('https://fumes-api.onrender.com/leonardo', headers = HEADERS, json = json_data, timeout = 500)

        # This returns
        #localStorage.setItem("cookie", data.token);
        #localStorage.setItem("sub", data.sub);
        #localStorage.setItem("u", data.u);

        print(response.content)

        # We obtain the first image, but we have one in ['1'] and another one in ['2']
        image_url = response.json()['img']['1']
        Downloader.download_image(image_url, output_filename)

    def __request_creation(self, request_url, prompt, negative_prompt):
        """
        Makes a creation request through the provided 'request_url' that is related to an
        specific image generation model.

        This method returns the 'id' that is the one with which we can ask for the status
        and receive the image to download when ready.

        This works here https://huggingface.co/spaces/FumesAI/text2Image-Models-Demo.
        """
        #negative_prompt = ' ,(bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3),poorly drawn,deformed hands,deformed fingers,deformed faces,deformed eyes,mutated fingers,deformedbody parts,mutated body parts,mutated hands, disfigured,oversaturated,bad anatom,cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, deformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck,deformed eyes'

        json_data = {
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'steps': '35',
            'gd': '7',
        }

        response = requests.post(request_url, headers = self.HUGGIN_FACE_IMAGE_MODELS_DEMO_HEADERS, json = json_data)
        
        id = response.json()

        return id
    
    def __request_status(self, id, tries = 12):
        """
        Makes a status request a maximum of 'tries' times to get the image when ready. It
        waits 10 seconds between each request.

        This method returns the image url if successfully generated, or False if something
        went wrong.

        This works here https://huggingface.co/spaces/FumesAI/text2Image-Models-Demo.
        """
        json_data = {
            'id': id,
        }

        for i in range(tries):
            time.sleep(10)
            response = requests.post('https://flask-hello-world-murex-sigma.vercel.app/status', headers = self.HUGGIN_FACE_IMAGE_MODELS_DEMO_HEADERS, json = json_data)

            response_json = response.json()
            if not 'status' in response_json and 'a' in response_json and 'b' in response_json:
                # It is returning 'a' and 'b' but are the same picture, don't know why
                image_url = response_json['a']

                return image_url
            
        return False
    
    def generate_sdxl(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/predict'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False

    def generate_playground_2_5(self, prompt, negative_prompt = '', output_filename = ''):
        """
        TODO: This method is not working
        """
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/piss'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_juggernaut_xl_v9(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/nut'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_proteus_04(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/p4'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_proteus_02(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/proteus'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_open_dalle_1_1(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/predict'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_proteus_03(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/p3'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_kandinsky_2_2(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/k'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_sdxl_emoji(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/emo'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_wuerstchen(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/w'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_dreamshaper_xl_turbo(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/dream'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
    
    def generate_pixart_alpha(self, prompt, negative_prompt = '', output_filename = ''):
        URL = 'https://flask-hello-world-murex-sigma.vercel.app/pixart'
        id = self.__request_creation(URL, prompt, negative_prompt)
        image_url = self.__request_status(id)

        if image_url:
            Downloader.download_image(image_url, output_filename)
            return True

        # Raise exception
        return False
        




    def test(self, prompt):
        # From here: https://dream.ai/create
        # TODO: This is not from AIFumes but I'm testing it quickly
        HEADERS = {
            'authority': 'paint.api.wombo.ai',
            'accept': '*/*',
            'accept-language': 'es-ES,es;q=0.9',
            'authorization': 'bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjYwOWY4ZTMzN2ZjNzg1NTE0ZTExMGM2ZDg0N2Y0M2M3NDM1M2U0YWYiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9wYWludC1wcm9kIiwiYXVkIjoicGFpbnQtcHJvZCIsImF1dGhfdGltZSI6MTcxMDI2OTIyMSwidXNlcl9pZCI6IkNoUGc1TTdsSWtOUUlyVHpLOHJUZzlCNDVZMzIiLCJzdWIiOiJDaFBnNU03bElrTlFJclR6SzhyVGc5QjQ1WTMyIiwiaWF0IjoxNzEwMjY5MjIxLCJleHAiOjE3MTAyNzI4MjEsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.eOsyYTm6ZrCunqah3zRuejVot4gYxEeTGkm9mvghSvuiHTXJqnCUduSe0huqBCUFhXIwvwrxM88A_BZlQNI1eKK8RXFcDFgo1B3hmaPvBvM7T06y-OIlTSUDlLsv5E0oIdd7POeKuxHJVWdxnfynF1-y3upDb37EBywZbIhAOXJWibsha8WNy4NDPDbmSG0b5WAiUCCPTr4eAetGaV7ouBssn1WdAfAsasbK0Ys5vxjXSlNMSWVDFWu7sNlDys6nnNGRgQlOKqheVzBTusBvfts8JnuKGyYp_kSEuadnybNPy418P0ySNbfGgKBw4kSkKDdU_wS6pDUdFl6q2Ju8VQ',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://dream.ai',
            'referer': 'https://dream.ai/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'x-app-version': 'WEB-2.0.0',
            'x-validation-token': 'eyJraWQiOiJYcEhKU0EiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOjE4MTY4MTU2OTM1OTp3ZWI6Mjc3MTMzYjU3ZmVjZjU3YWYwZjQzYSIsImF1ZCI6WyJwcm9qZWN0c1wvMTgxNjgxNTY5MzU5IiwicHJvamVjdHNcL3BhaW50LXByb2QiXSwicHJvdmlkZXIiOiJyZWNhcHRjaGFfZW50ZXJwcmlzZSIsImlzcyI6Imh0dHBzOlwvXC9maXJlYmFzZWFwcGNoZWNrLmdvb2dsZWFwaXMuY29tXC8xODE2ODE1NjkzNTkiLCJleHAiOjE3MTAyODcyMjAsImlhdCI6MTcxMDI2OTIyMCwianRpIjoiYXE2MXFWNDBaa3dRaFI1Q1E3U0xTcDI5cWtXSnhiOFFNS2RocmZ3Yk5rNCJ9.je_jITU4LhA4UlFwkJp0Pke8Pv6VB2ceLidBuwAbPoPWLO2MocVPpi-sBzukNQfOLmOytOZnzzSgon11kU8yP2vE3yJnzVlIelzN79BYIs7IIiDjftlqhtwZNLY-Est3VljRf7WE_p5FuW445PWGqgj-te_N-XFlKrjAReGbED8UBIpF3ZeQDwrRB9vCT4RxuxqiGltQ-vW3W4H-b58VWSizDiAz0gn5yj6132fZhavA-uPRgwCwkZyHhJGoJmXt-O98PB6ArQ8yNvnYpt3Z2VHxJdlqsy8g3UXAMbUS-wPjM0RchvtAsSe2lB4rCewtJKzsji31uFSQf6_9qNnxud9s-6Yt2d6TcMoP5dEAM_fr2iW3aht_LJ7WBBWHhNplYHUKN4b3uVQneaT_v_PAY70xMachEnrj0vYfDo-o-KPaWWxfs2oDpAGhOlERjejDNRkSfYfwEzoI-AhxYUbnWDCQNmw8Lp_7sJ8JJHr7D3RwbnvXRLTYIQYNoDldbpA6',
        }

        data = '{"is_premium":false,"input_spec":{"prompt":"' + prompt + '","style":115,"display_freq":10}}'

        response = requests.post('https://paint.api.wombo.ai/api/v2/tasks', headers = HEADERS, data = data)
        # I think that when token expired, this won't be a json
        response_json = response.json()
        id = response_json['id']
        # 'id' and 'user_id'?

        STATUS_HEADERS = {
            'authority': 'paint.api.wombo.ai',
            'accept': '*/*',
            'accept-language': 'es-ES,es;q=0.9',
            'authorization': 'bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjYwOWY4ZTMzN2ZjNzg1NTE0ZTExMGM2ZDg0N2Y0M2M3NDM1M2U0YWYiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9wYWludC1wcm9kIiwiYXVkIjoicGFpbnQtcHJvZCIsImF1dGhfdGltZSI6MTcxMDI2OTIyMSwidXNlcl9pZCI6IkNoUGc1TTdsSWtOUUlyVHpLOHJUZzlCNDVZMzIiLCJzdWIiOiJDaFBnNU03bElrTlFJclR6SzhyVGc5QjQ1WTMyIiwiaWF0IjoxNzEwMjY5MjIxLCJleHAiOjE3MTAyNzI4MjEsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.eOsyYTm6ZrCunqah3zRuejVot4gYxEeTGkm9mvghSvuiHTXJqnCUduSe0huqBCUFhXIwvwrxM88A_BZlQNI1eKK8RXFcDFgo1B3hmaPvBvM7T06y-OIlTSUDlLsv5E0oIdd7POeKuxHJVWdxnfynF1-y3upDb37EBywZbIhAOXJWibsha8WNy4NDPDbmSG0b5WAiUCCPTr4eAetGaV7ouBssn1WdAfAsasbK0Ys5vxjXSlNMSWVDFWu7sNlDys6nnNGRgQlOKqheVzBTusBvfts8JnuKGyYp_kSEuadnybNPy418P0ySNbfGgKBw4kSkKDdU_wS6pDUdFl6q2Ju8VQ',
            'origin': 'https://dream.ai',
            'referer': 'https://dream.ai/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'x-app-version': 'WEB-2.0.0',
        }

        # 'Web Dream API KEY' z8w6OPCOBstepOZXbR7L

        tries = 12
        for i in range(tries):
            time.sleep(10)
            response = requests.get('https://paint.api.wombo.ai/api/v2/tasks/' + id, headers = STATUS_HEADERS)
            response_json = response.json()

            if 'result' in response_json and response_json['result'] and response_json['result']['final']:
                download_by_url(response_json['result']['final'], 'test_dreamai.png')
                return True
            
        return False