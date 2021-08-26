from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.chrome.options import Options

# options = Options()
# options.binary_location = r'/Users/alisonkim12/Downloads/operadriver_mac64/operadriver' # change this to be where you downloaded
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
#get to the Property Records Webpage

driver.get('http://www.ustaxdata.com/nc/wilson/Search.cfm')
street_num_list = ["1110", "3311", "1664", "1007", "3701", "1800", "3815","2712", "1714", "1710","601"]
street_name_list = ["ELIZABETH","BOYETTE","LIPSCOMB","KENT","TARBORO","ASHBROOK","LONDON CHURCH","WARD","FOREST HILLS","LIPSCOMB", "DARTMORE", "BRIGGS"]
my_urls = []

for i in range(len(street_num_list)):
    #enter in the address within the search bar
    street_num = driver.find_element_by_xpath("/html/body/form/table[3]/tbody/tr/td/div/table/tbody/tr/td[1]/table[2]/tbody/tr/td/table[3]/tbody/tr[2]/td[1]/input")
    street_num.send_keys(street_num_list[i])
    street_name = driver.find_element_by_xpath("/html/body/form/table[3]/tbody/tr/td/div/table/tbody/tr/td[1]/table[2]/tbody/tr/td/table[3]/tbody/tr[2]/td[2]/input")
    street_name.send_keys(street_name_list[i])
    #click on search
    driver.find_element_by_xpath("/html/body/form/table[3]/tbody/tr/td/div/table/tbody/tr/td[1]/table[2]/tbody/tr/td/table[7]/tbody/tr/td/spacer/div/span/font/font/input").send_keys(Keys.ENTER)
    #click on the first option that pops up....this should be the url to the actual property records for that specific address

    first_option = driver.find_element_by_xpath("/html/body/form/table[3]/tbody/tr/td/table[2]/tbody/tr[2]/td[3]/div/p/a")
    first_option.send_keys(Keys.ENTER)
    my_url = driver.current_url
    my_urls.append(my_url)

print(my_urls)

data_dict = dict()
data_dict = {"Parcel ID": [], "Property Owner": [], "Owner's Mailing Address": [], "Market Value": [],
             "Assessed Value": [], "Sales Info: Grantor": [],
             "Sales Info: Sold Date": [], "Sales Info: Sold Amount": [],
             }

for i in range(len(my_urls)):
    driver.get(my_urls[i])

    # Parcel ID,
    xpath_parcelid = "/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[2]/div/font/strong"
    text = driver.find_elements_by_xpath(xpath_parcelid)[0].text
    print('Parcel ID', text)
    data_dict["Parcel ID"].append(text)

    # Property Owner,
    xpath_owner = "/html/body/form/table[2]/tbody/tr/td/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[1]/td/b/font"
    text = driver.find_elements_by_xpath(xpath_owner)[0].text
    print('Property Owner', text)
    data_dict["Property Owner"].append(text)

    # Owner's Mailing Address
    xpath_mailingaddress = "/html/body/form/table[2]/tbody/tr/td/table[2]/tbody/tr/td[2]/table[2]/tbody/tr[1]/td/b/font"
    text = driver.find_elements_by_xpath(xpath_mailingaddress)[0].text
    print("Owner's Mailing Address:", text)
    data_dict["Owner's Mailing Address"].append(text)

    # Market Value

    xpath_market = "/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[2]/td[2]"
    text = driver.find_elements_by_xpath(xpath_market)[0].text
    print('Market Value:', text)
    data_dict["Market Value"].append(text)

    # Assessed Value,

    xpath_assessed = '/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[6]/td[2]/div/font/b'
    text = driver.find_elements_by_xpath(xpath_assessed)[0].text
    print('Assessed Value:', text)
    data_dict["Assessed Value"].append(text)

    # Sales Info: Grantor,

    xpath_grantor = "/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[2]/table[2]/tbody/tr[10]/td[2]/div/font/strong"
    text = driver.find_elements_by_xpath(xpath_grantor)[0].text
    print('Sales info: grantor', text)
    data_dict["Sales Info: Grantor"].append(text)

    # Sales Info: Sold Date,
    xpath_sold_date = "/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[2]/table[2]/tbody/tr[12]/td[2]/div/font/font/strong"
    text = driver.find_elements_by_xpath(xpath_sold_date)[0].text
    print('Sales info: Sold date', text)
    data_dict["Sales Info: Sold Date"].append(text)

    # Sales Info: Sold Amount,
    xpath_sold_amount = "/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[2]/table[2]/tbody/tr[13]/td[2]/div/font/strong"
    text = driver.find_elements_by_xpath(xpath_sold_amount)[0].text
    print('Sales info: sold amount', text)
    data_dict["Sales Info: Sold Amount"].append(text)
    # Sales History: Date Sold,
    xpath_date_sold = "/html/body/form/table[2]/tbody/tr/td/table[4]/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody"
    text = driver.find_elements_by_xpath(xpath_date_sold)[0].text.split("\n")

    print('Sales history', text)
    columns = text[:6]
    number_of_sales = (len(text)/6)

    def chunker_list(seq, size):
        return (seq[i::size] for i in range(size))

    if number_of_sales > 0:
        data = list(chunker_list(text[6:], int(number_of_sales)))

    data = list(chunker_list(text[6:], 6))
    data_df = pd.DataFrame(data_dict)
    sales_df = pd.DataFrame(dict(zip(columns, data)))
    out_df =  pd.merge(data_df.assign(key=0), sales_df.assign(key=0), on='key').drop('key', axis=1)
    print(out_df)
