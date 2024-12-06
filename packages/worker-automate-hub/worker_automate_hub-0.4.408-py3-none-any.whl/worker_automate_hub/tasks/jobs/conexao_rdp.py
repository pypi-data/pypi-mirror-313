import asyncio
import os
import subprocess
import time

import pyautogui
import pygetwindow._pygetwindow_win as gw
from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import RpaProcessoEntradaDTO
from pygetwindow._pygetwindow_win import Win32Window
from rich.console import Console

from worker_automate_hub.utils.logger import logger

console = Console()


def tirar_screenshot(nome_etapa: str):
    """
    Tira um screenshot da tela atual e salva em um arquivo com o nome
    especificado e a data/hora atual.

    :param nome_etapa: nome da etapa que est  sendo executada
    :type nome_etapa: str
    :return: caminho do arquivo de screenshot gerado
    :rtype: str
    """
    if nome_etapa is None:
        raise ValueError("Nome da etapa não pode ser nulo")

    caminho_screenshot = f"{nome_etapa}_{int(time.time())}.png"
    try:
        pyautogui.screenshot(caminho_screenshot)
        console.print(f"Screenshot tirada: {caminho_screenshot}")
        return caminho_screenshot

    except Exception as e:
        console.print(f"Erro ao tirar screenshot: {e}")
        return None


def deletar_screenshots(caminhos_screenshots: str):
    """
    Recebe uma lista de caminhos de arquivos de screenshots e deleta cada um deles.

    :param caminhos_screenshots: lista de caminhos de arquivos de screenshots
    :type caminhos_screenshots: list[str]
    """
    if caminhos_screenshots is None:
        raise ValueError("Lista de caminhos de screenshots não pode ser nula")

    for caminho in caminhos_screenshots:
        if caminho is None:
            raise ValueError("Caminho de screenshot não pode ser nulo")

        try:
            os.remove(caminho)
            console.print(f"Screenshot deletada: {caminho}")
        except OSError as e:
            console.print(f"Erro ao deletar screenshot {caminho}: {e}")


def fechar_janelas_rdp_sem_ip():
    """
    Fecha as janelas de conex o RDP sem IP.

    Caso não tenha nenhuma conexão RDP aberta, não fará  nada.
    """
    janelas_rdp = [
        win
        for win in gw.getAllTitles()
        if "Conexão de  Área de Trabalho Remota" in win
        or "Remote Desktop Connection" in win
    ]
    for titulo in janelas_rdp:
        if not any(char.isdigit() for char in titulo):
            console.print(f"Fechando pop-up de conexão sem IP: {titulo}")
            janela: Win32Window = gw.getWindowsWithTitle(titulo)[0]
            if janela is None:
                raise RuntimeError(f"Janela {titulo} não existe")
            try:
                janela.close()
            except Exception as e:
                logger.error(f"Erro ao fechar janela {titulo}: {e}")
            time.sleep(2)


def fechar_janela_existente(ip: str):
    """
    Fecha a janela existente com o IP informado.

    Args:
        ip (str): IP da janela a ser fechada.

    Raises:
        Exception: Erro ao tentar fechar a janela.
    """
    try:
        janelas_encontradas = gw.getAllTitles()
        for titulo in janelas_encontradas:
            if ip in titulo:
                janela: Win32Window = gw.getWindowsWithTitle(titulo)[0]
                if janela is None:
                    raise RuntimeError(f"Janela {titulo} não existe")
                console.print(f"Fechando janela existente: {titulo}")
                janela.activate()
                pyautogui.hotkey("alt", "f4")
                time.sleep(1)
                break
        else:
            console.print(f"Nenhuma janela encontrada com o IP: {ip}")

        fechar_janelas_rdp_sem_ip()

    except Exception as e:
        console.print(f"Erro ao tentar fechar a janela: {e}", style="bold red")


def restaurar_janelas_rdp():
    """
    Função para restaurar todas as janelas de Conexão de área de Trabalho Remota
    que estão minimizadas e mover elas para uma posicão na tela.
    """
    janelas_rdp = [
        win
        for win in gw.getAllTitles()
        if "Conexão de Área de Trabalho Remota" in win
        or "Remote Desktop Connection" in win
    ]

    offset_x = 0
    offset_y = 0
    step_x = 30
    step_y = 30

    for titulo in janelas_rdp:
        janela: Win32Window = gw.getWindowsWithTitle(titulo)[0]
        if janela is None:
            console.print(
                f"Erro ao restaurar janela {titulo}: janela não existe",
                style="bold red",
            )
            continue

        console.print(f"Processando janela: {titulo}")
        if janela.isMinimized:
            try:
                janela.restore()
            except Exception as e:
                console.print(
                    f"Erro ao restaurar janela {titulo}: {e}", style="bold red"
                )
            else:
                console.print(f"Janela restaurada: {titulo}")
        else:
            console.print(f"Janela já está aberta: {titulo}")

        try:
            janela.moveTo(offset_x, offset_y)
        except Exception as e:
            console.print(f"Erro ao mover janela {titulo}: {e}", style="bold red")
        else:
            offset_x += step_x
            offset_y += step_y

        try:
            janela.activate()
        except Exception as e:
            console.print(f"Erro ao ativar janela {titulo}: {e}", style="bold red")
        time.sleep(2)


def redimensionar_janela_rdp(largura: int, altura: int):
    """
    Redimensiona a janela da Conexão de Área de Trabalho Remota.

    :param largura: Largura da janela em pixels
    :type largura: int
    :param altura: Altura da janela em pixels
    :type altura: int
    """
    janelas_rdp = [
        win
        for win in gw.getAllTitles()
        if "Conexão de Área de Trabalho Remota" in win
        or "Remote Desktop Connection" in win
    ]

    if janelas_rdp:
        try:
            janela_rdp: Win32Window = gw.getWindowsWithTitle(janelas_rdp[0])[0]
            if janela_rdp is None:
                raise RuntimeError("Janela RDP não existe")
            janela_rdp.resizeTo(largura, altura)
            janela_rdp.moveTo(20, 20)
            console.print(f"Janela redimensionada para {largura}x{altura}.")
            janela_rdp.activate()
            janela_rdp.restore()
            time.sleep(1)
        except Exception as e:
            console.print(f"Erro ao redimensionar janela RDP: {e}", style="bold red")
    else:
        console.print("Não foi possível encontrar a janela RDP para redimensionar.")


async def conexao_rdp(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:

    caminhos_screenshots = []
    try:
        if not task or not task.configEntrada:
            raise ValueError("Task inválida ou sem configurações de entrada.")

        ip = task.configEntrada.get("ip", "")
        user = task.configEntrada.get("user", "")
        password = task.configEntrada.get("password", "")

        if not ip or not user or not password:
            raise ValueError(
                "Configurações de entrada inválidas. Verifique se o IP, Usuário e Senha estão preenchidos."
            )

        pyautogui.hotkey("win", "d")
        console.print("1 - Minimizando todas as telas...")
        await asyncio.sleep(2)

        fechar_janela_existente(ip)

        subprocess.Popen("mstsc")
        console.print("2 - Abrindo conexão de trabalho remota...")
        await asyncio.sleep(2)

        redimensionar_janela_rdp(500, 500)

        await asyncio.sleep(2)

        janelas_rdp = [
            win
            for win in gw.getAllTitles()
            if "Conexão de Área de Trabalho Remota" in win
            or "Remote Desktop Connection" in win
        ]
        if not janelas_rdp:
            raise RuntimeError("Nenhuma janela RDP foi encontrada.")

        janela_rdp: Win32Window = gw.getWindowsWithTitle(janelas_rdp[0])[0]
        if janela_rdp is None:
            raise RuntimeError("Janela RDP não existe.")

        janela_rdp.activate()
        janela_rdp.restore()
        await asyncio.sleep(1)

        caminhos_screenshots.append(tirar_screenshot("antes_de_inserir_ip"))
        console.print("3 - Inserindo o IP...")
        pyautogui.write(ip)
        await asyncio.sleep(10)
        caminhos_screenshots.append(tirar_screenshot("depois_de_inserir_ip"))
        pyautogui.press("enter")
        await asyncio.sleep(5)
        caminhos_screenshots.append(tirar_screenshot("depois_de_inserir_usuario"))
        await asyncio.sleep(5)

        console.print("5 - Inserindo a Senha...")
        pyautogui.write(password)
        pyautogui.press("enter")
        await asyncio.sleep(10)
        caminhos_screenshots.append(tirar_screenshot("depois_de_inserir_senha"))

        console.print("6 - Apertando left...")
        pyautogui.press("left")
        await asyncio.sleep(2)
        console.print("7 - Apertando Enter...")
        pyautogui.press("enter")
        await asyncio.sleep(20)
        caminhos_screenshots.append(tirar_screenshot("depois_do_certificado"))

        console.print("8 - Minimizando todas as telas no final...")
        pyautogui.hotkey("win", "d")
        await asyncio.sleep(2)
        caminhos_screenshots.append(tirar_screenshot("depois_de_minimizar_todas"))

        restaurar_janelas_rdp()
        caminhos_screenshots.append(tirar_screenshot("depois_de_restaurar_janelas"))

        deletar_screenshots(caminhos_screenshots)

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Processo de conexão ao RDP executado com sucesso.",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as ex:
        err_msg = f"Erro ao executar conexao_rdp: {ex}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")
        caminhos_screenshots.append(tirar_screenshot("erro"))
        deletar_screenshots(caminhos_screenshots)
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=err_msg,
            status=RpaHistoricoStatusEnum.Falha,
        )
