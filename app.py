import streamlit as st
import base64
import time
from openai import OpenAI
from openai._exceptions import RateLimitError
from main import process_input, get_assistant_reply

## Used Chat GPT to build a website using Streamlit module, the functions here are more

# === CONFIG ===
st.set_page_config(page_title="🛋️ Virtual Retail Assistant", page_icon="🛋️", layout="wide")
instructions = """You are a friendly, knowledgeable, and insightful Virtual Retail Assistant specializing in helping customers choose outdoor sitting sets.

Your goal is to guide the customer through a natural, helpful, and well-reasoned consultation process that ensures they find the product that best fits their needs first, and budget second.

The customer may provide a picture of a product they found in a store. You can analyze it to identify materials, design, seating capacity, and other visible features.

You must follow these guidelines:

1. Ask clarifying questions before giving recommendations.
   - Examples: space size, weather conditions, usage frequency, number of people, preferred style, and color palette.
   - Never rush to conclusions — always collect enough context first.

2. - Search for similar or alternative options online (mocking or simulating results is acceptable).
   - Provide 2–3 options online, with short descriptions (materials, design, durability, price range).

3. Provide a structured comparison:
   - Highlight key features, pros/cons, and price differences.
   - Use clear and readable formatting (for example, bullet points or mini tables).

4. Emphasize important considerations such as:
   - Material type and weather resistance
   - Durability and maintenance needs
   - Warranty, comfort, and long-term value

5. Conclude with a thoughtful recommendation:
   - State whether the original set is worth buying or if an alternative is better.
   - Justify your advice clearly, based on the customer’s needs and environmental conditions.

Your conversation style should reflect the following:
- Naturalness and clarity: Maintain a conversational, human-like flow.
- Depth of reasoning: Provide meaningful, well-grounded advice.
- Guidance through questioning: Help the customer reflect on what truly matters for their situation.
- Quality recommendations: Prioritize fit and practicality before cost.
- Creativity and completeness: Deliver a full, satisfying consultation experience — as if you were a real in-store design expert.

Avoid overly generic responses. Each answer should show understanding, reasoning, and engagement.
"""


# === SESSION STATE ===
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": [{"type": "input_text", "text": instructions}]}]
if "history" not in st.session_state:
    st.session_state.history = []

# === SIDEBAR ===
st.sidebar.header("🗂️ Chat History")
if st.sidebar.button("🆕 Start New Conversation"):
    st.session_state.history.append(st.session_state.conversation)
    st.session_state.conversation = [{"role": "system", "content": [{"type": "input_text", "text": instructions}]}]

if st.session_state.history:
    for i, conv in enumerate(st.session_state.history[::-1]):
        st.sidebar.markdown(f"💬 Conversation #{len(st.session_state.history) - i}")

st.sidebar.markdown("---")
st.sidebar.info("Virtual Assistant for outdoor furniture selection 🛋️")

# === MAIN UI ===
st.markdown("<h2 style='text-align:center;color:black;'>🛋️ Virtual Retail Assistant</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Professional consultation for outdoor sitting sets.</p>",
            unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

chat_container = st.container()

# === DISPLAY CONVERSATION ===
with chat_container:
    for msg in st.session_state.conversation[1:]:  # דילוג על system
        role = msg["role"]
        if role == "user":
            for c in msg["content"]:
                if c["type"] == "input_text":
                    st.markdown(
                        f"<div style='background-color:#E1ECF4;color:black;padding:10px;border-radius:10px;margin:5px 0'><b>You:</b> {c['text']}</div>",
                        unsafe_allow_html=True)
                elif c["type"] == "input_image":
                    st.image(c["image_url"], caption="Uploaded Image", use_column_width=True)
        elif role == "assistant":
            for c in msg["content"]:
                if c["type"] == "output_text":
                    st.markdown(
                        f"<div style='background-color:#F7F7F7;color:black;padding:10px;border-radius:10px;margin:5px 0'><b>Assistant:</b> {c['text']}</div>",
                        unsafe_allow_html=True)

# === USER INPUT SECTION ===
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("💬 Your Message")

col1, col2 = st.columns([4, 1])
with col1:
    user_text = st.text_area("Type your message:", value="", height=100, key="user_input")
    uploaded_file = st.file_uploader("Upload an image (optional):", type=["png", "jpg", "jpeg"])
with col2:
    st.write("")
    st.write("")
    send_button = st.button("🚀 Send", use_container_width=True)

# === PROCESS INPUT ===
if send_button and (user_text or uploaded_file):
    user_message = process_input(user_text, uploaded_file)
    st.session_state.conversation.extend(user_message)

    reply = get_assistant_reply(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": [{"type": "output_text", "text": reply}]})
    st.rerun()
