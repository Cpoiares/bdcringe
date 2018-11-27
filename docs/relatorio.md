# Projecto Base de Dados
## Relatório Meta 2 (28 Novembro 2018)

## Contactos

| Nome | Email | Número de Estudante | 
|:---|---:|:---|
| Alexandre Faria | afaria@student.dei.uc.pt | 2014226180 |
| Carlos Poiares |  cpoiares@student.dei.uc.pt |  2014226236 |


## Table of Contents
1. [Contactos](#Contactos)
2. [Funcionalidades](#Funcionalidades)
    1. [Registo](#Registo)
    2. [Login](#Login)
    3. [Músicas](#Musicas)
3. [Diagramas](#Diagramas)
    1. [Diagrama Conceptual](#Conceptual)
    2. [Diagrama Físico](#Físico)

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
values
    (%s, %s)
```

### Login

Dado um nome e password de um utilizador, verifica se existe na base de dados.
```sql
SELECT
    * 
FROM
    utilizador 
where
    username like %s and
    password like %s
```
### Tornar Editor
##### Procurar utilizador
É feita uma listagem de todos os utilizadores na base de dados para tornar a procura mais fácil para o utilizador.
```sql
SELECT nome
FROM utilizador
```
##### Tornar utilizador
A partir do username introduzido pelo utilizador altera os seus privilégios de editor.
```sql
UPDATE
   utilizador 
SET
   editor = true 
WHERE
   nome like '%s'
```
### Procurar Artista

Dado um nome de um artista é retornada toda a informação relativa ao artista em questão, retorna erro no caso do artista não existir.

```sql
SELECT
    * 
FROM
    artista
WHERE
    nome like '%s'
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
            nome like '%s'
    ) and
    musica_id = id
```

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
            nome like %s
```

### Procura de um Album
Dado um nome de um album devolve toda a sua informação.

```sql
SELECT * 
FROM   album 
WHERE  nome LIKE %(LIKE)s ESCAPE '='
```

### Alterar o nome de um Album

Dado um nome original e um novo nome, procura e altera o album.

```sql
UPDATE album 
SET    nome = %s 
WHERE  nome LIKE %s 
```

### Apagar um album

Dado o nome de um album, remove-o da base de dados.

```sql
DELETE from album 
where nome like %s
```

### Inserir Editora

Dado um nome, insere uma nova editora na base de dados.

```sql
INSERT INTO editora 
            (nome) 
VALUES     (%s) 
```

### Procurar Editora

Dado um nome devolve toda a informação relativa a essa editora.
```sql
SELECT * 
FROM   editora 
WHERE  nome LIKE '%%s%' 
```

### Alterar o nome de uma editora

Dado um nome original e um novo nome, procura e altera a editora.

```sql
UPDATE editora
SET    nome = %s 
WHERE  nome LIKE %s
``` 

### Remover Editora

Dado o nome de um album, remove-o da base de dados.

```sql
DELETE from editora 
where nome like %s
```

### Inserir Grupo Musical
[comment]: <> "Feito de uma forma demasiado manhosa agora olhando para ela, claro que fui eu. Decidir como fazer e incluir depois"
FIX\n
Dado um nome, data de inicio e data de fim, insere um novo grupo musical.

```sql
INSERT
    INTO
        grupo_musical
        (nome, inicio, fim)
    VALUES
        (%s, %s, %s)
```

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
            a.nome like %s and
            g.nome like %s
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
        agm.grupo_musical_nome like %s and
        a.id = agm.artista_id
```
 
### Insere Música
Este processo é feito em dois passos, criando uma entrada na tabela musica e criando posteriormente uma entrada na tabela musica_artista.
#### Criar Musica e inserir na base de dados
[comment]: <> "assumimos que uma música está apenas num albúm ne, pq se estiver em dois diferentes vai ser rip"
Dado um nome da música, uma data de criação válida, um resumo breve da história, género, e nome do album cria uma nova música.

```sql
INSERT 
        INTO
            musica
            (nome, data, historia, genero, album_nome) 
        VALUES
            ('%s', '%s', '%s', '%s', '%s')
```
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
                m.nome like '%s' and
                a.nome like '%s'
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
    and m.nome like '%%s%'
```

## Diagramas

#### Conceptual
![image](images/meta1-conceptual.png)

#### Físico
![image](images/meta1-fisico.png)