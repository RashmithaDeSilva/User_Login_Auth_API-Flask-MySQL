from keras.models import load_model
import numpy as np


# Load Chatbot Modal
model = load_model('./model/chatbot.h5')

# User input predicter
def predict_output(user_input):
    # Preprocess the user input
    # processed_input = preprocess_input(user_input)

    # Make predictions
    predictions = model.predict(np.array([user_input]))

    # Assuming model returns a single output value
    print(predictions)
    return predictions[0]
