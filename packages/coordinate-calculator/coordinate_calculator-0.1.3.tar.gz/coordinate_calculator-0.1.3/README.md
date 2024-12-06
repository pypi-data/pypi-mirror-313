# Object Position Calculator

This library helps calculate the geographical position of detected objects using camera parameters and object detection results.

## Installation

```bash
pip install object-position-calculator
```

### Example
```python
if __name__ == "__main__":
    client = DroneYOLOClient("http://10.109.68.49:8000")
    client.connect()
    client.send_message_to_server("Hello, world from YOLO!")
    client.send_drone_command("capture_img")
    client.wait()
```

