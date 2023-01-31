from pathlib import Path

#C:\Users\Charles Hsu\PycharmProjects\Project1_New\samples\sample_input.txt

def _read_input_file_path(file = None) -> Path:
    """Reads the input file path from the standard input"""
    if file is None:
        file = Path(input())
    if file.exists() and file.is_file():
        return file
    else:
        raise FileExistsError(f"{file} not found or it's not a file")

def calculate(commend, cancel_time , devices, propagate, process, commend_str):
    msg = commend[1]["msg"]
    timer = commend[1]["timestamp"]
    temp_process = list()
    counter = 0
    if cancel_time > sum(propagate) + timer:
        counter = cancel_time // (sum(propagate) + timer)
    while True:
        for index in range(len(devices)):
            if index > 0:
                timer = timer + propagate[index - 1]
                temp_process.append((commend_str + " r", devices[index], devices[index - 1], msg, timer))
            if index + 1 == len(devices):
                temp_process.append((commend_str, devices[index], devices[0], msg, timer))
            else:
                temp_process.append((commend_str, devices[index], devices[index + 1], msg, timer))
        timer = timer + propagate[index]
        temp_process.append((commend_str + " r", devices[0], devices[index], msg, timer))
        counter -= 1
        if counter < 0:
            break
    process += temp_process

def calculate_cancel(cancel, cancel_time, devices, propagate, process):
    calculate(cancel,cancel_time, devices, propagate, process, "Cancel")

def calculate_alert(alerts, cancel_time, devices, propagate, process):
    calculate(alerts,cancel_time,devices, propagate, process, "Alert")

def calculate_process(alerts, cancel, devices, propagate, process):
    cancel_time = cancel[1]["timestamp"]
    calculate_cancel(cancel, cancel_time, devices, propagate, process)
    calculate_alert(alerts, cancel_time, devices, propagate, process)

def sort_process(process):
    temp_process = sorted(process, key =  lambda x:x[4])
    return temp_process.copy()

def generate_print_msg(process):
    for i in process:
        cmd, s, d, msg, time = i
        if cmd == "Cancel":
            print_cancel_msg(s, d, msg, time)
        elif cmd == "Cancel r":
            print_recieve_cancel_msg(s, d, msg, time)
        elif cmd == "Alert":
            print_alert_msg(s, d, msg, time)
        elif cmd == "Alert r":
            print_recieve_alert_msg(s, d, msg, time)
        elif cmd == "end":
            print_end_msg(time)

def print_cancel_msg(s, d, msg, time):
    print(f"@{time}: #{s} SENT CANCELLATION TO #{d}: {msg}")

def print_recieve_cancel_msg(s, d, msg, time):
    print(f"@{time}: #{s} RECEIVED CANCELLATION FROM #{d}: {msg}")

def print_alert_msg(s, d, msg, time):
    print(f"@{time}: #{s} SENT ALERT TO #{d}: {msg}")

def print_recieve_alert_msg(s, d, msg, time):
    print(f"@{time}: #{s} RECEIVED ALERT FROM #{d}: {msg}")

def print_end_msg(time):
    print(f"@{time}: END")

def main() -> None:
    """Runs the simulation program in its entirety"""
    # path = Path("C:/Users/Charles Hsu/PycharmProjects/Project1_New/samples/sample_input.txt")
    input_file_path = _read_input_file_path()

    length = 0
    devices = list()
    propagate = list()
    alerts = dict()
    cancel = dict()

    process = list()

    with open(input_file_path, "r") as file:
        for line in file:
            line = line.strip()
            line = line.split()
            if len(line) == 0:
                continue
            if line[0] == "LENGTH":
                length = int(line[1]) * 60000
                process.append(("end", 0, 0, 0, length))
            elif line[0] == "DEVICE":
                devices.append(int(line[1]))
            elif line[0] == "PROPAGATE":
                start, dest, delay = line[1:]
                propagate.append(int(delay))
            elif line[0] == "ALERT":
                start, msg, timestamp = line[1:]
                alerts[int(start)] = {"msg": msg, "timestamp": int(timestamp)}
            elif line[0] == "CANCEL":
                start, msg, timestamp = line[1:]
                cancel[int(start)] = {"msg": msg, "timestamp": int(timestamp)}



    # print(propagate)
    # print(alerts)
    # print(cancel)
    # _send_alerts(devices, alerts)
    # _propagate_alerts(devices, propagate)
    # _cancel_alerts(alerts, cancel)
    calculate_process(alerts, cancel, devices, propagate, process)
    process = sort_process(process)
    # print(process)
    generate_print_msg(process)


if __name__ == '__main__':
    main()

