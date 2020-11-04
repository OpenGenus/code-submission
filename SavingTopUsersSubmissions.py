import urllib.request, json, os
import main

only_active = "false" 
query = "https://codeforces.com/api/user.ratedList?activeOnly=" + only_active

def listOfUsers(number_of_users, parent_dir):

	with urllib.request.urlopen(query) as url:
		data = json.loads(url.read().decode())

	users = data["result"][:number_of_users]

	result = []
	for i in range(len(users)):
		result.append([users[i]['handle'], users[i]['maxRating']])
		
	result = sorted(result, key=lambda x: -x[1])

	for user in result:
		print(user[0])
		
		directory = user[0]
		path =  os.path.join(parent_dir, directory)
		os.mkdir(path)
		os.chdir(path)

		main.returnAcceptedSubmissions(user[0], 2)
		os.chdir("..")
		print(user[0])


if __name__ == "__main__":  
	listOfUsers(10, "C:/Users/HP/Documents/GitHub/code-submission/code")



	
