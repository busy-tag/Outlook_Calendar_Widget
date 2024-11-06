import time
import serial
import serial.tools.list_ports

def open_serial_connection(port='COM4', baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        return ser
    except serial.SerialException as e:
        print(f"Failed to open serial connection: {e}")
        return None

def send_serial_command(ser, command):
    try:
        if ser and ser.is_open:
            ser.write((command).encode())
            ser.flush()
            response = ser.readline().decode().strip()            
            return response
        else:
            print("Serial connection is not open.")
            return None
    except serial.SerialException as e:
        print(f"Failed to send command: {e}")
        return None

def close_serial_connection(ser):
    if ser and ser.is_open:
        ser.close()

def find_busy_tag_device():
    ports = serial.tools.list_ports.comports()
    for port_info in ports:
        port = port_info.device
        try:       
            ser = serial.Serial(port, baudrate=115200, timeout=1, write_timeout=1)             
            ser.flushInput()
            ser.flushOutput()
            ser.write(b'AT+GDN\r\n')
            response = ser.readline().decode('utf-8').strip()  
            
            if response.startswith("+DN:busytag-"):
                print(f"Connected to Busy Tag device on {port}")
                ser.close()
                return port
            else:
                print(f"No Busy Tag response on port: {port}")
            
            ser.close()
        
        except serial.SerialTimeoutException:
            print(f"Timeout on port {port}, moving to the next port.")
            continue
        
        except (serial.SerialException, UnicodeDecodeError, OSError) as e:
            print(f"Error on port {port}: {e}")
            continue
        
        except Exception as e:
            print(f"Unexpected error on port {port}: {e}")
            continue
        
        finally:
            try:
                if ser.is_open:
                    ser.close()
            except:
                pass

    print("No Busy Tag device found.")
    return None