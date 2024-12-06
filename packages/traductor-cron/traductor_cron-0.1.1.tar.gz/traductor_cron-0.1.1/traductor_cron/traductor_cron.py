import re
from typing import List, Optional
import logging
from datetime import datetime
from croniter import croniter

class CronTranslator:
    """
    Traductor de expresiones cron al español con traducciones concisas.
    """
    
    _MONTH_NAMES = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    _DAY_NAMES = [
        'domingo', 'lunes', 'martes', 'miércoles', 
        'jueves', 'viernes', 'sábado'
    ]
    
    def __init__(self, log_level: int = logging.INFO):
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _validate_cron_expression(self, expression: str) -> bool:
        """Valida la sintaxis de la expresión cron."""
        try:
            croniter(expression)
            return True
        except (ValueError, TypeError):
            return False
    
    def _parse_minutes(self, value: str) -> Optional[str]:
        """Parsea el campo de minutos."""
        if value == '*':
            return "Cada minuto"
        if value.startswith('*/'):
            intervalo = value.split('/')[1]
            return f'Cada {intervalo} minutos'
        if ',' in value:
            return f'En los minutos {value}'
        if '-' in value:
            inicio, fin = value.split('-')
            return f'De los minutos {inicio} a {fin}'
        return f'En el minuto {value}'

    def _parse_hours(self, value: str) -> Optional[str]:
        """Parsea el campo de horas."""
        if value == '*':
            return None
        if value.startswith('*/'):
            intervalo = value.split('/')[1]
            return f'Cada {intervalo} horas'
        if ',' in value:
            return f'A las {value} horas'
        if '-' in value:
            inicio, fin = value.split('-')
            return f'De las {inicio} a las {fin} horas'
        return f'A las {value} horas'

    def _parse_days_of_month(self, value: str) -> Optional[str]:
        """Parsea los días del mes."""
        if value == '*':
            return None
        if value == 'L':
            return 'El último día del mes'
        if value.startswith('*/'):
            intervalo = value.split('/')[1]
            return f'Cada {intervalo} días del mes'
        if ',' in value:
            return f'Los días {value.replace(",", ", ")}'
        if '-' in value:
            inicio, fin = value.split('-')
            return f'Del día {inicio} al {fin}'
        return f'El día {value}'

    def _parse_months(self, value: str) -> Optional[str]:
        """Parsea los meses."""
        if value == '*':
            return None
        if value.startswith('*/'):
            intervalo = value.split('/')[1]
            return f'Cada {intervalo} meses'
        if ',' in value:
            return f'En {", ".join(self._MONTH_NAMES[int(m)-1] for m in value.split(","))}'
        if '-' in value:
            inicio, fin = map(int, value.split('-'))
            return f'De {self._MONTH_NAMES[inicio-1]} a {self._MONTH_NAMES[fin-1]}'
        try:
            return f'En {self._MONTH_NAMES[int(value)-1]}'
        except (ValueError, IndexError):
            return f'En el mes {value}'

    def _parse_days_of_week(self, value: str) -> Optional[str]:
        """Parsea los días de la semana separados por comas."""
        if value == '*':
            return None
        if value.startswith('*/'):
            intervalo = value.split('/')[1]
            return f'Cada {intervalo} días de la semana'
        if ',' in value:
            return ','.join(self._DAY_NAMES[int(d)] for d in value.split(','))
        if '-' in value:
            if "1-5" == value:
                return 'días laborales'
            inicio, fin = map(int, value.split('-'))
            return f'{self._DAY_NAMES[inicio]}-{self._DAY_NAMES[fin]}'
        try:
            return self._DAY_NAMES[int(value)]
        except (ValueError, IndexError):
            return f'En el día {value}'

    def translate(self, cron_expression: str) -> str:
        """
        Traduce una expresión cron completa a español de manera robusta y compacta.
        """
        partes = cron_expression.split()
        while len(partes) < 5:
            partes.append('*')
        
        if not self._validate_cron_expression(' '.join(partes)):
            raise ValueError(f"Expresión cron inválida: {cron_expression}")
        
        minute, hour, day_of_month, month, day_of_week = partes
        traduccion_partes = []
        
        # Minutos
        minutos = self._parse_minutes(minute)
        if minutos:
            traduccion_partes.append(minutos)
        
        # Horas
        horas = self._parse_hours(hour)
        if horas:
            traduccion_partes.append(horas)
        
        # Días del mes
        dias_mes = self._parse_days_of_month(day_of_month)
        if dias_mes:
            traduccion_partes.append(dias_mes)
        
        # Meses
        meses = self._parse_months(month)
        if meses:
            traduccion_partes.append(meses)

        # Días de la semana
        dias_semana = self._parse_days_of_week(day_of_week)
        if dias_semana:
            if "-" in dias_semana:
                traduccion_partes.append(f'de {dias_semana}')
            elif "," in dias_semana or "laborales in dias_semana":
                traduccion_partes.append(f'los {dias_semana}')
            else:
                traduccion_partes.append(f'el {dias_semana}')

        traduccion = ', '.join(traduccion_partes)
        traduccion = traduccion.replace(' ,', ',')
        traduccion = re.sub(r'\s+y', ' y', traduccion)

        return traduccion.capitalize() if traduccion else 'Sin programación específica'

    
    def get_next_executions(self, cron_expression: str, count: int = 5) -> List[datetime]:
        """Calcula las próximas ejecuciones de una expresión cron."""
        try:
            # Completar la expresión con comodines si es necesario
            partes = cron_expression.split()
            while len(partes) < 5:
                partes.append('*')
            
            base = datetime.now()
            cron = croniter(' '.join(partes), base)
            return [cron.get_next(datetime) for _ in range(count)]
        except Exception as e:
            self.logger.error(f"Error calculando próximas ejecuciones: {e}")
            return []

def main():
    """Función de demostración"""
    translator = CronTranslator()
    
    cron_expressions = [
        '*/5 * * * *',               # Cada 5 minutos
        '* 2 * * 1-5',               # 2 AM en días laborables
        '0 */4 * * *',               # Cada 4 horas
        '30 12 15 * *',              # 12:30 PM el día 15 de cada mes
        '0 0 1 */2 *',               # Medianoche del primer día de cada dos meses
        '15,30 15,16 * * 1,3,5',     # 15 y 30 minutos, 3 y 4 PM, lunes, miércoles, viernes
        '0 0 1-5 6-8 *',             # Medianoche del 1 al 5 de junio a agosto
        '*/10 9-17 * * 1-5',         # Cada 10 minutos entre las 9 y 5 en días laborables
        '0 6 1 1 *',                 # 6 AM el 1 de enero
        '45 23 * * 0',               # 11:45 PM todos los domingos
        '*/15 */6 * 3 0',            # Cada 15 minutos, cada 6 horas, en marzo, domingos
        '0 8 10 4 2',                # 8 AM el 10 de abril, martes
        '0 0 L * *',                 # Medianoche el último día de cada mes
        '0 0 1 12 *',                # Medianoche el 1 de diciembre
        '0 0 * */3 6',               # Medianoche todos los sábados, cada tres meses
        '0 11,12 * * 1-5'            # 11:00 y 12:00 en días laborales
    ]

    
    for expression in cron_expressions:
        try:
            print(f"\nExpresión: {expression}")
            print("Traducción:", translator.translate(expression))
            print()
            # print("Próximas ejecuciones:")
            # for exec_time in translator.get_next_executions(expression):
            #     print(f"  - {exec_time}")
        except Exception as e:
            print(f"Error procesando {expression}: {e}")

if __name__ == "__main__":
    main()