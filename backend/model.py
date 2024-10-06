import re 
import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score, classification_report 
import joblib

data = pd.read_csv('./predicted_data2.csv') # load the dataset

print(data.columns)

##### FEATURE ENGINEERING ######

# count slashes in the url
# no of slashes in the url indicates potential vulnerability
def count_slashes(path):
    return path.count('/')

# check for suspcisous file extensions like a sh file
def has_suspicious_extension(path):
    return int(bool(re.search(r'\.php|\.jsp|\.exe|\.sh', path)))

# counts no of parameters, no of params indicates exploit
def count_parameters(body):
    return len(body.split('&')) if pd.notnull(body) else 0

# Create 3 more columns 
data['url_depth'] = data['path'].apply(count_slashes)
data['suspicious_extension'] = data['path'].apply(has_suspicious_extension)
data['param_count'] = data['body'].apply(count_parameters)

# include data in feature set
new_features = ['path_length', 'body_length', 'badwords_count', 'url_depth', 'suspicious_extension', 'param_count']
X = data[new_features]
print(f'Model trained on features: {new_features}')
y = data['class']

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

joblib.dump(clf, 'suspicious_model.pkl')

# test data
y_pred = clf.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(f'Classification Report: \n{classification_report(y_test, y_pred)}')
