//
//  ViewController.swift
//  SourdoughIOT
//
//  Created by Julie Gallagher on 2/23/22.
//

import UIKit
import AWSIoT

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        let credentials = AWSCognitoCredentialsProvider(regionType:.EUWest1, identityPoolId: "eu-west-1:cf504de5-9aec-4504-b0c7-25555c64de11")
        let configuration = AWSServiceConfiguration(region:.EUWest1, credentialsProvider: credentials)
        // Do any additional setup after loading the view.
        
        
        
        // Initialising AWS IoT And IoT DataManager
        AWSIoT.register(with: configuration!, forKey: "kAWSIoT")  // Same configuration var as above
        let iotEndPoint = AWSEndpoint(urlString: "wss://a2ct0i272lnfu5-ats.iot.eu-west-1.amazonaws.com/mqtt") // Access from AWS IoT Core --> Settings
        let iotDataConfiguration = AWSServiceConfiguration(region: .EUWest1,     // Use AWS typedef .Region
                                                           endpoint: iotEndPoint,
                                                           credentialsProvider: credentials)  // credentials is the same var as created above
            
        AWSIoTDataManager.register(with: iotDataConfiguration!, forKey: "kDataManager")

        // Access the AWSDataManager instance as follows:
        let dataManager = AWSIoTDataManager(forKey: "kDataManager")
        
        getAWSClientID{(clientId, error) in
              

               print("Get client Id complete")
            
            
            self.connectToAWSIoT(clientId: clientId)
            
                print("Connected Whoop")
            
            }
        

        
        print("Registered Whoop")
        
        
    }
    
    func getAWSClientID(completion: @escaping (_ clientId: String?,_ error: Error? ) -> Void) {
            // Depending on your scope you may still have access to the original credentials var
            let credentials = AWSCognitoCredentialsProvider(regionType:.EUWest1, identityPoolId: "eu-west-1:cf504de5-9aec-4504-b0c7-25555c64de11")
            
            credentials.getIdentityId().continueWith(block: { (task:AWSTask<NSString>) -> Any? in
                if let error = task.error as NSError? {
                    print("Failed to get client ID => \(error)")
                    completion(nil, error)
                    return nil  // Required by AWSTask closure
                }
                
                let clientId = task.result! as String
                print("Got client ID => \(clientId)")
                completion(clientId, nil)
                return nil // Required by AWSTask closure
            })
        }
    
    
    func connectToAWSIoT(clientId: String!) {
            
            func mqttEventCallback(_ status: AWSIoTMQTTStatus ) {
                switch status {
                case .connecting: print("Connecting to AWS IoT")
                case .connected:
                    print("Connected to AWS IoT")
                    registerSubscriptions()
                    // Register subscriptions here
                    // Publish a boot message if required
                case .connectionError: print("AWS IoT connection error")
                case .connectionRefused: print("AWS IoT connection refused")
                case .protocolError: print("AWS IoT protocol error")
                case .disconnected: print("AWS IoT disconnected")
                case .unknown: print("AWS IoT unknown state")
                default: print("Error - unknown MQTT state")
                }
            }
            
            // Ensure connection gets performed background thread (so as not to block the UI)
            DispatchQueue.global(qos: .background).async {
                do {
                    print("Attempting to connect to IoT device gateway with ID = \(clientId)")
                    let dataManager = AWSIoTDataManager(forKey: "kDataManager")
                    dataManager.connectUsingWebSocket(withClientId: clientId,
                                                      cleanSession: true,
                                                      statusCallback: mqttEventCallback)
                    
                } catch {
                    print("Error, failed to connect to device gateway => \(error)")
                }
            }
        }
    @IBAction func Button(_ sender: Any) {
        registerSubscriptions()
    }
    func messageReceived(payload: Data) {
        let payloadDictionary = jsonDataToDict(jsonData: payload)
        print("Message received: \(payloadDictionary)")
        
        // Handle message event here...
    }
    
    func registerSubscriptions() {
            func messageReceived(payload: Data) {
                let payloadDictionary = jsonDataToDict(jsonData: payload)
                print("Message received: \(payloadDictionary)")
                
                // Handle message event here...
            }
            
            let topicArray = ["esp32/pub" ]
            let dataManager = AWSIoTDataManager(forKey: "kDataManager")
            
            for topic in topicArray {
                print("Registering subscription to => \(topic)")
                dataManager.subscribe(toTopic: topic,
                                      qoS: .messageDeliveryAttemptedAtLeastOnce,  // Set according to use case
                                      messageCallback: messageReceived)
            }
    }

    func jsonDataToDict(jsonData: Data?) -> Dictionary <String, Any> {
            // Converts data to dictionary or nil if error
            do {
                let jsonDict = try JSONSerialization.jsonObject(with: jsonData!, options: [])
                let convertedDict = jsonDict as! [String: Any]
                return convertedDict
            } catch {
                // Couldn't get JSON
                print(error.localizedDescription)
                return [:]
            }
    }
    
    func publishMessage(message: String!, topic: String!) {
      let dataManager = AWSIoTDataManager(forKey: "kDataManager")
      dataManager.publishString(message, onTopic: topic, qoS: .messageDeliveryAttemptedAtLeastOnce) // Set QoS as needed
    }


}
