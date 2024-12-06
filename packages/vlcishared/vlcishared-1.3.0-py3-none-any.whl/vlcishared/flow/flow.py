import logging
import sys
import traceback

from vlcishared.mail.mail import Email

FAILED_EXEC = 1
SUCCESS_EXEC = 0


class FlowControl:
    '''Clase que implementa métodos que se usan para controlar
    el flujo de la ETL, por ejemplo para terminar la ejecución,
    para permitir que continue pero que envie un correo al final
    o para indicar que la ejecución ha sido exitosa'''

    flow_state = None

    def __init__(self, mail: Email = None) -> None:
        self.flow_state = SUCCESS_EXEC
        self.log = logging.getLogger()
        self.mail = mail

    def handle_error(self, cause: str, fatal: bool = False) -> None:
        '''Logea el error recibido, lo añade al correo que se va a enviar y
        si es un error fatal termina la ejecución de la ETL'''
        self.flow_state = FAILED_EXEC
        self.log.error(cause)
        self.log.error(f'Excepción: {traceback.format_exc(limit=1)}')

        if self.mail is not None:
            self.mail.append_line('Ejecución Fallida: ETL KO.')
            self.mail.append_line(f'Causa del fallo: {cause}')

        if fatal:
            self.end_exec()

    def end_exec(self):
        '''Termina la ejecución de la ETL retornando 1 en caso de fallo y 0
        en caso se exito'''
        if self.flow_state == FAILED_EXEC:
            self.log.info('Ejecución Fallida, ETL KO')
            if self.mail is not None:
                self.mail.append_line('Se adjuntan logs de la ejecución.')
                self.mail.add_attachment(
                    self.log.handlers[0].baseFilename, 'text/plain')
                self.mail.send()
        else:
            self.log.info('Ejecución Exitosa, ETL OK')

        return sys.exit(self.flow_state)
