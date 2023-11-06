from openai import OpenAI
import os
import time

# Initialize OpenAI client with API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Create an Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)

# Create a Thread
thread = client.beta.threads.create()

# Add a Message to the Thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)

# Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
)
run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)
while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run_status.status == "completed":
        break
    time.sleep(1)  # Simple polling, consider using a more sophisticated method in production

# Now list the messages
messages_response = client.beta.threads.messages.list(
    thread_id=thread.id
)
# ... (previous code)

# Now list the messages
messages_response = client.beta.threads.messages.list(
    thread_id=thread.id
)

# Extract the messages from the response
# Assuming that the SyncCursorPage object has an attribute called 'data' that contains the list of messages
messages = messages_response.data


# Define the function to print messages in a readable format
def print_messages(messages):
    for message in messages:
        # Extract the timestamp, role, and content from each message
        time_created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message.created_at))
        role = message.role.capitalize()
        # Check if the message content is not empty
        if message.content:
            # We will take the first element of the content list and retrieve its 'value'
            content = message.content[0].text.value
            print(f"{time_created} | {role} said: \"{content}\"")


sorted_messages = sorted(messages, key=lambda msg: msg.created_at)

# Call the function to print messages
print_messages(sorted_messages)
