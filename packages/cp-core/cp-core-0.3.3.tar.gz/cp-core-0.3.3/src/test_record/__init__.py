"""a record class to save the test record to a file"""

import json
import os
from datetime import datetime


class RecordForTest(object):
    def __init__(self, file_path="./tmp/test_records.json"):
        self.file_path = file_path
        self.records = self._load_records()

    def _load_records(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                content = f.read()
                return json.loads(content) if content else []
        return []

    def add_record(self, test_name, result, details=None):
        record = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "result": result,
            "details": details,
        }
        self.records.append(record)
        self._save_records()

    def _save_records(self):
        with open(self.file_path, "w") as f:
            json.dump(self.records, f, indent=2)

    def get_records(self):
        return self.records

    def clear_records(self):
        self.records = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
