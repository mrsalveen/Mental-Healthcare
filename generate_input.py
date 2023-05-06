import json

CUSTOMER = "Seeker:"
AGENT = "Supporter:"

class Message:
    def __init__(self, text, is_user=False):
        self.text = text
        self.is_user = is_user

    def get_decorated_text(self):
        prefix = CUSTOMER if self.is_user else AGENT
        return prefix + " " + self.get_raw_text()

    def get_raw_text(self):
        return self.text + ("" if self.text[-1] == "\n" else "\n")


class Conversation:
    def __init__(self, messages):
        self.messages = messages

    def to_json_list(self):
        json_list = []
        current_history = MessageList()
        for message in self.messages:
            current_history.add_message(message)
            if not message.is_user:
                json_entry = {
                    "prompt": current_history.get_prompt(),
                    "completion": current_history.get_answer()
                }
                json_list.append(json_entry)
        return json_list


class MessageList:
    def __init__(self, messages=None):
        if messages is None:
            messages = []
        self.messages = messages

    def add_message(self, message):
        self.messages.append(message)

    def get_prompt(self):
        prompt = ""
        for message in self.messages[:-1]:
            prompt += message.get_decorated_text()
        prompt += AGENT
        return prompt

    def get_answer(self):
        return self.messages[-1].get_raw_text()


def read_es_conv():
    with open('data_input/ESConv.json') as f:
        data = json.load(f)
        conversations = []
        for conversation_data in data:
            messages = []
            for message_data in conversation_data['dialog']:
                is_user = message_data['speaker'] == 'seeker'
                messages.append(Message(message_data['content'], is_user))
            conversations.append(Conversation(messages))
        return conversations


def create_output_data(conversations):
    output_data = []
    for conversation in conversations:
        output_data.extend(conversation.to_json_list())
    return output_data


def write_to_file(output_data):
    with open('data_output/gpt4_input.json', 'w') as f:
        json.dump(output_data, f)


if __name__ == '__main__':
    conversations = read_es_conv()
    output_data = create_output_data(conversations)
    write_to_file(output_data)
