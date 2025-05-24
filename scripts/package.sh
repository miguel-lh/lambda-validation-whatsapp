#!/bin/bash
set -e

echo "Empaquetando función Lambda..."
zip -r lambda_function.zip src/ config/ -x "*/__pycache__/*" "*.pyc"
echo "Empaquetado completo."
