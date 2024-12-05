import difflib
import getpass
import os
import re
from datetime import datetime, timedelta
import warnings
import time

import pyautogui
import pytesseract
import win32clipboard
from PIL import Image, ImageEnhance
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until
from pywinauto_recorder.player import set_combobox
from rich.console import Console
from worker_automate_hub.api.ahead_service import save_xml_to_downloads
from worker_automate_hub.api.client import (
    get_config_by_name,
    get_status_nf_emsys,
)
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    delete_xml,
    error_after_xml_imported,
    get_xml,
    import_nfe,
    incluir_registro,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_all_emsys,
    login_emsys,
    select_documento_type,
    carregamento_import_xml,
    set_variable,
    type_text_into_field,
    warnings_after_xml_imported,
    worker_sleep,
    check_nota_importada,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def entrada_de_notas_36(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que realiza entrada de notas no ERP EMSys(Linx).

    """
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        # Seta config entrada na var nota para melhor entendimento
        nota = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()

        # Download XML
        console.log("Realizando o download do XML..\n")
        await save_xml_to_downloads(nota["nfe"])

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field(
                "Nota Fiscal de Entrada", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(6)

        # Procura campo documento
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        document_type = await select_documento_type(
            "NOTA FISCAL DE ENTRADA ELETRONICA - DANFE"
        )
        if document_type.sucesso == True:
            console.log(document_type.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=document_type.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(4)

        # Clica em 'Importar-Nfe'
        imported_nfe = await import_nfe()
        if imported_nfe.sucesso == True:
            console.log(imported_nfe.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=imported_nfe.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(5)

        await get_xml(nota.get("nfe"))
        await worker_sleep(3)

        # VERIFICANDO A EXISTENCIA DE WARNINGS
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            warning_work = await warnings_after_xml_imported()
            if warning_work.sucesso == True:
                console.log(warning_work.retorno, style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=warning_work.retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                )

        # VERIFICANDO A EXISTENCIA DE ERRO
        erro_pop_up = await is_window_open("Erro")
        if erro_pop_up["IsOpened"] == True:
            error_work = await error_after_xml_imported()
            return RpaRetornoProcessoDTO(
                sucesso=error_work.sucesso,
                retorno=error_work.retorno,
                status=error_work.status,
            )

        app = Application().connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]

        # INTERAGINDO COM A NATUREZA DA OPERACAO
        cfop = int(nota.get("cfop"))
        nop = ''
        console.print(f"Inserindo a informação da CFOP, caso se aplique {cfop} ...\n")
        if str(cfop).startswith("510"):
            combo_box_natureza_operacao = main_window.child_window(
                class_name="TDBIComboBox", found_index=0
            )
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "1102-COMPRA DE MERCADORIA ADQ. TERCEIROS - 1.102")
            nop = "1102-COMPRA DE MERCADORIA ADQ. TERCEIROS - 1.102"
            await worker_sleep(3)
        elif str(cfop).startswith("540"):
            combo_box_natureza_operacao = main_window.child_window(
                class_name="TDBIComboBox", found_index=0
            )
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "1403-COMPRA DE MERCADORIAS - 1.403")
            nop = "1403-COMPRA DE MERCADORIAS - 1.403"
            await worker_sleep(3)
        else:
            console.print(
                "Erro mapeado, CFOP diferente de inicio com 540 ou 510, necessario ação manual ou ajuste no robo...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro mapeado, CFOP diferente de inicio com 540 ou 510, necessario ação manual ou ajuste no robo.",
                status=RpaHistoricoStatusEnum.Falha,
            )

        # INTERAGINDO COM O CAMPO ALMOXARIFADO
        fornecedor = nota.get("nomeFornecedor")
        filialEmpresaOrigem = nota.get("filialEmpresaOrigem")
        console.print(
            f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...\n"
        )
        try:
            new_app = Application(backend="uia").connect(
                title="Informações para importação da Nota Fiscal Eletrônica"
            )
            window = new_app["Informações para importação da Nota Fiscal Eletrônica"]
            edit = window.child_window(
                class_name="TDBIEditCode", found_index=3, control_type="Edit"
            )
            valor_almoxarifado = filialEmpresaOrigem + "50"
            edit.set_edit_text(valor_almoxarifado)
            edit.type_keys("{TAB}")
        except Exception as e:
            console.print(f"Erro ao iterar itens de almoxarifado: {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao iterar itens de almoxarifado: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(2)
        console.print("Clicando em OK... \n")

        max_attempts = 3
        i = 0
        while i < max_attempts:
            console.print("Clicando no botão de OK...\n")
            try:
                try:
                    btn_ok = main_window.child_window(title="Ok")
                    btn_ok.click()
                except:
                    btn_ok = main_window.child_window(title="&Ok")
                    btn_ok.click()
            except:
                console.print("Não foi possivel clicar no Botão OK... \n")

            await worker_sleep(3)

            console.print(
                "Verificando a existencia da tela Informações para importação da Nota Fiscal Eletrônica...\n"
            )

            try:
                informacao_nf_eletronica = await is_window_open(
                    "Informações para importação da Nota Fiscal Eletrônica"
                )
                if not informacao_nf_eletronica["IsOpened"]:
                    console.print(
                        "Tela Informações para importação da Nota Fiscal Eletrônica fechada, seguindo com o processo"
                    )
                    break
            except Exception as e:
                console.print(
                    f"Tela Informações para importação da Nota Fiscal Eletrônica encontrada. Tentativa {i + 1}/{max_attempts}."
                )

            i += 1

        if i == max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Número máximo de tentativas atingido, Não foi possivel finalizar os trabalhos na tela de Informações para importação da Nota Fiscal Eletrônica",
                status=RpaHistoricoStatusEnum.Falha,
            )


        waiting_for_delay = await carregamento_import_xml()
        if waiting_for_delay.sucesso:
            console.print(waiting_for_delay.retorno)
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=waiting_for_delay.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        console.print(
            "Verificando a existencia de POP-UP de Itens não localizados ou NCM ...\n"
        )
        itens_by_supplier = await is_window_open_by_class("TFrmAguarde", "TMessageForm")
        if itens_by_supplier["IsOpened"] == True:
            console.print(
            "Tela de POP-UP de Itens não localizados ou NCM encontrado ...\n"
            )
            itens_by_supplier_work = await itens_not_found_supplier(nota.get("nfe"))
            if itens_by_supplier_work["window"] == "NCM" or itens_by_supplier_work["window"] == "MultiplasRef":
                console.log(itens_by_supplier_work["retorno"], style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=itens_by_supplier_work["retorno"],
                    status=RpaHistoricoStatusEnum.Falha,
                )

        await worker_sleep(3)

        # VERIFICANDO A EXISTENCIA DE ERRO
        erro_pop_up = await is_window_open("Erro")
        if erro_pop_up["IsOpened"] == True:
            error_work = await error_after_xml_imported()
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=error_work.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        # # Trabalhando com o NOP Nota
        # console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        # console.print("Selecionando o NOP da Nota...\n")
        # document_type = await select_nop_document_type(nop)
        # send_keys("{DOWN " + ("1") + "}")
        # if document_type.sucesso == True:
        #     console.log(document_type.retorno, style="bold green")
        # else:
        #     return RpaRetornoProcessoDTO(
        #         sucesso=False,
        #         retorno=document_type.retorno,
        #         status=RpaHistoricoStatusEnum.Falha,
        #     )


        await worker_sleep(2)
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()
        console.print("Acessando a aba de Pagamentos... \n")
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        send_keys("{DOWN " + ("7") + "}")

        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TPageControl")

        panel_TabPagamento = panel_TTabSheet.child_window(class_name="TTabSheet")

        panel_TabParcelamento = panel_TTabSheet.child_window(title="Parcelamento")

        tipo_cobranca = panel_TabParcelamento.child_window(
            class_name="TDBIComboBox", found_index=0
        )

        console.print("Verificando o tipo de cobrança selecionado... \n")
        tipo_selecionado = tipo_cobranca.window_text()
        if "boleto" in tipo_selecionado.lower() or 'carteira' in tipo_selecionado.lower():
            console.print(f"Tipo de cobrança corretamente selecionado {tipo_selecionado}... \n")
        else:
            console.print(f"Tipo de cobrança não foi selecionado corretamente, interagindo com o campo para selecionar o campo corretamente... \n")
            tipo_cobranca.click()
            try:
                set_combobox("||List", "BANCO DO BRASIL BOLETO")
            except:
                set_combobox("||List", "CARTEIRA")
        
        await worker_sleep(2)
        tab_valores = panel_TabPagamento.child_window(title="Valores")
        valores_restantes = tab_valores.child_window(
            class_name="TDBIEditNumber", found_index=1
        )

        valores_informado = tab_valores.child_window(
            class_name="TDBIEditNumber", found_index=2
        )

        valores_informado_text = valores_informado.window_text()
        valores_restantes_text = valores_restantes.window_text()

        if '0,00' in valores_informado_text:
            console.print(f"Pagamento não informado, registrando... \n")
            dt_emissao = nota.get("dataEmissao")
            data_emissao_dt = datetime.strptime(dt_emissao, "%d/%m/%Y")
            dt_emissao = data_emissao_dt + timedelta(days=20)
            dt_vencimento = dt_emissao.strftime("%d/%m/%Y")
            console.print(f"Informando a data de vencimento, {dt_vencimento}... \n")

            vencimento = panel_TabParcelamento.child_window(
                class_name="TDBIEditDate"
            )
            vencimento.set_edit_text(dt_vencimento)

            await worker_sleep(2)
            console.print(f"Inserindo o valor {valores_restantes_text}... \n")
            valor = panel_TabParcelamento.child_window(
                class_name="TDBIEditNumber", found_index=3
            )
            valor.set_edit_text(valores_restantes_text)
            await worker_sleep(2)
            console.print(f"Adicionando o pagamento... \n")
            btn_add = panel_TabParcelamento.child_window(
                class_name="TDBIBitBtn", found_index=1
            )
            btn_add.click()

            await worker_sleep(4)
            console.print(f"Verificando se o pagamento foi adicionado com sucesso... \n")
            valores_informado = tab_valores.child_window(
                class_name="TDBIEditNumber", found_index=2
            )
            valores_informado_text = valores_informado.window_text()
            if '0,00' in valores_informado_text:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao adicionar o pagamento, valor informado {valores_informado_text}.",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            console.print(f"Processo de incluir pagamento realizado com sucesso... \n")

        await worker_sleep(3)
        console.print(f"Incluindo registro...\n")
        try:
            ASSETS_PATH = "assets"
            inserir_registro = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\entrada_notas\\IncluirRegistro.png", confidence=0.8
            )
            pyautogui.click(inserir_registro)
        except Exception as e:
            console.print(
                f"Não foi possivel incluir o registro utilizando reconhecimento de imagem, Error: {e}...\n tentando inserir via posição...\n"
            )
            await incluir_registro()

        await worker_sleep(3)
        console.print(
            "Verificando a existencia de POP-UP de Itens que Ultrapassam a Variação Máxima de Custo ...\n"
        )
        itens_variacao_maxima = await is_window_open_by_class(
            "TFrmTelaSelecao", "TFrmTelaSelecao"
        )
        if itens_variacao_maxima["IsOpened"] == True:
            app = Application().connect(class_name="TFrmTelaSelecao")
            main_window = app["TFrmTelaSelecao"]
            send_keys("%o")

        
        # Verificando se possui pop-up de Warning 
        await worker_sleep(6)
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            app = Application().connect(title="Warning")
            main_window = app["Warning"]
            main_window.set_focus()

            console.print(f"Obtendo texto do Warning...\n")
            console.print(f"Tirando print da janela do warning para realização do OCR...\n")

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = f"C:\\Users\\{username}\\Downloads\\warning_popup_{nota.get("nfe")}.png"
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(
                f"Texto Full capturado {captured_text}...\n"
            )
            os.remove(path_to_png)
            if 'movimento não permitido' in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Filial: {filialEmpresaOrigem} está com o livro fechado ou encerrado, verificar com o setor fiscal",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            elif 'informe o tipo de' in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Mensagem do Warning, Informe o tipo cobraça ",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            else:
                return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Warning não mapeado para seguimento do robo, mensagem: {captured_text}",
                status=RpaHistoricoStatusEnum.Falha,
                )
        

        # VERIFICANDO A EXISTENCIA DE ERRO
        erro_pop_up = await is_window_open("Erro")
        if erro_pop_up["IsOpened"] == True:
            error_work = await error_after_xml_imported()
            return RpaRetornoProcessoDTO(
                sucesso=error_work.sucesso,
                retorno=error_work.retorno,
                status=error_work.status,
            )
        
        await worker_sleep(3)
        # Verifica se a info 'Nota fiscal incluida' está na tela
        nf_imported = await check_nota_importada(nota.get("nfe"))
        if nf_imported.sucesso == True:
            await worker_sleep(3)
            console.print("\nVerifica se a nota ja foi lançada...")
            nf_chave_acesso = int(nota.get("nfe"))
            status_nf_emsys = await get_status_nf_emsys(nf_chave_acesso)
            if status_nf_emsys.get("status") == "Lançada":
                console.print("\nNota lançada com sucesso, processo finalizado...", style="bold green")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Nota Lançada com sucesso!",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            else:
                console.print("Erro ao lançar nota", style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pop-up nota incluida encontrada, porém nota não encontrada no EMSys - Reprocessar",
                    status=RpaHistoricoStatusEnum.Falha,
                )
        else:
            console.print("Erro ao lançar nota", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao lançar nota, erro: {nf_imported.retorno}",
                status=RpaHistoricoStatusEnum.Falha,
            )

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}

    finally:
        # Deleta o xml
        await delete_xml(nota.get("nfe"))
