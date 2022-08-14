# BlogNews

Este projeto foi pensado com o intuito de aprendizado através da aplicação da maioria das técnicas e funções disponibilizadas pelo Django, como modelos, views, templates, forms e etc. Além de testar em prática o conhecimento necessário para adaptar as classes disponibilizadas pelo Django ou criar classes próprias.

## Divisão do site

O site BlogNews é dividido em três partes:

1. **Área geral**: Disponível para o público geral, não sendo obrigatório o usuário estar logado, porém ainda com algumas limitações a serviços especificos, como comentários e pesquisas.
2. **Área para criadores de conteúdo**: Trata-se de uma área destinada a usuários com a marcação de criadores de conteúdo, onde é disponibizado a eles, páginas para criação, edição, exclusão e visualização de seus próprios Posts, albuns ou pesquisas.
3. **Área administrativa**: Trata-se de uma área para usuários com amplos poderes, onde usuários podem possuir um acesso mais profundo ao sistema de acordo com as permissões conferidas as eles por um **SuperUsuário**.

## Tipos de usuários

Os usuários do BlogNews podem ser divididos no geral em 4 grupos:

1. **Usuários finais**: São aqueles que não possuem a permissão para criar conteúdo, sendo assim, eles são limitados a apenas visualizar as informações existentes, fazer comentários ou denúncias e alterar informações próprias da conta.
2. **Criadores de conteúdos**: Possuem todos os privilegios dos usuários finais, além de poderem criar e publicar seus próprios Posts, albuns e pesquisas.
3. **Membros da Staff**: São aqueles que possuem acesso a área administrativa, porém eles estão limitados as permissões concedidas a eles pelos SuperUsuários. Sendo assim, se ele possuir permissão pode visualizar todo o contéudo do sistema, esteja ele publicado ou não, e fazer alterações ou exclusões a medida que achar necessário.
4. **SuperUsuários**: Trata-se do nível mais alto do sistema, podendo conceder permissões a si próprio e a outros usuários para assim administrar o sistema.
