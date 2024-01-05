Process
1. **KOF/Pronto** generan una orden de cobro hacia el cliente
1. Cliente decide hacer uso de línea de crédito y solicita generación de código QR con monto a requerir
1. Credit Application detona extracción de información actualizada del crédito del cliente con Mambú a través de Credit Enginc/CreditEngincAdapter y genera registro en DB
1. Mambú actualiza a Credit Engine/Credit Engine Adapter sobre el estatus actual de la cuenta y a su vez Credit Enactualiza la DB de Lending
1. Credit Engine/Credit Engine Adapter responde a Credit Application con el resultado de las validaciones y guarda en DB el resultado:
    1. Deuda. En caso de existir, el proceso termina
    2. Límite de crédito disponible. en caso de no ser suficiente para el monto solicitado, el proceso
    3. En cualquier caso registra en la BD de Lending el resultado de validaciones
1. En caso de ser exitosas las validaciones. Credit Application detona identifiación del usuario vía OTP y guarda registro en DB Lending el estado de la solicitud
1. CIAM envía OTP vía SMS al dispositivo móvil del cliente y guarda registro del resultado de dicha validación en DB
1. Lending valida el OTP introducido por el usuario, en caso erróneo, el proceso termina. En cualquier caso, guarda registro del resultado de dicha validación en DB
1. Credit Application detona la generación de la trx/compra y del código QR con los datos solicitados por el cliente en Disbursement y guarda el estado de la solicitud en DB
1. Disbursement genera folio de trx/compra y código QR en estados pendiente y con los siguientes datos:
    1. Identificador de trx
    2. Canal
    3. Monto
    4. Monto en centavos
    5. Vigencia
    6. Concepto
    7. Identificador Cliente
    8. Tipo Operacion
        - Hace registro en DB de estado y datos de trx/QR
        - Hace registro de la relación de trx hacia el cliente
        - Hace registro de la relación de trx hacia el catalogo de cuenta clabe por canal
1. Lending comparte al usuario el código QR generado
1. Cliente comparte el código al agente de KOF/Pronto. Kof/Pronto realiza lectura del código
1. Kof/Pronto envía los datos contenidos en el código QR hacia Lending para su validación y aplicación
1. Credit Application detona la segunda identifiación del usuario en la confirmación del pago vía OTP y guarda registro en DB Lending el estado de la solicitud
1. CIAM envía OTP vía SMS al dispositivo móvil del cliente para esta segunda identificación del usuario y guarda registro del resultado de dicha validación en DB
1. Lending valida el OTP introducido por el usuario en esta segunda Identificación del usuario, en caso erróneo, el proceso termina. En cualquier caso, guarda registro del resultado de dicha validación en
DB
1. Credit Application detona la validación del código QR/trx hacia disbursement y guarda el estado de la solicitud y código QR/Trx
1. Disbursement realiza validación:
    1. Datos de la trx original corresponden con los relacionados en el código QR (identificador de trx, monto, monto en centavos, vigencia, concepto, cliente)
    2. Valida la vigencia del código QR contra fecha/hora actual
        - en caso de no ser exitoso, el proceso termina y se comunica con usuario
1. Disbursement detona validación de deuda, saldo disponible y límite de crédito del cliente via Credit Engine/Credit Engine Adapter/Mambú
1. Credit Engine/Credit Engine Adapter realiza validación de deuda, límite de crédito y saldo. Guarda el resultado de las validaciones en DB. En caso de no ser exitosas el proceso termina.
1. Disbursement guarda el estado de la trx y de QR en DB
1. La lambda de Expiración de QR es ejecutada por Event Bridge periódicamente para consultar la BD en búsqueda Q no vigentes para cambiar al estado correspondiente
1. La lambda de Disbursements Disposal es ejecutada por levent errage perrodicamente para consulta
1. La lambda de Disbursements Disposal transforma el resultado de la consulta a DB en registros dentro de archivos con tamaño, esquema y formato definidos por BBVA en el bucket de S3 de dispersiones
1. El FTP Family Transfer Family de Lending liga la carpeta designada para aplicaciones de dispersión hacia las rutas predefinidas del bucket S3 de dispersiones
1. BBVA periódicamente extrae del FTP Transfer Family de Lending en la carpeta de dispersiones pendientes los archivos correspondientes al periodo de tiempo designado y los procesa para ejecutar
dichas dispersiones
1. BBVA deposita en la carpeta de respuestas de FTP Family de Lending el resultado de la ejecución de las dispersiones
1. La lambda de Disbursementes Responses procesa los archivos de resultado para realizar reintento de dispersión en caso de que sea necesario o para confirmar la dispersión hacia Kot/Pronto
1. En caso de reintento, la lambda de Disbursementes Responses genera el archivo de reintentos en la ruta designada para reintentos
1. En caso de reintento, la lambda de Disbursementes Responses registra en DB el estado de reintento y la fecha en la BD de Lending
1. En caso de éxito de dispersión, la lambda de Disbursementes Responses notifica via webhook a Kof/Pronto sobre dichas confirmaciones exitosas