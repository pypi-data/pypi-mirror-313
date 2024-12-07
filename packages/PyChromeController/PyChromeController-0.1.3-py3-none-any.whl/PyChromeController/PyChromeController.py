from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import urlparse
import subprocess
import pyautogui
import pyperclip
import time

class PyChromeController(object):

    def __init__(self, driver=None, options=None, headless=False, command_executor="http://localhost:4444/wd/hub"):
        """
        Initializes the ChromeController object.

        :param driver: An existing WebDriver instance (default is None).
        :param options: Browser options (default is None).
        :param headless: Boolean flag to enable/disable headless mode (default is False).
        :param command_executor: URL for the WebDriver server (default is "http://localhost:4444/wd/hub").
        """
        self.driver = driver
        self.options = options
        self.headless = headless
        self.command_executor = command_executor
        self.session_id = None

    def start_browser_session(self) -> bool:
        """
        Starts a new browser session.

        :return: True if the session starts successfully, False otherwise.
        """
        try:
            self.options = Options()
            self.options.headless = self.headless
            self.options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
            self.options.add_argument("--disable-popup-blocking")    # Prevent pop-ups

            # Performance-Logs in den Optionen aktivieren
            self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

            # Connect with the Remote WebDriver
            self.driver = webdriver.Remote(
                command_executor=self.command_executor,  # Server address
                options=self.options
            )
            self.session_id = self.driver.session_id
            return True
        except Exception as e:
            print(f"Error starting browser session: {e}")
            return False

    def attach_browser_session(self, session_id=None) -> bool:
        """
        Resumes an existing browser session based on a session ID.

        :param session_id: Optional session ID to attach (default is None).
        :return: True if the session is attached successfully, False otherwise.
        """
        try:
            self.options = Options()
            self.options.headless = self.headless
            self.options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
            self.options.add_argument("--disable-popup-blocking")    # Prevent pop-ups

            # Performance-Logs in den Optionen aktivieren
            self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

            self.driver = webdriver.Remote(
                command_executor=self.command_executor,
                options=self.options
            )

            self.driver.close()

            if session_id is None:
                self.driver.session_id = self.session_id
            else:
                self.driver.session_id = session_id
            self.session_id = self.driver.session_id
            return True
        except Exception as e:
            print(f"Error attaching browser session: {e}")
            return False

    def minimize_window(self) -> bool:
        """
        Minimizes the current window.

        :return: True if the operation is successful, False otherwise.
        """
        try:
            self.driver.minimize_window()
            return True
        except Exception as e:
            print(f"Error minimizing window: {e}")
            return False

    def maximize_window(self) -> bool:
        """
        Maximizes the current window.

        :return: True if the operation is successful, False otherwise.
        """
        try:
            self.driver.maximize_window()
            return True
        except Exception as e:
            print(f"Error maximizing window: {e}")
            return False

    def close_window(self) -> bool:
        """
        Closes the current window.

        :return: True if the operation is successful, False otherwise.
        """
        try:
            self.driver.close()
            return True
        except Exception as e:
            print(f"Error closing window: {e}")
            return False

    def close_browser(self) -> bool:
        """
        Closes the browser.

        :return: True if the operation is successful, False otherwise.
        """
        try:
            self.driver.quit()
            return True
        except Exception as e:
            print(f"Error closing browser: {e}")
            return False

    def open_url(self, url: str) -> bool:
        """
        Opens the specified URL inside the first tab.

        :param url: URL to open in the first tab.
        :return: True if the operation is successful, False otherwise.
        """
        self.driver.get(url)
        return True
        
    def open_new_tab(self, url):
        """
        Opens a new tab with the specified URL.

        :param url: URL to open in the new tab.
        :return: True if the operation is successful, False otherwise.
        """
        try:
            # Check if the browser is still active
            if not self.driver.window_handles:
                print("No active browser windows found.")
                return False

            # Open a new tab using JavaScript
            self.driver.execute_script(f"window.open('{url}');")
        
            # Wait briefly to ensure the new tab is registered
            time.sleep(1)

            # Verify if the tab was successfully added
            if len(self.driver.window_handles) > 0:
                print(f"Tab successfully opened with URL: {url}")
                return True
            else:
                print("Failed to open the new tab.")
                return False
        except Exception as e:
            print(f"Error opening tab with URL '{url}': {e}")
            return False

    def open_blank_tab(self) -> bool:
        """
        Opens a new blank tab without any URL.

        :return: Always returns True.
        """
        self.maximize_window()
        pyautogui.hotkey("ctrl", "t")
        time.sleep(0.5)
        return True

    def close_first_tab(self) -> bool:
        """
        Closes the first tab.

        :return: True if the tab is closed successfully, False otherwise.
        """
        if self.switch_tab(0):
            return self.close_tab()
        print("Failed to close the first tab.")
        return False

    def close_last_tab(self) -> bool:
        """
        Closes the last tab.

        :return: True if the tab is closed successfully, False otherwise.
        """
        last_tab_index = len(self.driver.window_handles) - 1
        if last_tab_index >= 0:
            if self.switch_tab(last_tab_index):
                return self.close_tab()
        print("Failed to close the last tab.")
        return False

    def close_tab(self) -> bool:
        """
        Closes the currently active tab.

        :return: True if the tab is closed successfully, False otherwise.
        """
        try:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return True
        except Exception as e:
            print(f"Error closing tab: {e}")
            return False

    def close_tab_by_index(self, index):
        """
        Closes a tab by its index in the window_handles list.

        :param index: Index of the tab to close.
        :return: True if the operation is successful, False otherwise.
        """
        try:
            # Ensure there are active tabs
            if not self.driver.window_handles:
                print("No active tabs to close.")
                return False
            
            # Validate the index
            if index < 0 or index >= len(self.driver.window_handles):
                print(f"Invalid index: {index}. Total tabs: {len(self.driver.window_handles)}")
                return False

            # Switch to the desired tab
            self.driver.switch_to.window(self.driver.window_handles[index])

            # Close the tab
            self.driver.close()
            print(f"Tab at index {index} closed.")
            
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            return True
        except Exception as e:
            print(f"Error closing tab at index {index}: {e}")
            return False

    def close_tab_by_url(self, target_url: str) -> bool:
        """
        Closes a tab based on a URL.

        :param target_url: URL of the tab to close.
        :return: True if the tab is closed successfully, False otherwise.
        """
        if self.switch_tab_by_url(target_url):
            return self.close_tab()
        print(f"Failed to close tab with URL '{target_url}'.")
        return False

    def close_tab_by_title(self, target_title: str) -> bool:
        """
        Closes a tab based on a title.

        :param target_title: Title or partial title of the tab to close.
        :return: True if the tab is closed successfully, False otherwise.
        """
        if self.switch_tab_by_title(target_title):
            return self.close_tab()
        print(f"Failed to close tab with title containing '{target_title}'.")
        return False

    def close_tab_by_image(self, image_path: str) -> bool:
        """
        Closes a tab based on an image of the searched tab.

        :param image_path: Path to the image to locate and close the tab.
        :return: True if the tab is closed successfully, False otherwise.
        """
        if self.switch_tab_by_image(image_path):
            return self.close_tab()
        print(f"Failed to close tab by image containing '{image_path}'.")
        return False

    def switch_tab(self, index: int = 0) -> bool:
        """
        Switches to a tab based on its index.

        :param index: Index of the tab to switch to (default is 0).
        :return: True if the tab is switched successfully, False otherwise.
        """
        try:
            if len(self.driver.window_handles) <= 1:
                print("Only one tab open. No switch possible.")
                return False

            if 0 <= index < len(self.driver.window_handles):
                self.driver.switch_to.window(self.driver.window_handles[index])
                print(f"Switched to tab #{index} with title: {self.driver.title}")
                return True

            print(f"No tab found for index {index}.")
            return False
        except Exception as e:
            print(f"Error switching to tab #{index}: {e}")
            return False

    def switch_tab_by_url(self, target_url: str) -> bool:
        """
        Switches to a tab based on its URL.
        :param target_url: URL of the tab to switch to.
        :return: True if the tab with the specified URL is found and switched, False otherwise.
        """
        try:
            target_netloc = urlparse(target_url).netloc  # Extrahiere Hostname der Ziel-URL
            for window in self.driver.window_handles:
                self.driver.switch_to.window(window)
                current_url = self.driver.current_url
                current_netloc = urlparse(current_url).netloc  # Extrahiere Hostname der aktuellen URL
                if target_netloc in current_netloc:  # Vergleiche nur Hostnames
                    print(f"Tab with URL '{target_url}' found and switched.")
                    return True
            print(f"No tab with URL '{target_url}' found.")
            return False
        except Exception as e:
            print(f"Error switching tab by URL '{target_url}': {e}")
            return False

    def switch_tab_by_title(self, target_title: str) -> bool:
        """
        Switches to a tab based on its title.

        :param target_title: Title or partial title of the tab to switch to.
        :return: True if the tab with the specified title is found and switched, False otherwise.
        """
        try:
            for window in self.driver.window_handles:
                self.driver.switch_to.window(window)
                if target_title in self.driver.title:
                    print(f"Tab with title '{target_title}' found and switched.")
                    return True
            print(f"No tab with title '{target_title}' found.")
            return False
        except Exception as e:
            print(f"Error switching tab by title '{target_title}': {e}")
            return False

    def switch_tab_by_image(self, image_path: str) -> bool:
        """
        Switches to a tab based on an image of the tab.

        :param image_path: File path of the image to locate the tab.
        :return: True if the tab with the specified image is found and switched, False otherwise.
        """
        self.minimize_window()
        self.maximize_window()
        time.sleep(1)

        tab_image_center = None
        timeout = 10  # Timeout in seconds
        start_time = time.time()  # Set start time

        while tab_image_center is None:
            tab_image = pyautogui.locateOnScreen(image_path, confidence=0.85)

            if tab_image is not None:
                tab_image_center = pyautogui.center(tab_image)
                pyautogui.click(tab_image_center)
                return True  # Tab found

            # Check whether timeout has been exceeded
            if time.time() - start_time > timeout:
                print(f"Timeout: No tab with the image {image_path} found.")
                return False  # Timeout reached, tab not found

    def write_session_id_to_file(self, path_to_file: str) -> bool:
        """
        Saves the current session ID to a file.

        :param path_to_file: Path of the file where the session ID will be saved.
        :return: True if the session ID is successfully written to the file, False otherwise.
        """
        try:
            self.session_id = self.driver.session_id
            with open(path_to_file, "w") as file:
                file.write(str(self.session_id))
            print(f"Saved session id: {self.session_id}")
            return True
        except Exception as e:
            print(f"Error writing session ID to file: {e}")
            return False

    def read_session_id_from_file(self, path_to_file: str) -> str:
        """
        Reads the session ID from a file.

        :param path_to_file: Path of the file to read the session ID from.
        :return: The session ID as a string, or an empty string if reading fails.
        """
        try:
            with open(path_to_file, "r") as file:
                self.session_id = file.read().strip()
            print(f"Read session id: {self.session_id}")
            return self.session_id
        except Exception as e:
            print(f"Error reading session ID from file: {e}")
            return ""

    def get_all_urls(self) -> list:
        """
        Returns a list of all URLs from open tabs.

        :return: A list of URLs from all open tabs, or an empty list if no URLs are found.
        """
        all_urls = []
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            all_urls.append(self.driver.current_url)

        if len(all_urls) > 1:
            return all_urls
        else:
            print("No URLs found.")
            return []

    def get_all_titles(self) -> list:
        """
        Returns a list of all titles from open tabs.

        :return: A list of titles from all open tabs, or an empty list if no titles are found.
        """
        all_titles = []
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            all_titles.append(self.driver.title)

        if len(all_titles) > 1:
            return all_titles
        else:
            print("No titles found.")
            return []

    def fetch_tab_urls(self) -> list:
        """
        Fetch the URLs of the open Chrome tabs.

        The method iterates through a maximum of 10 open tabs in Chrome, copying their URLs 
        from the address bar using keyboard shortcuts and adding them to a list. It avoids 
        duplicates and stops if it encounters a URL already in the list.

        Returns:
            list: A list of unique URLs from the currently open tabs. If there are no tabs or 
                an error occurs, the list may be empty.
        """
        self.minimize_window()
        self.maximize_window()
        time.sleep(1)

        tab_urls = []
        for _ in range(10):  # Assumption: Maximum 10 tabs
            # Set focus on the address bar and copy URL
            pyautogui.hotkey("ctrl", "l")  # Focus on the address bar
            time.sleep(0.2)
            pyautogui.hotkey("ctrl", "c")  # Copy the URL
            time.sleep(0.2)

            # Get the URL from the clipboard with pyperclip
            url = pyperclip.paste()

            # Avoid duplicate URLs and end the loop
            if url in tab_urls:
                break
            tab_urls.append(url)

            # Switch to the next tab
            pyautogui.hotkey("ctrl", "tab")
            time.sleep(0.5)

        return tab_urls

    def fetch_tab_titles(self) -> list:
        """
        Fetch the titles of the open Chrome tabs.

        The method iterates through a maximum of 10 open tabs in Chrome, retrieving the title 
        of each tab's window using the `xdotool` utility and adding it to a list. It avoids 
        duplicates and stops if it encounters a title already in the list.

        Returns:
            list: A list of unique window titles from the currently open tabs. If there are no tabs 
                or an error occurs, the list may be empty.
        """
        self.minimize_window()
        self.maximize_window()
        time.sleep(1)  # Give the system time to set the focus

        tab_titles = []
        for _ in range(10):  # Assumption: Maximum 10 tabs
            # Get the window title of the active tab
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                stdout=subprocess.PIPE,
                text=True,
            )
            window_title = result.stdout.strip()

            # Avoid duplicate titles and end the loop
            if window_title in tab_titles:
                break
            tab_titles.append(window_title)

            # Switch to the next tab
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(0.5)  # Wait briefly so that the next tab is loaded

        return tab_titles

    def check_title_in_list(self, target_title: str) -> bool:
        """
        Checks if a specific title exists in the list of open tab titles.

        :param target_title: The title to search for.
        :return: True if the title is found, False otherwise.
        """
        all_titles = self.get_all_titles()
        if target_title in all_titles:
            print(f"Title '{target_title}' found in open tabs.")
            return True
        else:
            print(f"Title '{target_title}' not found in open tabs.")
            return False

    def check_url_in_list(self, target_url: str) -> bool:
        """
        Checks whether a specific URL is present in the list of open tab URLs.

        :param target_url: The URL to search for.
        :return: True if the URL is found, False otherwise.
        """
        all_urls = self.get_all_urls()
        if target_url in all_urls:
            print(f"URL '{target_url}' found in open tabs.")
            return True
        else:
            print(f"URL '{target_url}' not found in open tabs.")
            return False

    def check_and_open_tab_by_url(self, target_url: str) -> None:
        """
        Checks whether a specific URL is present in the list of open tab URLs. 
        If yes, it switches to this tab; if no, a new tab with this URL is opened.

        Args:
            target_url (str): The URL to search for in the open tabs.
        
        Returns:
            None
        """
        if not self.switch_tab_by_url(target_url):
            self.open_new_tab(target_url)

    def check_and_open_tab_by_title(self, target_title: str, target_url: str) -> None:
        """
        Checks whether a specific title is present in the list of open tab titles. 
        If yes, it switches to this tab; if no, a new tab with the provided URL is opened.

        Args:
            target_title (str): The title to search for in the open tabs.
            target_url (str): The URL to open in a new tab if the title is not found.

        Returns:
            None
        """
        if not self.switch_tab_by_title(target_title):
            self.open_new_tab(target_url)

    def write_and_enter_url(self, url: str) -> None:
        """
        Writes and enters the specified URL in the address bar of the currently selected tab.

        This function formats the URL correctly if it contains "https://" or "http://", 
        and handles domain and path separately to ensure proper input.

        Args:
            url (str): The URL to write and enter into the address bar.

        Returns:
            None
        """
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.2)
        
        # Check whether "https://"" or "http://"" is present in the URL and separate it
        if "https://" in url:
            pyautogui.write("https:", interval=0.1)
            pyautogui.hotkey("shift", "7")
            pyautogui.hotkey("shift", "7")
            url = url.replace("https://", "", 1)
        elif "http://" in url:
            pyautogui.write("http:", interval=0.1)
            pyautogui.hotkey("shift", "7")
            pyautogui.hotkey("shift", "7")
            url = url.replace("http://", "", 1)

        # Split the URL at "/" and treat the first part separately
        if "/" in url:
            url_parts = url.split("/", 1)  # Parts only on the first "/"
            pyautogui.write(url_parts[0], interval=0.1)  # Output of the domain part
            url = url_parts[1] if len(url_parts) > 1 else ""
            if url:  # Only split if there is actually a path
                url = url.split("/")
        else:
            pyautogui.write(url, interval=0.1)  # If there is no "/", just enter the URL
            url = []  # Empty list to execute the following code cleanly

        # Enter the remaining parts of the URL
        for part in url:
            pyautogui.hotkey("shift", "7")
            pyautogui.write(part)
        
        pyautogui.press("enter")

    def change_url(self, new_url: str) -> bool:
        """
        Changes the URL of the current active tab.

        Args:
            new_url (str): The new URL to navigate to.

        Returns:
            bool: True if the URL was successfully changed, False otherwise.
        """
        try:
            self.write_and_enter_url(new_url)
            return True
        except Exception as e:
            print(f"Error while changing URL to '{new_url}': {e}")
            return False

    def change_url_of_tab(self, new_url: str, index: int = 0) -> bool:
        """
        Switches to a tab based on the index and changes the URL.

        Args:
            new_url (str): The new URL to navigate to.
            index (int, optional): The index of the tab to switch to. Defaults to 0.

        Returns:
            bool: True if the URL was successfully changed, False otherwise.
        """
        try:
            if self.switch_tab(index):
                self.write_and_enter_url(new_url)
                return True
            else:
                print(f"Failed to switch to tab with index {index}.")
                return False
        except Exception as e:
            print(f"Error while changing URL of tab {index} to '{new_url}': {e}")
            return False

    def change_url_of_tab_by_url(self, old_url: str, new_url: str) -> bool:
        """
        Switches to a tab based on a URL and changes the URL.

        Args:
            old_url (str): The URL of the tab to switch to.
            new_url (str): The new URL to navigate to.

        Returns:
            bool: True if the URL was successfully changed, False otherwise.
        """
        try:
            if self.switch_tab_by_url(old_url):
                self.write_and_enter_url(new_url)
                return True
            else:
                print(f"Tab with URL '{old_url}' not found.")
                return False
        except Exception as e:
            print(f"Error while changing URL of tab with URL '{old_url}' to '{new_url}': {e}")
            return False

    def change_url_of_tab_by_title(self, target_title: str, new_url: str) -> bool:
        """
        Switches to a tab based on a title and changes the URL.

        Args:
            target_title (str): The title of the tab to switch to.
            new_url (str): The new URL to navigate to.

        Returns:
            bool: True if the URL was successfully changed, False otherwise.
        """
        try:
            if self.switch_tab_by_title(target_title):
                self.write_and_enter_url(new_url)
                return True
            else:
                print(f"Tab with title '{target_title}' not found.")
                return False
        except Exception as e:
            print(f"Error while changing URL of tab with title '{target_title}' to '{new_url}': {e}")
            return False

    def change_url_of_tab_by_image(self, new_url: str, image_path: str) -> bool:
        """
        Switches to a tab based on an image of the searched tab and changes the URL.

        Args:
            new_url (str): The new URL to navigate to.
            image_path (str): The file path to the image used to identify the tab.

        Returns:
            bool: True if the URL was successfully changed, False otherwise.
        """
        try:
            if self.switch_tab_by_image(image_path):
                self.write_and_enter_url(new_url)
                return True
            else:
                print(f"Tab with image at '{image_path}' not found.")
                return False
        except Exception as e:
            print(f"Error while changing URL of tab identified by image '{image_path}' to '{new_url}': {e}")
            return False

    def enter_text(self, by, locator, text):
        """Finds the element by the specified locator and enters the provided text into a text field.
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the element.
            text: The text to be entered into the text field.
        """
        element = self.driver.find_element(by, locator)
        element.clear()  # Optional cleanup of the text field before entering new text
        element.send_keys(text)

    def click_button(self, by, locator):
        """Finds the element by the specified locator and clicks the button.
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the element.
        """
        element = self.driver.find_element(by, locator)
        element.click()

    def toggle_checkbox(self, by, locator, state):
        """Finds the checkbox element by the specified locator and toggles it to the desired state (checked or unchecked).
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the checkbox element.
            state: The desired state of the checkbox (True for checked, False for unchecked).
        """
        element = self.driver.find_element(by, locator)
        if element.is_selected() != state:
            element.click()

    def select_dropdown(self, by, locator, value=None, visible_text=None):
        """Selects an option from a dropdown menu based on either the value or visible text.
        
        Args:
            by: The method used to locate the dropdown element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the dropdown element.
            value: The value of the option to be selected (optional).
            visible_text: The visible text of the option to be selected (optional).
        """
        element = self.driver.find_element(by, locator)
        select = Select(element)
        if value:
            select.select_by_value(value)
        elif visible_text:
            select.select_by_visible_text(visible_text)

    def select_radio_button(self, driver, by, locator):
        """Finds a radio button element by the specified locator and selects it if it is not already selected.
        
        Args:
            driver: The WebDriver instance being used.
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the radio button element.
        """
        element = driver.find_element(by, locator)
        if not element.is_selected():
            element.click()

    def click_link(self, by, locator):
        """Finds the link element by the specified locator and clicks on it.
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the link element.
        """
        element = self.driver.find_element(by, locator)
        element.click()

    def upload_file(self, by, locator, file_path):
        """Finds the file input element by the specified locator and uploads a file.
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the file input element.
            file_path: The full path to the file to be uploaded.
        """
        element = self.driver.find_element(by, locator)
        element.send_keys(file_path)

    def take_screenshot(self, file_name):
        """Takes a screenshot of the current browser window and saves it to the specified file path.
        
        Args:
            file_name: The file path where the screenshot should be saved.
        """
        self.driver.save_screenshot(file_name)

    def scroll_to_element(self, by, locator):
        """Scrolls the page to bring the specified element into view.
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the element to scroll to.
        """
        element = self.driver.find_element(by, locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def hover_over_element(self, by, locator):
        """Hovers the mouse over the specified element.
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the element to hover over.
        """
        element = self.driver.find_element(by, locator)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    def verify_text(self, by, locator, expected_text):
        """Verifies that the text of the specified element matches the expected text.
        
        Args:
            by: The method used to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string used to identify the element.
            expected_text: The text that should match the element's text.
        
        Raises:
            AssertionError: If the text of the element does not match the expected text.
        """
        element = self.driver.find_element(by, locator)
        assert element.text == expected_text, f"Text mismatch: {element.text} != {expected_text}"

    def get_browser_info(self) -> dict:
        """
        Returns browser version and user-agent.

        Returns:
            dict: A dictionary containing the browser version, platform name, and user-agent string.
                Keys: "browser_version", "platform_name", "user_agent".
                Returns an empty dictionary if an error occurs.
        """
        try:
            browser_version = self.driver.capabilities.get("browserVersion", "Unknown")
            platform_name = self.driver.capabilities.get("platformName", "Unknown")
            user_agent = self.driver.execute_script("return navigator.userAgent;")
            return {
                "browser_version": browser_version,
                "platform_name": platform_name,
                "user_agent": user_agent,
            }
        except Exception as e:
            print(f"Error getting browser information: {e}")
            return {}

    def add_cookie(self, name: str, value: str, domain: str = None, path: str = "/") -> bool:
        """
        Adds a cookie to the current session.

        Args:
            name (str): The name of the cookie.
            value (str): The value of the cookie.
            domain (str, optional): The domain for the cookie. Defaults to None.
            path (str, optional): The path for the cookie. Defaults to "/".

        Returns:
            bool: True if the cookie is added successfully, False otherwise.
        """
        try:
            cookie = {"name": name, "value": value, "path": path}
            if domain:
                cookie["domain"] = domain
            self.driver.add_cookie(cookie)
            print(f"Cookie '{name}' added successfully.")
            return True
        except Exception as e:
            print(f"Error adding cookie: {e}")
            return False

    def delete_cookie(self, name: str) -> bool:
        """
        Deletes a cookie by name.

        Args:
            name (str): The name of the cookie to delete.

        Returns:
            bool: True if the cookie is deleted successfully, False otherwise.
        """
        try:
            self.driver.delete_cookie(name)
            print(f"Cookie '{name}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting cookie: {e}")
            return False

    def get_all_cookies(self) -> list:
        """
        Returns all cookies for the current session.

        Returns:
            list: A list of dictionaries representing the cookies. Returns an empty list if an error occurs.
        """
        try:
            return self.driver.get_cookies()
        except Exception as e:
            print(f"Error retrieving cookies: {e}")
            return []

    def close_all_other_tabs(self) -> bool:
        """
        Closes all tabs except the current one.

        Returns:
            bool: True if all other tabs are closed successfully, False otherwise.
        """
        try:
            current_tab = self.driver.current_window_handle
            all_tabs = self.driver.window_handles
            for tab in all_tabs:
                if tab != current_tab:
                    self.driver.switch_to.window(tab)
                    self.driver.close()
            self.driver.switch_to.window(current_tab)
            print("Closed all other tabs successfully.")
            return True
        except Exception as e:
            print(f"Error closing other tabs: {e}")
            return False

    def get_console_logs(self) -> list:
        """
        Fetches the browser console logs.

        Returns:
            list: A list of console log entries. Returns an empty list if an error occurs.
        """
        try:
            logs = self.driver.get_log("browser")
            return logs
        except Exception as e:
            print(f"Error fetching console logs: {e}")
            return []

    def get_network_logs(self) -> list:
        """
        Fetches network logs (if supported by the driver).

        Returns:
            list: A list of network log entries. Returns an empty list if an error occurs.
        """
        try:
            logs = self.driver.get_log("performance")
            network_logs = [entry for entry in logs if "Network" in entry["message"]]
            return network_logs
        except Exception as e:
            print(f"Error fetching network logs: {e}")
            return []

    def take_element_screenshot(self, by: str, locator: str, file_name: str) -> bool:
        """
        Takes a screenshot of a specific element.

        Args:
            by (str): The method to locate the element (e.g., By.ID, By.XPATH).
            locator (str): The locator string to find the element.
            file_name (str): The file path where the screenshot should be saved.

        Returns:
            bool: True if the screenshot is saved successfully, False otherwise.
        """
        try:
            element = self.driver.find_element(by, locator)
            element.screenshot(file_name)
            print(f"Screenshot saved as {file_name}.")
            return True
        except Exception as e:
            print(f"Error taking screenshot of element: {e}")
            return False

    def drag_and_drop(self, source_locator: tuple, target_locator: tuple) -> bool:
        """
        Drags an element from source to target.

        Args:
            source_locator (tuple): A tuple containing the method to locate the source element (e.g., (By.ID, "source_id")).
            target_locator (tuple): A tuple containing the method to locate the target element (e.g., (By.ID, "target_id")).

        Returns:
            bool: True if the drag-and-drop action is completed successfully, False otherwise.
        """
        try:
            source = self.driver.find_element(*source_locator)
            target = self.driver.find_element(*target_locator)
            ActionChains(self.driver).drag_and_drop(source, target).perform()
            print("Drag-and-drop action completed.")
            return True
        except Exception as e:
            print(f"Error performing drag-and-drop: {e}")
            return False

    def send_keys_to_body(self, keys: str) -> bool:
        """
        Sends key events to the body of the current page.

        Args:
            keys (str): The keys to send to the body element.

        Returns:
            bool: True if the keys are sent successfully, False otherwise.
        """
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(keys)
            print(f"Sent keys '{keys}' to the body.")
            return True
        except Exception as e:
            print(f"Error sending keys to body: {e}")
            return False

    def recover_session(self) -> bool:
        """
        Attempts to recover from a browser crash.

        Returns:
            bool: True if the session is recovered successfully, False otherwise.
        """
        try:
            self.driver.get("chrome://crash")
            print("Recovered browser session.")
            return True
        except Exception as e:
            print(f"Error recovering session: {e}")
            return False

    def wait_for_element(self, by: str, locator: str, timeout: int = 10):
        """
        Waits for an element to be present within a specified timeout.

        Args:
            by (str): The method to locate the element (e.g., By.ID, By.XPATH).
            locator (str): The locator string to find the element.
            timeout (int, optional): The maximum time to wait for the element, in seconds. Defaults to 10.

        Returns:
            WebElement: The found element if successful.
            None: If the element is not found within the timeout.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            print(f"Element found: {locator}")
            return element
        except Exception as e:
            print(f"Error waiting for element {locator}: {e}")
            return None

    def accept_cookies(self, id_name: str = "cookie", class_name: str = "cookie", accept_name: str = "accept") -> None:
        """
        Accepts cookies if the button is present, with customizable selectors.

        This function attempts to locate and click on cookie acceptance buttons 
        using various selectors. If no button is found or an error occurs, 
        the function handles exceptions gracefully.

        Args:
            id_name (str, optional): Part of the ID attribute for the cookie button. Default is "cookie".
            class_name (str, optional): Part of the class attribute for the cookie button or banner. Default is "cookie".
            accept_name (str, optional): Part of the ID, class, or text for the accept button. Default is "accept".

        Returns:
            None
        """
        try:
            # List of possible selectors for cookie buttons
            cookie_selectors = [
                f"button[id*='{id_name}']",    # Cookie button, based on ID
                f"button[class*='{class_name}']",  # Cookie button, based on class
                f"div[class*='{class_name}']",    # Cookie banner, based on div class
                f"button[id*='{accept_name}']",    # Accept cookie button based on ID
                f"//button[contains(text(), '{accept_name}')]"  # XPath selector for button with text
            ]
            
            # Try to find the cookie button with different selectors
            for selector in cookie_selectors:
                try:
                    if selector.startswith("//"):  # XPath selector
                        cookie_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:  # CSS selector
                        cookie_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    cookie_button.click()
                    print(f"Cookies accepted using selector: {selector}")
                    break  # Successfully accepted, cancel loop
                except (NoSuchElementException, TimeoutException):
                    continue  # If the button was not found, continue with the next selector

        except Exception as e:
            print(f"Error accepting cookies: {e}")

    def click_by_image(self, image_path: str) -> bool:
        """
        Clicks on an element on the screen based on an image.

        This function uses `pyautogui` to locate an image on the screen 
        and clicks on its center. If the image is not found within the 
        specified timeout, it returns `False`.

        Args:
            image_path (str): The file path to the image to locate on the screen.

        Returns:
            bool: `True` if the image was found and clicked, `False` otherwise.
        """
        self.minimize_window()
        self.maximize_window()
        time.sleep(1)

        image_center = None
        timeout = 10  # Timeout in seconds
        start_time = time.time()  # Set start time

        while image_center is None:
            image = pyautogui.locateOnScreen(image_path, confidence=0.85)

            if image is not None:
                image_center = pyautogui.center(image)
                pyautogui.click(image_center)
                return True  # Image found and clicked

            # Check whether timeout has been exceeded
            if time.time() - start_time > timeout:
                print(f"Timeout: No tab with the image {image_path} found.")
                return False  # Timeout reached, image not found
