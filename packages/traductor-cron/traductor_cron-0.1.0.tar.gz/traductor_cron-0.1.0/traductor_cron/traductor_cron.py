import re
from typing import List, Optional
import logging
from datetime import datetime
from croniter import croniter

class CronTranslator:
    """
    Traductor de expresiones cron al español con traducciones más naturales.
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
    
    def _parse_minutes(self, value: str) -> str:
        """Parsea el campo de minutos."""
        if value == '*':
            return ''
        if value == '*/5':
            return 'cada 5 minutos'
        if ',' in value:
            return f'en los minutos {value}'
        if '/' in value:
            _, intervalo = value.split('/')
            return f'cada {intervalo} minutos'
        return f'en el minuto {value}'
    
    def _parse_hours(self, value: str) -> str:
        """Parsea el campo de horas."""
        if value == '*':
            return ''
        if value == '*/2':
            return 'cada 2 horas'
        if ',' in value:
            return f'a las {value.replace(",", " y")} horas'
        return f'a las {value} horas'
    
    def _parse_days_of_month(self, value: str) -> str:
        """Parsea los días del mes."""
        if value == '*':
            return 'todos los días'
        if value == 'L':
            return 'el último día del mes'
        if ',' in value:
            return f'los días {value}'
        return f'el día {value}'
    
    def _parse_months(self, value: str) -> str:
        """Parsea los meses."""
        if value == '*':
            return 'todos los meses'
        if value == '*/2':
            return 'cada dos meses'
        if ',' in value:
            return f'en {", ".join(self._MONTH_NAMES[int(m)-1] for m in value.split(","))}'
        if '-' in value:
            inicio, fin = map(int, value.split('-'))
            return f'de {self._MONTH_NAMES[inicio-1]} a {self._MONTH_NAMES[fin-1]}'
        try:
            return f'en {self._MONTH_NAMES[int(value)-1]}'
        except (ValueError, IndexError):
            return f'en el mes {value}'
    
    def _parse_days_of_week(self, value: str) -> str:
        """Parsea los días de la semana."""
        if value == '*':
            return 'todos los días'
        if value == '1-5':
            return 'en días laborables'
        if ',' in value:
            return f'los {", ".join(self._DAY_NAMES[int(d)] for d in value.split(","))}'
        if '-' in value:
            inicio, fin = map(int, value.split('-'))
            return f'de {self._DAY_NAMES[inicio]} a {self._DAY_NAMES[fin]}'
        try:
            return f'los {self._DAY_NAMES[int(value)]}'
        except (ValueError, IndexError):
            return f'en el día {value}'
    
    def translate(self, cron_expression: str) -> str:
        """
        Traduce una expresión cron completa a español.
        
        :param cron_expression: Expresión cron estándar
        :return: Descripción en español de la ejecución
        """
        # Completar la expresión con comodines si es necesario
        partes = cron_expression.split()
        while len(partes) < 5:
            partes.append('*')
        
        if not self._validate_cron_expression(' '.join(partes)):
            raise ValueError(f"Expresión cron inválida: {cron_expression}")
        
        minute, hour, day_of_month, month, day_of_week = partes
        
        # Construir la traducción de manera más natural
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
            traduccion_partes.append(dias_semana)
        
        # Unir las partes de manera coherente
        traduccion = ' '.join(traduccion_partes)
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
        '*/5 * * * *',           # Cada 5 minutos
        '0 2 * * 1-5',            # 2 AM en días laborables
        '0 0 1 */2 *',            # Primer día de cada dos meses
        '30 3 15 * *',            # Día 15 de cada mes a las 3:30 AM
        '0 12 * * 1,3,5',         # Mediodía en lunes, miércoles y viernes
    ]
    
    for expression in cron_expressions:
        try:
            print(f"\nExpresión: {expression}")
            print("Traducción:", translator.translate(expression))
            print("Próximas ejecuciones:")
            for exec_time in translator.get_next_executions(expression):
                print(f"  - {exec_time}")
        except Exception as e:
            print(f"Error procesando {expression}: {e}")

if __name__ == "__main__":
    main()