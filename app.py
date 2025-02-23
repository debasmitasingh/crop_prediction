from flask import Flask, render_template, request,jsonify
import sqlite3
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact', methods = ['GET','POST'])
def contactus():
    if request.method == "POST":
        fname = request.form.get("name")
        pno = request.form.get("phone")
        email = request.form.get("email")
        add = request.form.get("address")
        msg = request.form.get("message")
        # print(fname,pno,email,add,msg)
        conn = sqlite3.connect("customerdatabase.db")
        cur = conn.cursor()
        cur.execute(f'''
                    INSERT INTO CONTACT VALUES("{fname}","{pno}",
                    "{email}","{add}","{msg}"
                    )
                    ''')
        conn.commit()
        return render_template("message.html")
    else:
        return render_template('contactus.html')
# Dictionary to map encoded values to crop names
@app.route('/cropanalysis')
def analysis():
    return render_template('cropanalysis.html')
crop_mapping = {
    0: 'Cotton',
    1: 'Ginger',
    2: 'Gram',
    3: 'Grapes',
    4: 'Groundnut',
    5: 'Jowar',
    6: 'Maize',
    7: 'Masoor',
    8: 'Moong',
    9: 'Rice',
    10: 'Soybean',
    11: 'Sugarcane',
    12: 'Tur',
    13: 'Turmeric',
    14: 'Urad',
    15: 'Wheat'
}

@app.route("/croppredictor", methods=['GET', 'POST'])
def cropprediction():
    if request.method == 'POST':
        nitrogen = request.form.get("Nitrogen")
        phos = request.form.get("Phosporus")
        pot = request.form.get("Potassium")
        ph = request.form.get("Ph")
        soil = request.form.get("soilColor")
        rain = request.form.get("Rainfall")
        temp = request.form.get("Temperature")

        # Load the model and make prediction
        with open("model.pickle", 'rb') as mod:
            model = pickle.load(mod)
        pred = model.predict([[float(nitrogen), float(phos), float(pot), float(ph), float(soil), float(rain), float(temp)]])
        
        # Map the encoded prediction to the crop name
        crop_name = crop_mapping.get(pred[0], "Unknown Crop")
        
        # Pass the crop name to the result template
        return render_template('result.html', pred=crop_name)
    else:
        return render_template("cropprediction.html")
# Create a dictionary to store the results
results = {
    "Logistic Regression": {
        "Training Accuracy": 0.7620,
        "Test Accuracy": 0.7719,
        "Training Loss": 0.6661,
        "Test Loss": 0.6685
    },
    "K-Nearest Neighbors": {
        "Training Accuracy": 0.9917,
        "Test Accuracy": 0.9546,
        "Training Loss": 0.0452,
        "Test Loss": 0.4048
    },
    "Random Forest": {
        "Training Accuracy": 1.0000,
        "Test Accuracy": 0.9967,
        "Training Loss": 0.0188,
        "Test Loss": 0.0506
    },
    "Gradient Boosting": {
        "Training Accuracy": 1.0000,
        "Test Accuracy": 0.9967,
        "Training Loss": 0.0165,
        "Test Loss": 0.0228
    },
    "XGBoost": {
        "Training Accuracy": 1.0000,
        "Test Accuracy": 0.9989,
        "Training Loss": 0.0060,
        "Test Loss": 0.0109
    },
    "Support Vector Machine": {
        "Training Accuracy": 0.9150,
        "Test Accuracy": 0.9147,
        "Training Loss": 0.2942,
        "Test Loss": 0.3243
    },
    "Naive Bayes": {
        "Training Accuracy": 0.7884,
        "Test Accuracy": 0.7841,
        "Training Loss": 0.6678,
        "Test Loss": 0.6601
    }
}
# You can now access the results dictionary for any model
print(results)
@app.route('/results')
def get_results():
    return jsonify(results)

@app.route('/output')
def output():
    return render_template('output.html')
if __name__ == '__main__':
    app.run()
    