import pytest
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Sample functions from the project
def clean_data(df):
    # Example cleaning function
    df = df.drop(columns=['case_enquiry_id'], errors='ignore')
    return df

def build_model(input_shape, num_classes):
    model = Sequential()
    model.add(Dense(128, input_shape=(input_shape,), activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(model, X_train, y_train, epochs=1):
    history = model.fit(X_train, y_train, epochs=epochs, verbose=0)
    return history

# Test cases
def test_clean_data():
    raw_data = pd.DataFrame({'case_enquiry_id': [1, 2], 'subject': ['Pothole', 'Trash']})
    cleaned_data = clean_data(raw_data)
    assert 'case_enquiry_id' not in cleaned_data.columns
    assert 'subject' in cleaned_data.columns

def test_model_build():
    input_shape = 10
    num_classes = 5
    model = build_model(input_shape, num_classes)
    assert model.output_shape[-1] == num_classes

def test_model_training():
    input_shape = 10
    num_classes = 3
    model = build_model(input_shape, num_classes)
    X_train = np.random.random((100, input_shape))
    y_train = np.random.randint(0, num_classes, size=(100,))
    y_train = np.eye(num_classes)[y_train]  # Convert to one-hot encoding
    history = train_model(model, X_train, y_train, epochs=1)
    assert 'accuracy' in history.history
