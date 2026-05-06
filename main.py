class Block:
    def __init__(self, start, size, free=True, pid=None):
        self.start = start
        self.size = size
        self.free = free
        self.pid = pid

    def __str__(self):
        if self.free:
            status = "Free"
        else:
            status = f"P{self.pid}"
        return f"[Start:{self.start} Size:{self.size} {status}]"

MEMORY_SIZE = 1000

memory = [Block(0, MEMORY_SIZE, True)]

def show_memory(memory):
    print("\nMemory Status:")
    for block in memory:
        print(block)

show_memory(memory)


def first_fit(memory, pid, size):
    for block in memory:
        if block.free and block.size >= size:

            # اگر بلوک بزرگتر از نیاز است، split می‌شود
            if block.size > size:
                new_block = Block(
                    start=block.start + size,
                    size=block.size - size,
                    free=True
                )
                index = memory.index(block)
                memory.insert(index + 1, new_block)
                block.size = size

            # تخصیص بلوک به فرآیند
            block.free = False
            block.pid = pid
            print(f"Process {pid} allocated successfully")
            return True

    print(f"Process {pid} cannot be allocated (no space)")
    return False

first_fit(memory, pid=1, size=200)
show_memory(memory)

first_fit(memory, pid=2, size=300)
show_memory(memory)

def deallocate(memory, pid):
    # آزاد کردن بلوک/بلوک‌های متعلق به این pid
    found = False
    for block in memory:
        if (not block.free) and block.pid == pid:
            block.free = True
            block.pid = None
            found = True

    if not found:
        print(f"No block found for process {pid}")
        return False

    # ادغام بلوک‌های آزاد مجاور
    i = 0
    while i < len(memory) - 1:
        current_block = memory[i]
        next_block = memory[i + 1]

        if current_block.free and next_block.free:
            # ادغام: اندازه‌ها جمع می‌شود
            current_block.size += next_block.size
            # بلوک بعدی حذف می‌شود
            memory.pop(i + 1)
            # i را زیاد نمی‌کنیم چون ممکن است دوباره با بلوک بعدی هم قابل ادغام باشد
        else:
            i += 1

    print(f"Process {pid} deallocated successfully")
    return True


print("\nDeallocating P2...")
deallocate(memory, pid=2)
show_memory(memory)