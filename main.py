from src.conexao import APIConnection

connection = APIConnection()
connection.authenticate()

code = input("Digite o code copiado: ") # code é o parâmetro da url 
access_token = connection.acquire_access_token(code)

print(f"Access Token: {access_token}")

response = connection.make_graph_request('me')
print(response)