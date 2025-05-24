#!/bin/bash
set -e

echo "Limpiando empaquetado anterior..."
rm -f lambda_function
mkdir -p lambda_buil

# Instalar requerimientos dentro de lambda_build
pip install -r requirements.txt -t lambda_build/

# Copiar código fuente a la carpeta build
cp -r src lambda_build/
cp -r config lambda_build/

# Crear el zip con todo el contenido
cd lambda_build
zip -r ../lambda_function.zip .
cd ..

ls -lh lambda_function.zip
