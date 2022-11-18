import pickle

import numpy as np
from flask import Flask, render_template, request

from attributes_of_url import Attributes

app = Flask(__name__)

rfc = pickle.load(open('model.pkl', 'rb'))


@app.route('/', methods=['GET', 'POST'])
def url_predict():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        url = request.form.get("url")
        obj = Attributes(url)

        x = np.array(obj.getFeaturesList()).reshape(1,13)
        print(x)

        y_pred = rfc.predict(x)[0]
        print(y_pred)

        if y_pred < 0:
            msg = "Don't worry, It seems it is a genuine website, Go ahead"
            val= 1
        else:
            msg = "Hold on there, it seems the website is an phishing website"
            val = "no"

        return render_template('result.html', msg=msg, url=url, val=val)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
