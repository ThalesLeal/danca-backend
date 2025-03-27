from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email


def validar_cpf(cpf):
    cpf = "".join(filter(str.isdigit, str(cpf)))
    mensagem = "O CPF informado é inválido"

    if len(set(cpf)) == 1 or len(cpf) != 11:
        raise ValidationError(mensagem)

    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = 11 - (soma % 11)
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(cpf[9]):
        raise ValidationError(mensagem)

    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = 11 - (soma % 11)
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(cpf[10]):
        raise ValidationError(mensagem)
    
def validar_cnpj(cnpj):
    cnpj = "".join(filter(str.isdigit, str(cnpj)))
    mensagem = "O CNPJ informado é inválido"

    if len(set(cnpj)) == 1 or len(cnpj) != 14:
        raise ValidationError(mensagem)

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = 11 - (soma % 11)
    if resto >= 10:
        resto = 0
    if resto != int(cnpj[12]):
        raise ValidationError(mensagem)

    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = 11 - (soma % 11)
    if resto >= 10:
        resto = 0
    if resto != int(cnpj[13]):
        raise ValidationError(mensagem)

def validar_cpf_cnpj(valor):
    valor = "".join(filter(str.isdigit, str(valor)))

    if len(valor) == 11:
        validar_cpf(valor)
    elif len(valor) == 14:
        validar_cnpj(valor)
    else:
        raise ValidationError("O CPF ou CNPJ informado é inválido")

def validar_email(email):
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError("O email informado é inválido")