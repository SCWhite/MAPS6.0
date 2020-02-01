
#command code
leading_cmd             = 0xAA
GET_TEMP_HUM_cmd        = 0xB0
GET_CO2_cmd             = 0xB1
GET_TVOC_cmd            = 0xB2
GET_LIGHT_cmd           = 0xB3
GET_PMS_cmd             = 0xB4
GET_SENSOR_ALL_cmd      = 0xB5
GET_INFO_VERSION_cmd    = 0xB6
GET_INFO_RUNTIME_cmd    = 0xB7
GET_INFO_ERROR_LOG_cmd  = 0xB8
GET_INFO_SENSOR_POR_cmd = 0xB9 # V1.1 (Update)
GET_RTC_DATE_TIME_cmd   = 0xBA
GET_INFO_PIN_STATE_cmd  = 0xBB # V1.1 (New)

SET_STATUS_LED_cmd       = 0xBF # V1.1 (New)
SET_PIN_CO2_CAL_cmd      = 0xC0
SET_PIN_PMS_RESET_cmd    = 0xC1
SET_PIN_PMS_SET_cmd      = 0xC2
SET_PIN_NBIOT_PWRKEY_cmd = 0xC3
SET_PIN_NBIOT_SLEEP_cmd  = 0xC4
SET_PIN_LED_ALL_cmd      = 0xC5
SET_POLLING_SENSOR_cmd   = 0xC6 # V1.1 (Update)
SET_RTC_DATE_TIME_cmd    = 0xC7 # V1.1 (Update)
SET_PIN_FAN_ALL_cmd      = 0xC8 # V1.1 (New)

SET_PIN_CO2_CAL_key      = bytearray([0x53,0x38,0x4C,0x50])
SET_PIN_PMS_RESET_key    = bytearray([0x50,0x4D,0x53,0x33])
SET_PIN_PMS_SET_key      = bytearray([0x33,0x30,0x30,0x33])
SET_PIN_NBIOT_PWRKEY_key = bytearray([0x4E,0x42,0x2D,0x49])
SET_PIN_NBIOT_SLEEP_key  = bytearray([0x2D,0x49,0x4F,0x54])
SET_PIN_LED_ALL_key      = bytearray([0x53,0x4C,0x45,0x44])
SET_PIN_FAN_ALL_key      = bytearray([0x46,0x41,0x4E,0x63]) # V1.1 (New)


PROTOCOL_I2C_WRITE_cmd    = 0xCA
PROTOCOL_I2C_READ_cmd     = 0xCB
PROTOCOL_UART_BEGIN_cmd   = 0xCC
PROTOCOL_UART_TX_RX_cmd   = 0xCD # V1.1 (Update)
PROTOCOL_UART_TXRX_EX_cmd = 0xCE # V1.1 (New)

ENABLE_UART_ACTIVE_RX_cmd = 0xCF # V1.1 (New)
ECHO_UART_ACTIVE_RX_cmd   = 0xCF # V1.1 (New)

#expect receive

GET_TEMP_HUM_resp        = 8
GET_CO2_resp             = 8
GET_TVOC_resp            = 16
GET_LIGHT_resp           = 16
GET_PMS_resp             = 16
GET_SENSOR_ALL_resp      = 48
GET_INFO_VERSION_resp    = 6
GET_INFO_RUNTIME_resp    = 9
GET_INFO_ERROR_LOG_resp  = 16
GET_INFO_SENSOR_POR_resp = 16 # V1.1 (Update)
GET_RTC_DATE_TIME_resp   = 10
GET_INFO_PIN_STATE_resp  = 11 # V1.1 (New)

SET_STATUS_LED_resp       = 4 # V1.1 (New)
SET_PIN_CO2_CAL_resp      = 4
SET_PIN_PMS_RESET_resp    = 4
SET_PIN_PMS_SET_resp      = 4
SET_PIN_NBIOT_PWRKEY_resp = 4
SET_PIN_NBIOT_SLEEP_resp  = 4
SET_PIN_LED_ALL_resp      = 4
SET_POLLING_SENSOR_resp   = 4 # V1.1 (Update)
SET_RTC_DATE_TIME_resp    = 4 # V1.1 (Update)
SET_PIN_FAN_ALL_resp      = 4 # V1.1 (New)

PROTOCOL_I2C_WRITE_resp    = 4
#PROTOCOL_I2C_READ_resp     = 6+n
PROTOCOL_UART_BEGIN_resp   = 4
#PROTOCOL_UART_TX_RX_resp   = 6+n # V1.1 (Update)
#PROTOCOL_UART_TXRX_EX_resp = 8+n # V1.1 (New)

ENABLE_UART_ACTIVE_RX_resp = 4 # V1.1 (New)
#ECHO_UART_ACTIVE_RX_resp   = 7+n # V1.1 (New)


class MAPSV6_MCU(object):
    def __init__(self, address=COM57, i2c=None,**kwargs):
        # self._logger = logging.getLogger('Adafruit_SHT.SHT31D')
        # # Create I2C device.
        # if i？2c is None:
        #     import Adafruit_GPIO.I2C as I2C
        #     i2c = I2C
        # self._device = i2c.get_i2c_device(address, **kwargs)
        time.sleep(5)  # Wait the required time

     def 