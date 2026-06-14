from app.core.memory.short_term import ShortTermMemory
from app.core.memory.long_term import LongTermMemory

class MemoryManager:

    def __init__(self):
        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory()

    def write_short(self, user_id: int, content: str):
        self.short_memory.write(user_id, content)

    def read_short(self, user_id: int):
        return self.short_memory.read(user_id)
    
    def write_long(self, user_id: int, content: str):
        self.long_memory.write(user_id, content)

    def read_long(self, user_id: int):
        return self.long_memory.read(user_id)