# Программа для создания изображений на основе TKinter

Данная программа представляет собой пример использования библиотеки TKinter для создания графического интерфейса.

## Класс DrawingApp

Инициализация __init__(self, root)

Конструктор класса принимает один параметр:

- `root`: Это корневой виджет Tkinter, который служит контейнером для всего интерфейса приложения.

## Внутри конструктора выполняются следующие ключевые действия:

- Устанавливается заголовок окна приложения.
- Создается объект изображения (`self.image`) с использованием библиотеки Pillow. Это изображение служит виртуальным
  холстом, на котором происходит рисование. Изначально оно заполнено белым цветом.
- Инициализируется объект `ImageDraw.Draw(self.image)`, который позволяет рисовать на объекте изображения.
- Создается виджет Canvas Tkinter, который отображает графический интерфейс для рисования. Размеры холста установлены в
  600x400 пикселей.
- Вызывается метод `self.setup_ui()`, который настраивает элементы управления интерфейса.
- Привязываются обработчики событий к холсту для отслеживания движений мыши при рисовании () и сброса состояния кисти
  при отпускании кнопки мыши ().
- Добавляются горячие клавиши для быстрого доступа к функциям: `Ctrl+S` для сохранения изображения и `Ctrl+C` для выбора цвета.

## Метод setup_ui(self)

Этот метод отвечает за создание и расположение виджетов управления:

- Создает элементы управления интерфейсом: кнопки "Очистить", "Выбрать цвет", "Сохранить", меню выбора размера кисти.
- Вызывает метод `create_brush_size_menu` для создания меню выбора размера кисти.

## Метод create_brush_size_menu(self, parent, sizes)

- Создает меню выбора размера кисти с заданными вариантами размеров.
- Создает слайдер для выбора размера кисти.

## Метод update_brush_size(self, value)

- Обновляет значение размера кисти в соответствии с выбранным значением.

## Метод paint(self, event)

Функция вызывается при движении мыши с нажатой левой кнопкой по холсту. Она рисует линии на холсте Tkinter и параллельно
на объекте Image из Pillow:

- event: Событие содержит координаты мыши, которые используются для рисования.
- Линии рисуются между текущей и последней зафиксированной позициями курсора, что создает непрерывное изображение.
- Обновляет последние координаты кисти.

## Метод reset(self, event)

Сбрасывает последние координаты кисти.
Это необходимо для корректного начала новой линии после того, как пользователь отпустил кнопку мыши и снова начал
рисовать.

## Метод clear_canvas(self)

Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDraw для нового изображения.

## Метод choose_color(self)

Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.

## Метод save_image(self)

Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.

## Метод use_eraser(self) - "Ластик"

Функциональность "Ластика" представлена в приложении следующим образом:

- При нажатии на кнопку "Ластик" текущий цвет кисти изменяется на белый, что позволяет стирать нарисованные линии на
  холсте.

## Метод use_brush(self) 
Переключает режим на кисть (с восстановлением обратно цвета кисти).


## Метод pick_color(self, event)

Извлекает цвет пикселя в месте клика правой кнопкой мыши и устанавливает его в качестве текущего цвета кисти.

- `event`: Событие мыши.


## Метод rgb_to_hex(self, rgb)

Преобразует кортеж RGB в шестнадцатеричный код цвета.

- `rgb`: Кортеж из трех значений (R, G, B).



## Обработка событий

- `<B1-Motion>`: Событие привязано к методу paint, позволяя рисовать на холсте при перемещении мыши с нажатой левой
  кнопкой.

- `<ButtonRelease-1>`: Событие привязано к методу reset, который сбрасывает состояние рисования для начала новой линии.

- `<Button-2>`: Событие привязано к правой кнопке мыши (трекпада) для вызова метода pick_color.

- `<Control-s>`: Событие привязано к методу save_image, позволяя сохранять изображение через комбинацию клавиш.

- `<Control-c>`: Событие привязано к методу choose_color, позволяя выбирать цвет кисти через комбинацию клавиш.


## Использование приложения

Пользователь может рисовать на холсте, выбирать цвет и размер кисти, использовать функцию "Ластика", очищать холст и
сохранять в формате PNG.

## Тестирование

Код покрыт модульными тестами для проверки функциональности основных методов класса `DrawingApp`.
Тесты выполняются с использованием библиотеки `unittest.mock` для замены стандартных объектов и функций на макеты (
mocks) в целях изоляции тестируемого кода.
Тесты включают в себя проверку рисования на холсте, выбора цвета и размера кисти, использования функции "Ластика",
очистки холста и сохранения изображения в формате PNG.
Каждый тест проверяет определенное поведение методов класса `DrawingApp`, обеспечивая корректность работы приложения в
различных сценариях использования.

Если у вас есть еще какие-то запросы или требуется дополнительная информация, не стесняйтесь обращаться.
