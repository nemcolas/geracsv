import os
import sys
import requests
from urllib.parse import urlparse
import time

def baixar_imagem(url, sku, pasta_destino='imagens'):
    """Baixa a imagem e salva com o nome do SKU"""
    try:
        # Cria a pasta base e a pasta específica do SKU
        os.makedirs(pasta_destino, exist_ok=True)
        sku_dir = os.path.join(pasta_destino, str(sku))
        os.makedirs(sku_dir, exist_ok=True)

        # Extrai nome/base e extensão da URL
        url_path = urlparse(url).path
        base_name = os.path.basename(url_path)
        extensao = os.path.splitext(base_name)[1]
        if not extensao or extensao.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            extensao = '.jpg'

        # Tenta usar o nome original da imagem quando possível, senão cria um nome baseado no SKU
        if base_name and os.path.splitext(base_name)[0]:
            nome_arquivo = base_name
        else:
            nome_arquivo = f"{sku}{extensao}"

        caminho_completo = os.path.join(sku_dir, nome_arquivo)

        # Se já existe um arquivo com o mesmo nome, gera um nome único acrescentando sufixo _1, _2, ...
        if os.path.exists(caminho_completo):
            base, ext = os.path.splitext(nome_arquivo)
            i = 1
            novo_nome = f"{base}_{i}{ext}"
            while os.path.exists(os.path.join(sku_dir, novo_nome)):
                i += 1
                novo_nome = f"{base}_{i}{ext}"
            caminho_completo = os.path.join(sku_dir, novo_nome)
        
        # Baixa a imagem
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()
        
        with open(caminho_completo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return 'success'
    except Exception as e:
        return f'error: {str(e)[:50]}'

def main():
    """Função principal"""
    print("="*70)
    print("    DOWNLOADER DE IMAGENS - GOOGLE SHOPPING")
    print("="*70)
    
    # Verifica argumentos
    if len(sys.argv) < 2:
        print("\n❌ Erro: Você precisa fornecer o arquivo lista_imagens.txt")
        print("\nUSO:")
        print("    python baixar_imagens.py lista_imagens.txt")
        sys.exit(1)
    
    arquivo_lista = sys.argv[1]
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_lista):
        print(f"\n❌ Erro: Arquivo não encontrado: {arquivo_lista}")
        sys.exit(1)
    
    print(f"\n📂 Lendo arquivo: {arquivo_lista}")
    
    # Lê a lista de imagens
    with open(arquivo_lista, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]
    
    total = len(linhas)
    print(f"📊 Total de imagens a baixar: {total}")
    print("\n🚀 Iniciando download...\n")
    
    # Estatísticas
    sucesso = 0
    existentes = 0
    erros = 0
    
    # Baixa cada imagem
    for i, linha in enumerate(linhas, 1):
        partes = linha.split('|')
        if len(partes) != 2:
            print(f"  Linha inválida: {linha[:60]}")
            erros += 1
            continue
        
        sku, url = partes
        
        # Mostra progresso a cada 50 imagens
        if i % 50 == 0:
            print(f"📥 Progresso: {i}/{total} ({i*100//total}%) - "
                  f"OK: {sucesso}, Já existe: {existentes}, Erros: {erros}")
        
        # Baixa a imagem
        resultado = baixar_imagem(url, sku)
        
        if resultado == 'success':
            sucesso += 1
        elif resultado == 'exists':
            existentes += 1
        else:
            erros += 1
            if i <= 10:  # Mostra os primeiros erros
                print(f"  Erro em {sku}: {resultado}")
        
        # Delay pra não sobrecarregar o servidor
        time.sleep(0.1)
    
    # Resumo final
    print("\n" + "="*70)
    print("RESUMO DO DOWNLOAD")
    print("="*70)
    print(f" Total de imagens: {total}")
    print(f" Baixadas com sucesso: {sucesso}")
    print(f"ℹ  Já existiam: {existentes}")
    print(f" Erros: {erros}")
    print(f" Pasta de destino: imagens/")
    print("="*70)

if __name__ == '__main__':
    main()
