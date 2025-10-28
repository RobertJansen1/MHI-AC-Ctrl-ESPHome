import re

def get_dataframe_info():
    """
    Contains the data mapping from the CSV analysis.
    Each entry defines a byte, its name, the function of each bit,
    and a general explanation.
    """
    return [
        {"Byte": 0, "Name": "SB0", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 1, "Name": "SB1", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 2, "Name": "SB2", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 3, "Name": "DB0", "bits": {7: "Vanes UD", 6: "Vanes UD", 4: "Mode", 3: "Mode", 2: "Mode", 0: "Power"}, "explanation": "Bits 7,6 are part of the Vanes Up/Down control. Bits 4,3,2 define the operating mode (Auto, Cool, etc.). Bit 0 is the Power On/Off flag."},
        {"Byte": 4, "Name": "DB1", "bits": {7: "Vanes UD", 5: "Vanes UD", 4: "Vanes UD", 2: "Fan", 1: "Fan", 0: "Fan"}, "explanation": "Bits 7,5,4 are part of the Vanes Up/Down control. Bits 2,1,0 define the Fan Speed."},
        {"Byte": 5, "Name": "DB2", "bits": {}, "explanation": "The full byte represents the Temperature Setpoint."},
        {"Byte": 6, "Name": "DB3", "bits": {}, "explanation": "The full byte represents the current Room Temperature."},
        {"Byte": 7, "Name": "DB4", "bits": {}, "explanation": "The full byte represents the current Error Code."},
        {"Byte": 8, "Name": "DB5", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 9, "Name": "DB6", "bits": {7: "OpData Flag"}, "explanation": "Bit 7 is a flag to differentiate operating data types when DB9 is the same (e.g., RETURN-AIR vs OUTDOOR)."},
        {"Byte": 10, "Name": "DB7", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 11, "Name": "DB8", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 12, "Name": "DB9", "bits": {}, "explanation": "The full byte is a code that selects the type of Operating Data in bytes DB10-DB12."},
        {"Byte": 13, "Name": "DB10", "bits": {5: "OpData Type", 4: "OpData Type", 3: "OpData Val", 2: "OpData Val", 1: "OpData Val", 0: "OpData Val"}, "explanation": "Bits 5,4 often specify the data subtype. Bits 3-0 often hold a value."},
        {"Byte": 14, "Name": "DB11", "bits": {}, "explanation": "The full byte holds an 8-bit value or the Low Byte of a 16-bit value for the Operating Data specified by DB9."},
        {"Byte": 15, "Name": "DB12", "bits": {}, "explanation": "The full byte holds the High Byte of a 16-bit value for the Operating Data specified by DB9."},
        {"Byte": 16, "Name": "DB13", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 17, "Name": "DB14", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 18, "Name": "CBH", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 19, "Name": "CBL", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 20, "Name": "DB15", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 21, "Name": "DB16", "bits": {2: "Vanes L/R", 1: "Vanes L/R", 0: "Vanes L/R"}, "explanation": "Bits 2,1,0 specify the Vanes Left/Right position. (Only for frame size 33)."},
        {"Byte": 22, "Name": "DB17", "bits": {2: "3D Auto", 0: "Vanes L/R Swing"}, "explanation": "Bit 2 is the 3D Auto flag. Bit 0 is the Vanes Left/Right swing flag. (Only for frame size 33)."},
        {"Byte": 23, "Name": "DB18", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 24, "Name": "DB19", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 25, "Name": "DB20", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 26, "Name": "DB21", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 27, "Name": "DB22", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 28, "Name": "DB23", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 29, "Name": "DB24", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 30, "Name": "DB25", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 31, "Name": "DB26", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
        {"Byte": 32, "Name": "CBL2", "bits": {}, "explanation": "Not referenced in the provided code snippet."},
    ]

def parse_log_line(line):
    """Extracts the data type (MISO/MOSI) and hex values from a log line."""
    match = re.search(r'(MISO|MOSI): ([\sA-Fa-f0-9]+)', line)
    if match:
        data_type = match.group(1)
        hex_data = match.group(2).strip().split()
        # The data is often repeated in the log, so we take the first meaningful chunk.
        # A common length seems to be around 20 or 33 bytes. We'll find a logical split.
        # For now, let's assume the first 20 bytes are the primary frame for standard analysis.
        # A more robust solution could try to find the repeating pattern.
        if len(hex_data) > 20:
             # Heuristic: if data repeats, like A B C A B C, find the second A
             try:
                 second_occurrence = hex_data.index(hex_data[0], 1)
                 return data_type, hex_data[:second_occurrence]
             except ValueError:
                 pass # No repetition found
        return data_type, hex_data
    return None, None

def analyze_frame(data_type, hex_bytes, dataframe_info):
    """Analyzes the hex data and prints a detailed explanation."""
    print(f"\n--- Analyzing {data_type} Frame ---")
    print(f"Data: {' '.join(hex_bytes)}")

    for i, hex_val in enumerate(hex_bytes):
        if i >= len(dataframe_info):
            print(f"\nByte {i}: {hex_val} - No definition available in the dataframe.")
            continue

        byte_info = dataframe_info[i]
        int_val = int(hex_val, 16)
        bin_val = f"{int_val:08b}"

        print(f"\nByte {i:<2} ({byte_info['Name']}) | Hex: {hex_val} | Bin: {bin_val}")

        # Case 1: The byte has specific bit definitions
        if byte_info['bits']:
            unexplained_bits = []
            has_explained_bits = False
            for bit_pos in range(7, -1, -1):
                is_set = (int_val >> bit_pos) & 1
                if is_set:
                    description = byte_info['bits'].get(bit_pos)
                    if description:
                        print(f"  - Bit {bit_pos}: SET -> {description}")
                        has_explained_bits = True
                    else:
                        unexplained_bits.append(str(bit_pos))
            
            if unexplained_bits:
                print(f"  - Unexplained SET bits: {', '.join(unexplained_bits)}")
            elif not has_explained_bits and int_val != 0:
                 print(f"  - No specific bit definitions for set bits in this byte.")


        # Case 2: The byte has a general explanation for its value
        else:
            if "Not referenced" in byte_info['explanation']:
                print(f"  - {byte_info['explanation']}")
            else:
                print(f"  - Value: {int_val} (0x{hex_val})")
                print(f"  - Explanation: {byte_info['explanation']}")

def main():
    """Main function to run the analyzer."""
    dataframe_info = get_dataframe_info()
    
    log_input = """
[14:42:32][D][mhi_ac_ctrl_core:321]: MISO: A9 05 47 AA 8F B8 FF 00 00 80 00 00 F1 F7 FF FF 0F 00 08 5A A9 05 47 AA 8F B8 FF 00 00 80 00 00 F1 
[14:42:33][D][mhi_ac_ctrl_core:322]: MOSI: 6D 80 04 AA 8F B8 92 00 00 88 00 FF FF FF FF FF 00 00 08 F7 6D 80 04 AA 8F B8 92 00 00 88 00 FF FF 
[14:42:37][D][mhi_ac_ctrl_core:321]: MISO: A9 00 07 AA 8F B8 FF 00 00 80 00 00 FF FF FF FF 0F 04 08 2F A9 00 07 AA 8F B8 FF 00 00 80 00 00 FF 
[14:42:37][D][mhi_ac_ctrl_core:322]: MOSI: 6D 80 04 AA 8F B8 92 00 00 88 00 FF FF FF FF FF 00 00 08 F7 6D 80 04 AA 8F B8 92 00 00 88 00 FF FF 
"""
    
    print("Analyzing provided log data...")
    for line in log_input.strip().split('\n'):
        data_type, hex_bytes = parse_log_line(line)
        if data_type and hex_bytes:
            analyze_frame(data_type, hex_bytes, dataframe_info)
            print("-" * 50)

    print("\n\nYou can now paste a single MISO or MOSI log line to analyze it.")
    print("Press Ctrl+C to exit.")
    try:
        while True:
            user_line = input("\nEnter log line: ")
            if user_line:
                data_type, hex_bytes = parse_log_line(user_line)
                if data_type and hex_bytes:
                    analyze_frame(data_type, hex_bytes, dataframe_info)
                else:
                    print("Could not parse the line. Please ensure it starts with 'MISO:' or 'MOSI:'.")
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    main()
