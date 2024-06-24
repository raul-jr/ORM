from hl7apy.core import Message
from datetime import datetime

def create_hl7_orm_message():
    """
    Creates an ORM HL7 message for ordering radiology exams.
    """
    msg = Message("ORM_O01", version="2.4")
    current_time = datetime.now().strftime("%Y%m%d%H%M")

    # MSH Segment
    msg.msh.msh_3 = "COMRAD"
    msg.msh.msh_4 = "IMED"
    msg.msh.msh_5 = "ReceivingApp"
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = current_time
    msg.msh.msh_9 = "ORM^O01^ORM_O01"
    msg.msh.msh_10 = "MSGID12345"
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.4"

    # PID Segment - Patient Information
    pid_segment = msg.add_segment("PID")
    pid_segment.pid_3 = "1234567890"
    pid_segment.pid_5 = "Doe^John^"
    pid_segment.pid_7 = "19900101"
    pid_segment.pid_8 = "M"
    pid_segment.pid_11 = "123 Main St.^^Anytown^VIC^12345^UA"

    # PV1 Segment - Patient Visit
    pv1_segment = msg.add_segment("PV1")
    pv1_segment.pv1_2 = "I"  # Patient class (I = Inpatient)
    pv1_segment.pv1_3 = "^^^GENHOSP^General Ward"  # Assigned Patient Location
    pv1_segment.pv1_19 = "123456"  # Visit Number

    # ORC Segment - Common Order
    orc_segment = msg.add_segment("ORC")
    orc_segment.orc_1 = "NW"  # Order control (NW = New Order)
    orc_segment.orc_2 = "ORD123456789^COMRAD"  # Placer Order Number
    orc_segment.orc_5 = "SC"  # Order Status (SC = In progress)
    orc_segment.orc_9 = current_time  # Date/Time of Transaction

    # OBR Segment - Observation Request
    obr_segment = msg.add_segment("OBR")
    obr_segment.obr_1 = "1"  # Set ID - OBR
    obr_segment.obr_2 = "ORD123456789^COMRAD"  # Placer Order Number
    obr_segment.obr_3 = ""  # Filler Order Number (Optional, if not available)
    obr_segment.obr_4 = "XRAY^Chest X-Ray^L"  # Universal Service Identifier
    obr_segment.obr_7 = current_time  # Observation Date/Time

    # Ensure to populate other required/optional fields as needed for your implementation

    return msg

# Create and print the HL7 message
hl7_orm_message = create_hl7_orm_message()


# Create and print the HL7 message
hl7_orm_message = create_hl7_orm_message()

# Create and print the HL7 message
hl7_orm_message = create_hl7_orm_message()

# Print each segment separately
print("MSH:", hl7_orm_message.msh.to_er7())
print("PID:", hl7_orm_message.get_segment("PID").to_er7())
print("PV1:", hl7_orm_message.get_segment("PV1").to_er7())
print("ORC:", hl7_orm_message.get_segment("ORC").to_er7())
print("OBR:", hl7_orm_message.get_segment("OBR").to_er7())

