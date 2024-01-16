import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense

# Read CSV
data = pd.read_csv('utils/datata.csv')

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
model = Sequential() #create ANN layer
model.add(Dense(128, input_dim=X_train.shape[1], activation='relu')) #input layer e.g:symptoms
model.add(Dense(64, activation='relu')) #dummy layer
model.add(Dense(len(le.classes_), activation='softmax'))  # Output layer with softmax for multiclass classification

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training the model
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))


def user_symptoms_utils(a, b, c, d, e):
    # Existing symptoms list from the dataset
    existing_symptoms = list(symptoms_encoded.columns)

    # Initialize input with zeros for all symptoms
    user_input = pd.DataFrame([[0] * len(existing_symptoms)], columns=existing_symptoms)

    if a is not '':
        user_input['Symptom_1_ ' + a] = 1
    if b is not '':
        user_input['Symptom_2_ ' + b] = 1
    if c is not '':
        user_input['Symptom_3_ ' + c] = 1
    if d is not '':
        user_input['Symptom_4_ ' + d] = 1
    if e is not '':
        user_input['Symptom_5_ ' + e] = 1

    # Disease prediction based on symptoms
    predicted = model.predict(user_input)
    predicted_disease = le.inverse_transform([predicted.argmax()])[0]

    return predicted_disease


