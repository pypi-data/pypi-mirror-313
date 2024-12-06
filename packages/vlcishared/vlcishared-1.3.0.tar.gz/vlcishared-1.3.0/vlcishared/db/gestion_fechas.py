import logging
from typing import Optional

from vlcishared.db.postgresql import PostgresConnector


class GestionFechas:

    def __init__(self, db_connector: PostgresConnector):
        self.db_connector = db_connector
        self.log = logging.getLogger()

    def gestion_fechas_inicio(
            self,
            identifier: str,
            param: str
    ) -> Optional[str]:
        """
        Gestión de fechas inicio: Se averigua la fecha, se obtiene y
        se registra el estado a 'En Proceso'
        """
        try:
            result = self.db_connector.call_procedure(
                'p_gf_averiguarejecucion',
                identifier,
                is_function=True
            )
            if result[0][1] == "f":
                return result[0]
            else:
                date_result = self.db_connector.call_procedure(
                    'p_gf_obtenerfecha',
                    identifier,
                    param,
                    is_function=True
                )
                self.db_connector.call_procedure(
                    'p_gf_registrarestadoetl',
                    identifier,
                    'EN PROCESO',
                    is_function=True
                )
                self.log.info("Gestión de fechas inicio completada.")
                return date_result[0][0]
        except Exception as e:
            self.log.error(f"Error en gestión de fechas inicio: {e}")
            raise e

    def gestion_fechas_fin(
            self,
            identifier: str,
            param: str,
            status: str
    ) -> Optional[str]:
        """Gestión de fechas fin: Se registra el estado a 'OK' o 'ERROR',
            se calcula la nueva fecha y se actualiza"""
        try:
            self.db_connector.call_procedure(
                'p_gf_registrarestadoetl',
                identifier,
                status,
                is_function=True
            )
            result = self.db_connector.call_procedure(
                'p_gf_calcularNuevaFecha',
                identifier,
                is_function=True
            )

            self.log.info("Gestión de fechas fin completada.")
            return result[0][0]
        except Exception as e:
            self.log.error(f"Error en gestión de fechas fin: {e}")
            raise e
