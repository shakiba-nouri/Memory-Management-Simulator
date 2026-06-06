# Memory Management Simulator

A Python-based simulation of Operating System memory management strategies. This project demonstrates how different allocation algorithms work and how memory deallocation and coalescing (merging) are handled to prevent fragmentation.

## 🚀 Features

- **Memory Allocation Algorithms:**
  - **First Fit:** Allocates the first available block that is large enough.
  - **Best Fit:** Allocates the smallest available block that fits the process requirements.
  - **Worst Fit:** Allocates the largest available block to leave the biggest possible leftover hole.
- **Dynamic Partitioning:** Supports splitting larger blocks into smaller ones during allocation.
- **Coalescing (Merging):** Automatically merges adjacent free blocks during deallocation to optimize space.
- **Interactive Menu:** User-friendly CLI to manage memory manually.
- **Automated Demo Scenarios:** Built-in test cases to showcase algorithm differences and fragmentation handling.

## 🛠️ How to Run

1. Ensure you have **Python 3.x** installed on your system.
2. Clone this repository or download the source code.
3. Run the script using the following command:
```bash
   python memory_manager.py
   
