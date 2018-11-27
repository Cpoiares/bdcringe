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
### Procurar música

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


### Listar as músicas de um artista

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


## Diagramas

#### Conceptual
![image](images/meta1-conceptual.png)

#### Físico
![image](images/meta1-fisico.png)