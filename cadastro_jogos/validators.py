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

def validar_email(email):
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError("O email informado é inválido")