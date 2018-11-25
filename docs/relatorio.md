# Base de Dados 2018

# Relatório meta 2 (28 Novembro 2018)

| Nome | Email | Número de Estudante | 
|:---|---:|:---|
| Alexandre Faria | afaria@student.dei.uc.pt | 2014226180 |
| Carlos Poiares |  cpoiares@student.dei.uc.pt |  2014226236 |

# Table of Contents
1. [Funcionalidades](#Funcionalidades)
2. [Procurar música](#Procurar música)
3. [Exemplo](#Exemplo)

## Funcionalidades
### Procurar música

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



## Exemplo