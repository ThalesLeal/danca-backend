from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import factory
from faker import Faker

from cadastro_jogos.models import Instituicao, Regional

UserModel = get_user_model()
faker = Faker("pt_BR")

class RegionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Regional

    nome = faker.name()
    numero = faker.random_int(min=1, max=99)
    cidade = faker.city()
    tipo_regional = faker.random_element(["escolar", "amador", "profissional"])
    

class InstituicaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instituicao

    nome = faker.company()
    cep = faker.postcode(False)
    bairro = faker.bairro()
    logradouro = faker.street_name()
    numero = faker.building_number()
    complemento = faker.word()
    municipio = faker.city()
    pertence_a_regional = faker.boolean()
    tipo_regional = faker.random_element(["escolar", "amador", "profissional"])
    regional = factory.SubFactory(RegionalFactory)
    rede_ensino = faker.random_element(["privada", "estadual", "municipal", "federal"])
    cpf_cnpj = factory.LazyFunction(
        lambda: faker.numerify("###########") 
        if faker.boolean() 
        else faker.numerify("##############")
    )

    



