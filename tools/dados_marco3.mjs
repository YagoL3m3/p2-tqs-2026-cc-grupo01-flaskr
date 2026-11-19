const auth = "flaskr/auth.py";
const blog = "flaskr/blog.py";
const db = "flaskr/db.py";
const schema = "flaskr/schema.sql";
const base = "flaskr/templates/base.html, linhas 7–22";
const registerForm = "flaskr/templates/auth/register.html, linhas 8–14";
const loginForm = "flaskr/templates/auth/login.html, linhas 8–14";
const feed = "flaskr/templates/blog/index.html, linhas 4–23";
const createForm = "flaskr/templates/blog/create.html, linhas 8–14";
const editForm = "flaskr/templates/blog/update.html, linhas 8–18";
const register = `${auth} · register(), linhas 46–81`;
const login = `${auth} · login(), linhas 84–109`;
const list = `${blog} · index(), linhas 16–25`;
const create = `${blog} · create(), linhas 60–83`;
const update = `${blog} · update(), linhas 86–110`;
const post = `${blog} · get_post(), linhas 28–57`;
const remove = `${blog} · delete(), linhas 113–125`;

export const requisitos = [
  ["RF-01", "Cadastrar uma conta com nome disponível e campos preenchidos. Impedir cadastro com campo obrigatório vazio ou nome duplicado.", "Funcional", "Média",
    "Uma conta inédita consegue iniciar sessão com as credenciais cadastradas. Campos vazios impedem o envio no navegador. O nome duplicado é rejeitado com aviso e a senha original permanece válida.",
    ["R-02", "R-07"], [register, registerForm, `${schema}, linha 9`]],
  ["RF-02", "Autenticar contas existentes e informar credenciais inválidas sem iniciar sessão.", "Funcional", "Alta",
    "Credenciais corretas levam a Posts e mostram o nome e Log Out. Nome inexistente ou senha incorreta mantêm o formulário de login e mostram a mensagem correspondente.",
    ["R-04"], [login, base]],
  ["RF-03", "Encerrar a sessão e exigir novo login para acessar rotas protegidas.", "Funcional", "Alta",
    "Após Log Out, Posts mostra Log In e Register. Abrir /create no mesmo navegador conduz à tela Log In.",
    ["R-04"], [`${auth} · logout() e login_required(), linhas 19–29 e 112–116`, create]],
  ["RF-04", "Exibir a lista pública com título, corpo e autor, ordenar por data decrescente e mostrar Edit apenas ao autor de cada post.", "Funcional", "Média",
    "Leitores veem o conteúdo mesmo sem sessão. Com horários distintos, o post mais recente vem antes. A base vazia abre sem artigos. Cada autor vê Edit somente nos próprios posts.",
    ["R-11", "R-01"], [list, feed]],
  ["RF-05", "Criar post com título preenchido e autoria da sessão, permitindo corpo vazio.", "Funcional", "Alta",
    "Os títulos não vazios da massa, incluindo um de um caractere, aceitam salvar. Corpo vazio é permitido. Posts mostra o artigo sob a conta ativa. Título vazio impede o envio.",
    ["R-02", "R-03"], [create, createForm]],
  ["RF-06", "Permitir edição pelo autor, exigir título e proteger publicações alheias e endereços inexistentes.", "Funcional", "Alta",
    "Alteração válida aparece em Posts. Título vazio impede o envio. Editar um post alheio pelo endereço retorna 403. Abrir a edição de um post inexistente retorna 404.",
    ["R-01", "R-02", "R-03"], [update, post, editForm]],
  ["RF-07", "Restringir a exclusão ao autor e remover apenas o post selecionado após confirmar o diálogo.", "Funcional", "Alta",
    "Cancelar conserva o post. O autor remove apenas o alvo. Repetir a exclusão do mesmo post retorna 404. Confirmar com outra conta na sessão retorna 403 e preserva o post.",
    ["R-01", "R-06"], [remove, post, editForm]],
  ["RNF-01", "Manter a senha armazenada como hash verificável e fora do HTML de resposta.", "Não funcional", "Alta",
    "Na conta fictícia verificada, SQLite contém exatamente uma senha armazenada diferente da entrada. check_password_hash confirma a senha de teste. O HTML da resposta de cadastro após redirecionamento não contém a senha.",
    ["R-05"], [register, login, `${schema}, linhas 7–11`]],
  ["RNF-02", "Preservar a criação e a edição de posts após reiniciar o aplicativo mantendo o mesmo arquivo SQLite.", "Não funcional", "Alta",
    "Após um reinício do processo sem reinicializar o banco, os dois posts preparados continuam visíveis. O post editado mantém título e corpo atualizados.",
    ["R-03"], [`${db} · get_db(), linhas 9–20`, create, update, list]],
  ["RNF-03", "Permitir completar o cadastro e a criação de post usando teclado no Safari configurado para navegação por Tab.", "Não funcional", "Média",
    "Atingir os campos e botões dos dois formulários com Tab, identificar foco e acionar os botões pelo teclado. Finalizar o cadastro, iniciar sessão e ver o novo post sem usar o ponteiro durante o fluxo.",
    ["R-08", "R-12"], [registerForm, loginForm, createForm, base]],
];

export const notasCasos = [
  "Execute cada caso com uma base local descartável, isolada dos demais casos. A Etapa 4A prepara o reset. Conclua a preparação específica de cada linha antes do passo 1.",
  "URL de referência: http://127.0.0.1:5001/. Se o grupo usar a porta 5000, troque apenas a porta. Use sessão anônima quando a linha pedir navegação sem login.",
  "Dados fictícios de referência: conta A = qa_autor_a / Senha-QA-A-2026! e conta B = qa_autor_b / Senha-QA-B-2026!. Cadastre as contas de cada pré-condição pelo formulário Register.",
  "Para preparar um post, entre com a conta indicada, abra New, informe Title e Body e clique Save. Para obter seu endereço de edição, copie o link Edit da própria conta.",
  "Responsável do catálogo conforme os papéis da Etapa 2. [PENDENTE-HUMANO: atribuir executores, executar os casos e anexar as evidências reais | Grupo 1]",
];

const anon = "Banco descartável vazio e navegador sem sessão.";
const contaA = "Conta A cadastrada. Navegador sem sessão.";
const loginA = "Sessão iniciada com a conta A.";
const postA = `${loginA} Prepare um único post com título «Post A» e corpo «Corpo A».`;
const doisPostsA = `${postA} Prepare também «Post B» com corpo «Corpo B», da mesma conta.`;
const limite = "Análise de valor-limite (0 e 1)";
const particao = "Particionamento de equivalência";
const limiteMinimo = "O código distingue vazio de preenchido. A fronteira 0/1 é observada no formulário. Nenhum tamanho máximo foi especificado para este caso.";

function caso(numero, requisito, detalhes) {
  return { id: `CT-${String(numero).padStart(3, "0")}`, requisito, ...detalhes };
}

export const casos = [
  caso(1, "RF-01", {
    titulo: "Cadastrar conta inédita", tipo: "Sistema / positivo", tecnica: particao, prioridade: "Média",
    pre: anon, dados: "Credenciais da conta A.",
    passos: ["Abra Register.", "Preencha Username e Password e clique em Register.", "Na página Log In, entre com as mesmas credenciais."],
    esperado: "O cadastro redireciona para Log In. Em seguida, Posts mostra qa_autor_a e Log Out.",
    candidato: "Sim", motivo: "Fluxo principal entre cadastro, gravação e autenticação.", riscos: ["R-02", "R-07"], fontes: [register, login],
  }),
  caso(2, "RF-01", {
    titulo: "Bloquear cadastro com nome vazio", tipo: "Sistema / fronteira", tecnica: limite, prioridade: "Média",
    pre: anon, dados: "Username vazio. Password da conta A.",
    passos: ["Abra Register.", "Deixe Username em branco e preencha Password.", "Clique em Register."],
    esperado: "O navegador impede o envio, sinaliza o campo Username e permanece no formulário.",
    candidato: "Não", motivo: "O texto da validação nativa varia conforme o navegador e o idioma.", riscos: ["R-02"], fontes: [registerForm, register], observacao: limiteMinimo,
  }),
  caso(3, "RF-01", {
    titulo: "Bloquear cadastro com senha vazia", tipo: "Sistema / negativo", tecnica: particao, prioridade: "Média",
    pre: anon, dados: "Username qa_autor_a. Password vazio.",
    passos: ["Abra Register.", "Preencha Username e deixe Password em branco.", "Clique em Register."],
    esperado: "O navegador impede o envio, sinaliza o campo Password e permanece em Register.",
    candidato: "Não", motivo: "O objetivo é observar a validação nativa no navegador utilizado pelo grupo.", riscos: ["R-02"], fontes: [registerForm, register],
  }),
  caso(4, "RF-01", {
    titulo: "Rejeitar nome de usuário duplicado", tipo: "Sistema / negativo", tecnica: particao, prioridade: "Média",
    pre: contaA, dados: "Username qa_autor_a já cadastrado. Tentativa com senha Troca-QA-2026!.",
    passos: ["Abra Register e envie o mesmo Username com a senha alternativa.", "Confira o aviso e abra Log In.", "Entre com a senha original da conta A."],
    esperado: "Register mostra «User qa_autor_a is already registered.». A senha original continua permitindo acesso à conta.",
    candidato: "Sim", motivo: "Valida a integração do cadastro com a restrição de unicidade no SQLite.", riscos: ["R-07"], fontes: [register, `${schema}, linha 9`, base],
  }),
  caso(5, "RF-01", {
    titulo: "Cadastrar nome com um caractere", tipo: "Sistema / fronteira", tecnica: limite, prioridade: "Média",
    pre: anon, dados: "Username q. Password Senha-QA-A-2026!.",
    passos: ["Em Register, informe q e a senha fictícia.", "Clique em Register.", "Em Log In, entre como q."],
    esperado: "O cadastro leva a Log In e a conta de um caractere autentica. O menu de Posts mostra q.",
    candidato: "Sim", motivo: "Fronteira mínima reproduzível ao lado do caso de zero caracteres.", riscos: ["R-02"], fontes: [register, registerForm, login], observacao: limiteMinimo,
  }),
  caso(6, "RF-02", {
    titulo: "Iniciar e manter sessão com credenciais válidas", tipo: "Sistema / positivo", tecnica: particao, prioridade: "Alta",
    pre: contaA, dados: "Credenciais da conta A.",
    passos: ["Em Log In, preencha os dados válidos e envie.", "Confira Posts.", "Recarregue a página no mesmo navegador."],
    esperado: "O login leva a Posts. Antes e depois do recarregamento, o menu exibe qa_autor_a e Log Out.",
    candidato: "Sim", motivo: "A autenticação e a continuidade da sessão são verificáveis.", riscos: ["R-04"], fontes: [login, `${auth} · load_logged_in_user(), linhas 32–43`, base],
  }),
  caso(7, "RF-02", {
    titulo: "Rejeitar login de conta inexistente", tipo: "Sistema / negativo", tecnica: particao, prioridade: "Alta",
    pre: contaA, dados: "Username qa_inexistente, ausente no banco. Password da conta A.",
    passos: ["Em Log In, informe qa_inexistente e a senha fictícia.", "Envie e observe o formulário e o menu."],
    esperado: "A tela continua em Log In e mostra «Incorrect username.». Log Out não aparece.",
    candidato: "Sim", motivo: "A mensagem e a ausência de sessão permitem validar o caminho negativo.", riscos: ["R-04"], fontes: [login, base],
  }),
  caso(8, "RF-02", {
    titulo: "Rejeitar senha errada de conta existente", tipo: "Sistema / negativo", tecnica: particao, prioridade: "Alta",
    pre: contaA, dados: "Username qa_autor_a. Password Senha-Incorreta-QA!.",
    passos: ["Em Log In, envie o usuário e a senha incorreta.", "Observe o formulário e o menu."],
    esperado: "A tela continua em Log In e mostra «Incorrect password.». Log Out não aparece.",
    candidato: "Sim", motivo: "Cobre o ramo de validação do hash de uma conta existente.", riscos: ["R-04"], fontes: [login, base],
  }),
  caso(9, "RF-03", {
    titulo: "Bloquear criação após encerrar a sessão", tipo: "Sistema / transição de estado", tecnica: "Transição de estados", prioridade: "Alta",
    pre: loginA, dados: "Endereço local /create.",
    passos: ["Abra New e confira que a tela New Post está acessível.", "Clique em Log Out e confira o menu de Posts.", "Digite /create novamente na mesma sessão do navegador."],
    esperado: "Depois de Log Out, Posts volta a mostrar Log In e Register. A nova navegação para /create leva à tela Log In.",
    candidato: "Sim", motivo: "A mudança de estado e o redirecionamento do formulário são observáveis.", riscos: ["R-04"], fontes: [`${auth} · logout() e login_required(), linhas 19–29 e 112–116`, create, base],
  }),
  caso(10, "RF-04", {
    titulo: "Ler uma publicação sem iniciar sessão", tipo: "Sistema / positivo", tecnica: particao, prioridade: "Média",
    pre: `${postA} Abra outra janela anônima.`, dados: "Post A, Corpo A e autor qa_autor_a.",
    passos: ["Na janela anônima, abra a página inicial.", "Confira título, corpo e autoria do artigo."],
    esperado: "O artigo mostra «Post A», «Corpo A» e «by qa_autor_a on» com a data. O menu permite Log In.",
    candidato: "Sim", motivo: "A consulta pública pode ser verificada sem cookies de sessão.", riscos: ["R-11"], fontes: [list, feed, base],
  }),
  caso(11, "RF-04", {
    titulo: "Ordenar publicações da mais recente à mais antiga", tipo: "Sistema / positivo", tecnica: "Ordenação com timestamps distintos", prioridade: "Baixa",
    pre: loginA, dados: "«Primeiro QA» e «Segundo QA», com corpos distintos.",
    passos: ["Crie Primeiro QA.", "Após voltar a Posts, aguarde pelo menos 2 segundos antes de criar Segundo QA.", "Abra Posts e compare a posição dos dois artigos."],
    esperado: "Segundo QA aparece acima de Primeiro QA.",
    candidato: "Sim", motivo: "A integração pode usar dados com horários fixos distintos para evitar espera.", riscos: ["R-11"], fontes: [list, `${schema}, linha 16`, feed],
  }),
  caso(12, "RF-04", {
    titulo: "Abrir a listagem com banco sem publicações", tipo: "Sistema / alternativa", tecnica: "Particionamento por quantidade (zero ou mais)", prioridade: "Média",
    pre: anon, dados: "Banco sem publicações.",
    passos: ["Abra a página inicial.", "Confira o título Posts e a região abaixo dele."],
    esperado: "A página Posts é exibida, sem artigos e sem mensagem de erro.",
    candidato: "Sim", motivo: "Banco descartável sem posts é uma massa determinística.", riscos: ["R-11"], fontes: [list, `${feed}, laço de publicações`],
  }),
  caso(13, "RF-04", {
    titulo: "Exibir Edit somente nos posts da conta ativa", tipo: "Sistema / permissão na interface", tecnica: "Tabela de decisão (autor ou outro usuário)", prioridade: "Alta",
    pre: `${postA} Cadastre a conta B, entre nela e publique «Post B».`, dados: "Post A pertence a qa_autor_a. Post B pertence a qa_autor_b.",
    passos: ["Com a conta B em sessão, abra Posts.", "Compare a presença do link Edit nos artigos Post A e Post B."],
    esperado: "Os dois artigos aparecem. Edit é mostrado no Post B e fica ausente no Post A.",
    candidato: "Sim", motivo: "A regra de visibilidade por artigo pode ser conferida no DOM.", riscos: ["R-01"], fontes: [list, feed],
  }),
  caso(14, "RF-05", {
    titulo: "Publicar título e corpo com autoria da sessão", tipo: "Sistema / positivo", tecnica: particao, prioridade: "Alta",
    pre: loginA, dados: "Title Rotina QA. Body Texto fictício da rotina.",
    passos: ["Abra New.", "Preencha Title e Body.", "Clique em Save e localize Rotina QA em Posts."],
    esperado: "Posts exibe «Rotina QA», «Texto fictício da rotina.» e autoria qa_autor_a.",
    candidato: "Sim", motivo: "Fluxo principal reproduzível de interface, sessão e persistência.", riscos: ["R-03"], fontes: [create, createForm, list, feed],
  }),
  caso(15, "RF-05", {
    titulo: "Aceitar título com um caractere", tipo: "Sistema / fronteira", tecnica: limite, prioridade: "Média",
    pre: loginA, dados: "Title X. Body Fronteira QA.",
    passos: ["Abra New.", "Informe X e o corpo proposto.", "Clique em Save e localize o artigo."],
    esperado: "A listagem contém o título «X» e o corpo «Fronteira QA».",
    candidato: "Sim", motivo: "Exercita o lado válido da fronteira zero/um sem depender de texto traduzido.", riscos: ["R-02"], fontes: [create, createForm], observacao: limiteMinimo,
  }),
  caso(16, "RF-05", {
    titulo: "Publicar com corpo vazio", tipo: "Sistema / alternativa", tecnica: particao, prioridade: "Média",
    pre: loginA, dados: "Title Sem corpo QA. Body vazio.",
    passos: ["Abra New.", "Preencha Title, deixe Body em branco e envie.", "Localize Sem corpo QA em Posts."],
    esperado: "O post está na listagem com o título informado e sem conteúdo no corpo.",
    candidato: "Sim", motivo: "Os dados evidenciam o caráter opcional do corpo do post.", riscos: ["R-02"], fontes: [create, createForm, feed],
  }),
  caso(17, "RF-05", {
    titulo: "Bloquear publicação sem título", tipo: "Sistema / fronteira", tecnica: limite, prioridade: "Média",
    pre: loginA, dados: "Title vazio. Body Este rascunho não deve aparecer.",
    passos: ["Em New, deixe Title em branco e escreva o corpo.", "Clique em Save e observe Title e a página.", "Abra Posts separadamente e procure o rascunho."],
    esperado: "O navegador impede o envio e permanece em New Post. O rascunho não aparece na listagem.",
    candidato: "Não", motivo: "Pode ser conferido visualmente em conjunto com foco e mensagem nativa.", riscos: ["R-02"], fontes: [createForm, create], observacao: limiteMinimo,
  }),
  caso(18, "RF-06", {
    titulo: "Editar título e corpo como autor", tipo: "Sistema / positivo", tecnica: particao, prioridade: "Alta",
    pre: postA, dados: "Novo título Post A revisado. Novo corpo Corpo A revisado.",
    passos: ["Em Post A, abra Edit.", "Substitua Title e Body pelos novos dados.", "Salve e confira o artigo em Posts."],
    esperado: "Posts exibe os novos valores sob a autoria qa_autor_a. Os valores antigos deixam de aparecer como título e corpo do artigo.",
    candidato: "Sim", motivo: "Confirma que o envio atualiza o registro correto.", riscos: ["R-03"], fontes: [update, editForm, list, feed],
  }),
  caso(19, "RF-06", {
    titulo: "Impedir que edição deixe título vazio", tipo: "Sistema / negativo", tecnica: "Análise de valor-limite (título vazio)", prioridade: "Média",
    pre: postA, dados: "Title vazio. Body Corpo A alterado.",
    passos: ["Abra Edit no Post A.", "Apague Title, altere Body e clique em Save.", "Abra Posts separadamente e confira Post A."],
    esperado: "O navegador impede o envio e permanece no editor. A listagem conserva «Post A» e «Corpo A».",
    candidato: "Não", motivo: "O teste isola a atuação do formulário antes de alteração no banco.", riscos: ["R-02"], fontes: [editForm, update],
  }),
  caso(20, "RF-06", {
    titulo: "Bloquear edição de post de outra conta", tipo: "Sistema / controle de acesso", tecnica: "Tabela de decisão (sessão e autoria)", prioridade: "Alta",
    pre: `${postA} Cadastre a conta B e copie o link Edit de Post A enquanto está como autor.`, dados: "Endereço local do editor de Post A, obtido na interface da conta A.",
    passos: ["Saia da conta A e entre na conta B.", "Abra o endereço local de Edit já copiado.", "Observe a resposta. Depois, entre na conta A e confira Post A em Posts."],
    esperado: "O acesso da conta B mostra Forbidden (HTTP 403) e não abre o editor. Post A conserva título e corpo.",
    candidato: "Sim", motivo: "É uma checagem de autorização no sistema local com duas contas fictícias.", riscos: ["R-01"], fontes: [update, post],
  }),
  caso(21, "RF-06", {
    titulo: "Tratar a abertura de edição de post inexistente", tipo: "Sistema / exceção", tecnica: particao, prioridade: "Alta",
    pre: "Banco sem posts. Cadastre a conta A e entre nela.",
    dados: "Endereço local /1/update. Nenhum post foi criado na base deste caso.",
    passos: ["Confirme que Posts está vazio.", "Abra /1/update no navegador autenticado."],
    esperado: "A resposta mostra Not Found (HTTP 404). O editor não é exibido.",
    candidato: "Sim", motivo: "A ausência do ID pode ser reproduzida com uma base vazia.", riscos: ["R-01"], fontes: [update, post],
  }),
  caso(22, "RF-07", {
    titulo: "Cancelar diálogo de exclusão", tipo: "Sistema / alternativa", tecnica: "Tabela de decisão (cancelar ou confirmar)", prioridade: "Alta",
    pre: doisPostsA, dados: "Alvo Post A. Controle Post B.",
    passos: ["Abra Edit no Post A e clique em Delete.", "Cancele o diálogo «Are you sure?».", "Abra Posts e procure os dois artigos."],
    esperado: "O cancelamento deixa o editor aberto. «Post A» e «Post B» continuam na listagem.",
    candidato: "Sim", motivo: "O Selenium pode cancelar o diálogo e conferir ambos os posts.", riscos: ["R-06"], fontes: [editForm, remove, feed],
  }),
  caso(23, "RF-07", {
    titulo: "Confirmar exclusão apenas do post selecionado", tipo: "Sistema / positivo", tecnica: "Tabela de decisão (cancelar ou confirmar)", prioridade: "Alta",
    pre: doisPostsA, dados: "Alvo Post A. Controle Post B.",
    passos: ["Abra Edit no Post A e clique em Delete.", "Confirme o diálogo «Are you sure?».", "Confira o conteúdo da listagem após voltar a Posts."],
    esperado: "Post A desaparece. Post B permanece com seu corpo e sua autoria.",
    candidato: "Sim", motivo: "A confirmação e a conservação do post de controle podem ser assertadas.", riscos: ["R-06"], fontes: [editForm, remove, post, feed],
  }),
  caso(24, "RF-07", {
    titulo: "Tratar nova exclusão em editor desatualizado", tipo: "Sistema / exceção", tecnica: "Transição de estados (existente para excluído)", prioridade: "Alta",
    pre: doisPostsA, dados: "Mesmo editor de Post A em duas abas autenticadas. Post B como controle.",
    passos: ["Abra Edit do Post A em duas abas no mesmo navegador.", "Na primeira, clique em Delete, confirme e veja Post A sumir.", "Na aba antiga, sem recarregar, clique em Delete e confirme.", "Volte a Posts e confira Post B."],
    esperado: "A primeira exclusão conclui. A segunda resposta mostra Not Found (HTTP 404). Post B permanece.",
    candidato: "Sim", motivo: "Verifica a resposta à segunda tentativa e evita excluir o registro errado.", riscos: ["R-06"], fontes: [editForm, remove, post],
  }),
  caso(25, "RF-07", {
    titulo: "Bloquear exclusão após trocar para conta não autora", tipo: "Sistema / controle de acesso", tecnica: "Tabela de decisão (sessão e autoria)", prioridade: "Alta",
    pre: `${postA} Cadastre também a conta B e mantenha o login da conta A para começar.`,
    dados: "Post A criado pela conta A. Conta B como usuária sem autoria.",
    passos: ["Na primeira aba, abra Edit do Post A como conta A.", "Em outra aba do mesmo navegador, saia da conta A e entre com a conta B.", "Na primeira aba, sem recarregar, clique em Delete e confirme.", "Abra Posts e confira Post A."],
    esperado: "O envio com a conta B mostra Forbidden (HTTP 403). A publicação Post A permanece com o título e o corpo originais.",
    candidato: "Sim", motivo: "Valida que o servidor usa a sessão e a autoria atuais para a decisão.", riscos: ["R-01"], fontes: [editForm, remove, post, `${auth} · load_logged_in_user(), linhas 32–43`],
  }),
  caso(26, "RNF-01", {
    titulo: "Verificar armazenamento e exibição da senha fictícia", tipo: "Não funcional / segurança básica", tecnica: "Inspeção de HTML e consulta SQLite somente leitura", prioridade: "Alta",
    pre: anon, dados: "Credenciais da conta A e verificação local descrita na aba Rastreabilidade.",
    passos: ["Registre a conta A no navegador e aguarde Log In.", "Abra o código-fonte HTML da tela após o redirecionamento e procure a senha fictícia.", "No mesmo ambiente e base local, siga a verificação de hash na aba Rastreabilidade."],
    esperado: "A busca acha zero ocorrências da senha no HTML. A conferência no banco retorna True para um único registro, para valor diferente da entrada e para hash válido.",
    candidato: "Sim", motivo: "A verificação do hash e da resposta pode ser automatizada sem expor o valor armazenado.", riscos: ["R-05"], fontes: [register, login, `${schema}, linhas 7–11`],
  }),
  caso(27, "RNF-02", {
    titulo: "Preservar criação e edição após reinício local", tipo: "Não funcional / confiabilidade", tecnica: "Reinício controlado com dados de controle", prioridade: "Alta",
    pre: doisPostsA, dados: "Edite Post A para «Post A persistente» e «Corpo persistente». Post B permanece como controle.",
    passos: ["Edite Post A e confira o título e o corpo novos em Posts.", "Encerre o processo local e inicie novamente com a mesma configuração e o mesmo arquivo SQLite. Não execute init-db neste reinício.", "Abra Posts em janela anônima e confira os dois artigos."],
    esperado: "Após o reinício, Posts exibe o título e o corpo atualizados de Post A e conserva Post B.",
    candidato: "Sim", motivo: "A validação pode reiniciar o processo reutilizando um arquivo SQLite isolado.", riscos: ["R-03"], fontes: [create, update, list, `${db} · get_db(), linhas 9–20`, "flaskr/__init__.py · create_app(), linhas 6–21"],
  }),
  caso(28, "RNF-03", {
    titulo: "Concluir cadastro e publicação usando teclado", tipo: "Não funcional / usabilidade", tecnica: "Inspeção por tarefa no Safari", prioridade: "Média",
    pre: `${anon} Safari com navegação por Tab habilitada. [CONFIRMAR] Configuração e foco visível no navegador usado.`,
    dados: "Credenciais da conta A. Title Teclado QA. Body Publicado com teclado.",
    passos: ["Abra a página inicial pelo endereço. Use Tab para focar Register e Return para abri-lo.", "Percorra Username, Password e Register com Tab. Preencha os campos e acione Register pelo teclado.", "Na tela Log In, entre com as mesmas credenciais usando o teclado.", "Em Posts, acione New pelo teclado. Percorra Title, Body e Save com Tab, preencha e salve. Observe o foco enquanto navega."],
    esperado: "Todos os campos e botões dos dois formulários recebem foco visível. A página final lista Teclado QA com o corpo informado.",
    candidato: "Não", motivo: "O foco visível e a experiência efetiva por teclado precisam de observação humana.", riscos: ["R-08", "R-12"], fontes: [registerForm, loginForm, createForm, base, feed],
  }),
];
