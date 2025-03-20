# nf-rnachrom-BridgeCodes

## Использование

python plotBridgeCodes.py <statistics_file> <mode> <input_path> <output_path> <u_parameter_arguments>

## Аргументы

- statistics_file - файл с данными
- mode - режим работы
- input_path - путь к входному файлу
- output_path - путь к выходному файлу
- u_parameter_arguments - параметры для фильтрации по длине

### Примеры

Для single-end данных:

python plotBridgeCodes.py "SRR17331267.codes.tsv" "SE" "/path/to/input/data/" "/path/to/output/" "F"

Для paired-end данных:

python plotBridgeCodes.py "SRR17331267_2.codes.tsv" "PE" "/path/to/input/data/" "/path/to/output/" "F0, R0"


### Выходные данные

Скрипт создает PNG файл с именем `{statistics_file}_{mode}.png` в указанной выходной директории. График содержит:
- Таблицу со всеми найденными кодами и их описанием
- Столбчатую диаграмму в логарифмическом масштабе
- Цветовую легенду:
  - Зеленый: RNA и DNA части прошли фильтр по длине
  - Желтый: RNA и DNA части не прошли фильтр по длине
  - Синий: все остальные случаи