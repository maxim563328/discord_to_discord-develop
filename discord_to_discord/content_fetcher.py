from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import urllib
import string


chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome("C:\chromium\chromedriver.exe", options=chrome_options)
driver.get("https://discord.com/login")

time.sleep(2)
driver.execute_script("""function login(token) {
    setInterval(() => {
    document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
    }, 50);
    setTimeout(() => {
    location.reload();
    }, 2500);
}

login("Njk2NzE5NDUxMjE4OTAzMTIw.YiImfg._LAPZFQ8vRQQzp_7H3_YEpRzDUE");""")
time.sleep(3)
driver.refresh()
time.sleep(3)

last_channel = 0

def main(servers, attachment=False):
    global last_channel
    if last_channel != servers["server_get_channel"]:
        driver.get("https://discord.com/channels/{}/{}".format(servers["server_get"], servers["server_get_channel"]))
        last_channel = servers["server_get_channel"]
        time.sleep(5)
    for i in range(3):
        try:
            root = driver.find_element(By.CLASS_NAME, 'scrollerInner-2PPAp2')
            messages_li = root.find_element(By.ID, f'chat-messages-{servers["last_id"]}')
            text = messages_li.find_element(By.ID, f'message-content-{servers["last_id"]}').text
        except:
            driver.refresh()
            time.sleep(3)
        else:
            break
    else:
        text = 403
    if attachment is True:
        img_data = {
        "url": "",
        "file_id": "",
        "errors": []
    }
        for i in range(3):
            try:
                root = driver.find_element(By.CLASS_NAME, 'scrollerInner-2PPAp2')
                messages_li = root.find_element(By.ID, f'chat-messages-{servers["last_id"]}')
                img_data["url"] = messages_li.find_element(By.CLASS_NAME, f'originalLink-Azwuo9').get_attribute('href')
                img_data["file_id"] = random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=6)
            except:
                driver.refresh()
                time.sleep(3)
            else:
                break
        else:
            img_data["errors"].append(403)
        if img_data["errors"] == []:
            for i in range(3):
                try:
                    urllib.urlretrieve(img_data["url"], "attachments/{}.png".format(img_data["file_id"]))
                except:
                    time.sleep(1)
                else:
                    break
            else:
                img_data["errors"].append(405)

            return {"text": text, "img": img_data}
        else:
            return {"text": text, "img": img_data}
    return {"text": text}


# 403 - can`t get image
# 405 - can`t download image

def get_image(servers):
    img_data = {
        "url": "",
        "file_id": "",
    }
    for i in range(3):
        try:
            root = driver.find_element(By.CLASS_NAME, 'scrollerInner-2PPAp2')
            messages_li = root.find_element(By.ID, f'chat-messages-{servers["last_id"]}')
            img_data["url"] = messages_li.find_element(By.CLASS_NAME, f'originalLink-Azwuo9').get_attribute('href')
            img_data["file_id"] = random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=6)
        except:
            driver.refresh()
            time.sleep(3)
        else:
            break
    else:
        return 403
    
    for i in range(3):
        try:
            urllib.urlretrieve(img_data["url"], "attachments/{}.png".format(img_data["file_id"]))
        except:
            time.sleep(1)
        else:
            break
    else:
        return 405
    return img_data

