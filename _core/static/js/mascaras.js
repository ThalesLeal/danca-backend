$(document).ready(function () {
    // Máscaras padrão
    $(".mask-data").mask("00/00/0000");
    $(".mask-cpf").mask("000.000.000-00", { reverse: true });
    $(".mask-cnpj").mask("00.000.000/0000-00", { reverse: true });
    $(".mask-cep").mask("00000-000");
    $(".mask-num-regional").mask("000");
    $(".mask-telefone").mask(mascara_telefone, mascara_telefone_opts);

    // Máscara dinâmica para CPF ou CNPJ
    $(".mask-cpf-cnpj").keydown(function () {
        try {
            $(".mask-cpf-cnpj").unmask();
        } catch (e) {}

        var tamanho = $(".mask-cpf-cnpj").val().length;

        if (tamanho < 11) {
            $(".mask-cpf-cnpj").mask("999.999.999-99");
        } else {
            $(".mask-cpf-cnpj").mask("99.999.999/9999-99");
        }

        var elem = this;
        setTimeout(function () {
            elem.selectionStart = elem.selectionEnd = 10000;
        }, 0);

        var currentValue = $(this).val();
        $(this).val('');
        $(this).val(currentValue);
    });

    // Máscara para valores monetários
    $(".mask-valor").on("input", function () {
        aplicarMascaraMoeda(this);
    });
});

// Função para máscara de telefone
const mascara_telefone = function (val) {
    return val.replace(/\D/g, "").length === 11
        ? "(00) 00000-0000"
        : "(00) 0000-00009";
};

const mascara_telefone_opts = {
    onKeyPress: function (val, e, field, options) {
        field.mask(mascara_telefone.apply({}, arguments), options);
    },
};

// Função para aplicar máscara de moeda
function aplicarMascaraMoeda(input) {
    let valor = input.value.replace(/\D/g, ""); // Remove tudo que não é dígito
    valor = (valor / 100).toFixed(2) + ""; // Divide por 100 e fixa 2 casas decimais
    valor = valor.replace(".", ","); // Substitui ponto por vírgula
    valor = valor.replace(/\B(?=(\d{3})+(?!\d))/g, "."); // Adiciona separadores de milhar
    input.value = "R$ " + valor; // Adiciona o prefixo "R$"
}

// Função para formatar CPF
function cpf(v) {
    v = v.replace(/\D/g, ""); // Remove tudo o que não é dígito
    v = v.replace(/(\d{3})(\d)/, "$1.$2"); // Coloca um ponto entre o terceiro e o quarto dígitos
    v = v.replace(/(\d{3})(\d)/, "$1.$2"); // Coloca um ponto entre o terceiro e o quarto dígitos novamente
    v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2"); // Coloca um hífen entre o terceiro e o quarto dígitos
    return v;
}

// Evento para buscar CEP
document.addEventListener('DOMContentLoaded', function () {
    var inputCep = document.getElementById('id_cep');

    if (inputCep) {
        inputCep.addEventListener('input', function () {
            if (document.activeElement === inputCep) {
                var CEP = inputCep.value.replace(/\D/g, '');

                if (CEP.length === 8) {
                    var url = 'https://viacep.com.br/ws/' + CEP + '/json/';

                    fetch(url)
                        .then(response => response.json())
                        .then(dados => {
                            if (!dados.erro) {
                                document.getElementById("id_logradouro").value = dados.logradouro;
                                document.getElementById("id_bairro").value = dados.bairro;
                                document.getElementById("id_municipio").value = dados.localidade;
                                document.getElementById('id_numero').focus();
                            } else {
                                alert("CEP não encontrado");
                                document.getElementById("id_logradouro").value = "";
                                document.getElementById("id_bairro").value = "";
                                document.getElementById("id_municipio").value = "";
                            }
                        });
                }
            }
        });
    }
});