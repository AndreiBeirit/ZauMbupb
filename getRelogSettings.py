import fnmatch
import os
import subprocess
import pymysql
from relog_config import host, port, user, db_password, db_name

path = "C:/RELOG/Settings.xml"
path2 = "C:/Users/vagrant/Downloads/"

for path2, dirs, files in os.walk(os.path.abspath(path2)):
    for filename in fnmatch.filter(files, "*.ps1"):
        profile_name = filename.split('.')[0]

try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=db_password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor # type: ignore
    )
    print("Successfully connected...")
    print("#" * 30)

    try:
        with connection.cursor() as cursor:
            select_prof = f"SELECT Settings FROM Profiles WHERE Name = \"{profile_name}\";" # type: ignore
            cursor.execute(select_prof)
            connection.commit()
            relog_prof = cursor.fetchone()['Settings'] # type: ignore
            print(relog_prof)
            f = open(path, 'w', encoding="utf-8")
            f.write(relog_prof)
            f.close()
    finally:
        connection.close()

except Exception as ex:
    print("Connection refused...")
    print(ex)

def run_ps_script(script_path):
    try:
        subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing PowerShell script: {e}")

script_files = [f for f in os.listdir(path2) if f.endswith(".ps1")]

if script_files:
    script_path = os.path.join(path2, script_files[0])
    run_ps_script(script_path)
else:
    print("No .ps1 script files found in the specified directory.")
