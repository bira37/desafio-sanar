from flask_restful import Resource
from flask import request
from flask import abort
from mundiapi.mundiapi_client import MundiapiClient
from mundiapi.models import *
from mundiapi.controllers import *
from mundiapi.exceptions.error_exception import *
from .User import User
from .Plan import Plan
from app import db

class SanarAPI(Resource):

  def get(self, user_id=None):
    try:
      assert user_id is not None, "id do usuario nao especificado"
      
      #Recupera usuario na base de dados
      user = User.query.filter_by(id = user_id).first()
      
      assert user is not None, "usuario nao existe"
      
      #Retorna as informacoes do usuario presentes na base
      return {"id": user.id, "nome": user.name, "plano": user.plan_name, "mundi_customer_id": user.mundi_customer_id, "mundi_subscription_id": user.mundi_subscription_id}, 200
      
    except ErrorException as ex:
      return {"message": ex.message + ". Errors: " + ex.errors}, 400
      abort(400)
    except AssertionError as ex:
      return {"message": "Assertion Error: " + str(ex)}, 400
    except Exception as ex:
      return {"message": "Exception: " + str(ex)}, 400
    
    
  def post(self):
    """ JSON para referencia:
      { cliente: {nome, email},
        cartao: {nome_cartao, numero, expiracao_mes, expiracao_ano, cvv}
        produto: {tipo, plano_id}
      } 
    """
    try:
      #Recupera o corpo da requisicao
      data = request.get_json(force=True)
      
      #Verifica se as informacoes constam no JSON
      assert "cliente" in data, "\"cliente\" nao consta no corpo da requisicao"
      assert "nome" in data["cliente"], "\"nome\" nao consta no corpo da requisicao"
      assert "email" in data["cliente"], "\"email\" nao consta no corpo da requisicao"
      assert "cartao" in data, "\"cartao\" nao consta no corpo da requisicao"
      assert "nome_cartao" in data["cartao"], "\"nome_cartao\" nao consta no corpo da requisicao"
      assert "numero" in data["cartao"], "\"numero\" nao consta no corpo da requisicao"
      assert "expiracao_mes" in data["cartao"], "\"expiracao_mes\" nao consta no corpo da requisicao"
      assert "expiracao_ano" in data["cartao"], "\"expiracao_ano\" nao consta no corpo da requisicao"
      assert "cvv" in data["cartao"], "\"cvv\" nao consta no corpo da requisicao"
      assert "produto" in data, "\"produto\" nao consta no corpo da requisicao"
      assert "tipo" in data["produto"], "\"tipo\" nao consta no corpo da requisicao"
      assert "plano_id" in data["produto"], "\"plano_id\" nao consta no corpo da requisicao"
      
      #Cria usuario no mundipagg
      customers_controller_instance = customers_controller.CustomersController()
      customer_request = create_customer_request.CreateCustomerRequest()
      customer_request.name = data["cliente"]["nome"]
      customer_request.email = data["cliente"]["email"]
      
      customer_result = customers_controller_instance.create_customer(customer_request)
      assert customer_result is not None, "erro durante a criacao do cliente"
      
      #Adicionando o seu cartao
      card_request = create_card_request.CreateCardRequest()
      card_request.number = data["cartao"]["numero"]
      card_request.holder_name = data["cartao"]["nome_cartao"]
      card_request.exp_month = data["cartao"]["expiracao_mes"]
      card_request.exp_year = data["cartao"]["expiracao_ano"]
      card_request.cvv = data["cartao"]["cvv"]
      
      #Obtem id do plano na base de dados
      plan = Plan.query.filter_by(id=data["produto"]["plano_id"]).first()
      assert plan is not None, "plano nao encontrado"
      
      plans_controller_instance = plans_controller.PlansController()
      plan_result = plans_controller_instance.get_plan(plan.mundi_plan_id)
      assert plan_result is not None, "erro ao obter plano / plano nao encontrado"
      
      #Cria assinatura com o plano para o cliente
      subscriptions_controller_instance = subscriptions_controller.SubscriptionsController()
      subscription_request = create_subscription_request.CreateSubscriptionRequest()
      subscription_request.plan_id = plan_result.id
      subscription_request.customer_id = customer_result.id
      subscription_request.card = card_request
      subscription_request.code = data["produto"]["tipo"]
      subscription_result = subscriptions_controller_instance.create_subscription(subscription_request)
      assert subscription_result is not None, "erro durante realizacao da assinatura"
        
      #Adiciona a informacao do usuario na base de dados
      new_user = User(name = customer_result.name, plan_name = plan_result.name, mundi_customer_id = customer_result.id, mundi_subscription_id = subscription_result.id)
      db.session.add(new_user)     
      db.session.commit()
      
      #Retorna informacoes do usuario cadastrado
      return {"nome": new_user.name, "mundi_subscription_id": subscription_result.id, "id": new_user.id, "plano": plan_result.name, "primeiros 6 digitos do cartao": subscription_result.card.first_six_digits, "ultimos 4 digitos do cartao": subscription_result.card.last_four_digits}, 200
      
    except ErrorException as ex:
      return {"message": ex.message + ". Errors: " + ex.errors}, 400
      abort(400)
    except AssertionError as ex:
      return {"message": "Assertion Error: " + str(ex)}, 400
    except Exception as ex:
      return {"message": "Exception: " + str(ex)}, 400
    
  def put(self, user_id=None):
    try:
      #Recupera o corpo da requisicao
      data = request.get_json(force=True)
      
      assert user_id is not None, "id do usuario nao especificado"
        
      #Recupera usuario na base de dados
      user = User.query.filter_by(id = user_id).first()
      
      #Verifica se as informacoes constam no JSON
      assert user is not None, "usuario nao existe"
      assert "cartao" in data, "\"cartao\" nao consta no corpo da requisicao"
      assert "nome_cartao" in data["cartao"], "\"nome_cartao\" nao consta no corpo da requisicao"
      assert "numero" in data["cartao"], "\"numero\" nao consta no corpo da requisicao"
      assert "expiracao_mes" in data["cartao"], "\"expiracao_mes\" nao consta no corpo da requisicao"
      assert "expiracao_ano" in data["cartao"], "\"expiracao_ano\" nao consta no corpo da requisicao"
      assert "cvv" in data["cartao"], "\"cvv\" nao consta no corpo da requisicao"
      
      #Cria o novo cartao a ser alterado
      new_card_request = create_card_request.CreateCardRequest()
      new_card_request.number = data["cartao"]["numero"]
      new_card_request.holder_name = data["cartao"]["nome_cartao"]
      new_card_request.exp_month = data["cartao"]["expiracao_mes"]
      new_card_request.exp_year = data["cartao"]["expiracao_ano"]
      new_card_request.cvv = data["cartao"]["cvv"]
      
      #Checa se deve alterar o cartao ou criar uma nova assinatura para o usuario utilizando este cartao
      if "produto" in data:
        #Cria uma nova assinatura pro usuario
        assert user.mundi_subscription_id is None, "assinatura ja existente"
        assert "tipo" in data["produto"], "\"tipo\" nao consta no corpo da requisicao"
        assert "plano_id" in data["produto"], "\"plano_id\" nao consta no corpo da requisicao"
        
        #Obtem o plano 
        plan = Plan.query.filter_by(id=data["produto"]["plano_id"]).first()
        assert plan is not None, "plano nao encontrado"
        plans_controller_instance = plans_controller.PlansController()
        plan_result = plans_controller_instance.get_plan(plan.mundi_plan_id)
        assert plan_result is not None, "erro ao obter plano / plano nao encontrado"
        
        #Cria assinatura com o plano para o cliente
        subscriptions_controller_instance = subscriptions_controller.SubscriptionsController()
        subscription_request = create_subscription_request.CreateSubscriptionRequest()
        subscription_request.plan_id = plan_result.id
        subscription_request.customer_id = user.mundi_customer_id
        subscription_request.card = new_card_request
        subscription_request.code = data["produto"]["tipo"]
        subscription_result = subscriptions_controller_instance.create_subscription(subscription_request)
        assert subscription_result is not None, "erro durante realizacao da assinatura"
        
        #Atualiza informacao na base de dados
        user.mundi_subscription_id = subscription_result.id
        user.plan_name = plan_result.name
        db.session.commit()
        
        #Retorna as informacoes da nova assinatura do cliente
        return {"nome": user.name, "id": user.id, "mundi_subscription_id": user.mundi_subscription_id, "plano": plan_result.name, "primeiros 6 digitos do cartao": subscription_result.card.first_six_digits, "ultimos 4 digitos do cartao": subscription_result.card.last_four_digits}, 200
      
      else:
        #Altera as informacoes do cartao da assinatura atual
        assert user.mundi_subscription_id is not None, "assinatura nao existente"
        subscriptions_controller_instance = subscriptions_controller.SubscriptionsController()
        card_update_request = update_subscription_card_request.UpdateSubscriptionCardRequest()
        card_update_request.card = new_card_request
        
        card_update_result = subscriptions_controller_instance.update_subscription_card(user.mundi_subscription_id, card_update_request)
        assert card_update_result is not None, "erro ao atualizar informacoes do cartao"
        
        #Retorna as informacoes da atualizacao do cartao do cliente
        return {"nome": user.name, "id": user.id, "plano": user.plan_name, "mundi_subscription_id": user.mundi_subscription_id, "primeiros 6 digitos do cartao": card_update_result.card.first_six_digits, "ultimos 4 digitos do cartao": card_update_result.card.last_four_digits}, 200
        
    except ErrorException as ex:
      return {"message": ex.message + ". Errors: " + ex.errors}, 400
      abort(400)
    except AssertionError as ex:
      return {"message": "Assertion Error: " + str(ex)}, 400
    except Exception as ex:
      return {"message": "Exception: " + str(ex)}, 400
    
  def delete(self, user_id=None):
    try:
      assert user_id is not None, "id do usuario nao especificado"
        
      #Recupera usuario na base de dados
      user = User.query.filter_by(id = user_id).first()
      
      assert user is not None, "usuario nao existe"
      
      #Cancela a assinatura atual do usuario
      assert user.mundi_subscription_id is not None, "assinatura nao existente"
      subscriptions_controller_instance = subscriptions_controller.SubscriptionsController()
      subscription_result = subscriptions_controller_instance.cancel_subscription(user.mundi_subscription_id)
      assert subscription_result is not None, "erro durante cancelamento da assinatura"
      assert subscription_result.status == "canceled", "erro durante cancelamento da assinatura"
      
      #Atualiza na base de dados removendo o id da assinatura
      return_plan_name = user.plan_name
      user.mundi_subscription_id = None
      user.plan_name = None
      db.session.commit()
      
      #Retorna as informacoes de cancelamento da assinatura para o cliente
      return {"id": user.id, "nome": user.name, "plano": return_plan_name, "mundi_subscription_id": subscription_result.id, "status": subscription_result.status}, 200
  
    except ErrorException as ex:
      return {"message": ex.message + ". Errors: " + ex.errors}, 400
      abort(400)
    except AssertionError as ex:
      return {"message": "Assertion Error: " + str(ex)}, 400
    except Exception as ex:
      return {"message": "Exception: " + str(ex)}, 400
