#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CompraJunto - Sistema de Compras Compartilhadas
Script de inicialização da aplicação web
"""

import os
import sys

# Adiciona o diretório 'api' ao caminho
api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api')
sys.path.insert(0, api_dir)

from app import app

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" " * 15 + "CompraJunto - Compras Compartilhadas")
    print("="*70)
    print("\n🚀 Iniciando servidor web...")
    print("📱 Acesse em: http://127.0.0.1:5000")
    print("⚠️  Pressione CTRL+C para parar o servidor\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
