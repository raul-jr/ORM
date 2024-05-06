"""
This script creates an HL7 ORM_O01 message using the hl7apy library. The ORM_O01 message type is used for 
order entry and consists of several segments including the Message Header (MSH), Patient Identification (PID),
Patient Visit (PV1), Common Order (ORC), and Observation Request (OBR). Each segment is populated with 
relevant information as per the requirements of a typical medical imaging order, such as an MRI scan.
"""

from hl7apy.core import Message
from datetime import datetime


# Initialize the HL7 message with the ORM_O01 message type
msg = Message("ORM_O01")

# Populate the MSH segment with necessary fields
msg.msh.msh_3 = "COMRAD"  # Sending application
msg.msh.msh_4 = ""  # Sending facility
msg.msh.msh_5 = "ReceivingApp"  # Receiving application
msg.msh.msh_6 = "ReceivingFacility"  # Receiving facility
msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")  # Date/time of message
msg.msh.msh_9 = "ORM^O01"  # Message type
msg.msh.msh_10 = "MSGID12317"  # Message control ID
msg.msh.msh_11 = "P"  # Processing ID
msg.msh.msh_12 = "2.4"  # Version ID
#print(msg.to_er7())

# Create and populate the PID segment with patient information
pid = msg.add_segment("PID")
pid.pid_3 = "TEST10017"  # Patient identifier
pid.pid_5 = "VR^Testing17"  # Patient name
pid.pid_7 = "19900101"  # Date of birth
pid.pid_8 = "F"  # Sex
pid.pid_11 = "123 Main St.^^Anytown^NSW^12345^AU"  # Patient address
#print(pid.to_er7())

# Create and populate the PV1 segment with patient visit information
pv1 = msg.add_segment("PV1")
pv1.pv1_1 = "1"  # Set ID
pv1.pv1_2 = "O"  # Patient class
pv1.pv1_3 = "PH"  # Assigned patient location
pv1.pv1_17 = "12340^Smith^John^MD^Dr."  # Attending doctor
pv1.pv1_19 = "V0017"  # Visit number
pv1.pv1_20 = "MB"  # Financial class
pv1.pv1_39 = "I^IMED"  # Diet type
pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")  # Admit date/time
#print(pv1.to_er7())

# Create and populate the ORC segment with common order information
orc = msg.add_segment("ORC")
orc.orc_1 = "CM"  # Order control
orc.orc_2 = "TEST-10017-XR"  # Placer order number
orc.orc_3 = "VR0017"  # Filler order number
orc.orc_5 = "CM"  # Order status
orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")  # Date/time of transaction
orc.orc_12 = "12345^IMED CLINIC^^^"  # Ordering provider
orc.orc_14 = "0123345^PH"  # Call back phone number
orc.orc_17 = "IMED"  # Entering organization
##print(orc.to_er7())

# Create and populate the OBR segment with observation request information
obr = msg.add_segment("OBR")
obr.obr_1 = "1"  # Set ID - OBR
obr.obr_2 = "TEST-10017-XR"      # Placer order number
obr.obr_3 = "VR0017"    # Filler order number
obr.obr_4 = "XRSPINE^DHP-XR C SPINE"# Universal Service ID
obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")  # Requested date/time
obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")  # Observation date/time
obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")  # Observation end date/time
obr.obr_10 = "COMRAD"  # Collector identifier
obr.obr_16 = "12345^Smith^John^MD^Dr."  # Ordering provider
obr.obr_31 = "accident"  # Reason for study
#obr.obr_34 = "TEST&TEST&12234"  # Technician
#obr.obr_44 = "USA"  # Procedure code
#print(obr.to_er7() + '\r')


# Open a file in write mode
with open("hl7_message.hl7", "w") as file:
    # Write the complete HL7 message to the file
    file.write(msg.to_er7())


'''
# Open a file in write mode
with open("hl7_message.hl7", "w") as file:
    # Write the HL7 message segments to the file
    file.write(msg.to_er7())
    file.write(pid.to_er7())
    file.write(pv1.to_er7())
    file.write(orc.to_er7())
    file.write(obr.to_er7())
'''

