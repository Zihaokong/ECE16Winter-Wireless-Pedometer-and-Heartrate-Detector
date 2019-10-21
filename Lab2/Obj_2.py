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
    byte_name_bad = ""