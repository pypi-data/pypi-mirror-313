import threading
import logging
import time
from Adlib.funcoes import esperarElemento, getCredenciais, setupDriver

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomationManager:
    def __init__(self, driver_path, login_function, main_task_function):
        self.driver_path = driver_path
        self.login_function = login_function
        self.main_task_function = main_task_function
        self.pause_event = threading.Event()
        self.pause_event.set()  # Initially not paused
        self.thread = threading.Thread(target=self.run_main_task)

    def run_main_task(self):
        self.main_task_function(self.pause_event)

    def start(self):
        self.thread.start()

    def pause(self):
        print("Pausing main task")
        self.pause_event.clear()

    def resume(self):
        print("Resuming main task")
        self.pause_event.set()

    def stop(self):
        print("Stopping automation")
        self.thread.join()

    def check_logout_condition(self) -> bool:
        try:
            return bool(esperarElemento(self.driver, '//*[@id="login"]', tempo_espera=5))
        except:
            return False

    def monitor_logout(self):
        while True:
            time.sleep(self.tempo_espera)
            if self.check_logout_condition():
                logging.info("Logout detected, attempting re-login.")
                self.login_function(self.driver)

    def start_monitoring(self):
        threading.Thread(target=self.monitor_logout, daemon=True).start()

    def start(self):
        self.start_monitoring()
        self.run_main_task()


if __name__ == "__main__":

    def login_facta(driver):
        userBank, passwordBank = getCredenciais(118)
        driver.get('https://desenv.facta.com.br/sistemaNovo/login.php')
        time.sleep(4)
        esperarElemento(driver, '//*[@id="login"]').send_keys(userBank)
        esperarElemento(driver, '//*[@id="senha"]').send_keys(passwordBank)
        time.sleep(2)
        esperarElemento(driver, '//*[@id="btnLogin"]').click()


    def main_task_facta(driver):
        userBank, passwordBank = getCredenciais(118)
        driver.get('https://desenv.facta.com.br/sistemaNovo/login.php')
        driver.maximize_window()
        time.sleep(4)
        esperarElemento(driver, '//*[@id="login"]').send_keys(userBank)
        esperarElemento(driver, '//*[@id="senha"]').send_keys(passwordBank)
        time.sleep(2)
        esperarElemento(driver, '//*[@id="btnLogin"]').click()
        time.sleep(999)

    automation = AutomationManager(
        driver_path=r"C:\Users\dannilo.costa\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe",
        login_function=login_facta,
        main_task_function=main_task_facta
    )
    try:
        automation.start()
    except Exception as e:
        logging.error(f"An error occurred in the automation system: {e}")