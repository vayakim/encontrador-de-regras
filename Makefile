#Autor : Vinicius Kamiya
#instalar dependencias
install:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt

#executar o programa
run:
	@echo "Boas vindas ao encontrador de regras! Autor: Vinicius Kamiya"
	@echo "Executando o programa..."
	@echo "Por favor, acesse o link http://localhost:8000 no seu navegador para visualizar o aplicativo."
	python codigo/code_v2/run.py

#instalar dependencias e executar o programa
all: install run
	@echo "Instalação e execução concluída com sucesso!"