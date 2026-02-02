#!/usr/bin/env python3
"""
Script para processar XML do Google Shopping e gerar SKUs pai
Agrupa itens por item_group_id e extrai informações do SKU pai

USO:
    python processar_google_shopping.py arquivo.xml
    
    ou faça upload do XML e execute:
    python processar_google_shopping.py /mnt/user-data/uploads/data.xml
"""

import xml.etree.ElementTree as ET
import csv
import re
import os
import sys
from collections import defaultdict

# Namespace do Google Shopping
NAMESPACE = {'g': 'http://base.google.com/ns/1.0'}

def remover_sufixo_tamanho(titulo):
    """Remove sufixos de tamanho do título (- P, - M, - G, - GG, etc)"""
    # Padrões comuns de tamanho no final do título
    padrao = r'\s*-\s*(PP|P|M|G|GG|XG|EG|XGG|EGG|[0-9]+|ÚNICO|UN|U|UNICO)\s*$'
    titulo_limpo = re.sub(padrao, '', titulo, flags=re.IGNORECASE)
    return titulo_limpo.strip()

def processar_xml(caminho_xml):
    """Processa o XML e agrupa itens por item_group_id"""
    print(f"\n📂 Lendo arquivo: {caminho_xml}")
    print("⏳ Processando XML...")
    
    # Parse do XML
    tree = ET.parse(caminho_xml)
    root = tree.getroot()
    
    # Encontra o canal (channel)
    channel = root.find('channel')
    if channel is None:
        raise ValueError("Tag <channel> não encontrada no XML")
    
    # Agrupa itens por item_group_id
    grupos = defaultdict(list)
    total_itens = 0
    
    # Itera sobre todos os <item>
    for item in channel.findall('item'):
        total_itens += 1
        
        # Extrai dados necessários
        sku_filho = item.findtext('g:id', namespaces=NAMESPACE)
        item_group_id = item.findtext('g:item_group_id', namespaces=NAMESPACE)
        titulo = item.findtext('title')
        imagem = item.findtext('g:image_link', namespaces=NAMESPACE)
        
        # Se não tem item_group_id, usa o próprio id removendo sufixo
        if not item_group_id and sku_filho:
            # Remove sufixo de tamanho do SKU para criar o group_id
            item_group_id = re.sub(r'-[A-Z0-9]+$', '', sku_filho)
        
        if item_group_id:
            grupos[item_group_id].append({
                'sku_filho': sku_filho,
                'titulo': titulo,
                'imagem': imagem
            })
    
    print(f"✅ Total de itens processados: {total_itens}")
    print(f"✅ Total de grupos (SKUs pai) encontrados: {len(grupos)}")
    return grupos

def gerar_skus_pai(grupos):
    """Gera lista de SKUs pai a partir dos grupos"""
    print("\n🔨 Gerando SKUs pai...")
    
    skus_pai = []
    
    for item_group_id, itens in grupos.items():
        # Pega o primeiro item do grupo como referência
        primeiro_item = itens[0]
        
        # Remove sufixo de tamanho do título
        nome_limpo = remover_sufixo_tamanho(primeiro_item['titulo'])
        
        # Pega a primeira imagem
        imagem_url = primeiro_item['imagem']
        
        # Informações do SKU pai
        sku_pai = {
            'sku': item_group_id,
            'name': nome_limpo,
            'image': imagem_url
        }
        
        skus_pai.append(sku_pai)
    
    print(f"✅ Total de SKUs pai gerados: {len(skus_pai)}")
    return skus_pai

def salvar_csv(skus_pai, arquivo_saida='sku_pai.csv'):
    """Salva os SKUs pai em um arquivo CSV"""
    print(f"\n💾 Salvando CSV em {arquivo_saida}...")
    
    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['sku', 'name', 'image'])
        writer.writeheader()
        writer.writerows(skus_pai)
    
    print(f"✅ CSV salvo com sucesso!")
    return arquivo_saida

def salvar_lista_imagens(skus_pai, arquivo_saida='lista_imagens.txt'):
    """Salva lista de URLs de imagens para download externo"""
    print(f"\n💾 Salvando lista de imagens em {arquivo_saida}...")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for sku in skus_pai:
            if sku['image']:
                # Formato: SKU|URL
                f.write(f"{sku['sku']}|{sku['image']}\n")
    
    print(f"✅ Lista de imagens salva!")
    return arquivo_saida

def main():
    """Função principal"""
    print("="*70)
    print("    PROCESSADOR DE XML GOOGLE SHOPPING - GERADOR DE SKUs PAI")
    print("="*70)
    
    # Verifica se foi passado o caminho do XML
    if len(sys.argv) < 2:
        print("\n❌ Erro: Você precisa fornecer o caminho do arquivo XML")
        print("\nUSO:")
        print("    python processar_google_shopping.py arquivo.xml")
        print("\nOu faça upload do XML e execute:")
        print("    python processar_google_shopping.py /mnt/user-data/uploads/data.xml")
        sys.exit(1)
    
    caminho_xml = sys.argv[1]
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_xml):
        print(f"\n❌ Erro: Arquivo não encontrado: {caminho_xml}")
        sys.exit(1)
    
    try:
        # Processa o XML
        grupos = processar_xml(caminho_xml)
        
        # Gera SKUs pai
        skus_pai = gerar_skus_pai(grupos)
        
        # Salva arquivos em pasta local ./outputs/ (criada automaticamente)
        print("\n" + "="*70)
        print("GERANDO ARQUIVOS DE SAÍDA")
        print("="*70)
        outputs_dir = os.path.join(os.getcwd(), 'outputs')
        os.makedirs(outputs_dir, exist_ok=True)
        csv_path = salvar_csv(skus_pai, os.path.join(outputs_dir, 'sku_pai.csv'))
        lista_imagens_path = salvar_lista_imagens(skus_pai, os.path.join(outputs_dir, 'lista_imagens.txt'))
        
        # Resumo
        print("\n" + "="*70)
        print("RESUMO")
        print("="*70)
        print(f"✅ Total de SKUs pai: {len(skus_pai)}")
        print(f"✅ CSV gerado: {csv_path}")
        print(f"✅ Lista de imagens: {lista_imagens_path}")
        print("="*70)
        
        # Mostra alguns exemplos
        print("\n📋 Exemplos de SKUs pai gerados:")
        for i, sku in enumerate(skus_pai[:5], 1):
            print(f"\n{i}. SKU: {sku['sku']}")
            print(f"   Nome: {sku['name'][:70]}{'...' if len(sku['name']) > 70 else ''}")
            print(f"   Imagem: {sku['image'][:60]}...")
        
        if len(skus_pai) > 5:
            print(f"\n... e mais {len(skus_pai) - 5} SKUs pai")
        
        print("\n" + "="*70)
        print("PRÓXIMOS PASSOS")
        print("="*70)
        print("1. Baixe o arquivo 'sku_pai.csv' com todas as informações")
        print("2. Para baixar as imagens, use o arquivo 'lista_imagens.txt'")
        print("   Você pode usar ferramentas como wget, curl ou scripts de download")
        print("   Formato do arquivo: SKU|URL_DA_IMAGEM")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
