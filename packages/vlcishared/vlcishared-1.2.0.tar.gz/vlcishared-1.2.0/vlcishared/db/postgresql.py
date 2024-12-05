import logging
from typing import Any, Sequence

from sqlalchemy import Engine, Row, TextClause, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from vlcishared.utils.interfaces import ConnectionInterface


class PostgresConnector(ConnectionInterface):

    def __init__(self,
                 host: str,
                 port: str,
                 database: str,
                 user: str,
                 password: str):

        self.log = logging.getLogger()
        self.engine: Engine
        self.session_maker: sessionmaker
        self.session: Session
        self.db_name = database
        self.connection_string =\
            f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def connect(self):
        """Función que se conecta a la base de datos
        definida en el constructor"""
        self.engine = create_engine(self.connection_string)
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = self.session_maker()
        self.log.info(f'Conectado a {self.db_name}')

    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        self.log.info(f'Desconectado de {self.db_name}.')

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
                    f'SELECT {procedure_name}({param_placeholders})')
                result = self.session.execute(sql, param_dict)
                self.session.commit()
                return result.fetchall()
            else:
                sql = text(f'CALL {procedure_name}({param_placeholders})')
                self.session.execute(sql, param_dict)
                self.session.commit()
                return []
        except Exception as e:
            self.session.rollback()
            self.log.error(f"Fallo llamando a {procedure_name}: {e}")
            raise e

    def execute(self, query: TextClause, params: dict):
        with self.engine.connect() as conn:
            result = conn.execute(query, params)
            conn.commit()
        return result
