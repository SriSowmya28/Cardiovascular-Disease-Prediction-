from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open("heart.pkl", 'rb'))

@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/home1', methods=['GET', 'POST'])
def home1():
    if request.method == 'POST':
        # Process the form data from page2.html
        Name = request.form.get('Name', '')
        age = request.form.get('age', '')

        # Redirect to personal_details with Name and age as query parameters
        return redirect(url_for('personal_details'))
    
    return render_template('page2.html')

@app.route('/personal_details', methods=['GET', 'POST'])
def personal_details():
    if request.method == 'POST':
        # Redirect to heart_disease_form with Name and age as query parameters
        return redirect(url_for('heart_disease_form', Name=request.args.get('Name'), age=request.args.get('age')))
    
    # Render page3.html with Name and age passed from home1
    return render_template('page3.html', Name=request.args.get('Name'), age=request.args.get('age'))

@app.route('/heart_disease_form', methods=['GET', 'POST'])
def heart_disease_form():
    if request.method == 'POST':
        try:
            # Extract and validate form data
            data = {}
            fields = [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ]
            
            for field in fields:
                if field not in request.form:
                    return f"Missing value for {field}", 400
                try:
                    data[field] = float(request.form[field])
                except ValueError:
                    return f"Invalid value for {field}", 400

            # Convert sex to binary value
            sex = 1 if request.form['sex'] == 'male' else 0
            data['sex'] = sex

            # Make prediction using the model
            features = np.array([list(data.values())])
            model_prediction = model.predict(features)

            result = "Health Alert: Risk Factors for Heart Disease Detected 😟" if model_prediction[0] == 1 else "You have a Healthy Heart!😄"

            # Render result2.html with prediction, Name, and age
            return render_template('result2.html', Name=request.form.get('Name'), age=request.form.get('age'), prediction=result)
        
        except KeyError as e:
            return f"KeyError: {e} is missing from the form data", 400
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    # Render page3.html with Name and age passed from personal_details
    return render_template('page3.html', Name=request.args.get('Name'), age=request.args.get('age'))

if __name__ == '__main__':
    app.run(debug=True)
