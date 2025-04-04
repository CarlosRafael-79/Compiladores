Compilador - Propriedade de Carlos Rafael Nogueira de Arruda Silva

Este documento descreve como executar o compilador desenvolvido por Carlos Rafael Nogueira de Arruda Silva.

REQUISITOS:
- Python: Certifique-se de que o Python esteja instalado em seu sistema, preferencialmente na versão mais recente. 
  Você pode verificar a versão do Python instalada usando o comando:
  
    python --version

- PLY: O compilador depende da biblioteca PLY (Python Lex-Yacc). Para instalá-la, execute o seguinte comando no terminal:

    pip install ply

FUNCIONAMENTO:
1. Código de entrada:
   - Os arquivos de código-fonte que serão compilados devem ser colocados na pasta:
   
     /parteUm/entradas

   - Para compilar um código específico, você deve modificar o caminho do arquivo de entrada no script:

     /parteUm/main.py

2. Execução:
   - Após iniciar a compilação, o sistema realizará a análise léxica, sintática e semântica do código.
   - Se o código não contiver erros (léxicos, sintáticos ou semânticos), o compilador gerará o código objeto no arquivo:

     /parteUm/codigo.txt

3. Execução do código objeto:
   - Para executar o código objeto gerado, basta rodar o script localizado em:

     /parteDois/main.py

   - O script irá ler o arquivo codigo.txt e executá-lo conforme as instruções presentes.

OBSERVAÇÕES:
- Certifique-se de que os caminhos para os arquivos de entrada e saída estão corretos antes de executar o compilador.
- Em caso de erros durante a execução, o compilador exibirá mensagens detalhadas indicando a linha e o tipo de erro (léxico, sintático ou semântico).
