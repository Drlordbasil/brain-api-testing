import requests
import re

BASE_URL = "http://127.0.0.1:5000"

class Brain:
    def __init__(self):
        self.history = []

    def think(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        # Step 1: Generate initial thoughts with structured tags
        initial_thoughts_prompt = f"""
You are an AI assistant that thinks before responding.

Please analyze the user's input and generate your thoughts enclosed in <thought></thought> tags.

**Example**:

User's input: 'Tell me a joke.'

Assistant's thoughts:
<thought>
- Think of a joke that's appropriate and funny.
- Ensure the joke is suitable for all audiences.
</thought>

Now, based on the user's input: '{user_input}', provide your thoughts.
        """

        initial_thoughts = self.generate_text(initial_thoughts_prompt)
        print(f"[DEBUG] Initial thoughts: {initial_thoughts}\n")

        if not initial_thoughts:
            return "I'm sorry, I couldn't generate any thoughts."

        # Extract thoughts from assistant's response
        thoughts = self.extract_thoughts(initial_thoughts)
        print(f"[DEBUG] Extracted thoughts: {thoughts}\n")

        # Step 2: Generate a final response based on the thoughts
        if thoughts:
            combined_thoughts = ' '.join(thoughts)
            final_response_prompt = f"""
You are an AI assistant ready to respond to the user.

Based on your thoughts: {combined_thoughts}

Construct a clear and helpful response to the user's input: '{user_input}'

Do not include your thoughts in the final response.

**Example**:

Thoughts:
- Consider a funny joke about animals.
- Make sure it's appropriate.

Assistant's response:
'Why did the scarecrow win an award? Because he was outstanding in his field!'

Now, provide your response.
            """

            final_response = self.generate_text(final_response_prompt)
            print(f"[DEBUG] Final response: {final_response}\n")
        else:
            final_response = "I'm sorry, I couldn't formulate any thoughts to respond."

        # Accept any non-empty response as a valid final answer
        if self.is_final_answer(final_response):
            self.history.append({"role": "assistant", "content": final_response})
            return final_response
        else:
            return "I'm sorry, I couldn't find a satisfactory response."

    def extract_thoughts(self, text):
        # Extract text enclosed in <thought></thought> tags
        pattern = r"<thought>(.*?)</thought>"
        thoughts = re.findall(pattern, text, re.DOTALL)
        return thoughts

    def generate_text(self, prompt):
        url = f"{BASE_URL}/generate_text"
        payload = {
            "prompt": prompt,
            "history": self.history  # Include conversation history for context
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            assistant_response = response.json().get("response", "").strip()
            # Do not append thoughts to history to avoid cluttering
            return assistant_response
        else:
            print(f"[ERROR] Failed to generate text: {response.text}")
            return ""

    def is_final_answer(self, response):
        # Accept any non-empty response as a valid final answer
        return len(response.strip()) > 0

def main():
    brain = Brain()
    user_input = input("You: ")
    response = brain.think(user_input)
    print("\nAI:", response)

if __name__ == "__main__":
    main()