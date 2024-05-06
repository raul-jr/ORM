from hl7apy.core import Message
from datetime import datetime

def create_hl7_orm_message():
    # Create an ORM message with correct structure
    msg = Message("ORM_O01", version='2.4')
    msg.msh.msh_3 = "SendingApp"
    msg.msh.msh_4 = "SendingFacility"
    msg.msh.msh_5 = "ReceivingApp"
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = "ORM^O01"
    msg.msh.msh_10 = "MSGID12345"
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.4"

    # Ensure the correct structure for PID, ORC, OBR within an ORM message
    # Note: This step may vary based on how hl7apy handles group structures within ORM_O01
    # Adding Patient Information (PID)
    pid_segment = msg.add_segment('PID')
    pid_segment.pid_1= "1"
    pid_segment.pid_3 = "1234567890"
    pid_segment.pid_5 = "Doe^John^"
    pid_segment.pid_7 = "19900101"
    pid_segment.pid_8 = "M"
    pid_segment.pid_11 = "123 Main St.^^Anytown^CA^12345^USA"

    # Assuming the ORM_O01 structure requires ORDER group for ORC, OBR segments
    # This part may need to be adjusted based on actual implementation and version of HL7apy
    order = msg.add_group("ORM_O01_ORDER")
    orc_segment = order.add_segment("ORC")
    orc_segment.orc_1 = "NW"
    orc_segment.orc_2 = "123456"
    orc_segment.orc_5 = "CM"
    orc_segment.orc_9 = datetime.now().strftime("%Y%m%d%H%M")

    obr_segment = order.add_segment("OBR")
    obr_segment.obr_1 = "1"
    obr_segment.obr_2 = "123456"
    obr_segment.obr_4 = "MRI Brain^Magnetic Resonance Imaging Brain"
    obr_segment.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr_segment.obr_16 = "12345^Smith^John^MD^Dr."
    obr_segment.obr_31 = "Urgent"

    return msg

hl7_orm_message = create_hl7_orm_message()
print(hl7_orm_message.to_er7())
