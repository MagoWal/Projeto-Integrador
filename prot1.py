import os

#Caracteres usados para fazer a encriptação
caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'()*+,-./:;<=>?@[]^_`{|}~ "
#Indica quantas casas para o lado irão ser movidas na encriptação
controle = 3

def encript(palavra): #encripta uma PALAVRA
    novo = "" #Resultado da palavra encriptada
    for i in palavra: #Ele vai circular cada caracter da palavra 
        ende = caracteres.find(i) #Achar o ENDEreço (index) dela na lista de caracteres
        
        #Achado o endereço nos caracteres, vamos mover (Controle) casas para direita 
        if ende+controle > len(caracteres): #Caso o endereço achado seja maior que a lista
            ende = (ende+controle) - len(caracteres) #Ela volta pro inicio
        else:
            ende = ende+controle
        novo+=caracteres[ende] #adiciona o caracter encriptado em NOVO
        
    return(novo)
    
def decript(palavra): #Decodificação - Basicamente o mesmo que encriptar, mas as casas movidas são para esquerda
    novo = ""
    for i in palavra:
        ende = caracteres.find(i)
        #O caso de erro dá se o endereço for menor que 0, já que se move para esquerda
        if ende-controle < 0: 
            ende = (ende-controle) + len(caracteres)
        else:
            ende = ende-controle
        novo+=caracteres[ende]
        
    return(novo)


def guardar(info): #guarda as informações num bloco de notas separado
    #info é uma LISTA com as informações do usuário
    
    i = 0
    arquivo = info[0] + ".txt" #o arquivo criado terá o nome de LOGIN da pessoa
    dados = open(arquivo, "a") #já que SEMPRE o primeiro elemento da lista é o LOGIN, pegamos o info[0]
    while i < len(info):
        dado = encript(info[i]) #Encriptamos cada dado (temos que ser sigilosos)
        if i == 0:
            dados.write(f"-Login:\n{dado}\n") #Note que "-Login:" também irá para o arquivo, porém não será encriptado
        if i == 1:
            dados.write(f"-Nome:\n{dado}\n") #Ele será incluso no arquivo para quando for exibido as informações estarem intuitivas
        if i == 2:
            dados.write(f"-Senha:\n{dado}\n") #Não há problemas quando for decriptar porque temos "-" antes
        if i == 3:
            dados.write(f"-Telefone:\n{dado}\n")
        if i == 4:
            dados.write(f"-Escolaridade:\n{dado}\n")
        if i == 5:
            dados.write(f"-Experiências:\n{dado}\n")
        if i == 6:
            dados.write(f"-Áreas de interesse:\n{dado}\n")
        
        i+=1
    
    dados.close()

def exibir(conta): #Exibe uma conta (se existir uma) com base no LOGIN
    try:#tenta o código, se não ouver arquivo com aquele LOGIN, roda o EXCEPT
        conta = conta + ".txt"
        dados = open(conta, "r") #dados é o documento de texto
        
        
        for linha in dados: #percorre cada LINHA de DADOS
            linha = linha.strip() #isso serve para tirar "\n" do texto
            
            if linha[0] == "-": #Caso a linha tenha um "-" antes, ela não será decodificada
                print(linha)
                continue
                
            linha = decript(linha)
            print(linha)
        
        dados.close
        
    except FileNotFoundError: #caso der erro, print isso aqui
        print("Conta não encontrada")

def recolher_dados(): #recolhe dados do usuário e devolve uma LISTA
    login = input("Login: ")
    nome = input("Nome: ")
    senha = input("Senha: ")
    telefone = input("Telefone: ")
    escolaridade = input("Escolaridade: ")
    carreira = input("Comente (se houver) seus cursos realizados e/ou experiências profissionais:\n" )
    interesse = input("Comente suas áreas de interesse:\n" )

    info = [login, nome, senha, telefone, escolaridade, carreira, interesse]
    
    return info

def verificar_login_disponivel(login):
    if login == "":
        return False
    
    arquivo = login + ".txt"
    if os.path.exists(arquivo):
        print("Já existe uma conta com esse login.")
        return False
    
    return True


def verificar_senha(login, senha):
    if login == "" or senha == "":
        return False
    
    arquivo = login + ".txt"
    
    if not os.path.exists(arquivo):
        print("Conta não encontrada.")
        return False
    
    with open(arquivo, "r") as dados:
        linhas = dados.readlines()
        senha_correta = decript(linhas[5].strip())
    
    if senha != senha_correta:
        print("Senha incorreta.")
        return False
    
    return True

    


# Basicamente, o fluxo do código todo
# a RESposta sempre começa vazia (""), ent ele pede um dos comandos abaixo
# caso res for "s", o programa é terminado
# ao final de cada ação, o programa vai pedir para pressionar qualquer tecla
# isso é feito para o usuário poder ler a informação antes dela ser apagada pelo código indicado
# Por fim, mas não menos importante
# Note que se você quiser fazer login, está escrito "Já tem uma conta? Entre aqui!"



def main():
    res = ""
    
    while res != "3":

        res = input("\nO que você deseja fazer?\nCriar uma conta -> 1\nJá tem uma conta? Entre aqui! -> 2\nSair -> 3\nComando: ")
        res.lower()
        
        if res == "1":
            informacao = recolher_dados()
            if verificar_login_disponivel(informacao[0]):
                guardar(informacao)
            
        elif res == "2":
            nom = input("Login: ")
            sen = input("\nSenha: ")
            
            if verificar_senha(nom, sen):
                exibir(nom)
        
        input("\n\nPressione qualquer coisa para sair.\n" )
        os.system('cls' if os.name == 'nt' else 'clear') #código apagador de terminais
        
        #Mais opções podem ser adicionadas

if __name__ == "__main__":
    main()