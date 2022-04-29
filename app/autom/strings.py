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

# Despesa
new_debt_select_box = '//*[@id="mainContent"]/div[2]/div[3]/div/div[1]/div/div/div[1]/button/span[2]'
new_debt_select_element =  'Despesa'

new_group_debt_select_box = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/button/span[2]'
new_group_debt_select_element = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/ul/li[4]/a'

new_intern_trans_select_box = '//*[@id="mainContent"]/div[2]/div[3]/div/div[1]/div/div/div[1]/button'
new_intern_trans_select_element = '//*[@id="mainContent"]/div[2]/div[3]/div/div[1]/div/div/div[1]/ul/li[6]/a'
btn_save_intern_transf = '//*[@id="f_main"]/div[5]/button[1]'

new_receive_select_box = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/button/span[2]'
new_receive_select_element = '//*[@id="mainContent"]/div[2]/div[2]/div/div[1]/div/div/div[1]/ul/li[1]/a'

save_debt_btn = '//*[@id="f_main"]/div[11]/button[1]'
save_and_new_debt_btn = '//*[@id="f_main"]/div[11]/button[2]'

file_upload_place = '//*[@id="tabAnexoAnexar"]/div/label'

modal_btn_no_xpath = '/html/body/div[17]/div[3]/a[2]'
modal_header_success_confirm = '/html/body/div[17]/div[3]/a' # Modal que aparece quando confirma o lançamento
modal_header = '/html/body/div[17]/div[1]/h3' # Modal que aparece quando confirma o lançamento e já existe um documento lançado com o mesmo número
confirm_modal_header = '/html/body/div[17]/div[3]/a[1]' # Botão de confirmar o modal que aparece quando já existe um lançamento com o mesmo número
reject_modal_header = '/html/body/div[17]/div[3]/a[2]' # Botão de cancelar o modal que aparece quando já existe um lançamento com o mesmo número


# Despesa em lote
debt_lot_select_element = '//*[@id="mainContent"]/div[2]/div[3]/div/div[1]/div/div/div[1]/ul/li[4]/a'
debt_lot_element_link_text = 'Despesa em Lote'

# Despesa em lote paths
# Main form
lot_form = '//*[@id="f_main"]'
add_debt_btn = '//*[@id="btn-adicionar"]'

#modal
modal_form = '//*[@id="form-despesa"]'
modal_date = '//*[@id="f_modaldata"]'
modal_doc_type = '//*[@id="s2id_f_modaltipodocumento"]'
modal_doc_num = '//*[@id="f_modaldocumento"]'
modal_doc_value = '//*[@id="f_modalvalor"]'
modal_emitter = '//*[@id="s2id_f_modalfornecedor"]'
modal_debt_type = '//*[@id="s2id_f_modaldespesa"]'
modal_hidtory = '//*[@id="s2id_f_modalhistorico"]'
modal_complement = '//*[@id="f_modalcomplemento"]'
modal_cost_center = '//*[@id="s2id_f_modalcentrocusto"]'
modal_debt_juros = '//*[@id="f_modaljuros"]'
modal_btn_confirm = '//*[@id="btn-adicionar-despesa"]'
modal_link_cancel = '//*[@id="form-despesa"]/div[2]/a'

# payment data
payment_date = '//*[@id="f_datapagamento"]'
payment_form = '//*[@id="f_formapagamento"]'
check_number = '//*[@id="f_numerocheque"]'
debt_account = '//*[@id="s2id_f_conta"]'
payment_history = '//*[@id="s2id_f_historico"]'
file_upload_btn = '//*[@id="tabAnexoAnexar"]'
lot_btn_save = '//*[@id="f_main"]/div[6]/button[1]'
lot_btn_save_new = '//*[@id="f_main"]/div[6]/button[2]'

# movimentação interna
intern_mov_element_xpath = '//*[@id="mainContent"]/div[2]/div[3]/div/div[1]/div/div/div[1]/ul/li[6]/a'
intern_mov_element_link_text = 'Movimentação Interna'

# Receitas
receivings_element_xpath = '//*[@id="mainContent"]/div[2]/div[3]/div/div[1]/div/div/div[1]/ul/li[1]/a'
receivings_element_link_text = 'Receita'