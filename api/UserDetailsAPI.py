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

class UserDetailsAPI(Resource):

  def get(self, user_id=None):
    try:
      assert user_id is not None, "id do usuario nao especificado"
      
      #Recupera usuario na base de dados
      user = User.query.filter_by(id = user_id).first()
      
      assert user is not None, "usuario nao existe"
      
      user_json = {}
      subscription_json = {}
      
      #Obtem informacoes do usuario na api da mundipagg
      customers_controller_instance = customers_controller.CustomersController()
      
      customer_result = customers_controller_instance.get_customer(user.mundi_customer_id)
      assert customer_result is not None, "erro durante a obtencao dos dados do cliente"
      
      user_json["id"] = user.id
      user_json["mundi_customer_id"] = customer_result.id
      user_json["nome"] = customer_result.name
      user_json["email"] = customer_result.email
      #user_json["criado em"] = customer_result.created_at
      #user_json["atualizado em"] = customer_result.updated_at
      
      if(user.mundi_subscription_id is None):
        subscription_json = None
      else:
        subscriptions_controller_instance = subscriptions_controller.SubscriptionsController()
        subscription_result = subscriptions_controller_instance.get_subscription(user.mundi_subscription_id)
        assert subscription_result is not None, "erro durante a obtencao dos dados da assinatura do cliente"
        
        subscription_json["cartao"] = {}
        subscription_json["produto"] = []
        subscription_json["codigo"] = subscription_result.code
        subscription_json["mundi_subscription_id"] = subscription_result.id
        subscription_json["status"] = subscription_result.status
        #subscription_json["criado em"] = subscription_result.created_at
        #subscription_json["atualizado em"] = subscription_result.updated_at
        subscription_json["moeda"] = subscription_result.currency
        subscription_json["tipo de pagamento"] = subscription_result.billing_type
        subscription_json["cartao"]["nome_cartao"] = subscription_result.card.holder_name
        subscription_json["cartao"]["primeiros 6 digitos"] = subscription_result.card.first_six_digits
        subscription_json["cartao"]["ultimos 4 digitos"] = subscription_result.card.last_four_digits
        subscription_json["cartao"]["expiracao_mes"] = subscription_result.card.exp_month
        subscription_json["cartao"]["expiracao_ano"] = subscription_result.card.exp_year
        
        for item in subscription_result.items:
          produto = {}
          produto["nome"] = item.name
          produto["quantidade"] = item.quantity
          produto["ciclos"] = item.cycles
          produto["preco"] = item.pricing_scheme.price
          subscription_json["produto"].append(produto)
        
      #Retorna as informacoes do cliente e da assinatura
      return {"cliente": user_json, "assinatura": subscription_json}, 200
      
    except ErrorException as ex:
      return {"message": ex.message + ". Errors: " + ex.errors}, 400
      abort(400)
    except AssertionError as ex:
      return {"message": "Assertion Error: " + str(ex)}, 400
    except Exception as ex:
      return {"message": "Exception: " + str(ex)}, 400
