from SimpleStepperDriverV1 import SimpleStepperDriverV1
import time



ssd = SimpleStepperDriverV1(method='rtu',serialPort = '/dev/ttyACM0')
#print(ssd.getUid(?))
# ssd.writeD0(True)
# print(ssd.readA5(),ssd.readA4())
# ssd.writeD0(0)
# ssd.on()
# ssd.on()
ssd.on()
ssd.stop()


while(1):
#     ssd.go_forward(steps_per_second=200,steps=200)
#     time.sleep(1)
#     ssd.go_backward(steps_per_second=200,steps=200)
    # print(ssd.readA0())
    ssd.go_backward(steps =100 ,steps_per_second=100)
    time.sleep(1)
    ssd.go_forward(steps =100 ,steps_per_second=100)
    time.sleep(1)
    # print(ssd.get_steps_from_start())
  # print(ssd.readMap())
    # ssd.stop()