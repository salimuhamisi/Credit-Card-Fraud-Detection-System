import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.metrics import precision_score, recall_score, f1_score
import pickle

# load dataset to the project.
data = pd.read_csv("creditcard.csv")

# Top 5 rows of dataset.
print(data.head())

# shape of dataset
print(data.shape)

# information about our dataset
print(data.info())

# check null values
print(data.isnull().sum())

# check duplicates
print(data.duplicated().any())

# drop duplicates
data = data.drop_duplicates()

# check distribution of our target class
print(data["Class"].value_counts())

# store feature matrix in X and target variable in Y
x = data.drop("Class", axis=1)
y = data["Class"]

print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
# Deal with imbalanced data (by oversampling)
x_res, y_res = SMOTE().fit_resample(x,y)
print(y_res.value_counts())

print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
# split dataset into training and testing
x_train, x_test, y_train,y_test= train_test_split(x_res,y_res, test_size=0.20, random_state=42)

# train the model
log = LogisticRegression()
log.fit(x_res, y_res)

model = log.predict(x_test)

# check scores
print(accuracy_score(y_test, model))
print(precision_score(y_test, model))
print(recall_score(y_test, model))
print(f1_score(y_test, model))

# save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
