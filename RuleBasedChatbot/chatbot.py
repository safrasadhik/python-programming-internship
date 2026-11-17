
import re
import json


# 1. Load FAQ data from the JSON file
def load_faq_data():
    try:
        with open("sample_faq.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    except FileNotFoundError:
        print("Error: FAQ dataset file not found.")
        return None

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None


# 2. Normalize user input
def normalize_input(user_input):
    user_input = user_input.lower().strip()
    user_input = re.sub(r"\s+", " ", user_input)
    return user_input


# 3. Check for greetings
def check_greeting(user_input, greetings):
    for greeting in greetings:
        pattern = r"\b" + re.escape(greeting.lower()) + r"\b"

        if re.search(pattern, user_input):
            return True

    return False


# 4. Find matching FAQs
def find_faq(user_input, faqs):
    stop_words = {
        "what", "are", "your", "how", "do", "i", "when",
        "will", "the", "my", "is", "a", "an", "to", "of",
        "can", "you", "me", "please"
    }

    for faq in faqs:
        question = faq["question"].lower()

        # Extract meaningful keywords from the FAQ question
        words = re.findall(r"\b[a-z]+\b", question)
        keywords = [word for word in words if word not in stop_words]

        # Check whether any meaningful keyword appears in the input
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, user_input):
                return faq

    return None


# 5. Generate chatbot response
def get_response(user_input, data):
    user_input = normalize_input(user_input)

    if not user_input:
        return "Please enter a message so I can help you."

    # Handle greetings
    if check_greeting(user_input, data["greetings"]):
        return "Hello! Welcome to our chatbot. How can I assist you today?"

    # Handle frequently asked questions
    matched_faq = find_faq(user_input, data["faqs"])

    if matched_faq:
        return matched_faq["answer"]

    # Default response if no match is found
    return (
        "Sorry, I couldn't understand your question. "
        "Please try asking about business hours, "
        "internship project submission, or certificates."
    )


# 6. Main chatbot function
def chatbot():
    data = load_faq_data()

    if data is None:
        return

    print("=" * 55)
    print("          RULE-BASED CUSTOMER SUPPORT CHATBOT")
    print("=" * 55)

    print("Bot: Hello! Welcome to our customer support chatbot.")
    print("Bot: How can I assist you today?")
    print("Bot: Type 'bye', 'exit', or 'quit' to end the chat.\n")

    while True:
        user_input = input("You: ")

        normalized_input = normalize_input(user_input)

        # Exit commands
        if normalized_input in ["bye", "exit", "quit"]:
            print("Bot: Thank you for chatting with me. Goodbye!")
            break

        # Generate and display response
        response = get_response(user_input, data)

        print("Bot:", response)


# 7. Run the chatbot
if __name__ == "__main__":
    chatbot()
