SELECT * FROM Usuario;

SELECT * FROM Perfil_produtor;

SELECT * FROM Produto;

SELECT p.codigo, p.descricao_producao, p.local_venda, p.img0, p.img1, p.img2, p.img3, p.Usuario_codigo, u.nome, u.email, u.endereco, u.contato
FROM Perfil_Produtor as p, Usuario as u
WHERE p.Usuario_codigo = u.codigo AND u.codigo = 1;

SELECT p.codigo, p.descricao_producao, p.local_venda, p.img0, p.img1, p.img2, p.img3, p.Usuario_codigo, u.nome, u.email, u.endereco, u.contato
FROM Perfil_Produtor as p, Usuario as u
WHERE p.Usuario_codigo = u.codigo AND u.codigo = 1;


INSERT INTO perfil_produtor(descricao_producao, local_venda, img0, img1, img2, img3, Usuario_codigo)
VALUES ("ABC", "abc", "abc", "abc", "abc", "abc", 1);

INSERT INTO perfil_produtor(descricao_producao, local_venda, img0, img1, img2, img3, Usuario_codigo)
VALUES ("Batata", "Apodi", "abc", "abc", "abc", "abc", 2);

INSERT INTO Produto(nome, quantidade, valor, classificacao, procedencia, usuario_codigo, img_produto, descricao)
VALUES ("Doris", 123, 123, "hortãliças", "orgânico", 1 , "abc", "123");

INSERT INTO Produto(nome, quantidade, valor, classificacao, procedencia, usuario_codigo, img_produto, descricao)
VALUES ("Natata", 123, 123, "hortãliças", "orgânico", 2 , "abc", "123");

INSERT INTO Usuario(nome, email, senha, endereco, tipo, nivel, contato)
VALUES ("Emilly", "Emi@gmail.com", 123, "Bacurau", "Produtor", 1 , "9999999");


SELECT DISTINCT p.codigo, p.nome, p.quantidade, p.valor, p.classificacao, p.procedencia, p.img_produto, p.descricao, p.Usuario_codigo as codigo_dono, u.nome as nome_do_produtor, u.contato, u.endereco, pf.local_venda
FROM Produto as p, Usuario as u, Perfil_produtor as pf
WHERE u.codigo = p.Usuario_codigo AND u.codigo = pf.Usuario_codigo
ORDER BY p.Usuario_codigo, p.nome;

SELECT u.nome, u.contato, u.endereco, pf.local_venda
FROM Usuario as u, Perfil_produtor as pf
WHERE u.codigo = pf.Usuario_codigo;


SELECT DISTINCT p.codigo, p.nome, p.quantidade, p.valor, p.classificacao, p.procedencia, p.img_produto, p.descricao, p.Usuario_codigo as codigo_dono, u.nome as nome_do_produtor, u.contato, u.endereco, pf.local_venda
FROM Produto as p, Usuario as u, Perfil_produtor as pf
WHERE u.codigo = p.Usuario_codigo AND u.codigo = pf.Usuario_codigo AND pf.Usuario_codigo = 1
ORDER BY p.Usuario_codigo, p.nome;

DELETE FROM Usuario WHERE codigo = 1;