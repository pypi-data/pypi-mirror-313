import wx
import serial.tools.list_ports
import re


class PortSelectionWindow(wx.Dialog):
    def __init__(self):
        super().__init__(None, title="Выбор COM порта и скорости", size=(450, 230))
        self.selected_port = None
        self.selected_baudrate = None

        # Основной layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Заголовок выбора порта
        port_label = wx.StaticText(self, label="Выберите или введите COM порт:")
        port_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(port_label, flag=wx.LEFT | wx.TOP, border=10)

        # COM-порт выбор
        port_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.port_combo = wx.ComboBox(self, choices=self.get_ports(), style=wx.CB_READONLY, size=(200, -1))
        self.port_combo.Bind(wx.EVT_COMBOBOX, self.on_selection_change)
        self.manual_port_input = wx.TextCtrl(self, size=(200, -1))
        self.manual_port_input.SetHint("Введите COM порт")
        self.manual_port_input.Bind(wx.EVT_TEXT, self.on_selection_change)
        port_sizer.Add(self.port_combo, flag=wx.RIGHT, border=5)
        port_sizer.Add(self.manual_port_input, flag=wx.LEFT, border=5)
        main_sizer.Add(port_sizer, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Заголовок выбора скорости
        baudrate_label = wx.StaticText(self, label="Выберите или введите скорость (Baudrate):")
        baudrate_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(baudrate_label, flag=wx.LEFT | wx.TOP, border=10)

        # Baudrate выбор
        baudrate_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.baudrate_combo = wx.ComboBox(self, choices=["9600", "19200", "38400", "57600", "115200"],
                                          style=wx.CB_READONLY, size=(200, -1))
        self.baudrate_combo.SetValue("115200")
        self.baudrate_combo.Bind(wx.EVT_COMBOBOX, self.on_selection_change)
        self.manual_baudrate_input = wx.TextCtrl(self, size=(200, -1))
        self.manual_baudrate_input.SetHint("Введите скорость")
        self.manual_baudrate_input.Bind(wx.EVT_TEXT, self.on_selection_change)
        baudrate_sizer.Add(self.baudrate_combo, flag=wx.RIGHT, border=5)
        baudrate_sizer.Add(self.manual_baudrate_input, flag=wx.LEFT, border=5)
        main_sizer.Add(baudrate_sizer, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Кнопки
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.confirm_button = wx.Button(self, label="Подтвердить")
        cancel_button = wx.Button(self, label="Отмена")
        self.confirm_button.Bind(wx.EVT_BUTTON, self.on_confirm)
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.confirm_button.Enable(False)  # Отключена по умолчанию
        button_sizer.Add(self.confirm_button, flag=wx.RIGHT, border=5)
        button_sizer.Add(cancel_button, flag=wx.LEFT, border=5)
        main_sizer.Add(button_sizer, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

        self.SetSizer(main_sizer)

    def get_ports(self):
        """Получает список доступных COM портов."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports if ports else ["Нет доступных портов"]

    def is_valid_port(self, port):
        """Проверяет корректность ввода COM-порта."""
        pattern = r'^COM\d+$'  # Проверяет, что порт имеет формат COM1, COM2 и т.д.
        return re.match(pattern, port) is not None

    def is_valid_baudrate(self, baudrate):
        """Проверяет корректность ввода скорости."""
        try:
            baudrate = int(baudrate)
            return 1 <= baudrate <= 1000000  # Ограничения на скорость
        except ValueError:
            return False

    def on_selection_change(self, event):
        """Активирует кнопку "Подтвердить", если ввод корректен."""
        manual_port = self.manual_port_input.GetValue().strip()
        manual_baudrate = self.manual_baudrate_input.GetValue().strip()
        selected_port = self.port_combo.GetValue()
        selected_baudrate = self.baudrate_combo.GetValue()

        # Проверяем ручной ввод или выбор из списка
        port = manual_port if manual_port else selected_port
        baudrate = manual_baudrate if manual_baudrate else selected_baudrate

        if port and self.is_valid_baudrate(baudrate) and self.is_valid_port(port):
            self.confirm_button.Enable(True)
        else:
            self.confirm_button.Enable(False)

    def on_confirm(self, event):
        """Обработка нажатия кнопки "Подтвердить"."""
        manual_port = self.manual_port_input.GetValue().strip()
        manual_baudrate = self.manual_baudrate_input.GetValue().strip()

        # Приоритет ручного ввода
        port = manual_port if manual_port else self.port_combo.GetValue()
        baudrate = manual_baudrate if manual_baudrate else self.baudrate_combo.GetValue()

        if not self.is_valid_port(port):
            wx.MessageBox("Некорректный COM порт! Используйте формат COM1, COM2 и т.д.", "Ошибка",
                          wx.OK | wx.ICON_ERROR)
            return

        if not self.is_valid_baudrate(baudrate):
            wx.MessageBox("Некорректная скорость! Скорость должна быть от 1 до 1000000.", "Ошибка",
                          wx.OK | wx.ICON_ERROR)
            return

        self.selected_port = port
        self.selected_baudrate = int(baudrate)
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        """Обработка нажатия кнопки "Отмена"."""
        self.EndModal(wx.ID_CANCEL)

    def get_selection(self):
        """Возвращает выбранные порт и скорость."""
        return self.selected_port, self.selected_baudrate


def select_com_port_and_baudrate():
    """
    Открывает окно выбора COM порта и скорости и возвращает результат.
    :return: Кортеж (port, baudrate) или (None, None), если выбор отменён.
    """
    app = wx.App(False)
    port_window = PortSelectionWindow()
    if port_window.ShowModal() == wx.ID_OK:
        result = port_window.get_selection()
    else:
        result = (None, None)
    port_window.Destroy()
    app.Destroy()
    return result


# Пример использования
if __name__ == "__main__":
    port, baudrate = select_com_port_and_baudrate()
    if port and baudrate:
        print(f"Выбран порт: {port}, скорость: {baudrate}")
    else:
        print("Порт или скорость не были выбраны.")
