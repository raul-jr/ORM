from hl7apy.core import Message
from datetime import datetime
import json

def generate_hl7_message_as_json(msg_id):
    # Initialize the HL7 message with the ORM_O01 message type
    msg = Message("ORM_O01")

    # Populate the MSH segment
    msg.msh.msh_3 = "Best Practice 1.10.0.880"
    msg.msh.msh_4 = "BP000000"
    msg.msh.msh_5 = "UNKNOWN"
    msg.msh.msh_6 = "I-MED Radiology Network"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = "ORM^O01"
    msg.msh.msh_10 = "00000020210301.773053457"  # Message control ID with leading zeros
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.4"
    msg.msh.msh_13 = "418"
    msg.msh.msh_15 = "NE"
    msg.msh.msh_16 = "AL"
    msg.msh.msh_17 = "AU"

    # Populate the PID segment
    pid = msg.add_segment("PID")
    pid.pid_1 = "1"
    pid.pid_3 = "2^^^BPS^PI-4133180467^1^AUSMC^AUSHIC^MC " # Patient identifier with leading zeros
    pid.pid_5 = "Doe^John^^^Mr.^"
    pid.pid_7 = "19900101"
    pid.pid_8 = "M"
    pid.pid_10 = "4^Neither Aboriginal nor Torre Strait Islander^602543"
    pid.pid_11 = "123 Main St.^^Melbourne^VIC^3004^^1"
    pid.pid_13 = "^PRN^CP^^^^0416328319^^^PH^^^02^^NET^Internet^testpatient@test.com.au"
    
    # Populate the PV1 segment
    pv1 = msg.add_segment("PV1")
    pv1.pv1_1 = "1"
    pv1.pv1_2 = "O"
    #pv1.pv1_3 = "PH"
    pv1.pv1_8  = "*******^Findacure^Frederick^^^Dr^^^AUSHICPR"
    pv1.pv1_9 = "*******^Findacure^Frederick^^^Dr^^^AUSHICPR"
    pv1.pv1_17 = "12340^Smith^John^MD^Dr."
    #pv1.pv1_19 = f"V{msg_id:04d}"  # Visit number with leading zeros
    pv1.pv1_20 = "PRIVATE"
    #pv1.pv1_39 = "I^IMED"
    #pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")

    # Populate the ORC segment
    orc = msg.add_segment("ORC")
    orc.orc_1 = "NW"
    orc.orc_2 = "773053457-1"  # Placer order number with leading zeros
    #orc.orc_3 = f"VR{msg_id:04d}"  # Filler order number with leading zeros
    orc.orc_4 = "773053457"
    #orc.orc_5 = "CM"
    orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")
    orc.orc_12 = "*******^Findacure^Frederick^^^Dr^^^AUSHICPR"
    orc.orc_14 = "^^^PH^^^07^44444444^^^FX^^^07^44444445^NET^Internet^findacur@bpsoftware.com.au"
    #orc.orc_17 = "IMED"
    
    # Create and populate the OBR segment with observation request information
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = "773053457-1"
    #obr.obr_3 = f"VR{msg_id:04d}"
    obr.obr_4 = "X-Ray Shoulder"
    obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_10 = "L"
    obr.obr_13 = "car accident"
    obr.obr_16 = "*******^Findacure^Frederick^^^Dr^^^AUSHICPR"
   # obr.obr_31 = "car accident injury"
    
    
    #Create and populate OBX segment 
    obx =msg.add_segment("OBX")
    obx.obx_1 = "1"
    obx.obx_2 = "RP"
    obx.obx_3 = "60572-5^^LN^ENTRY^^EN 13606"
    obx.obx_4 = "1"
    obx.obx_5 = "CEN-Repository-Consent.v1^Repository Consent&99A-9B6A27841D4552AB&L^TEXT^Octet-stream"

    #OBX2
    obx2 = msg.add_segment("OBX")
    obx2.obx_1 = "2"
    obx2.obx_2 ="CE"
    obx2.obx_3 = "728301000168101^Patient consent to upload healthcare document^SCT"
    obx2.obx_4 = "1.1"
    obx2.obx_5 = "728321000168105^Patient consent not withdrawn^SCT"
    
    #OBX3
    obx3 = msg.add_segment("OBX")
    obx3.obx_1 = "3"
    obx3.obx_2 = "CE"
    obx3.obx_3 = "728211000168106^eHealth record ownership^SCT"
    obx3.obx_4 = "1.2"
    obx3.obx_5 = "728231000168101^Patient does not have eHealth record^SCT"
    
    #OBX4
    obx4 = msg.add_segment("OBX")
    obx4.obx_1 = "4"
    obx4.obx_2 = "CE"
    obx4.obx_3 = "74835-2^Health Data Repository (Identifier)^LN"
    obx4.obx_4 = "1.3"
    obx4.obx_5 = "8003640002000050^MyEHR Health Repository^GSO"
    
    
    # Convert the HL7 message to a string and append 'O\n' to each segment
    hl7_str_with_custom_ending = msg.to_er7().replace('\r', '\n') + '\n'  # Assuming '\r' is the segment delimiter

    # Create the JSON object
    message_dict = {
        "name": f"name{msg_id}.ORM",
        "content": hl7_str_with_custom_ending,
        "type": "HL7"
    }

    # Serialize the dictionary to JSON
    json_output = json.dumps(message_dict, indent=4)

    # Output JSON to a file
    filename_json = f"hl7_message_{msg_id:04d}.json"
    with open(filename_json, "w") as json_file:
        json_file.write(json_output)

    # Optionally, return the JSON string if you want to use it directly
    return json_output

# Generate HL7 message as JSON for a specific message ID
json_output = generate_hl7_message_as_json(1)
print(json_output)
