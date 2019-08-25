import requests

def main():
  
  """ Primeiro caso de uso """
  print("Caso de Uso 1: Mario assinou o SanarFlix Mensal.")
  print("")
  use_case_json = {"cliente": {"nome": "Mario", "email":"mariosantos@gmail.com"}, "produto":{"tipo":"plano", "plano_id":"plan_mens"}, "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}}
  print("Acao: Realizar uma requisicao POST para \"http://127.0.0.1:5000/api/users/\", passando no corpo da requisicao o JSON com as informacoes do usuario mostrado abaixo.")
  print(use_case_json)
  print("")
  use_case_response = requests.post("http://127.0.0.1:5000/api/users/", json = use_case_json)
  print("Resultado: Ela retorna as seguintes informacoes mostradas abaixo.")
  print(use_case_response.json())
  print("")
  """ """
  
  print("-----------------------------------------------------------------------------------------------")
  
  """ Segundo caso de uso """
  print("Caso de Uso 2: Juliana assinou o SanarFlix com periodo de teste de 7 dias")
  print("")
  use_case_json = {"cliente": {"nome": "Juliana", "email":"juliana123@gmail.com"}, "produto":{"tipo":"plano", "plano_id":"plan_mens_teste"}, "cartao":{"nome_cartao": "juliana", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}}
  print("Acao: Realizar uma requisicao POST para \"http://127.0.0.1:5000/api/users/\", passando no corpo da requisicao o JSON com as informacoes do usuario mostrado abaixo.")
  print(use_case_json)
  print("")
  use_case_response = requests.post("http://127.0.0.1:5000/api/users/", json = use_case_json)
  print("Resultado: Ela retorna as seguintes informacoes mostradas abaixo.")
  print(use_case_response.json())
  print("")
  """ """
  
  print("-----------------------------------------------------------------------------------------------")
  
  """ Terceiro caso de uso """
  print("Caso de Uso 3: Pedro assinou o SanarFlix Trimestral")
  print("")
  use_case_json = {"cliente": {"nome": "Pedro", "email":"pedro147@gmail.com"}, "produto":{"tipo":"plano", "plano_id":"plan_trim"}, "cartao":{"nome_cartao": "pedro", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}}
  print("Acao: Realizar uma requisicao POST para \"http://127.0.0.1:5000/api/users/\", passando no corpo da requisicao o JSON com as informacoes do usuario mostrado abaixo.")
  print(use_case_json)
  print("")
  use_case_response = requests.post("http://127.0.0.1:5000/api/users/", json = use_case_json)
  print("Resultado: Ela retorna as seguintes informacoes mostradas abaixo.")
  print(use_case_response.json())
  print("")
  """ """
  
  print("-----------------------------------------------------------------------------------------------")
  
  """ Quarto caso de uso """
  print("Caso de Uso 4: Marcos deseja mudar o cartao de sua assinatura")
  print("Para simular essa acao, iremos criar uma assinatura para Marcos utilizando os seguintes dados que serao passados no corpo da requisicao, similar aos casos anteriores:")
  use_case_json = {"cliente": {"nome": "Marcos", "email":"marcos369@gmail.com"}, "produto":{"tipo":"plano", "plano_id":"plan_mens"}, "cartao":{"nome_cartao": "marcos", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}}
  print(use_case_json)
  print("")
  marcos_response = requests.post("http://127.0.0.1:5000/api/users/", json = use_case_json)
  print("Recebemos como retorno as seguintes informacoes:")
  print(marcos_response.json())
  print("")
  print("Acao de alteracao: Realizar uma requisicao PUT para \"http://127.0.0.1:5000/api/users/{}\", passando no corpo da requisicao o JSON com as informacoes do usuario mostrado abaixo.".format(marcos_response.json()["id"]))
  use_case_json = {"cartao": {"nome_cartao": "marcos", "numero": "4532912167490007", "expiracao_mes": 1, "expiracao_ano":28, "cvv": "123"}}
  print(use_case_json)
  print("")
  use_case_response = requests.put("http://127.0.0.1:5000/api/users/" + str(marcos_response.json()["id"]), json = use_case_json)
  print("Resultado: Ela retorna as seguintes informacoes mostradas abaixo.")
  print(use_case_response.json())
  print("")
  """ """
  
  print("-----------------------------------------------------------------------------------------------")
  
  """ Quinto caso de uso """
  print("Caso de Uso 5: Luiz assinou o SanarFlix Promocional com o Livro Yellowbook")
  print("")
  use_case_json = {"cliente": {"nome": "Luiz", "email":"luiz258@gmail.com"}, "produto":{"tipo":"plano", "plano_id":"plan_promo_yellowbook"}, "cartao":{"nome_cartao": "luiz", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}}
  print("Acao: Realizar uma requisicao POST para \"http://127.0.0.1:5000/api/users/\", passando no corpo da requisicao o JSON com as informacoes do usuario mostrado abaixo.")
  print(use_case_json)
  print("")
  use_case_response = requests.post("http://127.0.0.1:5000/api/users/", json = use_case_json)
  print("Resultado: Ela retorna as seguintes informacoes mostradas abaixo.")
  print(use_case_response.json())
  print("")
  """ """
  
  print("-----------------------------------------------------------------------------------------------")
  
  """ Sexto caso de uso """
  print("Caso de Uso 6: Ricardo deseja cancelar a sua assinatura")
  print("Para simular essa acao, iremos criar uma assinatura para Ricardo utilizando os seguintes dados que serao passados no corpo da requisicao, similar aos casos anteriores:")
  use_case_json = {"cliente": {"nome": "Ricardo", "email":"ricardo_000@gmail.com"}, "produto":{"tipo":"plano", "plano_id":"plan_trim"}, "cartao":{"nome_cartao": "ricardo", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}}
  print(use_case_json)
  print("")
  ricardo_response = requests.post("http://127.0.0.1:5000/api/users/", json = use_case_json)
  print("Recebemos como retorno as seguintes informacoes:")
  print(ricardo_response.json())
  print("")
  print("Acao de cancelamento: Realizar uma requisicao DELETE para \"http://127.0.0.1:5000/api/users/{}\", sem informacoes adicionais do corpo da requisicao.".format(ricardo_response.json()["id"]))
  use_case_response = requests.delete("http://127.0.0.1:5000/api/users/" + str(ricardo_response.json()["id"]))
  print("Resultado: Ela retorna as seguintes informacoes mostradas abaixo.")
  print(use_case_response.json())
  print("")
  """ """
  
if __name__ == "__main__":
  main()
