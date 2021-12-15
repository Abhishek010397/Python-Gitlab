import gitlab

gl = gitlab.Gitlab('https://git.services.securitysvcs.verizon.com',private_token='YOUR-PRIVATE-TOKEN')
gl.auth()
users = gl.users.list(all=True)

for user in users:    
    print(user)
