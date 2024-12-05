# OpenCAPIF SDK
[![PyPI version](https://img.shields.io/pypi/v/opencapif-sdk.svg)](https://pypi.org/project/opencapif-sdk/) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![Python](https://img.shields.io/badge/python-v3.12+-blue.svg) [![PyPI - Downloads](https://img.shields.io/pypi/dm/opencapif-sdk)](https://pypi.org/project/opencapif-sdk/)

![OpenCAPIF icon](./doc/images/opencapif_icon.jpg)

This repository develops a Python Software Development Kit(SDK) which focuses on connecting to OpenCAPIF (Common API Framework for 3GPP Northbound APIs) in a simple way, lowering integration complexity and allowing developers to focus on Network Applications (Network Apps) or services development. 

OpenCAPIF SDK provides a set of libraries to enable either CAPIF provider and invoker roles, and other functions to simplify procedures calls towards OpenCAPIF entity.

Current version of OpenCAPIF SDK is compatible with following publicly available releases:
- [OpenCAPIF Release 1.0](https://ocf.etsi.org/documentation/v1.0.0-release/)
- OpenCAPIF Release 2.0

This document serves as the [main bootstrap reference](#networkapp-developer-path) to start working with OpenCAPIF SDK. For advanced users, refer to [OpenCAPIF full documentation](./doc/sdk_full_documentation.md) section to dig into all available features.

# Table of Contents

 1. [Repository structure](#repository-structure) 
 2. [Network App developers](#network-app-developers)
 3. [OpenCAPIF SDK summary](#opencapif-sdk-summary)
 4. [OpenCAPIF SDK requirements](#opencapif-sdk-requirements)
 5. [OpenCAPIF sdk installation](#opencapif-sdk-installation)
 6. [OpenCAPIF SDK data schema](#opencapif-sdk-data-schema)
 7. [OpenCAPIF SDK Configuration](./doc/sdk_configuration.md)
 8. [Network App developer path](#network-app-developer-path)
    1. [Provider Network App](#provider-network-app)
        * [Provider Network App sample](#provider-network-app-sample)
    2. [Invoker Network App](#invoker-network-app)
        * [Provider Network App sample](#provider-network-app-sample)
 9. [**OpenCAPIF SDK full documentation**](./doc/sdk_full_documentation.md)
 10. [OpenCAPIF SDK known issues](#opencapif-sdk-known-issues)


# Repository structure

    pesp_capif_sdk
    ├── config
    ├── doc
    │   └── images
    ├── installation
    ├── network_app_samples
    │   ├── network_app_invoker_sample
    │   │   └── postman
    │   └── network_app_provider_sample
    ├── samples
    ├── scripts
    ├── opencapif_sdk
    └── test

- [config](./config/): contains OpenCAPIF SDK configuration files samples. These samples illustrate the structure of the configuration files ir order to use SDK properly. Go to the [configuration section](./doc/sdk_configuration.md) for more details,
- [doc](./doc/): contains documentation related files to this README,
- [installation](./installation/): this folder stores the Python [requeriments.txt](./installation/requirements.txt) file that is required to complete the [SDK developers section](./doc/sdk_developers.md),
- [network_app_samples](./network_app_samples/): this folder contains both provider and invoker Network App samples explained further in this document at [network app developer path](#network-app-developer-path),
- [samples](./samples/): contains sample files related to SDK configuration, API definitions and SDK configuration via environment variables,
- [scripts](./scripts/): single scripts to individually test functionality though command line. For more information on how to use these go to the [full documentation section](./doc/sdk_full_documentation.md),
- [opencapif_sdk](./opencapif_sdk/): where SDK code is stored,
- [test](./test/): contains a file named test.py containing tests to ensure all SDK flows work properly.

# Network App developers

In the scope of CAPIF, a Network App (Network Application) refers to an external application or service that interacts with the 3GPP network via standardized APIs. These Network Apps typically leverage the capabilities and services provided by the underlying mobile network infrastructure, such as network slicing, quality of service (QoS), or location services.

Network Apps can be developed by third-party service providers, network operators, or other stakeholders to offer a wide range of services, including enhanced communication features, IoT solutions, or content delivery, and they use CAPIF as the unified framework for securely discovering, accessing, and utilizing 3GPP network APIs.

Next image illustrates how CAPIF works and where the SDK provides means to integrate with it:

![CAPIF-illustration](./doc/images/flows_capif_illustration.jpg)

For that purpose Network Apps play 2 different roles when interacting with CAPIF:
- **Invoker**: a Network App acting as an Invoker is responsible for consuming APIs exposed by other services. This role represents an external application or service that  calls the 3GPP northbound APIs to utilize the network’s functionalities.

- **Provider**: a Network App acting as a Provider is responsible for exposing its own APIs/services for use by Invokers. This role represents an entity that offers services through APIs, making them available to other external applications or Invokers.A provider also is distinguished for having three parts.

  - The **AMF (API Management Function)**, supplies the API provider domain with administrative capabilities. Some of these capabilities include, auditing the service API invocation logs received from the CCF, on-boarding/off-boarding new API invokers and monitoring the status of the service APIs.One provider can have only one AMF.

  - The **APF (API Publishing Function)**, is responsible for the publication of the service APIs to CCF in order to enable the discovery capability to the API Invokers.One provider can have multiple APFs.

  - The **AEF (API Exposing Function)**, is responsible for the exposure of the service APIs. Assuming that API Invokers are authorized by the CCF, AEF validates the authorization and subsequently provides the direct communication entry points to the service APIs. AEF may also authorize API invokers and record the invocations in log files.One provider can have multiple AEFs

OpenCAPIF SDK brings a set of functions to integrate with the 5G Core's function CAPIF, as defined in [3GPP Technical Specification (TS) 29.222 V18.5.0 Common API Framework for 3GPP Northbound APIs](https://www.etsi.org/deliver/etsi_ts/129200_129299/129222/18.05.00_60/ts_129222v180500p.pdf). This section shows the mapping between the Python functions available in this SDK and the CAPIF OpenAPI APIs defined the reference standard:

| **3GPP CAPIF API**                                    | **OpenCAPIF SDK function**                                  | **Description**                                             |
|-------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------------|
| /onboardedInvokers (POST)                             | [onboard_invoker()](./doc/sdk_full_documentation.md#invoker-onboarding)                                           | Registers a new invoker.                                    |
| /onboardedInvokers/{onboardingId} (PUT)               | [update_invoker()](./doc/sdk_full_documentation.md#update-and-offboard-invoker)                                          | Updates an existing invoker for a specific `onboardingId`.                                |
| /onboardedInvokers/{onboardingId} (DELETE)            | [offboard_invoker()](./doc/sdk_full_documentation.md#update-and-offboard-invoker)                                         | Deletes an invoker for a specific `onboardingId`.                                         |
| registrations (POST)                                  | [onboard_provider()](./doc/sdk_full_documentation.md#provider-onboarding)                                          | Registers a new service provider.                           |
| /registrations/{registrationId} (PUT)                 | [update_provider()](./doc/sdk_full_documentation.md#update-and-offboard-provider)                                           | Updates a service provider's registration for a specific `registrationId`.                  |
| /registrations/{registrationId} (DELETE)              | [offboard_provider()](./doc/sdk_full_documentation.md#update-and-offboard-provider)                                         | Deletes a service provider's registration for a specific `registrationId`.                  |
| /allServiceAPIs (GET)                                 | [discover()](./doc/sdk_full_documentation.md#discover-process)                                                  | Retrieves a list of all available service APIs.             |
| /trustedInvokers (PUT//POST)                          | [get_tokens()](./doc/sdk_full_documentation.md#discover-process)                                                  | Registers or updates trusted invokers.                      |
| /securities/{securityId}/token (GET)                  | [get_tokens()](./doc/sdk_full_documentation.md#obtain-invoker-tokens)                                                | Retrieves a security token for a specific `securityId`. This JWT token is used to query the targeted services.      |
| /{apfId}/service-apis(POST)                           | [publish_services()](./doc/sdk_full_documentation.md#services-publishing)                                          | Registers a new service API into the system for a specific `apfId`                |
| /{apfId}/service-apis/{serviceApiId} (DELETE)         | [unpublish_service()](./doc/sdk_full_documentation.md#services-deletion)                                         | Deletes a service API from the system for a specific `apfId`and `serviceApiId`                      |
| /{apfId}/service-apis/{serviceApiId} (PUT)            | [update_service()](./doc/sdk_full_documentation.md#services-update)                                            | Updates the details of an existing service API for a specific `apfId`and `serviceApiId`             |
| /{apfId}/service-apis/{serviceApiId} (GET)                           | [get_service()](./doc/sdk_full_documentation.md#get-services)                                               | Retrieves the details of a specific service API for a specific `apfId` and `serviceApiId`           |
| /{apfId}/service-apis (GET)            | [get_all_services()](./doc/sdk_full_documentation.md#get-all-services)                                          | Retrieves a list of all available service APIs for a specific `apfId`            |
| /aef-security/v1/check-authentication (POST)            | [check_authentication()](./doc/sdk_full_documentation.md#check_authentication)                                          | This custom operation allows the API invoker to confirm the `supported_features` from the API exposing function(AEF)            |

NOTE: Above mentioned CAPIF APIs are defined in these 3GPP references:
- [CAPIF Invoker API specification](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_API_Invoker_Management_API.yaml)
- [CAPIF Provider API specification](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_API_Provider_Management_API.yaml)
- [CAPIF Discover API specification](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Discover_Service_API.yaml)
- [CAPIF Publish API specification](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Publish_Service_API.yaml) 
- [CAPIF Security API specification](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Security_API.yaml)
- [AEF Security API specification](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_AEF_Security_API.yaml)

NOTE: In the [3GPP Technical Specification (TS) 29.222 V18.5.0 Common API Framework for 3GPP Northbound APIs](https://www.etsi.org/deliver/etsi_ts/129200_129299/129222/18.05.00_60/ts_129222v180500p.pdf) the `service` concept is understood as equal as the `API` concept.


## OpenCAPIF SDK requirements

To use the OpenCAPIF SDK, a registered user account within the target CAPIF instance is required. 

**Contact the administrator to obtain the required predefined credentials (CAPIF username and password).**

## OpenCAPIF SDK installation

To install the OpenCAPIF SDK source code for developing purposes there is an available section: [OpenCAPIF SDK developers](./doc/sdk_developers.md).

To use the SDK, binary installer for the latest version is available at the [Python Package Index (Pipy)](https://pypi.org/project/opencapif-sdk/)

```console
pip install opencapif_sdk
```

## OpenCAPIF SDK Data Schema

Here is a visual look on the variables of the CAPIF sdk referenced in:
- [Important information for Invoker Consumer](#important-information-for-invoker-consumer) 
- [Important information for Provider Consumer](#important-information-for-provider-consumers)

![sdk_data_schema](./doc/images/flows_data_schema.png)

# Network App developer path

The Network App Developer Path guides the programmer through building and integrating Network Apps using CAPIF. This path is divided into two key sections: [Invoker Network App](#invoker-network-app) and [Provider Network App](#provider-network-app). Each section covers the essential flow and functions for developing Network Apps interaction with CAPIF, whether the user is acting as an invoker consuming services or a provider offering them. By following this path, developers will gain a comprehensive understanding of how to effectively use the SDK within the CAPIF ecosystem.

Here is a good explanation about how a usual flow of a Network App should work: [usual flow example](https://ocf.etsi.org/documentation/latest/testing/postman/)

## Provider Network App

A Network App development running as a Provider would typically follow this process step by step, making use of the SDK:

![PROVIDER_PATH](./doc/images/flows_provider_path.jpg)

Now, it is described in 4 simple steps how a Provider can be developed in just some code lines, below snippet. It describes the usual flow a Provider would follow to publish an API service.

```python
  import opencapif_sdk

  provider = opencapif_sdk.capif_provider_connector(config_file="path/to/capif_sdk_config.json")
  provider.onboard_provider()

  #translator = opencapif_sdk.api_schema_translator("./path/to/openapi.yaml")
  #translator.build("api_description_name",ip="0.0.0.0",port=9090)
  provider.api_description_path = "./api_description_name.json"

  APF = provider.provider_capif_ids["APF-1"]

  AEF1 = provider.provider_capif_ids["AEF-1"]
  AEF2 = provider.provider_capif_ids["AEF-2"]

  provider.publish_req['publisher_apf_id'] = APF
  provider.publish_req['publisher_aefs_ids'] = [AEF1, AEF2]
  provider.supported_features ="4"
  provider.publish_services()
```

Code is next explained step by step:

1. **Create a Provider object:** \
   Initialize the provider by creating an instance of the `capif_provider_connector` class, passing the required [configuration](./doc/sdk_configuration.md) file:

   Make sure that the configuration file is filled before creating the instance.


2. **Onboard the Provider:** \
    Register the provider with the CAPIF system to enable the publication of APIs:

    In this phase, the SDK creates and stores all the necessary files for using CAPIF as a provider, such as the authorization certificate, the server certificate and each of the APFs and AEFs certificates .Furthermore creates a file named `provider_capif_ids.json`, which stores important information about the provider.

3. **Prepare API details:** \
    In the `provider_folder`, more specifically in the `capif_username` folder, it will be sotres the provider API details file. This file contains all the APFs and AEFs IDs that have already onboarded with this `capif_username`.

    It is also important to have previously prepared the **API schema description** file of the API to be published. **This file must follow the [CAPIF_Publish_Service_API](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Publish_Service_API.yaml) 3GPP specification.**

    If the **API** is defined in an Openapi.yaml format, the sdk has a facility which creates automatically the **API schema description**.For using this functionality uncomment the translator lines. More information:[Translator functionality](./doc/sdk_full_documentation.md#openapi-translation)
   
    Choose one APF and the AEF identifiers, and fulfill the `publish_req` structure and the `api_description_path`.

    The `provider_capif_ids` variable is a dictionary which contains key-values of all the APFs and AEFs stored as name: ID.

    This `publish_req` field can also be filled with object variables already stored at provider object.

5. **Publish the services:** \
   Use the `publish_services()` method to register the APIs with the CAPIF framework. In this phase, the SDK does the publishing of the provided API specification.

   **At the end of this step, the API will be available for Invokers to be consumed.**

Now, Provider Network App is ready to receive requests from Invokers.

### Provider Network App sample

This repository provides an implementation sample of a [Provider-Network App](./network_app_samples/network_app_provider_sample/network_app_provider.py).

In this sample, the provider publishes two APIs and starts running the servers of each API on local environment.

### Important information for Provider consumers

Within the `provider_folder`, the SDK stores the created folders named with prefix of the provided `capif_username` that has been registered from administrator. At each folder, there will be found the following files:

- `provider_capif_ids.json`: contains all the APFs and AEFs ids that have already onboarded with this `capif_username`,
- `capif_<api_name>_<api_id>.json`: if it is already published or updated an API, it will contain a copy of the last payload,
- `service_received.json`: if it is already used to get an API or get all APIs functionality, it will contain the response of last request,
- `provider_service_ids.json`: contains the currently published APIs with their `api_id`.

All the configuration values are available within the object `capif_provider_connector`.

The `provider_service_ids` variable stores the `provider_service_ids.json` content in a dictionary form.

The `provider_capif_ids` variable stores the `provider_capif_ids.json` content in a dictionary form.


## Invoker Network App

A Network App development running as an Invoker would typically follow this process step by step, making use of the SDK: 

![INVOKER_PATH](./doc/images/flows_invoker_path.jpg)

Now, it is described in some simple steps how an Invoker can be developed in just some code lines. Find below the code snippet. It describes the usual flow an Invoker would follow to consume APIs from CAPIF.

```python
  import opencapif_sdk
  
  invoker = opencapif_sdk.capif_invoker_connector(config_file="path/to/the/capif_sdk_config.json")
  invoker.onboard_invoker()
  service_discoverer = opencapif_sdk.service_discoverer(config_file="path/to/the/capif_sdk_config.json")
  service_discoverer.discover()
  service_discoverer.get_tokens()
  jwt_token=service_discoverer.token
```

Code is next explained step by step:

1. **Create an Invoker object:** \
   Initialize the invoker by creating an instance of the `capif_invoker_connector` class, passing the required [configuration](./doc/sdk_configuration.md) file.
   
   Make sure that the configuration file is filled out before creating the instance.
   
2. **Onboard the Invoker**: \
   Register the target invoker with the CAPIF system to enable access to APIs.

   In this phase, the SDK creates and stores all the necessary files for using CAPIF as a invoker, such as the authorization certificate and the server certificate.Furthermore,it creates a file named `capif_api_security_context_details.json` , which stores important information about the invoker.

3. **Create a Service Discoverer object:** \
   Initialize the service discovery mechanism to search for available services(APIs) in CAPIF.

4. **Discover available services:** \
   Use the `discover()` method to retrieve a list of available APIs. In this phase, the SDK finds all the available APIs for the invoker. Consequently, it saves the most important information and stores it within the `capif_api_security_context_details.json`.

      **DISCLAIMER:** If it is the first time the user runs `discover()`, it will show a warning alert like following:

          WARNING - Received 404 error, redirecting to register security service

      This alert is expected because the SDK tries to update the security context first. If a 404 error is received, it means the security context is not created yet, so the next step for the SDK is to register a new security service. 

5. **Retrieve security tokens:** \
  Use the `get_tokens()` method to obtain the necessary tokens for authenticating API requests.
  

**At the end of this flow, the invoker has been onboarded and it is ready to use target APIs.** All required information, including the access_token to use the available APIs, is stored at `capif_api_security_context_details.json` file. This file is placed in the invoker_folder path, specifically in the folder that corresponds to the capif_username used in the `capif_sdk_config.json`. A sample of the [capif_api_security_context_details](./samples/capif_api_security_context_details_sample.json) is also available.

Now, Invoker Network App can use access tokens to consume real services.

### Invoker Network App sample

Here is a code sample of the implementation of an [Invoker-Network App](./network_app_samples/network_app_invoker_sample/network_app_invoker.py). 

In this sample, the invoker will discover the APIs published by the sample provider shown in this document and will return the access token for querying the APIs. This sample is prepared to run after the [Provider-Network App](./network_app_samples/network_app_provider_sample/network_app_provider.py).

Make sure that the [Provider-Network App](./network_app_samples/network_app_provider_sample/network_app_provider.py) is running before following this implementation.

For testing APIs availability, after running both samples([Provider-Network App](./network_app_samples/network_app_provider_sample/network_app_provider.py) and [Invoker-Network App](./network_app_samples/network_app_invoker_sample/network_app_invoker.py)) the invoker app will return the access token.

Also, in the same Invoker-Network folder is available a [Postman structure](./network_app_samples/network_app_invoker_sample/postman/).In order to test these APIs, the access token returned in the Invoker-Network App must be set in the Postman environment, more specifically in the `access_token` variable.

Another alternative is to import the [Postman structure](./network_app_samples/network_app_invoker_sample/postman/) in your own postman account and fill the `postman_api_key` and the `environment_id` fields within the [Invoker-Network App](./network_app_samples/network_app_invoker_sample/network_app_invoker.py). Here is an example of these two fields that need to be fulfilled. 

```python
    # Your Postman API Key
    postman_api_key = "AAAA-your-apikey"
    
    # Postman Environment ID
    environment_id = "your-environment-id-must-be-here"
```

### Important information for Invoker consumer

In the `invoker_folder`, it will be located several folders with each `capif_username` it has been onboarded as a provider. For each folder, it will be found:

- `capif_api_security_context_details.json`: This file contains the information of the invoker. It will contain:
        
    1. The `api_invoker_id`,
    2. If the Service Discovery Functionality has already been used , it will be found all the available APIs with their information,
    3. If the Service Get Token functionality has already been used , it will be found the access token for using the APIs that has already been discovered.

The `token` variable is also available for retrieving the JWT token after the `get_tokens()` method.

The `invoker_capif_details` variable stores the `capif_api_security_context_details.json` content in a dictionary form.

# OpenCAPIF SDK known issues

There are some features which **are not currently available at latest OpenCAPIF SDK release**. Those are assumed to be technical debt and might be available in future releases: 

  - [CAPIF Access control policy management](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Access_Control_Policy_API.yaml)
  - [CAPIF Auditing API management](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Auditing_API.yaml)
  - [CAPIF Events API management](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Events_API.yaml)
  - [CAPIF Logging API management](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Logging_API_Invocation_API.yaml)
  - [CAPIF Routing info API management](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Routing_Info_API.yaml)
  - [CAPIF Security API management](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS29222_CAPIF_Security_API.yaml)
    - /trustedInvokers/{apiInvokerId}/delete (POST)
    - /trustedInvokers/{apiInvokerId} (GET)
    - /trustedInvokers/{apiInvokerId} (DELETE)
