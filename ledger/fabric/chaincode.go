package chaincode

import (
 "encoding/json"
 "fmt"
 "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type Contract struct { contractapi.Contract }
type Event struct { EventID string `json:"event_id"`; WatermarkID string `json:"watermark_id"`; DocumentID string `json:"document_id"`; RecipientKeyID string `json:"recipient_key_id"`; Signature string `json:"signature"`; SignatureAlgorithm string `json:"signature_algorithm"`; PreviousRecordHash string `json:"previous_record_hash"` }

// RecordDecryption stores evidence only; identity attributes belong in a private collection.
func (c *Contract) RecordDecryption(ctx contractapi.TransactionContextInterface, eventID string, payload string) error {
 var e Event; if err:=json.Unmarshal([]byte(payload), &e); err != nil { return err }; if e.EventID != eventID || e.WatermarkID == "" || e.Signature == "" { return fmt.Errorf("invalid signed event") }
 existing, err:=ctx.GetStub().GetState(eventID); if err != nil { return err }; if existing != nil { return fmt.Errorf("event already exists") }
 return ctx.GetStub().PutState(eventID, []byte(payload))
}
func (c *Contract) GetByWatermark(ctx contractapi.TransactionContextInterface, watermarkID string) ([]byte,error) { results,err:=ctx.GetStub().GetStateByQuery(fmt.Sprintf("{\"selector\":{\"watermark_id\":\"%s\"}}",watermarkID)); if err!=nil{return nil,err}; defer results.Close(); var out [][]byte; for results.HasNext(){r,e:=results.Next();if e!=nil{return nil,e};out=append(out,r.Value)};return json.Marshal(out) }
func main(){cc,err:=contractapi.NewChaincode(new(Contract));if err!=nil{panic(err)};if err=cc.Start();err!=nil{panic(err)}}
