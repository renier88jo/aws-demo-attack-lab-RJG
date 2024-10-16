import requests, argparse, time
from urllib.parse import urlparse

with open('urltoattack.txt') as f:
    url = f.readline().rstrip()
    f.close()

url = "http://{}/helloworld/greeting".format(url)

# Set to bypass errors if the target site has SSL issues
requests.packages.urllib3.disable_warnings()

post_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

get_headers = {
    "prefix": "<%",
    "suffix": "%>//",
    # This may seem strange, but this seems to be needed to bypass some check that looks for "Runtime" in the log_pattern
    "c": "Runtime",
}

def main():
    parser = argparse.ArgumentParser(description='Spring Core RCE')
    parser.add_argument('--url', help='target url', required=False)
    parser.add_argument('--file', help='File to write to [no extension]', required=False, default="shell")
    parser.add_argument('--dir', help='Directory to write to. Suggest using "webapps/[appname]" of target app',
                        required=False, default="webapps/ROOT")

    file_arg = parser.parse_args().file
    dir_arg = parser.parse_args().dir
    url_arg = url

    filename = file_arg.replace(".jsp", "")

    if url_arg is None:
        print("Must pass an option for --url")
        return

    try:
        payload = ""
        headers = {}

        print("[+]----------------------------------------------------------------------------------------------------------------------------")
        print("[+] The URL for testing is: {}".format(url))

        # SQL Injection
        cmdSql = "{}/?id=-1+union+all+select+1,group_concat(user,0x3a,file_priv),3,4+from+mysql.user--".format(url)
        print("[+]----------------------------------------------------------------------------------------------------")
        print("[+] Attacking with SQL Injection")
        SQLInjecton = requests.request("GET",cmdSql, data=payload, headers=headers)
        if SQLInjecton.status_code != 200:
            print("[+] SQL Injection unsuccessful! Blocked by Prisma Cloud - {}".format(SQLInjecton))
        else:
            print("[+] SQL Injection successful! - {}".format(SQLInjecton))
        time.sleep(1)

        # Command Injection
        cmdCommandInjection = "{}/?codei=codei=__import__(%27os%27).popen(%27uname%20-a%27).read()".format(url)
        print("[+]----------------------------------------------------------------------------------------------------")
        print("[+] Attacking with Command Injection")
        CommandInjection = requests.request("GET",cmdCommandInjection, data=payload, headers=headers)
        if CommandInjection.status_code != 200:
            print("[+] Command Injection unsuccessful! Blocked by Prisma Cloud - {}".format(CommandInjection))
        else:
            print("[+] Command Injection successful! - {}".format(CommandInjection))
        time.sleep(1)

        # File Inclusion
        cmdFileInclusion = "{}/?lfi=/..0x2fboot.ini".format(url)
        print("[+]----------------------------------------------------------------------------------------------------")
        print("[+] Attacking with File Inclusion")
        FileInclusion = requests.request("GET",cmdFileInclusion, data=payload, headers=headers)
        if FileInclusion.status_code != 200:
            print("[+] Local File Inclusion unsuccessful! Blocked by Prisma Cloud - {}".format(FileInclusion))
        else:
            print("[+] Local File Inclusion successful! - {}".format(FileInclusion))
        time.sleep(1)

        # Cross-Site Scripting - <script>alert(1)</script>
        cmdXSS = "{}".format(url)
        print("[+]----------------------------------------------------------------------------------------------------")
        print("[+] Attacking with Cross-Site Scripting (XSS) - <script>alert(1)</script>")
        payload = '<script>alert(1)</script>'
        XSS = requests.request("POST",cmdXSS, data=payload, headers=headers)
        if XSS.status_code != 200:
            print("[+] Cross-Site Scripting (XSS) unsuccessful! Blocked by Prisma Cloud - {}".format(XSS))
        else:
            print("[+] Cross-Site Scripting (XSS) successful! - {}".format(XSS))
        time.sleep(1)

        ## Malformed HTTP Request
        cmdMalformed = "{}".format(url)
        print("[+]----------------------------------------------------------------------------------------------------")
        print("[+] Attacking with Malformed HTTP Request")
        payload = 'test-waas'
        Malformed = requests.request("GET",cmdMalformed, data=payload, headers=headers)
        if Malformed.status_code != 200:
            print("[+] Malformed HTTP Request unsuccessful! Blocked by Prisma Cloud - {}".format(Malformed))
        else:
            print("[+] Malformed HTTP Request successful! - {}".format(Malformed))
        time.sleep(1)

        print("[+]----------------------------------------------------------------------------------------------------")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()