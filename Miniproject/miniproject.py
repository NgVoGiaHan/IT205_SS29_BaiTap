import sys
from abc import ABC, abstractmethod

class BaseDevice(ABC):
    factory_name = "Rikkei Smart Factory"
    base_maintenance_cost = 1000000

    def __init__(self, device_code, device_name):
        if not self.validate_device_code(device_code):
            raise ValueError("ERR-IOT-01")
        self.device_code = device_code
        self._device_name = device_name.strip().upper()
        self.__operating_hours = 0

    @property
    def device_name(self):
        return self._device_name

    @device_name.setter
    def device_name(self, value):
        self._device_name = value.strip().upper()

    @property
    def operating_hours(self):
        return self.__operating_hours

    def add_hours(self, hours):
        if hours <= 0:
            raise ValueError("ERR-IOT-03")
        self.__operating_hours += hours

    @abstractmethod
    def track_performance(self, *args, **kwargs):
        pass

    @abstractmethod
    def run_diagnostic(self):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError("ERR-IOT-04")
        return self.operating_hours + other.operating_hours

    def __lt__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError("ERR-IOT-04")
        return self.operating_hours < other.operating_hours

    @staticmethod
    def validate_device_code(device_code):
        return len(device_code) == 10 and device_code[0].isalpha()

    @classmethod
    def update_maintenance_cost(cls, new_cost):
        cls.base_maintenance_cost = new_cost


class ProductionRobot(BaseDevice):
    def __init__(self, device_code, device_name):
        super().__init__(device_code, device_name)
        self.completed_products = 0

    def track_performance(self, hours, products):
        self.add_hours(hours)
        if products < 0:
            raise ValueError("ERR-IOT-03")
        self.completed_products += products
        if self.operating_hours > 0:
            return (self.completed_products / (self.operating_hours * 100)) * 100
        return 0.0

    def run_diagnostic(self):
        if self.completed_products > 10000:
            return f"Nguy hiểm: Cảnh báo bảo dưỡng! Sản lượng vượt 10,000 sản phẩm.\nĐịnh mức chi phí bảo trì hệ thống dự kiến: {self.base_maintenance_cost:,} VND"
        return "Trạng thái bình thường"


class ThermalSensor(BaseDevice):
    def __init__(self, device_code, device_name, safety_threshold=80.0):
        super().__init__(device_code, device_name)
        self.current_temperature = 0.0
        self.safety_threshold = safety_threshold

    def track_performance(self, hours, temperature):
        self.add_hours(hours)
        if temperature < 0:
            raise ValueError("ERR-IOT-03")
        self.current_temperature = temperature
        return self.current_temperature

    def run_diagnostic(self):
        if self.current_temperature > self.safety_threshold:
            return f"Nguy hiểm: Vượt ngưỡng nhiệt! (Nhiệt độ hiện tại: {self.current_temperature} độ C / Ngưỡng an toàn: {self.safety_threshold} độ C)\nĐịnh mức chi phí bảo trì hệ thống dự kiến: {self.base_maintenance_cost:,} VND"
        return "Trạng thái bình thường"


class HybridSmartActuator(ProductionRobot, ThermalSensor):
    def __init__(self, device_code, device_name, safety_threshold=80.0):
        BaseDevice.__init__(self, device_code, device_name)
        self.completed_products = 0
        self.current_temperature = 0.0
        self.safety_threshold = safety_threshold

    def track_performance(self, hours, products, temperature):
        self.add_hours(hours)
        if products < 0 or temperature < 0:
            raise ValueError("ERR-IOT-03")
        self.completed_products += products
        self.current_temperature = temperature
        return self.completed_products, self.current_temperature

    def run_diagnostic(self):
        issues = []
        if self.completed_products > 10000:
            issues.append("Sản lượng vượt 10,000")
        if self.current_temperature > self.safety_threshold:
            issues.append(f"Vượt ngưỡng nhiệt! (Nhiệt độ hiện tại: {self.current_temperature} độ C / Ngưỡng an toàn: {self.safety_threshold} độ C)")
        
        if issues:
            return f"Nguy hiểm: {' - '.join(issues)}\nĐịnh mức chi phí bảo trì hệ thống dự kiến: {self.base_maintenance_cost:,} VND"
        return "Trạng thái bình thường"


class MQTTEngineGateway:
    def process_stream(self, device):
        print("[Hệ thống MQTT Engine]: Đang khởi tạo băng thông kết nối dữ liệu IoT...")
        print(f"Dữ liệu của thiết bị {device.device_code} đã được đóng gói và xuất chuỗi luồng thành công.")


class ERPReportGateway:
    def process_stream(self, device):
        print("[Hệ thống ERP]: Đang đồng bộ số liệu...")
        print(f"Dữ liệu của thiết bị {device.device_code} đã được đồng bộ.")


def export_telemetry_data(data_gateway, device_object):
    if not hasattr(data_gateway, 'process_stream') or not callable(getattr(data_gateway, 'process_stream')):
        print("[Lỗi] (ERR-IOT-05): Xung đột kiến trúc! Không thể xuất dữ liệu do cấu hình cổng ngoại vi không tương thích.")
        return
    print("Xác thực cổng ngoại vi bằng Duck Typing thành công!")
    data_gateway.process_stream(device_object)


def print_error(code):
    errors = {
        "ERR-IOT-01": "[Lỗi] (ERR-IOT-01): Mã thiết bị không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng tiền tố quy định.",
        "ERR-IOT-02": "[Lỗi] (ERR-IOT-02): Thao tác bị từ chối! Hệ thống chưa có thông tin thiết bị hoạt động.",
        "ERR-IOT-03": "[Lỗi] (ERR-IOT-03): Định dạng dữ liệu sai! Giá trị nhập vào phải là số lớn hơn 0.",
        "ERR-IOT-04": "[Lỗi] (ERR-IOT-04): Lỗi kiểu dữ liệu! Không thể thực hiện toán tử với đối tượng ngoài hệ thống.",
        "ERR-IOT-05": "[Lỗi] (ERR-IOT-05): Xung đột kiến trúc! Không thể xuất dữ liệu do cấu hình cổng ngoại vi không tương thích.",
        "ERR-IOT-06": "[Lỗi] (ERR-IOT-06): Lựa chọn không hợp lệ! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 7."
    }
    print(errors.get(code, code))


def main():
    devices_list = []
    current_device = None

    while True:
        try:
            choice_input = input("Chọn chức năng (1-7): ")
            if not choice_input.isdigit():
                raise ValueError("ERR-IOT-06")
            
            choice = int(choice_input)
            if choice < 1 or choice > 7:
                raise ValueError("ERR-IOT-06")

            match choice:
                case 1:
                    print("--- ĐĂNG KÝ THIẾT BỊ IOT MỚI ---")
                    print("1. Production Robot (Robot sản xuất lắp ráp)\n2. Thermal Sensor (Cảm biến nhiệt độ)\n3. Hybrid Smart Actuator (Thiết bị truyền động lai)")
                    type_choice_input = input("Chọn phân loại thiết bị (1-3): ")
                    if not type_choice_input.isdigit() or int(type_choice_input) not in [1, 2, 3]:
                        print_error("ERR-IOT-06")
                        continue
                    
                    type_choice = int(type_choice_input)
                    code = input("Nhập mã thiết bị 10 ký tự: ")
                    name = input("Nhập tên thiết bị: ")

                    match type_choice:
                        case 1:
                            new_device = ProductionRobot(code, name)
                            type_name = "Robot sản xuất"
                        case 2:
                            new_device = ThermalSensor(code, name)
                            type_name = "Cảm biến nhiệt độ"
                        case 3:
                            new_device = HybridSmartActuator(code, name)
                            type_name = "Thiết bị truyền động lai"
                            
                    devices_list.append(new_device)
                    current_device = new_device
                    print(f"[Thành công]: Đăng ký {type_name} thành công!\nTên thiết bị: {current_device.device_name}")

                case 2 | 3 | 4 | 5 | 6 if not current_device:
                    raise ValueError("ERR-IOT-02")

                case 2:
                    print("--- THÔNG TIN THIẾT BỊ HIỆN TẠI ---")
                    print(f"Loại thiết bị: {current_device.__class__.__name__}")
                    print(f"Nhà máy: {current_device.factory_name}")
                    print(f"Mã thiết bị: {current_device.device_code}")
                    print(f"Tên thiết bị: {current_device.device_name}")
                    print(f"Số giờ vận hành: {current_device.operating_hours} giờ")
                    if hasattr(current_device, 'completed_products'):
                        print(f"Sản phẩm hoàn thành: {current_device.completed_products} sản phẩm")
                    if hasattr(current_device, 'current_temperature'):
                        print(f"Nhiệt độ hiện tại: {current_device.current_temperature} độ C")
                    mro_str = " -> ".join([cls.__name__ for cls in current_device.__class__.__mro__])
                    print(f"[Hệ thống MRO]: {mro_str}")

                case 3:
                    print("--- GHI NHẬN SỐ LIỆU VẬN HÀNH ---")
                    hours = float(input("Nhập số giờ chạy mới phát sinh: "))
                    match current_device:
                        case ProductionRobot() if not isinstance(current_device, HybridSmartActuator):
                            prods = int(input("Nhập số lượng sản phẩm hoàn thành mới bổ sung: "))
                            oee = current_device.track_performance(hours, prods)
                            print(f"[Thành công]: Đã cập nhật số liệu vận hành.\nTổng số giờ chạy tích lũy: {current_device.operating_hours} giờ.\nChỉ số hiệu suất thiết bị tổng thể (OEE): {oee:.1f}%")
                        case ThermalSensor() if not isinstance(current_device, HybridSmartActuator):
                            temp = float(input("Nhập nhiệt độ đo được: "))
                            current_device.track_performance(hours, temp)
                            print(f"[Thành công]: Đã cập nhật số liệu vận hành.\nTổng số giờ chạy tích lũy: {current_device.operating_hours} giờ.")
                        case HybridSmartActuator():
                            prods = int(input("Nhập số lượng sản phẩm hoàn thành mới bổ sung: "))
                            temp = float(input("Nhập nhiệt độ đo được: "))
                            current_device.track_performance(hours, prods, temp)
                            print(f"[Thành công]: Đã cập nhật số liệu vận hành.\nTổng số giờ chạy tích lũy: {current_device.operating_hours} giờ.")

                case 4:
                    print("--- QUY TRÌNH TỰ CHẨN ĐOÁN LỖI KỸ THUẬT ---")
                    diag = current_device.run_diagnostic()
                    if "Nguy hiểm" in diag:
                        print("[Cảnh báo hệ thống]: Thiết bị phát hiện trạng thái bất thường!")
                    print(f"Kết quả chẩn đoán: {diag}")

                case 5:
                    print("--- KIỂM KÊ & SO SÁNH TẢI (OPERATOR OVERLOADING) ---")
                    print(f"Thiết bị hiện tại (A): {current_device.device_code} (Số giờ chạy: {current_device.operating_hours} giờ)")
                    for idx, dev in enumerate(devices_list):
                        print(f"ID {idx}: {dev.device_code} - {dev.device_name} (Số giờ chạy: {dev.operating_hours} giờ)")
                    
                    idx_b = int(input("Chọn ID thiết bị đối ứng (B) từ danh sách: "))
                    if 0 <= idx_b < len(devices_list):
                        dev_b = devices_list[idx_b]
                        if current_device < dev_b:
                            print("[Kết quả So sánh (__lt__)]: Hao mòn (số giờ chạy) của thiết bị A ÍT HƠN thiết bị B.")
                        else:
                            print("[Kết quả So sánh (__lt__)]: Hao mòn (số giờ chạy) của thiết bị A KHÔNG ÍT HƠN thiết bị B.")
                        print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời gian tải vận hành của cả 2 thiết bị là: {current_device + dev_b} giờ.")
                    else:
                        print("ID không tồn tại trong danh sách.")

                case 6:
                    print("--- XUẤT DỮ LIỆU VẬN HÀNH RA CỔNG NGOẠI VI ---")
                    print("1. Xuất dữ liệu qua cổng MQTT (Cloud Stream)\n2. Đồng bộ số liệu vào hệ thống quản trị ERP")
                    gw_choice = int(input("Chọn cổng kết nối ngoại vi (1-2): "))
                    match gw_choice:
                        case 1:
                            export_telemetry_data(MQTTEngineGateway(), current_device)
                        case 2:
                            export_telemetry_data(ERPReportGateway(), current_device)
                        case _:
                            raise ValueError("ERR-IOT-06")

                case 7:
                    print("Cảm ơn bạn đã sử dụng hệ thống Quản lý Thiết bị Rikkei Smart Factory IoT Pro!")
                    sys.exit()

        except ValueError as e:
            if str(e) in ["ERR-IOT-01", "ERR-IOT-02", "ERR-IOT-03", "ERR-IOT-04", "ERR-IOT-05", "ERR-IOT-06"]:
                print_error(str(e))
            else:
                print_error("ERR-IOT-03")
        except TypeError as e:
            if str(e) == "ERR-IOT-04":
                print_error(str(e))
            else:
                print_error("ERR-IOT-04")

if __name__ == "__main__":
    main()