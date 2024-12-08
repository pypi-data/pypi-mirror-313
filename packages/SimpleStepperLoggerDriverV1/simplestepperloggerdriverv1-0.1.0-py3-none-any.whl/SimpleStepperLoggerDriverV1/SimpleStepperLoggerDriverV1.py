from numpy import uint
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.client.tcp import ModbusTcpClient
import struct 


STEP_MODE_1_4=4

class SimpleStepperLoggerDriverV1:

    def __init__(self,method,ip=None,serialPort=None):
        if(method=='rtu'):
            self.client = ModbusSerialClient(method='rtu', port=serialPort, timeout=1,baudrate=460800)
        else:
            self.client = ModbusTcpClient(host=ip,port = 80)
        self.client.read_holding_registers(40040+9,1,slave=4)

    def uint16_to_float32(self,MSB,LSB):
        float32_msb = MSB.to_bytes(2, byteorder='big', signed=False)
        float32_lsb = LSB.to_bytes(2, byteorder='big', signed=False)
        float32_full = float32_msb + float32_lsb
        float32 = struct.unpack(">f",float32_full)
        return float32[0]

    def uint16_to_int32(self,MSB,LSB):
        int32_msb = MSB.to_bytes(2, byteorder='big', signed=False)
        int32_lsb = LSB.to_bytes(2, byteorder='big', signed=False)
        int32_full = int32_msb + int32_lsb
        int32 = struct.unpack(">l",int32_full)
        return int32[0]

    def float32_to_uint16_t(self,val):
        ba = bytearray(struct.pack(">f", val)) 
        msb = struct.unpack(">H",ba[0:2])
        lsb = struct.unpack(">H",ba[2:4])
        return msb[0],lsb[0]

    def int32_to_uint16(self,val):
        ba = bytearray(struct.pack(">l", val)) 
        msb = struct.unpack(">H",ba[0:2])
        lsb = struct.unpack(">H",ba[2:4])
        return msb[0],lsb[0]

    def uint32_to_uint16(self,val):
        ba = bytearray(struct.pack(">L", val)) 
        msb = struct.unpack(">H",ba[0:2])
        lsb = struct.unpack(">H",ba[2:4])
        return msb[0],lsb[0]

    def uint16_to_uint32(self,MSB,LSB):
        uint32_msb = MSB.to_bytes(2, byteorder='big', signed=False)
        uint32_lsb = LSB.to_bytes(2, byteorder='big', signed=False)
        uint32_full = uint32_msb + uint32_lsb
        uint32 = struct.unpack(">L",uint32_full)
        return uint32[0]

    def uint16_to_hex_string(self,uintArray):
        hexStr=b''
        for uint in uintArray:
            hexStr+=uint.to_bytes(2, byteorder='big', signed=False)
        return hexStr.hex()

    def getUid(self):
        rslt = self.client.read_holding_registers(40004,6,slave=4).registers
        return self.uint16_to_hex_string(rslt)

    def getType(self):
        rslt = self.client.read_holding_registers(40010,1,slave=4).registers
        return rslt[0] 

    def on(self):
        self.client.write_registers(40049+3,1,slave=4)

    def off(self):
        self.client.write_registers(40049+3,0,slave=4)

    def stop(self):
        self.client.write_registers(40049+8,0,slave=4)

    def get_steps_from_start(self):
        rslt = self.client.read_holding_registers(40049+9,2,slave=4).registers
        return self.uint16_to_int32(rslt[0],rslt[1])/STEP_MODE_1_4

    def go_forward(self,steps_per_second=10,steps=0):
        steps=int(steps)
        steps_per_second=int(steps_per_second)
        self.client.write_registers(40049+4,steps_per_second*STEP_MODE_1_4,slave=4)#Set speed
        if(steps==0):
            self.client.write_registers(40049+7,1,slave=4)
            self.client.write_registers(40049+5,self.int32_to_uint16(10),slave=4)#Set angle
        else:
            self.client.write_registers(40049+7,2,slave=4)
            self.client.write_registers(40049+5,self.int32_to_uint16(steps*STEP_MODE_1_4),slave=4)#Set angle
        self.client.write_registers(40049+8,1,slave=4)


    def go_backward(self,steps_per_second=10,steps=0):
        steps=int(steps)
        steps_per_second=int(steps_per_second)
        self.client.write_registers(40049+4,steps_per_second*STEP_MODE_1_4,slave=4)#Set speed
        if(steps==0):
            print('cont')
            self.client.write_registers(40049+7,1,slave=4)
            self.client.write_registers(40049+5,self.int32_to_uint16(-10),slave=4)#Set angle
        else:
            print('ang')
            self.client.write_registers(40049+7,2,slave=4)
            self.client.write_registers(40049+5,self.int32_to_uint16(-steps*STEP_MODE_1_4),slave=4)#Set angle
        self.client.write_registers(40049+8,1,slave=4)

    def readA0(self):
        response = self.client.read_input_registers(30000,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA1(self):
        response = self.client.read_input_registers(30002,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA2(self):
        response = self.client.read_input_registers(30004,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA3(self):
        response = self.client.read_input_registers(30006,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA4(self):
        response = self.client.read_input_registers(30008,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA5(self):
        response = self.client.read_input_registers(30010,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readD0(self):
        return self.client.read_coils(0x00,4,slave=4).bits[0]

    def writeD0(self,value):
        return self.client.write_coil(0x00, value,slave=4)

    def readA12(self):
        response = self.client.read_input_registers(30016,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA13(self):
        response = self.client.read_input_registers(30018,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def read14(self):
        response = self.client.read_input_registers(30020,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA15(self):
        response = self.client.read_input_registers(30022,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA12A13(self):
        response = self.client.read_input_registers(30024,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA14A15(self):
        response = self.client.read_input_registers(30026,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA16(self):
        response = self.client.read_input_registers(30028,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA17(self):
        response = self.client.read_input_registers(30030,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA18(self):
        response = self.client.read_input_registers(30032,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA19(self):
        response = self.client.read_input_registers(30034,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA16A17(self):
        response = self.client.read_input_registers(30036,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA18A19(self):
        response = self.client.read_input_registers(30038,2,slave=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readAllA(self):
        response = self.client.read_input_registers(30000,40,slave=4)
        result = []
        for i in range(0,len(response.registers),2):
            result.append(self.uint16_to_float32(response.registers[i],response.registers[i+1]))
        return result
