r'''
[![npm version](https://badge.fury.io/js/cdk-internal-gateway.svg)](https://badge.fury.io/js/cdk-internal-gateway)
[![PyPI version](https://badge.fury.io/py/pharindoko.cdk-internal-gateway.svg)](https://badge.fury.io/py/pharindoko.cdk-internal-gateway)
[![Release](https://github.com/pharindoko/cdk-internal-gateway/actions/workflows/release.yml/badge.svg)](https://github.com/pharindoko/cdk-internal-gateway/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/pharindoko/cdk-internal-gateway/blob/main/LICENSE)

# CDK Internal Gateway

Use this CDK construct to create **internal serverless applications**.

Useful for larger companies to create internal  serverless applications that are not exposed to the internet and only accessible from the internal network.

## Installation

Using Typescript for aws cdk

```bash
npm i cdk-internal-gateway
```

Using Python for aws cdk

```bash
pip install pharindoko.cdk-internal-gateway
```

## Architecture

![cdk-internal-gateway-architecture](cdk-internal-gateway.drawio.png)

### Technical Details

Modularized approach with separate constructs

* attach multiple InternalApiGateway and InternalWebsite constructs to the same Internal Service to save costs and keep flexibility

**Internal Service Construct (mandatory construct):**

* creates an internal application loadbalancer

  * forwards traffic to VPC endpoint for execute-api
  * redirect http to https
* generates custom domains for the API Gateway
* generates certificates for the loadbalancer listener

**Internal Api Gateway Construct:**

* provides a securely configured apigateway resource out of the box

  * attach your aws components to the internal apigateway resource
  * sets api gateway to PRIVATE mode
  * sets resource policies to only allow traffic from vpc endpoint
* attaches custom domains to the API Gateway
* attaches certificates to the the API Gateway and the loadbalancer

**Internal Website Construct:**

* makes your website internally accessible
* redeploys your website with a single cdk deploy
* provides a securely configured private s3 bucket out of box
* works with SPA applications (written with Vue, Angular) and static websites
* is an extension of the InternalApiGateway Construct

## Requirements

* CDK V2 (2.46.0)
* A VPC
* A VPC Endpoint for execute-api
* A Hosted Zone
* Internally accessible subnets (for the load balancer)

## Usage

> Let`s assume we create a simple internal api for our company and start with a single lambda function...

1. Create a file called `/lib/my-new-stack.ts`

   ```python
   import { aws_apigateway as apigateway, aws_ec2 as ec2, aws_lambda as lambda, aws_route53 as route53, Stack, StackProps } from 'aws-cdk-lib';
   import { HttpMethod } from 'aws-cdk-lib/aws-events';
   import { InternalApiGateway, InternalApiGatewayProps, InternalService } from 'cdk-internal-gateway';
   import { Construct } from 'constructs';
   import * as path from 'path';

   // Create a new stack that inherits from the InternalApiGateway Construct
   export class ServerlessStack extends InternalApiGateway {
       constructor(scope: Construct, id: string, props: InternalApiGatewayProps) {
           super(scope, id, props);

           // The internal api gateway is available as member variable
           // Attach your lambda function to the this.apiGateway
           const defaultLambdaJavascript = this.apiGateway.root.resourceForPath("hey-js");
           const defaultHandlerJavascript = new lambda.Function(
               this,
               `backendLambdaJavascript`,
               {
                   functionName: `js-lambda`,
                   runtime: lambda.Runtime.NODEJS_14_X,
                   handler: "index.handler",
                   code: lambda.Code.fromAsset(path.join(__dirname, "../src")),
               }
           );

           defaultLambdaJavascript.addMethod(
               HttpMethod.GET,
               new apigateway.LambdaIntegration(defaultHandlerJavascript)
           );
       }
   }

   // Create a new stack that contains the whole service with all nested stacks
   export class ServiceStack extends Stack {
       constructor(scope: Construct, id: string, props: StackProps) {
           super(scope, id, props);

           // get all parameters to create the internal service stack
           const vpc = ec2.Vpc.fromLookup(this, 'vpcLookup', { vpcId: 'vpc-1234567890' });
           const subnetSelection = {
               subnets: ['subnet-0b1e1c6c7d8e9f0a2', 'subnet-0b1e1c6c7d8e9f0a3'].map((ip, index) =>
                   ec2.Subnet.fromSubnetId(this, `Subnet${index}`, ip),
               ),
           };
           const hostedZone = route53.HostedZone.fromLookup(this, 'hostedzone', {
               domainName: 'test.aws1234.com',
               privateZone: true,
               vpcId: vpc.vpcId,
           });
           const vpcEndpoint =
               ec2.InterfaceVpcEndpoint.fromInterfaceVpcEndpointAttributes(
                   this,
                   'vpcEndpoint',
                   {
                       port: 443,
                       vpcEndpointId: 'vpce-1234567890',
                   },
               );

           // create the internal service stack
           const serviceStack = new InternalService(this, 'InternalServiceStack', {
               hostedZone: hostedZone,
               subnetSelection: subnetSelection,
               vpcEndpointIPAddresses: ['192.168.2.1', '192.168.2.2'],
               vpc: vpc,
               subjectAlternativeNames: ['internal.example.com'],
               subDomain: "internal-service"
           })

           // create your stack that inherits from the InternalApiGateway
           new ServerlessStack(this, 'MyProjectStack', {
               domains: serviceStack.domains,
               stage: "dev",
               vpcEndpoint: vpcEndpoint,
           })

           // create another stack that inherits from the InternalApiGateway
           ...
           ...
       }
   }
   ```
2. Reference the newly created `ServiceStack` in the default `/bin/{project}.ts` file e.g. like this

   ```python
   new ServiceStack(app, 'MyProjectStack', {
   env:
   {
       account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT,
       region: process.env.CDK_DEPLOY_REGION || process.env.CDK_DEFAULT_REGION
   }
   ```

## Costs

You have to expect basic infra costs for 2 components in this setup:

| Count |  Type |  Estimated Costs |
|---|---|---|
|1 x| application load balancer  | 20 $  |
|2 x| network interfaces for the vpc endpoint  | 16 $  |

A shared vpc can lower the costs as vpc endpoint and their network interfaces can be used together...
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


class InternalApiGateway(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-internal-gateway.InternalApiGateway",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
        vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
        api_base_path_mapping_path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
        endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
        default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_watch_role: typing.Optional[builtins.bool] = None,
        deploy: typing.Optional[builtins.bool] = None,
        deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
        domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_export_name: typing.Optional[builtins.str] = None,
        endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
        fail_on_warnings: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        rest_api_name: typing.Optional[builtins.str] = None,
        retain_deployments: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domains: List of custom domains names to be used for the API Gateway.
        :param vpc_endpoint: VPC endpoint id of execute-api vpc endpoint. This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        :param api_base_path_mapping_path: Path for custom domain base path mapping that will be attached to the api gateway.
        :param stage: (deprecated) Stage name used for all cloudformation resource names and internal aws resource names.
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param endpoint_configuration: The EndpointConfiguration property type specifies the endpoint types of a REST API. Default: EndpointType.EDGE
        :param min_compression_size: A Size(in bytes, kibibytes, mebibytes etc) that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param minimum_compression_size: (deprecated) A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: - false if ``@aws-cdk/aws-apigateway:disableCloudWatchRole`` is enabled, true otherwise
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the RestApi construct. Default: - 'Automatically created by the RestApi construct'
        :param disable_execute_api_endpoint: Specifies whether clients can invoke the API using the default execute-api endpoint. To require that clients use a custom domain name to invoke the API, disable the default endpoint. Default: false
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: EndpointType.EDGE
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ae54245009148c66f767401f5250017b64fe5bce1d826b5a4ab5f903630362)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InternalApiGatewayProps(
            domains=domains,
            vpc_endpoint=vpc_endpoint,
            api_base_path_mapping_path=api_base_path_mapping_path,
            stage=stage,
            api_key_source_type=api_key_source_type,
            binary_media_types=binary_media_types,
            clone_from=clone_from,
            endpoint_configuration=endpoint_configuration,
            min_compression_size=min_compression_size,
            minimum_compression_size=minimum_compression_size,
            default_cors_preflight_options=default_cors_preflight_options,
            default_integration=default_integration,
            default_method_options=default_method_options,
            cloud_watch_role=cloud_watch_role,
            deploy=deploy,
            deploy_options=deploy_options,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            domain_name=domain_name,
            endpoint_export_name=endpoint_export_name,
            endpoint_types=endpoint_types,
            fail_on_warnings=fail_on_warnings,
            parameters=parameters,
            policy=policy,
            rest_api_name=rest_api_name,
            retain_deployments=retain_deployments,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def _api_gateway(self) -> _aws_cdk_aws_apigateway_ceddda9d.LambdaRestApi:
        '''Internal API Gateway This private api gateway is used to serve internal solutions (websites, apis, applications).

        Attach your methods to this api gateway.
        It is not exposed to the internet.
        It is only accessible from the load balancer`s target group.
        '''
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApi, jsii.get(self, "apiGateway"))


class _InternalApiGatewayProxy(InternalApiGateway):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InternalApiGateway).__jsii_proxy_class__ = lambda : _InternalApiGatewayProxy


@jsii.data_type(
    jsii_type="cdk-internal-gateway.InternalApiGatewayProps",
    jsii_struct_bases=[_aws_cdk_aws_apigateway_ceddda9d.RestApiProps],
    name_mapping={
        "default_cors_preflight_options": "defaultCorsPreflightOptions",
        "default_integration": "defaultIntegration",
        "default_method_options": "defaultMethodOptions",
        "cloud_watch_role": "cloudWatchRole",
        "deploy": "deploy",
        "deploy_options": "deployOptions",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "domain_name": "domainName",
        "endpoint_export_name": "endpointExportName",
        "endpoint_types": "endpointTypes",
        "fail_on_warnings": "failOnWarnings",
        "parameters": "parameters",
        "policy": "policy",
        "rest_api_name": "restApiName",
        "retain_deployments": "retainDeployments",
        "api_key_source_type": "apiKeySourceType",
        "binary_media_types": "binaryMediaTypes",
        "clone_from": "cloneFrom",
        "endpoint_configuration": "endpointConfiguration",
        "min_compression_size": "minCompressionSize",
        "minimum_compression_size": "minimumCompressionSize",
        "domains": "domains",
        "vpc_endpoint": "vpcEndpoint",
        "api_base_path_mapping_path": "apiBasePathMappingPath",
        "stage": "stage",
    },
)
class InternalApiGatewayProps(_aws_cdk_aws_apigateway_ceddda9d.RestApiProps):
    def __init__(
        self,
        *,
        default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
        default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_watch_role: typing.Optional[builtins.bool] = None,
        deploy: typing.Optional[builtins.bool] = None,
        deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
        domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_export_name: typing.Optional[builtins.str] = None,
        endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
        fail_on_warnings: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        rest_api_name: typing.Optional[builtins.str] = None,
        retain_deployments: typing.Optional[builtins.bool] = None,
        api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
        endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
        vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
        api_base_path_mapping_path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for ApiGateway Includes all properties of RestApiProps except: endpointConfiguration, policy This is done by intention to prevent the user from overriding the required security settings.

        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: - false if ``@aws-cdk/aws-apigateway:disableCloudWatchRole`` is enabled, true otherwise
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the RestApi construct. Default: - 'Automatically created by the RestApi construct'
        :param disable_execute_api_endpoint: Specifies whether clients can invoke the API using the default execute-api endpoint. To require that clients use a custom domain name to invoke the API, disable the default endpoint. Default: false
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: EndpointType.EDGE
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param endpoint_configuration: The EndpointConfiguration property type specifies the endpoint types of a REST API. Default: EndpointType.EDGE
        :param min_compression_size: A Size(in bytes, kibibytes, mebibytes etc) that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param minimum_compression_size: (deprecated) A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param domains: List of custom domains names to be used for the API Gateway.
        :param vpc_endpoint: VPC endpoint id of execute-api vpc endpoint. This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        :param api_base_path_mapping_path: Path for custom domain base path mapping that will be attached to the api gateway.
        :param stage: (deprecated) Stage name used for all cloudformation resource names and internal aws resource names.
        '''
        if isinstance(default_cors_preflight_options, dict):
            default_cors_preflight_options = _aws_cdk_aws_apigateway_ceddda9d.CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict):
            default_method_options = _aws_cdk_aws_apigateway_ceddda9d.MethodOptions(**default_method_options)
        if isinstance(deploy_options, dict):
            deploy_options = _aws_cdk_aws_apigateway_ceddda9d.StageOptions(**deploy_options)
        if isinstance(domain_name, dict):
            domain_name = _aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions(**domain_name)
        if isinstance(endpoint_configuration, dict):
            endpoint_configuration = _aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration(**endpoint_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d09850aa6d812c4e31fc3d6e1747f6fd2cd0e17db65131fb04491c03f3d23f9)
            check_type(argname="argument default_cors_preflight_options", value=default_cors_preflight_options, expected_type=type_hints["default_cors_preflight_options"])
            check_type(argname="argument default_integration", value=default_integration, expected_type=type_hints["default_integration"])
            check_type(argname="argument default_method_options", value=default_method_options, expected_type=type_hints["default_method_options"])
            check_type(argname="argument cloud_watch_role", value=cloud_watch_role, expected_type=type_hints["cloud_watch_role"])
            check_type(argname="argument deploy", value=deploy, expected_type=type_hints["deploy"])
            check_type(argname="argument deploy_options", value=deploy_options, expected_type=type_hints["deploy_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument endpoint_export_name", value=endpoint_export_name, expected_type=type_hints["endpoint_export_name"])
            check_type(argname="argument endpoint_types", value=endpoint_types, expected_type=type_hints["endpoint_types"])
            check_type(argname="argument fail_on_warnings", value=fail_on_warnings, expected_type=type_hints["fail_on_warnings"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument rest_api_name", value=rest_api_name, expected_type=type_hints["rest_api_name"])
            check_type(argname="argument retain_deployments", value=retain_deployments, expected_type=type_hints["retain_deployments"])
            check_type(argname="argument api_key_source_type", value=api_key_source_type, expected_type=type_hints["api_key_source_type"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument clone_from", value=clone_from, expected_type=type_hints["clone_from"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument min_compression_size", value=min_compression_size, expected_type=type_hints["min_compression_size"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument vpc_endpoint", value=vpc_endpoint, expected_type=type_hints["vpc_endpoint"])
            check_type(argname="argument api_base_path_mapping_path", value=api_base_path_mapping_path, expected_type=type_hints["api_base_path_mapping_path"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domains": domains,
            "vpc_endpoint": vpc_endpoint,
        }
        if default_cors_preflight_options is not None:
            self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None:
            self._values["default_integration"] = default_integration
        if default_method_options is not None:
            self._values["default_method_options"] = default_method_options
        if cloud_watch_role is not None:
            self._values["cloud_watch_role"] = cloud_watch_role
        if deploy is not None:
            self._values["deploy"] = deploy
        if deploy_options is not None:
            self._values["deploy_options"] = deploy_options
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if endpoint_export_name is not None:
            self._values["endpoint_export_name"] = endpoint_export_name
        if endpoint_types is not None:
            self._values["endpoint_types"] = endpoint_types
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy is not None:
            self._values["policy"] = policy
        if rest_api_name is not None:
            self._values["rest_api_name"] = rest_api_name
        if retain_deployments is not None:
            self._values["retain_deployments"] = retain_deployments
        if api_key_source_type is not None:
            self._values["api_key_source_type"] = api_key_source_type
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if clone_from is not None:
            self._values["clone_from"] = clone_from
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if min_compression_size is not None:
            self._values["min_compression_size"] = min_compression_size
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size
        if api_base_path_mapping_path is not None:
            self._values["api_base_path_mapping_path"] = api_base_path_mapping_path
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def default_cors_preflight_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions]:
        '''Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        :default: - CORS is disabled
        '''
        result = self._values.get("default_cors_preflight_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions], result)

    @builtins.property
    def default_integration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration]:
        '''An integration to use as a default for all methods created within this API unless an integration is specified.

        :default: - Inherited from parent.
        '''
        result = self._values.get("default_integration")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration], result)

    @builtins.property
    def default_method_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions]:
        '''Method options to use as a default for all methods created within this API unless custom options are specified.

        :default: - Inherited from parent.
        '''
        result = self._values.get("default_method_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions], result)

    @builtins.property
    def cloud_watch_role(self) -> typing.Optional[builtins.bool]:
        '''Automatically configure an AWS CloudWatch role for API Gateway.

        :default: - false if ``@aws-cdk/aws-apigateway:disableCloudWatchRole`` is enabled, true otherwise
        '''
        result = self._values.get("cloud_watch_role")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deploy(self) -> typing.Optional[builtins.bool]:
        '''Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes.

        Since API Gateway deployments are immutable, When this option is enabled
        (by default), an AWS::ApiGateway::Deployment resource will automatically
        created with a logical ID that hashes the API model (methods, resources
        and options). This means that when the model changes, the logical ID of
        this CloudFormation resource will change, and a new deployment will be
        created.

        If this is set, ``latestDeployment`` will refer to the ``Deployment`` object
        and ``deploymentStage`` will refer to a ``Stage`` that points to this
        deployment. To customize the stage options, use the ``deployOptions``
        property.

        A CloudFormation Output will also be defined with the root URL endpoint
        of this REST API.

        :default: true
        '''
        result = self._values.get("deploy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deploy_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.StageOptions]:
        '''Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled.

        If ``deploy`` is disabled,
        this value cannot be set.

        :default: - Based on defaults of ``StageOptions``.
        '''
        result = self._values.get("deploy_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.StageOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the RestApi construct.

        :default: - 'Automatically created by the RestApi construct'
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether clients can invoke the API using the default execute-api endpoint.

        To require that clients use a custom domain name to invoke the
        API, disable the default endpoint.

        :default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain_name(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions]:
        '''Configure a custom domain name and map it to this API.

        :default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions], result)

    @builtins.property
    def endpoint_export_name(self) -> typing.Optional[builtins.str]:
        '''Export name for the CfnOutput containing the API endpoint.

        :default: - when no export name is given, output will be created without export
        '''
        result = self._values.get("endpoint_export_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_types(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]]:
        '''A list of the endpoint types of the API.

        Use this property when creating
        an API.

        :default: EndpointType.EDGE
        '''
        result = self._values.get("endpoint_types")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]], result)

    @builtins.property
    def fail_on_warnings(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource.

        :default: false
        '''
        result = self._values.get("fail_on_warnings")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom header parameters for the request.

        :default: - No parameters.

        :see: https://docs.aws.amazon.com/cli/latest/reference/apigateway/import-rest-api.html
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def policy(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument]:
        '''A policy document that contains the permissions for this RestApi.

        :default: - No policy.
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument], result)

    @builtins.property
    def rest_api_name(self) -> typing.Optional[builtins.str]:
        '''A name for the API Gateway RestApi resource.

        :default: - ID of the RestApi construct.
        '''
        result = self._values.get("rest_api_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retain_deployments(self) -> typing.Optional[builtins.bool]:
        '''Retains old deployment resources when the API changes.

        This allows
        manually reverting stages to point to old deployments via the AWS
        Console.

        :default: false
        '''
        result = self._values.get("retain_deployments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def api_key_source_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType]:
        '''The source of the API key for metering requests according to a usage plan.

        :default: - Metering is disabled.
        '''
        result = self._values.get("api_key_source_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream".

        :default: - RestApi supports only UTF-8-encoded text payloads.
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def clone_from(self) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi]:
        '''The ID of the API Gateway RestApi resource that you want to clone.

        :default: - None.
        '''
        result = self._values.get("clone_from")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration]:
        '''The EndpointConfiguration property type specifies the endpoint types of a REST API.

        :default: EndpointType.EDGE

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration], result)

    @builtins.property
    def min_compression_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''A Size(in bytes, kibibytes, mebibytes etc) that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API.

        When compression is enabled, compression or
        decompression is not applied on the payload if the payload size is
        smaller than this value. Setting it to zero allows compression for any
        payload size.

        :default: - Compression is disabled.
        '''
        result = self._values.get("min_compression_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API.

        When compression is enabled, compression or
        decompression is not applied on the payload if the payload size is
        smaller than this value. Setting it to zero allows compression for any
        payload size.

        :default: - Compression is disabled.

        :deprecated: - superseded by ``minCompressionSize``

        :stability: deprecated
        '''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domains(self) -> typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName]:
        '''List of custom domains names to be used for the API Gateway.'''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName], result)

    @builtins.property
    def vpc_endpoint(self) -> _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint:
        '''VPC endpoint id of execute-api vpc endpoint.

        This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        '''
        result = self._values.get("vpc_endpoint")
        assert result is not None, "Required property 'vpc_endpoint' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint, result)

    @builtins.property
    def api_base_path_mapping_path(self) -> typing.Optional[builtins.str]:
        '''Path for custom domain base path mapping that will be attached to the api gateway.'''
        result = self._values.get("api_base_path_mapping_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Stage name  used for all cloudformation resource names and internal aws resource names.

        :deprecated: use deployOptions.stageName instead

        :stability: deprecated
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalApiGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InternalService(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-internal-gateway.InternalService",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        sub_domain: builtins.str,
        subject_alternative_names: typing.Sequence[builtins.str],
        subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
        add_load_balancer_redirect: typing.Optional[builtins.bool] = None,
        custom_domain_ssl_policy: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.SecurityPolicy] = None,
        enable_load_balancer_access_logs: typing.Optional[builtins.bool] = None,
        load_balancer_listener_ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.SslPolicy] = None,
        load_balancer_security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param hosted_zone: Hosted zone that will be used for the custom domain.
        :param sub_domain: Subdomain attached to hosted zone name.
        :param subject_alternative_names: List of alternative domains attached to the solution.
        :param subnet_selection: Subnets attached to the application load balancer.
        :param vpc: VPC attached to the application load balancer.
        :param vpc_endpoint_ip_addresses: VPC endpoint ip addresses attached to the load balancer`s target group.
        :param add_load_balancer_redirect: Add load balancer redirect from port 80 to 443. Default: true
        :param custom_domain_ssl_policy: SSLPolicy attached to the apigateway custom domain. Default: apigateway.SslPolicy.TLS_1_2
        :param enable_load_balancer_access_logs: Enable or disable access logs for the load balancer to follow AWS best practices for security. Default: true
        :param load_balancer_listener_ssl_policy: SSLPolicy attached to the load balancer listener. Default: elb.SslPolicy.FORWARD_SECRECY_TLS12_RES_GCM
        :param load_balancer_security_group: Use a custom security group used for the load balancer. By default, a security group will be created with inbound access to the typical private network CIDR ranges 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 and port 443. Any inbound access (0.0.0.0/0) is blocked by default to follow AWS best practices for security. Outbound traffic is allowed to all destinations.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6fdb0604ec77d74f01c7b51d0cc12d16e1d2a8b65e1698a885908e24dec96a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InternalServiceProps(
            hosted_zone=hosted_zone,
            sub_domain=sub_domain,
            subject_alternative_names=subject_alternative_names,
            subnet_selection=subnet_selection,
            vpc=vpc,
            vpc_endpoint_ip_addresses=vpc_endpoint_ip_addresses,
            add_load_balancer_redirect=add_load_balancer_redirect,
            custom_domain_ssl_policy=custom_domain_ssl_policy,
            enable_load_balancer_access_logs=enable_load_balancer_access_logs,
            load_balancer_listener_ssl_policy=load_balancer_listener_ssl_policy,
            load_balancer_security_group=load_balancer_security_group,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName]:
        '''List of domains created by the internal service stack and shared with the api gateway stack.'''
        return typing.cast(typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName], jsii.get(self, "domains"))


@jsii.data_type(
    jsii_type="cdk-internal-gateway.InternalServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone": "hostedZone",
        "sub_domain": "subDomain",
        "subject_alternative_names": "subjectAlternativeNames",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "vpc_endpoint_ip_addresses": "vpcEndpointIPAddresses",
        "add_load_balancer_redirect": "addLoadBalancerRedirect",
        "custom_domain_ssl_policy": "customDomainSSLPolicy",
        "enable_load_balancer_access_logs": "enableLoadBalancerAccessLogs",
        "load_balancer_listener_ssl_policy": "loadBalancerListenerSSLPolicy",
        "load_balancer_security_group": "loadBalancerSecurityGroup",
    },
)
class InternalServiceProps:
    def __init__(
        self,
        *,
        hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        sub_domain: builtins.str,
        subject_alternative_names: typing.Sequence[builtins.str],
        subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
        add_load_balancer_redirect: typing.Optional[builtins.bool] = None,
        custom_domain_ssl_policy: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.SecurityPolicy] = None,
        enable_load_balancer_access_logs: typing.Optional[builtins.bool] = None,
        load_balancer_listener_ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.SslPolicy] = None,
        load_balancer_security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''Properties for InternalService.

        :param hosted_zone: Hosted zone that will be used for the custom domain.
        :param sub_domain: Subdomain attached to hosted zone name.
        :param subject_alternative_names: List of alternative domains attached to the solution.
        :param subnet_selection: Subnets attached to the application load balancer.
        :param vpc: VPC attached to the application load balancer.
        :param vpc_endpoint_ip_addresses: VPC endpoint ip addresses attached to the load balancer`s target group.
        :param add_load_balancer_redirect: Add load balancer redirect from port 80 to 443. Default: true
        :param custom_domain_ssl_policy: SSLPolicy attached to the apigateway custom domain. Default: apigateway.SslPolicy.TLS_1_2
        :param enable_load_balancer_access_logs: Enable or disable access logs for the load balancer to follow AWS best practices for security. Default: true
        :param load_balancer_listener_ssl_policy: SSLPolicy attached to the load balancer listener. Default: elb.SslPolicy.FORWARD_SECRECY_TLS12_RES_GCM
        :param load_balancer_security_group: Use a custom security group used for the load balancer. By default, a security group will be created with inbound access to the typical private network CIDR ranges 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 and port 443. Any inbound access (0.0.0.0/0) is blocked by default to follow AWS best practices for security. Outbound traffic is allowed to all destinations.
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc10cdccafe7b9adef536e2eb7718e1b504c653f343e7e2cbb0c9201b00217a7)
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument sub_domain", value=sub_domain, expected_type=type_hints["sub_domain"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_endpoint_ip_addresses", value=vpc_endpoint_ip_addresses, expected_type=type_hints["vpc_endpoint_ip_addresses"])
            check_type(argname="argument add_load_balancer_redirect", value=add_load_balancer_redirect, expected_type=type_hints["add_load_balancer_redirect"])
            check_type(argname="argument custom_domain_ssl_policy", value=custom_domain_ssl_policy, expected_type=type_hints["custom_domain_ssl_policy"])
            check_type(argname="argument enable_load_balancer_access_logs", value=enable_load_balancer_access_logs, expected_type=type_hints["enable_load_balancer_access_logs"])
            check_type(argname="argument load_balancer_listener_ssl_policy", value=load_balancer_listener_ssl_policy, expected_type=type_hints["load_balancer_listener_ssl_policy"])
            check_type(argname="argument load_balancer_security_group", value=load_balancer_security_group, expected_type=type_hints["load_balancer_security_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hosted_zone": hosted_zone,
            "sub_domain": sub_domain,
            "subject_alternative_names": subject_alternative_names,
            "subnet_selection": subnet_selection,
            "vpc": vpc,
            "vpc_endpoint_ip_addresses": vpc_endpoint_ip_addresses,
        }
        if add_load_balancer_redirect is not None:
            self._values["add_load_balancer_redirect"] = add_load_balancer_redirect
        if custom_domain_ssl_policy is not None:
            self._values["custom_domain_ssl_policy"] = custom_domain_ssl_policy
        if enable_load_balancer_access_logs is not None:
            self._values["enable_load_balancer_access_logs"] = enable_load_balancer_access_logs
        if load_balancer_listener_ssl_policy is not None:
            self._values["load_balancer_listener_ssl_policy"] = load_balancer_listener_ssl_policy
        if load_balancer_security_group is not None:
            self._values["load_balancer_security_group"] = load_balancer_security_group

    @builtins.property
    def hosted_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        '''Hosted zone that will be used for the custom domain.'''
        result = self._values.get("hosted_zone")
        assert result is not None, "Required property 'hosted_zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, result)

    @builtins.property
    def sub_domain(self) -> builtins.str:
        '''Subdomain attached to hosted zone name.'''
        result = self._values.get("sub_domain")
        assert result is not None, "Required property 'sub_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject_alternative_names(self) -> typing.List[builtins.str]:
        '''List of alternative domains attached to the solution.'''
        result = self._values.get("subject_alternative_names")
        assert result is not None, "Required property 'subject_alternative_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''Subnets attached to the application load balancer.'''
        result = self._values.get("subnet_selection")
        assert result is not None, "Required property 'subnet_selection' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC attached to the application load balancer.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_endpoint_ip_addresses(self) -> typing.List[builtins.str]:
        '''VPC endpoint ip addresses attached to the load balancer`s target group.'''
        result = self._values.get("vpc_endpoint_ip_addresses")
        assert result is not None, "Required property 'vpc_endpoint_ip_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def add_load_balancer_redirect(self) -> typing.Optional[builtins.bool]:
        '''Add load balancer redirect from port 80 to 443.

        :default: true
        '''
        result = self._values.get("add_load_balancer_redirect")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_domain_ssl_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.SecurityPolicy]:
        '''SSLPolicy attached to the apigateway custom domain.

        :default: apigateway.SslPolicy.TLS_1_2
        '''
        result = self._values.get("custom_domain_ssl_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.SecurityPolicy], result)

    @builtins.property
    def enable_load_balancer_access_logs(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable access logs for the load balancer to follow AWS best practices for security.

        :default: true
        '''
        result = self._values.get("enable_load_balancer_access_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancer_listener_ssl_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.SslPolicy]:
        '''SSLPolicy attached to the load balancer listener.

        :default: elb.SslPolicy.FORWARD_SECRECY_TLS12_RES_GCM
        '''
        result = self._values.get("load_balancer_listener_ssl_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.SslPolicy], result)

    @builtins.property
    def load_balancer_security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Use a custom security group used for the load balancer.

        By default, a security group will be created with inbound access to the typical private network CIDR ranges 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 and port 443.
        Any inbound access (0.0.0.0/0) is blocked by default to follow AWS best practices for security.
        Outbound traffic is allowed to all destinations.
        '''
        result = self._values.get("load_balancer_security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InternalWebsite(
    InternalApiGateway,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-internal-gateway.InternalWebsite",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source_path: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        enable_source_deployment: typing.Optional[builtins.bool] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
        vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
        api_base_path_mapping_path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
        endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
        default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_watch_role: typing.Optional[builtins.bool] = None,
        deploy: typing.Optional[builtins.bool] = None,
        deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
        domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_export_name: typing.Optional[builtins.str] = None,
        endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
        fail_on_warnings: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        rest_api_name: typing.Optional[builtins.str] = None,
        retain_deployments: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source_path: Path of website folder containing the website`s sources.
        :param bucket_name: Name of s3 bucket to use for the website deployment.
        :param enable_source_deployment: Enable/disable automatic sync of the website`s sources to the S3bucket. Default: true
        :param website_index_document: Name of html index document used for the website. Default: index.html
        :param domains: List of custom domains names to be used for the API Gateway.
        :param vpc_endpoint: VPC endpoint id of execute-api vpc endpoint. This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        :param api_base_path_mapping_path: Path for custom domain base path mapping that will be attached to the api gateway.
        :param stage: (deprecated) Stage name used for all cloudformation resource names and internal aws resource names.
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param endpoint_configuration: The EndpointConfiguration property type specifies the endpoint types of a REST API. Default: EndpointType.EDGE
        :param min_compression_size: A Size(in bytes, kibibytes, mebibytes etc) that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param minimum_compression_size: (deprecated) A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: - false if ``@aws-cdk/aws-apigateway:disableCloudWatchRole`` is enabled, true otherwise
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the RestApi construct. Default: - 'Automatically created by the RestApi construct'
        :param disable_execute_api_endpoint: Specifies whether clients can invoke the API using the default execute-api endpoint. To require that clients use a custom domain name to invoke the API, disable the default endpoint. Default: false
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: EndpointType.EDGE
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d516b7187660b534cf465c6154956083e900ca2144209c0ad2326e2da9610ff6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InternalWebsiteProps(
            source_path=source_path,
            bucket_name=bucket_name,
            enable_source_deployment=enable_source_deployment,
            website_index_document=website_index_document,
            domains=domains,
            vpc_endpoint=vpc_endpoint,
            api_base_path_mapping_path=api_base_path_mapping_path,
            stage=stage,
            api_key_source_type=api_key_source_type,
            binary_media_types=binary_media_types,
            clone_from=clone_from,
            endpoint_configuration=endpoint_configuration,
            min_compression_size=min_compression_size,
            minimum_compression_size=minimum_compression_size,
            default_cors_preflight_options=default_cors_preflight_options,
            default_integration=default_integration,
            default_method_options=default_method_options,
            cloud_watch_role=cloud_watch_role,
            deploy=deploy,
            deploy_options=deploy_options,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            domain_name=domain_name,
            endpoint_export_name=endpoint_export_name,
            endpoint_types=endpoint_types,
            fail_on_warnings=fail_on_warnings,
            parameters=parameters,
            policy=policy,
            rest_api_name=rest_api_name,
            retain_deployments=retain_deployments,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-internal-gateway.InternalWebsiteProps",
    jsii_struct_bases=[InternalApiGatewayProps],
    name_mapping={
        "default_cors_preflight_options": "defaultCorsPreflightOptions",
        "default_integration": "defaultIntegration",
        "default_method_options": "defaultMethodOptions",
        "cloud_watch_role": "cloudWatchRole",
        "deploy": "deploy",
        "deploy_options": "deployOptions",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "domain_name": "domainName",
        "endpoint_export_name": "endpointExportName",
        "endpoint_types": "endpointTypes",
        "fail_on_warnings": "failOnWarnings",
        "parameters": "parameters",
        "policy": "policy",
        "rest_api_name": "restApiName",
        "retain_deployments": "retainDeployments",
        "api_key_source_type": "apiKeySourceType",
        "binary_media_types": "binaryMediaTypes",
        "clone_from": "cloneFrom",
        "endpoint_configuration": "endpointConfiguration",
        "min_compression_size": "minCompressionSize",
        "minimum_compression_size": "minimumCompressionSize",
        "domains": "domains",
        "vpc_endpoint": "vpcEndpoint",
        "api_base_path_mapping_path": "apiBasePathMappingPath",
        "stage": "stage",
        "source_path": "sourcePath",
        "bucket_name": "bucketName",
        "enable_source_deployment": "enableSourceDeployment",
        "website_index_document": "websiteIndexDocument",
    },
)
class InternalWebsiteProps(InternalApiGatewayProps):
    def __init__(
        self,
        *,
        default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
        default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_watch_role: typing.Optional[builtins.bool] = None,
        deploy: typing.Optional[builtins.bool] = None,
        deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
        domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_export_name: typing.Optional[builtins.str] = None,
        endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
        fail_on_warnings: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        rest_api_name: typing.Optional[builtins.str] = None,
        retain_deployments: typing.Optional[builtins.bool] = None,
        api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
        endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
        vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
        api_base_path_mapping_path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        source_path: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        enable_source_deployment: typing.Optional[builtins.bool] = None,
        website_index_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for InternalService.

        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: - false if ``@aws-cdk/aws-apigateway:disableCloudWatchRole`` is enabled, true otherwise
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the RestApi construct. Default: - 'Automatically created by the RestApi construct'
        :param disable_execute_api_endpoint: Specifies whether clients can invoke the API using the default execute-api endpoint. To require that clients use a custom domain name to invoke the API, disable the default endpoint. Default: false
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: EndpointType.EDGE
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param endpoint_configuration: The EndpointConfiguration property type specifies the endpoint types of a REST API. Default: EndpointType.EDGE
        :param min_compression_size: A Size(in bytes, kibibytes, mebibytes etc) that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param minimum_compression_size: (deprecated) A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param domains: List of custom domains names to be used for the API Gateway.
        :param vpc_endpoint: VPC endpoint id of execute-api vpc endpoint. This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        :param api_base_path_mapping_path: Path for custom domain base path mapping that will be attached to the api gateway.
        :param stage: (deprecated) Stage name used for all cloudformation resource names and internal aws resource names.
        :param source_path: Path of website folder containing the website`s sources.
        :param bucket_name: Name of s3 bucket to use for the website deployment.
        :param enable_source_deployment: Enable/disable automatic sync of the website`s sources to the S3bucket. Default: true
        :param website_index_document: Name of html index document used for the website. Default: index.html
        '''
        if isinstance(default_cors_preflight_options, dict):
            default_cors_preflight_options = _aws_cdk_aws_apigateway_ceddda9d.CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict):
            default_method_options = _aws_cdk_aws_apigateway_ceddda9d.MethodOptions(**default_method_options)
        if isinstance(deploy_options, dict):
            deploy_options = _aws_cdk_aws_apigateway_ceddda9d.StageOptions(**deploy_options)
        if isinstance(domain_name, dict):
            domain_name = _aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions(**domain_name)
        if isinstance(endpoint_configuration, dict):
            endpoint_configuration = _aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration(**endpoint_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5870defbfb19b1259aa25bc8864db1000e3c69b24aac88f8bdae9a291ecfa658)
            check_type(argname="argument default_cors_preflight_options", value=default_cors_preflight_options, expected_type=type_hints["default_cors_preflight_options"])
            check_type(argname="argument default_integration", value=default_integration, expected_type=type_hints["default_integration"])
            check_type(argname="argument default_method_options", value=default_method_options, expected_type=type_hints["default_method_options"])
            check_type(argname="argument cloud_watch_role", value=cloud_watch_role, expected_type=type_hints["cloud_watch_role"])
            check_type(argname="argument deploy", value=deploy, expected_type=type_hints["deploy"])
            check_type(argname="argument deploy_options", value=deploy_options, expected_type=type_hints["deploy_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument endpoint_export_name", value=endpoint_export_name, expected_type=type_hints["endpoint_export_name"])
            check_type(argname="argument endpoint_types", value=endpoint_types, expected_type=type_hints["endpoint_types"])
            check_type(argname="argument fail_on_warnings", value=fail_on_warnings, expected_type=type_hints["fail_on_warnings"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument rest_api_name", value=rest_api_name, expected_type=type_hints["rest_api_name"])
            check_type(argname="argument retain_deployments", value=retain_deployments, expected_type=type_hints["retain_deployments"])
            check_type(argname="argument api_key_source_type", value=api_key_source_type, expected_type=type_hints["api_key_source_type"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument clone_from", value=clone_from, expected_type=type_hints["clone_from"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument min_compression_size", value=min_compression_size, expected_type=type_hints["min_compression_size"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument vpc_endpoint", value=vpc_endpoint, expected_type=type_hints["vpc_endpoint"])
            check_type(argname="argument api_base_path_mapping_path", value=api_base_path_mapping_path, expected_type=type_hints["api_base_path_mapping_path"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument enable_source_deployment", value=enable_source_deployment, expected_type=type_hints["enable_source_deployment"])
            check_type(argname="argument website_index_document", value=website_index_document, expected_type=type_hints["website_index_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domains": domains,
            "vpc_endpoint": vpc_endpoint,
            "source_path": source_path,
        }
        if default_cors_preflight_options is not None:
            self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None:
            self._values["default_integration"] = default_integration
        if default_method_options is not None:
            self._values["default_method_options"] = default_method_options
        if cloud_watch_role is not None:
            self._values["cloud_watch_role"] = cloud_watch_role
        if deploy is not None:
            self._values["deploy"] = deploy
        if deploy_options is not None:
            self._values["deploy_options"] = deploy_options
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if endpoint_export_name is not None:
            self._values["endpoint_export_name"] = endpoint_export_name
        if endpoint_types is not None:
            self._values["endpoint_types"] = endpoint_types
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy is not None:
            self._values["policy"] = policy
        if rest_api_name is not None:
            self._values["rest_api_name"] = rest_api_name
        if retain_deployments is not None:
            self._values["retain_deployments"] = retain_deployments
        if api_key_source_type is not None:
            self._values["api_key_source_type"] = api_key_source_type
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if clone_from is not None:
            self._values["clone_from"] = clone_from
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if min_compression_size is not None:
            self._values["min_compression_size"] = min_compression_size
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size
        if api_base_path_mapping_path is not None:
            self._values["api_base_path_mapping_path"] = api_base_path_mapping_path
        if stage is not None:
            self._values["stage"] = stage
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if enable_source_deployment is not None:
            self._values["enable_source_deployment"] = enable_source_deployment
        if website_index_document is not None:
            self._values["website_index_document"] = website_index_document

    @builtins.property
    def default_cors_preflight_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions]:
        '''Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        :default: - CORS is disabled
        '''
        result = self._values.get("default_cors_preflight_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions], result)

    @builtins.property
    def default_integration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration]:
        '''An integration to use as a default for all methods created within this API unless an integration is specified.

        :default: - Inherited from parent.
        '''
        result = self._values.get("default_integration")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration], result)

    @builtins.property
    def default_method_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions]:
        '''Method options to use as a default for all methods created within this API unless custom options are specified.

        :default: - Inherited from parent.
        '''
        result = self._values.get("default_method_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions], result)

    @builtins.property
    def cloud_watch_role(self) -> typing.Optional[builtins.bool]:
        '''Automatically configure an AWS CloudWatch role for API Gateway.

        :default: - false if ``@aws-cdk/aws-apigateway:disableCloudWatchRole`` is enabled, true otherwise
        '''
        result = self._values.get("cloud_watch_role")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deploy(self) -> typing.Optional[builtins.bool]:
        '''Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes.

        Since API Gateway deployments are immutable, When this option is enabled
        (by default), an AWS::ApiGateway::Deployment resource will automatically
        created with a logical ID that hashes the API model (methods, resources
        and options). This means that when the model changes, the logical ID of
        this CloudFormation resource will change, and a new deployment will be
        created.

        If this is set, ``latestDeployment`` will refer to the ``Deployment`` object
        and ``deploymentStage`` will refer to a ``Stage`` that points to this
        deployment. To customize the stage options, use the ``deployOptions``
        property.

        A CloudFormation Output will also be defined with the root URL endpoint
        of this REST API.

        :default: true
        '''
        result = self._values.get("deploy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deploy_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.StageOptions]:
        '''Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled.

        If ``deploy`` is disabled,
        this value cannot be set.

        :default: - Based on defaults of ``StageOptions``.
        '''
        result = self._values.get("deploy_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.StageOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the RestApi construct.

        :default: - 'Automatically created by the RestApi construct'
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether clients can invoke the API using the default execute-api endpoint.

        To require that clients use a custom domain name to invoke the
        API, disable the default endpoint.

        :default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain_name(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions]:
        '''Configure a custom domain name and map it to this API.

        :default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions], result)

    @builtins.property
    def endpoint_export_name(self) -> typing.Optional[builtins.str]:
        '''Export name for the CfnOutput containing the API endpoint.

        :default: - when no export name is given, output will be created without export
        '''
        result = self._values.get("endpoint_export_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_types(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]]:
        '''A list of the endpoint types of the API.

        Use this property when creating
        an API.

        :default: EndpointType.EDGE
        '''
        result = self._values.get("endpoint_types")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]], result)

    @builtins.property
    def fail_on_warnings(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource.

        :default: false
        '''
        result = self._values.get("fail_on_warnings")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom header parameters for the request.

        :default: - No parameters.

        :see: https://docs.aws.amazon.com/cli/latest/reference/apigateway/import-rest-api.html
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def policy(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument]:
        '''A policy document that contains the permissions for this RestApi.

        :default: - No policy.
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument], result)

    @builtins.property
    def rest_api_name(self) -> typing.Optional[builtins.str]:
        '''A name for the API Gateway RestApi resource.

        :default: - ID of the RestApi construct.
        '''
        result = self._values.get("rest_api_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retain_deployments(self) -> typing.Optional[builtins.bool]:
        '''Retains old deployment resources when the API changes.

        This allows
        manually reverting stages to point to old deployments via the AWS
        Console.

        :default: false
        '''
        result = self._values.get("retain_deployments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def api_key_source_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType]:
        '''The source of the API key for metering requests according to a usage plan.

        :default: - Metering is disabled.
        '''
        result = self._values.get("api_key_source_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream".

        :default: - RestApi supports only UTF-8-encoded text payloads.
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def clone_from(self) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi]:
        '''The ID of the API Gateway RestApi resource that you want to clone.

        :default: - None.
        '''
        result = self._values.get("clone_from")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration]:
        '''The EndpointConfiguration property type specifies the endpoint types of a REST API.

        :default: EndpointType.EDGE

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration], result)

    @builtins.property
    def min_compression_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''A Size(in bytes, kibibytes, mebibytes etc) that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API.

        When compression is enabled, compression or
        decompression is not applied on the payload if the payload size is
        smaller than this value. Setting it to zero allows compression for any
        payload size.

        :default: - Compression is disabled.
        '''
        result = self._values.get("min_compression_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API.

        When compression is enabled, compression or
        decompression is not applied on the payload if the payload size is
        smaller than this value. Setting it to zero allows compression for any
        payload size.

        :default: - Compression is disabled.

        :deprecated: - superseded by ``minCompressionSize``

        :stability: deprecated
        '''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domains(self) -> typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName]:
        '''List of custom domains names to be used for the API Gateway.'''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName], result)

    @builtins.property
    def vpc_endpoint(self) -> _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint:
        '''VPC endpoint id of execute-api vpc endpoint.

        This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        '''
        result = self._values.get("vpc_endpoint")
        assert result is not None, "Required property 'vpc_endpoint' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint, result)

    @builtins.property
    def api_base_path_mapping_path(self) -> typing.Optional[builtins.str]:
        '''Path for custom domain base path mapping that will be attached to the api gateway.'''
        result = self._values.get("api_base_path_mapping_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Stage name  used for all cloudformation resource names and internal aws resource names.

        :deprecated: use deployOptions.stageName instead

        :stability: deprecated
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_path(self) -> builtins.str:
        '''Path of website folder containing the website`s sources.'''
        result = self._values.get("source_path")
        assert result is not None, "Required property 'source_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Name of s3 bucket to use for the website deployment.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_source_deployment(self) -> typing.Optional[builtins.bool]:
        '''Enable/disable automatic sync of the website`s sources to the S3bucket.

        :default: true
        '''
        result = self._values.get("enable_source_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def website_index_document(self) -> typing.Optional[builtins.str]:
        '''Name of html index document used for the website.

        :default: index.html
        '''
        result = self._values.get("website_index_document")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalWebsiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "InternalApiGateway",
    "InternalApiGatewayProps",
    "InternalService",
    "InternalServiceProps",
    "InternalWebsite",
    "InternalWebsiteProps",
]

publication.publish()

def _typecheckingstub__d9ae54245009148c66f767401f5250017b64fe5bce1d826b5a4ab5f903630362(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
    vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    api_base_path_mapping_path: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
    default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_watch_role: typing.Optional[builtins.bool] = None,
    deploy: typing.Optional[builtins.bool] = None,
    deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
    domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_export_name: typing.Optional[builtins.str] = None,
    endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
    fail_on_warnings: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    rest_api_name: typing.Optional[builtins.str] = None,
    retain_deployments: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d09850aa6d812c4e31fc3d6e1747f6fd2cd0e17db65131fb04491c03f3d23f9(
    *,
    default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
    default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_watch_role: typing.Optional[builtins.bool] = None,
    deploy: typing.Optional[builtins.bool] = None,
    deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
    domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_export_name: typing.Optional[builtins.str] = None,
    endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
    fail_on_warnings: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    rest_api_name: typing.Optional[builtins.str] = None,
    retain_deployments: typing.Optional[builtins.bool] = None,
    api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
    vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    api_base_path_mapping_path: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6fdb0604ec77d74f01c7b51d0cc12d16e1d2a8b65e1698a885908e24dec96a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    sub_domain: builtins.str,
    subject_alternative_names: typing.Sequence[builtins.str],
    subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
    add_load_balancer_redirect: typing.Optional[builtins.bool] = None,
    custom_domain_ssl_policy: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.SecurityPolicy] = None,
    enable_load_balancer_access_logs: typing.Optional[builtins.bool] = None,
    load_balancer_listener_ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.SslPolicy] = None,
    load_balancer_security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc10cdccafe7b9adef536e2eb7718e1b504c653f343e7e2cbb0c9201b00217a7(
    *,
    hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    sub_domain: builtins.str,
    subject_alternative_names: typing.Sequence[builtins.str],
    subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
    add_load_balancer_redirect: typing.Optional[builtins.bool] = None,
    custom_domain_ssl_policy: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.SecurityPolicy] = None,
    enable_load_balancer_access_logs: typing.Optional[builtins.bool] = None,
    load_balancer_listener_ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.SslPolicy] = None,
    load_balancer_security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d516b7187660b534cf465c6154956083e900ca2144209c0ad2326e2da9610ff6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source_path: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
    enable_source_deployment: typing.Optional[builtins.bool] = None,
    website_index_document: typing.Optional[builtins.str] = None,
    domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
    vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    api_base_path_mapping_path: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
    default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_watch_role: typing.Optional[builtins.bool] = None,
    deploy: typing.Optional[builtins.bool] = None,
    deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
    domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_export_name: typing.Optional[builtins.str] = None,
    endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
    fail_on_warnings: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    rest_api_name: typing.Optional[builtins.str] = None,
    retain_deployments: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5870defbfb19b1259aa25bc8864db1000e3c69b24aac88f8bdae9a291ecfa658(
    *,
    default_cors_preflight_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.CorsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    default_integration: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.Integration] = None,
    default_method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_watch_role: typing.Optional[builtins.bool] = None,
    deploy: typing.Optional[builtins.bool] = None,
    deploy_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.StageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[builtins.bool] = None,
    domain_name: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.DomainNameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_export_name: typing.Optional[builtins.str] = None,
    endpoint_types: typing.Optional[typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]] = None,
    fail_on_warnings: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    rest_api_name: typing.Optional[builtins.str] = None,
    retain_deployments: typing.Optional[builtins.bool] = None,
    api_key_source_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.ApiKeySourceType] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    clone_from: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRestApi] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.EndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_compression_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
    vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    api_base_path_mapping_path: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    source_path: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
    enable_source_deployment: typing.Optional[builtins.bool] = None,
    website_index_document: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
