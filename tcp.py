from hl7apy.core import Message
from datetime import datetime

def orm  ():
    msg = Message("ORM_O01")
    
    msg.msh.msh_3 = "COMRAD"
    msg.msh.msh_4 = "IMED"
    msg.msh.msh_5 = "ReceivingApp"
    msg.msh.msh_6 = "ReceivingFacility"
    msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M")
    msg.msh.msh_9 = "ORM^O01^ORM_O01"
    msg.msh.msh_10 = "MSGID12345"
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = "2.4"
    
   
    #pid= msg.add_segment("PID")
    pid=msg.add_group("ORM_O01_PATIENT")
    pid.ORM_O01_PATIENT.pid.pid_3 = "1234567890"
    pid.ORM_O01_PATIENT.pid.pid_5 = "Doe^John^"
    pid.ORM_O01_PATIENT.pid.pid_7 = "19900101"
    pid.ORM_O01_PATIENT.pid.pid_8 = "M"
    pid.ORM_O01_PATIENT.pid.pid_11 = "123 Main St.^^Anytown^VIC^12345^UA"
    
    
    #pv1 = msg.add_segment("PV1")
    pv1 =msg.add_group("ORM_O01_PATIENT_VISIT")
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_1 = "1"
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_2 = "O"
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_3 = "PH"
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_17 = "12345^Smith^John^MD^Dr."
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_19 = "VRTEST1"
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_20 = "MB"
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_39 = "I^IMED"
    pv1.ORM_O01_PATIENT_VISIT.pv1.pv1_44 = datetime.now().strftime("%Y%m%d%H%M")
    
    #orc = msg.add_segment("ORC")
    msg.ORM_O01_ORDER.orc.orc_1 = "SC"
    msg.ORM_O01_ORDER.orc.orc_2 = "TEST-1001-MRI"
    msg.ORM_O01_ORDER.orc.orc_3 = "TEST-1001-MRI"
    msg.ORM_O01_ORDER.orc.orc_5 = "SC"
    msg.ORM_O01_ORDER.orc.orc_9 = datetime.now().strftime("%Y%m%d%H%M")
    msg.ORM_O01_ORDER.orc.orc_12 = "12345^IMED CLINIC^^^"
    msg.ORM_O01_ORDER.orc.orc_14 = "0123345^PH"
    msg.ORM_O01_ORDER.orc.orc_17 = "IMED"
    
    obr = msg.add_segment("OBR")
    obr.obr_1 = "1"
    obr.obr_2 = "TEST-1001-MRI"
    obr.obr_3 = "TEST-1001-MRI"
    obr.obr_4 = "MRI Brain^Magnetic Resonance Imaging Brain"
    obr.obr_6 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_7 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_8 = datetime.now().strftime("%Y%m%d%H%M")
    obr.obr_10 = "COMRAD"
    obr.obr_16 = "12345^Smith^John^MD^Dr."
    obr.obr_31 = "Head Injury"
    obr.obr_34 = "TEST&TEST&12234"
    obr.obr_44 = "MRHBCN"
   
    return msg.to_er7()
print (orm())
