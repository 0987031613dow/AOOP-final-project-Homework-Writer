import svgwrite
from svgpathtools import svg2paths, Line
import serial
import time
import keyboard
import argparse
import cairosvg

# Function to generate SVG from text
def text_to_svg(text, filename='out.svg', font_size=20):
    # dwg = svgwrite.Drawing(filename, profile='tiny')
    dwg = svgwrite.Drawing(filename, size=('50mm', '50mm'), profile='tiny')

    dwg.add(dwg.text(text, insert=(0, font_size), font_size=font_size))
    dwg.save()

def convert_text_to_path_in_svg(input_svg, output_svg):
    """
    Convert text elements in an SVG file to path elements.

    Args:
    input_svg (str): Path to the input SVG file.
    output_svg (str): Path to the output SVG file with text converted to paths.
    """
    # Convert SVG with text to SVG with paths
    cairosvg.svg2svg(url=input_svg, write_to=output_svg)

# Function to convert SVG to G-code
def svg_to_gcode(svg_filename, feedrate=1000):
    """
    Convert an SVG file to G-code.

    Args:
    svg_filename (str): Filename of the SVG file to be converted.
    feedrate (int, optional): Feed rate for the G-code. Defaults to 1000.

    Returns:
    list: A list of G-code commands.
    """
    print("svg_filename = ",svg_filename)
    # Load the paths from the SVG file
    paths, b = svg2paths(svg_filename)
    print("b = ",b)

    # Initialize an empty list for G-code commands
    gcode = []
    print("paths = ",paths)
    # Iterate over each path in the SVG
    for path in paths:
        # Add G-code command to raise the pen/tool
        gcode.append('M3 S40')  # Modify as needed for your machine

        # Iterate over each segment in the path
        for segment in path:
            # Check if the segment is a line
            if isinstance(segment, Line):
                # Get the start and end points of the line
                start = segment.start
                end = segment.end

                # Move to the start position
                gcode.append(f'G00 X{start.real:.3f} Y{start.imag:.3f} F{feedrate}')
                gcode.append('M5')  # Lower the pen/tool (modify as needed for your machine
                # Draw the line to the end position
                gcode.append(f'G01 X{end.real:.3f} Y{end.imag:.3f} F{feedrate}')

    return gcode

if __name__ == '__main__':
    # Main program
    parser = argparse.ArgumentParser(description='Text to G-code Generator')
    parser.add_argument('text', type=str, help='Text to convert into G-code')
    args = parser.parse_args()

    # Generate SVG from text
    svg_filename = 'out.svg'
    svg_file1name = 'out1.svg'
    text_to_svg(args.text, svg_filename)
    convert_text_to_path_in_svg(svg_filename, svg_file1name)

    # Convert SVG to G-code
    gcode = svg_to_gcode(svg_file1name)
    print("gcode = ",gcode)
    with open('out1.gcode', 'w') as file:
        for command in gcode:
            file.write(command + '\n')

    #####################################################################
    # Step 5: Search for Arduino board
    arduino_ports = [
        p.device for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description or 'VID:PID' in p.description or 'tty' in p.description
    ]
    if not arduino_ports:
        raise IOError("No Arduino board found.")

    port = arduino_ports[0]  # Use the first Arduino board found
    baud_rate = 115200
    # Establish serial connection with the pen plotter
    ser = serial.Serial(port, baud_rate, timeout=1)
    # Wait for the connection to stabilize
    time.sleep(2)

    # Stop sending flag
    stop_sending = False
    def stop_sending_callback(event):
        global stop_sending
        stop_sending = True
    keyboard.on_press_key('a', stop_sending_callback)

    # Send G-code
    print("Sending G-code to device. Press 'a' to abort.")
    for command in gcode:
        if stop_sending:
            print("G-code sending aborted by user.")
            break
        ser.write(command.encode() + b'\n')
        while True:
            response = ser.readline().decode().strip()
            if response == 'ok':
                break

    # Close serial connection
    ser.close()
    print("G-code transmission complete.")
