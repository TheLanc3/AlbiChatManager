import json

from user_records import UserRecords

from os import listdir

def load_users():
    users_files = listdir("users_records")
    users = dict()
    if(len(users_files) > 0):
        for i in range(len(users_files)):
            with open("users_records/" + users_files[i]) as data:
                user = json.load(data)
                users[int(users_files[i].split('.json')[0])] = UserRecords(user["basketball"], user["football"], user["dart"], user["dice"], user["balling"])
    return users

        