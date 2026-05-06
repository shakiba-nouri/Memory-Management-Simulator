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


class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        # شروع حافظه با یک بلوک آزاد به اندازه کل فضا
        self.memory = [Block(0, total_size, True)]

    def show_status(self):
        print(f"\n--- Memory Status (Total: {self.total_size}) ---")
        for block in self.memory:
            print(block)

    def first_fit(self, pid, size):
        # همان کدی که با هم نوشتیم را اینجا قرار می‌دهیم (با تغییرات جزئی برای self.memory)
        for block in self.memory:
            if block.free and block.size >= size:
                if block.size > size:
                    new_block = Block(block.start + size, block.size - size)
                    idx = self.memory.index(block)
                    self.memory.insert(idx + 1, new_block)
                    block.size = size
                block.free = False
                block.pid = pid
                print(f"Process {pid} allocated via First Fit.")
                return True
        print(f"Error: No space for Process {pid}")
        return False

    def best_fit(self, pid, size):
    # پیدا کردن تمام بلوک‌های آزادی که اندازه کافی دارند
        candidates = [block for block in self.memory if block.free and block.size >= size]
        
        if not candidates:
            print(f"Error: No space for Process {pid} (Best Fit)")
            return False
        
        # انتخاب بلوکی که کوچکترین اندازه را در میان کاندیداها دارد
        best_block = min(candidates, key=lambda b: b.size)
        
        # تقسیم بلوک (Split) مشابه منطق قبلی که پیاده کرده بودی
        if best_block.size > size:
            new_block = Block(best_block.start + size, best_block.size - size)
            idx = self.memory.index(best_block)
            self.memory.insert(idx + 1, new_block)
            best_block.size = size
            
        best_block.free = False
        best_block.pid = pid
        print(f"Process {pid} allocated via Best Fit.")
        return True
    
    def worst_fit(self, pid, size):
        # پیدا کردن بلوک‌های آزاد مناسب
        candidates = [block for block in self.memory if block.free and block.size >= size]
        
        if not candidates:
            print(f"Error: No space for Process {pid} (Worst Fit)")
            return False
        
        # انتخاب بزرگ‌ترین بلوک آزاد
        worst_block = max(candidates, key=lambda b: b.size)
        
        # تقسیم بلوک در صورت نیاز
        if worst_block.size > size:
            new_block = Block(worst_block.start + size, worst_block.size - size)
            idx = self.memory.index(worst_block)
            self.memory.insert(idx + 1, new_block)
            worst_block.size = size
        
        worst_block.free = False
        worst_block.pid = pid
        print(f"Process {pid} allocated via Worst Fit.")
        return True


    def deallocate(self, pid):
        # همان منطق آزادسازی و ادغام که نوشتیم را اینجا می‌گذاریم
        found = False
        for block in self.memory:
            if not block.free and block.pid == pid:
                block.free = True
                block.pid = None
                found = True
        
        if found:
            self._merge_free_blocks()
            print(f"Process {pid} released.")
        else:
            print(f"Process {pid} not found.")

    def _merge_free_blocks(self):
        # تابع کمکی برای ادغام بلوک‌ها
        i = 0
        while i < len(self.memory) - 1:
            if self.memory[i].free and self.memory[i+1].free:
                self.memory[i].size += self.memory[i+1].size
                self.memory.pop(i+1)
            else:
                i += 1

def main():
    manager = MemoryManager(1000)

    while True:
        print("\n=== Memory Management Simulator ===")
        print("1) Show memory status")
        print("2) Allocate memory")
        print("3) Deallocate process")
        print("4) Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            manager.show_status()

        elif choice == "2":
            pid = input("Enter process ID: ")
            size = int(input("Enter memory size: "))

            print("\nSelect allocation algorithm:")
            print("1) First Fit")
            print("2) Best Fit")
            print("3) Worst Fit")
            algo = input("Your choice: ")

            if algo == "1":
                manager.first_fit(pid, size)
            elif algo == "2":
                manager.best_fit(pid, size)
            elif algo == "3":
                manager.worst_fit(pid, size)
            else:
                print("Invalid algorithm choice!")

        elif choice == "3":
            pid = input("Enter process ID to deallocate: ")
            manager.deallocate(pid)

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


