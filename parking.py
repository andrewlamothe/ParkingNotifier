import requests
from bs4 import BeautifulSoup
from sms_info import text_numbers, from_num


def get_page_data():
    url = "https://ottawa.ca/en/parking-roads-and-travel/road-and-sidewalk-maintenance/winter-maintenance"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') # setting up an html parser object
    results = soup.find("div", class_='status-desc').text # selecting the parking text
    return results


def check_page_change():  # checks the website for a change
    results = get_page_data()
    prev = open('texts/parking.txt', 'r').readline()  # load previously saved parking information
    message = "Change in winter parking detected. Current status: " + results + ".  reply 'no' to unsub"
    if prev != results:  # if saved info is different from current info, send text message to list
        print("\nALERT!! Change in winter parking. Current status: " + results + "\n")
        send_parking_text(message)
    else:
        print("\n\nNo change in winter parking. Current status: " + results + "\n\n")
    open('parking.txt', 'w').write(results)  # Currently only stored in a text file. Database implementation shortly


def send_parking_text(message):
    subs = open('texts/subscribers.txt')  # This will be where the database accesses the list for phone numbers
    numbers = subs.readlines()
    subs.close()
    print(numbers)
    for each in numbers:  # if sending text fails (i.e. 0 balance in Twilio), this is so the whole app doesn't crash
        try:
            text_numbers(each.strip(), from_num, message)
        except:
            print("Failed")