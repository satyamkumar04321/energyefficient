#include <iostream>
#include <queue>
#include <vector>
#include <cmath>
#include <thread> // For sleep function
#include <chrono>
using namespace std;

struct Process {
    int id;
    int burst_time;
    int priority;
    int remaining_time;
    
    // Overload < operator for priority queue (higher priority = smaller quantum)
    bool operator<(const Process& other) const {
        return priority > other.priority; // Higher priority values run later
    }
};

class EnergyEfficientScheduler {
private:
    priority_queue<Process> processQueue;
    int baseQuantum;

public:
    EnergyEfficientScheduler(int quantum) : baseQuantum(quantum) {}

    void addProcess(int id, int burst_time, int priority) {
        Process p = {id, burst_time, priority, burst_time};
        processQueue.push(p);
    }

    void schedule() {
        while (!processQueue.empty()) {
            Process current = processQueue.top();
            processQueue.pop();
            
            int dynamicQuantum = calculateDynamicQuantum(current.priority, current.remaining_time);
            cout << "Executing Process " << current.id << " for " << dynamicQuantum << " units" << endl;
            this_thread::sleep_for(chrono::milliseconds(1000)); // Simulate execution
            
            current.remaining_time -= dynamicQuantum;
            if (current.remaining_time > 0) {
                processQueue.push(current); // Reinsert unfinished process
            } else {
                cout << "Process " << current.id << " completed!" << endl;
            }
        }
    }

    int calculateDynamicQuantum(int priority, int remaining_time) {
        return max(1, min(baseQuantum - (priority * 2), remaining_time)); // Ensure process doesn’t take more than needed
    }
};

int main() {
    EnergyEfficientScheduler scheduler(10);
    scheduler.addProcess(1, 15, 2);
    scheduler.addProcess(2, 10, 1);
    scheduler.addProcess(3, 20, 3);
    scheduler.schedule();
    return 0;
}
