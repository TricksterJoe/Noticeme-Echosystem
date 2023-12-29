import subprocess


hwid = subprocess.check_output(
    "wmic diskdrive get serialnumber", shell=True, text=True).strip().split('\n')[-1]
print(hwid)
