562 Vista de linea de credito
---
- Faltaría definir los estados y sub-estados de la linea de crédito y del código de compra

591 Codigo de compra
---
- Hay user story para expirar los códigos generados? Se puede usar redis y guardar el id de redis en la base de datos en vez o además del código
- no se menciona el base64 encoding en la descripción de la story, es con base64 que debe proporcionar el código de compra el endpoint que lo genere?
- de que está compuesto el código de compra? Se menciona el encodeKey de Mambu.. ¿ “encodeKey” == “código de compra” o el encodeKey es una parte del código de compra?
- que es lo que encodea el código QR? el “código de compra” como texto o una URL por ejemplo que valide el código de compra?
- Se pueden crear varios codigos de compra que esten activos al mismo tiempo?
- Cuales son los terminos de la linea de credito y codigo de compra en ingles y a que corresponden en mambu

1288 Generate QR code
----
- Definir si el código QR se genra en el front end o si la guardamos en la based de dato en base64/redis, o en S3
- Como se va a leer el código QR? Cuando se lea que es lo que debe haber tras el QR code? el código como texto, una url, etc?

1290 Download image
---
- se require guardar la imagen en alguna base de datos de objetos e.g. S3 o se puede generar cada vez que se solicite?
- se va a generar en el backend (podría guardarse) o en el frontend (más factible por la reutilización de estilos y diseños que posiblemente se puedan transformar de HTML a imagen)? 

1291 Share code on mobile
---
- No se especifican los canales a través de los cuales se compartirá el código
- El link de compartir de cada canal será determinado en el frontend o en backend?
- No se especifica si se requiere guardar información en la base de datos sobre lo que se comparte (e.g. compartido en whatsapp el día X, descargado el día X en mobil con ip, etc)


Aparte
---
- LEER ESTO: https://digitalfemsa.atlassian.net/wiki/spaces/Lending/pages/523993510/Changarros+Landing+Page
