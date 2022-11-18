import pickle
import requests
import numpy as np
from flask import Flask, render_template, request

from attributes_of_url import Attributes

app = Flask(__name__)

rfc = pickle.load(open('model.pkl', 'rb'))
API_KEY = ""
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY,"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


@app.route('/', methods=['GET', 'POST'])
def url_predict():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        url = request.form.get("url")
        obj = Attributes(url)

        x = np.array(obj.getFeaturesList()).reshape(1, 13)
        print(x)

        y_pred = rfc.predict(x)[0]
        print(y_pred)
        values = [obj.getFeaturesList()]
        payload_scoring = {"input_data": [{"fields": ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen'], "values": values}]}

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/997c5696-a1ef-4259-978c-4c1ef58bd44e/predictions?version=2022-11-18',
            json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        if y_pred < 0:
            msg = "Don't worry, It seems it is a genuine website, Go ahead"
            val = 1
        else:
            msg = "Hold on there, it seems the website is an phishing website"
            val = "no"

        return render_template('result.html', msg=msg, url=url, val=val)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
