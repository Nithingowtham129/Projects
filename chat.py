"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os,re
import google.generativeai as genai

genai.configure(api_key="GEMINI_API_KEY")

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="you are selling a headsets. you are a salesperson negotiating the price with the customer. you have to offer a initial price to customer and negotiate with them until you sell for a profitable price.",
)

from textblob import TextBlob

history = []

# Define pricing logic
min_price = 120 # minimum price at which to make resonable profit.
max_price = 150 # maximum price at which the product can be sold.

def sentiment(user_input):
    val = TextBlob(user_input).sentiment.polarity
    threshold = 0.2
    if val > threshold:
        return "happy"
    elif val < threshold:
        return "angry"
    else:
        return "neutral"

def calculate_offer(user_price):
    if min_price <= user_price <= max_price:
        return "accept"
    elif user_price < min_price:
        return "counter"
    else:
        return "reject"

# print(f"Bot : The maximum retail price of the product is {max_price} inclusive of GST and other Charges")
while True:
    # Prompt user input
    user_input = input("User: ")

    # Check user sentiment
    mood = sentiment(user_input)

    # Exit condition
    if user_input.lower() == 'exit':
        print("Exiting the chat...")
        break

    # Start the chat session
    chat_session = model.start_chat(
        history = history
    )

    # Try to extract the price offered by the user from the input
    user_price = None
    match = re.search(r'\$\s*(\d+)', user_input)
    if match:
        user_price = int(match.group(1))
        # Incorporate business logic for negotiation
        outcome = calculate_offer(user_price)

        if outcome == "accept":
            bot_reply = f"I accept your offer of ${user_price}."
        elif outcome == "counter":
            if mood == "happy":
                counter_price = ((min_price + max_price) // 2) - 5 
                bot_reply = f"since you are happy, how about ${counter_price}?"
            elif mood == "angry":
                counter_price = ((min_price + max_price) // 2) + 10
                bot_reply = f"No we can't how about ${counter_price}?"
            else:
                counter_price = ((min_price + max_price) // 2)
                bot_reply = f"how about ${counter_price}?"
        else:
            bot_reply = f"I'm sorry, ${user_price} is too high for me. The highest I can offer is ${max_price} Rest you can give it as Tips."

        # Send the bot's reply
        response = chat_session.send_message(bot_reply)

        # Print the bot's reply
        print(f"Bot: {response.text}")

        # conversation history
        # history.append({"user": user_input, "bot": bot_reply})
    else:
        bot_reply = f"Please provide a valid price in your offer (e.g., 'I would like to offer $130')."
        response = chat_session.send_message(bot_reply)
        print (f"Bot: {response.text}")