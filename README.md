# Клавиатурный тренажер

Практикум Python 2024, 1 проект

Б05-328, Ларин Иван

## Установка

```
pip install -r requirements.txt
```

## Запуск

```
python main.py
```

---

# Документация

## Версия Python

3.10.4, но должно работать и на более новых

## Используемые библиотеки

Для графики: `flet`, `flet_timer`.

Остальное:

- `numpy, pandas, matplotlib, seaborn`
- стандартные библиотеки: `csv, random, typing, enum` и другие.

## Описание

Приложение "Клавиатурный тренажер" поможет пользователям улучшить свои навыки печати на клавиатуре. Пользователь может выбирать один из режимов для тренировки или измерения своей скорости печати. В процессе набора текста будут измеряться скорость и точность печати (и может быть другие показатели).

## Реализуемый функционал

Пользователь может настроить режим под себя:

### Содержание текста

*курсивом* буду помечать то, что не обязательно будет реализовано

- выбор языка
- добавить/убрать пунктуацию
- добавить/убрать цифры

### Размер текста

- по размеру текста (n слов)
- по времени (n секунд)

### Дополнительно

- *выбор темы приложения* (выбрать одну из нескольких заранее заготовленных цветовых схем)

В процессе печати пользователю будет видна текущаю скорость печати и точность. По завершению будет видна расширенная статистика.

## Архитектура

### Класс `TextGenerator`

Атрибуты:

- `language` - язык, на котором нужно генерировать текст
- `vocabulary` - массив, из которого нужно брать слова
- `punctuation: bool` - нужно ли добавлять пунктуацию
- `numbers: bool` - нужно ли добавлять числа

Методы:

- `toggle_punctuation()`
- `toggle_numbers()`
- `load_vocabulary(path)` - загружает `vocabulary` из заданного пути
- `generate() -> str` - создает текст согласно своим найстрокам

### Класс `Letter` (графический)

Хранит значение (`value`), цвет (`color`).
Создает объект вида `ft.Text`.

### Класс `MainText` (графический)

Атрибуты:

- `text` - то, что нужно отобразить
- `letter_colors: List[LetterColor]` - в какой цвет красить каждую букву (`LetterColor` &mdash; `enum`)

Методы:

- `generate_content()` - создает `ft.Container`, содержащий отрисованный текст

- `update_content(text, letter_colors)` - обновляет содержимое (в том числе перерисовывает себя)

### Класс `Statistics`

Хранит

- `test_size_mode: str` - `"words" | "time"` - какой режим человек выбрал для теста (по числу слов или по времени)
- `test_size` - число слов, либо число секунд в зависимости от прошлого атрибута
- `language`
- `start_time: datetime`, `end_time: datetime | None` - последнее равно `None` если сессия еще не закончилась
- `total_key_presses`, `correct_key_presses`
- `punctuation`, `numbers` - использовались ли эти настройки при генерации текста

Собирает статистику о каком-то тесте.

- `key_pressed(key, is_correct)` - изменяет `current_text` и обновляет статистику.
- `get_accuracy() -> float`
- `get_cpm() -> float` - смотрит на разницу текущего времени (или времени конца) и начала сессии, из этого вычисляет `wpm`
- `get_wpm() -> float` - аналогично `cpm`, из расчета, что одно слово в среднем 5 символов
- `end()` - записывает `end_time`
- `save()` - сохраняет информацию о себе в `.csv` файл

### Класс `HeatmapStatistics`

Атрибуты:

- `stats: Dict["en" | "ru", 2-d np.array]` - статистика по опечаткам для отрисовки `heatmap`-а, собранная по каждому языку отдельно

Методы:

- `add_key_press(need_type, typed)` - обновляет `self.stats` в зависимости от корректности написания
- `save()` - сохраняет себя в `.csv` файл

### Датакласс `TestInfo`

- `status` - запущен ли тест (`NOT_STARTED` | `RUNNING` | `ENDED`)
- `language`
- `size_mode` - `"words" | "time"`, описывалось ранее
- `available_time: int | None` - хранит число секунд если `size_mode == "time"`
- `words_to_generate` - количество слов согласно `size_mode`
- `can_type: bool` - нужно ли обрабатывать нажатия пользователя (т.е. он находится на нужной странице и готов печатать)

### Датакласс `TextInfo`

Хранит информацию о тексте для `TypingTest`

- `correct_text: str` - то, что нужно напечатать в процессе теста
- `letter_colors` - цвета, которые нужно подавать в `MainText`
- `display_text: str` - равно `correct_text`, но теоретически можно было бы показывать на неправильных позициях то, что написал пользователь, а не то, что нужно
- `printed_text: str` - то, что пользователь уже написал

### Класс `TypingTest`

Атрибуты:

- `test_info: TestInfo`

- `timer` - элемент, который каждую секунду будет вызывать `self.every_second()`

- `text_generator: TextGenerator`
- `main_text: MainText` - для отрисовки
- `settings_bar: SettingsBar` - ссылка на панель настроек чтобы передавать ей команды
- `information_bar: InformationBar`
- `statistics: Statistics`
- `heatmap: HeatmapStatistics`

- `visual_element` - то, что нужно отрисовать (меню настроек/информации и текст)

Методы:

- `start()` - начинает тест печати
- `stop()` - завершает тест печати
- `restart()` - обнуляет все (не сохраняет статистику если текущий тест был не окончен)
- `every_second()` - обновить информацию о тесте + проверить не закончился ли он если выбран режим времени

- `regenerate_text()` - обновляет текст согласно текущим настройкам
- `toggle_punctuation()` - обновляет настройки у себя и `text_generator`
- `toggle_numbers()`
- `select_words(count)` - обновляет режим теста и число слов
- `select_time(time)` - обновляет режим теста и время
- `update_information_bar()` - говорит `InformationBar` перерисовать себя
- `key_pressed()` - обрабатывает нажатие какой-то кнопки клавиатуры

### Класс `SettingsBar` (графический)

#### Подкласс `LabeledButton` (графический)

Для создания кнопок в `SettingsBar`.

Атрибуты:

- `text` - то, что будет написано на кнопке
- `is_on: bool` - включена опция или нет
- `on_click` - функция, которую нужно вызвать по нажатии

Методы:

- `toggle()` - перерисоывает себя
- `generate_content()` - возвращает `ft.Text` согласно атрибутам

---

Атрибуты:

все кнопки (`punctuation`, `numers`, кнопки для выбора режима и языка)

Методы:

- Обрабатывает нажатия на свои кнопки.
- `update_buttons()` - перерисовывает содержимое

### Класс `InformationBar` (графический)

#### Подкласс `TextElement` (графический)

Хранит название и значение (например `WPM: 100` и `WPM` - название, а `100` - значение).

---

Атрибуты:

- `wpm: self.TextElement`
- `accuracy: self.TextElement`

Методы:

- `set_wpm(value)`
- `set_accuracy(value)`

### Класс `StatisticsPage` (графический)

#### Подкласс `TestStatisticsVisualizer` (графический)

Хранит объект `Statistics` и из него создает `ft.Container`
со всей нужной информацией.

---

Атрибуты:

- `stats: pd.DataFrame` - статистика о всех сохраненных запусках

### Класс `HeatmapsPage` (графический)

#### Подкласс `LanguageHeatmap` (графический)

Атрибуты:

- `language`
- `heatmap_statistics: HeatmapStatistics`

Создает `.png` файл при инициализации, после чего `HeatmapsPage` может его отобразить.

---

Атрибуты:

- `stats: HeatmapStatistics` - статистика об опечатках на разных языках

Создает `ft.Row` из `heatmap`-ов.
