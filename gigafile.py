import argparse
import os
import pyperclip
import time
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.set_capability('acceptInsecureCerts', True)

def upload_file_and_get_link(file_path:str, password=None):
        try:
            service = webdriver.EdgeService(service_args=['--log-level=OFF'], log_output=None)
            driver = webdriver.Edge(options=options, service=service)
            print("ページを読み込んでいます")
            driver.get("https://gigafile.nu/")
            upload_panel = driver.find_element(By.ID, 'upload_panel_button')
            file_input = upload_panel.find_element(By.XPATH, ".//input[@type='file']")
            print(file_input.text)
            file_input.send_keys(file_path)
            time.sleep(1)
            print("アップロードしています")
            while True:
                time.sleep(1)
                elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'prog file_info_prog')]")
                all_complete = True
                for elementss in elements:
                    if "width: 100%;" not in elementss.get_attribute('style'):
                        all_complete = False
                        break
                if all_complete:
                    break
            print("zipにしています")
            password_field = driver.find_element(By.ID, "zip_dlkey")
            password_field.send_keys(password)
            zip_file_field = driver.find_element(By.ID, "zip_file_name")
            zip_file_field.send_keys("FILE")
            set_button = driver.find_element(By.ID, "matomete_btn")
            driver.execute_script("arguments[0].click();", set_button)
            time.sleep(1)
            alert = Alert(driver)
            alert_text = alert.text
            print(alert_text)
            alert.accept()
            link_element = driver.find_element(By.XPATH, "//a[@id='matomete_link_btn']")
            link = link_element.get_attribute("href")
            print("成功")
            print("クリップボードにコピーされました!")
            with open(os.path.join(os.path.dirname(file_path), 'upload_config.conf'), 'w', encoding='utf-8') as configfile:
                configfile.write('[{}]\nPassword: {}'.format(link, password))
            return '{}'.format(link)
        except:
            print("失敗")
            return "共有リンクの作成に失敗しました"

def main():
    Ap = argparse.ArgumentParser()
    Ap.add_argument("PATH", nargs='?', help="ファイルパスを入力")
    Ap.add_argument("-nP", "--none-password", help="パスワードが不要な場合に使用")
    Ap.add_argument("-c", "--configfile", nargs='?', help="設定ファイルを読み込むときに使用")
    Arguments = Ap.parse_args()
    # 各引数について確認します。
    if Arguments.none_password:
        password = None
        PATHs = Arguments.none_password
    elif Arguments.configfile:
        config_file = open(Arguments.configfile, 'r', encoding='utf-8').read()
        PATHs = Arguments.PATH
        password = config_file.split('\nPassword: ')[1]
    elif Arguments.PATH:
        password = input("パスワード>> ")
        PATHs = Arguments.PATH
    if os.path.isdir(PATHs):
        print(f"{PATHs} is a directory. Exiting.")
    if not '\\' or not '/' in PATHs:
        PATHs = os.path.join(os.getcwd(), PATHs)
    pyperclip.copy(upload_file_and_get_link(PATHs, password=password))

if __name__ == '__main__':
    main()