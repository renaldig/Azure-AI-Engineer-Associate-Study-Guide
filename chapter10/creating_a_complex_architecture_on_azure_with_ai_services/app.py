from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")  # e.g., "https://your-openai-service.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided.'}), 400
    
    try:
        response = openai.Completion.create(
            engine="YOUR_DEPLOYMENT_NAME",  # Replace with your deployment name
            prompt=prompt,
            max_tokens=150
        )
        generated_text = response.choices[0].text.strip()
        return jsonify({'result': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
