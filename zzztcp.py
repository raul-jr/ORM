from hl7apy.core import Message
from datetime import datetime
import socket

def generate_hl7_message(msg_id):
    # Initialize the HL7 message with the ORM_O01 message type
    msg = Message("ORM_O01")

    # Populate the MSH segment with necessary fields
    msg.msh.msh_3 = "COMRAD"
    msg.msh.msh_5 = "ReceivingApp"
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = "ORM^O01"
    msg.msh.msh_10 = f"MSGID{msg_id:04d}"  # Unique Message control ID with leading zeros
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.4"

    # Create and populate the PID segment with patient information
    pid = msg.add_segment("PID")
    pid.pid_3 = f"TEST1{msg_id:04d}"  # Patient identifier with leading zeros
    pid.pid_5 = f"VR^Testing{msg_id:-1d}"
    pid.pid_7 = "19900101"
    pid.pid_8 = "F"
    pid.pid_11 = "123 Main St.^^Anytown^NSW^12345^AU"

    # Create and populate the PV1 segment with patient visit information
    pv1 = msg.add_segment("PV1")
    pv1.pv1_1 = "1"
    pv1.pv1_2 = "O"
    pv1.pv1_3 = "PH"
    pv1.pv1_17 = "12340^Smith^John^MD^Dr."
    pv1.pv1_19 = f"V{msg_id:04d}"  # Visit number with leading zeros
    pv1.pv1_20 = "MB"
    pv1.pv1_39 = "I^IMED"
    pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")

    # Create and populate the ORC segment with common order information
    orc = msg.add_segment("ORC")
    orc.orc_1 = "CM"
    orc.orc_2 = f"TEST-1{msg_id:04d}-MRI"  # Placer order number with leading zeros
    orc.orc_3 = f"VR{msg_id:04d}"  # Filler order number with leading zeros
    orc.orc_5 = "CM"
    orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")
    orc.orc_12 = "12345^IMED CLINIC^^^"
    orc.orc_14 = "0123345^PH"
    orc.orc_17 = "IMED"

    # Create and populate the OBR segment with observation request information
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = f"TEST-1{msg_id:04d}-MRI"
    obr.obr_3 = f"VR{msg_id:04d}"
    obr.obr_4 = "MRI^NR PELVIS"
    obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_10 = "COMRAD"
    obr.obr_16 = "12345^Smith^John^MD^Dr."
    # obr.obr_31 = ""

    return msg.to_er7()

def send_hl7_message(message, host="127.0.0.1", port=2575):
    # MLLP framing
    mllp_message = f'\x0B{message}\x1C\x0D'
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(mllp_message.encode())
        
        # Optionally, receive the response from the server
        response = s.recv(1024)
        print("Received", response.decode())

# Generate and send HL7 messages from 1 to 9
for i in range(1, 10):
    hl7_message = generate_hl7_message(i)
    send_hl7_message(hl7_message)
