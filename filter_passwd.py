
if __name__ == '__main__':
    passwd = '1'
    with open(r"C:\Users\彭卓冰\Desktop\jikefeng.txt", 'r') as fh:
        with open("new_password.txt", 'w') as n:
            while passwd:
                passwd = fh.readline().strip()
                if len(passwd) > 7:
                    n.write(passwd+"\n")
