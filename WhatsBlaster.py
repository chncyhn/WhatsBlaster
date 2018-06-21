from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time


class WhatsBlaster:

    def __init__(self, chromedriver_path):
        options = webdriver.ChromeOptions()
        options.add_argument("--force-device-scale-factor=1")
        self.driver = webdriver.Chrome(chromedriver_path, chrome_options=options)
        self.driver.get("https://web.whatsapp.com")
        print("Login, and wait for app to load." )
        input("Then, hit enter to continue. ")

    def close(self):
        self.driver.close()

    def forward_message(self, contact_names):
        input("Select your message to forward, then click ENTER here.")
        driver = self.driver

        fails = []
        for contact_name in contact_names:
            popup_box = driver.find_element_by_css_selector("div[data-animate-modal-popup='true']")
            search = driver.find_element_by_css_selector("input[title='Search\u2026']")
            search.send_keys(contact_name)
            time.sleep(2)
            try:
                popup_box.find_element_by_css_selector(
                                "span[title='{}']".format(contact_name)
                                ).click()
            except:
                print("Failure: could not find contact {}.".format(contact_name))
                fails.append(contact_name)

            search.clear()
            time.sleep(2)

        popup_box = driver.find_element_by_css_selector("div[data-animate-modal-popup='true']")
        send_button = popup_box.find_element_by_css_selector("span[data-icon='send-light']")
        send_button.click()
        time.sleep(10)
        if fails:
            return "Failed to send " + ",".join(fails)
        else:
            return "All successfully sent."

    def send_message(self, contact_name, message, timeout=10):
        driver = self.driver
        # Find contact
        search = driver.find_element_by_css_selector("input[title='Search or start new chat']")
        search.send_keys(contact_name)
        try:
            element = WebDriverWait(driver, 10).until(
                    lambda driver: driver.find_element_by_css_selector(
                        "span[title='{}']".format(contact_name)
                        ))
        except:
            return "Failure: could not find contact {}.".format(contact_name)
        # Load chat
        time.sleep(4)
        driver.find_element_by_css_selector(
                "#pane-side span[title='{}']".format(contact_name)
                ).click()
        try:
            element = WebDriverWait(driver, 10).until(
                    lambda driver: driver.find_element_by_css_selector(
                        "#main [title='{}']".format(contact_name)
                        ))
        except:
            return "Failure: could not load chat with contact {}.".format(contact_name)
        # Send message + wait until successful
        messages_0 = driver.find_elements_by_css_selector("#main span.selectable-text.invisible-space.copyable-text")
        input_element = driver.find_element_by_css_selector("footer div.copyable-text.selectable-text")
        input_element.send_keys(message)
        input_element.send_keys(Keys.ENTER)
        for t in range(timeout):
            messages_1 = driver.find_elements_by_css_selector("#main span.selectable-text.invisible-space.copyable-text")
            if len(messages_0) != len(messages_1):
                return "Success: sent to {}.".format(contact_name)
            time.sleep(1)
        return "Message to {} may not have been sent.".format(contact_name)
