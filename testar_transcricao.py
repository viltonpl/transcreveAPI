#!/usr/bin/env python3
"""Script para testar a transcrição de áudio sem precisar de servidor HTTP"""

import speech_recognition as sr
from pydub import AudioSegment
import io
import os

def transcrever_audio(caminho_audio):
    """
    Transcreve um arquivo de áudio diretamente usando SpeechRecognition
    
    Args:
        caminho_audio: Caminho para o arquivo de áudio (MP3, WAV, OGG)
    
    Returns:
        str: Texto transcrito ou mensagem de erro
    """
    print(f"🎤 Processando áudio: {caminho_audio}")
    
    if not os.path.exists(caminho_audio):
        return f"❌ Erro: Arquivo não encontrado: {caminho_audio}"
    
    try:
        # Detectar tipo de arquivo
        extensao = caminho_audio.lower().split('.')[-1]
        
        # Se for MP3 ou OGG, converter para WAV
        if extensao in ['mp3', 'ogg']:
            print(f"📝 Convertendo {extensao.upper()} para WAV...")
            audio = AudioSegment.from_file(caminho_audio, format=extensao)
            audio = audio.set_frame_rate(16000).set_channels(1)
            wav_io = io.BytesIO()
            audio.export(wav_io, format='wav')
            wav_io.seek(0)
            audio_file = wav_io
        else:
            # Arquivo WAV direto
            audio_file = caminho_audio
        
        # Inicializar reconhecedor
        recognizer = sr.Recognizer()
        
        # Processar áudio
        print("🔍 Reconhecendo fala...")
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        
        # Transcrever usando Google Speech Recognition
        texto = recognizer.recognize_google(audio_data, language='pt-BR')
        
        print(f"\n✅ Transcrição concluída com sucesso!")
        print(f"📄 Texto transcrito:\n")
        print(f"   \"{texto}\"\n")
        
        return texto
        
    except sr.UnknownValueError:
        return "❌ Erro: Não foi possível reconhecer o áudio"
    except sr.RequestError as e:
        return f"❌ Erro ao se comunicar com o serviço de reconhecimento: {e}"
    except Exception as e:
        return f"❌ Erro inesperado: {e}"


if __name__ == '__main__':
    # Caminho do arquivo de áudio
    caminho = '/workspaces/transcreveAPI/audio.mp3'
    
    print("=" * 60)
    print("🎙️  TRANSCRIÇÃO DE ÁUDIO - Google Speech Recognition")
    print("=" * 60)
    print()
    
    resultado = transcrever_audio(caminho)
    
    if not resultado.startswith('❌'):
        print("=" * 60)
        print("✨ Processo finalizado!")
        print("=" * 60)
