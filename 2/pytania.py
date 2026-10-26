import json

#plik json
with open("pytania.json", "r", encoding="utf-8") as f:
    data = json.load(f)

questions = data["questions"]
rules = data["rules"]
user_answers = {}

print("=== SYSTEM EKSPERCKI: ROŚLINY ===\n")

#pytania dla uzytkownika
for q_id, q_data in questions.items():
    print(f"{q_id}: {q_data['text']}")
    options = q_data["answers"]
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    
    while True:
        choice = input("Wybierz numer lub wpisz odpowiedź: ").strip()
        if choice in options:
            user_answers[q_id] = choice
            break
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            user_answers[q_id] = options[int(choice) - 1]
            break
        print("Nieprawidłowy wybór, spróbuj ponownie.")
    print()

#pasujace reguly
matched_rules = []
for rule in rules:
    if all(user_answers.get(k) == v for k, v in rule["if"].items()):
        matched_rules.append(rule)

# 4. Wypisanie samej diagnozy
print("=== WYNIKI DIAGNOZY ===")
if matched_rules:
    for rule in matched_rules:
        print(f"- {rule['then']['diagnosis']}")
else:
    print("Brak pasujących reguł dla podanych odpowiedzi.")