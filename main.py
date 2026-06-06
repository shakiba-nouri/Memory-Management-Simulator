class Block:
    def __init__(self, start, size, free=True, pid=None):
        self.start = start
        self.size = size
        self.free = free
        self.pid = pid

    def __str__(self):
        status = "Free" if self.free else f"P{self.pid}"
        return f"[Start:{self.start:03d} Size:{self.size:03d} | {status}]"


class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        self.memory = [Block(0, total_size, True)]

    def show_status(self):
        print("\n" + "="*45)
        print(f"--- Memory Status (Total Capacity: {self.total_size}) ---")
        for block in self.memory:
            print(block)
        print("="*45)

    def first_fit(self, pid, size):
        for block in self.memory:
            if block.free and block.size >= size:
                self._allocate(block, pid, size)
                print(f"✅ Process {pid} (Size {size}) allocated via First Fit.")
                return True
        print(f"❌ Error: No space for Process {pid}")
        return False

    def best_fit(self, pid, size):
        candidates = [b for b in self.memory if b.free and b.size >= size]
        if not candidates:
            print(f"❌ Error: No space for Process {pid} (Best Fit)")
            return False
        best_block = min(candidates, key=lambda b: b.size)
        self._allocate(best_block, pid, size)
        print(f"✅ Process {pid} (Size {size}) allocated via Best Fit.")
        return True

    def worst_fit(self, pid, size):
        candidates = [b for b in self.memory if b.free and b.size >= size]
        if not candidates:
            print(f"❌ Error: No space for Process {pid} (Worst Fit)")
            return False
        worst_block = max(candidates, key=lambda b: b.size)
        self._allocate(worst_block, pid, size)
        print(f"✅ Process {pid} (Size {size}) allocated via Worst Fit.")
        return True

    def _allocate(self, block, pid, size):
        if block.size > size:
            new_block = Block(block.start + size, block.size - size)
            idx = self.memory.index(block)
            self.memory.insert(idx + 1, new_block)
            block.size = size
        block.free = False
        block.pid = pid

    def deallocate(self, pid):
        found = False
        for block in self.memory:
            if not block.free and str(block.pid) == str(pid):
                block.free = True
                block.pid = None
                found = True
        
        if found:
            self._merge_free_blocks()
            print(f"🧹 Process {pid} released and memory merged.")
        else:
            print(f"⚠️ Process {pid} not found.")

    def _merge_free_blocks(self):
        i = 0
        while i < len(self.memory) - 1:
            if self.memory[i].free and self.memory[i+1].free:
                self.memory[i].size += self.memory[i+1].size
                self.memory.pop(i+1)
            else:
                i += 1

    def run_test_scenario(self):
        print("\n🚀 Starting Automated Demo Scenarios...")
        
        # سناریوی اول: مقایسه الگوریتم‌ها
        print("\n--- SCENARIO 1: Algorithm Comparison ---")
        self.memory = [Block(0, 1000, True)] # ریست کردن حافظه
        # ایجاد حفره‌های مختلف
        self.first_fit("A", 100) # [0-100]
        self.first_fit("B", 200) # [100-300]
        self.first_fit("C", 100) # [300-400]
        self.deallocate("B")     # ایجاد حفره 200 واحدی در وسط
        self.show_status()
        
        print("\nTrying to allocate 150 units for Process X...")
        print("Note: First Fit takes the first 200 block, Best Fit takes the smallest possible.")
        self.best_fit("X", 150)
        self.show_status()

        # سناریوی دوم: آزادسازی و ادغام
        print("\n--- SCENARIO 2: Deallocation & Merging (Coalescing) ---")
        self.deallocate("A")
        print("After deallocating A (next to the free block):")
        self.show_status()
        print("As you see, blocks were merged to prevent fragmentation.")


def main():
    manager = MemoryManager(1000)

    while True:
        print("\n" + "*"*30)
        print("  MEMORY MANAGER SIMULATOR")
        print("*"*30)
        print("1) Show Memory Status")
        print("2) Allocate Memory (Manual)")
        print("3) Deallocate Process")
        print("4) Run Automated Demo Scenarios ✨")
        print("5) Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            manager.show_status()
        elif choice == "2":
            pid = input("Process ID: ")
            size = int(input("Size: "))
            print("1) First Fit  2) Best Fit  3) Worst Fit")
            algo = input("Choose Algorithm: ")
            if algo == "1": manager.first_fit(pid, size)
            elif algo == "2": manager.best_fit(pid, size)
            elif algo == "3": manager.worst_fit(pid, size)
        elif choice == "3":
            pid = input("Enter Process ID to release: ")
            manager.deallocate(pid)
        elif choice == "4":
            manager.run_test_scenario()
        elif choice == "5":
            break
        else:
            print("Invalid Option!")

if __name__ == "__main__":
    main()
