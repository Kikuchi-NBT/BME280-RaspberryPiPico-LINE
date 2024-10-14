from machine import I2C, Pin
import bme280
import utime

# 海面気圧 P0 (hPa)
SEA_LEVEL_PRESSURE = 1010

# I2Cインスタンスの作成
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

# BME280センサーのインスタンス化
bme = bme280.BME280(i2c=i2c)

# 標高を計算する関数
def calculate_altitude(pressure_hpa, temperature_c):
    # 温度をケルビンに変換
    temperature_k = temperature_c + 273.15
    # 標高の計算
    return ((((SEA_LEVEL_PRESSURE / pressure_hpa) ** 0.1903) - 1) * temperature_k) / 0.0065

while True:
    # センサーから気圧、温度、湿度を読み取る
    temp, pressure, humidity = bme.read_compensated_data()

    # hPa単位に変換
    pressure_hpa = pressure / 25600

    # 標高を計算
    altitude = calculate_altitude(pressure_hpa, temp / 100)

    # 測定値を出力
    print("Pressure: {:.2f} hPa, Altitude: {:.2f} meters, Temperature: {:.2f} C, Humidity: {:.2f}".format(pressure_hpa, altitude, temp / 100, humidity / 1024))

    import machine, utime
    import network, urequests
    from ssid import SSID, PASS

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASS)

    from linenotify import LineNotify

    # Line token
    TOKEN = 'あなたのLINEトークン'

    # Make instance
    line = LineNotify(TOKEN)

    # Send text message
    print("テキスト送信中")
    result = line.notify("Pressure: {:.2f} hPa, Temperature: {:.2f} C, Humidity: {:.2f}".format(pressure_hpa, temp / 100, humidity / 1024))
    print("result:", result)

    # 5秒待機→2時間待機に変更
    utime.sleep_ms(7200000)


