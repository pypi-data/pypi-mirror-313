
import json
# flake8: noqa

from opencapif_sdk import capif_invoker_connector, capif_provider_connector, service_discoverer


capif_sdk_config_path = "./capif_sdk_config_sample_test.json"

def preparation_for_update(APFs, AEFs, second_network_app_api,capif_provider_connector):
    
    capif_provider_connector.apfs = APFs
    capif_provider_connector.aefs = AEFs
    if second_network_app_api:
        capif_provider_connector.api_description_path = "./network_app_provider_api_spec_2.json"
    else:
        capif_provider_connector.api_description_path = "./network_app_provider_api_spec_3.json"         
    
    return capif_provider_connector

def ensure_update(chosen_apf, chosen_aefs, second_network_app_api,capif_provider_connector):  
    
    if second_network_app_api:
        # Get AEFs ids and APFs ids to publish an APi
        
        APF = capif_provider_connector.provider_capif_ids[chosen_apf]
        AEF1 = capif_provider_connector.provider_capif_ids[chosen_aefs[0]]
        AEF2 = capif_provider_connector.provider_capif_ids[chosen_aefs[1]]
        AEF3 = capif_provider_connector.provider_capif_ids[chosen_aefs[2]]
        
        if not APF or not AEF1 or not AEF2:
            raise ValueError("Not all necessary values were found in 'provider_service_ids.json'")

        # Update configuration file
        capif_provider_connector.publish_req['publisher_apf_id'] = APF
        capif_provider_connector.publish_req['publisher_aefs_ids'] = [AEF1, AEF2,AEF3]


    else:

        APF = capif_provider_connector.provider_capif_ids['APF-1']
        AEF1 = capif_provider_connector.provider_capif_ids['AEF-1']
        AEF2 = capif_provider_connector.provider_capif_ids['AEF-2']
        
        capif_provider_connector.publish_req['publisher_apf_id'] = APF
        capif_provider_connector.publish_req['publisher_aefs_ids'] = [AEF1, AEF2]

    capif_provider_connector.publish_services()

    if second_network_app_api:
        service_api_id = capif_provider_connector.provider_service_ids['Test-two']
    else:
        service_api_id = capif_provider_connector.provider_service_ids['Test-three']

    capif_provider_connector.publish_req['service_api_id'] = service_api_id

    capif_provider_connector.update_service()

    print("PROVIDER UPDATE SERVICE COMPLETED")

    capif_provider_connector.get_all_services()

    print("PROVIDER GET ALL SERVICES COMPLETED")

    capif_provider_connector.get_service()

    print("PROVIDER GET SERVICE COMPLETED")
    
    capif_provider_connector.unpublish_service()
    
    return capif_provider_connector


if __name__ == "__main__":
    try:
        # Initialization of the connector
        capif_provider_connector = capif_provider_connector(config_file=capif_sdk_config_path)
        
        capif_provider_connector.onboard_provider()
        print("PROVIDER ONBOARDING COMPLETED")

        # Get AEFs ids and APFs ids to publish an API


        APF1 = capif_provider_connector.provider_capif_ids['APF-1']
        APF2 = capif_provider_connector.provider_capif_ids['APF-2']
        AEF1 = capif_provider_connector.provider_capif_ids['AEF-1']
        AEF2 = capif_provider_connector.provider_capif_ids['AEF-2']
        AEF3 = capif_provider_connector.provider_capif_ids['AEF-3']

        capif_provider_connector.api_description_path="network_app_provider_api_spec.json"
        # Update configuration file
        capif_provider_connector.publish_req['publisher_apf_id'] = APF1
        capif_provider_connector.publish_req['publisher_aefs_ids'] = [AEF1, AEF2]

        capif_provider_connector.publish_services()

        print("PROVIDER PUBLISH COMPLETED")

        service_api_id = capif_provider_connector.provider_service_ids["Testtrece"]

        capif_provider_connector.publish_req['service_api_id'] = service_api_id

        capif_provider_connector.update_service()

        print("PROVIDER UPDATE COMPLETED")

        capif_provider_connector.get_all_services()

        print("PROVIDER GET ALL SERVICES COMPLETED")

        capif_provider_connector.get_service()

        print("PROVIDER GET SERVICE COMPLETED")

        capif_invoker_connector = capif_invoker_connector(config_file=capif_sdk_config_path)

        capif_invoker_connector.onboard_invoker()
        print("INVOKER ONBOARDING COMPLETED")

        discoverer = service_discoverer(config_file=capif_sdk_config_path)

        discoverer.discover()

        print("SERVICE DISCOVER COMPLETED")

        discoverer.get_tokens()

        print("SERVICE GET TOKENS COMPLETED")
        
        capif_invoker_connector.update_invoker()
        
        print("INVOKER UPDATE SERVICE COMPLETED")

        capif_invoker_connector.offboard_invoker()

        print("INVOKER OFFBOARD COMPLETED")

        capif_provider_connector.unpublish_service()

        print("PROVIDER UNPUBLISH SERVICE COMPLETED")

        capif_provider_connector = preparation_for_update(2, 4, True,capif_provider_connector)
        
        capif_provider_connector.update_provider()
        
        chosen_apf = "APF-2"
        
        chosen_aefs = ["AEF-1", "AEF-3", "AEF-4"]
        
        capif_provider_connector = ensure_update(chosen_apf, chosen_aefs, True,capif_provider_connector)
        
        print("PROVIDER UPDATE ONE COMPLETED")
        
        capif_provider_connector = preparation_for_update(1, 2, False,capif_provider_connector)
        
        capif_provider_connector.update_provider()
        
        chosen_apf = "APF-1"
        
        chosen_aefs = ["AEF-1", "AEF-2"]
        
        capif_provider_connector = ensure_update(chosen_apf, chosen_aefs, False,capif_provider_connector)
        
        print("PROVIDER UPDATE TWO COMPLETED")

        capif_provider_connector.offboard_provider()

        print("PROVIDER OFFBOARDING COMPLETED")
        
        print("ALL TESTS PASSED CORRECTLY")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error reading the JSON file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
