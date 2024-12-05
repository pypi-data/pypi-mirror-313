import logging
from typing import Any, Sequence

from sqlalchemy import Row, create_engine, text
from sqlalchemy.orm import sessionmaker

from vlcishared.utils.interfaces import ConnectionInterface


class OracleConnector(ConnectionInterface):

    def __init__(self,
                 host: str,
                 port: str,
                 sid: str,
                 user: str,
                 password: str):

        self.log = logging.getLogger()
        self.engine = None
        self.Session = None
        self.session = None
        self.connection_string =\
            f"oracle+oracledb://{user}:{password}@{host}:{port}/{sid}"

    def connect(self):
        """Función que se conecta a la base de datos
        definida en el constructor"""
        try:
            self.engine = create_engine(self.connection_string)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            self.log.info('Conexión a Oracle exitosa')
        except Exception as e:
            self.log.error(f"Error al conectar a la base de datos: {e}")
            raise e

    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()

    def call_procedure(
            self,
            procedure_name: str,
            *params: Any,
            is_function: bool = False) -> Sequence[Row[Any]]:
        """Llama a funciones o procedimientos almacenados en BD,
        recibe el nombre y los parámetros"""
        try:
            param_placeholders = ', '.join(
                [f':p{i}' for i in range(len(params))])
            param_dict = {f'p{i}': params[i] for i in range(len(params))}
            if is_function:
                sql = text(
                    f'SELECT {procedure_name}({param_placeholders}) FROM dual')
                result = self.session.execute(sql, param_dict)
                self.session.commit()
                return result.fetchall()
            else:
                sql = text(f'BEGIN {procedure_name}({param_placeholders}); END;')
                self.session.execute(sql, param_dict)
                self.session.commit()
                return []
        except Exception as e:
            self.session.rollback()
            self.log.error(f"Fallo llamando a {procedure_name}: {e}")
            raise e
