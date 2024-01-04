SELECT * FROM Usuario;

SELECT * FROM Perfil_produtor;

SELECT * FROM Produto;

SELECT * FROM Pedido;

SELECT * FROM Mensagem;

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

INSERT INTO Usuario(nome, email, senha, endereco, tipo, nivel, contato, estado_login, imagem_perfil)
VALUES ("Emilly", "Emi@gmail.com", 123, "Bacurau", "Produtor", 1 , "9999999", 0, "emi.png");

INSERT INTO Usuario(nome, email, senha, endereco, tipo, nivel, contato, estado_login, imagem_perfil)
VALUES ("Dorisvan", "Doris@gmail.com", 123, "Caraúbas", "Produtor", 1 , "9999999", 0, "doris.png");

INSERT INTO Pedido(data_pedido, data_entrega, quantidade, situacao, modo_entrega, status_compra, Usuario_codigo, Produto_codigo)
VALUES ("2023-11-23", "2023-10-21", 1, "Entregue", "Delivery", "Finalizada" , 1, 2);

INSERT INTO Mensagem(titulo, conteudo, tipo, situacao, Usuario_codigo)
VALUES("Aviso", "123", "Urgente", "Não_lida", 1);


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

DELETE FROM Perfil_produtor WHERE codigo = 3;


INSERT INTO Pedido(data_pedido, data_entrega, quantidade, situacao, modo_entrega, Usuario_codigo, Produto_codigo)
VALUES ("26-10-2022", "25-10-2222", 1, "Não Entregue", "Retirada", 2, 1);

SELECT DISTINCT pe.codigo,  pe.data_pedido, pe.data_entrega, pe.quantidade, pe.situacao, pe.modo_entrega, pe.Usuario_codigo, pe.Produto_codigo
FROM Pedido as pe, Produto as pr, Usuario as u  
WHERE pr.Usuario_codigo = 2 AND pr.codigo = pe.Produto_codigo;

SELECT * FROM Pedido WHERE Pedido.Usuario_codigo = 2;

SELECT DISTINCT p.codigo, p.nome, p.quantidade, p.valor, p.classificacao, p.procedencia, p.img_produto, p.descricao, p.Usuario_codigo as codigo_dono, u.nome as nome_do_produtor, u.contato, u.endereco, pf.local_venda 
FROM Produto as p, Perfil_produtor as pf , Usuario as u
WHERE u.codigo = p.Usuario_codigo AND u.codigo = pf.Usuario_codigo AND (p.codigo LIKE 1 OR p.nome LIKE 1 OR p.quantidade LIKE 1 OR p.valor LIKE 1 OR p.classificacao LIKE 1 OR p.img_produto LIKE 1 OR p.descricao LIKE 1 OR p.Usuario_codigo LIKE 1 OR u.nome LIKE 1 OR u.contato LIKE 1 OR u.endereco LIKE 1 OR pf.local_venda LIKE 1); 


SELECT * FROM Usuario;

