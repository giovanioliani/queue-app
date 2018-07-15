python3 main.py < tests/input-1 | diff tests/output-1 -

if [ $? -eq "0" ]; then
    echo "Testes foram bem sucedidos"
else
    echo "Saída difere do esperado"
fi
