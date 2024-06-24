import time
from hl7apy.core import Message
from datetime import datetime
import socket
import random
from faker import Faker
from itertools import cycle

fake = Faker('en_AU')

# List of Australian states
australian_states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "ACT", "NT"]

# Cycle over sending applications
sending_applications = cycle(["XRGE", "SIRJ"])

# Cycle over sending facilities
sending_facility = cycle(["COMRAD", "ProMedicus"])

# Medical Insurance
pv20_choice = ["MB", "BUPA", "HCF", "NIB"]

def generate_hl7_message(msg_id, event_type="A08"):
    # Initialize the HL7 message with the ADT_A01 message type
    msg = Message("ADT_A01", version='2.3.1')

    # Populate the MSH segment with necessary fields
    msg.msh.msh_3 = next(sending_applications)  # Sending Application
    msg.msh.msh_4 = next(sending_facility)  # Sending Facility
    msg.msh.msh_5 = ""  # Receiving Application
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = f"ADT^{event_type}"
    msg.msh.msh_10 = str(random.randint(1000000000, 9999999999))  # Random numeric Message Control ID
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.3.1"
    
    # Create and populate the EVN segment
    evn = msg.add_segment("EVN")
    evn.evn_1 = event_type
    evn.evn_2 = datetime.now().strftime("%Y%m%d")
    
    # Create and populate the PID segment with patient information
    pid = msg.add_segment("PID")
    pid.pid_3 = f"TEST1{msg_id:04d}"  # Patient identifier with leading zeros
    pid.pid_5 = f"{fake.last_name()}^{fake.first_name()}"
    pid.pid_7 = fake.date_of_birth(minimum_age=0, maximum_age=90).strftime("%Y%m%d")  # Random DOB
    pid.pid_8 = random.choice(["M", "F"])  # Random gender
    pid.pid_11 = f"{fake.street_address()}^^{fake.city()}^{random.choice(australian_states)}^{fake.postcode()}^AU"  # Australian address with random state
    
    # Create and populate the NK1 segment
    nk1 = msg.add_segment("NK1")
    nk1.nk1_1 = "1"
    nk1.nk1_2 = f"{fake.last_name()}^{fake.first_name()}"
    nk1.nk1_3 = random.choice(["MTH", "FTH", "SIS", "BRO"])  # Random relationship
    nk1.nk1_5 = format_phone_number(fake.phone_number())
    
    # Create and populate the PV1 segment with patient visit information
    pv1 = msg.add_segment("PV1")
    pv1.pv1_1 = "1"
    pv1.pv1_2 = "O"
    pv1.pv1_3 = "OU"
    pv1.pv1_17 = f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."  # Random attending doctor
    pv1.pv1_19 = f"V{msg_id:04d}"  # Visit number with leading zeros
    pv1.pv1_20 = random.choice(pv20_choice)
    pv1.pv1_39 = "I^IMED"
    pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")
    
    # Create and populate the AL1 segment
    al1 = msg.add_segment("AL1")
    al1.al1_1 = "1"
    al1.al1_3 = "Peanuts"  # Allergy type
    al1.al1_5 = "RASH"  # Reaction description
    
    # Create and populate the DG1 segment
    dg1 = msg.add_segment("DG1")
    dg1.dg1_1 = "1"
    dg1.dg1_2 = "ICD10"
    dg1.dg1_3 = "E0800"  # Diagnosis code
    dg1.dg1_4 = "Diabetes Mellitus"  # Diagnosis description
    
    # Add MRG segment if event_type is A43
    if event_type == "A43":
        mrg = msg.add_segment("MRG")
        mrg.mrg_1 = f"OLD{msg_id:04d}"  # Prior Patient ID
        mrg.mrg_2 = f"OLD{msg_id:04d}^OTHER"  # Prior Alternate Patient ID
        
    return msg.to_er7()

def format_phone_number(phone_number):
    # Format the phone number to fit HL7 TN data type requirements
    return ''.join(filter(str.isdigit, phone_number))[:10]

def send_hl7_message(message, host="127.0.0.1", ports=[2577]):
    # MLLP framing
    mllp_message = f'\x0B{message}\x1C\x0D'
    
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(mllp_message.encode())
                response = s.recv(1024)
                print(f"Received from port {port}: {response.decode()}")
        except Exception as e:
            print(f"Failed to send message to port {port}: {e}")

# Generate and send HL7 messages from 1 to 5
for i in range(1, 6):
    # Randomly choose event type A08 or A43
    event_type = random.choice(["A08", "A43"])
    hl7_message = generate_hl7_message(i, event_type=event_type)
    send_hl7_message(hl7_message, ports=[2577])
    time.sleep(1)
