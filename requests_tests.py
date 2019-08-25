import os
import unittest
import requests
from flask import Flask
from app import db
from api.User import User
from app import flaskApp

class FlaskAPITest(unittest.TestCase):

  def tearDown(self):
    # elimina todos os usuarios de teste da base de dados depois de cada teste
    User.query.filter_by(name = "teste").delete()
    db.session.commit()
    
  #testa buscar informacoes de um usuario inexistente  
  def test_get_request_on_non_existing_user(self):
    response = requests.get('http://127.0.0.1:5000/api/users/0')
    self.assertEqual(400, response.status_code)
  
  #testa realizar uma requisicao get sem informar o id
  def test_get_request_without_id_specified(self):
    response = requests.get('http://127.0.0.1:5000/api/users/')
    self.assertEqual(400, response.status_code)
  
  #testa adicionar um usuario com plano mensal
  def test_post_add_new_user_with_monthly_subscription(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)

    self.assertEqual(200, response.status_code)
    self.assertTrue(response.json()["id"] > 0)
    self.assertEqual(response.json()["nome"], "teste")
    self.assertEqual(response.json()["plano"], "Plano SanarFlix Mensal")
  
  #testa adicionar um usuario com plano trimestral  
  def test_post_add_new_user_with_three_months_subscription(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_trim"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, response.status_code)
    self.assertTrue(response.json()["id"] > 0)
    self.assertEqual(response.json()["nome"], "teste")
    self.assertEqual(response.json()["plano"], "Plano SanarFlix Trimestral")
  
  #testa adicionar um usuario com plano mensal com 7 dias de teste  
  def test_post_add_new_user_with_trial_subscription(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens_teste"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, response.status_code)
    self.assertTrue(response.json()["id"] > 0)
    self.assertEqual(response.json()["nome"], "teste")
    self.assertEqual(response.json()["plano"], "Plano SanarFlix Mensal com 7 Dias de Teste")
  
  #testa adicionar um usuario com plano mensal promocional com livro yellowbook 
  def test_post_add_new_user_with_trial_subscription(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_promo_yellowbook"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, response.status_code)
    self.assertTrue(response.json()["id"] > 0)
    self.assertEqual(response.json()["nome"], "teste")
    self.assertEqual(response.json()["plano"], "Plano SanarFlix Promocional Com Livro Yellowbook")
  
  #testa adicionar usuario com plano inexistente  
  def test_post_add_new_user_with_non_existing_plan(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_semestral"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(400, response.status_code)
  
  #testa adicionar usuario com informacoes faltando no corpo
  def test_post_add_new_user_with_missing_info(self):
    request_json = {"cliente": {"email":"joao123@gmail.com"}, 
                    "produto":{"plano_id":"plan_semestral"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv":"591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(400, response.status_code)
    
  #testa adicionar mais de um usuario com plano qualquer
  def test_post_add_more_than_one_user(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, response.status_code)
    self.assertTrue(response.json()["id"] > 0)
    self.assertEqual(response.json()["nome"], "teste")
    self.assertEqual(response.json()["plano"], "Plano SanarFlix Mensal")
    
    request_json["produto"]["plano_id"] = "plan_trim"
    request_json["cliente"]["email"] = "jonas312@hotmail.com"
    second_response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, second_response.status_code)
    self.assertTrue(second_response.json()["id"] > 0)
    self.assertEqual(second_response.json()["nome"], "teste")
    self.assertEqual(second_response.json()["plano"], "Plano SanarFlix Trimestral")
  
  #testa obter informacoes de um usuario com uma assinatura qualquer  
  def test_get_request_on_existing_user(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, response.status_code)
    self.assertTrue(response.json()["id"] > 0)
    self.assertEqual(response.json()["nome"], "teste")
    
    get_response = requests.get('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    self.assertEqual(200, get_response.status_code)
    self.assertEqual(get_response.json()["nome"], "teste")
    self.assertEqual(get_response.json()["id"], response.json()["id"])
  
  #testa cancelar assinatura de um usuario  
  def test_delete_cancel_subscription_of_user(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    self.assertEqual(200, response.status_code)
    
    delete_response = requests.delete('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    
    self.assertEqual(200, delete_response.status_code)
    self.assertEqual(delete_response.json()["status"], "canceled")
    self.assertEqual(response.json()["mundi_subscription_id"], delete_response.json()["mundi_subscription_id"])
    
    get_response = requests.get('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    self.assertEqual(200, get_response.status_code)
    self.assertEqual(None, get_response.json()["mundi_subscription_id"])
    
  #testa cancelar assinatura inexistente de um usuario
  def test_delete_cancel_subscription_already_cancelled(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    self.assertEqual(200, response.status_code)
    
    delete_response = requests.delete('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    
    self.assertEqual(200, delete_response.status_code)
    
    self.assertEqual(delete_response.json()["status"], "canceled")
    self.assertEqual(response.json()["mundi_subscription_id"], delete_response.json()["mundi_subscription_id"])
    
    new_delete_response = requests.delete('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    self.assertEqual(400, new_delete_response.status_code)
  
  #testa alterar cartao de credito de um usuario
  def test_put_change_user_card(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, response.status_code)
    
    card_json = {"cartao": {"nome_cartao": "jose", "numero": "4532912167490007", "expiracao_mes": 1, "expiracao_ano":28, "cvv": "123"}}
    
    put_response = requests.put('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]), json = card_json)
    
    self.assertEqual(200, put_response.status_code)
    self.assertEqual(response.json()["mundi_subscription_id"], put_response.json()["mundi_subscription_id"])
    self.assertEqual("453291", put_response.json()["primeiros 6 digitos do cartao"])
    self.assertEqual("0007", put_response.json()["ultimos 4 digitos do cartao"])
    
  #testa alterar cartao de credito de um usuario com o corpo da requisicao incompleto
  def test_put_change_user_with_missing_information(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    
    self.assertEqual(200, response.status_code)
    
    card_json = {"cartao": {"nome_cartao": "jose", "numero": "4532912167490007", "expiracao_mes": 1, "expiracao_ano":28}}
    
    put_response = requests.put('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]), json = card_json)
    
    self.assertEqual(400, put_response.status_code)
  
  #testa criar nova assinatura para um cliente antigo que cancelou a sua assinatura anterior  
  def test_put_create_new_subscription_for_existing_user(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    self.assertEqual(200, response.status_code)
    
    delete_response = requests.delete('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    self.assertEqual(200, delete_response.status_code)
    
    card_json = {"produto":{"tipo":"plano", "plano_id":"plan_trim"}, "cartao": {"nome_cartao": "jose", "numero": "4532912167490007", "expiracao_mes": 1, "expiracao_ano":28, "cvv": "123"}}
    
    put_response = requests.put('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]), json = card_json)
    
    self.assertEqual(200, put_response.status_code)
    self.assertEqual(put_response.json()["nome"], "teste")
    self.assertEqual(put_response.json()["id"], response.json()["id"])
    self.assertEqual("453291", put_response.json()["primeiros 6 digitos do cartao"])
    self.assertEqual("0007", put_response.json()["ultimos 4 digitos do cartao"])
    self.assertEqual(put_response.json()["plano"], "Plano SanarFlix Trimestral")
    
  #testa criar nova assinatura para um cliente antigo que cancelou a sua assinatura anterior com informacoes faltando 
  def test_put_create_new_subscription_for_existing_user_with_missing_information(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_mens"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    self.assertEqual(200, response.status_code)
    
    delete_response = requests.delete('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    self.assertEqual(200, delete_response.status_code)
    
    card_json = {"produto":{"tipo":"plano", "plano_id":"plan_trim"}}
    
    put_response = requests.put('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]), json = card_json)
    
    self.assertEqual(400, put_response.status_code)
    
  #testa obter informacoes detalhadas de um cliente e suas assinaturas (usando a assinatura promocional)
  def test_get_request_for_detailed_information(self):
    request_json = {"cliente": {"nome": "teste", "email":"joao123@gmail.com"}, 
                    "produto":{"tipo":"plano", "plano_id":"plan_promo_yellowbook"}, 
                    "cartao":{"nome_cartao": "joao", "numero":"4584441896453869", "expiracao_mes":12, "expiracao_ano":19, "cvv": "591"}
                   }
    
    response = requests.post('http://127.0.0.1:5000/api/users/', json = request_json)
    self.assertEqual(200, response.status_code)
    
    get_detailed_response = requests.get('http://127.0.0.1:5000/api/users/details/' + str(response.json()["id"]))
    self.assertEqual(200, get_detailed_response.status_code)
    
    get_response = requests.get('http://127.0.0.1:5000/api/users/' + str(response.json()["id"]))
    self.assertEqual(200, get_response.status_code)
    
    info = get_detailed_response.json()
    
    self.assertEqual(get_response.json()["mundi_customer_id"], info["cliente"]["mundi_customer_id"])
    self.assertEqual(get_response.json()["mundi_subscription_id"], info["assinatura"]["mundi_subscription_id"])
    self.assertEqual("teste", info["cliente"]["nome"])
    self.assertEqual("joao123@gmail.com", info["cliente"]["email"])
    self.assertEqual("458444", info["assinatura"]["cartao"]["primeiros 6 digitos"])
    self.assertEqual("3869", info["assinatura"]["cartao"]["ultimos 4 digitos"])
    self.assertEqual("Plano SanarFlix Mensal", info["assinatura"]["produto"][0]["nome"])
    self.assertEqual(None, info["assinatura"]["produto"][0]["ciclos"])
    self.assertEqual("Livro Yellowbook", info["assinatura"]["produto"][1]["nome"])
    self.assertEqual(1, info["assinatura"]["produto"][1]["ciclos"])
    
if __name__ == "__main__":
    unittest.main()
