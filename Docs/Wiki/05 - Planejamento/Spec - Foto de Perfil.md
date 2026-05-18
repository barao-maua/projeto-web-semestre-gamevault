---
title: Spec - Foto de Perfil
aliases:
  - Spec Foto de Perfil
  - Foto de Perfil
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - perfil
  - avatar
  - backlog
---

# Spec - Foto de Perfil

Esta nota define o plano para substituir o avatar por inicial por uma foto de perfil real no [[GameVault]].

## Objetivo

Permitir que o usuario:

- envie uma foto de perfil;
- visualize essa foto no perfil;
- visualize essa foto na navbar;
- troque a foto atual;
- remova a foto atual;
- mantenha fallback para inicial quando nao houver imagem.

## Escopo

Dentro do escopo:

- upload de imagem no perfil;
- troca de imagem existente;
- remocao da imagem;
- exibicao no perfil;
- exibicao na navbar;
- fallback para inicial.

Fora do escopo:

- crop avancado;
- compressao inteligente;
- editor de imagem no navegador;
- multiplas fotos por usuario;
- historico de imagens.

## Decisao Tecnica

Nao alterar o `User` padrao do Django.

Criar model auxiliar:

```python
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
```

Motivo:

- evita trocar o model de usuario;
- mantem compatibilidade com o resto do sistema;
- facilita evoluir outros dados de perfil no futuro;
- isola a responsabilidade de arquivo/imagem fora do `User`.

## Objetivos Funcionais

O usuario deve conseguir:

1. enviar uma imagem de perfil;
2. substituir a imagem atual;
3. remover a imagem atual;
4. ver a imagem refletida no perfil;
5. ver a imagem refletida na navbar;
6. cair no fallback de inicial quando nao houver imagem.

## Fluxos Do Usuario

### Fluxo 1 - Primeiro Upload

1. Usuario abre `/profile/`.
2. Ve o fallback atual por inicial.
3. Seleciona uma imagem.
4. Salva o perfil.
5. O perfil passa a mostrar a imagem.
6. A navbar passa a mostrar a mesma imagem.

### Fluxo 2 - Troca De Avatar

1. Usuario abre `/profile/`.
2. Seleciona nova imagem.
3. Salva o perfil.
4. A nova imagem substitui a anterior.

### Fluxo 3 - Remocao

1. Usuario abre `/profile/`.
2. Clica em `Remover foto`.
3. Confirma a acao.
4. O avatar some.
5. O sistema volta a mostrar a inicial.

## Persistencia E Midia

O projeto ja possui:

- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = BASE_DIR / "media"`

Esses dois pontos sao a base correta para armazenar avatares.

Esperado em desenvolvimento:

- arquivos em `media/avatars/`;
- acesso via `MEDIA_URL`;
- `config/urls.py` servindo `media/` em ambiente local.

## Validacao De Arquivo

Formatos aceitos:

- `.jpg`
- `.jpeg`
- `.png`
- `.webp`

Tamanho maximo recomendado:

- `2 MB`

Validacoes minimas:

- tipo/extensao do arquivo;
- tamanho maximo.

Nao entra nesta fase:

- validacao avancada de dimensoes;
- redimensionamento automatico;
- compressao automatica.

## Formulario

O perfil deve aceitar:

- `username`;
- `email`;
- `avatar`.

HTML necessario:

- `method="post"`
- `enctype="multipart/form-data"`

Acao adicional recomendada:

- botao separado `Remover foto`.

Motivo:

- fica mais claro do que um checkbox escondido;
- combina melhor com o restante da UX atual.

## View

A `profile_view` atual deve passar a:

1. receber `request.FILES`;
2. carregar ou criar `UserProfile`;
3. salvar `avatar` quando enviado;
4. remover `avatar` quando solicitado;
5. manter o fluxo atual de username/email/verificacao.

Ordem recomendada:

- salvar dados do `User`;
- salvar dados do `UserProfile`;
- mostrar mensagem clara de sucesso ou erro.

## Templates Impactados

### `templates/registration/profile.html`

Adicionar:

- bloco visual do avatar atual;
- input de upload;
- botao para remover foto;
- fallback quando nao houver imagem.

### `templates/components/navbar.html`

Hoje a navbar usa inicial do nome.

Passar a usar esta logica:

- se `user.profile.avatar` existir, renderizar imagem;
- senao, renderizar inicial.

## Comportamento Visual

### No Perfil

Mostrar:

- foto atual em destaque;
- fallback textual quando nao houver imagem;
- botao para escolher nova foto;
- botao para remover foto.

### Na Navbar

Mostrar:

- imagem circular pequena quando existir;
- inicial do usuario quando nao existir.

## CSS Necessario

### Perfil

- container do avatar;
- imagem circular;
- placeholder com inicial;
- alinhamento com o formulario.

### Navbar

- imagem circular pequena;
- `object-fit: cover`;
- dimensao fixa;
- alinhamento com o chip atual.

## Regras Importantes

- somente o proprio usuario altera sua foto;
- foto nao e obrigatoria;
- trocar foto substitui a anterior;
- remover foto volta para fallback textual;
- falha no upload nao deve apagar a foto anterior automaticamente.

## Riscos

- `media/` nao estar sendo servido corretamente;
- imagem quebrada por caminho invalido;
- arquivo antigo ficar orfao no disco ao trocar foto;
- arquivos grandes demais sem controle;
- usuarios antigos ainda nao terem `UserProfile`.

## Mitigacoes

- criar helper `get_or_create_user_profile(user)`;
- validar tamanho e extensao;
- manter fallback robusto no template;
- aceitar limpeza automatica de arquivo antigo como etapa futura, nao bloqueadora.

## Decisoes Recomendadas

- usar `UserProfile` como model auxiliar;
- usar `ImageField` com `upload_to="avatars/"`;
- limitar tamanho a `2 MB`;
- aceitar `jpg`, `jpeg`, `png` e `webp`;
- usar botao explicito para remover foto;
- manter fallback por inicial em perfil e navbar;
- nao implementar crop nesta fase.

## Arquivos Impactados

- `core/models.py`
- migration nova
- `core/forms.py`
- `core/views.py`
- `templates/registration/profile.html`
- `templates/components/navbar.html`
- `static/css/pages/profile.css`
- `static/css/components.css`
- possivelmente `config/urls.py`
- documentacao relacionada.

## Checklist De Implementacao

- [ ] Criar `UserProfile`.
- [ ] Criar migration.
- [ ] Criar helper `get_or_create_user_profile(user)`.
- [ ] Adicionar campo `avatar` ao form de perfil.
- [ ] Validar extensao do arquivo.
- [ ] Validar tamanho maximo.
- [ ] Ajustar `profile_view` para receber `request.FILES`.
- [ ] Implementar troca de avatar.
- [ ] Implementar remocao de avatar.
- [ ] Renderizar avatar no perfil.
- [ ] Renderizar avatar na navbar.
- [ ] Manter fallback por inicial.
- [ ] Garantir serving de `media/` em desenvolvimento.
- [ ] Atualizar documentacao relacionada.
- [ ] Testar upload, troca, remocao e fallback.

## Critério De Pronto

- Usuario consegue enviar foto.
- Foto aparece no perfil.
- Foto aparece na navbar.
- Usuario consegue trocar foto.
- Usuario consegue remover foto.
- Fallback por inicial continua funcionando.
- Upload invalido mostra erro claro.
- O sistema nao quebra sem `UserProfile`.

## Plano De Teste Manual

1. Abrir perfil sem avatar.
2. Confirmar fallback por inicial.
3. Enviar imagem valida.
4. Salvar perfil.
5. Verificar avatar no perfil.
6. Verificar avatar na navbar.
7. Trocar por outra imagem.
8. Confirmar atualizacao.
9. Remover foto.
10. Verificar retorno ao fallback.
11. Testar arquivo muito grande.
12. Testar formato invalido.

## Ordem Recomendada De Implementacao

1. Criar `UserProfile`.
2. Ajustar perfil para upload.
3. Ajustar navbar para consumir avatar.
4. Implementar remocao.
5. Refinar limpeza de arquivo antigo, se necessario.

## Notas Relacionadas

- [[Autenticacao]]
- [[Templates]]
- [[Static e CSS]]
- [[Backlog Pos-Entrega]]
