import requests # responsible for getting web page conent
from bs4 import BeautifulSoup # parsing the html code
import pandas # to store in data in csv
import argparse # argument parser in command line
import connect

# CSV saving function
def saving_csv():
    dataframes = pandas.DataFrame(scraped_info_list) # converting the scraped data to pandas dataframes
    print("\n\tCreating csv file....")
    dataframes.to_csv('product.csv') # conver dataframe to csv file


parser = argparse.ArgumentParser() # object
parser.add_argument("--page_num_max", help="Enter the number of pages to parse", type=int) # no of pages to parse
parser.add_argument("--dbname", help="Enter the database name", type=str) # db name

args = parser.parse_args()

main_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page="

# number of pages
page_num_max = args.page_num_max
scraped_info_list = [] # scraped data

connect.connect(args.dbname) # create database

for page_num in range(1,page_num_max):
    url = main_url + str(page_num)
    print('\nGET request for: ' + url)
    req = requests.get(url) # get api request

    content = req.content # getting the content from url
    # print(content)

    soup = BeautifulSoup(content, "html.parser") # parsing the html

    # ("tag",{"attribute":"value"}) 
    all_products = soup.find_all("div",{"class":"thumbnail"}) # returns a list if all the elements which satsfy the given condition in parenthesis

    for product in all_products:
        product_dic = {} # empty  dictionary
        product_dic["name"] = product.find("a",{"class":"title"}).text # name
        product_dic["price"] = product.find("h4",{"class":"price"}).text # price
        product_dic["review"] = product.find("p",{"class":"pull-right"}).text # review

        pro_desc = product.find("p",{"class":"description"}).text # description
        
        pro_desc_list = pro_desc.split(',') # converting the description into list

        # product_dic["Description"] = ', '.join(pro_desc_list[:4]) # description
        product_dic["Screen-size"] = ''.join(pro_desc_list[0]) # description - Screen-size
        product_dic["Processor"] = ''.join(pro_desc_list[1]) # description - Processor
        product_dic["RAM"] = ''.join(pro_desc_list[2]) # description - RAM
        product_dic["ROM"] = ''.join(pro_desc_list[3]) # description - ROM

        scraped_info_list.append(product_dic) # list of products' dictionary
        connect.insert_into_table(args.dbname, tuple(product_dic.values()))

        # print(pro_name,pro_price,pro_desc_list[:4],pro_review) 




# saving_csv()

# printing the scraped data in terminal
connect.get_product_info(args.dbname)
