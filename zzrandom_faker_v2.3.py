from hl7apy.core import Message
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

# Order control codes
order_control_codes = ["IP", "OC"]

# Medical Insurance
pv20_choice = ["MB", "BUPA", "HCF", "NIB"]

def generate_random_numeric(length=8):
    """Generate a random numeric string of given length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_hl7_message(patient_data, visit_data, order_data, orc_5):
    # Initialize the HL7 message with the ORM_O01 message type
    msg = Message("ORM_O01")

    # Populate the MSH segment with necessary fields
    msg.msh.msh_3 = patient_data['msh_3']
    msg.msh.msh_5 = "ReceivingApp"
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = "ORM^O01"
    msg.msh.msh_10 = str(random.randint(1000000000, 9999999999))  # Random numeric Message Control ID
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.4"

    # Create and populate the PID segment with patient information
    pid = msg.add_segment("PID")
    pid.pid_3 = patient_data['pid_3']
    pid.pid_5 = patient_data['pid_5']
    pid.pid_7 = patient_data['pid_7']
    pid.pid_8 = patient_data['pid_8']
    pid.pid_11 = patient_data['pid_11']

    # Create and populate the PV1 segment with patient visit information
    pv1 = msg.add_segment("PV1")
    pv1.pv1_1 = "1"
    pv1.pv1_2 = "O"
    pv1.pv1_3 = "PH"
    pv1.pv1_17 = visit_data['attending_doctor']
    pv1.pv1_19 = visit_data['pv1_19']
    pv1.pv1_20 = visit_data['pv1_20']
    pv1.pv1_39 = "I^IMED"
    pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")

    # Create and populate the ORC segment with common order information
    orc = msg.add_segment("ORC")
    orc.orc_1 = ""
    orc.orc_2 = order_data['placer_order_number']
    orc.orc_3 = order_data['filler_order_number']
    orc.orc_5 = orc_5
    orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")
    orc.orc_12 = "12345^IMED CLINIC^^^"
    orc.orc_14 = order_data['orc_14']
    orc.orc_17 = "IMED"

    # Create and populate the OBR segment with observation request information
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = order_data['placer_order_number']
    obr.obr_3 = order_data['filler_order_number']
    obr.obr_4 = order_data['obr_4']
    obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_10 = ""
    obr.obr_16 = visit_data['attending_doctor']
    obr.obr_31 = order_data['obr_31']

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

# Generate and send HL7 messages for each patient in sequence with SC, IP, OC, HD
num_patients = 24  # Total number of patients
interval = 6  # Number of patients per control code

patient_data_list = []
visit_data_list = []
order_data_list = []

for i in range(1, num_patients + 1):
    patient_data = {
        "msh_3": random.choice(["COMRAD", "ProMedicus"]),
        "pid_3": f"TEST1{i:04d}",
        "pid_5": f"{fake.last_name()}^{fake.first_name()}",
        "pid_7": fake.date_of_birth(minimum_age=0, maximum_age=90).strftime("%Y%m%d"),
        "pid_8": random.choice(["M", "F"]),
        "pid_11": f"{fake.street_address()}^^{fake.city()}^{random.choice(australian_states)}^{fake.postcode()}^AU"
    }
    attending_doctor = f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."
    visit_data = {
        "attending_doctor": attending_doctor,
        "pv1_19": f"V{i:04d}",
        "pv1_20": random.choice(pv20_choice),
    }
    placer_order_number = generate_random_numeric()
    filler_order_number = generate_random_numeric()
    order_data = {
        "placer_order_number": placer_order_number,
        "filler_order_number": filler_order_number,
        "orc_14": f"{random.randint(10000, 99999)}^PH",
        "obr_4": random.choice(medical_procedures),
        "obr_31": random.choice(clinical_reasons)
    }

    patient_data_list.append(patient_data)
    visit_data_list.append(visit_data)
    order_data_list.append(order_data)

# Send messages in intervals of 6 patients with the same control code
for idx, (patient_data, visit_data, order_data) in enumerate(zip(patient_data_list, visit_data_list, order_data_list)):
    orc_5 = order_control_codes[(idx // interval) % 2]  # Rotating between "IP" and "OC"
    hl7_message = generate_hl7_message(patient_data, visit_data, order_data, orc_5)
    send_hl7_message(hl7_message, ports=[2575, 2576])
