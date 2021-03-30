from flask import Flask, request
import parking
import loop
from multiprocessing import Process
from sms_info import text_numbers, from_num
from pymongo import MongoClient
app = Flask(__name__)

mongoClient = MongoClient()

# NOTE: THIS WILL NOT RUN. Passwords and tokens for twilio authorization are stored and read from local files only
# Flask server starts listeing on port 5000
# a local tunneler will bring any post requests from
# twilio API's to this running process

@app.route('/sms', methods=['POST'])  # when the server recieves a POST request from /sms url
def sms():
    # load subscriber phone numbers from MongoDB
    people = list(map(lambda o : o['phonenumber'], list(mongoClient.ParkingNotifier.subscribers.find({}))))
    print("Current list of numbers registered:\n",people,"\n")
    number = request.form['From']       # set variable 'number' to the number currently texting
    message_body = request.form['Body']  # set the variable ' message_body to the content of the text message

    print("From:", number, "   Message: ", message_body)  # debug use; used to see incoming texts in cmd window

    match = False # set initial match variable to false
    match_index = 0

    for index, numbers in enumerate(people):  # loop through the numbers list
        numbers = numbers.strip()  # removes any special characters such as \n from array of numbers
        if numbers == number:  # if number is found
            match = True
            match_index = index
            break
    if not match:
        if message_body.lower() != "yes":
            text_numbers(number, from_num, "Reply with 'Yes' (no quotes) to recieve automatic winter parking ban updates. 'No' Will unsubscribe. 'Status' for current ban status (Created by AndrewL)")
        if message_body.lower() == "yes":
            text_numbers(number, from_num, "Subscribed! You will be notified when parking on the street is banned in Ottawa. reply with 'NO' to unsub")
            text_numbers(number, from_num, "Current status: " + parking.get_page_data())
            people.append('\n'+number)
            mongoClient.ParkingNotifier.subscribers.insert_one({'phonenumber': number})
            print(str(number) + " appended to index " + str(len(people)))
    if match:
        if message_body.lower() == 'no':
            text_numbers(number, from_num, "Successfully unsubscribed")
            mongoClient.ParkingNotifier.subscribers.delete_one({'phonenumber': people[match_index]})
            people.pop(match_index)
        if message_body.lower() == 'status':
            text_numbers(number, from_num, "Current status: " + parking.get_page_data())
        elif message_body.lower() != 'no':
            text_numbers(number, from_num, "You are already subscribed for updates for Ottawa parking. reply 'No' to unsubscribe, or 'statuts' for current parking status")
            print("Already subscribed at", match_index, " index")

    return 'All good'


def run_app():
    app.run()


if __name__ == '__main__':
    p1 = Process(target=run_app)
    p1.start()
    p2 = Process(target=loop.parking_loop)
    p2.start()
