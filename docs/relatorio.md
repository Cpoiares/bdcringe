# Base de Dados 2018

# Relatório meta 2 (28 Novembro 2018)

# Table of Contents
1. [Contactos](#Contactos)
2. [Funcionalidades](#Funcionalidades)
    1. [Músicas](#Musicas)
3. [Diagrama Conceptual](#conceptual)
4. [Diagrama Físico](#fisico)


### Contactos

| Nome | Email | Número de Estudante | 
|:---|---:|:---|
| Alexandre Faria | afaria@student.dei.uc.pt | 2014226180 |
| Carlos Poiares |  cpoiares@student.dei.uc.pt |  2014226236 |


## Funcionalidades


### Procurar música

Dado um nome é retornada toda a informação geral de uma música e tambem a lista de artistas

```sql
select
    m.nome,
    m.data,
    m.historia,
    m.genero,
    a.nome,
    a.data_nascimento                         
from
    artista a,
    musica_artista ma,
    musica m                         
where
    a.id = ma.artista_id 
    and                               m.id = ma.musica_id 
    and                               m.nome like '%s'
```