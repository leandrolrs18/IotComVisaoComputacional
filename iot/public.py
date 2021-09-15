import publisher as pb

publicar = pb.Publisher()
client = publicar.connect_mqtt
publicar.publish(client)
