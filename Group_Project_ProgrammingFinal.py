#to extract information from a website (web scrapping)
import requests
from bs4 import BeautifulSoup
#enables to send emails
import smtplib
import html5lib
# os module has to be imported to interact with the operating system
import os
# boto3 module is necessary in order to use AWS
import boto3
# to raise exceptions while using boto3 (related to AWS or botocore)
from botocore.exceptions import ClientError

# in this dictionary, each article (key) is linked to a price limit (value) which expreses the max. willingness to pay of the user
dict = {'https://www.zalando.ch/deezee-buena-riemensandalette-black-d0x11a00n-q11.html':36, 'https://www.zalando.ch/nike-sportswear-air-force-1-sneaker-low-whitemetallic-silverblack-ni111a0zo-a11.html': 130, 'https://www.zalando.ch/tamaris-brautschuh-pearl-ta111b1fx-j11.html':71}

# here, we define the class attributes of the HTML page that refers to the brand, title, price of the article
class_brand = "OEhtt9 ka2E9k uMhVZi Kq1JPK pVrzNP _5Yd-hZ"
class_title = "EKabf7 R_QwOV"
class_price = "uqkIZw ka2E9k uMhVZi FxZV-M _6yVObe pVrzNP"

#gets information about your browser (on google look for "my user agent")
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2Safari/605.1.15'}

# send_mail function: use of AWS "Simple Email Service" to send automatic emails to recipient
# raise a ClientError if there are any AWS service errors (i.e. if the email adressess were not verified in SES)
def send_mail(url):
    SENDER = "Nina Ollagnon <nina.ollagnon@hotmail.com>"
    RECIPIENT = "trackingprices7@gmail.com "
    AWS_REGION = "eu-central-1"
    SUBJECT = "Zalando - Price Alert"
    BODY_TEXT = ("Hey, congratulations! The price went down for one of the articles you selected: " + url)
    CHARSET = "UTF-8"

#create a SES resource and specificy the region of the sender (using AWS)
    client = boto3.client('ses',region_name=AWS_REGION)

    try:
#        description of the content of the email
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
#     to get more info on the ClientError, we printed the error response dict 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# update_price function: use of HTTP "get" method to get HTML content via the urls
# create an instance of the Beautifilsoup class to parse the HTLM with the parser 'html5lib'
def update_price(url):
    page = requests.get(url, headers=headers)     
    soup = BeautifulSoup(page.content, 'html5lib')

# find() method for returning the exact string values of the class (class_) attributes (previously defined)
    brand = soup.find(class_=class_brand).get_text()
    title = soup.find(class_=class_title).get_text()
    price = soup.find(class_=class_price).get_text()

    converted_price = float(price[4:])

    return converted_price, brand, title

# function to extract the rating of the product from the HTML
def get_rating(url):
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html5lib')

# find() method for returning the string values (specific rating of the article) of the class attribute, inside the tag 'span'
    rating = soup.find('span', attrs={'class':'AKpsL5 ka2E9k uMhVZi Kq1JPK pVrzNP'}).get_text()
    print(rating)

    return rating

# iteration through the keys of the dictionary to call the update_price() function for each article
# and get the price, brand, and title (name of the product) from the HTML
for i in dict.keys():
    converted_price, brand, title = update_price(i)

    print("Brand: " + str(brand))
    print("Title: " + str(title))
    print("Price: " + str(converted_price))

# call the send_mail() function if the price of the article is below the max. wtp of the user
    if converted_price < dict[i]:
        send_mail(i)
# call the get_rating() function for the nike article as in the function, the class is specific to that article
nike_rating = get_rating('https://www.zalando.ch/nike-sportswear-air-force-1-sneaker-low-whitemetallic-silverblack-ni111a0zo-a11.html')
print("Nike shoes rating: " + str(nike_rating))