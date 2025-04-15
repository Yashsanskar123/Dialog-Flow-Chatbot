from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# API Key for Exchangerate API
API_KEY = 'abda6777ff9e67f23014859e7e428550'

@app.route('/', methods=['GET'])
def home():
    return "Currency Converter Bot is Running!"

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    try:
        # Extracting user data
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        # Fetch conversion factor by passing the amount
        conversion_rate = fetch_conversion_factor(source_currency, target_currency, amount)

        if conversion_rate is None:
            raise ValueError("Conversion rate not available")

        # Calculate final amount
        final_amount = round(amount * conversion_rate, 2)

        # Print to terminal (like your friend's code)
        print("Source Currency:", source_currency)
        print("Target Currency:", target_currency)
        print("Amount:", amount)
        print("Converted Amount:", final_amount)

        # Build Dialogflow response
        response_text = f"{amount} {source_currency} is {final_amount} {target_currency}"

    except Exception as e:
        print("Error:", str(e))
        response_text = "Sorry, I couldn't process your request. Please check the currencies and try again."

    return jsonify({
        'fulfillmentText': response_text
    })


def fetch_conversion_factor(source, target, amount):
    try:
        # Adding the 'amount' parameter in the API request
        url = f"https://api.exchangerate.host/convert?from={source}&to={target}&amount={amount}&access_key={API_KEY}"
        print(f"🌐 Requesting rate: {url}")
        response = requests.get(url)
        data = response.json()

        print(f"📊 API Response: {data}")  # Print the full response

        if "result" in data and data["result"] is not None:
            return data["result"]
        else:
            return None
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return None


if __name__ == "__main__":
    app.run(debug=True)
