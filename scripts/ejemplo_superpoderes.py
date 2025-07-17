#!/usr/bin/env python3
"""
🎬 Ejemplo de Uso - Estructura Estandarizada de Superpoderes
DesArroyo.tech - Sistema de Fabricación de Videos

Este script demuestra cómo usar la nueva estructura estandarizada
para crear videos de superpoderes de manera eficiente.
"""

import json
import requests
from datetime import datetime

class SuperpoderesVideoGenerator:
    def __init__(self, base_url="http://localhost:3000", token=None):
        self.base_url = base_url
        self.token = token or "tu_token_aqui"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def crear_video_superpoder(self, nombre_superpoder, clips_info):
        """
        Crea un video de superpoder usando la estructura estandarizada
        
        Args:
            nombre_superpoder (str): Nombre del superpoder (ej: "iPhone Scanner")
            clips_info (dict): Información de los clips necesarios
        """
        
        print(f"🎬 Creando video de superpoder: {nombre_superpoder}")
        print("=" * 50)
        
        # 1. Obtener plantilla de superpoderes
        template_id = self.obtener_plantilla_superpoderes()
        
        # 2. Subir clips con tipos específicos
        clip_ids = self.subir_clips_estandarizados(clips_info)
        
        # 3. Generar guión automático
        guion = self.generar_guion_superpoder(template_id, nombre_superpoder)
        
        # 4. Crear video con estructura fija
        video_id = self.generar_video_estandarizado(template_id, nombre_superpoder, clip_ids)
        
        # 5. Generar subtítulos automáticos
        self.generar_subtitulos_automaticos(video_id)
        
        print(f"✅ Video de superpoder '{nombre_superpoder}' creado exitosamente!")
        print(f"📁 ID del video: {video_id}")
        print(f"📝 Guión generado: {len(guion)} secciones")
        
        return video_id
    
    def obtener_plantilla_superpoderes(self):
        """Obtiene la plantilla de superpoderes estandarizada"""
        try:
            response = requests.get(
                f"{self.base_url}/api/dashboard/video-templates",
                headers=self.headers
            )
            
            if response.status_code == 200:
                templates = response.json()
                for template in templates:
                    if template.get('type') == 'superpoderes':
                        print(f"✅ Plantilla encontrada: {template['name']}")
                        return template['id']
            
            print("❌ No se encontró la plantilla de superpoderes")
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo plantilla: {e}")
            return None
    
    def subir_clips_estandarizados(self, clips_info):
        """
        Sube los clips con los tipos específicos para superpoderes
        
        Args:
            clips_info (dict): {
                'intro_fijo': 'ruta/al/intro.mp4',
                'video_muestra': 'ruta/a/la/muestra.mp4',
                'explicacion_instalacion': 'ruta/a/instalacion.mp4',
                'final_fijo': 'ruta/al/final.mp4'
            }
        """
        clip_ids = {}
        
        tipos_requeridos = [
            'intro_fijo',
            'video_muestra', 
            'explicacion_instalacion',
            'final_fijo'
        ]
        
        for tipo in tipos_requeridos:
            if tipo in clips_info:
                clip_id = self.subir_clip(clips_info[tipo], tipo)
                if clip_id:
                    clip_ids[tipo] = clip_id
                    print(f"✅ Clip {tipo} subido: {clip_id}")
                else:
                    print(f"❌ Error subiendo clip {tipo}")
        
        return clip_ids
    
    def subir_clip(self, file_path, clip_type):
        """Sube un clip individual"""
        try:
            with open(file_path, 'rb') as f:
                files = {'video': f}
                data = {
                    'clip_type': clip_type,
                    'description': f'Clip {clip_type} para superpoder',
                    'platform': 'tiktok',
                    'theme': 'superpoderes'
                }
                
                response = requests.post(
                    f"{self.base_url}/api/dashboard/upload-clip-advanced",
                    headers={"Authorization": f"Bearer {self.token}"},
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('clipId')
                else:
                    print(f"❌ Error subiendo clip: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error subiendo clip {file_path}: {e}")
            return None
    
    def generar_guion_superpoder(self, template_id, nombre_superpoder):
        """Genera guión automático para el superpoder"""
        try:
            data = {
                'template_id': template_id,
                'topic': f'Superpoder de {nombre_superpoder}',
                'additional_instructions': f'Enfócate en mostrar cómo {nombre_superpoder} puede mejorar la productividad'
            }
            
            response = requests.post(
                f"{self.base_url}/api/dashboard/generate-script",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                guion = result.get('script', {})
                print(f"✅ Guión generado con {len(guion.get('sections', []))} secciones")
                return guion
            else:
                print(f"❌ Error generando guión: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error generando guión: {e}")
            return None
    
    def generar_video_estandarizado(self, template_id, nombre, clip_ids):
        """Genera el video usando la estructura estandarizada"""
        try:
            data = {
                'template_id': template_id,
                'name': f'Superpoder {nombre}',
                'platform': 'tiktok',
                'quality': 'hd',
                'clip_ids': list(clip_ids.values()),
                'style': 'superpoderes',
                'transitions': 'smooth',
                'description': f'Video de superpoder: {nombre}'
            }
            
            response = requests.post(
                f"{self.base_url}/api/dashboard/generate-video-advanced",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                video_id = result.get('id')
                print(f"✅ Video enviado a generación: {video_id}")
                return video_id
            else:
                print(f"❌ Error generando video: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error generando video: {e}")
            return None
    
    def generar_subtitulos_automaticos(self, video_id):
        """Genera subtítulos automáticos para el video"""
        try:
            # Obtener clips del video
            response = requests.get(
                f"{self.base_url}/api/dashboard/generated-videos/{video_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                video_data = response.json()
                clips_used = json.loads(video_data.get('clips_used', '[]'))
                
                # Generar subtítulos para cada clip
                for clip_id in clips_used:
                    self.generar_subtitulos_clip(clip_id)
                    
                print(f"✅ Subtítulos generados para {len(clips_used)} clips")
            else:
                print(f"❌ Error obteniendo video: {response.text}")
                
        except Exception as e:
            print(f"❌ Error generando subtítulos: {e}")
    
    def generar_subtitulos_clip(self, clip_id):
        """Genera subtítulos para un clip específico"""
        try:
            response = requests.post(
                f"{self.base_url}/api/dashboard/generate-subtitles",
                headers=self.headers,
                json={'clip_id': clip_id}
            )
            
            if response.status_code == 200:
                print(f"✅ Subtítulos generados para clip {clip_id}")
            else:
                print(f"❌ Error generando subtítulos para clip {clip_id}")
                
        except Exception as e:
            print(f"❌ Error generando subtítulos: {e}")


def ejemplo_uso():
    """Ejemplo de cómo usar el generador de superpoderes"""
    
    # Configurar el generador
    generator = SuperpoderesVideoGenerator(
        base_url="http://localhost:3000",
        token="tu_token_aqui"
    )
    
    # Información de clips para un superpoder de iPhone
    clips_iphone = {
        'intro_fijo': './clips/intro_superpoder.mp4',
        'video_muestra': './clips/iphone_scanner_demo.mp4',
        'explicacion_instalacion': './clips/tutorial_instalacion.mp4',
        'final_fijo': './clips/final_superpoder.mp4'
    }
    
    # Crear video de superpoder
    video_id = generator.crear_video_superpoder(
        nombre_superpoder="iPhone Scanner",
        clips_info=clips_iphone
    )
    
    if video_id:
        print(f"\n🎉 ¡Video de superpoder creado exitosamente!")
        print(f"📊 ID: {video_id}")
        print(f"🔗 URL: http://localhost:3000/dashboard/videos/{video_id}")
        print(f"⏱️ Duración: 59 segundos (estructura estandarizada)")
        print(f"🎯 Estructura: Intro (8s) + Muestra (25s) + Instalación (20s) + Final (6s)")


if __name__ == "__main__":
    print("⚡ Generador de Videos de Superpoderes - DesArroyo.tech")
    print("=" * 60)
    ejemplo_uso() 