from hl7apy.core import Message
from hl7apy.parser import parse_message
from datetime import datetime
import socket
import random
from faker import Faker
import string

fake = Faker('en_AU')

# List of common medical procedures or observations
medical_procedures = [
    "XRAY^Chest X-Ray",
    "CT^CT Scan",
    "MRI^MRI Brain",
    "US^Ultrasound Abdomen",
]

# List of common clinical reasons for study
clinical_reasons = [
    "Chronic chest pain",
    "Abdominal pain",
    "Head injury",
    "Routine check-up",
    "High blood pressure",
    "Abnormal lab results",
    "Follow-up study",
    "Pre-operative evaluation",
    "Shortness of breath",
    "Persistent cough"
]

# List of Australian states
australian_states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "ACT", "NT"]

# Medical Insurance
pv20_choice = ["MB", "BUPA", "HCF", "NIB"]

def generate_random_numeric(length=8):
    """Generate a random numeric string of given length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_base_hl7_message(msg_id):
    # Initialize the HL7 message with the ORM_O01 message type
    msg = Message("ORM_O01")

    # Populate the MSH segment with necessary fields
    msg.msh.msh_3 = random.choice(["COMRAD", "VISAGE"])
    msg.msh.msh_5 = "ReceivingApp"
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = "ORM^O01"
    msg.msh.msh_10 = str(random.randint(1000000000, 9999999999))  # Random numeric Message Control ID
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.4"

    # Create and populate the PID segment with patient information
    pid = msg.add_segment("PID")
    pid.pid_3 = f"TEST1{msg_id:04d}"  # Patient identifier with leading zeros
    pid.pid_5 = f"{fake.last_name()}^{fake.first_name()}"
    pid.pid_7 = fake.date_of_birth(minimum_age=0, maximum_age=90).strftime("%Y%m%d")  # Random DOB
    pid.pid_8 = random.choice(["M", "F"])  # Random gender
    pid.pid_11 = f"{fake.street_address()}^^{fake.city()}^{random.choice(australian_states)}^{fake.postcode()}^AU"  # Australian address with random state

    # Create and populate the PV1 segment with patient visit information
    pv1 = msg.add_segment("PV1")
    pv1.pv1_1 = "1"
    pv1.pv1_2 = "O"
    pv1.pv1_3 = "PH"
    pv1.pv1_17 = f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."  # Random attending doctor
    pv1.pv1_19 = f"V{msg_id:04d}"  # Visit number with leading zeros
    pv1.pv1_20 = random.choice(pv20_choice)
    pv1.pv1_39 = "I^IMED"
    pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")

    return msg
def add_order_segments(msg, order_control_code):
    # Create a random numeric string for ORC-2 and OBR-2, and ORC-3 and OBR-3
    placer_order_number = generate_random_numeric()
    filler_order_number = generate_random_numeric()

    # Create and populate the ORC segment with common order information
    orc = msg.add_segment("ORC")
    orc.orc_1 = ""
    orc.orc_2 = placer_order_number  # Placer order number (random numeric)
    orc.orc_3 = filler_order_number  # Filler order number (random numeric)
    orc.orc_5 = order_control_code  # Sequential order control code
    orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")
    orc.orc_12 = "12345^IMED CLINIC^^^"
    orc.orc_14 = f"{random.randint(10000, 99999)}^PH"
    orc.orc_17 = "IMED"

    # Create and populate the OBR segment with observation request information
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = placer_order_number  # Placer order number (random numeric)
    obr.obr_3 = filler_order_number  # Filler order number (random numeric)
    obr.obr_4 = random.choice(medical_procedures)  # Random Universal Service Identifier
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_16 = "12345^Smith^John^MD^Dr."
    obr.obr_31 = random.choice(clinical_reasons)  # Random clinically relevant reason for study

    return msg

"""def add_order_segments(msg, order_control_code):
    # Create a random numeric string for ORC-2 and OBR-2, and ORC-3 and OBR-3
    placer_order_number = generate_random_numeric()
    filler_order_number = generate_random_numeric()

    # Create and populate the ORC segment with common order information
    orc = msg.add_segment("ORC")
    orc.orc_1 = ""
    orc.orc_2 = placer_order_number  # Placer order number (random numeric)
    orc.orc_3 = filler_order_number  # Filler order number (random numeric)
    orc.orc_5 = order_control_code  # Sequential order control code
    orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")
    orc.orc_12 = "12345^IMED CLINIC^^^"
    orc.orc_14 = f"{random.randint(10000, 99999)}^PH"
    orc.orc_17 = "IMED"

    # Create and populate the OBR segment with observation request information
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = placer_order_number  # Placer order number (random numeric)
    obr.obr_3 = filler_order_number  # Filler order number (random numeric)
    obr.obr_4 = random.choice(medical_procedures)  # Random Universal Service Identifier
    obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_10 = "COMRAD"
    obr.obr_16 = "12345^Smith^John^MD^Dr."
    obr.obr_31 = random.choice(clinical_reasons)  # Random clinically relevant reason for study
"""
    

def send_hl7_message(message, host="127.0.0.1", ports=[2575, 2576]):
    # MLLP framing
    mllp_message = f'\x0B{message}\x1C\x0D'
    
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(mllp_message.encode())
            
            # Optionally, receive the response from the server
            response = s.recv(1024)
            print(f"Received from port {port}: {response.decode()}")

# Generate the original HL7 message for a single patient
base_msg = generate_base_hl7_message(1)  # Assuming patient ID 1 for this example


# Get the ER7 string representation of the base message
er7_base_msg = base_msg.to_er7()



# Resend the original message with updated ORC-5 values
"""for order_control_code in ["SC", "IP", "OC", "HD"]:
    msg = parse_message(er7_base_msg)  # Create a new message instance from ER7 string
    add_order_segments(msg, order_control_code)  # Add order segments with specific ORC-5 value
    hl7_message = msg.to_er7()  # Convert the message to HL7 ER7 format
    send_hl7_message(hl7_message, ports=[2575, 2576])"""
# Resend the original message with updated ORC-5 values
for order_control_code in ["SC", "IP", "OC", "HD"]:
    msg = parse_message(er7_base_msg)  # Create a new message instance from ER7 string
    
    # Update ORC-5 value
    msg.ORC.ORC_5 = order_control_code
    
    hl7_message = msg.to_er7()  # Convert the message to HL7 ER7 format
    send_hl7_message(hl7_message, ports=[2575, 2576])