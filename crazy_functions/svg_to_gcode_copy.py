from toolbox import update_ui, CatchException, report_exception
from toolbox import write_history_to_file, promote_file_to_downloadzone

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


@CatchException
def txt2svg2gcode(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os
    chatbot.append([
        "函數插件功能？",
        "將文本轉換為sgv再轉換為gcode。函數插件貢獻者: Brian, Dow"])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    try:
        import svgwrite,serial, time, keyboard, argparse, cairosvg
        from svgpathtools import svg2paths, Line
    except:
        report_exception(chatbot, history, 
                         a = f"解析項目: {txt}", 
            b = f"導入軟體依賴失敗。使用該模塊需要額外依賴，安裝方法```pip install --upgrade svgwrite svgpathtools serial keyboard cairosvg```。")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    history = []

    if txt == "": 
        txt = '空空如也的項目欄'
        report_exception(chatbot, history, a = f"解析項目: {txt}", b = f"請輸入文字。")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面   
    else:
        svg_txt = txt
        report_exception(chatbot, history, a = f"開始轉換 {txt}成為svg檔", b = f"開始轉換。")
        yield from update_ui(chatbot=chatbot, history=history)

     # Generate SVG from text
    svg_filename = 'out.svg'
    svg_file1name = 'out1.svg'
    f1 = 'haha.png'
    text_to_svg(svg_txt, svg_filename)
    convert_text_to_path_in_svg(svg_filename, svg_file1name)
    with open(svg_file1name, 'r') as file:
        svg_content = file.read()
        print("svg_content = ",svg_content)
        print("stop")

    chatbot.append( 
        [f"轉換 {txt}成為svg檔",f"""可以到{svg_file1name}查看svg檔案。"""
    ])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 界面更新
    # chatbot.append( 
    #     ["轉換成功",f"""svg檔預覽: <br/><div style="text-align:center;"><img src="{f1}" alt="SVG Image"></div>"""
    # ])
    # yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 界面更新

    # Convert SVG to G-code
    gcode = svg_to_gcode(svg_file1name)
    # print("gcode = ",gcode)
    with open('out1.gcode', 'w') as file:
        for command in gcode:
            file.write(command + '\n')


    report_exception(chatbot, history, a = f"解析項目: {txt}", b = f"轉換成功，請查看 out1.gcode 文件。")
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面   










    


# if __name__ == '__main__':
#     # Main program
#     parser = argparse.ArgumentParser(description='Text to G-code Generator')
#     parser.add_argument('text', type=str, help='Text to convert into G-code')
#     args = parser.parse_args()

#     # Generate SVG from text
#     svg_filename = 'out.svg'
#     svg_file1name = 'out1.svg'
#     text_to_svg(args.text, svg_filename)
#     convert_text_to_path_in_svg(svg_filename, svg_file1name)

#     # Convert SVG to G-code
#     gcode = svg_to_gcode(svg_file1name)
#     print("gcode = ",gcode)
#     with open('out1.gcode', 'w') as file:
#         for command in gcode:
#             file.write(command + '\n')

#     #####################################################################
#     # Step 5: Search for Arduino board
#     arduino_ports = [
#         p.device for p in serial.tools.list_ports.comports()
#         if 'Arduino' in p.description or 'VID:PID' in p.description or 'tty' in p.description
#     ]
#     if not arduino_ports:
#         raise IOError("No Arduino board found.")

#     port = arduino_ports[0]  # Use the first Arduino board found
#     baud_rate = 115200
#     # Establish serial connection with the pen plotter
#     ser = serial.Serial(port, baud_rate, timeout=1)
#     # Wait for the connection to stabilize
#     time.sleep(2)

#     # Stop sending flag
#     stop_sending = False
#     def stop_sending_callback(event):
#         global stop_sending
#         stop_sending = True
#     keyboard.on_press_key('a', stop_sending_callback)

#     # Send G-code
#     print("Sending G-code to device. Press 'a' to abort.")
#     for command in gcode:
#         if stop_sending:
#             print("G-code sending aborted by user.")
#             break
#         ser.write(command.encode() + b'\n')
#         while True:
#             response = ser.readline().decode().strip()
#             if response == 'ok':
#                 break

#     # Close serial connection
#     ser.close()
#     print("G-code transmission complete.")
