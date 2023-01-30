from pathlib import Path
from typing import Dict, Tuple, List

#C:\Users\Charles Hsu\PycharmProjects\Project1_New\samples\sample_input.txt

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    file = Path(input())
    if file.exists() and file.is_file():
        return file
    else:
        raise FileExistsError(f"{file} not found or it's not a file")


def _send_alerts(devices: List[str], alerts: List[Tuple[int, str, int]]) -> Dict[int, Dict[str, int]]:
    """Send alerts with a delay time"""
    print(1)
    sent_alerts = {}
    for alert in alerts:
        device, message, time = alert
        for device in devices:
            sent_alerts[device] = {"device": device, "message": message, "time": time}
    return sent_alerts


def _propagate_alerts(alerts: Dict[int, Dict[str, int]], propagate: Dict[Tuple[int, int], int])-> Dict[int, Dict[str, int]]:
    """Propagate alerts between devices"""
    print(2)
    propagated_alerts = {}
    for (start, dest, delay) in propagate.items():
        if start in alerts:
            device = alerts[start]["device"]
            message = alerts[start]["message"]
            propagated_alerts[dest] = {"device": dest, "message": message, "delay": delay}
    return propagated_alerts


def _cancel_alerts(alerts: Dict[int, Dict[str, int]], cancel: Dict[Tuple[int, int], int]):
    """Cancel the alert on devices"""
    print(3)
    cancel_alerts = {}
    for alert in alerts:
        device, message, time = alert
        for start, dest, delay in cancel:
            if start == device:
                cancel_alerts[dest] = {"device": dest, "message": message, "delay": time}
    return cancel_alerts


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()

    devices = []
    propagate = {}
    alerts = {}
    cancel = {}

    with open(input_file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("LENGTH"):
                length = int(line.split()[1])
            elif line.startswith("DEVICE"):
                devices.append(line.split()[1])
            elif line.startswith("PROPAGATE"):
                start, dest, delay = line.split()[1:]
                propagate[(start, dest, delay)] = int(delay)
                _propagate_alerts(devices, propagate)
            elif line.startswith("ALERT"):
                start, alert, timestamp = line.split()[1:]
                alerts[(start, alert, timestamp)] = int(timestamp)
                _send_alerts(devices, alerts)
            elif line.startswith("CANCEL"):
                start, alert, timestamp = line.split()[1:]
                cancel[(start, alert, timestamp)] = int(timestamp)
                _cancel_alerts(alerts, cancel)

    print(propagate)
    print(alerts)
    print(cancel)



if __name__ == '__main__':
    main()
