import browser_cookie3

f = open("cookiefile.txt","w")
cj = browser_cookie3.firefox()

for cookie in cj:
   value = cookie.name+cookie.value
   f.write(value)
   f.write("\n")

with open('cookiefile.txt', 'r') as f:
     for line in f:
         if "PHPSESSID" in line:
            print(line)