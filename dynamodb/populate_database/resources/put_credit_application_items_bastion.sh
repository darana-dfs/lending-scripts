aws dynamodb create-table --cli-input-json file://table_schema.json

aws dynamodb put-item --table-name CreditApplication --item file://credit_application/credit_application_details.json
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/credit_details.json
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/incode_session.json
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/prospect_address.json
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/prospect_housing.json
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/prospect_identity.json         
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/prospect_personal_references.json
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/prospect_validations.json
aws dynamodb put-item --table-name CreditApplication --item file://credit_application/step_details.json

aws dynamodb put-item --table-name Catalogs --item file://catalogs/CBU_1.json
aws dynamodb put-item --table-name Catalogs --item file://catalogs/CBU_2.json
aws dynamodb put-item --table-name Catalogs --item file://catalogs/PPO_1.json
aws dynamodb put-item --table-name Catalogs --item file://catalogs/PPO_2.json
aws dynamodb put-item --table-name Catalogs --item file://catalogs/TAC_1.json
aws dynamodb put-item --table-name Catalogs --item file://catalogs/TAC_2.json