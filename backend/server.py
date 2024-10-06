from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load('./suspicious_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    df = pd.DataFrame([data])

    new_features = ['path_length', 'body_length', 'badwords_count', 'url_depth', 'suspicious_extension', 'param_count']

    if not all(key in df.columns for key in new_features):
        return jsonify({'error': 'Invalid input data. Required fields are missing.'}), 400

    X = df[new_features]

    prediction = model.predict(X)

    result = 'suspicious' if prediction[0] == 1 else 'good'

    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
