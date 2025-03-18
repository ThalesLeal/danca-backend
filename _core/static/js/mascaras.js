$(document).ready(function () {
	$(".mask-data").mask("00/00/0000");
	$(".mask-cpf").mask("000.000.000-00", { reverse: true });
	$(".mask-cnpj").mask("00.000.000/0000-00", { reverse: true });
	$(".mask-cep").mask("00000-000");
	$(".mask-num-regional").mask("000");
	$(".mask-telefone").mask(mascara_telefone, mascara_telefone_opts);
});

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

function cpf(v){
    v=v.replace(/\D/g,"")                    //Remove tudo o que não é dígito
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
                                             //de novo (para o segundo bloco de números)
    v=v.replace(/(\d{3})(\d{1,2})$/,"$1-$2") //Coloca um hífen entre o terceiro e o quarto dígitos
    return v
}
