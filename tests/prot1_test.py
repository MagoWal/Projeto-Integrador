from prot1 import encript, decript, guardar, exibir, recolher_dados, verificar_login_disponivel, verificar_senha, main
#Importar funções do código principal


def test_encript(): #Testar função encript

    texto_original = 'abc' #Entrada fixa
    texto_encriptado = encript(texto_original) #Utilizar função

    print(texto_encriptado)
    assert texto_encriptado == 'def' #Verificar se a saída está correta

    
def test_decript(): #Testar função decript

    texto_encriptado = 'def' #Entrada fixa
    texto_original = decript(texto_encriptado) #Utilizar função

    print(texto_original)
    assert texto_original == 'abc' #Verificar se a saída está correta


def test_guardar(mocker): #Testar função guardar

    arquivo = 'login' #Nome do arquivo criado

    import os
    if os.path.exists(arquivo): #Garantir que o arquivo não exista antes do teste
        os.remove(arquivo)

    mock_encript = mocker.patch(
        'prot1.encript', #Simula a função encript para isolar o teste da lógica de criptografia
        side_effect=lambda x: f'encriptado({x})') 
    informacoes = [
        arquivo, #Entrada fixa
        'nome', 
        'senha', 
        'telefone', 
        'escolaridade', 
        'experiencias', 
        'interesse'
    ] 
    guardar(informacoes) #Utilizar função
    
    with open(f'{arquivo}.txt', 'r') as info: #Abrir e mostrar conteúdo
        conteudo = info.read()
        print(conteudo)

    mock_encript.assert_any_call('nome') #Verificar se a função encript foi chamada com o argumento "nome"
    assert '-Nome:' in conteudo #Verificar se o conteúdo "-Nome:" foi salvo
    assert 'encriptado(nome)' in conteudo #Verificar se o resultado da função encript foi salvo
    assert mock_encript.call_count == 7 #Verificar se a função encript foi chamada para cada informação da lista


def test_exibir(mocker): #Testar função exibir:

    mock_decript = mocker.patch( #Simula a função decript para isolar o teste da lógica de descriptografia
        'prot1.decript',
        side_effect=lambda x: f'decriptado({x})'
    )

    mock_print = mocker.patch('builtins.print') #Simula a função print para verificar o que está sendo impresso

    exibir('login') #Utilizar função

    assert mock_decript.call_count == 35 #Verificar se a função decript foi chamada para cada linha que não começa com "-"
    print(mock_decript.call_args_list) #Mostrar as chamadas feitas à função decript
    mock_decript.assert_any_call('encriptado(nome)') #Verificar se a função decript foi chamada com o argumento "encriptado(nome)"
    mock_print.assert_any_call('decriptado(encriptado(nome))') #Verificar se a função print foi chamada com o resultado da função decript


def test_recolher_dados(mocker): #Testar função recolher_dados

    mocker.patch( #Simular os inputs
        'builtins.input',
        side_effect=[ 
            'login',
            'nome', 
            'senha', 
            'telefone', 
            'escolaridade', 
            'experiencias', 
            'interesse'
        ] 
    )

    resultado = recolher_dados() #Utilizar função

    assert resultado == [ #Verificar se todo os dados estão corretos
        'login', 
        'nome', 
        'senha', 
        'telefone', 
        'escolaridade', 
        'experiencias', 
        'interesse'
    ] 


def test_verificar_login_disponivel(mocker): #Testar função verificar_login_disponivel

    mocker.patch('os.path.exists', return_value=False) #Simular que o arquivo não existe

    assert verificar_login_disponivel('novo_login') == True #Verificar se a função retorna True para um login disponível

    mocker.patch('os.path.exists', return_value=True) #Simular que o arquivo existe

    assert verificar_login_disponivel('login_existente') == False #Verificar se a função retorna False para um login já existente


def test_verificar_senha(mocker): #Testar função verificar_senha

    mocker.patch('os.path.exists', return_value=True) #Simular que o arquivo existe

    conteudo_valido = "\n" * 5 + "encriptado(senha_correta)\n" #Criar um conteúdo com 5 linhas vazias e a senha na 6ª linha

    mocker.patch('builtins.open', mocker.mock_open(read_data=conteudo_valido)) #Simular o conteúdo do arquivo com a senha correta encriptada

    mocker.patch('prot1.decript', return_value='senha_correta') #Mockar a função decript do seu arquivo prot1 para retornar 'senha_correta'

    assert verificar_senha('login', '') == False #Verificar se a função retorna False para senha vazia
    assert verificar_senha('', 'senha_correta') == False #Verificar se a função retorna False para login vazio 

    assert verificar_senha('login', 'senha_correta') == True #Verificar se a função retorna True para a senha correta
    assert verificar_senha('login', 'senha_incorreta') == False #Verificar se a função retorna False para a senha incorreta


def test_main(mocker): #Testar função main

    mock_input = mocker.patch( #Simular os inputs para criar uma conta e depois sair
        'builtins.input',
        side_effect=[
            '1',             # comando
            'login',
            'nome',
            'senha',
            '9999',
            'medio',
            'curso',
            'python',
            '',              # pressione qualquer tecla
            '3',             # sair
            ''
        ]
    )

    mocker.patch('prot1.verificar_login_disponivel', return_value=True) #Simular que o login está disponível

    mock_guardar = mocker.patch('prot1.guardar') #Simular a função guardar para verificar se ela é chamada

    main() #Utilizar função

    assert mock_guardar.called #Verificar se a função guardar foi chamada durante a execução do main