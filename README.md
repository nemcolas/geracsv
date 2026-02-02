# Processador de XML Google Shopping - Gerador de SKUs Pai

Scripts para processar XML do Google Shopping, agrupar produtos por `item_group_id` e gerar SKUs pai com suas respectivas informações.

## 📁 Arquivos

1. **processar_google_shopping.py** - Script principal que processa o XML
2. **baixar_imagens.py** - Script auxiliar para baixar as imagens
3. **README.md** - Este arquivo com instruções

## 🚀 Como Usar

### Passo 1: Obter o XML

Baixe o arquivo XML do Google Shopping:
```bash
# Opção 1: Via navegador
Acesse: https://verline.com.br/media/feed/data.xml
Salve o arquivo como: data.xml

# Opção 2: Via linha de comando (se tiver wget ou curl)
wget https://verline.com.br/media/feed/data.xml
# ou
curl -O https://verline.com.br/media/feed/data.xml
```

### Passo 2: Processar o XML

```bash
python processar_google_shopping.py data.xml
```

Este comando irá:
- ✅ Ler e processar o XML
- ✅ Agrupar itens por `item_group_id`
- ✅ Gerar SKUs pai (removendo sufixos de tamanho dos títulos)
- ✅ Criar arquivo `sku_pai.csv` com as colunas:
  - `sku` - SKU do produto pai
  - `name` - Nome do produto (sem sufixo de tamanho)
  - `image` - URL da primeira imagem do grupo
- ✅ Criar arquivo `lista_imagens.txt` com SKU|URL para download

### Passo 3: Baixar as Imagens (Opcional)

```bash
python baixar_imagens.py lista_imagens.txt
```

Este comando irá:
- 📥 Baixar todas as imagens listadas
- 💾 Salvar com o nome do SKU (ex: 3314V07.jpg)
- 📁 Criar pasta `imagens/` com todos os arquivos

## 📊 Estrutura do XML

O script espera XML no padrão Google Shopping:

```xml
<rss xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <item>
      <g:id>3314V07-P</g:id>
      <g:item_group_id>3314V07</g:item_group_id>
      <title>Vestido Longo Estampado - P</title>
      <g:image_link>https://exemplo.com/imagem.jpg</g:image_link>
      ...
    </item>
    <item>
      <g:id>3314V07-M</g:id>
      <g:item_group_id>3314V07</g:item_group_id>
      <title>Vestido Longo Estampado - M</title>
      <g:image_link>https://exemplo.com/imagem.jpg</g:image_link>
      ...
    </item>
  </channel>
</rss>
```

## 🎯 Lógica de Processamento

1. **Agrupamento**: Itens são agrupados por `<g:item_group_id>`
2. **SKU Pai**: O valor de `item_group_id` vira o SKU pai
3. **Nome Limpo**: Remove sufixos de tamanho (- P, - M, - G, - GG, etc)
4. **Imagem**: Usa a primeira imagem encontrada no grupo

### Exemplo de Transformação

**XML (SKUs Filhos):**
- `3314V07-P` → Vestido Longo Estampado - P
- `3314V07-M` → Vestido Longo Estampado - M
- `3314V07-G` → Vestido Longo Estampado - G

**CSV (SKU Pai):**
- SKU: `3314V07`
- Name: `Vestido Longo Estampado`
- Image: URL da primeira imagem

## 📋 Formato dos Arquivos de Saída

### sku_pai.csv
```csv
sku,name,image
3314V07,Vestido Longo Estampado,https://exemplo.com/imagem1.jpg
3315V08,Blusa Casual Lisa,https://exemplo.com/imagem2.jpg
```

### lista_imagens.txt
```
3314V07|https://exemplo.com/imagem1.jpg
3315V08|https://exemplo.com/imagem2.jpg
```

## 🔧 Requisitos

```bash
# Apenas para o script principal (processar_google_shopping.py)
- Python 3.6+
- Nenhuma biblioteca externa necessária (usa apenas bibliotecas padrão)

# Para o script de download de imagens (baixar_imagens.py)
pip install requests
```

## ⚙️ Sufixos de Tamanho Reconhecidos

O script remove automaticamente estes sufixos dos títulos:
- PP, P, M, G, GG, XG, EG, XGG, EGG
- ÚNICO, UN, U, UNICO
- Números (ex: - 38, - 40)

Padrão: `nome - TAMANHO` → `nome`

## 💡 Dicas

1. **Grande Volume**: Para XMLs muito grandes, o processamento pode levar alguns minutos
2. **Download de Imagens**: O script adiciona um delay de 0.1s entre downloads para não sobrecarregar o servidor
3. **Imagens Existentes**: Se uma imagem já foi baixada, o script pula automaticamente
4. **Formato de Imagem**: O script detecta automaticamente a extensão (.jpg, .png, etc)

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique se o caminho do XML está correto
- Use caminho absoluto se necessário: `/caminho/completo/data.xml`

### Erro ao baixar imagens
- Verifique sua conexão com a internet
- Algumas URLs podem estar inválidas ou inacessíveis
- O script continua mesmo com erros individuais

### XML mal formatado
- Certifique-se de que o XML está no padrão Google Shopping
- Verifique se tem a tag `<channel>` e namespace correto

## 📞 Suporte

Se encontrar problemas:
1. Verifique se o XML está no formato correto
2. Confira os requisitos do Python
3. Revise as mensagens de erro para detalhes
