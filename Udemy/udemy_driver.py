import os

from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
url = 'https://www.udemy.com/courses'
file_dir = os.path.dirname(__file__)



class Driver(object):
    def __init__(self):
        self.driver = Chrome()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
            self.driver.quit()

    def open(self, url):
        self.driver.get(url)

    def hover(self, element_to_hover):
        hover = ActionChains(self.driver).move_to_element(element_to_hover)
        hover.perform()
    @staticmethod
    def add_to_aleady_added(name, url):
        with open(os.path.join(file_dir, 'already_added.txt'), 'a') as already_added:
            already_added.write('\nname: {} url: {}'.format(name, url))


    def udemy_login(self, email, password):

        self.open(url)
        login_btn = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_css_selector('require-auth[data-purpose="login"]'))
        login_btn.click()

        email_box = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_css_selector('#id_email'))
        email_box.send_keys(email)

        pass_box = self.driver.find_element_by_css_selector('#id_password')
        pass_box.send_keys(password)

        self.driver.find_element_by_xpath('//*[@id="submit-id-submit"]').click()
        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_css_selector('img[data-purpose="dropdown-user-avatar"]'))
        print '\nLogged correctly\n'

    def add_course(self, course_url, name):
        self.open(course_url)
        try:
            element = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_css_selector('a[data-purpose="buy-this-course-button"]'))
            element.click()
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_css_selector('button[data-purpose="go-to-course"]'))
            print '*** {} successfully added ***\n'.format(name)
            self.add_to_aleady_added(name, course_url)
        except TimeoutException:
            try:
                WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_css_selector('h3[id="recent-activity"]'))
                print 'Course already added'
            except:
                print 'Btn not found'



