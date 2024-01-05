# 1288: Crear código de compra - Generar QR

## Activity

### Create QR code

```mermaid
sequenceDiagram
Frontend ->> Orchestrator: POST otp/validate
Note left of Frontend: In OTP validation view. <br>User enters OTP
Orchestrator->>CIAM: otp/validate
CIAM-->>Orchestrator: OK
Orchestrator->>CreditEngineAdapter:POST loans/{loanAccountId}/disbursement
CreditEngineAdapter->>Mambu: request disbursment
Mambu-->>CreditEngineAdapter: OK
CreditEngineAdapter-->>Orchestrator: OK
Orchestrator->>Orchestrator: Calcular 1a fecha de pago 
Orchestrator->>DynamoDB: store disbursement
Orchestrator->>DynamoDB: update creditDetails
Note left of DynamoDB: state=ACTIVO, substate=<br>DISPOCICION_AUTORIZADA
Orchestrator->>Orchestrator: create QR image
Orchestrator->>Frontend: details
Note left of Frontend: Show QR code view
```
### Scan QR code
```mermaid
sequenceDiagram
Frontend ->> Frontend: Scan QR code
Frontend ->> Orchestrator: POST loans/{loanAccountId}/use
Orchestrator->>DynamoDB: get credit application info
alt is valid
    Orchestrator->>DynamoDB: update credit details
    Note left of DynamoDB: state=ACTIVO<br>substate=DESEMBOLSADO
    Orchestrator->>Frontend: details
    Note left of Frontend: Show QR code view
else is not valid
    Orchestrator->>Frontend: 403
end
```

## Endpoints
### ~~Ver detalles de código de compra~~
```
REQUEST
GET credit-line/{id}/purchase/{id}

RESPONSES
200:
{ 
    "code" : string // el id/folio/codigo de compra
    "credit_id" : string
    "amount" : int // to display to the user
    "expiration_date" : date // to display to the user
    "state" : enum (**GENERADO**|USADO|VENCIDO)
    "created_at" : timestamp,
    "updated_at" : timestamp,
}
400 - Bad request
403 - Forbidden
404 - Not Found
```
### Validar código de compra
```
REQUEST
GET GET credit-line/{id}/purchase/{id}/valid

RESPONSES
200:
{
    "clientId" : string
    "provider" : string
    "amount" : int 
    "timestamp" : date 
    
    // suggested
    "status" : enum (**GENERADO**|USADO|VENCIDO) // to check if not used or expired
    "expiration_date" : date // check expiration date
}
400 - Bad request
403 - Forbidden
404 - Not Found
``````

## ER Diagram
```mermaid
erDiagram
    QR_DATA {
        string clientId FK "mambu client id"
        string loanAccountId FK "mambu loanAccount id"
        string provider  "associate purchase line"
        string amount  "loan amount"
        string code "loan code"
        enum status "TBD: one of GENERATED | USED | EXPIRED | ACTIVE"
        enum sub_status "TBD: one of DISPOSICION_AUTORIZADA| DESEMBOLSADA"
        dateTime submitDateTime "request timestamp"
        dateTime expirationDateTime "expiration timestamp"
    }
```

## Questions
- Definir si el código QR se genera en el front end o si la guardamos en la based de dato en base64/redis, o en S3
- Como se va a leer el código QR? Cuando se lea que es lo que debe haber tras el QR code? el código como texto, una url, etc?


