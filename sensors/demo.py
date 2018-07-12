import tsl2561
import veml6070
import bme280
import json
import pika
import time





if __name__ == '__main__':


    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="queue")
    i = 0
    while i < 3:
        veml = veml6070.Veml6070()
        uv_raw = veml.get_uva_light_intensity_raw()
        uv = veml.get_uva_light_intensity()
        print "UVA Light value : %f W/(m*m) from raw value %d" % (uv, uv_raw)

        temperature,pressure,humidity = bme280.readBME280All()
        print "Temperature : ", temperature, "C"
        print "Pressure : ", pressure, "hPa"
        print "Humidity : ", humidity, "%"
        (ch0,ch1)= tsl2561.readValues()
        print "Full Spectrum(IR + Visible) :%d lux" %ch0
        print "Infrared Value :%d lux" %ch1
        print "Visible Value :%d lux" %(ch0 - ch1)

        datos= {
                "humedad": humidity,
                "temperatura": temperature,
          "presion": pressure,
          "UVA":{
             "UV": uv,
            "raw":uv_raw},
            "fullSpectrum": {
         "visible": (ch0-ch1),
         "infrarrojo": ch1
           },
          "fecha": time.strftime("%d/%m/%y"),
           "hora": time.strftime("%H:%M:%S")
          }

        message = json.dumps(datos)
        channel.basic_publish(exchange='', routing_key="queue", body=message)
        print(" [x] Sent datos to RabbitMQ")
        time.sleep(2)
        i+=1
    connection.close()
