from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint import StateSnapshot, MemoryCheckpoint
import os
import json
from langgraph.checkpoint.sqlite import SqliteSaver

class MemoryManager:

    def __init__(self, snapshot_file="memory_snapshot.json"):
        self.memory = MemorySaver()
        self.snapshot_file = snapshot_file

    # ----------------- SHORT-TERM MEMORY -----------------
    def get_short_term_memory(self):
        return self.memory

    # ----------------- SAVE SNAPSHOT -----------------
    def save_snapshot(self, state):
        snapshot = StateSnapshot(state=state)
        json_data = snapshot.model_dump()

        with open(self.snapshot_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        print("\n[Snapshot saved]\n")

    # ----------------- LOAD SNAPSHOT -----------------
    def load_snapshot(self):
        if not os.path.exists(self.snapshot_file):
            print("[No snapshot found — starting fresh]")
            return None

        with open(self.snapshot_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        snapshot = StateSnapshot(**data)
        print("\n[Snapshot loaded]\n")
        return snapshot.state
