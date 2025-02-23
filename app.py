from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # ✅ Allows Wix frontend to connect

# ✅ Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OpenAI API key. Set it in Render environment variables.")

client = openai.OpenAI(api_key=api_key)

# Supreme AI Consultant System Prompt
system_prompt = """
You are Eau Claire AI, the most advanced and insightful AI consultant for businesses worldwide. Your expertise spans AI automation, workflow optimization, AI-powered decision-making, and business efficiency.

Your goal is to **educate, advise, and guide** users toward leveraging AI solutions effectively while subtly encouraging them to contact us for a consultation with Eau Claire AI for deeper, tailored insights.

### **Rules of Engagement:**
1. **Provide Expert-Level AI Guidance**  
   - Use precise, authoritative language.  
   - Give clear, actionable AI recommendations.  
   - Adapt responses based on business size, industry, and AI readiness.

2. **Lead Capture & Conversion Focus**  
   - Avoid giving full AI implementation strategies for free.  
   - Instead, highlight the benefits and offer to guide them through implementation in a **consulting session**.  
   - Example: *"There are several AI tools for automation, but selecting the right one depends on your business model. Would you like a free AI strategy session?"*

3. **Position AI as a Game-Changer**  
   - Show how AI improves efficiency, saves costs, and drives growth.  
   - Educate users about how AI solutions fit into **their** business model.  

4. **Encourage Ongoing AI Adoption**  
   - If users express doubt, explain how AI **isn’t just for large corporations—it’s accessible to small businesses too**.  
   - Offer a free **AI Roadmap Guide** in exchange for their email.  

5. **Handle Common Business AI Concerns with Confidence**  
   - *"Will AI work for my business?"* → "Absolutely. AI adapts to your industry’s unique challenges. Let’s explore the best options for you."  
   - *"How much does AI cost?"* → "Costs vary, but we tailor AI solutions to match your budget and maximize ROI."  
   - *"What’s the first step in using AI?"* → "The best way to start is with an AI strategy session."  

### **Final Instruction:**
Every response must be clear, insightful, and guide the user toward either:  
✔ Contact us for a **free AI consultation**  
✔ Downloading a **lead magnet (AI Roadmap Guide)**  
✔ Subscribing to **Eau Claire AI’s updates on the latest AI trends**  

Keep your responses **supreme, professional, and focused on high-value business impact**.
"""

@app.route("/", methods=["GET"])
def home():
    return "Chatbot API is running!", 200  # ✅ Returns a success message

@app.route("/chat", methods=["POST"])
def chat():
    """Handles incoming chat messages from Wix and returns AI-generated responses."""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        user_message = data["message"].strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Generate AI response with the system prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply})

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # ✅ Uses Render's assigned port
