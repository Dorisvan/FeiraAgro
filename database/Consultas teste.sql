SELECT * FROM Usuario;

SELECT * FROM Perfil_produtor;

SELECT p.codigo, p.descricao_producao, p.local_venda, p.img0, p.img1, p.img2, p.img3, p.Usuario_codigo, u.nome, u.email, u.endereco, u.contato
FROM Perfil_Produtor as p, Usuario as u
WHERE p.Usuario_codigo = u.codigo AND u.codigo = 1;

SELECT p.codigo, p.descricao_producao, p.local_venda, p.img0, p.img1, p.img2, p.img3, p.Usuario_codigo, u.nome, u.email, u.endereco, u.contato
FROM Perfil_Produtor as p, Usuario as u
WHERE p.Usuario_codigo = u.codigo AND u.codigo = 1;