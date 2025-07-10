#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTROL DE PRESUPUESTO AUTOMÁTICO - Sistema Híbrido DesArroyo Tech
Monitoreo en tiempo real de gastos SMS + Llamadas para mantenerse en 300-600€/mes
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

class ControlPresupuesto:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        self.presupuesto_mensual_max = 600  # €
        self.presupuesto_mensual_min = 300  # €
        self.presupuesto_diario_max = 20    # €
        
        # Costes por contacto
        self.coste_sms = 0.07
        self.coste_llamada = 0.12
        self.coste_llamada_sms = 0.19  # Llamada + SMS si acepta
        
        # Archivos de seguimiento
        self.archivo_gastos = Path("gastos_mensuales.json")
        self.archivo_estadisticas = Path("estadisticas_campanas.json")
        
    def cargar_gastos_mes_actual(self):
        """Carga gastos del mes actual"""
        mes_actual = datetime.now().strftime('%Y-%m')
        
        if self.archivo_gastos.exists():
            with open(self.archivo_gastos, 'r') as f:
                gastos = json.load(f)
                return gastos.get(mes_actual, {
                    'sms_enviados': 0,
                    'llamadas_realizadas': 0,
                    'sms_post_llamada': 0,
                    'coste_total': 0.0,
                    'dias_activos': []
                })
        return {
            'sms_enviados': 0,
            'llamadas_realizadas': 0,
            'sms_post_llamada': 0,
            'coste_total': 0.0,
            'dias_activos': []
        }
    
    def estimar_gastos_diarios(self):
        """Estima gastos diarios según configuración actual"""
        
        # SMS: cada 6h, 5 ciudades en paralelo
        sms_por_dia = 5 * 4  # 20 SMS por día
        coste_sms_diario = sms_por_dia * self.coste_sms
        
        # Llamadas: cada 12h, 3 ciudades, límite controlado
        llamadas_por_dia = 3 * 2 * 8  # 3 ciudades × 2 veces × 8 llamadas promedio = 48 llamadas
        coste_llamadas_diario = llamadas_por_dia * self.coste_llamada
        
        # SMS post-llamada (estimando 40% conversión)
        sms_post_llamada = llamadas_por_dia * 0.4
        coste_sms_post = sms_post_llamada * self.coste_sms
        
        coste_total_diario = coste_sms_diario + coste_llamadas_diario + coste_sms_post
        
        return {
            'sms_masivos': sms_por_dia,
            'coste_sms_masivos': coste_sms_diario,
            'llamadas': llamadas_por_dia,
            'coste_llamadas': coste_llamadas_diario,
            'sms_post_llamada': int(sms_post_llamada),
            'coste_sms_post': coste_sms_post,
            'coste_total_diario': coste_total_diario
        }
    
    def proyectar_gastos_mensuales(self):
        """Proyecta gastos para el mes completo"""
        gastos_diarios = self.estimar_gastos_diarios()
        dias_mes = 30
        
        proyeccion = {
            'sms_masivos_mes': gastos_diarios['sms_masivos'] * dias_mes,
            'llamadas_mes': gastos_diarios['llamadas'] * dias_mes,
            'sms_post_llamada_mes': gastos_diarios['sms_post_llamada'] * dias_mes,
            'coste_total_mes': gastos_diarios['coste_total_diario'] * dias_mes
        }
        
        return proyeccion
    
    def evaluar_rendimiento_canales(self):
        """Evalúa qué canal rinde mejor (ROI)"""
        
        # Estadísticas estimadas
        conversiones = {
            'sms_masivo': {
                'tasa_respuesta': 0.05,  # 5%
                'coste_por_contacto': self.coste_sms,
                'coste_por_conversion': self.coste_sms / 0.05
            },
            'llamadas_conversacionales': {
                'tasa_respuesta': 0.45,  # 45%
                'coste_por_contacto': self.coste_llamada_sms,
                'coste_por_conversion': self.coste_llamada_sms / 0.45
            }
        }
        
        # Calcular ROI (asumiendo Plan Escalable 449€)
        precio_venta = 449
        for canal in conversiones:
            coste_conversion = conversiones[canal]['coste_por_conversion']
            roi = (precio_venta - coste_conversion) / coste_conversion * 100
            conversiones[canal]['roi_porcentaje'] = roi
            conversiones[canal]['beneficio_neto'] = precio_venta - coste_conversion
        
        return conversiones
    
    def generar_reporte_completo(self):
        """Genera reporte completo de presupuesto y rendimiento"""
        gastos_actuales = self.cargar_gastos_mes_actual()
        gastos_diarios = self.estimar_gastos_diarios()
        proyeccion = self.proyectar_gastos_mensuales()
        rendimiento = self.evaluar_rendimiento_canales()
        
        # Calcular días restantes del mes
        hoy = datetime.now()
        ultimo_dia_mes = datetime(hoy.year, hoy.month + 1, 1) - timedelta(days=1)
        dias_restantes = (ultimo_dia_mes - hoy).days
        
        # Proyección gastos restantes
        gastos_restantes = gastos_diarios['coste_total_diario'] * dias_restantes
        total_mes_proyectado = gastos_actuales['coste_total'] + gastos_restantes
        
        # Estado del presupuesto
        if total_mes_proyectado <= self.presupuesto_mensual_max:
            estado_presupuesto = "✅ DENTRO DEL PRESUPUESTO"
            emoji_estado = "🟢"
        elif total_mes_proyectado <= self.presupuesto_mensual_max * 1.1:
            estado_presupuesto = "⚠️ CERCA DEL LÍMITE"
            emoji_estado = "🟡"
        else:
            estado_presupuesto = "❌ EXCEDE PRESUPUESTO"
            emoji_estado = "🔴"
        
        return {
            'gastos_actuales': gastos_actuales,
            'gastos_diarios': gastos_diarios,
            'proyeccion': proyeccion,
            'rendimiento': rendimiento,
            'dias_restantes': dias_restantes,
            'total_mes_proyectado': total_mes_proyectado,
            'estado_presupuesto': estado_presupuesto,
            'emoji_estado': emoji_estado
        }
    
    def enviar_reporte_telegram(self, reporte):
        """Envía reporte por Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            print("⚠️ Telegram no configurado")
            return
        
        # Formatear mensaje
        mensaje = f"""📊 **REPORTE PRESUPUESTO HÍBRIDO** {reporte['emoji_estado']}

💰 **ESTADO MENSUAL:**
• Gastado hasta hoy: {reporte['gastos_actuales']['coste_total']:.2f}€
• Proyección mes completo: {reporte['total_mes_proyectado']:.2f}€
• Presupuesto máximo: {self.presupuesto_mensual_max}€
• {reporte['estado_presupuesto']}

📈 **ESTADÍSTICAS ACTUALES:**
• SMS enviados: {reporte['gastos_actuales']['sms_enviados']}
• Llamadas realizadas: {reporte['gastos_actuales']['llamadas_realizadas']}
• SMS post-llamada: {reporte['gastos_actuales']['sms_post_llamada']}

📅 **PROYECCIÓN DIARIA:**
• SMS masivos: {reporte['gastos_diarios']['sms_masivos']} ({reporte['gastos_diarios']['coste_sms_masivos']:.2f}€)
• Llamadas: {reporte['gastos_diarios']['llamadas']} ({reporte['gastos_diarios']['coste_llamadas']:.2f}€)
• SMS post-llamada: {reporte['gastos_diarios']['sms_post_llamada']} ({reporte['gastos_diarios']['coste_sms_post']:.2f}€)
• **Total diario: {reporte['gastos_diarios']['coste_total_diario']:.2f}€**

🎯 **RENDIMIENTO CANALES:**
📱 SMS Masivo: {reporte['rendimiento']['sms_masivo']['tasa_respuesta']*100:.0f}% conversión | ROI: {reporte['rendimiento']['sms_masivo']['roi_porcentaje']:.0f}%
📞 Llamadas: {reporte['rendimiento']['llamadas_conversacionales']['tasa_respuesta']*100:.0f}% conversión | ROI: {reporte['rendimiento']['llamadas_conversacionales']['roi_porcentaje']:.0f}%

💡 **RECOMENDACIÓN:**
{'🔥 Llamadas más rentables' if reporte['rendimiento']['llamadas_conversacionales']['roi_porcentaje'] > reporte['rendimiento']['sms_masivo']['roi_porcentaje'] else '📱 SMS más económico'}

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}
🗓️ Días restantes mes: {reporte['dias_restantes']}"""

        try:
            response = requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': mensaje,
                    'parse_mode': 'Markdown'
                }
            )
            
            if response.status_code == 200:
                print("✅ Reporte enviado por Telegram")
            else:
                print(f"❌ Error enviando reporte: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error enviando Telegram: {str(e)}")
    
    def guardar_estadisticas(self, reporte):
        """Guarda estadísticas para análisis histórico"""
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        
        estadisticas = {
            'fecha': fecha_hoy,
            'coste_diario': reporte['gastos_diarios']['coste_total_diario'],
            'coste_mes_proyectado': reporte['total_mes_proyectado'],
            'dentro_presupuesto': reporte['total_mes_proyectado'] <= self.presupuesto_mensual_max,
            'roi_sms': reporte['rendimiento']['sms_masivo']['roi_porcentaje'],
            'roi_llamadas': reporte['rendimiento']['llamadas_conversacionales']['roi_porcentaje']
        }
        
        try:
            if self.archivo_estadisticas.exists():
                with open(self.archivo_estadisticas, 'r') as f:
                    datos = json.load(f)
            else:
                datos = []
            
            # Evitar duplicados del mismo día
            datos = [d for d in datos if d.get('fecha') != fecha_hoy]
            datos.append(estadisticas)
            
            # Mantener solo últimos 60 días
            if len(datos) > 60:
                datos = datos[-60:]
            
            with open(self.archivo_estadisticas, 'w') as f:
                json.dump(datos, f, indent=2)
                
            print(f"📊 Estadísticas guardadas: {fecha_hoy}")
            
        except Exception as e:
            print(f"❌ Error guardando estadísticas: {str(e)}")

def main():
    """Función principal"""
    print("📊 Iniciando control de presupuesto...")
    
    control = ControlPresupuesto()
    reporte = control.generar_reporte_completo()
    
    # Mostrar resumen en consola
    print(f"\n{reporte['estado_presupuesto']}")
    print(f"💰 Proyección mensual: {reporte['total_mes_proyectado']:.2f}€")
    print(f"📅 Coste diario: {reporte['gastos_diarios']['coste_total_diario']:.2f}€")
    
    # Enviar por Telegram
    control.enviar_reporte_telegram(reporte)
    
    # Guardar estadísticas
    control.guardar_estadisticas(reporte)
    
    print("✅ Control de presupuesto completado")

if __name__ == "__main__":
    main() 