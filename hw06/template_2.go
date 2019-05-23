package main // import "main"

import (
	"encoding/hex"
	"fmt"
	"os"
	"strings"
	"crypto/sha256"
	"crypto/rand"
	"go.dedis.ch/cothority/v3"
	"go.dedis.ch/cothority/v3/skipchain"
	"go.dedis.ch/onet/v3"
	"go.dedis.ch/onet/v3/network"
)

const email = "fouad.mazen@epfl.ch"

func GenerateRandomBytes(n int) ([]byte, error) {
    b := make([]byte, n)
    _, err := rand.Read(b)
    // Note that err == nil only if we read len(b) bytes.
    if err != nil {
        return nil, err
    }

    return b, nil
}

func main() {
	if len(os.Args) <= 1 {
		fmt.Println("Missing URL (tls://com402.epfl.ch:7002)")
		os.Exit(1)
	}
	// Get the address
	arg := os.Args[1]

	roster := onet.NewRoster([]*network.ServerIdentity{
		&network.ServerIdentity{
			Address: network.Address(arg),
			// necessary to create a roster..
			Public: cothority.Suite.Point(),
		},
	})

	bb := "6a6ea0e9f701862ddd746ad80d331fc4834a5f358443572eadc138a93cfdbd3a"

	id, err := hex.DecodeString(strings.Trim(bb, "\n"))
	if err != nil {
		fmt.Printf("%v\n", err)
		os.Exit(1)
	}
	//This is the genesis id
	sid := skipchain.SkipBlockID(id)

	fmt.Println("Genesis")
	fmt.Println(sid)

	//Creating a new client for the skipchain
	cl := skipchain.NewClient()
	// Get the latest block for the hash -- Add your code here
	for i:=0 ; i<3 ; i++{
		fmt.Println("Get latest block: Add code")
		all_blocks, error_ := cl.GetUpdateChain(roster, sid)
		if error_ != nil {
			fmt.Println(error_)
		}
		latest_hash := all_blocks.Update[len(all_blocks.Update)-1].Hash
		// Mine a correct hash with 3 leading 0 bytes -- Add your code here
		fmt.Println("Mine a correct hash with 3 leading 0 bytes: Add code")
		email_byte := []byte(email)
		var data []uint8
		for{
			random_nonce, err := GenerateRandomBytes(32)
			data_random_hash := append(random_nonce, latest_hash...)
			data = append(data_random_hash, email_byte...)
			// SHA256 of the data
			hash_fn := sha256.New()
			hash_fn.Write(data)
			hash_bytes := hash_fn.Sum(nil)
			hash_hex := hex.EncodeToString(hash_bytes)
			if err != nil {
				fmt.Println(err)
			}
			if hash_hex[0:6] == "000000"{
				break
			}
	
		}
		//Store the new block -- Add your code here
		fmt.Println("Storing the new block: Add code")
		two_latest_blocks, err_ := cl.StoreSkipBlock(all_blocks.Update[0], nil, data)

		if err_ != nil{
			fmt.Println(err_)
		}
		fmt.Println(two_latest_blocks)
	}
	
}
