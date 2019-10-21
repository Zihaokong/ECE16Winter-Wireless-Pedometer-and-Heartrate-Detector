<<<<<<< HEAD
name = "Zihao"
try:
    byte_name = name.encode('utf-8')
    byte_name.decode()
    print(byte_name)
except:
    print("error")


try:
    byte_name_bad = byte_name + b'\xef'
except:
    print("error")
try:
    byte_name_bad.decode()
    print(byte_name_bad)
except UnicodeDecodeError:
=======
name = "Zihao"
try:
    byte_name = name.encode('utf-8')
    byte_name.decode()
    print(byte_name)
except:
    print("error")


try:
    byte_name_bad = byte_name + b'\xef'
except:
    print("error")
try:
    byte_name_bad.decode()
    print(byte_name_bad)
except UnicodeDecodeError:
>>>>>>> 79e8aca31fccd6bd1f2a14e67439178edf95c6b2
    byte_name_bad = ""