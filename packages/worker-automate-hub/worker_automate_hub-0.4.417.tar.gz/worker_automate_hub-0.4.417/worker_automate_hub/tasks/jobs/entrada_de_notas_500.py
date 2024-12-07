import getpass
import os
import re
import warnings

import pyautogui
import pytesseract
from PIL import Image, ImageEnhance
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until
from pywinauto_recorder.player import set_combobox
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
    sync_get_config_by_name,
    get_status_nf_emsys,
)
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    error_after_xml_imported,
    get_xml_outras_empresas,
    import_nfe,
    incluir_registro,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_all_emsys,
    login_emsys,
    select_documento_type,
    select_nop_document_type,
    set_variable,
    type_text_into_field,
    verify_nf_incuded,
    worker_sleep,
    check_nota_importada,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def entrada_de_notas_500(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
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

        #Verifica se a nota ja foi lançada
        console.print("\nVerifica se a nota ja foi lançada...")
        nf_chave_acesso = int(nota.get("nfe"))
        status_nf_emsys = await get_status_nf_emsys(nf_chave_acesso)
        if status_nf_emsys.get("status") == "Lançada":
            console.print("\nNota ja lançada, processo finalizado...", style="bold green")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Nota já lançada",
                status=RpaHistoricoStatusEnum.Descartado,
            )
        else:
            console.print("\nNota não lançada, iniciando o processo...")
        

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
            "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077"
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

        nf_outras_empresas = await get_xml_outras_empresas()
        if nf_outras_empresas.sucesso == True:
            console.log(nf_outras_empresas.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=nf_outras_empresas.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(5)

        #INTERAGINDO COM A TELA DE NOTAS DE OUTRAS EMPRESAS
        app = Application().connect(class_name="TFrmImportarNotaOutraEmpresa")
        main_window = app["TFrmImportarNotaOutraEmpresa"]
        console.print("A tela de Importar Nota de Outra Empresa foi encontrada!")

        console.print('Inserindo o codigo da empresa 171...')
        edit = main_window.child_window(
            class_name="TDBIEditCode", found_index=0
        )
        edit.set_edit_text("171")

        console.print('Inserindo a data de emissão da nota')
        dt_emissao = nota.get("dataEmissao")
        numero_nota = nota.get("numeroNota")
        filialEmpresaOrigem = nota.get("filialEmpresaOrigem")
        
        edit = main_window.child_window(
            class_name="TDBIEditDate", found_index=0
        )
        edit.set_edit_text(dt_emissao)
        edit = main_window.child_window(
            class_name="TDBIEditDate", found_index=1
        )
        edit.set_edit_text(dt_emissao)

        console.print('Inserindo o numero da nota')
        edit = main_window.child_window(
            class_name="TDBIEditString", found_index=0
        )
        edit.set_edit_text(numero_nota)

        await worker_sleep(2)

        pesquisar_full_path = "assets\\entrada_notas\\PesquisarNFOutrasEmpresas.png"
        try:
            button_location = pyautogui.locateCenterOnScreen(pesquisar_full_path, confidence=0.6)
            if button_location:
                pyautogui.click(button_location)
                console.print("Botão 'Pesquisar' clicado com sucesso!")
        except pyautogui.ImageNotFoundException:
            window_rect = main_window.rectangle()
            console.print(f"Area que sera utulizada para o screenshot {window_rect}...\n")

            try:
                button_location = pyautogui.locateCenterOnScreen(pesquisar_full_path, region=(window_rect.left, window_rect.top, window_rect.width(), window_rect.height()))
                if button_location:
                    button_location = (button_location.x + window_rect.left, button_location.y + window_rect.top)
                    console.print(f"Botão encontrado nas coordenadas: {button_location}")
                    pyautogui.click(button_location)
            except pyautogui.ImageNotFoundException:
                console.print("Erro - Botão Pesquisar na tela de Importação de Outras Empresas não foi encontrado após tentar capturar a tela")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Erro - Botão Pesquisar na tela de Importação de Outras Empresas não foi encontrado após tentar capturar a tela",
                    status=RpaHistoricoStatusEnum.Falha,
                )
        except Exception as e:
            console.print(
                f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de Pesquisar na tela Importação de Outras Empresas,Error: {e}...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de Pesquisar na tela Importação de Outras Empresas,Error: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        i = 0
        max_attempts = 17

        while i < max_attempts:
            i += 1
            console.print("Verificando se a nota foi encontrada...\n")
            try:
                main_window.set_focus()
                no_data_full_path = "assets\\entrada_notas\\no_data_display.png"
                img_no_data = pyautogui.locateCenterOnScreen(no_data_full_path, confidence=0.6)
                if img_no_data:
                    console.print("'No data display' ainda aparente. Tentando novamente...")
                    await worker_sleep(10)
            except pyautogui.ImageNotFoundException:
                console.print("'No data display' não encontrado na tela!")
                break

            except Exception as e:
                console.print(f"Ocorreu um erro: {e}")


        console.print(f"Clicando em Importar")
        pyautogui.press('tab', presses=2)
        importar_btn_full_path = "assets\\entrada_notas\\importar_nf_outras_empresa.png"
        try:
            button_location = pyautogui.locateCenterOnScreen(importar_btn_full_path, confidence=0.6)
            if button_location:
                pyautogui.moveTo(button_location)
                await worker_sleep(1)
                pyautogui.click(button_location)
                console.print("Botão 'Importar' clicado com sucesso!")
                await worker_sleep(1)
                
                attempts = 0
                max_attempts = 7
                while attempts < max_attempts:
                    attempts += 1
                    try:
                        button_location = pyautogui.locateCenterOnScreen(importar_btn_full_path, confidence=0.6)
                        if button_location:
                            pyautogui.moveTo(button_location)
                            await worker_sleep(1)
                            pyautogui.click(button_location)
                            console.print("Botão 'Importar' ainda persiste, clicando...")
                    except pyautogui.ImageNotFoundException:
                        console.print("Botão 'Importar' não encontrado, saindo...")
                        break
        except pyautogui.ImageNotFoundException:
                window_rect = main_window.rectangle()
                console.print(f"Area que sera utlizada para o screenshot {window_rect}...\n")

                try:
                    button_location = pyautogui.locateCenterOnScreen(importar_btn_full_path, region=(window_rect.left, window_rect.top, window_rect.width(), window_rect.height()))
                    if button_location:
                        button_location = (button_location.x + window_rect.left, button_location.y + window_rect.top)
                        console.print(f"Botão encontrado nas coordenadas: {button_location}")
                        pyautogui.click(button_location)
                except pyautogui.ImageNotFoundException:
                    console.print("Erro - Botão Importar na tela de Importação de Outras Empresas não foi encontrado após tentar capturar a tela")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Erro - Botão Importar na tela de Importação de Outras Empresas não foi encontrado após tentar capturar a tela",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
        except Exception as e:
            console.print(
                f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de Importar na tela Importação de Outras Empresas,Error: {e}...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de Importar na tela Importação de Outras Empresas,Error: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )


        await worker_sleep(5)
        # VERIFICANDO A EXISTENCIA DE ERRO
        erro_pop_up = await is_window_open("Erro")
        if erro_pop_up["IsOpened"] == True:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Nota não encontrada no EMsys",
                status=RpaHistoricoStatusEnum.Falha,
            )
        

        max_attempts = 10
        i = 0

        while i < max_attempts:
            information_pop_up = await is_window_open("Informações para importação da Nota Fiscal Eletrônica")
            if information_pop_up["IsOpened"] == True:
                break
            else:
                console.print(f"Aguardando a tela Informações para importação da Nota Fiscal Eletrônica...\n")
                await worker_sleep(3)
                i += 1
        
        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Nota não encontrada no EMsys",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        console.print(
            f"Marcando o agrupar por unidade de medida...\n"
        )

        app = Application(backend="uia").connect(title="Informações para importação da Nota Fiscal Eletrônica")
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]
        checkbox = main_window.child_window(
            title="Utilizar unidade de agrupamento dos itens",
            class_name="TCheckBox",
            control_type="CheckBox",
        )
        if not checkbox.get_toggle_state() == 1:
            checkbox.click()
            console.print("Realizado o agrupamento por unidade de medida... \n")
        

        await worker_sleep(2)
        console.print(
            f"Marcando Manter calculo PIS/COFINS...\n"
        )

        try:
            checkbox = main_window.child_window(
                title="Manter cálculo PIS/COFINS",
                class_name="TCheckBox",
                control_type="CheckBox",
            )
        except:
            checkbox = main_window.child_window(
                title=re.compile(".*PIS/COFINS.*"),
                class_name="TCheckBox",
                control_type="CheckBox"
            )
        if not checkbox.get_toggle_state() == 1:
            checkbox.click()
            console.print("Realizado com sucesso... \n")

        
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

        await worker_sleep(70)

        console.print(
            "Verificando a existencia de POP-UP de Itens não localizados ou NCM ...\n"
        )
        itens_by_supplier = await is_window_open_by_class("TFrmAguarde", "TMessageForm")
        if itens_by_supplier["IsOpened"] == True:
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

        panel_TabPagamentoCaixa = panel_TTabSheet.child_window(title="Pagamento Pelo Caixa")

        tipo_cobranca = panel_TabPagamentoCaixa.child_window(
            class_name="TDBIComboBox", found_index=0
        )

        console.print(f"Selecionando a Especie de Caixa... \n")
        tipo_cobranca.click()
        try:
            set_combobox("||List", "27 - TRANFERENCIA DO CD")
        except:
            set_combobox("||List", "27 - TRANFERENCIA DO CD")
        
        await worker_sleep(2)

        console.print(f"Capturando o valor em Valores Restante... \n")
        tab_valores = panel_TabPagamento.child_window(title="Valores")
        valores_restantes = tab_valores.child_window(
            class_name="TDBIEditNumber", found_index=1
        )
        valores_restantes_text = valores_restantes.window_text()
        console.print(f"Valor capturado {valores_restantes_text}, inserindo no campo Valor em Pagamento pelo Caixa... \n")

        valor = panel_TabPagamentoCaixa.child_window(
            class_name="TDBIEditNumber", found_index=0
        )
        valor.set_edit_text(valores_restantes_text)

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
        

        await worker_sleep(7)
        aviso_pop_up = await is_window_open("Aviso")
        if aviso_pop_up["IsOpened"] == True:
            app = Application().connect(title="Aviso")
            main_window = app["Aviso"]
            main_window.set_focus()

            console.print(f"Clicando em Aviso, para andamento do processo...\n")
            btn_no = main_window.child_window(title="OK")
            if btn_no.exists(timeout=5) and btn_no.is_enabled():
                btn_no.set_focus()
                btn_no.click()
                await worker_sleep(2)

            try:
                pyautogui.click(623, 374)
                await worker_sleep(1)
                pyautogui.press('home')
                console.print("Alterando a NOP...\n")

                app = Application().connect(class_name="TFrmNotaFiscalEntrada", timeout=30)
                main_window = app["TFrmNotaFiscalEntrada"]
                main_window.set_focus()

                select_box_nop_select = main_window.child_window(class_name="TDBIComboBox", found_index=0)
                select_box_nop_select.click()
                pyautogui.write("1152")
                await worker_sleep(2)
                pyautogui.hotkey("enter")
                await worker_sleep(2)

                max_try =  10
                i = 0
                first_nop = False
                while i <= max_try:
                    select_box_nop_select = main_window.child_window(class_name="TDBIComboBox", found_index=0)
                    nop_selected = select_box_nop_select.window_text()
                    if '1152 - ENTRADAS P/ TRANSFERENCIA DE MERCADORIAS- 1.152' == nop_selected and first_nop == False:
                        first_nop = True
                    else:
                        if '1152 - ENTRADAS P/ TRANSFERENCIA DE MERCADORIAS- 1.152' == nop_selected:
                            break
                    
                    pyautogui.press('down')
                    await worker_sleep(2)
                    i = i + 1


                if i <= max_try and first_nop:
                    console.print(f"A segunda correspondência '1152 - ENTRADAS P/ TRANSFERENCIA DE MERCADORIAS- 1.152' foi encontrada e selecionada.")
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro não foi encontrada a segunda correspondência dentro do número máximo de tentativas ({max_try})",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
                    
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
                await worker_sleep(10)

                console.print("Verificando a existencia de POP-UP de Itens que Ultrapassam a Variação Máxima de Custo ...\n")
                itens_variacao_maxima = await is_window_open_by_class("TFrmTelaSelecao", "TFrmTelaSelecao")
                if itens_variacao_maxima["IsOpened"] == True:
                    app = Application().connect(class_name="TFrmTelaSelecao")
                    main_window = app["TFrmTelaSelecao"]
                    send_keys("%o")
                    await worker_sleep(7)
                
                aviso_pop_up = await is_window_open("Aviso")
                if aviso_pop_up["IsOpened"] == True:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro na validação de CFOP, foi encontrado mais de uma opção com a mesma informação",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
                
                console.print("Verificando a existencia de Warning informando que a Soma dos pagamentos não bate com o valor da nota. ...\n")
                warning_pop_up_pagamentos = await is_window_open("Warning")
                if warning_pop_up_pagamentos["IsOpened"] == True:
                    return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"A soma dos pagamentos não bate com o valor da nota.",
                    status=RpaHistoricoStatusEnum.Falha,
                )
                
                await worker_sleep(60)
                console.print("\nVerifica se a nota ja foi lançada...")
                nf_chave_acesso = int(nota.get("nfe"))
                status_nf_emsys = await get_status_nf_emsys(nf_chave_acesso)
                if status_nf_emsys.get("status") == "Lançada":
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno="Nota Lançada com sucesso!",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )            
            except Exception as e:
                select_box_nop_select.click()
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao alterar o NOP, erro {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                )

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
