import socket

def send_test_message(host="127.0.0.1", port=2575):
    # Define a simple HL7 message (ORM^O01)
    hl7_message = (
        "MSH|^~\\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|"
        "202106151200||ORM^O01|MSGID0001|P|2.4\r"
        "PID|||TEST1234||Doe^John||19900101|M|||123 Main St.^^Anytown^NSW^12345^AU\r"
        "PV1||O|PH||||12340^Smith^John^MD^Dr.|||||||||||||V1234|MB|||I^IMED|202106151200\r"
        "ORC|CM|TEST-10001-MRI|VR0001|CM|202106151200|12345^IMED CLINIC^^^|0123345^PH|IMED\r"
        "OBR|1|TEST-10001-MRI|VR0001|MRI^NR PELVIS|202106151200|202106151200|202106151200|COMRAD|12345^Smith^John^MD^Dr.\r"
    )
    
    # Wrap the HL7 message with MLLP frame
    mllp_message = f'\x0B{hl7_message}\x1C\x0D'
    
    # Establish a TCP connection to Mirth Connect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(mllp_message.encode())
        
        # Receive the response from Mirth Connect (optional)
        response = s.recv(1024)
        print("Received", response.decode())

# Send a test message
send_test_message()
