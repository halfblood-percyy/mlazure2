import pickle
import pypyodbc
import numpy as np
import pandas as pd
from flask import Flask
from flask import request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
model = pickle.load(open('SalaryPrediction.pkl','rb'))

# app = Flask(__name__, static_folder='/opt/defaultsite')
class Details(Resource):
    #@app.route('/api', methods=['POST'])
    def post(self):
        # Get the data from the POST request.
        data = request.get_json(force=True)  # Make prediction using model loaded from disk as per the data.
        ## Get the Input from DB to predict.
        ################################################################################
        server = 'heathrowserverpoc.database.windows.net'
        database = 'heathrowdbpoc'
        username = 'anjanwahwar'
        password = 'Anjan$1234'
        driver = '{ODBC Driver 17 for SQL Server}'
        cnxn = pypyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        dfdata = pd.read_sql("SELECT * FROM dbo.InputEmpData", cnxn)

        ############################################################################
        prediction = model.predict(dfdata[["Experiance"]])  # Take the first value of prediction
        cursor = cnxn.cursor()
        for i in range(len(prediction)):
            cursor.execute('''
                INSERT INTO dbo.OutputEmpData (Salary)
                VALUES
                (?)
                ''', int(prediction[i][0]))
            cnxn.commit()
        cursor.close()
        cnxn.close()

        return jsonify(['OK'])

api.add_resource(Details, '/test')  # Route_1
    #if __name__ == '__main__':
     #   app.run(port=5000, debug=True)

if __name__ == "__main__":
    app.run()
