#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTROL DE HORARIOS COMERCIALES - DESARROYO TECH
Sistema que controla automáticamente cuándo hacer llamadas:
- LUNES-VIERNES: 9:00-14:00 y 16:00-20:00
- SÁBADOS: 10:00-13:00 (horario suave)
- DOMINGOS: PARADO
"""

import os
import sys
from datetime import datetime, time
import json

class ControlHorarios:
    def __init__(self):
        self.horarios_comerciales = {
            # Lunes a Viernes (0-4)
            'laborables': {
                'manana': {'inicio': time(9, 0), 'fin': time(14, 0)},
                'tarde': {'inicio': time(16, 0), 'fin': time(20, 0)}
            },
            # Sábado (5) - horario suave
            'sabado': {
                'manana': {'inicio': time(10, 0), 'fin': time(13, 0)}
            },
            # Domingo (6) - CERRADO
            'domingo': None
        }
        
    def esta_en_horario_comercial(self):
        """
        Verifica si AHORA MISMO estamos en horario comercial
        Returns: (bool, str) - (en_horario, razon)
        """
        now = datetime.now()
        hora_actual = now.time()
        dia_semana = now.weekday()  # 0=lunes, 6=domingo
        
        # DOMINGO - Cerrado
        if dia_semana == 6:
            return False, "DOMINGO: Sistema cerrado"
        
        # SÁBADO - Horario reducido
        elif dia_semana == 5:
            sabado = self.horarios_comerciales['sabado']
            if (sabado['manana']['inicio'] <= hora_actual <= sabado['manana']['fin']):
                return True, f"SÁBADO: Horario comercial (10:00-13:00)"
            else:
                return False, f"SÁBADO: Fuera de horario (10:00-13:00)"
        
        # LUNES-VIERNES - Horario completo  
        else:
            laborables = self.horarios_comerciales['laborables']
            
            # Horario de mañana (9:00-14:00)
            if (laborables['manana']['inicio'] <= hora_actual <= laborables['manana']['fin']):
                return True, f"LABORABLE: Horario mañana (9:00-14:00)"
            
            # Horario de tarde (16:00-20:00)
            elif (laborables['tarde']['inicio'] <= hora_actual <= laborables['tarde']['fin']):
                return True, f"LABORABLE: Horario tarde (16:00-20:00)"
            
            # Fuera de horario
            else:
                if hora_actual < laborables['manana']['inicio']:
                    return False, f"Muy temprano (abre a las 9:00)"
                elif laborables['manana']['fin'] < hora_actual < laborables['tarde']['inicio']:
                    return False, f"Horario de comida (reabre a las 16:00)"
                else:
                    return False, f"Muy tarde (cierra a las 20:00)"
    
    def tiempo_hasta_siguiente_apertura(self):
        """
        Calcula cuánto tiempo falta hasta la próxima apertura
        """
        now = datetime.now()
        dia_semana = now.weekday()
        hora_actual = now.time()
        
        # Si estamos en horario, no hay espera
        en_horario, _ = self.esta_en_horario_comercial()
        if en_horario:
            return 0, "Sistema ACTIVO ahora"
        
        # DOMINGO - próxima apertura el lunes 9:00
        if dia_semana == 6:
            dias_hasta_lunes = 1
            return dias_hasta_lunes, "Próxima apertura: LUNES 9:00"
        
        # SÁBADO fuera de horario - próxima apertura lunes 9:00
        elif dia_semana == 5:
            if hora_actual > time(13, 0):  # Después de las 13:00 del sábado
                return 2, "Próxima apertura: LUNES 9:00"
            else:  # Antes de las 10:00 del sábado
                return 0, "Próxima apertura: HOY 10:00"
        
        # LUNES-VIERNES
        else:
            laborables = self.horarios_comerciales['laborables']
            
            # Muy temprano - abre a las 9:00
            if hora_actual < laborables['manana']['inicio']:
                return 0, "Próxima apertura: HOY 9:00"
            
            # Horario comida - abre a las 16:00  
            elif laborables['manana']['fin'] < hora_actual < laborables['tarde']['inicio']:
                return 0, "Próxima apertura: HOY 16:00"
            
            # Muy tarde - abre mañana a las 9:00
            else:
                return 1, "Próxima apertura: MAÑANA 9:00"
    
    def obtener_estado_completo(self):
        """
        Obtiene estado completo del sistema de horarios
        """
        now = datetime.now()
        en_horario, razon = self.esta_en_horario_comercial()
        tiempo_espera, siguiente = self.tiempo_hasta_siguiente_apertura()
        
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        estado = {
            'timestamp': now.isoformat(),
            'hora_actual': now.strftime('%H:%M'),
            'dia_actual': dias[now.weekday()],
            'en_horario_comercial': en_horario,
            'razon_estado': razon,
            'siguiente_apertura': siguiente,
            'tiempo_espera_dias': tiempo_espera
        }
        
        return estado
    
    def verificar_y_reportar(self):
        """
        Verifica horario y genera reporte completo
        """
        estado = self.obtener_estado_completo()
        
        print("⏰ CONTROL DE HORARIOS COMERCIALES")
        print("=" * 50)
        print(f"🕐 Hora actual: {estado['hora_actual']} ({estado['dia_actual']})")
        
        if estado['en_horario_comercial']:
            print(f"✅ SISTEMA ACTIVO: {estado['razon_estado']}")
            print("🚀 Las llamadas pueden realizarse AHORA")
        else:
            print(f"❌ SISTEMA PARADO: {estado['razon_estado']}")
            print(f"⏳ {estado['siguiente_apertura']}")
            print("🚫 NO se realizarán llamadas hasta la próxima apertura")
        
        print("\n📋 HORARIOS CONFIGURADOS:")
        print("   🏢 Lunes-Viernes: 9:00-14:00 y 16:00-20:00")
        print("   🌅 Sábados: 10:00-13:00 (horario suave)")
        print("   🛌 Domingos: CERRADO")
        
        return estado['en_horario_comercial']

def verificar_horario_antes_de_llamar():
    """
    Función principal para verificar horario antes de cualquier campaña
    """
    control = ControlHorarios()
    return control.verificar_y_reportar()

def main():
    """Test del sistema de control de horarios"""
    print("🧪 TEST CONTROL DE HORARIOS")
    print("=" * 40)
    
    control = ControlHorarios()
    
    # Test con hora actual
    en_horario = control.verificar_y_reportar()
    
    print("\n" + "=" * 40)
    if en_horario:
        print("🎯 RESULTADO: Sistema LISTO para llamadas")
    else:
        print("⏸️ RESULTADO: Sistema PAUSADO hasta próxima apertura")
    
    # Mostrar estado detallado
    estado = control.obtener_estado_completo()
    print(f"\n📊 ESTADO DETALLADO:")
    for key, value in estado.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    main() 