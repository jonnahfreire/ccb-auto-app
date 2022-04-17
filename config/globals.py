from os import environ, path, sys


sist_name = "ccb-autom"

chrome_driver_path = "/usr/local/bin/chromedriver" if not sys.platform == "win32" else ""
chrome_window_size = "900,600" 
selenium_brw_size = "1920,1080"
screen_size = chrome_window_size.split(',')

user_docs_path = path.join("/home", environ["USER"], "Documentos" or "Documents")\
    if not sys.platform == "win32" else path.join(environ['USERPROFILE'], "Documentos" or "Documents")


sist_path = path.join(user_docs_path, sist_name)

config = ".config" if not sys.platform == "win32" else "config"
db_path = path.join(sist_path, config, "user.db")
log_path = path.join(sist_path, config, "logs.db")

struct_dirs_1000 = ["1000", "3006", "3007", "3008", 
                    "3010", "3011", "3012", "3014", 
                    "3015", "3016", "3023", "3026", 
                    "3027"]

struct_dirs_1010 = ["1010", "3010", "3011", "3012",
                    "3016", "3020", "3021", "3023", 
                    "3027", "3030", "3051", "3052", 
                    "3300", "3301", "3302", "3006",
                    "3007", "3008", "3014", "1120", 
                    "11101", "11102"]

struct_dirs = [struct_dirs_1000, struct_dirs_1010]

accepted_accounts = struct_dirs_1000 + struct_dirs_1010

extensions = [".pdf", ".png", ".jpg", ".jpeg"]

form_ids = ['form-competencias', 'form-executar-programa', 
            'f-calendar', 'f_main', 'form-competencia', 'f_fecharacessoremoto', 
            'form-selecionarlocalpadrao', 'form-selecionarlocalidade']
            
debt_code_list = [
    '104 - DIREITOS REALIZAVEIS',
    '1041 - TITULOS A RECEBER',
    '1043 - ADIANTAMENTOS A FUNCIONARIOS',
    '10410 - IMPOSTOS E CONTRIBUICOES A COMPENSAR',
    '1049 - DEPOSITOS EM GARANTIA DE LOCACAO',
    '106 - CONTAS CORRENTES',
    '10612 - TRANSFERENCIAS COLETAS FUNDO MUSICAL',
    '111 - CASAS DE ORACAO EM CONSTRUCAO',
    '11101 - BR 05-0024 - BOA VIAGEM - FAZENDA PEREIRO',
    '11102 - BR 05-0632 - PEDRA BRANCA - DISTRITO MINEIROLANDIA',
    '112 - CASAS DE ORACAO EM REFORMA',
    '1120 - REFORMA LAGOA DO MATO',
    '300 - SERVICOS E FORNECIMENTOS EXTERNOS',
    '3000- SERV MANUT DE IMOVEIS E INSTALACOES',
    '3001- SERV MANUT DE MOVEIS E UTENSILIOS',
    '3002- SERV MANUT DE ORGAOS E INSTRUMENTOS',
    '3003- SERV MANUT DE MAQUINAS E FERRAMENTAS',
    '3004- SERVPROFISSIONAIS ADMINISTRATIVOS',
    '3005- FRETES E CARRETOS',
    '3006- ENERGIA ELETRICA E ILUMINACAO',
    '3007- AGUA E ESGOTO',
    '3008- DESPESAS COM TELECOMUNICACOES',
    '3009- ALUGUEIS',
    '30010- SERV MANUT DE EQUIPAMENTOS E SISTEMAS',
    '30011- SERV MANUT DE VEICULOS',
    '30012- SERV MANUT PINTURAS EM GERAL',
    '30013- SERV MANUT AREAS E JARDINS',
    '30014- SERV MANUT E REPAROS ELETRICOS',
    '30015- SERV MANUT EM SOM, ACUSTICA E TELEFONIA',
    '30016- SERV MANUT ALARME',
    '30017- SERV MANUT LUZ DE EMERGENCIA',
    '30018- SERV MANUT PARA-RAIOS',
    '30019- SERV MANUT SINALIZACAO E SEGURANCA',
    '30020- SERV MANUT RECARGA DE EXTINTORES',
    '30021- SERV MANUT CORTINAS E PASSADEIRAS',
    '30022- SERV MANUT TELHADOS E COBERTURAS',
    '30023- SERV MANUT DE PISOS E REVESTIMENTOS',
    '30024- SERV MANUT DE IMPERMEABILIZACOES',
    '30025- SERV MANUT E PEQUEN ADAPT EM ALVENARIA',
    '30026- SERV DE LOCACAO DE CACAMBAS',
    '30027- SERV DE LOCACAO DE EQUIPAMENTOS',
    '30028- SERVICOS PRESTADOS PARA MEDICINA E SEGU',
    '301- MATERIAIS DE MANUTENCAO E CONSUMO',
    '3010- MAT MANUT DE IMOVEIS E INSTALACOES',
    '3011- MAT MANUT DE MOVEIS E UTENSILIOS',
    '3012- MAT MANUT DE ORGAOS E INSTRUMENTOS',
    '3013- MAT MANUT DE MAQUINAS E FERRAMENTAS',
    '3014- MAT DE LIMPEZA E CONSERVACAO',
    '3015- MAT PARA BATISMOS E SANTAS CEIAS',
    '3016- IMPRESSOS E MATERIAIS DE ESCRITORIO',
    '3017- DESPESAS COM COPIADORAS',
    '3018- MATERIAIS DE EMBALAGENS',
    '3019- PROCESSAMENTO DE DADOS',
    '30110- MAT MANUT DE VEICULOS',
    '30111- MATERIAIS MANUT PINTURAS EM GERAL',
    '30112- MATERIAIS MANUT AREAS E JARDINS',
    '30113- MATERIAIS MANUT ELETRICOS',
    '30114- MATERIAIS MANUT HIDRAULICA',
    '30115- MATERIAIS MANUT SOM, ACUSTICA E TELEFON',
    '30116- MATERIAIS MANUT ALARMES',
    '30117- MATERIAIS MANUT LUZ DE EMERGENCIA',
    '30118- MATERIAIS MANUT PARA-RAIOS',
    '30119- MATERIAIS MANUT SINALIZACAO E SEGURANCA',
    '30120- MATERIAIS MANUT DE RECARGA DE EXTINTORE',
    '30121- MATERIAIS MANUT DE CORTINAS E PASSADEIR',
    '30122- MATERIAIS MANUT DE TELHADOS E COBERTURA',
    '30123- MATERIAIS MANUT DE PISOS E REVESTIMENTO',
    '30124- MATERIAIS MANUT DE IMPERMEABILIZACOES',
    '30125- MATERIAIS MANUT PEQUEN REPAROS EM ALVEN',
    '30126- MATERIAL DE PRIMEIROS SOCORROS',
    '30128- MATERIAL DE MEDICINA E SEGURANCA DO TRA',
    '302- DESPESAS GERAIS',
    '3020- IMPOSTOS E TAXAS DIVERSAS',
    '3021- DESPESAS POSTAIS',
    '3022- DESP COM ASSEMB REUN MINISTERIAIS',
    '3023- DESP LEGAIS CUSTAS CARTORIOS',
    '3025- DESP COM DISTRIBDE BIBLIAS E HINARIOS',
    '3026- DESPESA COM CONDUCAO E LOCOMOCAO',
    '3027- DESPESA COM ALIMENTACAO E REFEICAO',
    '3028- DOACOES BIBLIAS E HINARIOS',
    '3029- SEGUROS',
    '30210- BENS DE PEQUENO VALOR',
    '30211- COMBUSTIVEIS E LUBRIFICANTES',
    '30212- DESPESAS COM LAVANDERIAS',
    '30217- DEPRECIACOES',
    '30218- AMORTIZACOES',
    '30219- PUBLICACOES',
    '30220- CURSOS, LIVROS E TREINAMENTOS DE MEDICI',
    '303- DESPESAS FINANCEIRAS',
    '3030- DESPESAS BANCARIAS',
    '3031- DESPESA TARIFA CARTAO COLETA',
    '3035- IR PAGO RENDAS APLICACAO FINANCEIRA',
    '3036- MULTAS E JUROS',
    '3037- VARIACAO CAMBIAL PASSIVA',
    '305- DESPESAS COM SETOR MUSICAL',
    '3050- DOACOES DE INSTRUMENTOS MUSICAIS',
    '3051- MANUTENCAO INSTRMUSICAIS ACESSORIOS',
    '3052- DESPESAS COM ENSINO MUSICAL',
    '306- DESPESAS SOCIAIS',
    "3060- SALARIOS E ORDENADOS",
    "3061- PREVIDENCIA SOCIAL-INSS",
    "3062- F.G.T.S",
    "3063- P.I.S",
    "3064- ENCARGOS SOCIAIS DIVERSOS",
    "3065- SEGUROS ACIDENTES DE TRABALHO",
    "3066- VALE TRANSPORTE",
    "3067- CESTA BASICA - VALE REFEICAO",
    "3068- FERIAS",
    "3069- 13 SALARIO",
    "30610- RESCISOES TRABALHISTAS",
    "30611- HORAS EXTRAS E DSR",
    "30612- CURSOS E TREINAMENTOS",
    "30613- CONVENIO MEDICO",
    "30614- CONVENIO ODONTOLOGICO",
    "30615- BOLSA AUXILIO ESTAGIARIOS",
    "310- ATENDIMENTOS",
    "3106- HIGIENE PESSOAL",
    "3109- ASSISTENCIA SOCIAL",
    "31010- DESPESAS COM FUNERAL",
    "320- DESPESAS  VIAGENS NAIONAIS",
    "3201- DESPESAS  HOSPEDAGEM NAIONAIS",
    "3202- DESPESAS  ALIMENTACAO NAIONAIS",
    "321- DESPESAS  VIAGENS INTERNAIONAIS",
    "3211- DESPESAS  HOSPEDAGEM INTERNAIONAIS",
    "3212- DESPESAS  ALIMENTACAO INTERNACIONAIS",
    "330- REUNIOES GERAIS",
    "3300- GENEROS ALIMENTICIOS PARA REUNIOES",
    "3301- GAS DE COZINHA",
    "3302- PEQUENOS UTENSILIOS DE COZINHA",
    "3303- DESPESAS COM VIAGENS DE RETORNO-REUNIOES",
    "3304- UNIFORMES EM GERAL",
    "3305- HIGIENE PESSOAL",
    "340- TRANSFERENCIAS POUTRAS ADMINISTRACOES",
    "3401- TRANSF.REMETIDAS OBRA DA PIEDADE",
    "3402- TRANSF.REMETIDAS VIAGENS MISSIONARIAS",
    "3403- TRANSF.REMETIDAS ADMINISTRATIVAS",
    "3405- TRANSF.REMETIDAS SETOR MUSICAL",
    "3406- TRANSF.REMETIDAS ASSEMBLEIAS E REUNIOES",
    "3408- TRANSF.REMETIDAS BIBLIAS E HINARIOS",
    "3409- TRANSF.REMETIDAS NECESSIDADES DIVERSAS",
    "34010- TRANSF.REMETIDAS ESPECIAL PIEDADE",
    "350- DESPESAS",
    "3500- PERDAS EVENTUAIS",
    "3501- INDENIZACOES"
]

