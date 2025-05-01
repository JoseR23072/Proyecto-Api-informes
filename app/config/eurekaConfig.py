from py_eureka_client import eureka_client
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

async def iniciar_eureka() -> None:
    """
    Inicializa y registra esta instancia FastAPI en el servidor Eureka.
    """
    try:
        await eureka_client.init_async(
            eureka_server=settings.EUREKA_SERVER,
            app_name=settings.EUREKA_APP_NAME,
            instance_port=settings.INSTANCE_PORT,
            instance_ip=settings.INSTANCE_IP,
            health_check_url=(
                f"http://{settings.INSTANCE_IP}:"
                f"{settings.INSTANCE_PORT}{settings.HEALTH_CHECK_PATH}"
            ),
            status_page_url=(
                f"http://{settings.INSTANCE_IP}:"
                f"{settings.INSTANCE_PORT}{settings.STATUS_PAGE_PATH}"
            ),
            prefer_same_zone=True,
        )
        logger.info("Registrado correctamente en Eureka: %s", settings.EUREKA_APP_NAME)
    except Exception as exc:
        logger.error("Error al inicializar cliente Eureka: %s", exc)
        
