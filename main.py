from src.conexao import APIConnection

connection = APIConnection()
connection.authenticate()

code = input("Digite o code copiado: ")
access_token = connection.acquire_access_token(code)

print(f"Access Token: {access_token}")

# Example of making a request
response = connection.make_graph_request('me')
print(response)