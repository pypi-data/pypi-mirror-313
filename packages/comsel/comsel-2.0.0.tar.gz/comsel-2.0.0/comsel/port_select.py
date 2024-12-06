import dearpygui.dearpygui as dpg
import serial.tools.list_ports
import re


class PortSelectionWindow:
    def __init__(self):
        self.selected_port = None
        self.selected_baudrate = None
        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.baudrates = ["9600", "19200", "38400", "57600", "115200"]
        self.is_window_open = True
        self.width = 440
        self.height = 210

    def update_com_ports(self):
        """Функция для обновления списка доступных COM портов."""
        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        if not self.available_ports:
            self.available_ports = ["No available COM ports."]
        # else:
        #     dpg.configure_item(label="", items=self.available_ports, default_value="115200", tag="baudrate_combo")
        dpg.configure_item("port_combo_select", items=self.available_ports, default_value=self.available_ports[0])

    def validate_port(self, port):
        """Проверка правильности COM порта."""
        pattern = r'^COM\d+$'  # Должен начинаться с 'COM' и быть числом
        return bool(re.match(pattern, port))

    def validate_baudrate(self, baudrate):
        """Проверка правильности скорости (Baudrate)."""
        try:
            baudrate = int(baudrate)
            return 1 <= baudrate <= 1000000  # Проверяем, что скорость в пределах допустимых значений
        except ValueError:
            return False  # Если это не число

    def on_confirm(self):
        """Обработка подтверждения выбора."""
        # Получаем выбранный COM порт из комбобокса или введенный вручную
        port = dpg.get_value("manual_port_input") if dpg.get_value("manual_port_input") else dpg.get_value("port_combo_select")
        baudrate = dpg.get_value("manual_baudrate_input") if dpg.get_value("manual_baudrate_input") else dpg.get_value("baudrate_combo")

        # Проверка введенных значений
        if port and baudrate:
            if self.validate_port(port) and self.validate_baudrate(baudrate):
                self.selected_port = port
                self.selected_baudrate = baudrate
                dpg.set_value("error_message", " ")  # Очистить ошибку
                dpg.stop_dearpygui()  # Закрыть окно после успешного выбора
            else:
                dpg.set_value("error_message", "Invalid COM port or Baudrate. Please check the values.")
        else:
            dpg.set_value("error_message", "Port or Baudrate was not selected or entered.")

    def show_window(self):
        """Создает окно выбора COM порта и скорости."""
        dpg.create_context()

        # Создаем окно
        with dpg.window(label="COM Port and Baudrate Selection", width=self.width, height=self.height, no_resize=True):
            # Основной горизонтальный контейнер
            with dpg.group(horizontal=True):
                # Левый контейнер (COM порты), ограничиваем ширину
                with dpg.group(width=200):  # Ограничиваем ширину для COM портов
                    dpg.add_text("Select COM port:")
                    if not self.available_ports:
                        self.available_ports = ["No available COM ports."]
                    dpg.add_combo(label="", items=self.available_ports, default_value=self.available_ports[0], tag="port_combo_select")
                    dpg.add_text("Or enter COM port manually:")
                    dpg.add_input_text(label="", tag="manual_port_input", hint="Enter COM port manually")
                    dpg.add_button(label="Update COM Ports", callback=self.update_com_ports)

                # Правая часть (Baudrate), ограничиваем ширину
                with dpg.group(width=200):  # Ограничиваем ширину для Baudrate
                    dpg.add_text("Select Baudrate:")
                    baudrates = ["9600", "19200", "38400", "57600", "115200"]
                    dpg.add_combo(label="", items=baudrates, default_value="115200", tag="baudrate_combo")
                    dpg.add_text("Or enter Baudrate manually:")
                    dpg.add_input_text(label="", tag="manual_baudrate_input", hint="Enter Baudrate manually")

            # Спейсер и кнопка подтверждения
            dpg.add_spacer(height=15)
            dpg.add_button(label="Confirm", callback=self.on_confirm, tag="confirm_button")
            dpg.add_text(" ", tag="error_message", color=(255, 0, 0))

        # Создаем основной viewport с уменьшенными размерами и отключаем изменение размера
        dpg.create_viewport(title='COM Port and Baudrate Selection', width=self.width, height=self.height, resizable=False)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        dpg.start_dearpygui()
        dpg.destroy_context()

    def get_selection(self):
        """Возвращает выбранные порт и скорость."""
        return self.selected_port, self.selected_baudrate


def select_com_port_and_baudrate():
    """
    Открывает окно выбора COM порта и скорости и возвращает результат.
    :return: Кортеж (port, baudrate) или (None, None), если выбор отменён.
    """
    window = PortSelectionWindow()
    window.show_window()
    return window.get_selection()
