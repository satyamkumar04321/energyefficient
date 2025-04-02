import heapq
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx

# Process class
class Process:
    def __init__(self, pid, burst_time, energy_consumption):
        self.pid = pid
        self.burst_time = burst_time
        self.energy_consumption = energy_consumption
    
    def __lt__(self, other):
        return self.energy_consumption < other.energy_consumption

# Scheduler class
class EnergyEfficientScheduler:
    def __init__(self):
        self.process_queue = []
        self.resource_allocation = {}
        self.resource_request = {}

    def add_process(self, pid, burst_time, energy_consumption):
        process = Process(pid, burst_time, energy_consumption)
        heapq.heappush(self.process_queue, process)
    
    def schedule(self):
        execution_order = []
        total_energy_used = 0
        while self.process_queue:
            process = heapq.heappop(self.process_queue)
            execution_order.append((process.pid, process.energy_consumption))
            total_energy_used += process.energy_consumption
        return execution_order, total_energy_used

    def add_resource_allocation(self, process_id, allocated, requested):
        self.resource_allocation[process_id] = allocated
        self.resource_request[process_id] = requested
    
    def detect_deadlock(self):
        graph = nx.DiGraph()
        
        for process, resources in self.resource_allocation.items():
            for resource in resources:
                graph.add_edge(resource, process)
        
        for process, resources in self.resource_request.items():
            for resource in resources:
                graph.add_edge(process, resource)
        
        try:
            cycle = nx.find_cycle(graph, orientation='original')
            return True, cycle
        except nx.NetworkXNoCycle:
            return False, []

# GUI Functions
def add_process():
    try:
        pid = int(entry_pid.get())
        burst_time = int(entry_burst.get())
        energy = int(entry_energy.get())
        scheduler.add_process(pid, burst_time, energy)
        messagebox.showinfo("Success", f"Process {pid} added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter integers only.")

def run_scheduler():
    execution_order, total_energy = scheduler.schedule()
    result_text.set(f"Execution Order: {[p[0] for p in execution_order]}\nTotal Energy: {total_energy} units")
    plot_energy_consumption(execution_order)

def plot_energy_consumption(execution_order):
    pids = [p[0] for p in execution_order]
    energy_values = [p[1] for p in execution_order]
    plt.figure(figsize=(6, 4))
    plt.bar(pids, energy_values, color='green')
    plt.xlabel("Process ID")
    plt.ylabel("Energy Consumption")
    plt.title("Energy Consumption per Process")
    plt.show()

def check_deadlock():
    has_deadlock, cycle = scheduler.detect_deadlock()
    if has_deadlock:
        messagebox.showwarning("Deadlock Detected", "A deadlock has been detected!")
        visualize_deadlock(cycle)
    else:
        messagebox.showinfo("No Deadlock", "No deadlock detected.")

def visualize_deadlock(cycle):
    G = nx.DiGraph()
    G.add_edges_from(cycle)
    plt.figure(figsize=(6, 4))
    nx.draw(G, with_labels=True, node_color='red', edge_color='black', node_size=1500, font_size=10)
    plt.title("Deadlock Detection Graph")
    plt.show()

# GUI Setup
scheduler = EnergyEfficientScheduler()
root = tk.Tk()
root.title("Energy-Efficient CPU Scheduler")

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Process ID:").grid(row=0, column=0)
entry_pid = tk.Entry(frame)
entry_pid.grid(row=0, column=1)

tk.Label(frame, text="Burst Time:").grid(row=1, column=0)
entry_burst = tk.Entry(frame)
entry_burst.grid(row=1, column=1)

tk.Label(frame, text="Energy Consumption:").grid(row=2, column=0)
entry_energy = tk.Entry(frame)
entry_energy.grid(row=2, column=1)

tk.Button(frame, text="Add Process", command=add_process).grid(row=3, columnspan=2, pady=10)
tk.Button(frame, text="Run Scheduler", command=run_scheduler).grid(row=4, columnspan=2, pady=10)
tk.Button(frame, text="Check Deadlock", command=check_deadlock).grid(row=5, columnspan=2, pady=10)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text).pack()

root.mainloop()
