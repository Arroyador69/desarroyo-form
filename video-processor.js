const ffmpeg = require('fluent-ffmpeg');
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

class VideoProcessor {
    constructor() {
        // Configurar rutas de FFmpeg si es necesario
        // En producción podrías necesitar especificar la ruta exacta
        // ffmpeg.setFfmpegPath('/path/to/ffmpeg');
        // ffmpeg.setFfprobePath('/path/to/ffprobe');
        
        this.videoOutputDir = path.join(__dirname, 'videos/output');
        this.videoThumbnailsDir = path.join(__dirname, 'videos/thumbnails');
        this.videoTempDir = path.join(__dirname, 'videos/temp');
    }

    /**
     * Obtener información de un archivo de video
     */
    async getVideoInfo(videoPath) {
        return new Promise((resolve, reject) => {
            ffmpeg.ffprobe(videoPath, (err, metadata) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                const videoStream = metadata.streams.find(stream => stream.codec_type === 'video');
                const audioStream = metadata.streams.find(stream => stream.codec_type === 'audio');
                
                resolve({
                    duration: metadata.format.duration,
                    size: metadata.format.size,
                    format: metadata.format.format_name,
                    resolution: videoStream ? `${videoStream.width}x${videoStream.height}` : null,
                    hasAudio: !!audioStream,
                    bitrate: metadata.format.bit_rate
                });
            });
        });
    }

    /**
     * Generar thumbnail de un video
     */
    async generateThumbnail(videoPath, outputPath, timeOffset = 1) {
        return new Promise((resolve, reject) => {
            ffmpeg(videoPath)
                .seekInput(timeOffset)
                .frames(1)
                .size('320x568') // Formato vertical para redes sociales
                .output(outputPath)
                .on('end', () => resolve(outputPath))
                .on('error', reject)
                .run();
        });
    }

    /**
     * Recortar video a duración específica
     */
    async trimVideo(inputPath, outputPath, duration = 59) {
        return new Promise((resolve, reject) => {
            ffmpeg(inputPath)
                .duration(duration)
                .output(outputPath)
                .on('end', () => resolve(outputPath))
                .on('error', reject)
                .run();
        });
    }

    /**
     * Redimensionar video a formato vertical (9:16)
     */
    async resizeToVertical(inputPath, outputPath) {
        return new Promise((resolve, reject) => {
            ffmpeg(inputPath)
                .size('1080x1920') // Formato vertical estándar
                .aspect('9:16')
                .autopad(true, 'black')
                .output(outputPath)
                .on('end', () => resolve(outputPath))
                .on('error', reject)
                .run();
        });
    }

    /**
     * Añadir texto overlay al video
     */
    async addTextOverlay(inputPath, outputPath, text, style = {}) {
        return new Promise((resolve, reject) => {
            const {
                fontsize = 48,
                fontcolor = 'white',
                position = 'center',
                fontfile = null // Opcional: ruta a fuente personalizada
            } = style;

            let filterText = `drawtext=text='${text}':fontsize=${fontsize}:fontcolor=${fontcolor}:`;
            
            // Posicionar texto
            switch (position) {
                case 'top':
                    filterText += 'x=(w-text_w)/2:y=50';
                    break;
                case 'bottom':
                    filterText += 'x=(w-text_w)/2:y=h-text_h-50';
                    break;
                case 'center':
                default:
                    filterText += 'x=(w-text_w)/2:y=(h-text_h)/2';
                    break;
            }

            if (fontfile) {
                filterText += `:fontfile=${fontfile}`;
            }

            ffmpeg(inputPath)
                .videoFilters(filterText)
                .output(outputPath)
                .on('end', () => resolve(outputPath))
                .on('error', reject)
                .run();
        });
    }

    /**
     * 🎬 Aplicar subtítulos automáticos al video con estilo personalizado
     * Estilo: Amarillo con bordes negros, mayúsculas
     */
    async addSubtitlesToVideo(inputPath, outputPath, subtitles) {
        return new Promise((resolve, reject) => {
            try {
                if (!subtitles || subtitles.length === 0) {
                    // Si no hay subtítulos, simplemente copia el video
                    fs.copyFileSync(inputPath, outputPath);
                    return resolve(outputPath);
                }

                // Crear archivo SRT temporal
                const videoId = uuidv4();
                const srtPath = path.join(this.videoTempDir, `subtitles_${videoId}.srt`);
                
                // Generar contenido SRT
                let srtContent = '';
                subtitles.forEach((subtitle, index) => {
                    const startTime = this.formatSRTTime(subtitle.start_time);
                    const endTime = this.formatSRTTime(subtitle.end_time);
                    const text = subtitle.edited_text || subtitle.original_text;
                    
                    srtContent += `${index + 1}\n`;
                    srtContent += `${startTime} --> ${endTime}\n`;
                    srtContent += `${text.toUpperCase()}\n\n`;
                });
                
                fs.writeFileSync(srtPath, srtContent, 'utf8');

                // Aplicar subtítulos con FFmpeg con estilo amarillo y bordes negros
                ffmpeg(inputPath)
                    .videoFilters([
                        `subtitles=${srtPath}:force_style='FontSize=36,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=3,Bold=1,Alignment=2'`
                    ])
                    .output(outputPath)
                    .on('end', () => {
                        // Limpiar archivo SRT temporal
                        if (fs.existsSync(srtPath)) {
                            fs.unlinkSync(srtPath);
                        }
                        resolve(outputPath);
                    })
                    .on('error', (error) => {
                        // Limpiar archivo SRT temporal en caso de error
                        if (fs.existsSync(srtPath)) {
                            fs.unlinkSync(srtPath);
                        }
                        reject(error);
                    })
                    .run();

            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * 🎬 Formatear tiempo para archivos SRT (formato: HH:MM:SS,mmm)
     */
    formatSRTTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        const milliseconds = Math.floor((seconds % 1) * 1000);
        
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${milliseconds.toString().padStart(3, '0')}`;
    }

    /**
     * 🎬 Procesar video con subtítulos automáticos
     */
    async processVideoWithSubtitles(inputPath, outputPath, subtitles) {
        try {
            // Primero redimensionar a formato vertical
            const resizedPath = path.join(this.videoTempDir, `resized_${uuidv4()}.mp4`);
            await this.resizeToVertical(inputPath, resizedPath);
            
            // Luego aplicar subtítulos
            await this.addSubtitlesToVideo(resizedPath, outputPath, subtitles);
            
            // Limpiar archivo temporal
            if (fs.existsSync(resizedPath)) {
                fs.unlinkSync(resizedPath);
            }
            
            return outputPath;
            
        } catch (error) {
            throw new Error(`Error procesando video con subtítulos: ${error.message}`);
        }
    }

    /**
     * Combinar múltiples clips en un video final
     */
    async combineClips(clips, template, outputName) {
        return new Promise(async (resolve, reject) => {
            try {
                const videoId = uuidv4();
                const tempFiles = [];
                const outputPath = path.join(this.videoOutputDir, `${outputName}_${videoId}.mp4`);
                
                // Procesar cada clip según la plantilla
                const processedClips = [];
                
                for (let i = 0; i < clips.length; i++) {
                    const clip = clips[i];
                    const tempPath = path.join(this.videoTempDir, `temp_${videoId}_${i}.mp4`);
                    tempFiles.push(tempPath);
                    
                    // Redimensionar a formato vertical
                    await this.resizeToVertical(clip.file_path, tempPath);
                    
                    // Añadir overlay de texto si está configurado en la plantilla
                    if (template.structure.text_overlay && clip.type === 'body') {
                        const textPath = path.join(this.videoTempDir, `text_${videoId}_${i}.mp4`);
                        tempFiles.push(textPath);
                        
                        await this.addTextOverlay(tempPath, textPath, 
                            `Tip #${i + 1}: DesArroyo.tech`, 
                            template.style_config);
                        
                        processedClips.push(textPath);
                    } else {
                        processedClips.push(tempPath);
                    }
                }

                // Crear archivo de lista para concatenar
                const listPath = path.join(this.videoTempDir, `list_${videoId}.txt`);
                const listContent = processedClips.map(clip => `file '${clip}'`).join('\n');
                fs.writeFileSync(listPath, listContent);
                tempFiles.push(listPath);

                // Concatenar clips
                ffmpeg()
                    .input(listPath)
                    .inputOptions(['-f', 'concat', '-safe', '0'])
                    .outputOptions(['-c', 'copy'])
                    .output(outputPath)
                    .on('end', async () => {
                        try {
                            // Verificar duración y recortar si es necesario
                            const videoInfo = await this.getVideoInfo(outputPath);
                            
                            if (videoInfo.duration > template.max_duration) {
                                const trimmedPath = path.join(this.videoOutputDir, `${outputName}_${videoId}_trimmed.mp4`);
                                await this.trimVideo(outputPath, trimmedPath, template.max_duration);
                                
                                // Eliminar el video original largo
                                fs.unlinkSync(outputPath);
                                
                                // Generar thumbnail
                                const thumbnailPath = path.join(this.videoThumbnailsDir, `${outputName}_${videoId}.jpg`);
                                await this.generateThumbnail(trimmedPath, thumbnailPath);
                                
                                // Limpiar archivos temporales
                                this.cleanupTempFiles(tempFiles);
                                
                                resolve({
                                    outputPath: trimmedPath,
                                    thumbnailPath,
                                    duration: template.max_duration,
                                    videoInfo
                                });
                            } else {
                                // Generar thumbnail
                                const thumbnailPath = path.join(this.videoThumbnailsDir, `${outputName}_${videoId}.jpg`);
                                await this.generateThumbnail(outputPath, thumbnailPath);
                                
                                // Limpiar archivos temporales
                                this.cleanupTempFiles(tempFiles);
                                
                                resolve({
                                    outputPath,
                                    thumbnailPath,
                                    duration: videoInfo.duration,
                                    videoInfo
                                });
                            }
                        } catch (error) {
                            this.cleanupTempFiles(tempFiles);
                            reject(error);
                        }
                    })
                    .on('error', (error) => {
                        this.cleanupTempFiles(tempFiles);
                        reject(error);
                    })
                    .run();

            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Procesar video según plantilla educativa
     */
    async processEducationalVideo(clips, template, outputName) {
        // Orden específico para videos educativos: intro -> body -> outro
        const orderedClips = [
            ...clips.filter(c => c.type === 'intro'),
            ...clips.filter(c => c.type === 'body'),
            ...clips.filter(c => c.type === 'outro')
        ];

        return this.combineClips(orderedClips, template, outputName);
    }

    /**
     * Procesar video según plantilla inspiracional
     */
    async processInspirationalVideo(clips, template, outputName) {
        // Para videos inspiracionales, pueden tener un orden más libre
        const orderedClips = [
            ...clips.filter(c => c.type === 'intro'),
            ...clips.filter(c => c.type === 'body'),
            ...clips.filter(c => c.type === 'outro')
        ];

        return this.combineClips(orderedClips, template, outputName);
    }

    /**
     * Procesar video de superpoderes con estructura estandarizada
     * Estructura: INTRO FIJO + VIDEO MUESTRA + EXPLICACIÓN INSTALACIÓN + FINAL FIJO
     */
    async processSuperpoderesVideo(clips, template, outputName) {
        return new Promise(async (resolve, reject) => {
            try {
                const videoId = uuidv4();
                const tempFiles = [];
                const outputPath = path.join(this.videoOutputDir, `${outputName}_${videoId}.mp4`);
                
                // Estructura estandarizada para superpoderes
                const structure = template.structure;
                const orderedClips = [];
                
                // 1. INTRO FIJO (siempre el mismo)
                const introClips = clips.filter(c => c.type === 'intro_fijo' || c.type === 'intro');
                if (introClips.length > 0) {
                    orderedClips.push({
                        clip: introClips[0],
                        type: 'intro_fijo',
                        duration: structure.intro_duration || 8,
                        color: template.style_config.superpoder_style?.intro_color || '#FF6B35'
                    });
                }
                
                // 2. VIDEO MUESTRA (contenido específico del superpoder)
                const muestraClips = clips.filter(c => c.type === 'video_muestra' || c.type === 'body');
                if (muestraClips.length > 0) {
                    orderedClips.push({
                        clip: muestraClips[0],
                        type: 'video_muestra',
                        duration: structure.muestra_duration || 25,
                        color: template.style_config.superpoder_style?.muestra_color || '#00D4AA'
                    });
                }
                
                // 3. EXPLICACIÓN INSTALACIÓN (cómo instalar el superpoder)
                const instalacionClips = clips.filter(c => c.type === 'explicacion_instalacion' || c.type === 'body');
                if (instalacionClips.length > 0) {
                    orderedClips.push({
                        clip: instalacionClips[0],
                        type: 'explicacion_instalacion',
                        duration: structure.instalacion_duration || 20,
                        color: template.style_config.superpoder_style?.instalacion_color || '#F7931E'
                    });
                }
                
                // 4. FINAL FIJO (siempre el mismo)
                const finalClips = clips.filter(c => c.type === 'final_fijo' || c.type === 'outro');
                if (finalClips.length > 0) {
                    orderedClips.push({
                        clip: finalClips[0],
                        type: 'final_fijo',
                        duration: structure.final_duration || 6,
                        color: template.style_config.superpoder_style?.final_color || '#667eea'
                    });
                }
                
                // Procesar cada clip con su estilo específico
                const processedClips = [];
                
                for (let i = 0; i < orderedClips.length; i++) {
                    const clipData = orderedClips[i];
                    const clip = clipData.clip;
                    const tempPath = path.join(this.videoTempDir, `temp_${videoId}_${i}.mp4`);
                    tempFiles.push(tempPath);
                    
                    // Redimensionar a formato vertical
                    await this.resizeToVertical(clip.file_path, tempPath);
                    
                    // Añadir overlay específico para cada sección
                    const textPath = path.join(this.videoTempDir, `text_${videoId}_${i}.mp4`);
                    tempFiles.push(textPath);
                    
                    // Texto específico según la sección
                    let overlayText = '';
                    switch (clipData.type) {
                        case 'intro_fijo':
                            overlayText = '⚡ SUPERPODER';
                            break;
                        case 'video_muestra':
                            overlayText = '🎯 FUNCIONAMIENTO';
                            break;
                        case 'explicacion_instalacion':
                            overlayText = '🔧 INSTALACIÓN';
                            break;
                        case 'final_fijo':
                            overlayText = '🚀 DesArroyo.tech';
                            break;
                    }
                    
                    // Aplicar estilo específico de la sección
                    const sectionStyle = {
                        ...template.style_config,
                        colors: {
                            ...template.style_config.colors,
                            primary: clipData.color
                        }
                    };
                    
                    await this.addTextOverlay(tempPath, textPath, overlayText, sectionStyle);
                    processedClips.push(textPath);
                }

                // Crear archivo de lista para concatenar
                const listPath = path.join(this.videoTempDir, `list_${videoId}.txt`);
                const listContent = processedClips.map(clip => `file '${clip}'`).join('\n');
                fs.writeFileSync(listPath, listContent);
                tempFiles.push(listPath);

                // Concatenar clips con transiciones suaves
                ffmpeg()
                    .input(listPath)
                    .inputOptions(['-f', 'concat', '-safe', '0'])
                    .outputOptions([
                        '-c', 'copy',
                        '-filter_complex', 'fade=t=in:st=0:d=0.5,fade=t=out:st=58.5:d=0.5'
                    ])
                    .output(outputPath)
                    .on('end', async () => {
                        try {
                            // Verificar duración y recortar si es necesario
                            const videoInfo = await this.getVideoInfo(outputPath);
                            
                            if (videoInfo.duration > template.max_duration) {
                                const trimmedPath = path.join(this.videoOutputDir, `${outputName}_${videoId}_trimmed.mp4`);
                                await this.trimVideo(outputPath, trimmedPath, template.max_duration);
                                
                                // Eliminar el video original largo
                                fs.unlinkSync(outputPath);
                                
                                // Generar thumbnail
                                const thumbnailPath = path.join(this.videoThumbnailsDir, `${outputName}_${videoId}.jpg`);
                                await this.generateThumbnail(trimmedPath, thumbnailPath);
                                
                                // Limpiar archivos temporales
                                this.cleanupTempFiles(tempFiles);
                                
                                resolve({
                                    outputPath: trimmedPath,
                                    thumbnailPath,
                                    duration: template.max_duration,
                                    videoInfo,
                                    structure: 'superpoderes_estandarizado'
                                });
                            } else {
                                // Generar thumbnail
                                const thumbnailPath = path.join(this.videoThumbnailsDir, `${outputName}_${videoId}.jpg`);
                                await this.generateThumbnail(outputPath, thumbnailPath);
                                
                                // Limpiar archivos temporales
                                this.cleanupTempFiles(tempFiles);
                                
                                resolve({
                                    outputPath,
                                    thumbnailPath,
                                    duration: videoInfo.duration,
                                    videoInfo,
                                    structure: 'superpoderes_estandarizado'
                                });
                            }
                        } catch (error) {
                            this.cleanupTempFiles(tempFiles);
                            reject(error);
                        }
                    })
                    .on('error', (error) => {
                        this.cleanupTempFiles(tempFiles);
                        reject(error);
                    })
                    .run();

            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Añadir música de fondo
     */
    async addBackgroundMusic(videoPath, musicPath, outputPath, musicVolume = 0.3) {
        return new Promise((resolve, reject) => {
            ffmpeg()
                .input(videoPath)
                .input(musicPath)
                .outputOptions([
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-filter_complex', `[1:a]volume=${musicVolume}[music];[0:a][music]amix=inputs=2:duration=first[out]`,
                    '-map', '0:v',
                    '-map', '[out]'
                ])
                .output(outputPath)
                .on('end', () => resolve(outputPath))
                .on('error', reject)
                .run();
        });
    }

    /**
     * Limpiar archivos temporales
     */
    cleanupTempFiles(files) {
        files.forEach(file => {
            if (fs.existsSync(file)) {
                try {
                    fs.unlinkSync(file);
                } catch (error) {
                    console.error(`Error eliminando archivo temporal ${file}:`, error);
                }
            }
        });
    }

    /**
     * Validar que FFmpeg esté instalado
     */
    async checkFFmpegInstallation() {
        return new Promise((resolve) => {
            ffmpeg()
                .getAvailableFormats((err, formats) => {
                    if (err) {
                        resolve(false);
                    } else {
                        resolve(true);
                    }
                });
        });
    }
}

module.exports = VideoProcessor; 