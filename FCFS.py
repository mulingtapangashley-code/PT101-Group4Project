print("=" * 55)
print("          FCFS CPU SCHEDULING SYSTEM")
print("=" * 55)

# USER INPUT
while True:
    try:
        n = int(input("\nEnter number of processes: "))
        if n > 0:
            break
        print("Please enter at least 1 process.")
    except ValueError:
        print("Invalid input! Enter a number.")

processes = []

for i in range(n):

    print(f"\nEnter details for Process {i + 1}")

    pid = input("Process ID: ")

    while True:
        try:
            at = int(input("Arrival Time: "))
            bt = int(input("Burst Time: "))

            if at >= 0 and bt > 0:
                break

            print("Arrival time must be >= 0 and burst time > 0.")

        except ValueError:
            print("Invalid input! Enter integers only.")

    processes.append({
        "pid": pid,
        "at": at,
        "bt": bt,
        "ct": 0,
        "tat": 0,
        "wt": 0,
        "rt": 0
    })

processes.sort(key=lambda p: p["at"])

time = 0
timeline = []

total_ct = 0
total_tat = 0
total_wt = 0
total_rt = 0

for p in processes:

    if time < p["at"]:
        timeline.append({
            "pid": "IDLE",
            "start": time,
            "end": p["at"]
        })

        time = p["at"]

    start_time = time
    p["rt"] = start_time - p["at"]

    time += p["bt"]

    p["ct"] = time

    p["tat"] = p["ct"] - p["at"]

    p["wt"] = p["tat"] - p["bt"]

    timeline.append({
        "pid": p["pid"],
        "start": start_time,
        "end": time
    })

    total_ct += p["ct"]
    total_tat += p["tat"]
    total_wt += p["wt"]
    total_rt += p["rt"]

print("\n" + "=" * 55)
print("                  GANTT CHART")
print("=" * 55)

width = 9

for segment in timeline:
    print("+" + "-" * width, end="")
print("+")

for segment in timeline:
    print("|" + segment["pid"].center(width), end="")
print("|")

for segment in timeline:
    print("+" + "-" * width, end="")
print("+")

print("\nTIME INTERVALS:")

for segment in timeline:
    print(f"{segment['start']} -> ", end="")

print(timeline[-1]["end"])

print("\n" + "=" * 75)
print("                    PROCESS TABLE")
print("=" * 75)

print(
    f"{'PID':<12}"
    f"{'AT':<10}"
    f"{'BT':<10}"
    f"{'CT':<10}"
    f"{'TAT':<10}"
    f"{'WT':<10}"
    f"{'RT':<10}"
)

print("-" * 75)

for p in processes:
    print(
        f"{p['pid']:<12}"
        f"{p['at']:<10}"
        f"{p['bt']:<10}"
        f"{p['ct']:<10}"
        f"{p['tat']:<10}"
        f"{p['wt']:<10}"
        f"{p['rt']:<10}"
    )

print("-" * 75)

avg_ct = total_ct / n
avg_tat = total_tat / n
avg_wt = total_wt / n
avg_rt = total_rt / n

print("\n" + "=" * 55)
print("                AVERAGE RESULTS")
print("=" * 55)

print(f"Average Completion Time   : {avg_ct:.2f}")
print(f"Average Turnaround Time   : {avg_tat:.2f}")
print(f"Average Waiting Time      : {avg_wt:.2f}")
print(f"Average Response Time     : {avg_rt:.2f}")

print("\n" + "=" * 55)
print("              FCFS COMPARISON")
print("=" * 55)

print("Algorithm: First Come, First Served")
print("Type: Non-Preemptive")
print("Scheduling: Based on Arrival Time")
print("Execution: First process to arrive runs first.")
print("Preemption: Not allowed.")

print("\nFCFS CPU Scheduling Completed!")
print("=" * 55)
