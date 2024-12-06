import aiohttp

from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.models.dao.rpa_historico import RpaHistorico
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoRequestDTO,
)
from worker_automate_hub.utils.logger import logger


async def store(data: RpaHistoricoRequestDTO) -> dict:
    """
    Armazena o histórico de um processo com status Processando.

    Recebe um RpaHistoricoRequestDTO como parâmetro e salva o
    histórico com status Processando. Retorna um dicionário com o uuid do
    histórico salvo.

    Args:
        data (RpaHistoricoRequestDTO): O histórico a ser salvo.

    Returns:
        RpaHistorico: Dicionário com o uuid do histórico salvo.
    """
    env_config, _ = load_env_config()

    if not data:
        raise ValueError("Parâmetro data deve ser informado")

    if not isinstance(data, RpaHistoricoRequestDTO):
        raise TypeError("Parâmetro data deve ser do tipo RpaHistoricoRequestDTO")

    headers_basic = {
        "Authorization": f"Basic {env_config["API_AUTHORIZATION"]}",
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            payload = data.model_dump_json()

            async with session.post(
                f"{env_config["API_BASE_URL"]}/historico",
                data=payload,
                headers=headers_basic,
            ) as response:
                response_text = await response.text()
                logger.info(f"Resposta store: {response_text}")

                if response.status == 200:
                    try:
                        response_data = await response.json()
                        return RpaHistorico(**response_data)
                    except aiohttp.ContentTypeError:
                        return {
                            "error": "Resposta não é JSON",
                            "status_code": response.status,
                        }
                else:
                    return {"error": response_text, "status_code": response.status}
    except aiohttp.ClientError as e:
        logger.error(f"Erro de cliente aiohttp: {str(e)}")
        return {"error": str(e), "status_code": 500}
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {"error": str(e), "status_code": 500}


async def update(data: RpaHistoricoRequestDTO) -> dict:
    """
    Atualiza um registro de histórico com base no uuidHistorico informado.

    Args:
        data (RpaHistoricoRequestDTO): Os dados do histórico a ser atualizado.

    Returns:
        RpaHistorico: O histórico atualizado.
    """
    env_config, _ = load_env_config()
    headers_basic = {
        "Authorization": f"Basic {env_config["API_AUTHORIZATION"]}",
        "Content-Type": "application/json",
    }
    if not data or not isinstance(data, RpaHistoricoRequestDTO):
        raise TypeError("Parâmetro data deve ser do tipo RpaHistoricoRequestDTO")
    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            if not data.uuidHistorico:
                raise ValueError("Parâmetro uuidHistorico deve ser informado")

            payload = data.model_dump_json()

            async with session.put(
                f"{env_config["API_BASE_URL"]}/historico",
                data=payload,
                headers=headers_basic,
            ) as response:
                response_text = await response.text()
                logger.info(f"Resposta update: {response_text}")

                if response.status == 200:
                    try:
                        response_data = await response.json()
                        return RpaHistorico(**response_data)
                    except aiohttp.ContentTypeError:
                        return {
                            "error": "Resposta não é JSON",
                            "status_code": response.status,
                        }
                else:
                    return {"error": response_text, "status_code": response.status}
    except aiohttp.ClientError as e:
        logger.error(f"Erro de cliente aiohttp: {str(e)}")
        return {"error": str(e), "status_code": 500}
    except ValueError as e:
        logger.error(f"Erro de valor: {str(e)}")
        return {"error": str(e), "status_code": 400}
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {"error": str(e), "status_code": 500}
