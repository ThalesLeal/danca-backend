# Como Testar Pagamento com Cartão

## Dados de Cartão de Teste

### Para PagSeguro (Sandbox)
Use os seguintes dados para testar pagamentos aprovados:

**Cartão Aprovado:**
- Número: `4111 1111 1111 1111`
- CVV: `123`
- Validade: `12/2025`
- Nome: `JOÃO DA SILVA`

### Para InfinitePay
Use os seguintes dados para testar pagamentos aprovados:

**Cartão Aprovado:**
- Número: `4111 1111 1111 1111`
- CVV: `123`
- Validade: `12/2025`
- Nome: `JOÃO DA SILVA`

## Como Testar no Frontend

1. Acesse a página de Inscrições
2. Clique no botão "Pagar" em uma inscrição
3. Selecione "Cartão de Crédito"
4. Preencha os dados do cartão de teste
5. Clique em "Pagar"

## Configuração Necessária

Antes de testar, configure as credenciais no arquivo `.env`:

```bash
# Para PagSeguro
PAGSEGURO_EMAIL=seu_email@exemplo.com
PAGSEGURO_TOKEN=seu_token_sandbox

# Para InfinitePay
INFINITEPAY_API_KEY=sua_api_key
```

## URLs de Teste

- **PagSeguro Sandbox**: https://sandbox.api.pagseguro.com
- **InfinitePay**: https://api.infinitepay.io.br

## Status de Resposta

- `pago`: Pagamento aprovado
- `pendente`: Pagamento aguardando confirmação
- `cancelado`: Pagamento cancelado

## Observações Importantes

⚠️ **IMPORTANTE**: Esses cartões de teste funcionam APENAS em ambiente de desenvolvimento/sandbox. Nunca use em produção!

Para produção, você precisará:
1. Solicitar credenciais reais no gateway escolhido
2. Configurar as chaves de produção no servidor
3. Usar cartões reais dos clientes

