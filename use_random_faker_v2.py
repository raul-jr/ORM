from hl7apy.core import Message
from datetime import datetime
import socket
import random
from faker import Faker
import string
from itertools import cycle

fake = Faker('en_AU')

# List of common medical procedures or observations
medical_procedures = [
"CTA^CT ABDOMEN AND PELVIS",
"CTANGIO^CT ANGIOGRAM",
"CTLAR^CT RIGHT ANKLE",
"CTCARDIAC^CT CARDIAC"
"DEXASC^DEXA",
"MRHBCN^MRI BRAIN",
"MRNRKL^MRI LEFT KNEE",
"MRI^MRI NR PELVIS",
"MRSBF^MRI FOR FISTULISING PERIANAL",
"CTNECKW^CT PARORTID AND NECK",
"USA^US ABDOMEN",
"USACHILLES^US LEFT ACHILLES",
"USNUCHA^US NUCHAL TRANSLUCENCY",
"USPREGLV2^US PREGNANCY LV2 2O WEEKS",
"XRCHESTW^XR CHEST",
"XRSPINE^XR C SPINE"
    
]

# List of common clinical reasons for study
clinical_reasons = [
    "Chronic chest pain",
    "Abdominal pain",
    "Head injury",
    "Routine check-up",
    "High blood pressure",
    "Sport injury shoulder",
    "Follow-up study",
    "Pre-operative evaluation",
    "Shortness of breath",
    "Persistent cough",
    "Car Accident"
]

# List of Australian states
australian_states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "ACT", "NT"]

# Cycle through the list of order control codes
order_control_codes = cycle(["IP"])

#Medical Insurance
pv20_choice = ["MB","BUPA","HCF","NIB"]
# Random attending doctor
attending_doctor=f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."  

def generate_random_numeric(length=8):
    """Generate a random numeric string of given length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_hl7_message(msg_id):
    # Initialize the HL7 message with the ORM_O01 message type
    msg = Message("ORM_O01")

    # Populate the MSH segment with necessary fields
    msg.msh.msh_3 = "SIRJ" # Sending Application
    msg.msh.msh_4 = random.choice (["COMRAD","ProMedicus"])
    msg.msh.msh_5 = "SmartWorklist"
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = "ORM^O01"
    msg.msh.msh_10 = str(random.randint(1000000000, 9999999999))  # Random numeric Message Control ID
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.3.1"

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
    pv1.pv1_17 = attending_doctor #f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."  # Random attending doctor
    pv1.pv1_19 = f"V{msg_id:04d}"  # Visit number with leading zeros
    pv1.pv1_20 = random.choice(pv20_choice)
    pv1.pv1_39 = "I^IMED"
    pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")

    # Create a random numeric string for ORC-2 and OBR-2, and ORC-3 and OBR-3
    placer_order_number = generate_random_numeric()
    filler_order_number = generate_random_numeric()

    # Create and populate the ORC segment with common order information
    orc = msg.add_segment("ORC")
    orc.orc_1 = ""
    orc.orc_2 = placer_order_number  # Placer order number (random numeric)
    orc.orc_3 = filler_order_number  # Filler order number (random numeric)
    orc.orc_5 = next(order_control_codes)  # Sequential order control code
    orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")
    orc.orc_12 = attending_doctor
    orc.orc_14 = f"{random.randint(10000, 99999)}^PH"
    orc.orc_17 = "IMED Radiology"

    # Create and populate the OBR segment with observation request information
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = placer_order_number  # Placer order number (random numeric)
    obr.obr_3 = filler_order_number  # Filler order number (random numeric)
    obr.obr_4 = random.choice(medical_procedures)  # Random Universal Service Identifier
    obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_10 = ""
    obr.obr_16 = attending_doctor
    obr.obr_31 = random.choice(clinical_reasons ) # Random clinically relevant reason for study

    return msg.to_er7()

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

# Generate and send HL7 messages from 1 to 9
for i in range(1, 6):
    hl7_message = generate_hl7_message(i)
    send_hl7_message(hl7_message, ports=[2575, 2576])
