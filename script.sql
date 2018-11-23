CREATE TABLE musica (
  id			 SERIAL,
  nome			 VARCHAR(512) NOT NULL,
  data			 DATE,
  historia		 VARCHAR(512),
  genero			 VARCHAR(512),
  ficheiro BYTEA,
  extensao VARCHAR(512),
  album_nome		 VARCHAR(512) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE compositor (
  artista_id BIGINT,
  PRIMARY KEY(artista_id)
);

CREATE TABLE album (
  nome		 VARCHAR(512),
  lancamento	 DATE,
  editora_id	 BIGINT NOT NULL,
  grupo_musical_nome VARCHAR(512) NOT NULL,
  PRIMARY KEY(nome)
);

CREATE TABLE grupo_musical (
  nome	 VARCHAR(512),
  inicio DATE,
  fim	 DATE,
  PRIMARY KEY(nome)
);

CREATE TABLE concerto (
  id		 SERIAL,
  data		 DATE,
  morada		 VARCHAR(512),
  grupo_musical_nome VARCHAR(512) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE critica (
  pontuacao		 FLOAT(8) NOT NULL,
  justificacao	 VARCHAR(512) NOT NULL,
  album_nome		 VARCHAR(512),
  utilizador_username VARCHAR(512) NOT NULL,
  PRIMARY KEY(album_nome)
);

CREATE TABLE playlist (
  id			 SERIAL,
  nome		 VARCHAR(512) NOT NULL,
  privada		 BOOL NOT NULL DEFAULT true,
  utilizador_username VARCHAR(512) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE letra (
  texto		 VARCHAR(512) NOT NULL,
  musica_id		 BIGINT,
  compositor_artista_id BIGINT NOT NULL,
  PRIMARY KEY(musica_id)
);

CREATE TABLE utilizador (
  username VARCHAR(512) UNIQUE NOT NULL,
  password VARCHAR(512) NOT NULL,
  editor	 BOOL NOT NULL DEFAULT false,
  PRIMARY KEY(username)
);

CREATE TABLE artista (
  id		 SERIAL,
  nome		 VARCHAR(512) NOT NULL,
  data_nascimento DATE,
  PRIMARY KEY(id)
);

CREATE TABLE editora (
  id	 SERIAL,
  nome VARCHAR(512) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE musica_utilizador (
  musica_id BIGINT,
  utilizador_username	 VARCHAR(512),
  PRIMARY KEY(musica_id,utilizador_username)
);

CREATE TABLE musica_artista (
  musica_id BIGINT,
  artista_id		 BIGINT,
  PRIMARY KEY(musica_id,artista_id)
);

CREATE TABLE artista_grupo_musical (
  artista_id	 BIGINT,
  grupo_musical_nome VARCHAR(512),
  PRIMARY KEY(artista_id,grupo_musical_nome)
);

CREATE TABLE playlist_musica (
  playlist_id		 BIGINT,
  musica_id BIGINT,
  PRIMARY KEY(playlist_id,musica_id)
);

ALTER TABLE musica ADD CONSTRAINT musica_fk1 FOREIGN KEY (album_nome) REFERENCES album(nome);
ALTER TABLE compositor ADD CONSTRAINT compositor_fk1 FOREIGN KEY (artista_id) REFERENCES artista(id);
ALTER TABLE album ADD CONSTRAINT album_fk1 FOREIGN KEY (editora_id) REFERENCES editora(id);
ALTER TABLE album ADD CONSTRAINT album_fk2 FOREIGN KEY (grupo_musical_nome) REFERENCES grupo_musical(nome);
ALTER TABLE concerto ADD CONSTRAINT concerto_fk1 FOREIGN KEY (grupo_musical_nome) REFERENCES grupo_musical(nome);
ALTER TABLE critica ADD CONSTRAINT critica_fk1 FOREIGN KEY (album_nome) REFERENCES album(nome);
ALTER TABLE critica ADD CONSTRAINT critica_fk2 FOREIGN KEY (utilizador_username) REFERENCES utilizador(username);
ALTER TABLE playlist ADD CONSTRAINT playlist_fk1 FOREIGN KEY (utilizador_username) REFERENCES utilizador(username);
ALTER TABLE letra ADD CONSTRAINT letra_fk1 FOREIGN KEY (musica_id) REFERENCES musica(id);
ALTER TABLE letra ADD CONSTRAINT letra_fk2 FOREIGN KEY (compositor_artista_id) REFERENCES compositor(artista_id);
ALTER TABLE musica_utilizador ADD CONSTRAINT musica_utilizador_fk1 FOREIGN KEY (musica_id) REFERENCES musica(id);
ALTER TABLE musica_utilizador ADD CONSTRAINT musica_utilizador_fk2 FOREIGN KEY (utilizador_username) REFERENCES utilizador(username);
ALTER TABLE musica_artista ADD CONSTRAINT musica_artista_fk1 FOREIGN KEY (musica_id) REFERENCES musica(id);
ALTER TABLE musica_artista ADD CONSTRAINT musica_artista_fk2 FOREIGN KEY (artista_id) REFERENCES artista(id);
ALTER TABLE artista_grupo_musical ADD CONSTRAINT artista_grupo_musical_fk1 FOREIGN KEY (artista_id) REFERENCES artista(id);
ALTER TABLE artista_grupo_musical ADD CONSTRAINT artista_grupo_musical_fk2 FOREIGN KEY (grupo_musical_nome) REFERENCES grupo_musical(nome);
ALTER TABLE playlist_musica ADD CONSTRAINT playlist_musica_fk1 FOREIGN KEY (playlist_id) REFERENCES playlist(id);
ALTER TABLE playlist_musica ADD CONSTRAINT playlist_musica_fk2 FOREIGN KEY (musica_id) REFERENCES musica(id);

