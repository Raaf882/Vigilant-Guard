from flask import request, jsonify, render_template
from app import app, model, scalar, extract_features, check_malware
import pandas as pd


malware_hashes = pd.read_csv('malware_hashes.csv')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get the file from the request
#     file = request.files.get('file')
#     try:
        
#         # Extract features from the file
#         file_features = extract_features(file)
#         # Feature scaling
#         features_transformed = scalar.transform(file_features)
#         # Make a prediction using the loaded model
#         prediction = model.predict(features_transformed)

#         print('prediction', prediction)
#         return jsonify({'prediction': prediction.tolist()})
#     except:
#         return jsonify({'error': 'No file uploaded'}, 400)

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get the file from the request
#     file = request.files.get('file')
#     print(file)
#     try:
#         print(check_malware(file, malware_hashes))
        
#         is_malware, file_hash = check_malware(file, malware_hashes)
        
#         print(is_malware)
        
#         if is_malware:
#             return jsonify({'prediction': [0]})
        
#         else:
#             # Save the new hash to the CSV file
#             # malware_hashes.append(file_hash) 
#             malware_hashes = malware_hashes.append({'md5': file_hash})
            
#             print(malware_hashes.head())
#             # Continue with feature extraction and prediction
#             # Extract features from the file
#             file_features = extract_features(file)
#             print(file_features)
#             # Feature scaling
#             features_transformed = scalar.transform(file_features)
#             # Make a prediction using the loaded model
#             prediction = model.predict(features_transformed)
#             return jsonify({'prediction': prediction.tolist()})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# from flask import Flask, request, jsonify
# import hashlib
# import pandas as pd

# app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    
    # Get the file from the request
    file = request.files.get('file')
    
    if file:
        try:

            # Extract features from the file
            file_features = extract_features(file)

            # Assume malware_hashes is a pandas Series containing known malware hashes
            #malware_hashes = pd.read_csv('malware_hashes.csv').drop('Unnamed: 0', axis=1)
            malware_hashes = r'malware_hashes.csv'
    
            is_malware, file_hash = check_malware(file, malware_hashes)
            
            print(file_hash)
            print(is_malware)
            
            if is_malware:
                return jsonify({'prediction': [1]})
                
            else:

                # Feature scaling
                features_transformed = scalar.transform(file_features)
                
                # Make a prediction using the loaded model
                prediction = model.predict(features_transformed)
                
                print(prediction)

                return jsonify({'prediction': prediction.tolist()})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No file uploaded'}), 400



