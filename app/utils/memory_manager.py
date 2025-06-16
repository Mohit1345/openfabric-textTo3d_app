import json
import os
from datetime import datetime
import logging

class MemoryManager:
    def __init__(self):
        self.short_term_memory = []

        self.outputs_dir = "/openfabric/app/outputs"
        os.makedirs(self.outputs_dir, exist_ok=True)

        self.chat_data_file = os.path.join(self.outputs_dir, 'chat_data.json')
        if not os.path.isfile(self.chat_data_file):
            with open(self.chat_data_file, 'w') as f:
                json.dump([], f)

    def append_short_term(self, entry: dict):
        logging.info(f"Appending to short-term memory: {entry}")
        self.short_term_memory.append(entry)

    def save_to_long_term(self):
        try:
            with open(self.chat_data_file, 'r') as f:
                existing_data = json.load(f)

            existing_data.append({
                'session_end_time': datetime.utcnow().isoformat(),
                'session_data': self.short_term_memory
            })

            with open(self.chat_data_file, 'w') as f:
                json.dump(existing_data, f, indent=4)

            self.short_term_memory.clear()
            print("✅ Memory saved to chat_data.json")
        except Exception as e:
            print(f"❌ Error saving chat_data.json: {str(e)}")
