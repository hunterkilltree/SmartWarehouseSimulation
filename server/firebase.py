import firebase_admin

print(firebase_admin)
from firebase_admin import credentials
from firebase_admin import db


class Firebase:
    def __init__(self):
        self.cred = credentials.Certificate('./server/sdk2.json')
        self.default_app = firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://testfirebase2-102ac-default-rtdb.firebaseio.com/'
        })
        self.ref_node = db.reference('map')
        self.current_upload_node = ""
        self.previous_upload_node = ""

    def update_item_data(self, item_name):
        # get current data
        # + 1
        # update new data
        pass

    def update_node_data(self, current_node):
        if current_node != "" and self.current_upload_node != current_node:
            self.previous_upload_node = self.current_upload_node
            self.current_upload_node = current_node
            self.ref_node.update({current_node: 1})
            if self.previous_upload_node != "":
                print("wrong here")
                print(self.previous_upload_node)
                self.ref_node.update({self.previous_upload_node: 0})



        # current_node set 1
        # previous_node set 0
        pass

# ref = db.reference('map')
# print(ref.get())
