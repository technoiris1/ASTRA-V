'''
ASTRA-V flight code
this is most probably not going to be used in its current form as once i get im going to do a lot of testing
and things are going to change a lot over iterations but this is my interpretation of what its base would look like

note - AI was used in creation of this code as this is something not going to be used to fire the rocket.
'''
from machine import Pin, I2C, UART, PWM
import time
import uos

PLACEHOLDER_FUEL_SERVO_PIN = 14
PLACEHOLDER_IGNITER_SERVO_PIN = 15
PLACEHOLDER_LEG_SERVO_PINS = [18,19,20,21]

PLACEHOLDER_I2C_SDA = 0
PLACEHOLDER_I2C_SCL = 1

PLACEHOLDER_TFLUNA_UART0_TX = 0
PLACEHOLDER_TFLUNA_UART0_RX = 1
PLACEHOLDER_TFLUNA_UART1_TX = 4
PLACEHOLDER_TFLUNA_UART1_RX = 5

PLACEHOLDER_TRIGGER_PIN = 6

PLACEHOLDER_ARM_SWITCH_PIN = 7

PLACEHOLDER_IGNITER_POWER_PIN = 10

TF_LUNA_BAUD = 115200

SERVO_FREQ = 50

SERVO_MIN_US = 500
SERVO_MAX_US = 2500

APOGEE_SHUTOFF_FT = 15.0
APOGEE_SHUTOFF_M = APogee_cut = APOL = APOGEE_SHUTOFF_FT * 0.3048

REAPPLY_ALT_LOW_FT = 4.5
REAPPLY_ALT_HIGH_FT = 5.0
REAPPLY_ALT_LOW_M = REAPPLY_ALT_LOW_FT * 0.3048
REAPPLY_ALT_HIGH_M = REAPPLY_ALT_HIGH_FT * 0.3048

VALVE_OPEN_MS = 250
IGNITE_PULSE_MS = 200
ARM_HOLD_MS = 2000
SAFETY_TIMEOUT_MS = 20000

LOG_FILENAME = "log.csv"

def pwm_us_to_duty(us):

    period_us = 1_000_000 // SERVO_FREQ
    duty = int((us / period_us) * 65535)
    if duty < 0: duty = 0
    if duty > 65535: duty = 65535
    return duty

class Servo:
    def __init__(self, pwm_pin):
        self.pwm = PWM(Pin(pwm_pin))
        self.pwm.freq(SERVO_FREQ)
        self.min_us = SERVO_MIN_US
        self.max_us = SERVO_MAX_US

    def set_us(self, us):
        duty = pwm_us_to_duty(us)
        self.pwm.duty_u16(duty)

    def set_angle(self, angle):

        us = self.min_us + (self.max_us - self.min_us) * (angle/180.0)
        self.set_us(int(us))

    def detach(self):
        self.pwm.deinit()

i2c = I2C(0, scl=Pin(PLACEHOLDER_I2C_SCL), sda=Pin(PLACEHOLDER_I2C_SDA), freq=400000)

MPU_ADDR = 0x68
def init_mpu6050():
    try:
        i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')

        print("MPU6050 init OK")
    except Exception as e:
        print("MPU6050 init failed:", e)

def read_mpu6050():

    try:
        data = i2c.readfrom_mem(MPU_ADDR, 0x3B, 14)
        ax = int.from_bytes(data[0:2], 'big', signed=True) / 16384.0
        ay = int.from_bytes(data[2:4], 'big', signed=True) / 16384.0
        az = int.from_bytes(data[4:6], 'big', signed=True) / 16384.0
        gx = int.from_bytes(data[8:10], 'big', signed=True) / 131.0
        gy = int.from_bytes(data[10:12], 'big', signed=True) / 131.0
        gz = int.from_bytes(data[12:14], 'big', signed=True) / 131.0
        return (ax, ay, az, gx, gy, gz)
    except Exception as e:

        return (None, None, None, None, None, None)

BMP_ADDR = 0x76

def init_bmp280():
    try:

        i2c.writeto_mem(BMP_ADDR, 0xE0, b'\xB6')
        time.sleep_ms(2)

        i2c.writeto_mem(BMP_ADDR, 0xF4, b'\x27')
        i2c.writeto_mem(BMP_ADDR, 0xF5, b'\xA0')

        calib = i2c.readfrom_mem(BMP_ADDR, 0x88, 24)

        global dig_T1, dig_T2, dig_T3, dig_P1, dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9
        dig_T1 = int.from_bytes(calib[0:2], 'little')
        dig_T2 = int.from_bytes(calib[2:4], 'little', signed=True)
        dig_T3 = int.from_bytes(calib[4:6], 'little', signed=True)
        dig_P1 = int.from_bytes(calib[6:8], 'little')
        dig_P2 = int.from_bytes(calib[8:10], 'little', signed=True)
        dig_P3 = int.from_bytes(calib[10:12], 'little', signed=True)
        dig_P4 = int.from_bytes(calib[12:14], 'little', signed=True)
        dig_P5 = int.from_bytes(calib[14:16], 'little', signed=True)
        dig_P6 = int.from_bytes(calib[16:18], 'little', signed=True)
        dig_P7 = int.from_bytes(calib[18:20], 'little', signed=True)
        dig_P8 = int.from_bytes(calib[20:22], 'little', signed=True)
        dig_P9 = int.from_bytes(calib[22:24], 'little', signed=True)
        print("BMP280 init OK")
    except Exception as e:
        print("BMP280 init failed:", e)

t_fine = 0
def read_bmp280():

    global t_fine
    try:
        data = i2c.readfrom_mem(BMP_ADDR, 0xF7, 6)
        pres_raw = (data[0]<<12) | (data[1]<<4) | (data[2]>>4)
        temp_raw = (data[3]<<12) | (data[4]<<4) | (data[5]>>4)

        var1 = (((temp_raw>>3) - (dig_T1<<1)) * dig_T2) >> 11
        var2 = (((((temp_raw>>4) - dig_T1) * ((temp_raw>>4) - dig_T1)) >> 12) * dig_T3) >> 14
        t_fine = var1 + var2
        temp_c = ((t_fine * 5) + 128) >> 8
        temp_c = temp_c / 100.0

        var1_p = t_fine - 128000
        var2_p = var1_p * var1_p * dig_P6
        var2_p = var2_p + ((var1_p * dig_P5) << 17)
        var2_p = var2_p + (dig_P4 << 35)
        var1_p = ((var1_p * var1_p * dig_P3) >> 8) + ((var1_p * dig_P2) << 12)
        var1_p = (((1 << 47) + var1_p) * dig_P1) >> 33
        if var1_p == 0:
            return (temp_c, None)
        p = 1048576 - pres_raw
        p = int((((p << 31) - var2_p) * 3125) / var1_p)
        var1_p = (dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2_p = (dig_P8 * p) >> 19
        p = ((p + var1_p + var2_p) >> 8) + (dig_P7 << 4)
        pressure = p / 256.0
        return (temp_c, pressure)
    except Exception as e:

        return (None, None)

class TFLuna:
    def __init__(self, uart_id, rx_pin, tx_pin=None):

        self.uart = UART(uart_id, baudrate=TF_LUNA_BAUD, rx=Pin(rx_pin), tx=Pin(tx_pin) if tx_pin is not None else None)

        while self.uart.any():
            self.uart.read()

    def read_distance(self):

        if self.uart.any() < 9:
            return None
        data = self.uart.read(9)

        idx = data.find(b'\x59\x59')
        if idx == -1:

            self.uart.read(1)
            return None
        if idx + 9 > len(data):
            return None
        frame = data[idx:idx+9]

        dist = frame[2] + (frame[3] << 8)
        strength = frame[4] + (frame[5] << 8)
        temp = frame[6] + frame[7] / 100.0

        return dist / 100.0

fuel_servo = Servo(PLACEHOLDER_FUEL_SERVO_PIN)
igniter_servo = Servo(PLACEHOLDER_IGNITER_SERVO_PIN)
leg_servos = [Servo(p) for p in PLACEHOLDER_LEG_SERVO_PINS]
other_servos = [Servo(p) for p in PLACEHOLDER_OTHER_SERVO_PINS]

igniter_power = Pin(PLACEHOLDER_IGNITER_POWER_PIN, Pin.OUT)
igniter_power.value(0)

trigger_pin = Pin(PLACEHOLDER_TRIGGER_PIN, Pin.IN, Pin.PULL_DOWN)
arm_switch = Pin(PLACEHOLDER_ARM_SWITCH_PIN, Pin.IN, Pin.PULL_DOWN)

tfluna0 = TFLuna(0, PLACEHOLDER_TFLUNA_UART0_RX, PLACEHOLDER_TFLUNA_UART0_TX)
tfluna1 = TFLuna(1, PLACEHOLDER_TFLUNA_UART1_RX, PLACEHOLDER_TFLUNA_UART1_TX)

init_mpu6050()
init_bmp280()

def log_init():

    try:
        if LOG_FILENAME not in uos.listdir():
            with open(LOG_FILENAME, "w") as f:
                f.write("t_ms, state, ax,ay,az,gx,gy,gz, tempC, pressurePa, dist0_m, dist1_m\n")
    except Exception as e:
        print("Log init error:", e)

def log_row(state, ax,ay,az,gx,gy,gz, tempC, pressure, d0, d1):
    t_ms = time.ticks_ms()
    try:
        with open(LOG_FILENAME, "a") as f:
            f.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(
                t_ms, state,
                ax if ax is not None else "",
                ay if ay is not None else "",
                az if az is not None else "",
                gx if gx is not None else "",
                gy if gy is not None else "",
                gz if gz is not None else "",
                tempC if tempC is not None else "",
                pressure if pressure is not None else "",
                d0 if d0 is not None else "",
                d1 if d1 is not None else ""
            ))
    except Exception as e:
        print("Log write err", e)

def servo_open_fuel():

    fuel_servo.set_angle(120)

def servo_close_fuel():
    fuel_servo.set_angle(10)

def servo_ignite_press():

    igniter_servo.set_angle(120)

def servo_ignite_release():
    igniter_servo.set_angle(10)

def deploy_legs():
    for s in leg_servos:
        s.set_angle(90)
        time.sleep_ms(100)

    time.sleep(1)
    for s in leg_servos:
        s.detach()

def wait_for_arm():
    print("Waiting for ARM switch ON and hold {} ms...".format(ARM_HOLD_MS))
    while True:
        if arm_switch.value():
            t0 = time.ticks_ms()
            while arm_switch.value():
                if time.ticks_diff(time.ticks_ms(), t0) >= ARM_HOLD_MS:
                    print("ARM confirmed")
                    return True
                time.sleep_ms(10)
        time.sleep_ms(50)

def wait_for_trigger(timeout_ms=None):
    print("Waiting for trigger signal (nRF) or manual input...")
    start = time.ticks_ms()
    while True:
        if trigger_pin.value():
            print("Trigger received")
            return True
        if timeout_ms is not None and time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            print("Trigger wait timeout")
            return False
        time.sleep_ms(20)

def fire_sequence_once():

    t_start = time.ticks_ms()
    servo_open_fuel()
    time.sleep_ms(30)

    try:
        igniter_power.value(1)
    except:
        pass
    servo_ignite_press()
    time.sleep_ms(IGNITE_PULSE_MS)
    servo_ignite_release()
    try:
        igniter_power.value(0)
    except:
        pass

    time.sleep_ms(VALVE_OPEN_MS - IGNITE_PULSE_MS if VALVE_OPEN_MS>IGNITE_PULSE_MS else 50)
    servo_close_fuel()
    return time.ticks_diff(time.ticks_ms(), t_start)

def read_lidars():
    d0 = tfluna0.read_distance()
    d1 = tfluna1.read_distance()
    return d0, d1

def mission_main_loop():
    log_init()
    print("Entering mission control loop.")

    if not wait_for_arm():
        print("Not armed.")
        return

    if not wait_for_trigger(timeout_ms=60000):
        print("No trigger - abort.")
        return

    print("Trigger accepted - starting initial burn")
    state = "initial_burn"
    burn_start = time.ticks_ms()

    servo_open_fuel()

    time.sleep_ms(40)
    try:
        igniter_power.value(1)
    except:
        pass
    servo_ignite_press()
    time.sleep_ms(IGNITE_PULSE_MS)
    servo_ignite_release()
    try:
        igniter_power.value(0)
    except:
        pass

    apogee_reached = False
    shutoff_time = None
    while True:

        ax,ay,az,gx,gy,gz = read_mpu6050()
        tempC, pressure = read_bmp280()
        d0, d1 = read_lidars()

        alt_m = None
        if d0 is not None and d1 is not None:
            alt_m = min(d0,d1)
        elif d0 is not None:
            alt_m = d0
        elif d1 is not None:
            alt_m = d1

        log_row(state, ax,ay,az,gx,gy,gz, tempC, pressure, d0, d1)

        if alt_m is not None and alt_m >= APogee_cut:
            print("Apogee threshold reached (alt_m={:.2f} m) - shutting off fuel".format(alt_m))
            servo_close_fuel()
            shutoff_time = time.ticks_ms()
            apogee_reached = True
            state = "coast_freefall"
            break

        if time.ticks_diff(time.ticks_ms(), burn_start) > SAFETY_TIMEOUT_MS:
            print("Safety timeout - shutting off")
            servo_close_fuel()
            state = "aborted_timeout"
            return

        time.sleep_ms(30)

    print("Monitoring for reapply window ({}-{} ft => {:.3f}-{:.3f} m)".format(
        REAPPLY_ALT_LOW_FT, REAPPLY_ALT_HIGH_FT, REAPPLY_ALT_LOW_M, REAPPLY_ALT_HIGH_M))
    reapply_done = False
    start_coast = time.ticks_ms()
    while True:
        ax,ay,az,gx,gy,gz = read_mpu6050()
        tempC, pressure = read_bmp280()
        d0, d1 = read_lidars()
        alt_m = None
        if d0 is not None and d1 is not None:
            alt_m = min(d0,d1)
        elif d0 is not None:
            alt_m = d0
        elif d1 is not None:
            alt_m = d1

        log_row(state, ax,ay,az,gx,gy,gz, tempC, pressure, d0, d1)

        if alt_m is not None and REAPPLY_ALT_LOW_M <= alt_m <= REAPPLY_ALT_HIGH_M:
            print("Reapply window hit (alt {:.2f} m). Pulsing thruster.".format(alt_m))

            servo_open_fuel()
            time.sleep_ms(30)
            try:
                igniter_power.value(1)
            except:
                pass
            servo_ignite_press()
            time.sleep_ms(IGNITE_PULSE_MS)
            servo_ignite_release()
            try:
                igniter_power.value(0)
            except:
                pass

            servo_close_fuel()

            print("Bounce pulse done. Deploying legs.")
            deploy_legs()
            reapply_done = True
            state = "post_bounce"
            break

        if time.ticks_diff(time.ticks_ms(), start_coast) > 120000:
            print("Coast timeout - abort")
            break

        time.sleep_ms(40)

    print("Mission sequence complete. Disarming servos.")

    for s in other_servos:
        s.detach()
    fuel_servo.detach()
    igniter_servo.detach()

if __name__ == "__main__":
    try:
        mission_main_loop()
    except Exception as e:
        print("Fatal error in mission:", e)

        try:
            servo_close_fuel()
            servo_ignite_release()
        except:
            pass
