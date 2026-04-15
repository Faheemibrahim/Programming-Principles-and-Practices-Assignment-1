# Warehouse Robot Optimization

## Overview
This project simulates a warehouse robot and finds the most efficient way to complete delivery tasks using a brute-force optimization approach.

---

## Problem
The robot operates in a 5×5 grid:
- `R` → Start position  
- `L` → Loading dock  
- `S1–S6` → Shelves  
- `.` → Empty space  

Each task requires the robot to:
1. Go to the loading dock  
2. Pick up an item  
3. Deliver it to a shelf  

The challenge is that **task order affects total distance**.

---

## Approach
- Generate all possible task orders (permutations)  
- Compute total distance for each  
- Select the minimum-cost solution  

---

## Distance Metric
Uses **Manhattan distance**:
- Horizontal and vertical movement only  
- No diagonal movement  

---

## Result
- Finds the **optimal solution** for 1–3 tasks  
- Demonstrates **algorithmic problem-solving**  
- Limited scalability due to brute-force approach  

---

## Reflection
This project improved my:
- Problem decomposition  
- Algorithmic thinking  
- Code structure and debugging  

It also reinforced concepts like functions, control flow, and basic data structures.


---
## Run

```bash
git clone https://github.com/your-username/warehouse-robot-optimization.git
cd warehouse-robot-optimization
python3 Final.py
