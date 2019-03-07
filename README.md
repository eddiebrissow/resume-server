# Resume Server

## Instalação:

Clonar o repositorio:

`$ git clone https://github.com/eddiebrissow/resume-server`

Dentro da pasta 'resume-server' executar os seguintes comandos para gerar a base de dados:

`$ python manager.py makemigrations`

`$ python manager.py migrate`

Para criar o super usuario:

`$ python manager.py createsuperuser`

Para iniciar o serviço:

`$ python manager.py runserver`


#API

### Permissões

Para criar e alterar as permissões de um usuario basta acessar o endereço http://127.0.0.1:8000/admin/ e fazer as 
alterações conforme a necesidade.

### User

Criar um novo usuário:
    
    Metodo: POST
    Autenticação: Nenhuma
    Parâmetros: {
    "username": "1234",
    "password": "1234",
    "email": "1234@1234.com"
    }
    Url: http://localhost:8000/users/
    
### Login

O sistema autentica um usuário utlizando Oath2, é necessário requisitar um token
e depois enviar o token na Header de Authorization.

Requisitar um token:

    Metodo: GET
    Url:  http://localhost:8000/o/token/?grant_type=password&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&username={USERNAME}&password={PASSWORD}

A resposta contém o "access_token", que será necessario para requisições que necessitam de autenticação.

### Resume

O usuário logado poderá criar, atualizar e baixar um curriculo (Resume).

Criar um Resume:

    Metodo: POST
    Autenticação: Oath2
    Parâmetros: {
    "file": arquivo_a_ser_carregado
    }
    Url: http://localhost:8000/resumes/
    
Atualizar um Resume:

    Metodo: PUT
    Autenticação: Oath2
    Parâmetros: {
    "file": arquivo_a_ser_carregado
    }
    Url: http://localhost:8000/resumes/<int:resume_id>
    
Baixar um Resume:

    Metodo: PUT
    Autenticação: Oath2
    Url: http://localhost:8000/resumes/<str:username>/<str:filename>
    

Listar Resumes:

    Metodo: GET
    Autenticação: Oath2
    Url: http://localhost:8000/resumes/<int:resume_id>
    
    
Ordernação:

    Metodo: GET
    Autenticação: Oath2
    Url: http://localhost:8000/resumes?ordering=<campo_requisitado>
    
Filtrar Resumes:

    Metodo: GET
    Autenticação: Oath2
    Url: http://localhost:8000/resumes?<campo_requisitado>=<valor_do_campo>

    