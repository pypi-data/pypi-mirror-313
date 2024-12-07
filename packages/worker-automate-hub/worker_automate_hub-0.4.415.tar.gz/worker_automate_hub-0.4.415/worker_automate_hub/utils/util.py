import asyncio
import datetime
import getpass
import io
import math
import os
import re
import subprocess
import time
import warnings
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, TypedDict

import aiohttp
import cv2
import psutil
import pyautogui
import pyperclip
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image, ImageEnhance
from prompt_toolkit.shortcuts import checkboxlist_dialog
from pytesseract import pytesseract
from pywinauto.application import Application, findwindows
from pywinauto_recorder.player import set_combobox
from pywinauto.keyboard import send_keys
from rich.console import Console

from worker_automate_hub.config.settings import load_worker_config
from worker_automate_hub.decorators.repeat import repeat
from worker_automate_hub.models.dao.rpa_configuracao import RpaConfiguracao
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.updater import get_installed_version

console = Console()

ASSETS_PATH = "assets"

global_variables = {}


def set_variable(key, value):
    global_variables[key] = value


def get_variable(key):
    return global_variables.get(key, None)


async def worker_sleep(multiplier: int):
    """
    Função que espera o tempo configurado multiplicado por um fator.

    O tempo de espera é definido pela variável global "timeout_multiplicador".
    Caso essa variável não esteja definida, uma exceção ValueError será levantada.
    Se o valor da variável for menor ou igual a zero, uma exceção ValueError será
    levantada.

    :param int multiplier: Fator de multiplicação do tempo de espera.
    :raises ValueError: Se a variável "timeout_multiplicador" não estiver definida
        ou for menor ou igual a zero.
    :raises TypeError: Se o valor da variável "timeout_multiplicador" não for um
        número (int ou float).
    """
    timeout_multiplicador = get_variable("timeout_multiplicador")
    if timeout_multiplicador is None:
        timeout_multiplicador = 1
        console.log("O timeout multiplicador não foi definido")
    
    # Adicionando delay de 1/3 em todas as chamadas do método
    delay = (timeout_multiplicador * multiplier) * 1.3

    console.log(
        f"Aguardando {(delay)} segundos...",
        style="bold yellow",
    )
    await asyncio.sleep(delay)


async def get_system_info():
    worker_config = load_worker_config()
    max_cpu = psutil.cpu_percent(interval=10.0)
    cpu_percent = psutil.cpu_percent(interval=1.0)
    memory_info = psutil.virtual_memory()

    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "maxCpu": f"{max_cpu}",
        "maxMem": f"{memory_info.total / (1024 ** 3):.2f}",
        "usoCpu": f"{cpu_percent}",
        "usoMem": f"{memory_info.used / (1024 ** 3):.2f}",
        "situacao": "{'status': 'em desenvolvimento'}",
    }


async def get_new_task_info():
    worker_config = load_worker_config()
    atual_version = get_installed_version("worker-automate-hub")
    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "versao": atual_version,
    }


def multiselect_prompt(options, title="Select options"):
    result = checkboxlist_dialog(
        values=[(option, option) for option in options],
        title=title,
        text="Use space to select multiple options.\nPress Enter to confirm your selection.",
    ).run()

    if result is None:
        console.print("[red]No options selected.[/red]")


async def kill_process(process_name: str):
    """
    Mata um processo com o nome especificado.

    :param process_name: O nome do processo a ser finalizado.
    :type process_name: str

    :return: None
    :rtype: None

    :raises Exception: Se houver um erro ao tentar finalizar o processo.
    """
    try:
        # Obtenha o nome do usuário atual
        current_user = os.getlogin()

        # Liste todos os processos do sistema
        result = await asyncio.create_subprocess_shell(
            f'tasklist /FI "USERNAME eq {current_user}" /FO CSV /NH',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            err_msg = f"Erro ao listar processos: {stderr.decode().strip()}"
            logger.error(err_msg)
            console.print(err_msg, style="bold red")
            return

        if stdout is None:
            err_msg = "Não foi possível obter a lista de processos."
            logger.error(err_msg)
            console.print(err_msg, style="bold red")
            return

        lines = stdout.decode().strip().split("\n")
        for line in lines:
            # Verifique se o processo atual corresponde ao nome do processo
            if process_name in line:
                try:
                    # O PID(Process ID)   a segunda coluna na saída do tasklist
                    pid = int(line.split(",")[1].strip('"'))
                    await asyncio.create_subprocess_exec(
                        "taskkill", "/PID", str(pid), "/F"
                    )
                    log_msg = f"Processo {process_name} (PID {pid}) finalizado."
                    logger.info(log_msg)
                    console.print(
                        f"\n{log_msg}\n",
                        style="bold green",
                    )
                except Exception as ex:
                    err_msg = f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}"
                    logger.error(err_msg)
                    console.print(
                        err_msg,
                        style="bold red",
                    )
        else:
            log_msg = f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}."
            logger.info(
                log_msg,
                None,
            )
            console.print(
                log_msg,
                style="bold yellow",
            )

    except Exception as e:
        err_msg = f"Erro ao tentar matar o processo: {e}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")


async def find_element_center(image_path, region_to_look, timeout):
    try:
        counter = 0
        confidence_value = 1.00
        grayscale_flag = False

        while counter <= timeout:
            try:
                element_center = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region_to_look,
                    confidence=confidence_value,
                    grayscale=grayscale_flag,
                )
            except Exception as ex:
                element_center = None
                console.print(
                    f"[{counter+1}] - Elemento não encontrado na posição: {region_to_look}"
                )

            if element_center:
                console.print(
                    f"[{counter+1}] - Elemento encontrado na posição: {region_to_look}\n",
                    style="green",
                )
                return element_center
            else:
                counter += 1

                if confidence_value > 0.81:
                    confidence_value -= 0.01

                if counter >= math.ceil(timeout / 2):
                    grayscale_flag = True

                await worker_sleep(1)

        return None
    except Exception as ex:
        console.print(
            f"{counter} - Buscando elemento na tela: {region_to_look}",
            style="bold yellow",
        )
        return None


def type_text_into_field(text, field, empty_before, chars_to_empty):
    try:
        if empty_before:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)

        field.type_keys(text, with_spaces=True)

        if str(field.texts()[0]) == text:
            return
        else:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)
            field.type_keys(text, with_spaces=True)

    except Exception as ex:
        logger.error("Erro em type_text_into_field: " + str(ex), None)
        console.print(f"Erro em type_text_into_field: {str(ex)}", style="bold red")


async def wait_element_ready_win(element, trys):
    max_trys = 0

    while max_trys < trys:
        try:
            if element.wait("exists", timeout=2):
                await worker_sleep(1)
                if element.wait("exists", timeout=2):
                    await worker_sleep(1)
                    if element.wait("enabled", timeout=2):
                        element.set_focus()
                        await worker_sleep(1)
                        if element.wait("enabled", timeout=1):
                            return True

        except Exception as ex:
            logger.error("wait_element_ready_win -> " + str(ex), None)
            console.print(
                f"Erro em wait_element_ready_win: {str(ex)}", style="bold red"
            )

        max_trys = max_trys + 1

    return False


async def login_emsys_fiscal(
    config: dict, app, task: RpaProcessoEntradaDTO
) -> RpaRetornoProcessoDTO:
    """
    Função que realiza o login no EMSys Fiscal.

    Args:
        config (dict): Dicionario com as configuracoes do login no EMSys Fiscal.
        app: Aplicacao do EMSys Fiscal.
        task (RpaProcessoEntradaDTO): Dicionario com as informacoes do processo.

    Returns:
        RpaRetornoProcessoDTO: Dicionario com o resultado do login.
    """

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    filial_cod = task.configEntrada.get("empresa")
    console.print(f'Empresa a ser processada: {filial_cod}')

    try:
        console.print("\nEMSys Fiscal inciado com sucesso...", style="bold green")
        app = Application().connect(class_name="TFrmLoginModulo")
        main_window = app["Login"]

        user = config.get("user")
        password = config.get("pass")

        if not user or not password:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro: Não foi possivel obter as credencias para login",
                status=RpaHistoricoStatusEnum.Falha,
            )

        main_window.set_focus()
        await worker_sleep(2)
        edit_user = main_window.child_window(class_name="TcxCustomInnerTextEdit", found_index=1)
        edit_user.click()
        await worker_sleep(2)
        pyautogui.write(user)

        await worker_sleep(2)
        edit_password = main_window.child_window(class_name="TcxCustomInnerTextEdit", found_index=0)
        edit_password.click()
        await worker_sleep(2)
        pyautogui.write(password)


        await worker_sleep(2)
        edit_password.type_keys("{ENTER}")
        await worker_sleep(6)


        max_attempts = 15
        i = 0
        while i < max_attempts:
            selecionar_empresa = await is_window_open_by_class("TFrmSelecaoEmpresa", "TFrmSelecaoEmpresa")
            if selecionar_empresa["IsOpened"] == True:
                console.print("janela para gerar seleção da empresa foi aberta com sucesso...\n")
                break
            else:
                warning_pop_up = await is_window_open("Warning")
                information_pop = await is_window_open("Information")
                if warning_pop_up["IsOpened"] == True or information_pop == True:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Pop-up Warning/Information ao tentar realizar login",
                        status=RpaHistoricoStatusEnum.Falha,
                    )                    
                else:
                    edit_password.type_keys("{ENTER}")
                    await worker_sleep(1)
                    i = i+1
        
        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela para seleção da empresa, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
            )

        # Seleciona a filial do emsys
        console.print(f"Seleciona a filial {filial_cod} no emsys...")
        app = Application().connect(class_name="TFrmSelecaoEmpresa")
        main_window = app["TFrmSelecaoEmpresa"]
        main_window.set_focus()

        edit_filial = main_window.child_window(class_name="TEdit", found_index=0)
        edit_filial.click()
        await worker_sleep(1)
        pyautogui.write(filial_cod)
        await worker_sleep(2)
        edit_filial.type_keys("{ENTER}")

        
        await worker_sleep(5)
        console.print(
            f"Verificando a presença de Warning..."
        )
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro: Não foi possível acessar a filial {filial_cod}, esta com o CNPJ bloqueado, por favor verificar",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        information_pop_up = await is_window_open_by_class("TMessageForm","TMessageForm")
        if information_pop_up["IsOpened"] == True:
            app_information = Application().connect(
            class_name="TMessageForm"
            )
            main_window_information = app_information["TMessageForm"]
            main_window.set_focus()
            await worker_sleep(2)
            btn_no = main_window_information["&No"]
            if btn_no.exists():
                try:
                    btn_no.click()
                    await worker_sleep(3)
                    console.print("O botão No após selecionar a filiam na seleção de empresa foi clicado com sucesso.", style="green")
                except:
                    console.print("Falha ao clicar no botão No após selecionar a filiam na seleção de empresa", style="red")
            else:
              return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro: Botão No, nao existe no pop-up information após a seleção da filial da empresa",
                status=RpaHistoricoStatusEnum.Falha,
            )  
            
        max_attempts = 10
        i = 0
        while i < max_attempts:
            console.print("Aguardando o EMSys Fiscal...\n")
            emsys_opened= await is_window_open_by_class("TFrmPrincipalFiscal", "TFrmPrincipalFiscal")
            if emsys_opened["IsOpened"] == True:
                console.print("Login realizado com sucesso.", style="bold green")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Logou com sucesso no emsys!",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            else:
                i = i+1
                await worker_sleep(1)
        
        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir o EMSys Fiscal, tela de login não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
            )


    except Exception as e:
        log_msg = f"Erro ao realizar login no EMSys Fiscal, erro: {e}..."
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha
        )


async def login_emsys(
    config: dict, app, task: RpaProcessoEntradaDTO
) -> RpaRetornoProcessoDTO:
    """
    Função que realiza o login no EMSys.

    Args:
        config (dict): Dicionario com as configuracoes do login no EMSys.
        app: Aplicacao do EMSys.
        task (RpaProcessoEntradaDTO): Dicionario com as informacoes do processo.

    Returns:
        RpaRetornoProcessoDTO: Dicionario com o resultado do login.
    """

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    await worker_sleep(15)
    # await asyncio.sleep(10)
    # Testa se existe alguma mensagem no Emsys
    console.print("Testando se existe alguma mensagem no Emsys...")
    window_message_login_emsys = await find_element_center(
        "assets/emsys/window_message_login_emsys.png", (560, 487, 1121, 746), 15
    )

    # Clica no "Não mostrar novamente" se existir
    console.print("Clicando no 'Não mostrar novamente' se existir...")
    if window_message_login_emsys:
        pyautogui.click(window_message_login_emsys.x, window_message_login_emsys.y)
        pyautogui.click(
            window_message_login_emsys.x + 383, window_message_login_emsys.y + 29
        )
        console.print("Mensagem de login encontrada e fechada.", style="bold green")

    # Ve se o Emsys esta aberto no login
    console.print("Verificando se o Emsys esta aberto no login...")
    image_emsys_login = await find_element_center(
        "assets/emsys/logo_emsys_login.png", (800, 200, 1400, 700), 60
    )

    # if image_emsys_login == None:
    #     image_emsys_login = await find_element_center(
    #     "assets/emsys/logo_emsys_linx_login.png", (800, 200, 1400, 700), 60
    # )

    if image_emsys_login:
        console.print("Aguardando a janela de login ficar pronta...")
        if await wait_element_ready_win(app["Login"]["Edit2"], 80):
            console.print("Procurando o icone disconect_database...")
            disconect_database = await find_element_center(
                "assets/emsys/disconect_database.png", (1123, 452, 1400, 578), 60
            )

            if disconect_database:
                # Realiza login no Emsys
                console.print("Realizando login no Emsys...")
                type_text_into_field(
                    config.get("user"), app["Login"]["Edit2"], True, "50"
                )
                pyautogui.press("tab")
                type_text_into_field(
                    config.get("pass"),
                    app["Login"]["Edit1"],
                    True,
                    "50",
                )
                pyautogui.press("enter")

                # Seleciona a filial do emsys
                console.print("Seleciona a filial do emsys...")
                selecao_filial = await find_element_center(
                    "assets/emsys/selecao_filial.png", (480, 590, 820, 740), 15
                )

                console.print(f"Selecao filial via imagem: {selecao_filial}")
                if selecao_filial == None:
                    screenshot_path = take_screenshot()
                    selecao_filial = find_target_position(
                        screenshot_path, "Grupo", 0, -50, attempts=15
                    )
                    console.print(
                        f"Selecao filial localização de texto: {selecao_filial}"
                    )
                    if selecao_filial == None:
                        selecao_filial = (700, 639)
                        console.print(f"Selecao filial posição fixa: {selecao_filial}")

                    pyautogui.click(selecao_filial)
                    console.print(
                        f"Escrevendo [{task.configEntrada.get("filialEmpresaOrigem", "N/A")}] no campo filial..."
                    )

                    pyautogui.write(
                        task.configEntrada.get("filialEmpresaOrigem", "N/A")
                    )

                else:
                    console.print(
                        f"Escrevendo [{task.configEntrada.get("filialEmpresaOrigem", "N/A")}] no campo filial..."
                    )
                    type_text_into_field(
                        task.configEntrada.get("filialEmpresaOrigem", "N/A"),
                        app["Seleção de Empresas"]["Edit"],
                        True,
                        "50",
                    )
                pyautogui.press("enter")

                button_logout = await find_element_center(
                    "assets/emsys/button_logout.png", (0, 0, 130, 150), 60
                )

                if button_logout:
                    console.print("Login realizado com sucesso.", style="bold green")
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno="Logou com sucesso no emsys!",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )

        else:
            log_msg = "Elemento de login não está pronto."
            logger.info(log_msg)
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Falha ao logar no EMSys!",
                status=RpaHistoricoStatusEnum.Falha,
            )

    else:
        screen_width, screen_height = pyautogui.size()
        log_msg = f"A tela de login não foi encontrada. Resolução atual: {screen_width}x{screen_height}."
        logger.info(log_msg)
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha
        )


async def api_simplifica(
    urlSimplifica: str,
    status: str,
    observacao: str,
    uuidsimplifica: str,
    numero_nota: str,
    valor_nota: str,
) -> None:
    """
    Envia notificacao para o simplifica com status e observacao.

    Args:
    urlSimplifica (str): URL do endpoint do simplifica.
    status (str): Status da notificacao.
    observacao (str): Observacao da notificacao.
    uuidsimplifica (str): UUID da notificacao.
    numero_nota (str): Numero da nota.
    valor_nota (str): Valor da nota.
    """
    if not urlSimplifica:
        raise ValueError("URL do endpoint do simplifica esta vazia.")

    if not status:
        raise ValueError("Status da notificacao esta vazio.")

    if not observacao:
        raise ValueError("Observacao da notificacao esta vazia.")

    if not uuidsimplifica:
        raise ValueError("UUID da notificacao esta vazio.")

    data = {
        "uuid_simplifica": uuidsimplifica,
        "status": status,
        "numero_nota": numero_nota,
        "observacao": observacao,
        "valor_nota": valor_nota,
    }

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.post(f"{urlSimplifica}", data=data) as response:
                if response.status != 200:
                    raise Exception(f"Erro ao enviar notificacao: {response.text()}")

                data = await response.text()
                log_msg = f"\nSucesso ao enviar {data}\n para o simplifica"
                console.print(
                    log_msg,
                    style="bold green",
                )
                logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao comunicar com endpoint do Simplifica: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.info(err_msg)


def add_start_on_boot_to_registry():
    import winreg as reg

    try:
        # Caminho para a chave Run
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Nome da chave
        key_name = "worker-startup"

        # Caminho para o executável no diretório atual
        directory_value = os.path.join(os.getcwd(), "worker-startup.bat")

        # Acessar a chave de registro
        registry_key = reg.OpenKey(
            reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_SET_VALUE
        )

        # Adicionar ou modificar o valor
        reg.SetValueEx(registry_key, key_name, 0, reg.REG_SZ, directory_value)

        # Fechar a chave de registro
        reg.CloseKey(registry_key)

        log_msg = f"Chave {key_name} adicionada ao registro com sucesso com o valor '{directory_value}'!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao adicionar ao registro: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def create_worker_bat():
    try:
        # Caminho do diretório atual
        current_dir = os.getcwd()
        nome_arquivo = "worker-startup.bat"

        # Conteúdo do arquivo
        # cd %USERPROFILE%
        bat_content = f"""@echo off
cd {current_dir}   
pipx install worker-automate-hub --force     
start /min "" "worker" "run" "--assets"
"""

        # Caminho completo para o arquivo
        bat_file_path = os.path.join(current_dir, nome_arquivo)

        # Escrevendo o conteúdo no arquivo
        with open(bat_file_path, "w") as file:
            file.write(bat_content.strip())

        log_msg = f"Arquivo {nome_arquivo} criado com sucesso em {bat_file_path}!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao criar o arquivo {nome_arquivo}: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def take_screenshot() -> Path:
    """
    Tira um screenshot da tela atual e salva em um arquivo com o nome
    especificado e a data/hora atual.

    :return: caminho do arquivo de screenshot gerado
    :rtype: str
    """
    if not Path.cwd().exists():
        raise FileNotFoundError("O caminho atual nao existe.")

    screenshot_path = Path.cwd() / "temp" / "screenshot.png"

    if not screenshot_path.parent.exists():
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
    except Exception as e:
        raise Exception("Erro ao tirar screenshot") from e

    if not screenshot_path.exists():
        raise FileNotFoundError("O arquivo de screenshot nao foi gerado")

    return screenshot_path


def preprocess_image(image_path):
    # Carregar a imagem
    image = cv2.imread(str(image_path))

    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold binário
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Remover ruído com medianBlur
    denoised_image = cv2.medianBlur(binary_image, 3)

    # Aumentar o contraste
    contrast_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=0)

    return contrast_image


def take_target_position(
    screenshot_path: Path, target_text: str, vertical=0, horizontal=0
) -> tuple | None:

    selected_image = Image.open(screenshot_path).convert("L")

    # Configurações do pytesseract
    # custom_config = r'--oem 3 --psm 6'

    # Extrair dados do texto usando pytesseract
    text_data = pytesseract.image_to_data(
        selected_image,
        output_type=pytesseract.Output.DICT,
        lang="por",  # , config=custom_config
    )

    # Identificar a posição do texto desejado
    field_center = None
    for i, text in enumerate(text_data["text"]):
        if len(text) > 0:
            if target_text.lower() in str(text).lower():
                x = text_data["left"][i]
                y = text_data["top"][i]
                w = text_data["width"][i]
                h = text_data["height"][i]
                # Centralizando nas coordenadas do campo
                field_center = (x + w // 2, y + h // 2)
                break

    # Aplicar as modificações de posição
    if field_center:
        field_center = (field_center[0] + horizontal, field_center[1] + vertical)

    return field_center


def find_target_position(
    screenshot_path: Path,
    target_text: str,
    vertical_pos: int = 0,
    horizontal_pos: int = 0,
    attempts: int = 5,
) -> tuple | None:
    """
    Encontra a posição de um campo na tela com base em uma imagem de screenshot.

    Args:
        screenshot_path (Path): Caminho para a imagem de screenshot.
        target_text (str): Texto do campo a ser encontrado.
        vertical_pos (int, optional): Posição vertical do campo. Defaults to 0.
        horizontal_pos (int, optional): Posição horizontal do campo. Defaults to 0.
        attempts (int, optional): Número de tentativas. Defaults to 5.

    Returns:
        tuple | None: Posição do campo encontrada ou None.
    """
    if screenshot_path is None:
        raise ValueError("screenshot_path não pode ser nulo")

    if not screenshot_path.exists():
        raise FileNotFoundError(f"O arquivo {screenshot_path} não existe")

    if target_text is None or len(target_text.strip()) == 0:
        raise ValueError("target_text não pode ser nulo ou vazio")

    attempt = 0
    target_pos = None

    while attempt < attempts:
        target_pos = take_target_position(
            screenshot_path,
            target_text,
            vertical=vertical_pos,
            horizontal=horizontal_pos,
        )
        console.print(f"Tentativa {attempt + 1} - Posição: {target_pos}")
        if target_pos is not None:
            log_msg = (
                f"Posição do campo [{target_text}] encontrada na tentativa [{attempt + 1}], "
                f"com valor de: {target_pos}"
            )
            console.print(log_msg, style="green")
            logger.info(log_msg)
            return target_pos

        attempt += 1

    # Caso não tenha encontrado após todas as tentativas
    log_msg = f"Não foi possível encontrar o campo [{target_text}] em [{attempts}] tentativas!"
    console.print(log_msg, style="red")

    return None


def select_model_capa() -> RpaRetornoProcessoDTO:
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Documento", 0, 140, 5)
    if field == None:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno="Não foi possivel encontrar o campo 'Documento'",
            status=RpaHistoricoStatusEnum.Falha,
        )
    pyautogui.click(field)
    pyautogui.write("Nfe")
    pyautogui.hotkey("enter")
    # Procura o tipo de documento "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077"
    while True:
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "Documento", 0, 140, 5)
        if field is None:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel encontrar o campo 'Documento'",
                status=RpaHistoricoStatusEnum.Falha,
            )

        pyautogui.click(field)
        worker_sleep(1)
        pyautogui.write("Nfe")
        pyautogui.hotkey("enter")
        # Procura o tipo de documento "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077"
        while True:
            screenshot_path = take_screenshot()
            field_doc = find_target_position(screenshot_path, "77", 0, 140, 5)
            if field_doc is not None:
                break
            else:
                pyautogui.click(field)
                pyautogui.hotkey("enter")
                pyautogui.hotkey("down")
                pyautogui.hotkey("enter")
                pyautogui.hotkey("tab")
                worker_sleep(2)

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Modelo Selecionado",
            status=RpaHistoricoStatusEnum.Sucesso,
        )


async def download_xml(
    google_drive_folder_id: str,
    get_gcp_token: RpaConfiguracao,
    get_gcp_credentials: RpaConfiguracao,
    chave_nota: str,
) -> RpaRetornoProcessoDTO:
    """
    Baixa um arquivo xml do Google Drive com base em um ID de pasta e um nome de arquivo.

    Args:
        google_drive_folder_id (str): ID da pasta do Google Drive.
        get_gcp_token (RpaConfiguracao): Configurações para obter o token do GCP.
        get_gcp_credentials (RpaConfiguracao): Configurações para obter as credenciais do GCP.
        chave_nota (str): Chave da nota para buscar o arquivo xml.

    Returns:
        RpaRetornoProcessoDTO: Retorna um objeto RpaRetornoProcessoDTO com o resultado da execução do processo.
    """
    try:
        console.print("Verificando a existência do arquivo no Google Drive...\n")
        chave_nota = f"{chave_nota}.xml"
        gcp_credencial = GetCredsGworkspace(
            token_dict=get_gcp_token.conConfiguracao,
            credentials_dict=get_gcp_credentials.conConfiguracao,
        )
        creds = gcp_credencial.get_creds_gworkspace()

        if not creds:
            console.print(f"Erro ao obter autenticação para o GCP...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao obter autenticação para o GCP",
                status=RpaHistoricoStatusEnum.Falha,
            )

        # Inicializando o serviço do Google Drive
        drive_service = build("drive", "v3", credentials=creds)

        # Query para procurar o arquivo com o nome da chave da nota
        query = (
            f"'{google_drive_folder_id}' in parents and name contains '{chave_nota}'"
        )
        results = (
            drive_service.files()
            .list(
                q=query,
                pageSize=10,  # Reduzindo o número de resultados
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                fields="files(id, name)",
            )
            .execute()
        )

        # Verificando se o arquivo foi encontrado
        items = results.get("files", [])

        if not items:
            console.print(f"Nenhum arquivo com o nome {chave_nota} foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nenhum arquivo com o nome {chave_nota} foi encontrado no Google Drive",
                status=RpaHistoricoStatusEnum.Falha,
            )

        # Pegando o primeiro arquivo encontrado
        file_id = items[0]["id"]
        file_name = items[0]["name"]
        console.print(f"Arquivo {file_name} encontrado. Iniciando o download...\n")

        # Definindo o caminho local para salvar o arquivo
        file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

        # Iniciando o download
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            console.print(f"Download {int(status.progress() * 100)}% concluído.")

        console.print(
            f"Arquivo {file_name} baixado com sucesso e salvo em {file_path}.\n"
        )
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Arquivo {file_name} baixado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        console.print(f"Erro ao baixar o arquivo do Google Drive, erro: {e}...\n")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao baixar o arquivo do Google Drive, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def get_xml_outras_empresas() -> RpaRetornoProcessoDTO:
    """
    Função para recuperar o XML da NF-e.

    Returns:
    - None
    """

    console.print("Verificando a existencia da tela de importação do XML... \n")
    app = Application().connect(title="Selecione a forma de obter o XML da NF-e")
    main_window = app["Selecione a forma de obter o XML da NF-e"]

    # Verificando se a janela principal existe
    if main_window.exists():
        console.print("Janela principal encontrada com sucesso... \n")
    else:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Janela principal de importação do XML não foi encontrada.",
            status=RpaHistoricoStatusEnum.Falha,
        )

    console.print("Selecionando Notas de outras empresas... \n")
    arquivo_xml_button = main_window.child_window(title="Notas de Outras Empresas")
    if arquivo_xml_button.exists() and arquivo_xml_button.is_enabled():
        arquivo_xml_button.click()
        console.print("Notas de outras empresas XML selecionado com sucesso... \n")
    else:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Botão Notas de outras empresas não foi encontrado.",
            status=RpaHistoricoStatusEnum.Falha,
        )

    await worker_sleep(3)

    console.print("Verificando se o botão OK existe ... \n")
    ok_button = main_window.child_window(title="OK", class_name="TBitBtn")
    if ok_button.exists() and ok_button.is_enabled():
        max_attempts = 3
        i = 0
        for i in range(max_attempts):
            console.print("Clicando em OK... \n")
            try:
                ok_button.click()
                console.print("Botão OK clicado com sucesso... \n")
            except:
                console.print("Não foi possivel clicar no Botão OK... \n")
                continue

            await worker_sleep(3)

            console.print("Verificando a existência da tela para importar o XML...\n")
            try:
                app = Application().connect(class_name="TFrmImportarNotaOutraEmpresa")
                main_window = app["TFrmImportarNotaOutraEmpresa"]
                console.print("A tela de Importar Nota de Outra Empresa foi encontrada!")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"A tela de Importar Nota de Outra Empresa foi encontrada!",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            except Exception as e:
                console.print(
                    f"Tela de importação não encontrada. Tentativa {i + 1}/{max_attempts}."
                )

            i += 1

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Número máximo de tentativas atingido. A tela para importar o Nota de Outra Empresa não foi encontrada.",
            status=RpaHistoricoStatusEnum.Falha,
        )
    else:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Botão OK não foi encontrado para acessar Notas de outras empresas.",
        )



async def get_xml(xml_file: str) -> None:
    """
    Função para recuperar o XML da NF-e.

    Args:
    - xml_file (str): Nome do arquivo do XML da NF-e sem a extensão .xml

    Returns:
    - None
    """

    console.print("Verificando a existencia da tela de importação do XML... \n")
    app = Application().connect(title="Selecione a forma de obter o XML da NF-e")
    main_window = app["Selecione a forma de obter o XML da NF-e"]

    # Verificando se a janela principal existe
    if main_window.exists():
        console.print("Janela principal encontrada com sucesso... \n")
    else:
        raise Exception("Janela principal de importação do XML não foi encontrada.")

    console.print("Selecionando Arquivo XML para seguir com a importação... \n")
    arquivo_xml_button = main_window.child_window(title="Arquivo XML")
    if arquivo_xml_button.exists() and arquivo_xml_button.is_enabled():
        arquivo_xml_button.click()
        console.print("Arquivo XML selecionado com sucesso... \n")
    else:
        raise Exception("Botão Arquivo XML não foi encontrado.")

    await worker_sleep(3)

    console.print("Verificando se o botão OK existe ... \n")
    ok_button = main_window.child_window(title="OK", class_name="TBitBtn")
    if ok_button.exists() and ok_button.is_enabled():
        max_attempts = 3
        i = 0
        while i < max_attempts:
            console.print("Clicando em OK... \n")
            try:
                ok_button.click()
                console.print("Botão OK clicado com sucesso... \n")
            except:
                console.print("Não foi possivel clicar no Botão OK... \n")

            await worker_sleep(3)

            console.print("Verificando a existência da tela para importar o XML...\n")
            try:
                app = Application().connect(title="Abrir")
                main_window = app["Abrir"]
                console.print("A tela de importação foi encontrada!")
                break
            except Exception as e:
                console.print(
                    f"Tela de importação não encontrada. Tentativa {i + 1}/{max_attempts}."
                )

            i += 1

        if i == max_attempts:
            raise Exception(
                "Número máximo de tentativas atingido. A tela para importar o XML não foi encontrada."
            )

    else:
        raise Exception("Botão OK não foi encontrado.")

    await worker_sleep(10)

    console.print("Conectando na tela de importação do XML...\n")
    app = Application().connect(title="Abrir")
    main_window = app["Abrir"]

    # Verificando se a janela principal existe
    if main_window.exists():
        console.print("Janela para importar o xml encontrada com sucesso... \n")
    else:
        raise Exception("Janela para importar o xml não foi encontrada.")

    console.print("Carregando informações do XML a ser importado...\n")
    username = getpass.getuser()
    xml_name = f"{xml_file}.xml"
    path_to_xml = f"C:\\Users\\{username}\\Downloads\\{xml_name}"
    console.print("Inserindo caminho do XML...\n")
    main_window.type_keys("%n")
    await worker_sleep(2)
    pyautogui.write(path_to_xml)
    await worker_sleep(2)
    main_window.type_keys("%a")
    await worker_sleep(2)


async def delete_xml(nfe_key: str) -> None:
    """
    Deleta o arquivo xml referente a nota fiscal eletrônica informada.

    Args:
    nfe_key (str): Chave da nota fiscal eletrônica a ser deletada.

    Returns:
    None
    """
    try:
        if not nfe_key:
            raise ValueError("nfe_key não pode ser nulo ou vazio")

        xml_filename = f"{nfe_key}.xml"
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(download_folder, xml_filename)

        if not os.path.exists(file_path):
            console.print(
                f"Arquivo {xml_filename} não encontrado em {download_folder}.",
                style="bold yellow",
            )
            return

        if not os.path.isfile(file_path):
            raise ValueError(f"{file_path} não é um arquivo")

        os.remove(file_path)
        console.print(
            f"Arquivo {xml_filename} deletado com sucesso.", style="bold green"
        )
    except Exception as e:
        console.print(
            f"Erro ao deletar o arquivo {xml_filename}: {str(e)}", style="bold red"
        )
        raise Exception(f"Erro ao deletar o arquivo {xml_filename}: {str(e)}") from e


def config_natureza():
    """
    Configura a natureza da nota fiscal no EMSys.

    Clica no campo Natureza, escreve "16", pressiona a tecla down sete vezes e pressiona enter.
    """
    pyautogui.click(869, 370)
    worker_sleep(1)
    pyautogui.write("16")
    worker_sleep(1)
    pyautogui.press("down", presses=7)
    worker_sleep(1)
    pyautogui.hotkey("enter")
    worker_sleep(1)


def config_almoxarifado(cod_almoxarifado: str) -> None:
    """
    Configura o almoxarifado da nota fiscal no EMSys.

    Clica no campo Almoxarifado, escreve o código do almoxarifado, pressiona a tecla tab e clica em OK.

    :param cod_almoxarifado: Código do almoxarifado.
    :type cod_almoxarifado: str
    :return: None
    :rtype: None
    """
    pyautogui.click(841, 390)
    worker_sleep(1)
    pyautogui.write(cod_almoxarifado)
    worker_sleep(1)
    pyautogui.press("tab")
    worker_sleep(1)
    pyautogui.click(1099, 727)


def check_itens_nota():
    """
    Verifica se os itens da nota fiscal foram cadastrados.

    Clica no botão "Itens" na tela de Nota Fiscal de Entrada e espera 1 segundo.
    Em seguida, clica no botão "OK" na tela de Itens da Nota Fiscal e espera 1 segundo.

    :return: None
    :rtype: None
    """
    pyautogui.click(631, 343)
    worker_sleep(1)
    pyautogui.click(626, 545)
    worker_sleep(1)


def check_pagamento():
    """
    Verifica se o pagamento foi realizado.

    Clica no botão "Pagamento" na tela de Nota Fiscal de Entrada, espera 1 segundo, clica no botão "OK" na tela de Pagamento, espera 1 segundo, escreve "ba" e pressiona a tecla Enter.

    :return: None
    :rtype: None
    """
    pyautogui.click(623, 374)
    worker_sleep(1)
    pyautogui.click(878, 544)
    worker_sleep(1)
    pyautogui.write("ba")
    worker_sleep(1)
    pyautogui.hotkey("enter")
    worker_sleep(1)


def check_pagamento_transferencia_cd():
    pyautogui.click(623, 374)
    worker_sleep(1)
    pyautogui.click(916, 349)
    worker_sleep(1)
    pyautogui.press("down", presses=19)
    worker_sleep(1)
    pyautogui.hotkey("enter")


def preencher_valor_restante(restante):
    pyautogui.click(1284, 351)
    worker_sleep(1)
    pyautogui.write(restante)
    worker_sleep(1)


async def incluir_registro():
    pyautogui.click(594, 297)
    await worker_sleep(30)
    # pyautogui.click(1225, 635)
    # worker_sleep(30)
    # pyautogui.click(959, 564)


def finalizar_importacao():
    """
    Finaliza a importacao de notas no EMSys.

    Clica no botao "Finalizar" na tela de Importacao de Notas e pressiona a tecla enter.

    :return: None
    :rtype: None
    """
    pyautogui.click(597, 299)
    worker_sleep(1)
    pyautogui.hotkey("enter")


async def importar_notas_outras_empresas(data_emissao, numero_nota, empresa=None):
    try:
        # Digita empresa
        data_emissao = data_emissao.replace("/", "")
        if empresa is not None:
            pyautogui.write(empresa)
        else:
            pyautogui.write("171")
        await worker_sleep(1)
        # Digita datas
        pyautogui.click(768, 428)
        await worker_sleep(1)
        pyautogui.write(data_emissao)
        await worker_sleep(1)
        pyautogui.click(859, 430)
        await worker_sleep(1)
        pyautogui.write(data_emissao)
        await worker_sleep(1)
        # Clica Campo 'Num:'"
        pyautogui.click(1014, 428)
        pyautogui.write(numero_nota)
        await worker_sleep(1)
        # Click pesquisar
        pyautogui.click(1190, 428)
        await worker_sleep(20)
        # Click em importar
        pyautogui.click(1207, 684)
        await worker_sleep(20)
        return True
    except Exception as e:
        print(f"Erro ao importar nota: {e}")
        return False


def digitar_datas_emissao(data_emissao: str) -> None:
    """
    Digita as datas de emissão na tela de notas.

    Encontra as posições dos campos 'Data de emissão' e 'Data de emissão fim' na tela
    e digita a data informada.

    :param data_emissao: Data de emissão no formato 'DDMMYYYY'
    :type data_emissao: str
    :raises Exception: Caso não consiga encontrar os campos 'Data de emissão' ou 'Data de emissão fim'
    """
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "emissão", 0, 40, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o campo 'Data de emissão'")
    pyautogui.click(field)
    pyautogui.write(data_emissao)

    field = find_target_position(screenshot_path, "a", 0, 40, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o campo 'Data de emissão fim'")
    pyautogui.click(field)
    pyautogui.write(data_emissao)


async def import_nfe() -> RpaRetornoProcessoDTO:
    """
    Função que clica no botão 'Importar NF-e' no sistema EMsys.

    Retorna um objeto RpaRetornoProcessoDTO com o status do processo.
    Se o botão for encontrado e clicado com sucesso, o status será 'Sucesso'.
    Caso contrário, o status será 'Falha'.

    :return: RpaRetornoProcessoDTO
    """
    await worker_sleep(2)
    console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")

    try:
        importar_nfe = pyautogui.locateOnScreen(
            ASSETS_PATH + "\\entrada_notas\\ImportarNF-e.png", confidence=0.7
        )
        if importar_nfe:
            pyautogui.click(importar_nfe)
            await worker_sleep(8)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Clicou Importar nfe",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possivel localizar o campo 'Importar NF-e' ",
                status=RpaHistoricoStatusEnum.Falha,
            )
    except:
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]
        tpanel = main_window.child_window(class_name="TPanel")
        tpanel.set_focus()
        await worker_sleep(2)

        # Coordernadas relativa a Janela de Notas de entrada e ao filho TPainel
        x_start = 515
        y_start = 1
        x_end = 620
        y_end = 37

        absolute_x = x_start + tpanel.rectangle().left + (x_end - x_start) // 2
        absolute_y = y_start + tpanel.rectangle().top + (y_end - y_start) // 2
        pyautogui.click(absolute_x, absolute_y)
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Clicou Importar nfe",
            status=RpaHistoricoStatusEnum.Sucesso,
        )


def digitar_numero_nota(numero_nota: str) -> None:
    """
    Digita o numero da nota no campo 'Núm Nota' e clica em 'Pesquisar'

    :param numero_nota: Numero da nota a ser digitado
    :type numero_nota: str
    :raises Exception: Caso não consiga encontrar o campo 'Núm Nota' ou o botão 'Pesquisar'
    """
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Núm", 0, 60, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o campo 'Núm Nota'")
    # pyautogui.click(field)
    pyautogui.write(numero_nota)
    console.log("Escreveu numero da nota", style="bold green")
    field = find_target_position(screenshot_path, "pesquisar", 0, 0, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o botão 'Pesquisar'")
    console.log("Clicando em pesquisar", style="bold green")
    pyautogui.click(field)


def select_nfe(nfe_type: str) -> bool:
    """
    Seleciona o tipo de nota fiscal no sistema.

    Args:
        nfe_type (str): Tipo de nota fiscal.

    Returns:
        bool: True se a seleção for feita com sucesso, False caso contrário.
    """
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, nfe_type, 0, 0, 15)
    if field is None:
        raise ValueError(f"Campo '{nfe_type}' não encontrado")

    pyautogui.click(field)

    return True


async def transmitir_nota(
    task: RpaProcessoEntradaDTO, nota_fiscal: str, valor_nota: str
) -> RpaRetornoProcessoDTO:
    """
    Função responsável por transmitir a nota fiscal.

    Args:
        task (RpaProcessoEntradaDTO): Objeto com as informações da nota.
        nota_fiscal (str): Número da nota fiscal.
        valor_nota (str): Valor da nota fiscal.

    Returns:
        RpaRetornoProcessoDTO: Um objeto com o resultado da transmissão da nota.
    """
    pyautogui.click(875, 596)
    logger.info("\nNota Transmitida")
    console.print("\nNota Transmitida", style="bold green")

    await worker_sleep(7)

    # Fechar transmitir nota
    console.print("Fechando a transmissão da nota...\n")

    pyautogui.click(957, 556)

    await worker_sleep(15)
    screenshot_path = take_screenshot()
    transmitir_fechar = find_target_position(screenshot_path, "fechar", attempts=15)
    if transmitir_fechar is not None:
        pyautogui.click(transmitir_fechar)
        log_msg = f"Nota Transmitida com sucesso"
        logger.info(log_msg)
        console.print(log_msg, style="bold green")
    else:
        log_msg = f"Nota não transmitida"
        logger.info(log_msg)
        console.print(log_msg, style="bold red")
        await api_simplifica(
            task.configEntrada.get("urlRetorno"),
            "ERRO",
            log_msg,
            task.configEntrada.get("uuidSimplifica"),
            nota_fiscal,
            valor_nota,
        )
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=log_msg,
            status=RpaHistoricoStatusEnum.Falha,
        )

    return RpaRetornoProcessoDTO(
        sucesso=True,
        retorno="Nota transmitida com sucesso",
        status=RpaHistoricoStatusEnum.Sucesso,
    )


async def select_model_pre_venda(
    text_to_find: str, task: RpaProcessoEntradaDTO
) -> bool:
    """
    Procura se o campo de select ja possui a opção que você precisa selecionada,
    caso sim, retorna True, caso contrário, chama a função find_desired_model
    para selecionar o modelo desejado.

    Args:
        text_to_find (str): Texto a ser procurado no campo modelo
        task (RpaProcessoEntradaDTO): Processo em andamento

    Returns:
        bool: Se o modelo foi selecionado corretamente
    """
    if task is None:
        raise ValueError("task não pode ser nulo")
    if text_to_find is None or len(text_to_find.strip()) == 0:
        raise ValueError("text_to_find não pode ser nulo ou vazio")

    screenshot = take_screenshot()
    field = find_target_position(screenshot, text_to_find, 0, 0, 5)
    if field is None:
        return False
    else:
        return True


async def extract_value():
    # pyautogui.click(1304, 780)
    logger.info("Extrindo Valor da nota")
    pyautogui.doubleClick(1304, 780, interval=0.3)
    pyautogui.doubleClick(1304, 780, interval=0.3)
    pyautogui.hotkey("ctrl", "c")
    console.log(f"Valor nota copiado: {pyperclip.paste()}", style="bold green")
    valor_nota = pyperclip.paste()
    # valor_nota = re.findall(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', valor_nota)
    # print(valor_nota)
    logger.info(valor_nota)
    return valor_nota


async def extract_nf_number() -> str | None:
    """
    Extrai o numero da nota fiscal, baseado na posição do botão gerada na tela

    Returns:
        str: Numero da nota fiscal, None em caso de erro
    """
    logger.info("Extraindo Numero da nota")
    try:
        # screenshot_path = take_screenshot()
        # nota_fiscal_gerada = find_target_position(6395, "gerada", attempts=15)
        # pyautogui.click(nota_fiscal_gerada)
        pyautogui.click(965, 515)
        await asyncio.sleep(5)
        pyautogui.hotkey("ctrl", "c")
        nota_fiscal = pyperclip.paste()
        nota_fiscal = re.findall(r"\d+-?\d*", nota_fiscal)
        if nota_fiscal is None or len(nota_fiscal) == 0:
            raise Exception("Erro ao extrair o numero da nota fiscal")
        logger.info(nota_fiscal)
        return nota_fiscal[0]
    except Exception as e:
        logger.error(f"Erro ao extrair o numero da nota fiscal: {e}")
        return None


async def find_desired_model(text_to_find: str, task: RpaProcessoEntradaDTO) -> bool:
    """
    Encontra o modelo da nota com base na query "get_index_modelo_emsys"

    Args:
        text_to_find (str): Texto a ser procurado no campo modelo
        task (RpaProcessoEntradaDTO): Processo em andamento

    Returns:
        bool: Se o modelo foi selecionado corretamente
    """
    try:
        from worker_automate_hub.api.client import get_index_modelo_emsys

        index = await get_index_modelo_emsys(
            task.configEntrada.get("filialEmpresaOrigem"), text_to_find
        )
        if index is None or index.get("indice") is None:
            raise Exception("Erro ao obter o índice do modelo")
        console.log(f"Indice do banco: {index.get('indice')}")
    except Exception as e:
        console.log(f"Erro ao obter o índice do modelo: {e}", style="bold red")
        return False

    # Se não achou clica no campo modelo e sobe ate a primeira opção
    modelo_select_position = (830, 268)
    pyautogui.click(modelo_select_position)
    # Sobe para o primeiro modelo disponivel
    pyautogui.hotkey("enter")
    pyautogui.press("up", presses=20, interval=0.1)
    try:
        indice: int = int(index.get("indice"))
    except Exception as e:
        console.log(
            f"Erro ao converter o índice do modelo para inteiro: {e}", style="bold red"
        )
        return False
    # Seleciona o modelo com base na query "get_index_modelo_emsys"
    pyautogui.press("down", presses=indice)
    pyautogui.hotkey("tab")

    await worker_sleep(3)
    screenshot = take_screenshot()
    field = find_target_position(screenshot, text_to_find, 0, 0, 5)
    if field:
        console.log("Selecionou Modelo da nota corretamente", style="bold green")
        return True
    else:
        console.log("Modelo não selecionado corretamente", style="bold red")
        return False


async def faturar_pre_venda(task: RpaProcessoEntradaDTO) -> dict:
    await worker_sleep(10)

    # Clica em Faturar
    app = Application().connect(
                class_name="TFrmPreVenda"
            )
    main_window = app["TFrmPreVenda"]
    panel_window = main_window.child_window(class_name="TPage", found_index=0)
    btn_window = panel_window.child_window(class_name="TBitBtn", found_index=7)
    
    if btn_window.exists():
        try:
            btn_window.click()
            await worker_sleep(3)
            console.print("O botão Faturar foi clicado com sucesso.", style="green")
        except:
            console.print("Falha ao clicar no botão faturar.", style="red")
            return {"sucesso": False, "retorno": "Falha ao clicar no botão faturar."}
    else:
        console.print("O Botão Faturar não foi encontrado.", style="red")
        return {"sucesso": False, "retorno": "O Botão Faturar não foi encontrado."}
    
    await worker_sleep(20)
    
    # Alert 
    try:
        app = Application().connect(
                    class_name="TMessageForm"
                )
        main_window = app["TMessageForm"]

        btn_yes = main_window["&Yes"]
        if btn_yes.exists():
            try:
                btn_yes.click()
                await worker_sleep(3)
                console.print("O botão Yes de Faturar foi clicado com sucesso.", style="green")
            except:
                console.print("Falha ao clicar no botão Yes de faturar.", style="red")
                # return {"sucesso": False, "retorno": "Falha ao clicar no botão Yes de faturar."}
        else:
            console.print("O Botão Yes de Faturar não foi encontrado.", style="red")
            # return {"sucesso": False, "retorno": "O Botão Yes de Faturar não foi encontrado."}
    except:
        console.print("O Botão Yes de Faturar não foi encontrado.", style="red")
    
    
    
    await worker_sleep(2)
    console.print(f"Clicou em: 'Faturar'", style="bold green")

    await worker_sleep(10)

    # Aviso "Deseja faturar pré-venda?"
    button_yes = (918, 557)  # find_target_position(screenshot_path, "yes", attempts=15)
    pyautogui.click(button_yes)

    # app = Application().connect(
    #             class_name="TMessageForm"
    #         )
    # main_window = app["TMessageForm"]

    # btn_yes = main_window["&Yes"]
    # if btn_yes.exists():
    #     try:
    #         btn_yes.click()
    #         await worker_sleep(3)
    #         console.print("O botão Yes de deseja faturar pré venda foi clicado com sucesso.", style="green")
    #     except:
    #         console.print("Falha ao clicar no botão Yes de deseja faturar pré venda.", style="red")
    #         return {"sucesso": False, "retorno": "Falha ao clicar no botão Yes de deseja faturar pré venda."}
    # else:
    #     console.print("O Botão Yes de deseja faturar pré venda não foi encontrado.", style="red")
    #     return {"sucesso": False, "retorno": "O Botão Yes de deseja faturar pré venda não foi encontrado."}

    await worker_sleep(10)

    # Verifica se existe a mensagem de recalcular parcelas
    screenshot_path = take_screenshot()
    message_recalcular = find_target_position(screenshot_path, "Recalcular", attempts=5)
    # Se existir clica em nao
    if message_recalcular is not None:
        button_no = (
            999,
            560,
        )  # find_target_position(screenshot_path, "No", attempts=15)
        pyautogui.click(button_no)
        log_msg = "Clicou em 'No' na mensagem de recalcular parcelas"
        console.log(log_msg, style="bold green")
        logger.info(log_msg)
    else:
        log_msg = "A Mensagem de recalcular parcelas não existe"
        logger.info(log_msg)
        console.print(log_msg, style="bold yellow")

    await worker_sleep(8)

    # Seleciona Modelo
    console.log("Selecionando o modelo...\n", style="bold green")
    try:
        app = Application().connect(
                class_name="TFrmDadosFaturamentoPreVenda"
            )
        main_window = app["TFrmDadosFaturamentoPreVenda"]

    
        combo_box_model = main_window.child_window(
            class_name="TDBIComboBox", found_index=1
        )
        combo_box_model.click()

        await worker_sleep(3)
        set_combobox("||List", "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077")
        await worker_sleep(3)

    except Exception as e:
    
        err_msg = "Falha ao selecionar o Modelo"
        await api_simplifica(
            task.configEntrada.get("urlRetorno"),
            "ERRO",
            err_msg,
            task.configEntrada.get("uuidSimplifica"),
            None,
            None,
        )
        return {"sucesso": False, "retorno": err_msg}

    # Extrai total da Nota
    console.log("Obtendo o total da Nota...\n", style="bold green")
    valor_nota = await extract_value()
    console.print(f"\nValor NF: '{valor_nota}'", style="bold green")

    # Clicar no botao "OK" com um certo verde
    app = Application().connect(
                class_name="TFrmDadosFaturamentoPreVenda"
            )
    main_window = app["TFrmDadosFaturamentoPreVenda"]
    btn_window = main_window.child_window(class_name="TBitBtn", found_index=1)
    
    if btn_window.exists():
        try:
            btn_window.click()
            await worker_sleep(3)
            console.print("O botão Ok verde foi clicado com sucesso.", style="green")
        except:
            console.print("Falha ao clicar no botão Ok verde.", style="red")
            return {"sucesso": False, "retorno": "Falha ao clicar no botão Ok verde."}
    else:
        console.print("O Botão Ok verde não foi encontrado.", style="red")
        return {"sucesso": False, "retorno": "O Botão Ok verde não foi encontrado."}
    
    await worker_sleep(10)

    # Alert de pré venda
    try:
        app = Application().connect(
                    class_name="TMessageForm"
                )
        main_window = app["TMessageForm"]

        btn_yes = main_window["&Yes"]
        if btn_yes.exists():
            try:
                btn_yes.click()
                await worker_sleep(3)
                console.print("O botão Yes de deseja faturar pré venda foi clicado com sucesso.", style="green")
            except:
                console.print("Falha ao clicar no botão Yes de deseja faturar pré venda.", style="red")
                return {"sucesso": False, "retorno": "Falha ao clicar no botão Yes de deseja faturar pré venda."}
        else:
            console.print("O Botão Yes de deseja faturar pré venda não foi encontrado.", style="red")
            return {"sucesso": False, "retorno": "O Botão Yes de deseja faturar pré venda não foi encontrado."}
    except:
        console.print("O Botão Yes de deseja faturar pré venda não foi encontrado.", style="red")
        return {"sucesso": False, "retorno": "O Botão Yes de deseja faturar pré venda não foi encontrado."}
    
    return {"sucesso": True, "retorno": "Faturar pre venda concluído com sucesso!", "valor_nota": valor_nota}

@repeat(times=5, delay=30)
async def wait_window_close(window_name):
    from pywinauto import Desktop
    desktop = Desktop(backend="uia")
    # Loop infinito para verificar continuamente a janela
    while True:
        try:
            # Tenta localizar a janela com o título que contém "Aguarde"
            window = desktop.window(title_re=window_name)
            # Se a janela existe, continua monitorando
            if window.exists():
                console.print(
                    f"Janela '{window_name}' ainda aberta", style="bold yellow"
                )
            else:
                await worker_sleep(5)
                console.print(
                    f"Janela '{window_name}' foi fechada.", style="bold green"
                )
                try:
                    window = desktop.window(title_re=window_name)
                    if window.exists():
                        console.print(
                            f"Janela '{window_name}' ainda aberta", style="bold yellow"
                        )
                        continue
                except:
                    console.log("Janela 'Aguarde' não existe mais.", style="bold green")
                # Clica em ok "processo finalizado"
                await worker_sleep(5)
                pyautogui.click(957, 556)
                # Clica em fechar
                await worker_sleep(2)
                pyautogui.click(1200, 667)
                return False  # Retorna falso pois a janela esta fechada
            await worker_sleep(2)  # Espera 2 (* o multiplicador) segundos antes de verificar novamente
        except Exception as e:
            console.print(f"Erro: {e}")
            return True

    # console.log("Esperando transmissao da nota", style='bold green')
    # aguardando_nota = True
    # timeout = 40
    # timeout_try = 0
    # while(aguardando_nota == False or timeout >= timeout_try):
    #     console.print(f"Tentativa número: {timeout_try}", style="bold yellow")
    #     logger.info(f"Tentativa número: {timeout_try}")
    #     await worker_sleep(15)
    #     screenshot_path = take_screenshot()
    #     target = find_target_position(screenshot_path, "gerando", 1, 0, 6)
    #     if target:
    #         console.print("Aguardando nota ser transmitida...", style="bold yellow")
    #         logger.info("Aguardando nota ser transmitida...")
    #         timeout_try += 1
    #         await worker_sleep(8)
    #         continue
    #     else:
    #         await worker_sleep(5)
    #         console.print("Verificando lançamento da nota", style="bold yellow")
    #         logger.info("Verificando lançamento da nota")
    #         screenshot_path = take_screenshot()
    #         target_nota_lancada = find_target_position(screenshot_path, "autorizado", 1, 0, 3)
    #         if target_nota_lancada:
    #             console.print("Nota lançada com sucesso.", style="bold green")
    #             logger.info("Nota lançada com sucesso.")
    #             #Fechar transmitir nota
    #             console.print("Fechando a transmissão da nota...\n", style='bold green')
    #             logger.info("Fechando a transmissão da nota...")
    #             #Clica em ok "processo finalizado"
    #             await worker_sleep(5)
    #             pyautogui.click(957, 556)
    #             #Clica em  fechar
    #             await worker_sleep(2)
    #             pyautogui.click(1200, 667)
    #             aguardando_nota = False
    #             break
    #         else:
    #             console.print("Nota ainda não lançada", style="bold yellow")
    #             logger.info("Nota ainda não lançada")
    #             timeout_try += 1
    #             await worker_sleep(8)

    # return aguardando_nota


async def verify_nf_incuded() -> bool:
    """
    Verifica se a nota fiscal foi incluída com sucesso.

    Returns:
        bool: True se a nota foi incluída, False caso contrário
    """
    try:
        nota_incluida = pyautogui.locateOnScreen(
            ASSETS_PATH + "\\entrada_notas\\nota_fiscal_incluida.png", confidence=0.7
        )
        if nota_incluida:
            return True
        else:
            return False
            # pyautogui.click(959, 562)
    except Exception as e:
        console.print(f"Error: {e}")
        return False


async def rateio_window(nota: dict):
    """
    Abre a janela de rateio de nota e preenche todos os campos com base na nota informada.

    Args:
        nota (dict): Dicionario com as informacoes da nota.

    Raises:
        ValueError: Se a nota for nula.
        RuntimeError: Se nao for possivel encontrar o campo "todos" na tela.
        RuntimeError: Se nao for possivel converter o valor da nota para inteiro.
    """
    if nota is None:
        raise ValueError("Nota nao pode ser nula")

    screenshot_path = take_screenshot()

    # Clica em Selecionar todos
    field = find_target_position(screenshot_path, "todos", 0, 0, 15)
    if field is None:
        raise RuntimeError("Nao foi possivel encontrar o campo 'todos'")

    pyautogui.click(field)
    await worker_sleep(2)

    # Digita "Centro" 1000 + filialEmpresaOrigem
    pyautogui.click(788, 514)
    try:
        filial = 1000 + int(nota.get("filialEmpresaOrigem"))
    except TypeError:
        raise RuntimeError("Nao foi possivel converter o valor da nota para inteiro")
    pyautogui.write(str(filial))
    pyautogui.hotkey("tab")

    # Marca "Aplicar rateio aos itens selecionados"
    pyautogui.hotkey("space")
    pyautogui.hotkey("tab")

    # Digita % Rateio
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("del")
    pyautogui.write("100")

    # Clica Incluir registro
    pyautogui.click(1161, 548)
    await asyncio.sleep(20)

    # Clica OK
    pyautogui.click(1200, 683)
    await worker_sleep(5)


def check_screen_resolution():
    """
    Verifica se a resolução atual da tela é a recomendada.

    Imprime um aviso se a resolução atual for diferente da recomendada.
    """
    screen_width, screen_height = pyautogui.size()
    screen_width_recommended = 1280
    screen_height_recommended = 720

    if (
        screen_width != screen_width_recommended
        or screen_height != screen_height_recommended
    ):
        console.print(
            f"\nAviso: A resolução atual da tela é {screen_width}x{screen_height}. Recomendado: {screen_width_recommended}x{screen_height_recommended}. Podem ocorrer erros nos processos.\n",
            style="bold yellow",
        )
        logger.info(
            f"Aviso: A resolução atual da tela é {screen_width}x{screen_height}. Recomendado: {screen_width_recommended}x{screen_height_recommended}."
        )


async def capture_and_send_screenshot(uuidRelacao: str, desArquivo: str) -> None:
    """
    Função que captura uma screenshot da tela, salva em um buffer e a envia usando a função send_file.

    Args:
        uuidRelacao (str): UUID da relação associada ao arquivo.
        desArquivo (str): Descrição do arquivo.
        tipo (str): Tipo de arquivo (imagem, etc).
    """
    try:
        from worker_automate_hub.api.client import send_file

        # Tira a screenshot
        screenshot = pyautogui.screenshot()

        # Salva a screenshot em um buffer de memória em formato PNG
        screenshot_buffer = io.BytesIO()
        screenshot.save(screenshot_buffer, format="PNG")

        # Reseta o cursor do buffer para o início
        screenshot_buffer.seek(0)

        # Adiciona um timestamp ao nome do arquivo para evitar duplicatas
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        desArquivo = f"{desArquivo}_{timestamp}.png"

        # Chama a função para enviar o arquivo
        await send_file(uuidRelacao, desArquivo, "img", screenshot_buffer.read())

    except Exception as e:
        err_msg = f"Erro ao capturar ou enviar a screenshot: {str(e)}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


async def read_xml_file(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespaces = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

        itens = []

        for item in root.findall(".//nfe:det", namespaces):
            prod = item.find("nfe:prod", namespaces)
            if prod is not None:
                codigo = (
                    prod.find("nfe:cProd", namespaces).text
                    if prod.find("nfe:cProd", namespaces) is not None
                    else None
                )
                descricao = (
                    prod.find("nfe:xProd", namespaces).text
                    if prod.find("nfe:xProd", namespaces) is not None
                    else None
                )
                quantidade = (
                    prod.find("nfe:qCom", namespaces).text
                    if prod.find("nfe:qCom", namespaces) is not None
                    else None
                )
                valor_unitario = (
                    prod.find("nfe:vUnCom", namespaces).text
                    if prod.find("nfe:vUnCom", namespaces) is not None
                    else None
                )
                n_item = item.attrib.get("nItem", None)

                itens.append(
                    {
                        "n_item": n_item,
                        "codigo": codigo,
                        "descricao": descricao,
                        "quantidade": quantidade,
                        "valor_unitario": valor_unitario,
                    }
                )

        return itens

    except FileNotFoundError:
        raise Exception(f"arquivo XML não encontrado")
    except ET.ParseError as e:
        raise Exception(f"Erro ao analisar o arquivo XML: {e}")
    except Exception as e:
        raise Exception(f"Ocorreu um erro: {e}")


async def extract_group_by_itens(itens):
    informacoes = []

    for item in itens:
        n_item = item["n_item"]
        descricao = item["descricao"]

        console.print(f"Tentando obter o formato no primeiro regex - item {descricao}.. \n")
        try:
            match = re.search(r"\((\d+)X(\d+)(L|KG)?\)", descricao)
            formato = match.group(0) if match else None
        except Exception as e:
            console.print(f" Erro ao obter o regex no primeiro formato - item {descricao}, erro {e}.. \n")
            formato = None


        if formato is None:
            try:
                match = re.search(r"(\d+X\d+(\w+))", descricao)
                formato = match.group(0) if match else None
            except Exception as e:
                console.print(f" Erro ao obter o regex no segundo formato - item {descricao}, erro {e}.. \n")
                formato = None
        
        if formato is not None:
            formato = formato.replace("(", "").replace(")", "")
        else:
            console.print(f"Formato não encontrado para o item {n_item}: {descricao}\n")

        informacoes.append(
            {"n_item": n_item, "formato": formato, "descricao": descricao}
        )

    return informacoes


async def select_documento_type(document_type: str) -> RpaRetornoProcessoDTO:
    """
    Função que seleciona o tipo de documento na janela de Nota Fiscal de Entrada.

    Args:
        document_type (str): Tipo de documento a ser selecionado.

    Returns:
        RpaRetornoProcessoDTO: Retorna um objeto com informações sobre o status do processo.
    """
    try:
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()

        console.print(
            "Controles encontrados na janela 'Nota Fiscal de Entrada, navegando entre eles...\n"
        )
        panel_TNotebook = main_window.child_window(
            class_name="TNotebook", found_index=0
        )
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(
            class_name="TPageControl", found_index=0
        )
        panel_TTabSheet = panel_TPageControl.child_window(
            class_name="TTabSheet", found_index=0
        )
        combo_box_tipo_documento = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=1
        )
        combo_box_tipo_documento.click()
        console.print(
            "Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n"
        )
        await worker_sleep(4)
        set_combobox("||List", document_type)
        console.print(
            f"Tipo de documento '{document_type}', selecionado com sucesso...\n"
        )

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Documento {document_type} selecionado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel selecionar o tipo do documento, erro: {e} ",
            status=RpaHistoricoStatusEnum.Falha,
        )


class WindowStatus(TypedDict):
    IsOpened: bool
    Janela: str


async def is_window_open(window_title: str) -> WindowStatus:
    """
    Verifica se uma janela esta aberta atraves do titulo da janela.

    Args:
    - window_title (str): Titulo da janela

    Returns:
    - WindowStatus: Dicionario com a chave IsOpened e o valor bool e a chave Janela com o valor da janela
    """
    try:
        app = Application().connect(title=window_title)
        main_window = app[window_title]
        return WindowStatus(IsOpened=True, Janela=window_title)

    except findwindows.ElementNotFoundError:
        return WindowStatus(IsOpened=False, Janela=window_title)

    except Exception as e:
        raise ValueError(f"Erro ao verificar telas erros/warnings {e}")


async def is_window_open_by_class(window_class: str, app_class: str) -> WindowStatus:
    """
    Verifica se uma janela esta aberta atraves da classe da janela.

    Args:
    - window_class (str): Classe da janela
    - app_class (str): Classe do aplicativo

    Returns:
    - WindowStatus: Dicionario com a chave IsOpened e o valor bool e a chave Janela com o valor da janela
    """
    try:
        app = Application().connect(class_name=window_class)
        return WindowStatus(IsOpened=True, Janela=app_class)

    except findwindows.ElementNotFoundError:
        return WindowStatus(IsOpened=False, Janela=app_class)

    except Exception as e:
        raise ValueError(f"Erro ao verificar telas erros itens/warnings {e}")



async def warnings_after_xml_imported() -> RpaRetornoProcessoDTO:
    """
    Função responsável por verificar se existe um warning após a importação do xml,
    e clicar no botão NO para andamento do processo.

    :return: RpaRetornoProcessoDTO com o status e o retorno da operação.
    """
    console.print("Interagindo com a tela de warning após a importação do xml...\n")
    app = Application().connect(title="Warning")
    main_window = app["Warning"]

    console.print("Verificando se existe o botao NO, para andamento do processo...\n")
    # btn_no = main_window.child_window(title="&No")
    btn_no = main_window["&No"]

    if btn_no.exists():
        try:
            console.print("Clicando em NO, para andamento do processo...\n")
            btn_no.click()
            await worker_sleep(4)
            if main_window.exists():
                console.print(
                    "Verificando se existe um segundo botao NO, para andamento do processo...\n"
                )
                btn_no = main_window["&No"]
                # btn_no = main_window.child_window(title="&No")
                console.print("Clicando novamente em NO")
                btn_no.click()
                await worker_sleep(5)
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Sucesso para clicar em NO",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

            else:
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Sucesso para clicar em NO",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

        except Exception as e:
            console.print(f"Erro ao clicar em NO: {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Warning: Erro ao clicar em NO: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

    else:
        console.print("Warning - Erro após a importação do arquivo...\n")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno="Warning - Erro após a importação do arquivo, não foi encontrado o botão No para andamento do processo... \n",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def error_after_xml_imported() -> RpaRetornoProcessoDTO:
    await worker_sleep(3)
    """
    Função responsável por verificar se existe um erro após a importação do xml,
    e capturar a mensagem de erro para posterior log.

    :return: RpaRetornoProcessoDTO com o status e o retorno da operação.
    """
    console.print("Interagindo com a tela de erro após a importação do xml...\n")
    app = Application().connect(title="Erro")
    main_window = app["Erro"]
    await worker_sleep(7)
    all_controls_from_error = main_window.children()
    capturar_proxima_mensagem = False
    console.print("Obtendo mensagem de erro mapeada...\n")

    for control in all_controls_from_error:
        control_text = control.window_text()
        console.print(control_text)

        if "Mensagem do Banco de Dados" in control_text:
            capturar_proxima_mensagem = True

        elif capturar_proxima_mensagem:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro do banco de dados: {control_text} \n",
                status=RpaHistoricoStatusEnum.Falha,
            )

        elif "XML já foi importado anteriormente" in control_text:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nota descartada: {control_text}... \n",
                status=RpaHistoricoStatusEnum.Descartado,
            )

        elif "xml" in control_text.lower():
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nota descartada: {control_text}... \n",
                status=RpaHistoricoStatusEnum.Descartado,
            )
        

async def error_before_persist_record() -> RpaRetornoProcessoDTO:
    try:
        console.print("Interagindo com a tela de erro após clicar em incluir registro...\n")
        app = Application().connect(title="Information")
        main_window = app["Erro"]
        await worker_sleep(7)
        all_controls_from_error = main_window.children()
        capturar_proxima_mensagem = False
        console.print("Obtendo mensagem de erro mapeada...\n")

        for control in all_controls_from_error:
            control_text = control.window_text()

            if "que a data de entrada" in control_text:
                 return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao incluir registro, As datas das parcelas não podem ser menores que a data de entrada da nota: {control_text} \n",
                status=RpaHistoricoStatusEnum.Falha,
            )

            elif capturar_proxima_mensagem:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao incluir registro: {control_text} \n",
                    status=RpaHistoricoStatusEnum.Falha,
                )
    except:
        console.print("Erro ao capturar mensagem de erro")


# TODO: Melhorar o retorno
async def itens_not_found_supplier(xml: str):
    try:
        username = getpass.getuser()
        console.print("Verificando se existe tela de multiplas referencias.\n")
        await worker_sleep(10)

        itens_fornecedor = await is_window_open_by_class(
            "TFrmSelecionaItensFornecedor", "TFrmSelecionaItensFornecedor"
        )

        if itens_fornecedor["IsOpened"] == True:
            console.print("Tela de multiplas referencias existe.\n")
            return {
                "sucesso": True,
                "retorno": f"Tela de Itens fornecedor - Multiplas referencias",
                "window": "MultiplasRef",
            }
        
        console.print("Iteragindo com a tela de itens não localizados // NCM ...\n")
    
        app = Application().connect(class_name="TFrmAguarde", timeout=60)

        max_attempts = 60
        i = 0

        while i < max_attempts:
            try:
                main_window = app["TMessageForm"]
                console.print(f"Janela 'TMessageForm' encontrada!")
                break
            except Exception as e:
                console.print(f"Erro ao tentar acessar TMessageForm: {e}")
                janela_aguarde = await is_window_open_by_class(
                    "TFrmAguarde", "TFrmAguarde"
                )
                if janela_aguarde["IsOpened"] == True:
                    console.print(f"Aguardando tela de aguarde desaparecer ou conectar a tela de information...\n")
                else:
                    try:
                        main_window = app["TMessageForm"]
                        if main_window.exists():
                            console.print(f"Janela 'TMessageForm' encontrada!")
                            break
                    except:
                        return {
                            "sucesso": True,
                            "retorno": f"Tela de aguardar carregada - Seguindo com andamento do processo",
                            "window": "NCM",
                        }
            await worker_sleep(3)
            i += 1

        window_title = main_window.window_text()

        if "Confirm" in window_title:
            console.print(f"Itens nao localizados para o fornecedor...\n")
            if main_window.exists():
                main_window.type_keys("%n")

                await worker_sleep(10)
                console.print(
                    "Verificando a existencia de tela de selecionar Itens Fornecedor...\n"
                )
                itens_fornecedor = await is_window_open_by_class(
                    "TFrmSelecionaItensFornecedor", "TFrmSelecionaItensFornecedor"
                )

                if itens_fornecedor["IsOpened"] == True:
                    return {
                        "sucesso": True,
                        "retorno": f"Tela de Itens fornecedor - Multiplas referencias",
                        "window": "MultiplasRef",
                    }
                else:
                    console.print(
                    "Não possui a existencia de tela de selecionar Itens Fornecedor...\n"
                    )
                

                await worker_sleep(10)
                console.print("Verificando a existe da tela dos itens com erro...\n")

                max_attempts = 60
                i = 0
                while i < max_attempts:
                    logs_erro = await is_window_open_by_class("TFrmExibeLogErroImportacaoNfe","TFrmExibeLogErroImportacaoNfe")
                    if logs_erro["IsOpened"] == True:
                        break
                    else:
                        console.print(f"Aguardando confirmação de tela de erro importação NFe...\n")
                        try:
                            app = Application().connect(class_name="TFrmAguarde")
                            main_window = app["TMessageForm"]
                            console.print(f"Janela 'Information' encontrada!")
                            window_title = main_window.window_text()
                            if "Information" in window_title:
                                main_window.type_keys("%n")
                            else:
                                console.print(
                                    "Não possui a existencia de tela de Information, seguindo...\n"
                                )
                        except:
                            console.print(
                            "Não possui a existencia de tela de Information...\n"
                            )
                        await worker_sleep(5)
                        i += 1

                logs_erro = await is_window_open_by_class("TFrmExibeLogErroImportacaoNfe","TFrmExibeLogErroImportacaoNfe")
                if logs_erro["IsOpened"] == True:
                    app = Application().connect(class_name="TFrmExibeLogErroImportacaoNfe")
                    main_window = app["TFrmExibeLogErroImportacaoNfe"]
                    console.print("Tela com itens com erro existe, salvando os itens...\n")

                    btn_save = main_window.child_window(
                        title="Salvar", class_name="TBitBtn"
                    )

                    if btn_save.exists():
                        max_attempts = 3
                        i = 0
                        while i < max_attempts:
                            console.print("Clicando no botão de salvar...\n")
                            try:
                                btn_save.click()
                            except:
                                console.print("Não foi possivel clicar no Botão OK... \n")

                            await worker_sleep(3)

                            console.print(
                                "Verificando a existencia da tela para informar o caminho do arquivo...\n"
                            )

                            try:
                                app = Application().connect(title="Salvar")
                                main_window = app["Salvar"]
                                console.print(
                                    "Tela para informar o caminho do arquivo existe"
                                )
                                break
                            except Exception as e:
                                console.print(
                                    f"Tela para informar o caminho do arquivo não encontrada. Tentativa {i + 1}/{max_attempts}."
                                )

                            i += 1

                        if i == max_attempts:
                            raise Exception(
                                "Número máximo de tentativas atingido. Tela para informar o caminho do arquivo existe."
                            )

                        await worker_sleep(4)
                        console.print(
                            "Interagindo com a tela para informar o caminho do arquivo...\n"
                        )
                        app = Application().connect(title="Salvar")
                        main_window = app["Salvar"]
                        console.print(
                            "Tela para informar o caminho do arquivo existe, inserindo o diretorio...\n"
                        )
                        await worker_sleep(2)
                        main_window.type_keys("%n")
                        path_to_txt = (
                            f"C:\\Users\\{username}\\Downloads\\erro_itens{xml}.txt"
                        )
                        pyautogui.write(path_to_txt)
                        await worker_sleep(1)
                        main_window.type_keys("%l")
                        console.print(f"Arquivo salvo com sucesso... \n")

                        conteudo = ""
                        await worker_sleep(3)
                        with open(
                            path_to_txt, "r", encoding="latin1", errors="replace"
                        ) as arquivo:
                            conteudo = arquivo.read()
                            console.print(
                                f"Arquivo salvo com sucesso, itens com erro {conteudo}...\n"
                            )

                        os.remove(path_to_txt)
                        console.print(
                            f"Removendo o arquivo e enviando os itens para o backoffice... \n"
                        )
                        console.print(
                            f"Itens nao localizados para o fornecedor salvo e retornando como falha no backoffice para correção...\n"
                        )
                        return {
                            "sucesso": True,
                            "retorno": f"Itens nao localizados para o fornecedor, Mensagem: {conteudo}",
                            "window": "Itens",
                        }
                    else:
                        console.print(f"Botao Salvar - Não foi encontrado...\n")
                        return {
                            "sucesso": False,
                            "retorno": f"Botao Salvar - Não foi encontrado",
                            "window": "Itens",
                        }
                else:
                    return {
                        "sucesso": False,
                        "retorno": f"Tela para salvar as informações dos itens com erro não encontrada, tentar novamente...",
                        "window": "Erro",
                    }
            else:
                return {
                        "sucesso": False,
                        "retorno": f"Erro não mapeado, pop-up Confirm não encontrado...",
                        "window": "Erro",
                    }
        elif "Information" in window_title:
            console.print(f"Tela de NCM para o fornecedor...\n")
            if main_window.exists():
                console.print(
                    f"Tela de NCM clicando em NO para andamento no processo...\n"
                )
                main_window.type_keys("%n")
                return {
                    "sucesso": True,
                    "retorno": f"Tela de NCM - clicado em NO para andamento do processo ",
                    "window": "NCM",
                }
    except Exception as e:
        return {
            "sucesso": False,
            "retorno": f"Erro ao processar tela de itens // ncm {e}",
            "window": "Erro",
        }



async def tipo_despesa(tipo: str) -> RpaRetornoProcessoDTO:
    console.print(f"Conectando a tela de Informações para importação da Nota Fiscal Eletrônica para seleção do tipo de despesas...\n")
    try:
        new_app = Application(backend="uia").connect(
        title="Informações para importação da Nota Fiscal Eletrônica"
        )
        window = new_app["Informações para importação da Nota Fiscal Eletrônica"]

        console.print(f"Conectado com sucesso, acessando o atributo filho ' Tipo de Despesa'...\n")
        tipo_despesa = window.child_window(title=" Tipo de Despesa", class_name="TGroupBox")

        console.print(f"Conectado com sucesso, inserindo o valor do tipo de despesa...\n")

        edit = tipo_despesa.child_window(
            class_name="TDBIEditCode", found_index=1, control_type="Edit"
        )

        if edit.exists():
            edit.set_edit_text(tipo)
            edit.type_keys("{TAB}")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Sucesso para inserir o valor da despesa",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            console.print(f"Campo tipo de despesas - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Campo tipo de despesas - Não foi encontrado... \n",
            status=RpaHistoricoStatusEnum.Falha,
        )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para inserir o tipo de despesa, erro: {e}... \n",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def zerar_icms() -> RpaRetornoProcessoDTO:
    console.print(f"Conectando a tela de Informações para importação da Nota Fiscal Eletrônica para marcar a opção Zerar ICMS...\n")
    try:
        new_app = Application(backend="uia").connect(
        title="Informações para importação da Nota Fiscal Eletrônica"
        )
        window = new_app["Informações para importação da Nota Fiscal Eletrônica"]

        checkbox = window.child_window(
            title="Zerar tributação ICMS", class_name="TCheckBox", control_type="CheckBox"
        )
        if checkbox.exists():
            if not checkbox.get_toggle_state() == 1:
                checkbox.click()
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Sucesso para interagir com o checkbox para zerar o valor do icms",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
        else:
            console.print(f"Campo zerar icms - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Sucesso para inserir o valor da despesa",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para marcar a opção de zerar ICMS, erro: {e}... \n",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def cod_icms(codigo: str) -> RpaRetornoProcessoDTO:
    console.print(f"Conectando a tela de Informações para importação da Nota Fiscal Eletrônica para informar o codigo do icms...\n")
    try:
        new_app = Application(backend="uia").connect(
        title="Informações para importação da Nota Fiscal Eletrônica"
        )
        window = new_app["Informações para importação da Nota Fiscal Eletrônica"]

        console.print(f"Conectado com sucesso, acessando o atributo filho 'ICMS'...\n")
        icms_codigo = window.child_window(title="ICMS", class_name="TGroupBox")

        console.print(f"Conectado com sucesso, inserindo o valor do codigo do icms...\n")

        edit = icms_codigo.child_window(
            class_name="TDBIEditCode", found_index=0, control_type="Edit"
        )

        if edit.exists():
            edit.set_edit_text(codigo)
            edit.type_keys("{TAB}")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Sucesso para inserir o codigo do icms",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            console.print(f"Campo codigo do icms - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo codigo do icms - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para inserir o codigo do icms, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def rateio_despesa(unidade_code: str)  -> RpaRetornoProcessoDTO:
    console.print(f"Conectando a tela de Rateio da Despesa para encerramento do processo...\n")
    console.print(f"Código filial {unidade_code}...\n")
    try:

        console.print(f"Tentando clicar em Selecionar todos...\n")
        try:
            selecionar_todos = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\entrada_notas\\SelecionarTodos.png", confidence=0.5
            )
            if selecionar_todos:
                console.print(f"Campo selecionar todos encontrado, interagindo...\n")
                pyautogui.click(selecionar_todos)
                
        except Exception as e:
            console.print(f"Error ao interagir com o campo de selecionar todos : {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Error ao interagir com o campo de selecionar todos : {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(5)

        try:
            app = Application().connect(class_name="TFrmDadosRateioDespesa")
            main_window = app["TFrmDadosRateioDespesa"]
            console.print(f"Conectado com pela classe do emsys...\n")
        except:
            app = Application().connect(title="Rateio da Despesa")
            main_window = app["Rateio da Despesa"]
            console.print(f"Conectado pelo title...\n")
        

        main_window.set_focus()

        console.print(f"Conectado com sucesso, acessando o atributo filho 'Centro'...\n")
        panel_centro = main_window.child_window(class_name="TPanel", found_index=1)

        console.print(f"Conectado com sucesso, inserindo o valor do tipo de despesa...\n")

        edit = panel_centro.child_window(class_name="TDBIEditCode", found_index=1)

        try:
            value_centro = int(unidade_code) + 1000
        except ValueError:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Unidade code não é um número válido.",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        value_centro_str = str(value_centro)
        console.print(f"Valor final a ser inserido no Centro {value_centro_str}...\n")

        if edit.exists():
            edit.set_edit_text(value_centro_str)
            edit.type_keys("{TAB}")
        else:
            console.print(f"Campo tipo de despesas - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo tipo de despesas - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        console.print(f"Conectado com sucesso, inserindo o valor do rateio...\n")
        edit = panel_centro.child_window(class_name="TDBIEditNumber", found_index=0)

        if edit.exists():
            edit.set_edit_text("100")
            edit.click()
            edit.type_keys("{TAB}")
        else:
            console.print(f"Campo valor do rateio - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo valor do rateio - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        await worker_sleep(3)
        
        console.print(f"Selecionando a opção 'Aplicar Rateio aos Itens Selecionados'...\n")
        try:
            checkbox = panel_centro.child_window(
                title="Aplicar Rateio aos Itens Selecionados",
                class_name="TDBICheckBox",
            )
            checkbox.click()
            console.print("A opção 'Aplicar Rateio aos Itens Selecionados' selecionado com sucesso... \n")
        except:
            try:
                aplicar_rateio = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\entrada_notas\\aplicar_rateio_itens.png", confidence=0.5
                )
                if aplicar_rateio:
                    console.print(f"Campo aplicar rateio itens encontrado, clicando...\n")
                    center_x, center_y = pyautogui.center(aplicar_rateio)
                    try:
                        pyautogui.click(center_x, center_y)
                    except:
                        pyautogui.click(aplicar_rateio)
            except:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Campo aplicar rateio - Não foi encontrado",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            
        console.print(f"Tentando clicar em Incluir Registro...\n")
        await worker_sleep(2)
        try:
            console.print(f"Não foi possivel clicar em Incluir Registro, tentando via hotkeys..\n")
            pyautogui.press('tab')
            pyautogui.press('tab')
            await worker_sleep(2)
            pyautogui.press('enter')
            await worker_sleep(4)
        except Exception as e:
            try:
                incluir_registro_rateio = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\entrada_notas\\importar_registro_rateio_despesas.png", confidence=0.5
                )
                if incluir_registro_rateio:
                    console.print(f"Campo selecionar todos encontrado, interagindo...\n")
                    pyautogui.click(incluir_registro_rateio)
            except:
                console.print(f"Clicando em Incluir registro para vincular ao centro de custo '...\n")
                edit = panel_centro.child_window(class_name="TDBITBitBtn", found_index=3)

                if edit.exists():
                    edit.click()
                else:
                    console.print(f"Campo Incluir registro nao foi encontrado...\n")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Campo Incluir registro nao foi encontrado",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
                
        await worker_sleep(3)

        console.print(f"Verificando se o item foi rateado com sucesso...\n")
        panel_centro = main_window.child_window(class_name="TPanel", found_index=0)
        edit = panel_centro.child_window(class_name="TDBIEditNumber", found_index=0)

        if edit.exists():
            valor_total_rateado = edit.window_text()
            if valor_total_rateado != '0,00':
                console.print(f"Rateio inserido com sucesso., clicando em OK..\n")
                send_keys('%o')
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Rateio de despesa interagido com sucesso",
                    status=RpaHistoricoStatusEnum.Sucesso,
                ) 
            
        else:
            console.print(f"Campo valor do rateio - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Campo valor do rateio - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
            )        

        
    except Exception as e:
        return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para inserir o tipo de despesa, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )


async def select_nop_document_type(nop: str) -> RpaRetornoProcessoDTO:
    """
    Função que seleciona o tipo o NOP Nota na janela de Nota Fiscal de Entrada.

    Args:
        nop (str): Qual opção nop a ser selecionada.

    Returns:
        RpaRetornoProcessoDTO: Retorna um objeto com informações sobre o status do processo.
    """
    try:
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]

        main_window.set_focus()

        console.print(
            "Controles encontrados na janela 'Nota Fiscal de Entrada, navegando entre eles...\n"
        )
        panel_TNotebook = main_window.child_window(
            class_name="TNotebook", found_index=0
        )
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(
            class_name="TPageControl", found_index=0
        )
        panel_TTabSheet = panel_TPageControl.child_window(
            class_name="TTabSheet", found_index=0
        )
        combo_box_nop_nota = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=0
        )
        combo_box_nop_nota.click()
        console.print(
            "Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n"
        )
        await worker_sleep(2)
        set_combobox("||List", nop)
        console.print(
            f"NOP Nota '{nop}', selecionado com sucesso...\n"
        )

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"NOP Nota {nop} selecionado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel selecionar o NOP Nota, erro: {e} ",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def carregamento_import_xml() -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name="TFrmAguarde", timeout=20)
        max_attempts = 60
        i = 0

        while i < max_attempts:
            try:
                main_window = app["TMessageForm"]
                window_title = main_window.window_text()
                if "Confirm" in window_title or "Information" in window_title:
                    console.print(f"Janela 'TMessageForm' encontrada!")
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno=f"Janela de information encontrada",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )
            except:
                console.print(f"Janela 'TMessageForm' não encontrada!")

            try:
               app = Application().connect(class_name="TFrmAguarde")
            except Exception as e:
                console.print(f"Nota importada sem Warnings ou Informations, seguindo com andamento do fluxo")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Nota importada sem Warnings ou Informations, seguindo com andamento do fluxo",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
                
            await worker_sleep(2)
            i += 1
            
        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Tentando seguir com o fluxo",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

    except Exception as e:
        console.print(f"Não foi possivel conectar a tela de aguarde para carregamento da nota: {e}")
        return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Não foi possivel conectar a tela de aguarde para carregamento da nota, mas tentando seguir com o fluxo",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
    
async def check_nota_importada(xml_nota: str) -> RpaRetornoProcessoDTO:
    try:
        max_attempts = 60
        i = 0

        while i < max_attempts:
            information_pop_up = await is_window_open("Information")
            if information_pop_up["IsOpened"] == True:
                break
            else:
                console.print(f"Aguardando confirmação de nota incluida...\n")
                await worker_sleep(5)
                i += 1
                
        information_pop_up = await is_window_open("Information")
        if information_pop_up["IsOpened"] == True:
            app = Application().connect(class_name="TFrmNotaFiscalEntrada")
            main_window = app["Information"]

            main_window.set_focus()

            console.print(f"Obtendo texto do Information...\n")
            console.print(f"Tirando print da janela do Information para realização do OCR...\n")

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
            path_to_png = f"C:\\Users\\{username}\\Downloads\\information_popup_{xml_nota}.png"
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
            if 'nota fiscal inc' in captured_text.lower():
                console.print(f"Tentando clicar no Botão OK...\n")
                btn_ok = main_window.child_window(class_name="TButton")

                if btn_ok.exists():
                    btn_ok.click()
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno=f"Nota incluida com sucesso",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Pop_up Information não mapeado para andamento do robô, mensagem {captured_text}",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
        else:
            console.print(f"Aba Information não encontrada")
            try:
                nota_incluida = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\entrada_notas\\nota_fiscal_incluida.png", confidence=0.7
                )
                if nota_incluida:
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno=f"Nota incluida com sucesso",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro ao lançar nota",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
            except Exception as e:
                console.print(f"Error: {e}")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                )
    except Exception as e:
        console.print(f"Erro ao conectar à janela Information para obter retorno de status de inclusão da nota: {e}\n")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def kill_all_emsys():
    try:
        await kill_process("EMSysFiscal")
        await kill_process("EMSys")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"EMSys encerrado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao fechar o emsys, erro{e}",
            status=RpaHistoricoStatusEnum.Falha,
        )