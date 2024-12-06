import getpass
import warnings
import os

import pyautogui
import pytesseract
from pywinauto.application import Application
from PIL import Image, ImageEnhance
from pywinauto.keyboard import send_keys
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
    extract_group_by_itens,
    get_xml,
    import_nfe,
    incluir_registro,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_all_emsys,
    login_emsys,
    read_xml_file,
    select_documento_type,
    set_variable,
    type_text_into_field,
    warnings_after_xml_imported,
    worker_sleep,
    check_nota_importada,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def entrada_de_notas_207(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

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
        console.print(f"Inserindo a informação da CFOP, caso se aplique {cfop} ...\n")
        if cfop == 5655 or str(cfop).startswith("56"):
            combo_box_natureza_operacao = main_window.child_window(
                class_name="TDBIComboBox", found_index=0
            )
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "1652-COMPRA DE MERCADORIAS- 1.652")
            await worker_sleep(3)

        else:
            console.print(
                "Erro mapeado, CFOP diferente de 5655 ou 56, necessario ação manual ou ajuste no robo...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro mapeado, CFOP diferente de 5655 ou 56, necessario ação manual ou ajuste no robo",
                status=RpaHistoricoStatusEnum.Falha,
            )

        # INTERAGINDO COM O CAMPO ALMOXARIFADO
        filialEmpresaOrigem = nota.get("filialEmpresaOrigem")
        console.print(
            f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...\n"
        )
        # task_bar_toast("Teste toast bar", f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...", 'Worker', 10)
        # show_toast("Teste toast", f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...")
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

        await worker_sleep(3)
        # INTERAGINDO COM CHECKBOX Utilizar unidade de agrupamento dos itens
        console.print("Verificando se a nota é do fornecedor SIM Lubrificantes \n")
        fornecedor = nota["nomeFornecedor"]
        console.print(f"Fornecedor: {fornecedor} ...\n")
        if "sim lubrificantes" in fornecedor.lower():
            console.print(
                f"Sim, nota emitida para: {fornecedor}, marcando o agrupar por unidade de medida...\n"
            )
            checkbox = window.child_window(
                title="Utilizar unidade de agrupamento dos itens",
                class_name="TCheckBox",
                control_type="CheckBox",
            )
            if not checkbox.get_toggle_state() == 1:
                checkbox.click()
                console.print("Realizado o agrupamento por unidade de medida... \n")
        else:
            console.print(
                "Não foi necessario realizar o agrupamento por unidade de medida... \n"
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
                if informacao_nf_eletronica["IsOpened"] == False:
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
                retorno=f"Número máximo de tentativas atingido, Não foi possivel finalizar os trabalhos na tela de Informações para importação da Nota Fiscal Eletrônica",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(6)

        try:
            console.print(
                "Verificando a existencia de POP-UP de Itens não localizados ou NCM ...\n"
            )
            itens_by_supplier = await is_window_open_by_class("TFrmAguarde", "TMessageForm")
            if itens_by_supplier["IsOpened"] == True:
                itens_by_supplier_work = await itens_not_found_supplier(nota.get("nfe"))
                if itens_by_supplier_work.get("window") == "NCM":
                    console.log(itens_by_supplier_work.get("retorno"), style="bold green")
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=itens_by_supplier_work.get("retorno"),
                        status=RpaHistoricoStatusEnum.Falha,
                    )
        except Exception as error:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Falha ao verificar a existência de POP-UP de itens não localizados: {error}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(3)
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()
        console.print("Acessando os itens da nota... \n")
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        send_keys("{DOWN " + ("5") + "}")

        # CONFIRMANDO SE A ABA DE ITENS FOI ACESSADA COM SUCESSO
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TPage.wait("visible")
        panel_TTabSheet = panel_TPage.child_window(class_name="TTabSheet")
        title_n_serie = panel_TPage.child_window(title="N° Série")

        console.print("Verificando se os itens foram abertos com sucesso... \n")
        if not title_n_serie:
            console.print(f"Não foi possivel acessar a aba de 'Itens da nota...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possivel acessar a aba de 'Itens da nota'",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(2)

        console.print("Acessando os itens indivualmente... \n")
        send_keys("{TAB 2}", pause=0.1)
        await worker_sleep(2)

        username = getpass.getuser()
        path_to_xml = f"C:\\Users\\{username}\\Downloads\\{nota["nfe"]}.xml"
        get_xml_itens = await read_xml_file(path_to_xml)
        itens = await extract_group_by_itens(get_xml_itens)

        console.print(
            f"Trabalhando com os itens, alterando a unidade com base na descrição do item \n"
        )
        try:
            for item in itens:
                n_item = item["n_item"]
                formato = item["formato"]
                descricao = item["descricao"]
                if formato is None:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Não foi possivel acessar a extrair a quantidade/Unidade de medidade do XML, item: {item}",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
                pos_x = formato.find("X")
                cod_split = str(formato[0:pos_x])

                cod_split = cod_split.replace("(","")

                console.print(f"Item a ser ajustado: {cod_split} \n")

                send_keys("^({HOME})")
                await worker_sleep(1)

                if int(n_item) > 1:
                    send_keys("{DOWN " + str(n_item) + "}")

                if cod_split != "1":
                    console.print(f"Item a ser ajustado: {descricao} \n")
                    await worker_sleep(2)
                    send_keys("+{F10}")
                    await worker_sleep(1)
                    send_keys("{DOWN 2}")
                    await worker_sleep(1)
                    send_keys("{ENTER}")

                    await worker_sleep(2)
                    app = Application().connect(title="Alteração de Item")
                    main_window = app["Alteração de Item"]

                    main_window.set_focus()

                    edit = main_window.child_window(
                        class_name="TDBIEditCode", found_index=0
                    )

                    # ITERAGINDO COM O IPI
                    tpage_ipi = main_window.child_window(
                        class_name="TPanel", found_index=0
                    )
                    ipi = tpage_ipi.child_window(
                        class_name="TDBIComboBox", found_index=2
                    )

                    ipi_value = ipi.window_text()

                    console.print(
                        f"Trabalhando com os itens, valor do IP {ipi_value}... \n"
                    )
                    if len(ipi_value) == 0:
                        console.print(
                            f"Trabalhando com os itens, valor do IP em branco, selecionando IPI 0% ... \n"
                        )
                        ipi.click_input()
                        send_keys("^({HOME})")
                        send_keys("{DOWN 6}")
                        send_keys("{ENTER}")

                        await worker_sleep(4)
                        tpage_ipi = main_window.child_window(
                            class_name="TPanel", found_index=0
                        )
                        ipi = tpage_ipi.child_window(
                            class_name="TDBIComboBox", found_index=2
                        )

                        ipi_value = ipi.window_text()

                        if "IPI 0%" in ipi_value:
                            console.print(
                                f"Trabalhando com os itens, sucesso ao selecionar o valor do IPI ... \n"
                            )
                        else:
                            return RpaRetornoProcessoDTO(
                                sucesso=False,
                                retorno=f"Erro ao selecionar o IPI de unidade nos itens, IPI: {ipi_value}",
                                status=RpaHistoricoStatusEnum.Falha,
                            )

                        await worker_sleep(4)

                    try:
                        get_unidade = main_window.child_window(
                            class_name="TDBIComboBox", found_index=1
                        )
                        console.print(
                            f"VALOR ATUALMENTE SELECIONADO {get_unidade} ...\n"
                        )
                        if str(cod_split) in get_unidade.window_text():
                            console.print(
                                f"UNIDADE SELECIONADA CORRETAMENTE {get_unidade} ...\n"
                            )
                        else:
                            console.print(
                                f"SELECIONANDO UN-{cod_split} - F PARA UNIDADE ...\n"
                            )
                            get_unidade = main_window.child_window(
                                class_name="TDBIComboBox", found_index=1
                            )
                            combo_box_group = "UN-" + cod_split + " - F"
                            if str(cod_split) in get_unidade.window_text():
                                get_unidade.click_input()
                                set_combobox("||List", combo_box_group)
                                await worker_sleep(4)

                            # VERIFICANDO SE FOI SELECIONADO CORRETAMENTE
                            console.print(
                                f"VERIFICANDO SE FOI SELECIONADO UN-{cod_split} - F PARA UNIDADE ...\n"
                            )
                            get_unidade = main_window.child_window(
                                class_name="TDBIComboBox", found_index=1
                            )
                            if str(cod_split) in get_unidade.window_text():
                                combo_box_group = "UN-" + cod_split + " - F"
                                console.print(
                                    f"NÃO FOI SELECIONADO UN-{cod_split} - F PARA UNIDADE, TENTANDO SELECIONAR COMO CAIXA...\n"
                                )
                                num_adjusted = cod_split
                                if int(cod_split) < 9:
                                    num_adjusted = "0" + str(cod_split)
                                combo_box_group = "CAIXA C/" + num_adjusted
                                get_unidade.click_input()
                                set_combobox("||List", combo_box_group)
                                await worker_sleep(4)

                            get_unidade = main_window.child_window(
                                class_name="TDBIComboBox", found_index=1
                            )
                            if str(cod_split) in get_unidade.window_text():
                                return RpaRetornoProcessoDTO(
                                    sucesso=False,
                                    retorno=f"Erro ao selecionar o tipo de unidade nos itens, item: {n_item} {descricao}, não possui UN-{cod_split} - F OU CAIXA C/{cod_split} ",
                                    status=RpaHistoricoStatusEnum.Falha,
                                )

                            else:
                                console.print(
                                    f"SELECIONADO COMO CAIXA PARA UNIDADE...\n"
                                )

                    except Exception as e:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Erro ao selecionar o tipo de unidade nos itens: {e}",
                            status=RpaHistoricoStatusEnum.Falha,
                        )
                    
                    console.print(
                        f"Iten selecionado com sucesso, clicando em alterar ...\n"
                    )
                    await worker_sleep(2)

                    try:
                        btn_alterar = main_window.child_window(title="&Alterar")
                        btn_alterar.click()
                    except:
                        btn_alterar = main_window.child_window(title="Alterar")
                        btn_alterar.click()
                    await worker_sleep(3)

        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao trabalhar nas alterações dos itens: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(2)
        # Inclui registro
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

        await worker_sleep(2)

        # Verifica se a info 'Nota fiscal incluida' está na tela
        await worker_sleep(6)
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