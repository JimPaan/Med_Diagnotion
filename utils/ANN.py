import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense

# Read CSV
data = pd.read_csv('datata.csv')

# Extract features (symptoms) and target variable (disease)
symptoms = data.drop('Disease', axis=1)
diseases = data['Disease']

# Encode categorical variables
le = LabelEncoder()
diseases_encoded = le.fit_transform(diseases)
symptoms_encoded = pd.get_dummies(symptoms)  # Convert symptoms to binary encoding

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(symptoms_encoded, diseases_encoded, test_size=0.2, random_state=42)

# Building the ANN
model = Sequential()
model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(le.classes_), activation='softmax'))  # Output layer with softmax for multiclass classification

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training the model
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))


# Existing symptoms list from the dataset
existing_symptoms = list(symptoms_encoded.columns)

# Initialize input with zeros for all symptoms
user_input = pd.DataFrame([[0] * len(existing_symptoms)], columns=existing_symptoms)

# User's symptoms
x = 'muscle_wasting'
y = 'patches_in_throat'
z = 'dark_urine'
a = 'chest_pain'
b = ''

if x is not '':
    user_input['Symptom_1_ ' + x] = 1
if y is not '':
    user_input['Symptom_2_ ' + y] = 1
if z is not '':
    user_input['Symptom_3_ ' + z] = 1
if a is not '':
    user_input['Symptom_4_ ' + a] = 1
if b is not '':
    user_input['Symptom_5_ ' + b] = 1

# Disease prediction based on symptoms
predicted = model.predict(user_input)
predicted_disease = le.inverse_transform([predicted.argmax()])[0]
print("Predicted Disease: ", predicted_disease)
