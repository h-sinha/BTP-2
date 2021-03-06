import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
lat_min, lat_max, lng_min, lng_max = -1, -1, -1, -1

# gets city bounding box
def get_bounding_box(city):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
        city + ",India&key=AIzaSyDUjKlnObDJwUO6f2ueMvzc3UyF_Jepd5U"
    resp = requests.get(url=url)
    data = resp.json()
    global lat_min, lat_max, lng_max, lng_min
    north_east = data['results'][0]['geometry']['bounds']['northeast']
    south_west = data['results'][0]['geometry']['bounds']['southwest']
    lat_min = south_west['lat'] - 1
    lat_max = north_east['lat'] + 1
    lng_min = south_west['lng'] - 1
    lng_max = north_east['lng'] + 1
    print(lat_min+1, lat_max-1, lng_min+1, lng_max-1)
    return 1
    # except:
    # return 0
get_bounding_box("Hyderabad")

# Downloads data from bhuvan
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(
    "/usr/lib/chromium-browser/chromedriver", options=options)
# opens bhuvan data download homepage
driver.get('https://bhuvan-app3.nrsc.gov.in/data/download/index.php')

# loads bhuvan credentials
with open('credentials.txt', 'r') as myfile:
    cred = myfile.read().split('\n')
    username = cred[0]
    password = cred[1]

# login on bhuvan website
def login(username, password):
    login_button = driver.find_element_by_link_text('Login')
    login_button.click()
    sleep(5)
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])
    # enter username
    username_box = driver.find_element_by_id('username')
    username_box.send_keys(username)
    # enter password
    password_box = driver.find_element_by_id('password')
    password_box.send_keys(password)
    submit_button = driver.find_element_by_name('submit')
    submit_button.click()
    sleep(5)
    driver.switch_to.default_content
    # driver.switch_to_default_content()
    sleep(2)

login(username, password)

# downloads data after login
def download(lat_min, lng_min, lat_max, lng_max):
	# checks if the lat, lng lie inside india(based on bounds given on bhuvan)
    assert lat_min >= 6 and lat_min <= 40, "latitude should be between 6 and 40 degree"
    assert lat_max >= 6 and lat_max <= 40, "latitude should be between 6 and 40 degree"
    assert lng_min >= 66 and lng_min <= 102, "longiitude should be between 66 and 102 degree"
    assert lng_max >= 66 and lng_max <= 102, "longiitude should be between 66 and 102 degree"
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("startPageFrame"))
    category = driver.find_element_by_id('Prj')
    category.click()
    project = Select(driver.find_element_by_id('subcategory'))
    project.select_by_value('C3')
    product = Select(driver.find_element_by_id('prdcts'))
    product.select_by_value('cdv3r1|MAP')
    min_lon = driver.find_element_by_id('bottom')
    min_lat = driver.find_element_by_id('left')
    max_lon = driver.find_element_by_id('right')
    max_lat = driver.find_element_by_id('top')
    # enters bounding box for data download on bhuvan
    min_lon.send_keys(str(lng_min))
    max_lon.send_keys(str(lng_max))
    min_lat.send_keys(str(lat_min))
    max_lat.send_keys(str(lat_max))
    sleep(2)
    select_button = driver.find_element_by_name('select_button')
    select_button.click()
    sleep(2)
    next_button = driver.find_element_by_xpath("//img[@alt='Next']")
    next_button.click()
    sleep(2)
    # clicks on download button to start download
    download_button = driver.find_element_by_xpath(
        "//img[@title='Click to download tile']")
    download_button.click()
    sleep(20)
download(lat_min, lng_min, lat_max, lng_max)