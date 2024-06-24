import time
from hl7apy.core import Message
from datetime import datetime
import socket
import random
from faker import Faker
import string
from itertools import cycle
import os,csv

fake = Faker('en_AU')

# List of common medical procedures or observations
medical_procedures = [
    "CTA^CT ABDOMEN AND PELVIS",
    "CTANGIO^CT ANGIOGRAM",
    "CTLAR^CT RIGHT ANKLE",
    "CTCARDIAC^CT CARDIAC",
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

# cycle over sending applications
sending_applications = cycle(["XRGE", "SIRJ"])

# cycle over sending facility
sending_facility = cycle(["COMRAD", "ProMedicus"])

# Cycle through the list of order control codes
order_control_codes = cycle(["SC", "IP", "HD", "CM", "CA"]) # use CM status # PSOne uses "IP"

# Entering Organization ORC 17.1
site_code = cycle([
    "Bairnsdale", "Collins Street Medical Imaging", "Box Hill",
    "Castle Hill", "Chatswood", "Ipswich", "Fortitude Valley",
    "Hobart Private Hospital", "Latrobe Regional Hospital", "West Gippsland",
    "Yarrawonga", "Launcheston General Hospital"
])

# Medical Insurance
pv20_choice = ["MB", "BUPA", "HCF", "NIB"]

#modalities 
modalities = cycle(["CT", "MR", "US", "XA","DEXA"])

def generate_random_numeric(length=8):
    """Generate a random numeric string of given length."""
    return ''.join(random.choices(string.digits, k=length))

def load_obr5_values_from_csv(file_path):
    """Load OBR-5 values from a CSV file."""
    obr5_values = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            obr5_values.append(row['OBR-5'])
    return obr5_values

def generate_hl7_message(msg_id,obr5_value): # added new parameter read over csv file
    # Initialize the HL7 message with the ORM_O01 message type
    msg = Message("ORM_O01")

    # Populate the MSH segment with necessary fields
    msg.msh.msh_3 = next(sending_applications)  # Sending Application
    msg.msh.msh_4 = next(sending_facility)  # Sending Facility
    msg.msh.msh_5 = ""
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
    pv1.pv1_3 = "OU"
    pv1.pv1_17 = f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."  # Random attending doctor
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
    orc.orc_12 = f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."  
    orc.orc_14 = f"{random.randint(10000, 99999)}^PH"
    orc.orc_17 = f"IMED Radiology - ^{next(site_code)}^[IMED-IT]"

    # Create and populate the OBR segment with observation request information
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = placer_order_number  # Placer order number (random numeric)
    obr.obr_3 = filler_order_number  # Filler order number (random numeric)
    obr.obr_4 = random.choice(medical_procedures)  # Random Universal Service Identifier
    obr.obr_5 = obr5_value  # OBR value in csv
    obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_10 = ""
    obr.obr_16 = f"{random.randint(10000, 99999)}^{fake.last_name()}^{fake.first_name()}^MD^Dr."  
    obr.obr_24 = next(modalities ) # Random modality
    obr.obr_25 = ""
    obr.obr_31 = random.choice(clinical_reasons)  # Random clinically relevant reason for study

    return msg.to_er7()

def send_hl7_message(message, host="127.0.0.1", ports=[2575, 2576]):
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

def save_message_to_file(message, folder="output_messages"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filename = os.path.join(folder, f"message_{datetime.now().strftime('%Y%m%d%H%M%S')}.hl7")
    with open(filename, 'w') as file:
        file.write(message)
                      
if __name__ == "__main__":
    num_updates = 4  # Number of times to update and resend the message
    num_patients = 2  # Number of different patients to send messages for
    update_interval = 2  # Interval in seconds between sending updates
    
    obr5_values = load_obr5_values_from_csv("obr5_values.csv")  # Load OBR-5 values from CSV
    obr5_cycle = cycle(obr5_values)  # Cycle through the OBR-5 values


    for patient_id in range(1, num_patients + 1):
        original_obr5 = next(obr5_cycle)  # Get the next OBR-5 value
        # Generate the original HL7 message
        original_hl7_message = generate_hl7_message(patient_id,original_obr5)
        
        # Save the original HL7 message to a file
        save_message_to_file(original_hl7_message)
        
        # Send the original HL7 message
        send_hl7_message(original_hl7_message, ports=[2575, 2576])

        # Extract ORC segment from the original message
        original_segments = original_hl7_message.split('\r')
        original_orc_segment = [segment for segment in original_segments if segment.startswith('ORC')][0]

        for update in range(1,num_updates+1):
            # Generate a new ORC-5 value
            new_orc5 = next(order_control_codes)
            
            # Update the ORC-5 field in the ORC segment
            orc_fields = original_orc_segment.split('|')
            orc_fields[5] = new_orc5  # ORC-5 is the fifth field in the ORC segment
            updated_orc_segment = '|'.join(orc_fields)

            # Replace the original ORC segment with the updated ORC segment in the message
            updated_hl7_message = original_hl7_message.replace(original_orc_segment, updated_orc_segment, 1)
            
                # Save the updated HL7 message to a file
            save_message_to_file(updated_hl7_message)

            # Send the updated HL7 message
            send_hl7_message(updated_hl7_message, ports=[2575, 2576])
            
            # Wait for the specified interval before sending the next update
            time.sleep(update_interval)
            
