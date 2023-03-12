from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pandas as pd
from mongoDB_url import mongoDB_url
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


client = MongoClient(mongoDB_url())
db = client["mydatabase"]
collection = db["practice"]

class ExtractData(Resource):
    def post(self):
        # Load spreadsheet data
        spreadsheet_file = pd.ExcelFile("C:\\Users\\DELL\\Downloads\\practice.xlsx")
        worksheet = spreadsheet_file.sheet_names
        append_data = []

        # Iterate over each sheet in the spreadsheet
        for sheet_data_name in worksheet:
            details = "PU"

            df = pd.read_excel(spreadsheet_file, sheet_data_name, header=0)
            df = df[["phone", "delimit", details]]
             

            # Convert DataFrame to list of dictionaries
            data = df.to_dict("records")

            # Insert data into MongoDB Atlas collection
            collection.insert_many(data)

        return jsonify({"message": "Data uploaded successfully."})

    


api.add_resource(ExtractData, '/api/v1/data')


class CheckPhoneNumber(Resource):
    def get(self, phone_number):
        result = collection.find_one({"phone": phone_number})

        if result:
            return {"status":True, "message":f"{phone_number} is a verified agent", "data":{"phone": result["phone"], "PU": result["PU"],"delimit": result["delimit"]}}
            
        else:
            return {"status":False, "message":f"{phone_number} is not a verified agent"}


api.add_resource(CheckPhoneNumber, '/api/v1/phone/<int:phone_number>')


if __name__ == '__main__':
    app.run(debug=True)