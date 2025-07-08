# 🎬 Configuración de Subtítulos Automáticos con IA

## ✅ Funcionalidades Implementadas

### 🤖 Transcripción Inteligente con DeepSeek
- **Motor IA**: DeepSeek (único proveedor)
- **Análisis**: Duración real del video para contexto
- **Generación**: Transcripción viral optimizada para engagement
- **Estilo**: Contenido que maximiza viralidad por plataforma
- **Inteligencia**: Adapta vocabulario y hooks según duración del clip

### 🎨 Estilo de Subtítulos
- **Color**: Amarillo (`#FFFF00`)
- **Borde**: Negro con grosor 3px
- **Fuente**: Negrita (Bold)
- **Formato**: MAYÚSCULAS automático
- **Posición**: Centrado en la parte inferior
- **Tamaño**: 36px (ajustable)

### 📝 Editor de Subtítulos
- Previsualización en tiempo real del estilo
- Edición de texto, tiempos de inicio y fin
- Indicador de confianza de la IA
- Eliminación de segmentos individuales
- Guardado automático de cambios

## 🔧 Configuración Requerida

### Variables de Entorno
```bash
# Clave API de DeepSeek (ÚNICO proveedor de IA)
DEEPSEEK_API_KEY=tu_clave_deepseek

# Otras configuraciones existentes
JWT_SECRET=tu_clave_jwt
```

### Dependencias Instaladas
```json
{
  "form-data": "^4.0.0"
}
```

### Motor de IA
- **DeepSeek**: Único proveedor de IA para transcripción inteligente y optimización viral
- **FFmpeg**: Procesamiento de audio/video y aplicación de subtítulos

## 🚀 Cómo Usar

### 1. Generar Subtítulos
1. Ve a la pestaña "🎬 Fábrica de Videos"
2. En la sección "Mis Clips", haz clic en **"Subtítulos"** en cualquier clip
3. El sistema extraerá el audio y lo transcribirá con IA
4. Se abrirá automáticamente el editor de subtítulos

### 2. Editar Subtítulos
- **Texto**: Modifica el contenido transcrito
- **Tiempo**: Ajusta inicio y fin de cada segmento
- **Eliminar**: Quita segmentos innecesarios
- **Guardar**: Los cambios se guardan automáticamente

### 3. Aplicar a Videos
Los subtítulos se aplicarán automáticamente al generar videos usando las plantillas con el estilo configurado.

## 📊 Base de Datos

### Nueva Tabla: `video_subtitles`
```sql
CREATE TABLE video_subtitles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER,
    clip_id INTEGER,
    original_text TEXT,      -- Transcripción original de la IA
    edited_text TEXT,        -- Texto editado por el usuario
    start_time REAL,         -- Tiempo de inicio en segundos
    end_time REAL,           -- Tiempo de fin en segundos
    confidence REAL,         -- Confianza de la transcripción (0-1)
    status TEXT DEFAULT 'pending', -- 'pending', 'reviewed', 'approved'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🎛️ APIs Implementadas

### POST `/api/dashboard/generate-subtitles`
- Genera subtítulos automáticos para un clip
- Parámetros: `clip_id`
- Utiliza DeepSeek + Whisper Local para transcripción y optimización viral

### GET `/api/dashboard/subtitles/:clip_id`
- Obtiene subtítulos existentes de un clip
- Devuelve array de subtítulos ordenados por tiempo

### PUT `/api/dashboard/subtitles/:id`
- Actualiza un subtítulo específico
- Parámetros: `edited_text`, `start_time`, `end_time`, `status`

### DELETE `/api/dashboard/subtitles/:id`
- Elimina un subtítulo específico

## 🔄 Integración con VideoProcessor

### Nuevas Funciones
- `addSubtitlesToVideo()`: Aplica subtítulos con estilo
- `formatSRTTime()`: Convierte tiempos a formato SRT
- `processVideoWithSubtitles()`: Procesa video completo con subtítulos

### Estilo FFmpeg
```javascript
subtitles=${srtPath}:force_style='FontSize=36,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=3,Bold=1,Alignment=2'
```

## 📱 Interfaz Usuario

### Modal de Edición
- Vista previa del estilo en tiempo real
- Campos editables para cada segmento
- Barra de confianza de la IA
- Botones de acción (Guardar/Eliminar)

### Botón de Acceso
- Nuevo botón "Subtítulos" en cada clip
- Color amarillo para identificación visual
- Icono de closed-captioning

## ⚠️ Consideraciones

### Limitaciones
- Requiere conexión a internet para OpenAI API
- Consume créditos de OpenAI por transcripción
- Calidad depende de la claridad del audio

### Recomendaciones
- Audio claro y sin ruido de fondo
- Verificar siempre los subtítulos generados
- Ajustar tiempos para sincronización perfecta

## 🎯 Estado Actual

✅ **Completado:**
- Transcripción automática con DeepSeek + Whisper Local
- Editor visual de subtítulos
- Aplicación de estilo amarillo con bordes negros
- Optimización viral automática con DeepSeek
- Integración completa en dashboard
- APIs REST completas

🔄 **Próximos pasos:**
- Integración en proceso de generación de videos
- Publicación automática con subtítulos
- Soporte para múltiples idiomas 