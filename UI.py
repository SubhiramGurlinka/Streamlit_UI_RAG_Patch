# import streamlit as st
# import requests
# import uuid

# # Backend base URL
# BASE_URL = "http://localhost:8000"

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = str(uuid.uuid4())
# if "interrupted" not in st.session_state:
#     st.session_state.interrupted = False
# if "last_message_count" not in st.session_state:
#     st.session_state.last_message_count = 0


# with st.sidebar:
#     if st.button("New Chat"):
#         st.session_state.thread_id = str(uuid.uuid4())
#         st.session_state.messages = []
#         st.session_state.interrupted = False
#         st.session_state.last_message_count = 0

# st.warning("This is a proof of concept. The agent is designed to assist you with information from BigFix documentation. We're continuously adding more content to the database to improve its responses. Currently, it has knowledge of the available BigFix documents.\n"
# "There is no streaming suport as of now. so the response will take a while to reflect"
# "")

# # Display past messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # User input
# if prompt := st.chat_input("Say something..."):
#     # Show user message
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Select endpoint
#     if len(st.session_state.messages) == 1 or not st.session_state.interrupted:
#         endpoint = f"{BASE_URL}/chat_initiate"
#         params = {
#             "thread_id": st.session_state.thread_id,
#             "message": prompt,
#         }
#     else:
#         endpoint = f"{BASE_URL}/chat-continue"
#         params = {
#             "thread_id": st.session_state.thread_id,
#             "response": prompt,
#         }

#     # Make request
#     try:
#         response = requests.get(endpoint, params=params)
#         response.raise_for_status()
#         response_json = response.json()
#         state = response_json.get("state", {})
#         interrupt_list = state.get("__interrupt__", [])
#         print("The state is ", state)
#         print("The interrupt list is ", interrupt_list)
#         # Decide what to show as AI message
#         # Extract all AI messages
#         all_ai_messages = [
#             msg["content"]
#             for msg in state.get("messages", [])
#             if msg.get("type") == "ai"
#         ]

#         # Show only new AI messages since last round
#         new_ai_messages = all_ai_messages[st.session_state.last_message_count:]
#         print("The new AI messages are: ", new_ai_messages)
#         # if interrupt_list:
#         #     interrupt_question = interrupt_list[0].get("value", {}).get("question", "🤖 (interrupted, but no question found)")
#         #     new_ai_messages.append(interrupt_question)
#         #     st.session_state.interrupted = True
#         if interrupt_list:
#             interrupt_question = interrupt_list[0].get("value", {}).get("question", "🤖 (interrupted, but no question found)")
#             interrupt_question = f"🔎 **{interrupt_question}**"
#             new_ai_messages.append(interrupt_question)
#             st.session_state.interrupted = True
#         else:
#             st.session_state.interrupted = False
#         # Update last_message_count
#         st.session_state.last_message_count = len(all_ai_messages)

#     except Exception as e:
#         ai_message = f"❌ API error: {e}"
#         st.session_state.interrupted = False
#         with st.chat_message("assistant"):
#             st.markdown(ai_message)
#             st.session_state.messages.append({"role": "assistant", "content": ai_message})
#     # Display new messages
#     print("The final new AI messages are: ", new_ai_messages)
#     for ai_msg in new_ai_messages:
#         print("ai message is ", ai_msg)
#         if ai_msg:
#             with st.chat_message("assistant"):
#                 st.markdown(ai_msg)
#             st.session_state.messages.append({"role": "assistant", "content": ai_msg})
import streamlit as st
import requests
import uuid
import time

BASE_URL = "http://localhost:8000"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "interrupted" not in st.session_state:
    st.session_state.interrupted = False
if "last_message_count" not in st.session_state:
    st.session_state.last_message_count = 0

with st.sidebar:
    if st.button("New Chat"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.interrupted = False
        st.session_state.last_message_count = 0

st.warning(
    "This is a proof of concept. The agent is designed to assist you with information from BigFix documentation. "
    "We're continuously adding more content to the database to improve its responses. Currently, it has knowledge of the available BigFix documents.\n"
    "There is no streaming support as of now, so the response will take a while to reflect."
)

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Say something..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Select endpoint
    if len(st.session_state.messages) == 1 or not st.session_state.interrupted:
        endpoint = f"{BASE_URL}/chat_initiate"
        params = {"thread_id": st.session_state.thread_id, "message": prompt}
    else:
        endpoint = f"{BASE_URL}/chat-continue"
        params = {"thread_id": st.session_state.thread_id, "response": prompt}

    # Show loading animation while waiting for API
    with st.status("🤖 Thinking...", expanded=True) as status:
        # Optional: staged messages for a nicer effect
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            response_json = response.json()
            # status.write("🔍 Firing up the LLM...")
            # time.sleep(10)
            # status.write("🔍 Searching for relevant data...")
            # time.sleep(10)
            # status.write("⏳ Fetching information from the server...")
            # time.sleep(10)
            # status.write("⚡ Preparing the response...")
            state = response_json.get("state", {})

            # Extract AI messages only
            all_ai_messages = [
                msg["content"]
                for msg in state.get("messages", [])
                if msg.get("type") == "ai"
            ]
            new_ai_messages = all_ai_messages[st.session_state.last_message_count:]
            st.session_state.last_message_count = len(all_ai_messages)

            status.update(label="✅ Response received!", state="complete", expanded=False)

        except Exception as e:
            new_ai_messages = [f"❌ API error: {e}"]
            status.update(label="⚠️ Error occurred", state="error", expanded=False)

    # Display only the AI messages to the chat
    for ai_msg in new_ai_messages:
        if ai_msg:
            with st.chat_message("assistant"):
                st.markdown(ai_msg)
            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
