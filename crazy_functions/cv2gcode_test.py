# import cv2
# import numpy as np
# import serial
# import serial.tools.list_ports
# import time
# import keyboard
# import argparse





# # Step 1: Read the image
# parser = argparse.ArgumentParser(description='G-code Generator')
# parser.add_argument('image', type=str, help='Path to the image file')
# args = parser.parse_args()
# image = cv2.imread(args.image)

# # Step 2: Preprocess the image
# image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
# image = cv2.flip(image, 0)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (5, 5), 0)
# edged = cv2.Canny(blur, 10, 255)
# #Preview
# cv2.imshow("edged", edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# # Step 3: Get image contours
# contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# # Step 4: Convert contours to G-code
# feedrate = 1000
# gcode = []
# for contour in contours:
#     gcode.append('M3 S40')  # Raise pen
#     for point in contour:
#         x, y = point[0] / 25.4 # The machine moves in inches, turn into mm first
#         gcode.append('G00 X{:.3f} Y{:.3f} F{}'.format(x, y, feedrate))  # Move pen to starting point
#         gcode.append('M5')  # Lower pen
#         gcode.append('G01 X{:.3f} Y{:.3f} F{}'.format(x, y, feedrate))  # Draw the contour
# # Move to the origin
# gcode.append('M3 S40')
# gcode.append('\n')
# gcode.append('G00 X0 Y0 F{}'.format(feedrate))
# # Save gcode file
# with open('out.gcode', 'w') as file:
#     for command in gcode:
#         file.write(command + '\n')

# print("G-code generation complete.")

# # Step 5: Search for Arduino board
# arduino_ports = [
#     p.device for p in serial.tools.list_ports.comports()
#     if 'Arduino' in p.description or 'VID:PID' in p.description or 'tty' in p.description
# ]
# if not arduino_ports:
#     raise IOError("No Arduino board found.")

# port = arduino_ports[0]  # Use the first Arduino board found
# baud_rate = 115200
# # Establish serial connection with the pen plotter
# ser = serial.Serial(port, baud_rate, timeout=1)
# # Wait for the connection to stabilize
# time.sleep(2)


# stop_sending = False  # Flag to track if user requested to stop sending

# def stop_sending_callback(event):
#     global stop_sending
#     stop_sending = True

# # Register 'a' key press event
# keyboard.on_press_key('a', stop_sending_callback)

# # Step 6: Send the G-code commands
# print("G-code start sending to plotter. Press 'a' to abort.")
# for command in gcode:
#     ser.write(command.encode())
#     ser.write(b'\n')
#     # Wait for the command to be processed
#     while True:
#         response = ser.readline().decode().strip()
#         if response == 'ok':
#             break
    
#     # Abort mechanism
#     if stop_sending:
#         print("User stopped the G-code sending.")
#         time.sleep(2)
#         ser.write(b'M3 S40')
#         ser.write(b'\n')
#         ser.write(b'G00 X0 Y0')  # Move pen plotter to (0, 0)
#         ser.write(b'\n')
#         ser.write(b'M5')
#         ser.write(b'\na')
#         ser.close()
#         print("Pen plotter moved to (0, 0). Program closed.")
#         break

# # Close the serial connection
# ser.close()

# if stop_sending is False:
#     print("G-code sent to the pen plotter.")


# import serial
# import serial.tools.list_ports
# import time

# def list_serial_ports():
#     """ Lists serial port names """
#     return [port.device for port in serial.tools.list_ports.comports()]

# def test_robot_serial():
#     print("haha")
#     port ='/dev/cu.usbmodem11301' 
#     baud_rate=115200
#     ser = None
#     try:
#         # Establish connection
#         ser = serial.Serial(port, baud_rate, timeout=1)
#         time.sleep(2)  # Wait for connection to stabilize

#         # Send a test command (e.g., 'ping')
#         test_command = 'ping'
#         print(f"Sending test command: {test_command}")
#         ser.write(test_command.encode())

#         # Wait for response
#         response = ser.readline().decode().strip()
#         print(f"Received response: {response}")

#     except serial.SerialException as e:
#         print(f"Serial error: {e}")

#     finally:
#         if ser:
#             ser.close()
#             print("Serial connection closed.")

# # Usage example
# print("Available serial ports:", list_serial_ports())
# Replace with your device's port and appropriate baud rate.
# Replace with your device's port and appropriate baud rate.
# test_robot_serial('/dev/cu.usbmodem11301', 115200)


from toolbox import update_ui, CatchException, report_exception
from toolbox import write_history_to_file, promote_file_to_downloadzone
import serial
import serial.tools.list_ports
import time

class RobotController():
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.history = []

    def list_serial_ports(self):
        """ Lists serial port names """
        return [port.device for port in serial.tools.list_ports.comports()]

    def establish_connection(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for connection to stabilize
            self.history.append(f"Connection established on port {self.port}")
        except serial.SerialException as e:
            self.history.append(f"Serial error: {e}")
            raise e

    def send_test_command(self, test_command='ping'):
        try:
            if self.ser:
                self.ser.write(test_command.encode())
                response = self.ser.readline().decode().strip()
                self.history.append(f"Sent '{test_command}', received response: {response}")
        except serial.SerialException as e:
            self.history.append(f"Serial error: {e}")
            raise e

    def close_connection(self):
        if self.ser:
            self.ser.close()
            self.history.append("Serial connection closed.")

    def run_test(self):
        self.establish_connection()
        self.send_test_command()
        self.close_connection()
        return self.history

@CatchException
def test_robot_serial(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    chatbot.append(["Function plugin?", "Testing serial communication with a robot."])
    yield from update_ui(chatbot=chatbot, history=history)

    robot = RobotController('/dev/cu.usbmodem11301', 115200)
    try:
        results = robot.run_test()
        history.extend(results)
        chatbot.append(["Test Results", "\n".join(results)])
    except Exception as e:
        report_exception(chatbot, history, a="Robot Test", b=str(e))

    yield from update_ui(chatbot=chatbot, history=history)
    res = write_history_to_file(history)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(["Finished?", res])
    yield from update_ui(chatbot=chatbot, history=history)

# Main execution
if __name__ == "__main__":
    history = []
    chatbot = []  # Replace with actual chatbot object if available
    system_prompt = ""
    web_port = 8000  # Replace with actual web port if necessary
    test_robot_serial(chatbot, history, system_prompt, web_port)
