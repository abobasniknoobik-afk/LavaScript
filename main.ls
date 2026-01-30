type "--- ИГРА: ТЕРМИНАЛЬНЫЙ ВУЛКАН ---"
molten secret << random(10)
type "Я загадал число от 0 до 10. Попробуй угадать!"

ask guess << "Твой вариант: "
molten g_num << int(guess)

flow g_num == secret : type "ПОБЕДА! Ты предсказал извержение!"
flow g_num != secret : type "МИМО... Магма застыла. Это было число: " + str(secret)

type "--- КОНЕЦ СЕССИИ ---"
