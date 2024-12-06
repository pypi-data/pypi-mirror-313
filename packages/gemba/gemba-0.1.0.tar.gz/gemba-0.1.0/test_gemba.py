from gemba import get_gemba_scores

source = ["Hello, how are you?", "I am fine, thank you.", "I am not fine, thank you."]
hypothesis = ["Hallo, wie geht es dir?", "Ich bin gut, danke.", "Ich bin Adolf, wer bist du?"]
source_lang = "en"
target_lang = "de"

answers, errors = get_gemba_scores(source, hypothesis, source_lang, target_lang, method="GEMBA-MQM_norm")

for answer, error in zip(answers, errors):
    print(answer, error)
