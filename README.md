# Pipes and Filters

Python пакет для упрощения реализации архитектурного паттерна "Pipes and Filters". Этот пакет предоставляет простые и элегантные инструменты для создания конвейеров обработки данных.

## Особенности

- **Pipe**: Последовательное применение фильтров к данным
- **Splitter**: Разделение данных на несколько потоков обработки
- **Pipeline**: Обработка итерируемых источников данных через одну функцию
- **Flow**: Продвинутая обработка данных с разделением на множественные значения и их агрегацией
- Простой и интуитивный API
- Типизированный код
- Покрытие тестами

## Установка

### Из исходного кода
```bash
git clone <repository-url>
cd pipes-and-filters
pip install .
```

### Для разработки
```bash
pip install -e .[dev]
```

## Быстрый старт

```python
from pipes_and_filters import Pipe, Splitter, Pipeline, Flow

# Простой конвейер
pipe = Pipe(
    lambda x: x * 2,
    lambda x: x + 1,
    lambda x: x ** 2
)
result = pipe(5)  # ((5 * 2) + 1) ** 2 = 121
```

## Примеры использования

### 1. Pipe - Последовательная обработка

```python
from pipes_and_filters import Pipe

def even_step(x):
    print('Even step:', x)
    return x // 2

def odd_step(x):
    print('Odd step:', x)
    return 3 * x + 1

# Коллацовая последовательность (гипотеза Коллатца)
collatz_pipe = Pipe(
    even_step,  # 12 / 2 = 6
    even_step,  # 6 / 2 = 3
    odd_step,   # 3 * 3 + 1 = 10
    even_step,  # 10 / 2 = 5
    odd_step,   # 3 * 5 + 1 = 16
    even_step,  # 16 / 2 = 8
    even_step,  # 8 / 2 = 4
    even_step,  # 4 / 2 = 2
    even_step   # 2 / 2 = 1
)

result = collatz_pipe(12)
print('Result:', result)  # Result: 1
```

### 2. Splitter - Разделение потоков

```python
from math import sqrt
from pipes_and_filters import Splitter, Pipe

# Решение квадратного уравнения x^2 - x - 6 = 0
params = (1, -1, -6)  # (a, b, c)

# Вычисление дискриминанта
discriminant_pipe = Pipe(
    lambda x: (x, x[1] * x[1] - 4 * x[0] * x[2]),  # (params, D)
    lambda y: (y[0], sqrt(y[1]))  # (params, sqrt(D))
)

# Splitter для вычисления двух корней
solver = Splitter(
    input_pipe=discriminant_pipe,
    outputs_pipes=[
        lambda z: (-z[0][1] + z[1]) / (2 * z[0][0]),  # x1
        lambda z: (-z[0][1] - z[1]) / (2 * z[0][0]),  # x2
    ]
)

roots = solver(params)
print(roots)  # [3.0, -2.0]
```

### 3. Pipeline - Обработка последовательностей

```python
from pipes_and_filters import Pipeline, Pipe

# Шифр Цезаря
text = 'Hello'
key = 5

# Шифрование
encrypt_pipeline = Pipeline(
    source=text,
    pipe=Pipe(
        ord,           # Преобразование в ASCII
        lambda x: x + key,  # Сдвиг на ключ
        chr            # Обратно в символ
    )
)

encrypted_text = ''.join(encrypt_pipeline())

# Расшифровка
decrypt_pipeline = Pipeline(
    source=encrypted_text,
    pipe=Pipe(
        ord,
        lambda x: x - key,
        chr
    )
)

decrypted_text = ''.join(decrypt_pipeline())

print('Original text:', text)        # Original text: Hello
print('Encrypted text:', encrypted_text)  # Encrypted text: Mjqqt
print('Decrypted text:', decrypted_text)  # Decrypted text: Hello
```

### 4. Обработка числовых последовательностей

```python
from pipes_and_filters import Pipeline

# Возведение в квадрат чисел от 0 до 9
pipeline = Pipeline(
    source=range(10),
    pipe=lambda x: x ** 2
)

squares = list(pipeline())
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 5. Flow - Разделение и агрегация данных

**Flow** очень похож на **Pipeline**, но имеет ключевое отличие:
- **Pipeline** применяет одну функцию к каждому элементу и возвращает один результат
- **Flow** использует `splitter` (который возвращает множественные значения) и `sink` функцию для объединения этих значений в итоговый результат

Это позволяет Flow выполнять более сложную обработку данных, где необходимо разделить элемент на несколько компонентов и затем их агрегировать.

```python
from math import sqrt
from pipes_and_filters import Flow, Splitter
from pipes_and_filters.utils import identity

def std_dev(scores):
    """Расчет стандартного отклонения"""
    mean = sum(scores) / len(scores)
    return sqrt(sum((x - mean)**2 for x in scores) / len(scores))

def report(avg, max_score, min_score, score_range, std):
    """Форматирование отчета"""
    return f"Mean: {avg:.1f} | Max: {max_score} | Min: {min_score} | Range: {score_range} | Std Dev: {std:.1f}"

# Оценки студентов
student_scores = [
    [85, 92, 78, 96, 88],  # Студент 1
    [75, 68, 82, 91, 79],  # Студент 2
    [95, 85, 93, 87, 91],  # Студент 3
]

# Splitter для расчета статистики
stats_splitter = Splitter(
    input_pipe=identity,
    outputs_pipes=[
        lambda scores: sum(scores) / len(scores),  # среднее
        max,                                       # максимум
        min,                                       # минимум
        lambda scores: max(scores) - min(scores),  # диапазон
        std_dev                                    # стандартное отклонение
    ]
)

# Flow для обработки данных каждого студента
flow = Flow(
    source=student_scores,
    splitter=stats_splitter,
    sink=report
)

# Получение отчетов
for i, student_report in enumerate(flow(), 1):
    print(f"Student {i}: {student_report}")

# Вывод:
# Student 1: Mean: 87.8 | Max: 96 | Min: 78 | Range: 18 | Std Dev: 6.7
# Student 2: Mean: 79.0 | Max: 91 | Min: 68 | Range: 23 | Std Dev: 8.9
# Student 3: Mean: 90.2 | Max: 95 | Min: 85 | Range: 10 | Std Dev: 3.9
```

## API Reference

### Pipe

Класс для создания последовательности фильтров.

```python
class Pipe:
    def __init__(self, *filters):
        """
        Инициализирует pipe с набором фильтров.

        Args:
            *filters: Функции-фильтры для последовательного применения
        """

    def __call__(self, arg):
        """
        Применяет все фильтры последовательно к аргументу.

        Args:
            arg: Входные данные

        Returns:
            Результат применения всех фильтров
        """
```

### Splitter

Класс для разделения входного потока на несколько выходных.

```python
class Splitter:
    def __init__(self, input_pipe, outputs_pipes):
        """
        Инициализирует splitter.

        Args:
            input_pipe: Входной pipe для предварительной обработки
            outputs_pipes: Список pipe'ов для обработки результата input_pipe
        """

    def __call__(self, *args):
        """
        Применяет input_pipe, затем каждый из outputs_pipes к результату.

        Args:
            *args: Аргументы для input_pipe

        Returns:
            Список результатов от каждого output_pipe
        """
```

### Pipeline

Класс для обработки итерируемых источников данных.

```python
class Pipeline:
    def __init__(self, source, pipe):
        """
        Инициализирует pipeline.

        Args:
            source: Итерируемый источник данных
            pipe: Функция или Pipe для обработки каждого элемента
        """

    def __call__(self):
        """
        Генератор, который применяет pipe к каждому элементу source.

        Yields:
            Результат применения pipe к каждому элементу
        """
```

### Flow

Класс для объединения операций разделения и агрегации данных. Похож на Pipeline, но с ключевым отличием: использует splitter для получения множественных значений из каждого элемента и sink для их объединения.

```python
class Flow:
    def __init__(self, source, splitter, sink=lambda x: x):
        """
        Инициализирует flow.

        Args:
            source: Итерируемый источник данных
            splitter: Функция или Splitter, который обрабатывает каждый элемент
                     и возвращает множественные значения
            sink: Функция для объединения результатов splitter'а в итоговый результат
                 (по умолчанию - identity функция)
        """

    def __call__(self):
        """
        Генератор, который применяет splitter к каждому элементу source,
        а затем sink к результатам splitter'а.

        Yields:
            Результат применения sink к распакованным результатам splitter'а
            для каждого элемента source
        """
```

## Разработка

### Установка зависимостей для разработки

```bash
pip install -e .[dev]
```

### Запуск тестов

```bash
python -m pytest tests/
```

### Сборка пакета

```bash
python -m build
```

### Установка собранного пакета

```bash
pip install dist/pipes_and_filters-0.1.0-py3-none-any.whl
```

## Требования

- Python >= 3.7

## Лицензия

Этот проект создан Олегом Дудником (Oleggelo86@gmail.com).

## Примеры реального использования

Паттерн "Pipes and Filters" особенно полезен для:

- Обработки текстовых данных
- Валидации и трансформации данных
- Создания ETL пайплайнов
- Обработки изображений и сигналов
- Функционального программирования

Этот пакет предоставляет простые инструменты для реализации таких задач в элегантном и читаемом стиле.
