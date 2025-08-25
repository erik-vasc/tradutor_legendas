import pysrt
from deep_translator import GoogleTranslator

def traduzir_legenda(input_file, output_file, src_lang='en', dest_lang='pt'):
    # Carrega a legenda original
    subs = pysrt.open(input_file)
    translator = GoogleTranslator(source=src_lang, target=dest_lang)

    for sub in subs:
        texto_original = sub.text
        try:
            traducao = translator.translate(texto_original)
            sub.text = traducao
        except Exception as e:
            print(f"Erro ao traduzir: {texto_original} -> {e}")

    # Salva a nova legenda traduzida
    subs.save(output_file, encoding='utf-8')
    print(f"Legenda traduzida salva como: {output_file}")

if __name__ == "__main__":
    arquivo_origem = "legenda_original.srt"
    arquivo_destino = "legenda_traduzida.srt"
    traduzir_legenda(arquivo_origem, arquivo_destino)
