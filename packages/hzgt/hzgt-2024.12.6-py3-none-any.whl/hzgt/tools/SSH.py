


try:
    import paramiko
except Exception as err:
    print(err)
    os.system(INSTALLCMD("paramiko==3.4.0"))
    import paramiko






