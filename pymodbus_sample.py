from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusUdpClient

client = ModbusUdpClient("192.168.1.100", 5002, strict=False)
connection = client.connect()

if (connection):
    request = client.read_holding_registers(0, 12)
    if (request.isError()):
        print(request)
    else:
        result = request.registers
        print(result)

# [200, 0, 300, 0, 100, 0, 300, 0, 700, 0, 100, 0]
# client.write_registers(0, [10, 0])
# client.write_registers(2, [100, 0])
# client.write_registers(4, [400, 0])
# from datascience import machine_learning
# machine_learning()
# [11, 0, 37, 0, 85, 0, 51, 0, 50, 0, 86, 0]
# client.write_registers(0, machine_learning())