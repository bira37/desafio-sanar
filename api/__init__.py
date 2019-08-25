from flask_restful import Api
from app import flaskApp
from .SanarAPI import SanarAPI
from .UserDetailsAPI import UserDetailsAPI
from mundiapi.mundiapi_client import MundiapiClient
from mundiapi.models import *
from mundiapi.controllers import *
from mundiapi.exceptions.error_exception import *
from app import db
from api.User import User
from api.Plan import Plan

#Configura a API e a Mundipagg API
restServer = Api(flaskApp)

restServer.add_resource(SanarAPI, '/api/users/<user_id>', '/api/users/')
restServer.add_resource(UserDetailsAPI, '/api/users/details/<user_id>')

MundiapiClient.config.basic_auth_user_name = "sk_test_RYwm6wBcMjt387nb"
  
#Cria Planos a serem usados (Planos não são criados se já existem)
plans_controller_instance = plans_controller.PlansController()

#Cria o Plano Mensal Normal
plan = Plan.query.filter_by(id="plan_mens").first()
if plan is None:
  request = create_plan_request.CreatePlanRequest()
  request.name = "Plano SanarFlix Mensal"
  request.currency = "BRL"
  request.interval = "month"
  request.interval_count = 1
  request.billing_type = "prepaid"
  request.items = [create_plan_item_request.CreatePlanItemRequest()]
  request.items[0].name = "Plano SanarFlix Mensal"
  request.items[0].quantity = 1
  request.items[0].pricing_scheme = create_pricing_scheme_request.CreatePricingSchemeRequest()
  request.items[0].pricing_scheme.price = 2450
  try:
    result = plans_controller_instance.create_plan(request)
    assert result is not None
    print('Plano ' + result.name + ' criado')
    plan = Plan(id = "plan_mens", name = result.name, mundi_plan_id = result.id)
    db.session.add(plan)
    db.session.commit()
  except ErrorException as ex:
    print(ex.message)
    print("Errors: ", ex.errors)
  except Exception as ex:
    raise ex
    
#Cria o Plano Mensal Com Teste de 7 dias
plan = Plan.query.filter_by(id = 'plan_mens_teste').first()
if plan is None:
  request = create_plan_request.CreatePlanRequest()
  request.name = "Plano SanarFlix Mensal com 7 Dias de Teste"
  request.currency = "BRL"
  request.interval = "month"
  request.interval_count = 1
  request.billing_type = "prepaid"
  request.trial_period_days = 7
  request.items = [create_plan_item_request.CreatePlanItemRequest()]
  request.items[0].name = "Plano SanarFlix Mensal com 7 Dias de Teste"
  request.items[0].quantity = 1
  request.items[0].pricing_scheme = create_pricing_scheme_request.CreatePricingSchemeRequest()
  request.items[0].pricing_scheme.price = 2450
  try:
    result = plans_controller_instance.create_plan(request)
    assert result is not None
    print('Plano ' + result.name + ' criado')
    plan = Plan(id="plan_mens_teste", name = result.name, mundi_plan_id = result.id)
    db.session.add(plan)
    db.session.commit()
  except ErrorException as ex:
    print(ex.message)
    print("Errors: ", ex.errors)
  except Exception as ex:
    raise ex

#Cria o Plano Trimestral Normal
plan = Plan.query.filter_by(id = 'plan_trim').first()
if plan is None:
  request = create_plan_request.CreatePlanRequest()
  request.name = "Plano SanarFlix Trimestral"
  request.currency = "BRL"
  request.interval = "month"
  request.interval_count = 3
  request.billing_type = "prepaid"
  request.items = [create_plan_item_request.CreatePlanItemRequest()]
  request.items[0].name = "Plano SanarFlix Trimestral"
  request.items[0].quantity = 1
  request.items[0].pricing_scheme = create_pricing_scheme_request.CreatePricingSchemeRequest()
  request.items[0].pricing_scheme.price = 6990
  try:
    result = plans_controller_instance.create_plan(request)
    assert result is not None
    print('Plano ' + result.name + ' criado')
    plan = Plan(id = "plan_trim", name = result.name, mundi_plan_id = result.id)
    db.session.add(plan)
    db.session.commit()
  except ErrorException as ex:
    print(ex.message)
    print("Errors: ", ex.errors)
  except Exception as ex:
    raise ex
    
#Cria o Plano Promocional
plan = Plan.query.filter_by(id = 'plan_promo_yellowbook').first()
if plan is None:
  request = create_plan_request.CreatePlanRequest()
  request.name = "Plano SanarFlix Promocional Com Livro Yellowbook"
  request.currency = "BRL"
  request.interval = "month"
  request.interval_count = 1
  request.billing_type = "prepaid"
  request.items = [create_plan_item_request.CreatePlanItemRequest(), create_plan_item_request.CreatePlanItemRequest()]
  request.items[0].name = "Plano SanarFlix Mensal"
  request.items[0].quantity = 1
  request.items[0].pricing_scheme = create_pricing_scheme_request.CreatePricingSchemeRequest()
  request.items[0].pricing_scheme.price = 2450
  request.items[1].name = "Livro Yellowbook"
  request.items[1].quantity = 1
  request.items[1].cycles = 1
  request.items[1].pricing_scheme = create_pricing_scheme_request.CreatePricingSchemeRequest()
  request.items[1].pricing_scheme.price = 13990
  try:
    result = plans_controller_instance.create_plan(request)
    assert result is not None
    print('Plano ' + result.name + ' criado')
    plan = Plan(id = "plan_promo_yellowbook", name = result.name, mundi_plan_id = result.id)
    db.session.add(plan)
    db.session.commit()
  except ErrorException as ex:
    print(ex.message)
    print("Errors: ", ex.errors)
  except Exception as ex:
    raise ex
  
    
