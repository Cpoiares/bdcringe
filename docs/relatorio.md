---
stylesheet: https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/2.10.0/github-markdown.min.css
body_class: markdown-body
highlight_style: atom-one-dark
displayHeaderFooter: true
pdf_options:
  format: A4
  margin: 30mm 20mm
  displayHeaderFooter: true
  headerTemplate: |-
    <style>
      section {
        margin: 0 auto;
        font-family: Roboto;
        font-size: 8px;
      }
    </style>
    <section>
    </section>
  footerTemplate: |-
    <section>
      <div>
        <span class="pageNumber"></span>
        /
        <span class="totalPages"></span>
      </div>
    </section>
css: |-
  .page-break { page-break-after: always; }
  .markdown-body { font-size: 11px; }
  .markdown-body pre > code { white-space: pre-wrap; }
---
# Projecto Base de Dados
## Relatório Meta 2 (28 Novembro 2018)

## Contactos

| Nome | Email | Número de Estudante | 
|:---|---:|:---|
| Alexandre Faria | afaria@student.dei.uc.pt | 2014226180 |
| Carlos Poiares | cpoiares@student.dei.uc.pt | 2014226236 |


## Table of Contents
1. [Contactos](#Contactos)
2. [Instalação](#Instalação)
3. [Funcionalidades](#Funcionalidades)
    1. [Registo](#Registo)
    2. [Login](#Login)
    3. [Músicas](#Musicas)
4. [Diagramas](#Diagramas)
    1. [Diagrama Conceptual](#Conceptual)
    2. [Diagrama Físico](#Físico)


## Instalação
O projeto foi feito para python 3.

A configuração da ligação com a base de dados está definida em `config.py`

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python3 -m bdcringe.main
```

<div class="page-break"></div>

## Funcionalidades

### Registo

Insere na base de dados um novo utilizador com o username e password fornecidos.
Dá erro de inserção caso já exista algum utilizador com o mesmo username devido ao campo `username`
servir de chave primária (unique).

```sql
INSERT
INTO
    utilizador
    (username, password)
VALUES
    (%s, %s)
returning
    username, editor
```

### Login

Dado um nome e password de um utilizador, verifica se existe na base de dados.
```sql
SELECT
    username, editor
FROM
    utilizador
WHERE
    username LIKE %s and
    password LIKE %s
```

<div class="page-break"></div>

### Promover utilizador a editor

Para promover outro utilizador a editor são necessárias duas operações, uma de pesquisa e uma de atualização.

##### Procurar utilizador

É feita uma listagem de utilizadores sem permissoes de editor com base no nome a procurar para tornar a procura mais fácil para o utilizador.

```sql
SELECT
    nome
FROM
    utilizador
WHERE
    username LIKE %%s% and
    editor = false
```

##### Tornar editor
A partir do username introduzido pelo utilizador altera os seus privilégios de editor.
```sql
UPDATE
   utilizador 
SET
   editor = true 
WHERE
   nome LIKE '%s'
```

<div class="page-break"></div>

### Procurar Artista

Dado um nome de um artista é retornada toda a informação relativa ao artista em questão, retorna erro no caso do artista não existir.

```sql
SELECT
    * 
FROM
    artista
WHERE
    nome LIKE '%s'
```

### Listar as músicas de um Artista

Dado um nome de um artista, devolve todas as músicas dele

```sql
SELECT
    nome,
    data,
    historia
FROM
    musica,
    musica_artista
WHERE
    artista_id = (
        SELECT
            id 
        FROM
            artista 
        WHERE
            nome LIKE '%s'
    ) and
    musica_id = id
```

<div class="page-break"></div>

### Inserir um Album

[comment]: <>  "Definir o que é uma data válida para todos os dados date"
Dado um nome, uma data de lançamento válida, um nome de grupo musical e o nome da editora correspondente, insere um novo album.
O id da editora é obtido através de uma subconsulta.
```sql
INSERT
    INTO
        album
        (nome, lancamento, editora_id, grupo_musical_nome)
        SELECT
            %s,
            %s,
            id,
            %s
        FROM
            editora
        WHERE
            nome LIKE %s
```

### Procura de um Album
Dado um nome de um album devolve toda a sua informação.

```sql
SELECT
    *
FROM
    album
WHERE
    nome LIKE %(like)s ESCAPE '='
```

### Alterar o nome de um Album

Dado um nome original e um novo nome, procura e altera o album.

```sql
UPDATE
    album
SET
    nome = %s
WHERE
    nome LIKE %s
```

### Apagar um album

Dado o nome de um album, remove-o da base de dados.

```sql
DELETE
    FROM
        album
    WHERE
        nome LIKE %s
```

<div class="page-break"></div>

## Criticas


### Escrever uma crítica a um album

É pedido ao utilizador uma pontuaçao e uma justificação textual para essa pontuação e é registada na tabela de críticas.

```sql
INSERT
    INTO
        critica
        (album_nome, utilizador_username, pontuacao, justificacao)
    VALUES
        (%s, %s, %s, %s)
```

<div class="page-break"></div>

### Inserir Editora

Dado um nome, insere uma nova editora na base de dados.

```sql
INSERT
    INTO
        editora
        (nome)
    VALUES
        (%s)
```

### Procurar Editora

Dado um nome devolve toda a informação relativa a essa editora.
```sql
SELECT
    *
FROM
    editora
WHERE
    nome LIKE %%s%
```

### Alterar o nome de uma editora

Dado um nome original e um novo nome, procura e altera a editora.

```sql
UPDATE
    editora
SET
    nome = %s
WHERE
    nome LIKE %s
``` 

### Remover Editora

Dado o nome de um album, remove-o da base de dados.

```sql
DELETE
FROM
    editora
WHERE
    nome LIKE %s
```

### Inserir Grupo Musical
Dado um nome, data de inicio e data de fim, insere um novo grupo musical.

```sql
INSERT
    INTO
        grupo_musical
        (nome, inicio, fim)
    VALUES
        (%s, %s, %s)
```

<div class="page-break"></div>

### Adiciona Artista ao Grupo Musical

Dado um nome de artista e o nome do grupo musical, insere o artista um novo artista_grupo_musical.

```sql
INSERT
    INTO
        artista_grupo_musical
        (artista_id, grupo_musical_nome)
        SELECT
            a.id,
            g.nome
        FROM
            artista a,
            grupo_musical g
        WHERE
            a.nome LIKE %s and
            g.nome LIKE %s
```

### Listar membros de um Grupo Musical 
[comment]: <> "Se calhar pesquisas complexas é melhor explicar assim não"
[comment]: <> "add_artist e add_artist_id suponho que o add_artist seja o meu e seja para apagar -> groups.py"
Dado um nome do grupo musical, lista todos os artista presentes no grupo.
A pesquisa é feita através do id do grupo_musical(nome) na tabela de artista_grupo_musical, 
listando toda informação dos artistas associados ao id do grupo_musical(nome).

```sql
SELECT
    *
FROM
    artista a,
    artista_grupo_musical agm
WHERE
    agm.grupo_musical_nome LIKE %s and
    a.id = agm.artista_id
```
 
### Insere Música
Este processo é feito em dois passos, criando uma entrada na tabela musica e criando posteriormente uma entrada na tabela musica_artista.
#### Criar Musica e inserir na base de dados
Dado um nome da música, uma data de criação válida, um resumo breve da história, género, e nome do album cria uma nova música.

```sql
INSERT 
    INTO
        musica
        (nome, data, historia, genero, album_nome) 
    VALUES
        ('%s', '%s', '%s', '%s', '%s')
```

<div class="page-break"></div>

#### Associar a música a um artista

Dado o nome do artista a quem está associada a música, associa a música ao artista através da tabela musica_artista.
A associação é feita através dos identificadores, o que é devolvido pela subconsulta.
```sql
INSERT 
    INTO
        musica_artista
        (artista_id, musica_id)
        SELECT
            a.id,
            m.id
        FROM
            artista a,
            musica m
        WHERE
            m.nome LIKE '%s' and
            a.nome LIKE '%s'
```
### Procurar Música

Dado um nome é retornada toda a informação geral e a lista de artistas de cada música encontrada.

```sql
SELECT
    m.nome,
    m.data,
    m.historia,
    m.genero,
    a.nome,
    a.data_nascimento
FROM
    artista a,
    musica_artista ma,
    musica m
WHERE
    a.id = ma.artista_id
    and m.id = ma.musica_id
    and m.nome LIKE '%%s%'
```

<div class="page-break"></div>

## Diagramas

#### Conceptual
![image](images/meta1-conceptual.png)

<div class="page-break"></div>

#### Físico
![image](images/meta1-fisico.png)