import asyncio
import warnings
from datetime import datetime, timedelta

import pyperclip
import pyautogui
from pywinauto.application import Application
from rich.console import Console

from worker_automate_hub.utils.logger import logger
from pywinauto_recorder import set_combobox
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.util import (
    kill_process, 
    login_emsys, 
    type_text_into_field, 
    worker_sleep,
    set_variable,
    )

ASSETS_BASE_PATH = 'assets/fidc/'
console = Console()



async def remessa_cobranca_cnab240(task):
    '''
       Processo FIDC - Remessa de Cobrança CNAB240
    '''
    try:
        #Setando tempo de timeout
        multiplicador_timeout = int(float(task["sistemas"][0]["timeout"]))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        #Pega Config para logar no Emsys
        config = await get_config_by_name("login_emsys")
        #folders_paths = await get_config_by_name("Folders_Fidc")
        # console.print(task)
        # #Abre um novo emsys
        # await kill_process("EMSys")
        # app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        # warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        # console.print("\nEMSys iniciando...", style="bold green")
        # return_login = await login_emsys(config['conConfiguracao'], app, task)

        # if return_login['sucesso'] == True:
        #     type_text_into_field('Remessa de Cobrança', app['TFrmMenuPrincipal']['Edit'], True, '50')
        #     pyautogui.press('enter')
        #     await worker_sleep(1)
        #     pyautogui.press('enter')
        #     console.print(f"\nPesquisa: 'Impressao de Boletos' realizada com sucesso", style="bold green")
        # else:
        #     logger.info(f"\nError Message: {return_login["retorno"]}")
        #     console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
        #     return return_login
        
        # await worker_sleep(10)
        #Identificando jenela principal
        app = Application().connect(title="Gera Arquivo Cobranca", backend="uia")
        main_window_arquivo_cobranca = app["Gera Arquivo Cobranca"]

        #Digitando Cobrança
        # cobranca = main_window_arquivo_cobranca.child_window(class_name="TDBIEditCode", found_index=2)
        # console.print("Selecionando Cobrança", style='bold green')
        # cobranca.type_keys("4")
        # pyautogui.hotkey("tab")
        # await worker_sleep(5)
        # pyautogui.press("down", presses=3, interval=0.5)
        # pyautogui.hotkey("enter")
        
        #TODO passo 8 da IT


        # #Seleciona Banco
        # pyautogui.click(800, 395)
        # pyautogui.press("down", presses=2)
        # pyautogui.hotkey("enter")
        
        # Data atual
        data_atual = datetime.now()
        # Data(8 dias atrás)
        start_date = data_atual - timedelta(days=8)
        # Data(1 dia atrás)
        end_date = data_atual - timedelta(days=1)

        #Data de emissão
        pyautogui.click(690, 485)
        pyautogui.write(start_date.strftime("%d%m%Y"))
        pyautogui.click(780, 485)
        pyautogui.write(end_date.strftime("%d%m%Y"))

        print("")
    
    except Exception as ex:
        observacao = f"Erro Processo Remessa de Cobranca CNAB240: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}
    finally:
       ... # await kill_process("EMSys")


    

    



if __name__ == "__main__":
    task_fake = {
        "configEntrada":{
            "filialEmpresaOrigem": "1"
        },
        "sistemas": [
            {
            "sistema": "EMSys",
            "timeout": "1.0"
            },
            {
            "sistema": "AutoSystem",
            "timeout": "1.0"
            }
        ]
    }
    asyncio.run(remessa_cobranca_cnab240(task_fake))