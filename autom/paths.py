ccb_siga = "https://appl2.ccbsiga.congregacao.org.br/index.aspx"

input_user =  '//*[@id="f_usuario"]'
input_pass ='//*[@id="f_senha"]'
login_confirm = '//*[@id="form1"]/div[4]/div[1]/button'

work_month_date_select = '//*[@id="a_competencia"]'

open_month_date_options =  "Outros Meses"
open_select_month_date = '//*[@id="select2-chosen-10"]'
menu_tesouraria = '//*[@id="link_modulo_TES"]/span'
caixa_bancos = "/html/body/div[3]/div[1]/ul/li[8]/ul/li[2]/a"

select_doc_emitter_opt1 = '//*[@id="select2-chosen-14"]'
select_doc_emitter_opt2 = '//*[@id="s2id_f_centrocusto_rateio"]'

new_debt_select_box = '#mainContent > div.page-content > div:nth-child(3) > div > div:nth-child(1) > div > div > div:nth-child(1) > button > span.hidden-phone'
new_debt_select_element =  'Despesa'

new_group_debt_select_box = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/button/span[2]'
new_group_debt_select_element = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/ul/li[4]/a'
new_intern_trans_select_box = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/button/span[2]'
new_intern_trans_select_element = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/ul/li[6]/a'
new_receive_select_box = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/button/span[2]'
new_receive_select_element = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/ul/li[1]/a'

save_debt_btn = '//*[@id="f_main"]/div[11]/button[1]'
save_and_new_debt_btn = '//*[@id="f_main"]/div[11]/button[2]'

file_upload_place = '//*[@id="tabAnexoAnexar"]/div/label'

modal_header_success_confirm = '/html/body/div[17]/div[3]/a' # Modal que aparece quando confirma o lançamento
modal_header = '/html/body/div[17]/div[1]' # Modal que aparece quando confirma o lançamento e já existe um documento lançado com o mesmo número
confirm_modal_header = '/html/body/div[17]/div[3]/a[1]' # Botão de confirmar o modal que aparece quando já existe um lançamento com o mesmo número
reject_modal_header = '/html/body/div[17]/div[3]/a[2]' # Botão de cancelar o modal que aparece quando já existe um lançamento com o mesmo número


