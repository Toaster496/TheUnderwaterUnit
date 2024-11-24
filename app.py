from flask import Flask, request, jsonify, send_from_directory
from g4f.client import Client
import os
from flask_cors import CORS  # For handling CORS issues
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins to access the API
# Initialize the Flask app


# Initialize G4F Client
client = Client()

# Serve the home page (index.html)
@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'index.html')

# Serve static files (CSS, JS, Images)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route('/chat', methods=['POST'])
def chat():
    # Handle the conversation
    try:
        data = request.json  # Parse incoming JSON data
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"reply": "Message cannot be empty."}), 400

        # Create an empty messages list for each session
        messages = [{"role": "user", "content": user_message}]

        # Get GPT's response
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            provider="Airforce"
        )

        # Extract and return the GPT response
        gpt_response = response.choices[0].message.content
        return jsonify({"reply": gpt_response})

    except Exception as e:
        # Handle errors
        return jsonify({"reply": f"Error generating response: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)