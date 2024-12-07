import requests
import urllib.request
import base64
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
def oca_solve_captcha(driver, actions, user_api_key, action_type, number_captcha_attempts):
    action_type = action_type.lower()
    if action_type == "tiktokcircle" or action_type == "tiktokpuzzle" or action_type == "tiktok3D":
        try:
            for i in range(0, number_captcha_attempts):
                is_exist_capctha_whirl = driver.find_elements("xpath", '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]')
                is_exist_capctha_slide = driver.find_elements("xpath",'//div[contains(@class,"captcha_verify_img")]/img[contains(@class,"captcha_verify_img_slide")]/following::div/following::div//div[contains(@class,"captcha-drag-icon")]')
                is_exist_3d_capctha = driver.find_elements("xpath", '//div[contains(@class,"captcha_verify_img")]/img | //div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[contains(@src,"/3d_") and //div[contains(@class,"cap")]//img/following-sibling::button]')
                is_exist_icon_capctha = driver.find_elements("xpath", '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[contains(@src,"/icon_") and //div[contains(@class,"cap")]//img/following-sibling::button]')
                if len(is_exist_capctha_whirl) < 1 and len(is_exist_capctha_slide) < 1 and len(is_exist_3d_capctha) < 1 and len(is_exist_icon_capctha) < 1:
                    break
                else:
                    get_refresh_buttton = driver.find_elements("xpath", '//a[contains(@class,"refresh")]/span[contains(@class,"refresh")][text()] | //button[contains(@class,"cap-items")][1]')
                    if len(get_refresh_buttton) > 0:
                        update_captcha_img = driver.find_element(By.XPATH, '//a[contains(@class,"refresh")]/span[contains(@class,"refresh")][text()] | //button[contains(@class,"cap-items")][1]')
                    else:
                        update_captcha_img = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_action")]//button[1]//div[contains(@class,"Button-label")][text()]')
               
                    if len(is_exist_capctha_whirl) > 0:
                        get_full_img = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]/img[1]').get_attribute("src")
                        open_full_img_url = urllib.request.urlopen(get_full_img)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64
                        get_slider_square = driver.find_element(By.XPATH, '//div[contains(@class,"slidebar")] | //div[contains(@class, "cap")]/div[contains(@draggable, "true")]/parent::div')
                        img_width = get_slider_square.value_of_css_property("width")
                        img_width = round(float(img_width.replace('px', '')))
                        img_height = get_slider_square.value_of_css_property("height")
                        img_height = round(float(img_height.replace('px', '')))                      
                        small_img_url = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]/img[2]').get_attribute("src") #get link small img
                        open_small_img_url = urllib.request.urlopen(small_img_url)
                        small_img_url_html_bytes = open_small_img_url.read()
                        small_screenshot_img_url_base64 = base64.b64encode(small_img_url_html_bytes).decode('utf-8')
                        small_img = small_screenshot_img_url_base64
                        get_slider_captcha = driver.find_element(By.XPATH, '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"] | //div[contains(@class, "cap")]/div[contains(@draggable, "true")]/button//*[name()="svg"]')                                                       
                        captcha_action_type = "tiktokcircle"
                        multipart_form_data = {
                            'FULL_IMG_CAPTCHA': (None, full_img),
                            'SMALL_IMG_CAPTCHA': (None, small_img),
                            'FULL_IMG_WIDTH': (None, img_width),
                            'FULL_IMG_HEIGHT': (None, img_height),
                            'ACTION': (None, captcha_action_type),
                            'USER_KEY': (None, user_api_key)
                        }
                        request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                        response_solve_captcha_content = request_solve_captcha.content
                        if isinstance(response_solve_captcha_content, bytes):
                            response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')
                        if response_solve_captcha_content == "ERROR_USER_KEY":
                            raise Exception("Invalid API key / Make sure you using correct API key")
                        elif response_solve_captcha_content == "ZERO_BALANCE":
                            raise Exception("Balance is zero / Top up your balance")
                        if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                            response_solve_captcha = request_solve_captcha.json()
                            response_cordinate_x = int(response_solve_captcha["cordinate_x"])
                            response_cordinate_y = int(response_solve_captcha["cordinate_y"])
                            random_move_left_right = random.randint(15, 50)
                            random_move_number = random.randint(1, 2)
                            if random_move_number == 1:
                                response_cordinate_x_random_move = int(response_cordinate_x) - int(random_move_left_right)
                                actions.reset_actions()
                                actions.click_and_hold(get_slider_captcha)
                                for i in range(0, 1):
                                    actions.move_by_offset(response_cordinate_x_random_move, 0)  
                                    time.sleep(random.uniform(0.000001, 0.000003))
                                slide_moving_speed = random.uniform(0.000005, 0.000009)
                                remaining_distance = random_move_left_right
                                for i in range(0, random_move_left_right):
                                    if remaining_distance <= 5:
                                        break
                                    random_offset = random.randint(2, min(8, remaining_distance))
                                    actions.move_by_offset(random_offset, 0).perform()
                                    remaining_distance -= random_offset
                                    time.sleep(slide_moving_speed)
                                for i in range(0, remaining_distance):
                                    actions.move_by_offset(1, 0).perform()
                                    time.sleep(slide_moving_speed)
                            else:
                                response_cordinate_x_random_move = int(response_cordinate_x) + int(random_move_left_right)         
                                actions.reset_actions()
                                actions.click_and_hold(get_slider_captcha)
                                for i in range(0, 1):
                                    actions.move_by_offset(response_cordinate_x_random_move, 0)  
                                    time.sleep(random.uniform(0.000001, 0.000003))
                                slide_moving_speed = random.uniform(0.000005, 0.000009)
                                remaining_distance = random_move_left_right
                                for i in range(0, random_move_left_right):
                                    if remaining_distance <= 5:
                                        break
                                    random_offset = random.randint(2, min(8, remaining_distance))
                                    actions.move_by_offset(-random_offset, 0).perform()
                                    remaining_distance -= random_offset
                                    time.sleep(slide_moving_speed)
                                for i in range(0, remaining_distance):
                                    actions.move_by_offset(-1, 0).perform()
                                    time.sleep(slide_moving_speed)
                            actions.release().perform() 
                            time.sleep(10)    
                        else:
                            update_captcha_img.click()
                            time.sleep(random.uniform(8, 10))


                    if len(is_exist_capctha_slide) > 0:                                                                 
                        get_full_img = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img[contains(@id,"captcha-verify-image")] | //div[contains(@class, "cap") and count(img) = 1]/img/following-sibling::div/img/parent::div/parent::div').get_attribute("src") #get link full img
                        open_full_img_url = urllib.request.urlopen(get_full_img)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64
                        get_slider_square = driver.find_element(By.XPATH, '//div[contains(@class,"slidebar")] | //div[contains(@class, "cap")]/div[contains(@draggable, "true")]/parent::div')
                        img_width = get_slider_square.value_of_css_property("width")
                        img_width = round(float(img_width.replace('px', '')))
                        img_height = get_slider_square.value_of_css_property("height")
                        img_height = round(float(img_height.replace('px', '')))  
                        small_img_url = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img[contains(@class,"captcha_verify_img_slide")] | //div[contains(@class, "cap") and count(img) = 1]/img/following-sibling::div/img/parent::div').get_attribute("src") 
                        open_small_img_url = urllib.request.urlopen(small_img_url)
                        small_img_url_html_bytes = open_small_img_url.read()
                        small_screenshot_img_url_base64 = base64.b64encode(small_img_url_html_bytes).decode('utf-8')
                        small_img = small_screenshot_img_url_base64
                        get_slider_captcha = driver.find_element(By.XPATH, '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"] | //div[contains(@class, "cap")]/div[contains(@draggable, "true")]/button//*[name()="svg"]')
                        captcha_action_type = "tiktokpuzzle"
                        multipart_form_data = {
                            'FULL_IMG_CAPTCHA': (None, full_img),
                            'SMALL_IMG_CAPTCHA': (None, small_img),
                            'FULL_IMG_WIDTH': (None, img_width),
                            'FULL_IMG_HEIGHT': (None, img_height),
                            'ACTION': (None, captcha_action_type),
                            'USER_KEY': (None, user_api_key)
                        }
                        request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                        response_solve_captcha_content = request_solve_captcha.content
                        if isinstance(response_solve_captcha_content, bytes):
                            response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')
                        if response_solve_captcha_content == "ERROR_USER_KEY":
                            raise Exception("Invalid API key / Make sure you using correct API key")
                        elif response_solve_captcha_content == "ZERO_BALANCE":
                            raise Exception("Balance is zero / Top up your balance")
                        if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                            response_solve_captcha = request_solve_captcha.json()
                            response_cordinate_x = int(response_solve_captcha["cordinate_x"])
                            response_cordinate_y = int(response_solve_captcha["cordinate_y"])
                            random_move_left_right = random.randint(15, 50)
                            random_move_number = random.randint(1, 2)
                            if random_move_number == 1:
                                response_cordinate_x_random_move = int(response_cordinate_x) - int(random_move_left_right)
                                actions.reset_actions()
                                actions.click_and_hold(get_slider_captcha)
                                for i in range(0, 1):
                                    actions.move_by_offset(response_cordinate_x_random_move, 0)  
                                    time.sleep(random.uniform(0.000001, 0.000003))
                                slide_moving_speed = random.uniform(0.000005, 0.000009)
                                remaining_distance = random_move_left_right
                                for i in range(0, random_move_left_right):
                                    if remaining_distance <= 5:
                                        break
                                    random_offset = random.randint(2, min(8, remaining_distance))
                                    actions.move_by_offset(random_offset, 0).perform()
                                    remaining_distance -= random_offset
                                    time.sleep(slide_moving_speed)
                                for i in range(0, remaining_distance):
                                    actions.move_by_offset(1, 0).perform()
                                    time.sleep(slide_moving_speed)
                            else:
                                response_cordinate_x_random_move = int(response_cordinate_x) + int(random_move_left_right)         
                                actions.reset_actions()
                                actions.click_and_hold(get_slider_captcha)
                                for i in range(0, 1):
                                    actions.move_by_offset(response_cordinate_x_random_move, 0)  
                                    time.sleep(random.uniform(0.000001, 0.000003))
                                slide_moving_speed = random.uniform(0.000005, 0.000009)
                                remaining_distance = random_move_left_right
                                for i in range(0, random_move_left_right):
                                    if remaining_distance <= 5:
                                        break
                                    random_offset = random.randint(2, min(8, remaining_distance))
                                    actions.move_by_offset(-random_offset, 0).perform()
                                    remaining_distance -= random_offset
                                    time.sleep(slide_moving_speed)
                                for i in range(0, remaining_distance):
                                    actions.move_by_offset(-1, 0).perform()
                                    time.sleep(slide_moving_speed)
                            actions.release().perform() 
                            time.sleep(10)    
                        else:
                            update_captcha_img.click()
                            time.sleep(random.uniform(8, 10))
                            


                    if len(is_exist_icon_capctha) > 0:
                        get_full_img = driver.find_element(By.XPATH, '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[contains(@src,"/icon_")]')
                        get_question = driver.find_element(By.XPATH, '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//span[text()]').text
                        img_width = round(float(get_full_img.get_attribute("width")))
                        img_height = round(float(get_full_img.get_attribute("height")))
                        coordinate_full_img_url = get_full_img.location
                        coordinate_full_img_url_x = coordinate_full_img_url['x']
                        coordinate_full_img_url_y = coordinate_full_img_url['y']
                        get_full_img_url = get_full_img.get_attribute("src")                  
                        open_full_img_url = urllib.request.urlopen(get_full_img_url)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64
                        captcha_action_type = "tiktokIcon"
                        multipart_form_data = {
                            'FULL_IMG_CAPTCHA': (None, full_img),
                            'CAPTCHA_QUESTION': (None, get_question),
                            'FULL_IMG_WIDTH': (None, img_width),
                            'FULL_IMG_HEIGHT': (None, img_height),
                            'ACTION': (None, captcha_action_type),
                            'USER_KEY': (None, user_api_key)
                        }   
                        request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                        response_solve_captcha_content = request_solve_captcha.content
                        if isinstance(response_solve_captcha_content, bytes):
                            response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')
                        if response_solve_captcha_content == "ERROR_USER_KEY":
                            raise Exception("Invalid API key / Make sure you using correct API key")
                        elif response_solve_captcha_content == "ZERO_BALANCE":
                            raise Exception("Balance is zero / Top up your balance")
                        if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                            json_solve_captcha_data = request_solve_captcha.json()
                            coordinates = [(f"cordinate_x_{i}", f"cordinate_y_{i}") for i in range(1, len(json_solve_captcha_data) // 2 + 1)]
                            target_coordinates = []
                            for x_key, y_key in coordinates:
                                cordinate_x = int(json_solve_captcha_data[x_key])
                                cordinate_y = int(json_solve_captcha_data[y_key])
                                random_move_number = random.randint(1, 2)
                                random_click_coordinates = random.randint(0, 5)
                                if random_move_number == 1:
                                    target_cordinate_x = cordinate_x + coordinate_full_img_url_x - random_click_coordinates
                                    target_cordinate_y = cordinate_y + coordinate_full_img_url_y - random_click_coordinates
                                else:
                                    target_cordinate_x = cordinate_x + coordinate_full_img_url_x + random_click_coordinates
                                    target_cordinate_y = cordinate_y + coordinate_full_img_url_y + random_click_coordinates
                                target_coordinates.append((target_cordinate_x, target_cordinate_y))
                            for x, y in target_coordinates:
                                actions.reset_actions()
                                actions.move_by_offset(x, y).click().perform()
                                time.sleep(random.uniform(0.05, 1))                        
                            driver.find_element(By.XPATH, '//div[contains(@class,"verify-captcha-submit-button")] | //div[contains(@class,"cap")]//img/following-sibling::button').click()
                            time.sleep(random.uniform(10, 12)) 
                        else:
                            update_captcha_img.click()
                            time.sleep(random.uniform(8, 10))
                            
                            
                            
                    if len(is_exist_3d_capctha) > 0:
                        get_full_img = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img | //div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[contains(@src,"/3d_")]')
                        img_width = round(float(get_full_img.get_attribute("width")))
                        img_height = round(float(get_full_img.get_attribute("height")))
                        coordinate_full_img_url = get_full_img.location
                        coordinate_full_img_url_x = coordinate_full_img_url['x']
                        coordinate_full_img_url_y = coordinate_full_img_url['y']
                        get_full_img_url = get_full_img.get_attribute("src")                  
                        open_full_img_url = urllib.request.urlopen(get_full_img_url)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64
                        captcha_action_type = "tiktok3D"
                        multipart_form_data = {
                            'FULL_IMG_CAPTCHA': (None, full_img),
                            'FULL_IMG_WIDTH': (None, img_width),
                            'FULL_IMG_HEIGHT': (None, img_height),
                            'ACTION': (None, captcha_action_type),
                            'USER_KEY': (None, user_api_key)
                        }   
                        request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                        response_solve_captcha_content = request_solve_captcha.content
                        if isinstance(response_solve_captcha_content, bytes):
                            response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')
                        if response_solve_captcha_content == "ERROR_USER_KEY":
                            raise Exception("Invalid API key / Make sure you using correct API key")
                        elif response_solve_captcha_content == "ZERO_BALANCE":
                            raise Exception("Balance is zero / Top up your balance")
                        if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                            json_solve_captcha_data = request_solve_captcha.json()
                            cordinate_x1 = int(json_solve_captcha_data["cordinate_x1"])
                            cordinate_y1 = int(json_solve_captcha_data["cordinate_y1"])
                            cordinate_x2 = int(json_solve_captcha_data["cordinate_x2"])
                            cordinate_y2 = int(json_solve_captcha_data["cordinate_y2"])
                            random_move_number = random.randint(1, 2)
                            random_click_coordinates = random.randint(0, 5)
                            if random_move_number == 1:
                                target_cordinate_x_1 = int(cordinate_x1) + int(coordinate_full_img_url_x) - int(random_click_coordinates)
                                target_cordinate_y_1 = int(cordinate_y1) + int(coordinate_full_img_url_y) - int(random_click_coordinates)
                                target_cordinate_x_2 = int(cordinate_x2) + int(coordinate_full_img_url_x) - int(random_click_coordinates)
                                target_cordinate_y_2 = int(cordinate_y2) + int(coordinate_full_img_url_y) - int(random_click_coordinates)
                            else:
                                target_cordinate_x_1 = int(cordinate_x1) + int(coordinate_full_img_url_x) + int(random_click_coordinates)
                                target_cordinate_y_1 = int(cordinate_y1) + int(coordinate_full_img_url_y) + int(random_click_coordinates)
                                target_cordinate_x_2 = int(cordinate_x2) + int(coordinate_full_img_url_x) + int(random_click_coordinates)
                                target_cordinate_y_2 = int(cordinate_y2) + int(coordinate_full_img_url_y) + int(random_click_coordinates)
                            actions.reset_actions()
                            actions.move_by_offset(target_cordinate_x_1, target_cordinate_y_1).click().perform()
                            actions.reset_actions()
                            time.sleep(random.uniform(0.01, 1))
                            actions.move_by_offset(target_cordinate_x_2, target_cordinate_y_2).click().perform()
                            time.sleep(random.uniform(0.05, 1))    
                            driver.find_element(By.XPATH, '//div[contains(@class,"verify-captcha-submit-button")] | //div[contains(@class,"cap")]//img/following-sibling::button').click()
                            time.sleep(random.uniform(10, 12)) 
                        else:
                            update_captcha_img.click()
                            time.sleep(random.uniform(8, 10))
                            
        except Exception as e:
            print(f"Error: {e}")
    elif action_type == "datadomeaudio" or action_type == "datadomeimage":
        try:
            print("fsfsd")
        except Exception as e:
            print(f"Error: {e}")
    elif action_type == "geetesticon":
        try:
            print("fsfsd")
        except Exception as e:
            print(f"Error: {e}")
    else:
        ("Invalid action type / Supports: tiktokCircle, tiktokPuzzle, tiktok3D, dataDomeAudio, dataDomeImage, geetestIcon")
