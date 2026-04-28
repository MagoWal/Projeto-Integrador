caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'()*+,-./:;<=>?@[]^_`{|}~"
controle = 3

def encript(palavra):
    novo = ""
    for i in palavra:
        ende = caracteres.find(i)
        if ende+controle > len(caracteres):
            ende = (ende+controle) - len(caracteres)
        else:
            ende = ende+controle
        novo+=caracteres[ende]
        
    return(novo)
    
def decript(palavra):
    novo = ""
    for i in palavra:
        ende = caracteres.find(i)
        if ende-controle < 0:
            ende = (ende-controle) + len(caracteres)
        else:
            ende = ende-controle
        novo+=caracteres[ende]
        
    return(novo)


def guardar(nome, login, senha):
    login = encript(login)
    senha = encript(senha)
    info = login + "\n" + senha
    nome = nome + ".txt"
    dados = open(nome, "w")
    dados.write(info)
    dados.close


def exibir(conta):
    try:
        conta = conta + ".txt"
        dados = open(conta, "r")
        for linha in dados:
            linha = linha.strip()
            linha = decript(linha)
            print(linha)
        
        dados.close
    except FileNotFoundError:
        print("Conta não encontrada")
    
res = ""

while res != "s":

    res = input("\nO que você deseja fazer?\nCriar -> c\nExibir -> e\nSair -> s\nComando: ")
    res.lower()
    if res == "c":
        nom = input("Nome: ")
        log = input("Login: ")
        sen = input("Senha: ")
        guardar(nom, log, sen)
    elif res == "e":
        nom = input("Conta: ")
        exibir(nom)
