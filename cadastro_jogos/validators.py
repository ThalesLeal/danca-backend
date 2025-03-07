from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email


def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")

    if len(cpf) != 11 or not cpf.isdecimal() or not int(cpf):
        erro = "O CPF informado é inválido"
        raise ValidationError(erro)

    d1 = int(cpf[-2])
    d2 = int(cpf[-1])
    v1 = v2 = 0
    cpf = cpf[:-2]

    for i in range(len(cpf)):
        d = int(cpf[9 - i - 1])
        v1 += d * (9 - i)
        v2 += d * (9 - i - 1)
    v1 = (v1 % 11) % 10
    v2 += v1 * 9
    v2 = (v2 % 11) % 10

    cpf_valido = (d1 == v1) and (d2 == v2)
    if not cpf_valido:
        erro = "O CPF informado é inválido"
        raise ValidationError(erro)

def validar_email(email):
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError("O email informado é inválido")