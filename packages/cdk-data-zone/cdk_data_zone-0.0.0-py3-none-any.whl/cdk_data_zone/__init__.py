r'''
<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg" alt="Apache 2.0 License"></a>
  <a href="https://github.com/cdklabs/cdk-cicd-wrapper/actions/workflows/release.yml"><img src="https://github.com/cdklabs/cdk-data-zone/actions/workflows/release.yml/badge.svg" alt="Release badge"></a>
  <a href="https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cdklabs/cdk-data-zone"><img src="https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue" alt="Open in DEV Containers"></a>
</p>

# CDK Amazon DataZone Construct Library

**CDK Amazon DataZone** is an AWS CDK construct library that simplifies the creation and management of **Amazon DataZone** resources. This library enables developers to automate data governance, data cataloging, and secure data sharing across domains by using familiar infrastructure-as-code practices with AWS CDK.

## Features

* Easily create and manage Amazon DataZone components, such as Domains, Projects, and Environments.
* Seamless integration with the AWS CDK ecosystem, allowing users to manage DataZone resources alongside other AWS resources.
* Support for secure resource configurations like KMS encryption, S3 bucket management, and domain-level blueprinting.

## Installation

To install this library, use the following npm command:

```bash
npm install @cdklabs/cdk-data-zone
```

## Usage Example

Here’s an example of how to use the **@cdklabs/cdk-data-zone** library in your AWS CDK project:

```python
from aws_cdk import App, RemovalPolicy
from aws_cdk.aws_kms import Key
from aws_cdk.aws_s3 import Bucket, BucketEncryption


app = App()
stack = Stack(app, "TestStack")

# Create an S3 Bucket for the Blueprint
bucket = Bucket(stack, "BlueprintBucket",
    enforce_sSL=True,
    removal_policy=RemovalPolicy.DESTROY,
    auto_delete_objects=True,
    encryption=BucketEncryption.S3_MANAGED
)

# Create a DataZone Domain
domain = Domain(stack, "Domain",
    name="integration",
    encryption_key=Key(stack, "Key", enable_key_rotation=True)
)

# Enable a Blueprint for the Domain
blueprint = domain.enable_blueprint(BlueprintEnvironmentIdentifiers.DEFAULT_DATA_LAKE,
    parameters={
        "S3Location": f"s3://{bucket.bucketName}"
    }
)

# Create a Project within the Domain
project = domain.create_project("test-project",
    name="test-project",
    glossaries=Glossaries.from_file("./resources/glossaries.json"),
    forms=Forms.from_file("./resources/form-metadata.json")
)

# Create an Environment Profile for the Project
environment_profile = EnvironmentProfile(stack, "EnvironmentProfile",
    name="dev",
    blueprint=blueprint,
    project=project
)

# Create an Environment using the Environment Profile
Environment(stack, "environment",
    project=project,
    name="DEV",
    environment_profile=environment_profile
)

app.synth()
```

### Key Features Highlighted

* **Domain Creation**: Easily create Amazon DataZone Domains with encryption and other security features.
* **Project Management**: Use Blueprints, Forms, and Glossaries to structure data governance.
* **Environment Profiles**: Manage different environments within your data projects to ensure proper data governance policies.

## Projen for Development

This project leverages **Projen** for managing development workflows. Projen automates common tasks like dependency management, testing, and versioning.

### Getting Started with Development

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/cdklabs/cdk-data-zone.git
   cd cdk-data-zone
   ```
2. **Install Dependencies**:

   ```bash
   npx projen install
   ```
3. **Run Projen** to synthesize files:

   ```bash
   npx projen
   ```
4. **Build the Project**:

   ```bash
   npx projen build
   ```
5. **Run Tests**:

   ```bash
   npx projen test
   ```

## API Reference

Detailed documentation of the available constructs, their properties, and methods is available in the [API.md](API.md) file.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) guide for more details on how to get involved.

## Security policy

Please see the [SECURITY.md](SECURITY.md) for more information.

## License

This project is licensed under the **Apache-2.0** License. See the [LICENSE](LICENSE) file for more information.
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
import aws_cdk.aws_datazone as _aws_cdk_aws_datazone_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="cdk-data-zone.AssignmentType")
class AssignmentType(enum.Enum):
    '''
    :stability: experimental
    '''

    AUTOMATIC = "AUTOMATIC"
    '''
    :stability: experimental
    '''
    MANUAL = "MANUAL"
    '''
    :stability: experimental
    '''


class BlueprintEnvironmentIdentifiers(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.BlueprintEnvironmentIdentifiers",
):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_DATA_LAKE")
    def DEFAULT_DATA_LAKE(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_DATA_LAKE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_DATA_WAREHOUSE")
    def DEFAULT_DATA_WAREHOUSE(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_DATA_WAREHOUSE"))


@jsii.data_type(
    jsii_type="cdk-data-zone.BlueprintOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled_regions": "enabledRegions",
        "manage_access_role": "manageAccessRole",
        "parameters": "parameters",
        "provisioning_role": "provisioningRole",
        "regional_parameters": "regionalParameters",
    },
)
class BlueprintOptions:
    def __init__(
        self,
        *,
        enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''
        :param enabled_regions: 
        :param manage_access_role: 
        :param parameters: 
        :param provisioning_role: 
        :param regional_parameters: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9174e9e48b11fc149d0542cb6d797f68f53c56947552a33abfbb2c02f96fc524)
            check_type(argname="argument enabled_regions", value=enabled_regions, expected_type=type_hints["enabled_regions"])
            check_type(argname="argument manage_access_role", value=manage_access_role, expected_type=type_hints["manage_access_role"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument provisioning_role", value=provisioning_role, expected_type=type_hints["provisioning_role"])
            check_type(argname="argument regional_parameters", value=regional_parameters, expected_type=type_hints["regional_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled_regions is not None:
            self._values["enabled_regions"] = enabled_regions
        if manage_access_role is not None:
            self._values["manage_access_role"] = manage_access_role
        if parameters is not None:
            self._values["parameters"] = parameters
        if provisioning_role is not None:
            self._values["provisioning_role"] = provisioning_role
        if regional_parameters is not None:
            self._values["regional_parameters"] = regional_parameters

    @builtins.property
    def enabled_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def manage_access_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("manage_access_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def provisioning_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioning_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def regional_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("regional_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlueprintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.BlueprintProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "environment_blueprint_identifier": "environmentBlueprintIdentifier",
        "enabled_regions": "enabledRegions",
        "manage_access_role": "manageAccessRole",
        "parameters": "parameters",
        "provisioning_role": "provisioningRole",
        "regional_parameters": "regionalParameters",
    },
)
class BlueprintProps:
    def __init__(
        self,
        *,
        domain: "IDomain",
        environment_blueprint_identifier: builtins.str,
        enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''
        :param domain: 
        :param environment_blueprint_identifier: 
        :param enabled_regions: 
        :param manage_access_role: 
        :param parameters: 
        :param provisioning_role: 
        :param regional_parameters: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5d519c2328168c0fc7d2f83cdd29d93512a17dd1179c3659c4156010685e52)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument environment_blueprint_identifier", value=environment_blueprint_identifier, expected_type=type_hints["environment_blueprint_identifier"])
            check_type(argname="argument enabled_regions", value=enabled_regions, expected_type=type_hints["enabled_regions"])
            check_type(argname="argument manage_access_role", value=manage_access_role, expected_type=type_hints["manage_access_role"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument provisioning_role", value=provisioning_role, expected_type=type_hints["provisioning_role"])
            check_type(argname="argument regional_parameters", value=regional_parameters, expected_type=type_hints["regional_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "environment_blueprint_identifier": environment_blueprint_identifier,
        }
        if enabled_regions is not None:
            self._values["enabled_regions"] = enabled_regions
        if manage_access_role is not None:
            self._values["manage_access_role"] = manage_access_role
        if parameters is not None:
            self._values["parameters"] = parameters
        if provisioning_role is not None:
            self._values["provisioning_role"] = provisioning_role
        if regional_parameters is not None:
            self._values["regional_parameters"] = regional_parameters

    @builtins.property
    def domain(self) -> "IDomain":
        '''
        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast("IDomain", result)

    @builtins.property
    def environment_blueprint_identifier(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("environment_blueprint_identifier")
        assert result is not None, "Required property 'environment_blueprint_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def manage_access_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("manage_access_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def provisioning_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioning_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def regional_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("regional_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlueprintProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.CronOptions",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "time_zone": "timeZone",
        "week_day": "weekDay",
        "year": "year",
    },
)
class CronOptions:
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param day: (experimental) The day of the month to run this rule at. Default: - Every day of the month
        :param hour: (experimental) The hour to run this rule at. Default: - Every hour
        :param minute: (experimental) The minute to run this rule at. Default: - Every minute
        :param month: (experimental) The month to run this rule at. Default: - Every month
        :param time_zone: 
        :param week_day: (experimental) The day of the week to run this rule at. Default: - Any day of the week
        :param year: (experimental) The year to run this rule at. Default: - Every year

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947a0afbab5f8fb394387ef22cfb3a49ed5252de97be2b9b1a354db6a1f009ac)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if week_day is not None:
            self._values["week_day"] = week_day
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''(experimental) The day of the month to run this rule at.

        :default: - Every day of the month

        :stability: experimental
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hour to run this rule at.

        :default: - Every hour

        :stability: experimental
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        '''(experimental) The minute to run this rule at.

        :default: - Every minute

        :stability: experimental
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        '''(experimental) The month to run this rule at.

        :default: - Every month

        :stability: experimental
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        '''(experimental) The day of the week to run this rule at.

        :default: - Any day of the week

        :stability: experimental
        '''
        result = self._values.get("week_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def year(self) -> typing.Optional[builtins.str]:
        '''(experimental) The year to run this rule at.

        :default: - Every year

        :stability: experimental
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.DataSourceOptions",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "description": "description",
        "enabled": "enabled",
        "publish_on_import": "publishOnImport",
        "recommendation": "recommendation",
        "schedule": "schedule",
    },
)
class DataSourceOptions:
    def __init__(
        self,
        *,
        configuration: "IDataSourceConfiguration",
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        publish_on_import: typing.Optional[builtins.bool] = None,
        recommendation: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional["Schedule"] = None,
    ) -> None:
        '''
        :param configuration: 
        :param description: 
        :param enabled: 
        :param publish_on_import: 
        :param recommendation: 
        :param schedule: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d31fb03f6e7a17261639cb6cecfc9f6030d51ba05d5e1f621e18c52e272f49)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument publish_on_import", value=publish_on_import, expected_type=type_hints["publish_on_import"])
            check_type(argname="argument recommendation", value=recommendation, expected_type=type_hints["recommendation"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if publish_on_import is not None:
            self._values["publish_on_import"] = publish_on_import
        if recommendation is not None:
            self._values["recommendation"] = recommendation
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def configuration(self) -> "IDataSourceConfiguration":
        '''
        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("IDataSourceConfiguration", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_on_import(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("publish_on_import")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def recommendation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("recommendation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["Schedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.DataSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "environment": "environment",
        "name": "name",
        "project": "project",
        "description": "description",
        "enabled": "enabled",
        "publish_on_import": "publishOnImport",
        "recommendation": "recommendation",
        "schedule": "schedule",
    },
)
class DataSourceProps:
    def __init__(
        self,
        *,
        configuration: "IDataSourceConfiguration",
        environment: "IEnvironment",
        name: builtins.str,
        project: "IProject",
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        publish_on_import: typing.Optional[builtins.bool] = None,
        recommendation: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional["Schedule"] = None,
    ) -> None:
        '''
        :param configuration: 
        :param environment: 
        :param name: 
        :param project: 
        :param description: 
        :param enabled: 
        :param publish_on_import: 
        :param recommendation: 
        :param schedule: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c421054e1a8ec68e5fbd291de58b7620712135aa80aa4aac00ed7ed9c3a9b8)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument publish_on_import", value=publish_on_import, expected_type=type_hints["publish_on_import"])
            check_type(argname="argument recommendation", value=recommendation, expected_type=type_hints["recommendation"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
            "environment": environment,
            "name": name,
            "project": project,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if publish_on_import is not None:
            self._values["publish_on_import"] = publish_on_import
        if recommendation is not None:
            self._values["recommendation"] = recommendation
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def configuration(self) -> "IDataSourceConfiguration":
        '''
        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("IDataSourceConfiguration", result)

    @builtins.property
    def environment(self) -> "IEnvironment":
        '''
        :stability: experimental
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast("IEnvironment", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> "IProject":
        '''
        :stability: experimental
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast("IProject", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_on_import(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("publish_on_import")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def recommendation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("recommendation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["Schedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.DomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "domain_execution_role": "domainExecutionRole",
        "encryption_key": "encryptionKey",
        "single_sign_on": "singleSignOn",
        "tags": "tags",
    },
)
class DomainProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        domain_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        single_sign_on: typing.Optional[typing.Union["SingleSignOn", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: (experimental) The name of the Amazon DataZone domain.
        :param description: (experimental) The description of the Amazon DataZone domain.
        :param domain_execution_role: (experimental) The domain execution role that is created when an Amazon DataZone domain is created. The domain execution role is created in the AWS account that houses the Amazon DataZone domain.
        :param encryption_key: (experimental) The identifier of the AWS Key Management Service (KMS) key that is used to encrypt the Amazon DataZone domain, metadata, and reporting data.
        :param single_sign_on: (experimental) The single sign-on details in Amazon DataZone.
        :param tags: (experimental) The tags specified for the Amazon DataZone domain.

        :stability: experimental
        '''
        if isinstance(single_sign_on, dict):
            single_sign_on = SingleSignOn(**single_sign_on)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be61ee14bceb92d33c880ff02266f1d05a6cdbb2ac48816a7e2a344cd6c3036f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_execution_role", value=domain_execution_role, expected_type=type_hints["domain_execution_role"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument single_sign_on", value=single_sign_on, expected_type=type_hints["single_sign_on"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if domain_execution_role is not None:
            self._values["domain_execution_role"] = domain_execution_role
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if single_sign_on is not None:
            self._values["single_sign_on"] = single_sign_on
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-name
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''(experimental) The domain execution role that is created when an Amazon DataZone domain is created.

        The domain execution role is created in the AWS account that houses the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-domainexecutionrole
        :stability: experimental
        '''
        result = self._values.get("domain_execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The identifier of the AWS Key Management Service (KMS) key that is used to encrypt the Amazon DataZone domain, metadata, and reporting data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-kmskeyidentifier
        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def single_sign_on(self) -> typing.Optional["SingleSignOn"]:
        '''(experimental) The single sign-on details in Amazon DataZone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-singlesignon
        :stability: experimental
        '''
        result = self._values.get("single_sign_on")
        return typing.cast(typing.Optional["SingleSignOn"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The tags specified for the Amazon DataZone domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-domain.html#cfn-datazone-domain-tags
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.EnvironmentOptions",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "environment_role": "environmentRole",
        "glossary_terms": "glossaryTerms",
        "name": "name",
        "user_parameters": "userParameters",
    },
)
class EnvironmentOptions:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''
        :param description: (experimental) The description of the environment.
        :param environment_role: (experimental) The ARN of the environment role.
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon environment.
        :param name: (experimental) The name of the Amazon environment.
        :param user_parameters: (experimental) The user parameters of this Amazon environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664794b57fc9315d65327a443c89737ee5a48877ce6cc76518087a5e14c113db)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_role", value=environment_role, expected_type=type_hints["environment_role"])
            check_type(argname="argument glossary_terms", value=glossary_terms, expected_type=type_hints["glossary_terms"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument user_parameters", value=user_parameters, expected_type=type_hints["user_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if environment_role is not None:
            self._values["environment_role"] = environment_role
        if glossary_terms is not None:
            self._values["glossary_terms"] = glossary_terms
        if name is not None:
            self._values["name"] = name
        if user_parameters is not None:
            self._values["user_parameters"] = user_parameters

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''(experimental) The ARN of the environment role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-environmentrolearn
        :stability: experimental
        '''
        result = self._values.get("environment_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def glossary_terms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The glossary terms that can be used in this Amazon  environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-glossaryterms
        :stability: experimental
        '''
        result = self._values.get("glossary_terms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Amazon  environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-name
        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty]]]]:
        '''(experimental) The user parameters of this Amazon  environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-userparameters
        :stability: experimental
        '''
        result = self._values.get("user_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.EnvironmentProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "blueprint": "blueprint",
        "name": "name",
        "project": "project",
        "aws_account_id": "awsAccountId",
        "aws_account_region": "awsAccountRegion",
        "description": "description",
        "user_parameters": "userParameters",
    },
)
class EnvironmentProfileProps:
    def __init__(
        self,
        *,
        blueprint: "IBlueprint",
        name: builtins.str,
        project: "IProject",
        aws_account_id: typing.Optional[builtins.str] = None,
        aws_account_region: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironmentProfile.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''
        :param blueprint: (experimental) The identifier of a blueprint with which an environment profile is created.
        :param name: (experimental) The name of the environment profile.
        :param project: (experimental) The identifier of a project in which an environment profile exists.
        :param aws_account_id: (experimental) The identifier of an AWS account in which an environment profile exists. Default: the Domain account
        :param aws_account_region: (experimental) The AWS Region in which an environment profile exists. Default: the Domain region
        :param description: (experimental) The description of the environment profile.
        :param user_parameters: (experimental) The user parameters of this Amazon environment profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce7a8b5af595307cf5e5a57ffffe8cb4ea40412a444f9b32567726d9ee9416e)
            check_type(argname="argument blueprint", value=blueprint, expected_type=type_hints["blueprint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_account_region", value=aws_account_region, expected_type=type_hints["aws_account_region"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument user_parameters", value=user_parameters, expected_type=type_hints["user_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blueprint": blueprint,
            "name": name,
            "project": project,
        }
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if aws_account_region is not None:
            self._values["aws_account_region"] = aws_account_region
        if description is not None:
            self._values["description"] = description
        if user_parameters is not None:
            self._values["user_parameters"] = user_parameters

    @builtins.property
    def blueprint(self) -> "IBlueprint":
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-environmentblueprintidentifier
        :stability: experimental
        '''
        result = self._values.get("blueprint")
        assert result is not None, "Required property 'blueprint' is missing"
        return typing.cast("IBlueprint", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the environment profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-name
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> "IProject":
        '''(experimental) The identifier of a project in which an environment profile exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-projectidentifier
        :stability: experimental
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast("IProject", result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The identifier of an AWS account in which an environment profile exists.

        :default: the  Domain account

        :stability: experimental
        '''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_account_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS Region in which an environment profile exists.

        :default: the  Domain region

        :stability: experimental
        '''
        result = self._values.get("aws_account_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the environment profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-description
        :stability: experimental
        :attribute: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_datazone_ceddda9d.CfnEnvironmentProfile.EnvironmentParameterProperty]]]]:
        '''(experimental) The user parameters of this Amazon  environment profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environmentprofile.html#cfn-datazone-environmentprofile-userparameters
        :stability: experimental
        '''
        result = self._values.get("user_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_datazone_ceddda9d.CfnEnvironmentProfile.EnvironmentParameterProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.EnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "environment_profile": "environmentProfile",
        "name": "name",
        "project": "project",
        "description": "description",
        "environment_role": "environmentRole",
        "glossary_terms": "glossaryTerms",
        "user_parameters": "userParameters",
    },
)
class EnvironmentProps:
    def __init__(
        self,
        *,
        environment_profile: "IEnvironmentProfile",
        name: builtins.str,
        project: "IProject",
        description: typing.Optional[builtins.str] = None,
        environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''
        :param environment_profile: (experimental) The identifier of the environment profile that is used to create this Amazon environment.
        :param name: (experimental) The name of the Amazon environment.
        :param project: (experimental) The identifier of the Amazon project in which this environment is created.
        :param description: (experimental) The description of the environment.
        :param environment_role: (experimental) The ARN of the environment role.
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon environment.
        :param user_parameters: (experimental) The user parameters of this Amazon environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310ebc674182b1a77a8be6c07f83aa9b03eda25f34236464136dad18d5c49b5c)
            check_type(argname="argument environment_profile", value=environment_profile, expected_type=type_hints["environment_profile"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_role", value=environment_role, expected_type=type_hints["environment_role"])
            check_type(argname="argument glossary_terms", value=glossary_terms, expected_type=type_hints["glossary_terms"])
            check_type(argname="argument user_parameters", value=user_parameters, expected_type=type_hints["user_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "environment_profile": environment_profile,
            "name": name,
            "project": project,
        }
        if description is not None:
            self._values["description"] = description
        if environment_role is not None:
            self._values["environment_role"] = environment_role
        if glossary_terms is not None:
            self._values["glossary_terms"] = glossary_terms
        if user_parameters is not None:
            self._values["user_parameters"] = user_parameters

    @builtins.property
    def environment_profile(self) -> "IEnvironmentProfile":
        '''(experimental) The identifier of the environment profile that is used to create this Amazon  environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-environmentprofileidentifier
        :stability: experimental
        '''
        result = self._values.get("environment_profile")
        assert result is not None, "Required property 'environment_profile' is missing"
        return typing.cast("IEnvironmentProfile", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the Amazon  environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-name
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> "IProject":
        '''(experimental) The identifier of the Amazon  project in which this environment is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-projectidentifier
        :stability: experimental
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast("IProject", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''(experimental) The ARN of the environment role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-environmentrolearn
        :stability: experimental
        '''
        result = self._values.get("environment_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def glossary_terms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The glossary terms that can be used in this Amazon  environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-glossaryterms
        :stability: experimental
        '''
        result = self._values.get("glossary_terms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty]]]]:
        '''(experimental) The user parameters of this Amazon  environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-environment.html#cfn-datazone-environment-userparameters
        :stability: experimental
        '''
        result = self._values.get("user_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.FilterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "filter_expressions": "filterExpressions",
        "schema_name": "schemaName",
    },
)
class FilterConfiguration:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        filter_expressions: typing.Optional[typing.Sequence[typing.Union["FilterExpression", typing.Dict[builtins.str, typing.Any]]]] = None,
        schema_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: 
        :param filter_expressions: 
        :param schema_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0986bc3d0b93775c7380054ed7eef1eb47b04253092559571beeb2c689f80fb)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument filter_expressions", value=filter_expressions, expected_type=type_hints["filter_expressions"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
        }
        if filter_expressions is not None:
            self._values["filter_expressions"] = filter_expressions
        if schema_name is not None:
            self._values["schema_name"] = schema_name

    @builtins.property
    def database_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_expressions(self) -> typing.Optional[typing.List["FilterExpression"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("filter_expressions")
        return typing.cast(typing.Optional[typing.List["FilterExpression"]], result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.FilterExpression",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression", "filter_type": "filterType"},
)
class FilterExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        filter_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: 
        :param filter_type: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d25925af03022c6278dec9408a538c2b630c8718cfce52cef0fb0bfbb113c7)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if filter_type is not None:
            self._values["filter_type"] = filter_type

    @builtins.property
    def expression(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_type(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("filter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilterExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.FormMetadataOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "smithy_model": "smithyModel",
    },
)
class FormMetadataOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        smithy_model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param description: 
        :param smithy_model: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a819549416a173f3d9a2ac9241fc5a11ed9c9de2155fea28d75e9bd61ecf4262)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument smithy_model", value=smithy_model, expected_type=type_hints["smithy_model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if smithy_model is not None:
            self._values["smithy_model"] = smithy_model

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smithy_model(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("smithy_model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FormMetadataOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.FormMetadataProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "project": "project",
        "description": "description",
        "smithy_model": "smithyModel",
    },
)
class FormMetadataProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        project: "Project",
        description: typing.Optional[builtins.str] = None,
        smithy_model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param project: 
        :param description: 
        :param smithy_model: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7a06fb4f8ed49c7a486693f21a93d98bd83dc206d4a93849d6ef79e7bf96e1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument smithy_model", value=smithy_model, expected_type=type_hints["smithy_model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project": project,
        }
        if description is not None:
            self._values["description"] = description
        if smithy_model is not None:
            self._values["smithy_model"] = smithy_model

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast("Project", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smithy_model(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("smithy_model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FormMetadataProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Forms(metaclass=jsii.JSIIMeta, jsii_type="cdk-data-zone.Forms"):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(cls, path: builtins.str) -> "Forms":
        '''
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4db4c02c2fb0dc84bddc127bf74d0f2c9bcd78fb3bce93af85b3ef162071ab5)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("Forms", jsii.sinvoke(cls, "fromFile", [path]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, *options: FormMetadataOptions) -> "Forms":
        '''
        :param options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63acf890d658dc5eded567a6fff59c57245fe73e1bedb7be979fa726d56513fb)
            check_type(argname="argument options", value=options, expected_type=typing.Tuple[type_hints["options"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Forms", jsii.sinvoke(cls, "fromInline", [*options]))

    @builtins.property
    @jsii.member(jsii_name="metadataOptions")
    def metadata_options(self) -> typing.List[FormMetadataOptions]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[FormMetadataOptions], jsii.get(self, "metadataOptions"))


class Glossaries(metaclass=jsii.JSIIMeta, jsii_type="cdk-data-zone.Glossaries"):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(cls, path: builtins.str) -> "Glossaries":
        '''
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70150c439ae952f7bcc7b1a2e279c30668bfa336ea9e48cc1e309be2eb7926fd)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("Glossaries", jsii.sinvoke(cls, "fromFile", [path]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, *options: "GlossaryOptions") -> "Glossaries":
        '''
        :param options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f07aaa08eacd1bf8183d168acd09ee55f3496929f779ecd23bb81df97ddb96)
            check_type(argname="argument options", value=options, expected_type=typing.Tuple[type_hints["options"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Glossaries", jsii.sinvoke(cls, "fromInline", [*options]))

    @builtins.property
    @jsii.member(jsii_name="glossariesList")
    def glossaries_list(self) -> typing.List["GlossaryOptions"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["GlossaryOptions"], jsii.get(self, "glossariesList"))


@jsii.data_type(
    jsii_type="cdk-data-zone.GlossaryOptions",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "terms": "terms"},
)
class GlossaryOptions:
    def __init__(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        terms: typing.Optional[typing.Sequence[typing.Union["GlossaryTermOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param description: 
        :param name: 
        :param terms: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34522afadc47cf22b048237a90a7f11811d2602ad1249c220a7c35e3e79c06d3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument terms", value=terms, expected_type=type_hints["terms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "name": name,
        }
        if terms is not None:
            self._values["terms"] = terms

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terms(self) -> typing.Optional[typing.List["GlossaryTermOptions"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("terms")
        return typing.cast(typing.Optional[typing.List["GlossaryTermOptions"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlossaryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.GlossaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "project": "project",
        "terms": "terms",
    },
)
class GlossaryProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        project: "Project",
        terms: typing.Optional[typing.Sequence[typing.Union["GlossaryTermOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param description: 
        :param name: 
        :param project: 
        :param terms: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57d3ec706033ed8c378b2cb7657b3bf0375d7ccaf31ae4dfa275181495270fa)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument terms", value=terms, expected_type=type_hints["terms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "name": name,
            "project": project,
        }
        if terms is not None:
            self._values["terms"] = terms

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast("Project", result)

    @builtins.property
    def terms(self) -> typing.Optional[typing.List["GlossaryTermOptions"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("terms")
        return typing.cast(typing.Optional[typing.List["GlossaryTermOptions"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlossaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.GlossaryTermOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "enabled": "enabled",
        "long_description": "longDescription",
        "short_description": "shortDescription",
    },
)
class GlossaryTermOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        long_description: typing.Optional[builtins.str] = None,
        short_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param description: 
        :param enabled: 
        :param long_description: 
        :param short_description: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee37fb28a680fae7dd63770e7012a0e0abbc53fa4a06b772a31f0606e13290c4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument long_description", value=long_description, expected_type=type_hints["long_description"])
            check_type(argname="argument short_description", value=short_description, expected_type=type_hints["short_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if long_description is not None:
            self._values["long_description"] = long_description
        if short_description is not None:
            self._values["short_description"] = short_description

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def long_description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("long_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("short_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlossaryTermOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.GlossaryTermProps",
    jsii_struct_bases=[],
    name_mapping={
        "glossary": "glossary",
        "name": "name",
        "description": "description",
        "enabled": "enabled",
        "long_description": "longDescription",
        "short_description": "shortDescription",
    },
)
class GlossaryTermProps:
    def __init__(
        self,
        *,
        glossary: "IGlossary",
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        long_description: typing.Optional[builtins.str] = None,
        short_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param glossary: 
        :param name: 
        :param description: 
        :param enabled: 
        :param long_description: 
        :param short_description: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f7dbf13e321db0e2c80848935eb374e79f4ab5699445d83e484a4da333d40d)
            check_type(argname="argument glossary", value=glossary, expected_type=type_hints["glossary"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument long_description", value=long_description, expected_type=type_hints["long_description"])
            check_type(argname="argument short_description", value=short_description, expected_type=type_hints["short_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "glossary": glossary,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if long_description is not None:
            self._values["long_description"] = long_description
        if short_description is not None:
            self._values["short_description"] = short_description

    @builtins.property
    def glossary(self) -> "IGlossary":
        '''
        :stability: experimental
        '''
        result = self._values.get("glossary")
        assert result is not None, "Required property 'glossary' is missing"
        return typing.cast("IGlossary", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def long_description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("long_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("short_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlossaryTermProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-data-zone.IDataSourceConfiguration")
class IDataSourceConfiguration(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_datazone_ceddda9d.CfnDataSource.DataSourceConfigurationInputProperty:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _IDataSourceConfigurationProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IDataSourceConfiguration"

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_datazone_ceddda9d.CfnDataSource.DataSourceConfigurationInputProperty:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_datazone_ceddda9d.CfnDataSource.DataSourceConfigurationInputProperty, jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDataSourceConfiguration).__jsii_proxy_class__ = lambda : _IDataSourceConfigurationProxy


@jsii.interface(jsii_type="cdk-data-zone.IFormMetadata")
class IFormMetadata(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="formName")
    def form_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="formRevision")
    def form_revision(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _IFormMetadataProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IFormMetadata"

    @builtins.property
    @jsii.member(jsii_name="formName")
    def form_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "formName"))

    @builtins.property
    @jsii.member(jsii_name="formRevision")
    def form_revision(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "formRevision"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFormMetadata).__jsii_proxy_class__ = lambda : _IFormMetadataProxy


@jsii.interface(jsii_type="cdk-data-zone.IGlossary")
class IGlossary(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="glossaryId")
    def glossary_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addGlossaryTerms")
    def add_glossary_terms(
        self,
        terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
    ) -> typing.List["GlossaryTerm"]:
        '''
        :param terms: -

        :stability: experimental
        '''
        ...


class _IGlossaryProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IGlossary"

    @builtins.property
    @jsii.member(jsii_name="glossaryId")
    def glossary_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "glossaryId"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        return typing.cast("Project", jsii.get(self, "project"))

    @jsii.member(jsii_name="addGlossaryTerms")
    def add_glossary_terms(
        self,
        terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
    ) -> typing.List["GlossaryTerm"]:
        '''
        :param terms: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6cf000c38726d09ae0d29fb5be2383e80b10e5015924ad7c90d459fe70c585)
            check_type(argname="argument terms", value=terms, expected_type=type_hints["terms"])
        return typing.cast(typing.List["GlossaryTerm"], jsii.invoke(self, "addGlossaryTerms", [terms]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGlossary).__jsii_proxy_class__ = lambda : _IGlossaryProxy


@jsii.interface(jsii_type="cdk-data-zone.IGlossaryTerm")
class IGlossaryTerm(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="glossaryTermId")
    def glossary_term_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _IGlossaryTermProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IGlossaryTerm"

    @builtins.property
    @jsii.member(jsii_name="glossaryTermId")
    def glossary_term_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "glossaryTermId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGlossaryTerm).__jsii_proxy_class__ = lambda : _IGlossaryTermProxy


@jsii.interface(jsii_type="cdk-data-zone.IResource")
class IResource(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedAt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was updated.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: UpdatedAt
        '''
        ...


class _IResourceProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IResource"

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was updated.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResource).__jsii_proxy_class__ = lambda : _IResourceProxy


@jsii.data_type(
    jsii_type="cdk-data-zone.MemberOptions",
    jsii_struct_bases=[],
    name_mapping={
        "designation": "designation",
        "group_identifier": "groupIdentifier",
        "user_identifier": "userIdentifier",
    },
)
class MemberOptions:
    def __init__(
        self,
        *,
        designation: typing.Optional[builtins.str] = None,
        group_identifier: typing.Optional[builtins.str] = None,
        user_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param designation: 
        :param group_identifier: 
        :param user_identifier: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073b6b415151bee91b07bbfbf7f89a996446093cd162308f6712b97d92bd20d1)
            check_type(argname="argument designation", value=designation, expected_type=type_hints["designation"])
            check_type(argname="argument group_identifier", value=group_identifier, expected_type=type_hints["group_identifier"])
            check_type(argname="argument user_identifier", value=user_identifier, expected_type=type_hints["user_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if designation is not None:
            self._values["designation"] = designation
        if group_identifier is not None:
            self._values["group_identifier"] = group_identifier
        if user_identifier is not None:
            self._values["user_identifier"] = user_identifier

    @builtins.property
    def designation(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("designation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_identifier(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_identifier(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemberOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.ProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "forms": "forms",
        "glossaries": "glossaries",
        "glossary_terms": "glossaryTerms",
        "management_role": "managementRole",
    },
)
class ProjectOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        forms: typing.Optional[Forms] = None,
        glossaries: typing.Optional[Glossaries] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> None:
        '''
        :param name: (experimental) The name of a project.
        :param description: (experimental) The description of a project.
        :param forms: 
        :param glossaries: 
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon project.
        :param management_role: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b761796969f0d3e670ed3b0006657e72d98c1701c48439ffd336a6e7d59235ee)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument forms", value=forms, expected_type=type_hints["forms"])
            check_type(argname="argument glossaries", value=glossaries, expected_type=type_hints["glossaries"])
            check_type(argname="argument glossary_terms", value=glossary_terms, expected_type=type_hints["glossary_terms"])
            check_type(argname="argument management_role", value=management_role, expected_type=type_hints["management_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if forms is not None:
            self._values["forms"] = forms
        if glossaries is not None:
            self._values["glossaries"] = glossaries
        if glossary_terms is not None:
            self._values["glossary_terms"] = glossary_terms
        if management_role is not None:
            self._values["management_role"] = management_role

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-name
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forms(self) -> typing.Optional[Forms]:
        '''
        :stability: experimental
        '''
        result = self._values.get("forms")
        return typing.cast(typing.Optional[Forms], result)

    @builtins.property
    def glossaries(self) -> typing.Optional[Glossaries]:
        '''
        :stability: experimental
        '''
        result = self._values.get("glossaries")
        return typing.cast(typing.Optional[Glossaries], result)

    @builtins.property
    def glossary_terms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The glossary terms that can be used in this Amazon  project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-glossaryterms
        :stability: experimental
        '''
        result = self._values.get("glossary_terms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def management_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("management_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-data-zone.ProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "name": "name",
        "description": "description",
        "forms": "forms",
        "glossaries": "glossaries",
        "glossary_terms": "glossaryTerms",
        "management_role": "managementRole",
    },
)
class ProjectProps:
    def __init__(
        self,
        *,
        domain: "IDomain",
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        forms: typing.Optional[Forms] = None,
        glossaries: typing.Optional[Glossaries] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> None:
        '''
        :param domain: (experimental) The identifier of a Amazon domain where the project exists.
        :param name: (experimental) The name of a project.
        :param description: (experimental) The description of a project.
        :param forms: 
        :param glossaries: 
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon project.
        :param management_role: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d47d1d493aefcb3756340c66339ea0fb5bf4e7e6e1c8b921088768b24aaa56e)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument forms", value=forms, expected_type=type_hints["forms"])
            check_type(argname="argument glossaries", value=glossaries, expected_type=type_hints["glossaries"])
            check_type(argname="argument glossary_terms", value=glossary_terms, expected_type=type_hints["glossary_terms"])
            check_type(argname="argument management_role", value=management_role, expected_type=type_hints["management_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if forms is not None:
            self._values["forms"] = forms
        if glossaries is not None:
            self._values["glossaries"] = glossaries
        if glossary_terms is not None:
            self._values["glossary_terms"] = glossary_terms
        if management_role is not None:
            self._values["management_role"] = management_role

    @builtins.property
    def domain(self) -> "IDomain":
        '''(experimental) The identifier of a Amazon  domain where the project exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-domainidentifier
        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast("IDomain", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-name
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forms(self) -> typing.Optional[Forms]:
        '''
        :stability: experimental
        '''
        result = self._values.get("forms")
        return typing.cast(typing.Optional[Forms], result)

    @builtins.property
    def glossaries(self) -> typing.Optional[Glossaries]:
        '''
        :stability: experimental
        '''
        result = self._values.get("glossaries")
        return typing.cast(typing.Optional[Glossaries], result)

    @builtins.property
    def glossary_terms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The glossary terms that can be used in this Amazon  project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datazone-project.html#cfn-datazone-project-glossaryterms
        :stability: experimental
        '''
        result = self._values.get("glossary_terms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def management_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("management_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.ResourceBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2653735f026813879c695ad00ec9da3eb2ee8b45db72909b698dec0c236eb83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    @abc.abstractmethod
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedAt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    @abc.abstractmethod
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was updated.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: UpdatedAt
        '''
        ...


class _ResourceBaseProxy(
    ResourceBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was updated.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ResourceBase).__jsii_proxy_class__ = lambda : _ResourceBaseProxy


class Schedule(metaclass=jsii.JSIIMeta, jsii_type="cdk-data-zone.Schedule"):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromCron")
    @builtins.classmethod
    def from_cron(
        cls,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> "Schedule":
        '''
        :param day: (experimental) The day of the month to run this rule at. Default: - Every day of the month
        :param hour: (experimental) The hour to run this rule at. Default: - Every hour
        :param minute: (experimental) The minute to run this rule at. Default: - Every minute
        :param month: (experimental) The month to run this rule at. Default: - Every month
        :param time_zone: 
        :param week_day: (experimental) The day of the week to run this rule at. Default: - Any day of the week
        :param year: (experimental) The year to run this rule at. Default: - Every year

        :stability: experimental
        '''
        options = CronOptions(
            day=day,
            hour=hour,
            minute=minute,
            month=month,
            time_zone=time_zone,
            week_day=week_day,
            year=year,
        )

        return typing.cast("Schedule", jsii.sinvoke(cls, "fromCron", [options]))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezone"))


@jsii.data_type(
    jsii_type="cdk-data-zone.SingleSignOn",
    jsii_struct_bases=[],
    name_mapping={"sso_type": "ssoType", "user_assignment": "userAssignment"},
)
class SingleSignOn:
    def __init__(
        self,
        *,
        sso_type: "SingleSignOnType",
        user_assignment: typing.Optional[AssignmentType] = None,
    ) -> None:
        '''
        :param sso_type: 
        :param user_assignment: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d0be0fd72922e3b5144179fab0566e9caf316e037e370764fe12699af51531)
            check_type(argname="argument sso_type", value=sso_type, expected_type=type_hints["sso_type"])
            check_type(argname="argument user_assignment", value=user_assignment, expected_type=type_hints["user_assignment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sso_type": sso_type,
        }
        if user_assignment is not None:
            self._values["user_assignment"] = user_assignment

    @builtins.property
    def sso_type(self) -> "SingleSignOnType":
        '''
        :stability: experimental
        '''
        result = self._values.get("sso_type")
        assert result is not None, "Required property 'sso_type' is missing"
        return typing.cast("SingleSignOnType", result)

    @builtins.property
    def user_assignment(self) -> typing.Optional[AssignmentType]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_assignment")
        return typing.cast(typing.Optional[AssignmentType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SingleSignOn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-data-zone.SingleSignOnType")
class SingleSignOnType(enum.Enum):
    '''
    :stability: experimental
    '''

    IAM_IDC = "IAM_IDC"
    '''
    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="cdk-data-zone.SourceOptions",
    jsii_struct_bases=[],
    name_mapping={
        "filter_configurations": "filterConfigurations",
        "data_access_role": "dataAccessRole",
    },
)
class SourceOptions:
    def __init__(
        self,
        *,
        filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
        data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> None:
        '''
        :param filter_configurations: 
        :param data_access_role: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462cf6a60c403adadbe13c3e507d2d99decf7241492bd212afd90cd0fca56719)
            check_type(argname="argument filter_configurations", value=filter_configurations, expected_type=type_hints["filter_configurations"])
            check_type(argname="argument data_access_role", value=data_access_role, expected_type=type_hints["data_access_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_configurations": filter_configurations,
        }
        if data_access_role is not None:
            self._values["data_access_role"] = data_access_role

    @builtins.property
    def filter_configurations(self) -> typing.List[FilterConfiguration]:
        '''
        :stability: experimental
        '''
        result = self._values.get("filter_configurations")
        assert result is not None, "Required property 'filter_configurations' is missing"
        return typing.cast(typing.List[FilterConfiguration], result)

    @builtins.property
    def data_access_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_access_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDataSourceConfiguration)
class DataSourceConfigurationBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.DataSourceConfigurationBase",
):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromGlue")
    @builtins.classmethod
    def from_glue(
        cls,
        *,
        auto_import_data_quality_result: typing.Optional[builtins.bool] = None,
        filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
        data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> IDataSourceConfiguration:
        '''
        :param auto_import_data_quality_result: 
        :param filter_configurations: 
        :param data_access_role: 

        :stability: experimental
        '''
        options = GlueOptions(
            auto_import_data_quality_result=auto_import_data_quality_result,
            filter_configurations=filter_configurations,
            data_access_role=data_access_role,
        )

        return typing.cast(IDataSourceConfiguration, jsii.sinvoke(cls, "fromGlue", [options]))

    @jsii.member(jsii_name="fromRedshift")
    @builtins.classmethod
    def from_redshift(
        cls,
        *,
        credentials: _aws_cdk_aws_secretsmanager_ceddda9d.Secret,
        name: builtins.str,
        redshift_type: builtins.str,
        filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
        data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> IDataSourceConfiguration:
        '''
        :param credentials: 
        :param name: 
        :param redshift_type: 
        :param filter_configurations: 
        :param data_access_role: 

        :stability: experimental
        '''
        options = RedshiftOptions(
            credentials=credentials,
            name=name,
            redshift_type=redshift_type,
            filter_configurations=filter_configurations,
            data_access_role=data_access_role,
        )

        return typing.cast(IDataSourceConfiguration, jsii.sinvoke(cls, "fromRedshift", [options]))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    @abc.abstractmethod
    def configuration(
        self,
    ) -> _aws_cdk_aws_datazone_ceddda9d.CfnDataSource.DataSourceConfigurationInputProperty:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="filterType")
    @abc.abstractmethod
    def filter_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _DataSourceConfigurationBaseProxy(DataSourceConfigurationBase):
    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_datazone_ceddda9d.CfnDataSource.DataSourceConfigurationInputProperty:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_datazone_ceddda9d.CfnDataSource.DataSourceConfigurationInputProperty, jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DataSourceConfigurationBase).__jsii_proxy_class__ = lambda : _DataSourceConfigurationBaseProxy


@jsii.implements(IFormMetadata)
class FormMetadataBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.FormMetadataBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653f241962f59123bb5f01155d6e25b61d2da7c5d6bf48a6e88193d19e243ace)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="formName")
    @abc.abstractmethod
    def form_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="formRevision")
    @abc.abstractmethod
    def form_revision(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _FormMetadataBaseProxy(
    FormMetadataBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="formName")
    def form_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "formName"))

    @builtins.property
    @jsii.member(jsii_name="formRevision")
    def form_revision(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "formRevision"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FormMetadataBase).__jsii_proxy_class__ = lambda : _FormMetadataBaseProxy


@jsii.implements(IGlossary)
class GlossaryBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.GlossaryBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a0138fc421a725e636fb7cda918efc2a8164229bed82b6bc520b3fdd8006a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addGlossaryTerms")
    @abc.abstractmethod
    def add_glossary_terms(
        self,
        terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
    ) -> typing.List["GlossaryTerm"]:
        '''
        :param terms: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="glossaryId")
    @abc.abstractmethod
    def glossary_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    @abc.abstractmethod
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        ...


class _GlossaryBaseProxy(
    GlossaryBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @jsii.member(jsii_name="addGlossaryTerms")
    def add_glossary_terms(
        self,
        terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
    ) -> typing.List["GlossaryTerm"]:
        '''
        :param terms: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d724a56bccbe14280ca9d1c4dc66868bba00415f1544e88afefbfbb51455b00d)
            check_type(argname="argument terms", value=terms, expected_type=type_hints["terms"])
        return typing.cast(typing.List["GlossaryTerm"], jsii.invoke(self, "addGlossaryTerms", [terms]))

    @builtins.property
    @jsii.member(jsii_name="glossaryId")
    def glossary_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "glossaryId"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        return typing.cast("Project", jsii.get(self, "project"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, GlossaryBase).__jsii_proxy_class__ = lambda : _GlossaryBaseProxy


@jsii.implements(IGlossaryTerm)
class GlossaryTermBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.GlossaryTermBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38852639e497edbdd8194e6b2bb2d7c6cb79c43ad6992f02a0c0f20e65450d46)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="glossaryTermId")
    @abc.abstractmethod
    def glossary_term_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _GlossaryTermBaseProxy(
    GlossaryTermBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="glossaryTermId")
    def glossary_term_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "glossaryTermId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, GlossaryTermBase).__jsii_proxy_class__ = lambda : _GlossaryTermBaseProxy


@jsii.data_type(
    jsii_type="cdk-data-zone.GlueOptions",
    jsii_struct_bases=[SourceOptions],
    name_mapping={
        "filter_configurations": "filterConfigurations",
        "data_access_role": "dataAccessRole",
        "auto_import_data_quality_result": "autoImportDataQualityResult",
    },
)
class GlueOptions(SourceOptions):
    def __init__(
        self,
        *,
        filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
        data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        auto_import_data_quality_result: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param filter_configurations: 
        :param data_access_role: 
        :param auto_import_data_quality_result: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542e7401c305eccdb74bbb1d633133befe1a3bcdc4493941a7f98c72859002a4)
            check_type(argname="argument filter_configurations", value=filter_configurations, expected_type=type_hints["filter_configurations"])
            check_type(argname="argument data_access_role", value=data_access_role, expected_type=type_hints["data_access_role"])
            check_type(argname="argument auto_import_data_quality_result", value=auto_import_data_quality_result, expected_type=type_hints["auto_import_data_quality_result"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_configurations": filter_configurations,
        }
        if data_access_role is not None:
            self._values["data_access_role"] = data_access_role
        if auto_import_data_quality_result is not None:
            self._values["auto_import_data_quality_result"] = auto_import_data_quality_result

    @builtins.property
    def filter_configurations(self) -> typing.List[FilterConfiguration]:
        '''
        :stability: experimental
        '''
        result = self._values.get("filter_configurations")
        assert result is not None, "Required property 'filter_configurations' is missing"
        return typing.cast(typing.List[FilterConfiguration], result)

    @builtins.property
    def data_access_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_access_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def auto_import_data_quality_result(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("auto_import_data_quality_result")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-data-zone.IBlueprint")
class IBlueprint(IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="blueprintId")
    def blueprint_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addParameters")
    def add_parameters(
        self,
        region: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param region: -
        :param parameters: -

        :stability: experimental
        '''
        ...


class _IBlueprintProxy(
    jsii.proxy_for(IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IBlueprint"

    @builtins.property
    @jsii.member(jsii_name="blueprintId")
    def blueprint_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "blueprintId"))

    @jsii.member(jsii_name="addParameters")
    def add_parameters(
        self,
        region: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param region: -
        :param parameters: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fac4ec4f68689051a6dd148a5d761cbad1aeef1c58e9a4aa49d387f359ad82)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        return typing.cast(None, jsii.invoke(self, "addParameters", [region, parameters]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBlueprint).__jsii_proxy_class__ = lambda : _IBlueprintProxy


@jsii.interface(jsii_type="cdk-data-zone.IDataSource")
class IDataSource(IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The identifier of the data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> "IEnvironment":
        '''(experimental) The ID of the environment in which the data source exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastRunAssetCount")
    def last_run_asset_count(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''(experimental) The count of the assets created during the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAssetCount
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastRunAt")
    def last_run_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source run was last performed.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastRunStatus")
    def last_run_status(self) -> builtins.str:
        '''(experimental) The status of the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunStatus
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "IProject":
        '''(experimental) The project ID included in the data source run activity.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: ProjectId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the data source.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        ...


class _IDataSourceProxy(
    jsii.proxy_for(IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IDataSource"

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The identifier of the data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> "IEnvironment":
        '''(experimental) The ID of the environment in which the data source exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentId
        '''
        return typing.cast("IEnvironment", jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="lastRunAssetCount")
    def last_run_asset_count(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''(experimental) The count of the assets created during the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAssetCount
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "lastRunAssetCount"))

    @builtins.property
    @jsii.member(jsii_name="lastRunAt")
    def last_run_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source run was last performed.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "lastRunAt"))

    @builtins.property
    @jsii.member(jsii_name="lastRunStatus")
    def last_run_status(self) -> builtins.str:
        '''(experimental) The status of the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "lastRunStatus"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "IProject":
        '''(experimental) The project ID included in the data source run activity.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast("IProject", jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the data source.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDataSource).__jsii_proxy_class__ = lambda : _IDataSourceProxy


@jsii.interface(jsii_type="cdk-data-zone.IDomain")
class IDomain(IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="managedAccount")
    def managed_account(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="portalUrl")
    def portal_url(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addSingleSignOn")
    def add_single_sign_on(
        self,
        *,
        sso_type: SingleSignOnType,
        user_assignment: typing.Optional[AssignmentType] = None,
    ) -> None:
        '''
        :param sso_type: 
        :param user_assignment: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="createProject")
    def create_project(
        self,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        forms: typing.Optional[Forms] = None,
        glossaries: typing.Optional[Glossaries] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> "Project":
        '''
        :param id: -
        :param name: (experimental) The name of a project.
        :param description: (experimental) The description of a project.
        :param forms: 
        :param glossaries: 
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon project.
        :param management_role: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="enableBlueprint")
    def enable_blueprint(
        self,
        blueprint_identifier: builtins.str,
        *,
        enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> "Blueprint":
        '''
        :param blueprint_identifier: -
        :param enabled_regions: 
        :param manage_access_role: 
        :param parameters: 
        :param provisioning_role: 
        :param regional_parameters: 

        :stability: experimental
        '''
        ...


class _IDomainProxy(
    jsii.proxy_for(IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IDomain"

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="managedAccount")
    def managed_account(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedAccount"))

    @builtins.property
    @jsii.member(jsii_name="portalUrl")
    def portal_url(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "portalUrl"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @jsii.member(jsii_name="addSingleSignOn")
    def add_single_sign_on(
        self,
        *,
        sso_type: SingleSignOnType,
        user_assignment: typing.Optional[AssignmentType] = None,
    ) -> None:
        '''
        :param sso_type: 
        :param user_assignment: 

        :stability: experimental
        '''
        single_sign_on = SingleSignOn(
            sso_type=sso_type, user_assignment=user_assignment
        )

        return typing.cast(None, jsii.invoke(self, "addSingleSignOn", [single_sign_on]))

    @jsii.member(jsii_name="createProject")
    def create_project(
        self,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        forms: typing.Optional[Forms] = None,
        glossaries: typing.Optional[Glossaries] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> "Project":
        '''
        :param id: -
        :param name: (experimental) The name of a project.
        :param description: (experimental) The description of a project.
        :param forms: 
        :param glossaries: 
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon project.
        :param management_role: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83bce09fdde411da69d6f8e444344372d6c37585f218deebd3327d0207556cf)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ProjectOptions(
            name=name,
            description=description,
            forms=forms,
            glossaries=glossaries,
            glossary_terms=glossary_terms,
            management_role=management_role,
        )

        return typing.cast("Project", jsii.invoke(self, "createProject", [id, options]))

    @jsii.member(jsii_name="enableBlueprint")
    def enable_blueprint(
        self,
        blueprint_identifier: builtins.str,
        *,
        enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> "Blueprint":
        '''
        :param blueprint_identifier: -
        :param enabled_regions: 
        :param manage_access_role: 
        :param parameters: 
        :param provisioning_role: 
        :param regional_parameters: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee71a9b0868b645e54f0aac90cccca828ac7679dd777894102f9d7106eb4b88)
            check_type(argname="argument blueprint_identifier", value=blueprint_identifier, expected_type=type_hints["blueprint_identifier"])
        options = BlueprintOptions(
            enabled_regions=enabled_regions,
            manage_access_role=manage_access_role,
            parameters=parameters,
            provisioning_role=provisioning_role,
            regional_parameters=regional_parameters,
        )

        return typing.cast("Blueprint", jsii.invoke(self, "enableBlueprint", [blueprint_identifier, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDomain).__jsii_proxy_class__ = lambda : _IDomainProxy


@jsii.interface(jsii_type="cdk-data-zone.IEnvironment")
class IEnvironment(IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''(experimental) The identifier of the AWS account in which an environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: AwsAccountId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''(experimental) The AWS Region in which an environment exists.

        :stability: experimental
        :cloudformationAttribute: AwsAccountRegion
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedBy
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''(experimental) The identifier of the Amazon  domain in which the environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: DomainId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentBlueprintId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentProfile")
    def environment_profile(self) -> "IEnvironmentProfile":
        '''(experimental) The identifier of the environment profile with which the environment was created.

        :stability: experimental
        :cloudformationAttribute: EnvironmentProfileId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "IProject":
        '''(experimental) The identifier of the project in which the environment exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        '''(experimental) The provider of the environment.

        :stability: experimental
        :cloudformationAttribute: Provider
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        ...

    @jsii.member(jsii_name="addDataSource")
    def add_data_source(
        self,
        name: builtins.str,
        *,
        configuration: IDataSourceConfiguration,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        publish_on_import: typing.Optional[builtins.bool] = None,
        recommendation: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[Schedule] = None,
    ) -> "DataSource":
        '''
        :param name: -
        :param configuration: 
        :param description: 
        :param enabled: 
        :param publish_on_import: 
        :param recommendation: 
        :param schedule: 

        :stability: experimental
        '''
        ...


class _IEnvironmentProxy(
    jsii.proxy_for(IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IEnvironment"

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''(experimental) The identifier of the AWS account in which an environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: AwsAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''(experimental) The AWS Region in which an environment exists.

        :stability: experimental
        :cloudformationAttribute: AwsAccountRegion
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountRegion"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedBy
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''(experimental) The identifier of the Amazon  domain in which the environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: DomainId
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentBlueprintId
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentBlueprintId"))

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @builtins.property
    @jsii.member(jsii_name="environmentProfile")
    def environment_profile(self) -> "IEnvironmentProfile":
        '''(experimental) The identifier of the environment profile with which the environment was created.

        :stability: experimental
        :cloudformationAttribute: EnvironmentProfileId
        '''
        return typing.cast("IEnvironmentProfile", jsii.get(self, "environmentProfile"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "IProject":
        '''(experimental) The identifier of the project in which the environment exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast("IProject", jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        '''(experimental) The provider of the environment.

        :stability: experimental
        :cloudformationAttribute: Provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "provider"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @jsii.member(jsii_name="addDataSource")
    def add_data_source(
        self,
        name: builtins.str,
        *,
        configuration: IDataSourceConfiguration,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        publish_on_import: typing.Optional[builtins.bool] = None,
        recommendation: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[Schedule] = None,
    ) -> "DataSource":
        '''
        :param name: -
        :param configuration: 
        :param description: 
        :param enabled: 
        :param publish_on_import: 
        :param recommendation: 
        :param schedule: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af8458257f33f2d7d1c0c007f6c3c8b72d490ada23b8989d1e23b0485d74c8e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = DataSourceOptions(
            configuration=configuration,
            description=description,
            enabled=enabled,
            publish_on_import=publish_on_import,
            recommendation=recommendation,
            schedule=schedule,
        )

        return typing.cast("DataSource", jsii.invoke(self, "addDataSource", [name, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEnvironment).__jsii_proxy_class__ = lambda : _IEnvironmentProxy


@jsii.interface(jsii_type="cdk-data-zone.IEnvironmentProfile")
class IEnvironmentProfile(IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment profile.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentProfileId")
    def environment_profile_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment profile.

        :stability: experimental
        :attribute: Id
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "IProject":
        '''(experimental) The identifier of a project in which an environment profile exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> "Environment":
        '''
        :param id: -
        :param description: (experimental) The description of the environment.
        :param environment_role: (experimental) The ARN of the environment role.
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon environment.
        :param name: (experimental) The name of the Amazon environment.
        :param user_parameters: (experimental) The user parameters of this Amazon environment.

        :stability: experimental
        '''
        ...


class _IEnvironmentProfileProxy(
    jsii.proxy_for(IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IEnvironmentProfile"

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountRegion"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment profile.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentBlueprintId"))

    @builtins.property
    @jsii.member(jsii_name="environmentProfileId")
    def environment_profile_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment profile.

        :stability: experimental
        :attribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentProfileId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "IProject":
        '''(experimental) The identifier of a project in which an environment profile exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast("IProject", jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> "Environment":
        '''
        :param id: -
        :param description: (experimental) The description of the environment.
        :param environment_role: (experimental) The ARN of the environment role.
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon environment.
        :param name: (experimental) The name of the Amazon environment.
        :param user_parameters: (experimental) The user parameters of this Amazon environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcca0809563154f3d4e97ccfb669481540ac60c4bfb9cdc1fc47baae323712b8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = EnvironmentOptions(
            description=description,
            environment_role=environment_role,
            glossary_terms=glossary_terms,
            name=name,
            user_parameters=user_parameters,
        )

        return typing.cast("Environment", jsii.invoke(self, "addEnvironment", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEnvironmentProfile).__jsii_proxy_class__ = lambda : _IEnvironmentProfileProxy


@jsii.interface(jsii_type="cdk-data-zone.IProject")
class IProject(IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the project.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="projectDomainId")
    def project_domain_id(self) -> builtins.str:
        '''(experimental) The identifier of a Amazon  domain where the project exists.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        '''(experimental) The identifier of a project.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addFormMetadata")
    def add_form_metadata(self, forms: Forms) -> None:
        '''
        :param forms: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addGlossaries")
    def add_glossaries(self, glossaries: Glossaries) -> None:
        '''
        :param glossaries: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addGlossary")
    def add_glossary(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "Glossary":
        '''
        :param description: 
        :param name: 
        :param terms: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addGlossaryTerm")
    def add_glossary_term(self, term: builtins.str) -> None:
        '''
        :param term: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addMember")
    def add_member(
        self,
        id: builtins.str,
        *,
        designation: typing.Optional[builtins.str] = None,
        group_identifier: typing.Optional[builtins.str] = None,
        user_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param designation: 
        :param group_identifier: 
        :param user_identifier: 

        :stability: experimental
        '''
        ...


class _IProjectProxy(
    jsii.proxy_for(IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-data-zone.IProject"

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the project.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="projectDomainId")
    def project_domain_id(self) -> builtins.str:
        '''(experimental) The identifier of a Amazon  domain where the project exists.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectDomainId"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        '''(experimental) The identifier of a project.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @jsii.member(jsii_name="addFormMetadata")
    def add_form_metadata(self, forms: Forms) -> None:
        '''
        :param forms: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95382963200337ac8e178328051aa7f1ea7b1073ae2b5a058592fe92965b3984)
            check_type(argname="argument forms", value=forms, expected_type=type_hints["forms"])
        return typing.cast(None, jsii.invoke(self, "addFormMetadata", [forms]))

    @jsii.member(jsii_name="addGlossaries")
    def add_glossaries(self, glossaries: Glossaries) -> None:
        '''
        :param glossaries: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315c6b4f2e95ee7a5e2630172a762f7fb84549707b71f6b6a9a19715c738cbff)
            check_type(argname="argument glossaries", value=glossaries, expected_type=type_hints["glossaries"])
        return typing.cast(None, jsii.invoke(self, "addGlossaries", [glossaries]))

    @jsii.member(jsii_name="addGlossary")
    def add_glossary(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "Glossary":
        '''
        :param description: 
        :param name: 
        :param terms: 

        :stability: experimental
        '''
        options = GlossaryOptions(description=description, name=name, terms=terms)

        return typing.cast("Glossary", jsii.invoke(self, "addGlossary", [options]))

    @jsii.member(jsii_name="addGlossaryTerm")
    def add_glossary_term(self, term: builtins.str) -> None:
        '''
        :param term: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fd79973c1029cde79f05f570b9ff46b1de91f68a7c85719a7e5e8759518193)
            check_type(argname="argument term", value=term, expected_type=type_hints["term"])
        return typing.cast(None, jsii.invoke(self, "addGlossaryTerm", [term]))

    @jsii.member(jsii_name="addMember")
    def add_member(
        self,
        id: builtins.str,
        *,
        designation: typing.Optional[builtins.str] = None,
        group_identifier: typing.Optional[builtins.str] = None,
        user_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param designation: 
        :param group_identifier: 
        :param user_identifier: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54932b2748bbd8e2c08e2eb93bacf1eb74972f8ce656abe0e7b60f3f271e3a77)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = MemberOptions(
            designation=designation,
            group_identifier=group_identifier,
            user_identifier=user_identifier,
        )

        return typing.cast(None, jsii.invoke(self, "addMember", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProject).__jsii_proxy_class__ = lambda : _IProjectProxy


@jsii.implements(IProject)
class ProjectBase(
    ResourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.ProjectBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4436757b2f53ad06613c0be552854da3b637e053b8f0f354baa3ae5c98ace620)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addFormMetadata")
    @abc.abstractmethod
    def add_form_metadata(self, forms: Forms) -> None:
        '''
        :param forms: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addGlossaries")
    @abc.abstractmethod
    def add_glossaries(self, glossaries: Glossaries) -> None:
        '''
        :param glossaries: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addGlossary")
    @abc.abstractmethod
    def add_glossary(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "Glossary":
        '''
        :param description: 
        :param name: 
        :param terms: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addGlossaryTerm")
    @abc.abstractmethod
    def add_glossary_term(self, term: builtins.str) -> None:
        '''
        :param term: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addMember")
    @abc.abstractmethod
    def add_member(
        self,
        id: builtins.str,
        *,
        designation: typing.Optional[builtins.str] = None,
        group_identifier: typing.Optional[builtins.str] = None,
        user_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param designation: 
        :param group_identifier: 
        :param user_identifier: 

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    @abc.abstractmethod
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the project.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="projectDomainId")
    @abc.abstractmethod
    def project_domain_id(self) -> builtins.str:
        '''(experimental) The identifier of a Amazon  domain where the project exists.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="projectId")
    @abc.abstractmethod
    def project_id(self) -> builtins.str:
        '''(experimental) The identifier of a project.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ProjectBaseProxy(
    ProjectBase,
    jsii.proxy_for(ResourceBase), # type: ignore[misc]
):
    @jsii.member(jsii_name="addFormMetadata")
    def add_form_metadata(self, forms: Forms) -> None:
        '''
        :param forms: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b41948bfafe6f368a85395c3eded5f10deea30fb5ced358cae2167757c537d5)
            check_type(argname="argument forms", value=forms, expected_type=type_hints["forms"])
        return typing.cast(None, jsii.invoke(self, "addFormMetadata", [forms]))

    @jsii.member(jsii_name="addGlossaries")
    def add_glossaries(self, glossaries: Glossaries) -> None:
        '''
        :param glossaries: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27742b00d372a9c06c2f87b7a8b40d5abc47e7998b4fd891435a822ebe1264a7)
            check_type(argname="argument glossaries", value=glossaries, expected_type=type_hints["glossaries"])
        return typing.cast(None, jsii.invoke(self, "addGlossaries", [glossaries]))

    @jsii.member(jsii_name="addGlossary")
    def add_glossary(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "Glossary":
        '''
        :param description: 
        :param name: 
        :param terms: 

        :stability: experimental
        '''
        options = GlossaryOptions(description=description, name=name, terms=terms)

        return typing.cast("Glossary", jsii.invoke(self, "addGlossary", [options]))

    @jsii.member(jsii_name="addGlossaryTerm")
    def add_glossary_term(self, term: builtins.str) -> None:
        '''
        :param term: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9995ec8b5f0b86f9ab0efc48d38efd5a011188dd21f03021e1015605025017c)
            check_type(argname="argument term", value=term, expected_type=type_hints["term"])
        return typing.cast(None, jsii.invoke(self, "addGlossaryTerm", [term]))

    @jsii.member(jsii_name="addMember")
    def add_member(
        self,
        id: builtins.str,
        *,
        designation: typing.Optional[builtins.str] = None,
        group_identifier: typing.Optional[builtins.str] = None,
        user_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param designation: 
        :param group_identifier: 
        :param user_identifier: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141d478e9d364f0a2559b5326365e433d92ca523d789881244b408401318fb4f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = MemberOptions(
            designation=designation,
            group_identifier=group_identifier,
            user_identifier=user_identifier,
        )

        return typing.cast(None, jsii.invoke(self, "addMember", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the project.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="projectDomainId")
    def project_domain_id(self) -> builtins.str:
        '''(experimental) The identifier of a Amazon  domain where the project exists.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectDomainId"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        '''(experimental) The identifier of a project.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ProjectBase).__jsii_proxy_class__ = lambda : _ProjectBaseProxy


@jsii.data_type(
    jsii_type="cdk-data-zone.RedshiftOptions",
    jsii_struct_bases=[SourceOptions],
    name_mapping={
        "filter_configurations": "filterConfigurations",
        "data_access_role": "dataAccessRole",
        "credentials": "credentials",
        "name": "name",
        "redshift_type": "redshiftType",
    },
)
class RedshiftOptions(SourceOptions):
    def __init__(
        self,
        *,
        filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
        data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        credentials: _aws_cdk_aws_secretsmanager_ceddda9d.Secret,
        name: builtins.str,
        redshift_type: builtins.str,
    ) -> None:
        '''
        :param filter_configurations: 
        :param data_access_role: 
        :param credentials: 
        :param name: 
        :param redshift_type: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7716389965728144a006197d03926ab920aaa81e23ade4c0b7f8315c03eb55)
            check_type(argname="argument filter_configurations", value=filter_configurations, expected_type=type_hints["filter_configurations"])
            check_type(argname="argument data_access_role", value=data_access_role, expected_type=type_hints["data_access_role"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument redshift_type", value=redshift_type, expected_type=type_hints["redshift_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_configurations": filter_configurations,
            "credentials": credentials,
            "name": name,
            "redshift_type": redshift_type,
        }
        if data_access_role is not None:
            self._values["data_access_role"] = data_access_role

    @builtins.property
    def filter_configurations(self) -> typing.List[FilterConfiguration]:
        '''
        :stability: experimental
        '''
        result = self._values.get("filter_configurations")
        assert result is not None, "Required property 'filter_configurations' is missing"
        return typing.cast(typing.List[FilterConfiguration], result)

    @builtins.property
    def data_access_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_access_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def credentials(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''
        :stability: experimental
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redshift_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("redshift_type")
        assert result is not None, "Required property 'redshift_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IBlueprint)
class BlueprintBase(
    ResourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.BlueprintBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f683691be47fbe4d67b0c75bf2c725fe20eba7da5241acd66584e7176ca514c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addParameters")
    @abc.abstractmethod
    def add_parameters(
        self,
        region: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param region: -
        :param parameters: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blueprintId")
    @abc.abstractmethod
    def blueprint_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _BlueprintBaseProxy(
    BlueprintBase,
    jsii.proxy_for(ResourceBase), # type: ignore[misc]
):
    @jsii.member(jsii_name="addParameters")
    def add_parameters(
        self,
        region: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param region: -
        :param parameters: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ef75223420896e4239b46f9054d3eb7ca68855356bbf07a8bc2ccdfde3e80b)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        return typing.cast(None, jsii.invoke(self, "addParameters", [region, parameters]))

    @builtins.property
    @jsii.member(jsii_name="blueprintId")
    def blueprint_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "blueprintId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BlueprintBase).__jsii_proxy_class__ = lambda : _BlueprintBaseProxy


@jsii.implements(IDataSource)
class DataSourceBase(
    ResourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.DataSourceBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961dbb93204583b2725c8fba135eb02e15928e1c32407bd5a6dd0cdd83f84ed3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    @abc.abstractmethod
    def data_source_id(self) -> builtins.str:
        '''(experimental) The identifier of the data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environment")
    @abc.abstractmethod
    def environment(self) -> IEnvironment:
        '''(experimental) The ID of the environment in which the data source exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastRunAssetCount")
    @abc.abstractmethod
    def last_run_asset_count(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''(experimental) The count of the assets created during the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAssetCount
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastRunAt")
    @abc.abstractmethod
    def last_run_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source run was last performed.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lastRunStatus")
    @abc.abstractmethod
    def last_run_status(self) -> builtins.str:
        '''(experimental) The status of the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunStatus
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    @abc.abstractmethod
    def project(self) -> IProject:
        '''(experimental) The project ID included in the data source run activity.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: ProjectId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="status")
    @abc.abstractmethod
    def status(self) -> builtins.str:
        '''(experimental) The status of the data source.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        ...


class _DataSourceBaseProxy(
    DataSourceBase,
    jsii.proxy_for(ResourceBase), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The identifier of the data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> IEnvironment:
        '''(experimental) The ID of the environment in which the data source exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentId
        '''
        return typing.cast(IEnvironment, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="lastRunAssetCount")
    def last_run_asset_count(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''(experimental) The count of the assets created during the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAssetCount
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "lastRunAssetCount"))

    @builtins.property
    @jsii.member(jsii_name="lastRunAt")
    def last_run_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source run was last performed.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "lastRunAt"))

    @builtins.property
    @jsii.member(jsii_name="lastRunStatus")
    def last_run_status(self) -> builtins.str:
        '''(experimental) The status of the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "lastRunStatus"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> IProject:
        '''(experimental) The project ID included in the data source run activity.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast(IProject, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the data source.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DataSourceBase).__jsii_proxy_class__ = lambda : _DataSourceBaseProxy


@jsii.implements(IDomain)
class DomainBase(
    ResourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.DomainBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28b2ea92bdf2ccea5a48be7a0247229d4388c6ac679464ec0b956895277f414)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSingleSignOn")
    @abc.abstractmethod
    def add_single_sign_on(
        self,
        *,
        sso_type: SingleSignOnType,
        user_assignment: typing.Optional[AssignmentType] = None,
    ) -> None:
        '''
        :param sso_type: 
        :param user_assignment: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="createProject")
    def create_project(
        self,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        forms: typing.Optional[Forms] = None,
        glossaries: typing.Optional[Glossaries] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> "Project":
        '''
        :param id: -
        :param name: (experimental) The name of a project.
        :param description: (experimental) The description of a project.
        :param forms: 
        :param glossaries: 
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon project.
        :param management_role: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5748c751cd6fa1e7c9a20e02cdd0d6970d7a0e29027ecb2538203719dda9981d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ProjectOptions(
            name=name,
            description=description,
            forms=forms,
            glossaries=glossaries,
            glossary_terms=glossary_terms,
            management_role=management_role,
        )

        return typing.cast("Project", jsii.invoke(self, "createProject", [id, options]))

    @jsii.member(jsii_name="enableBlueprint")
    def enable_blueprint(
        self,
        blueprint_identifier: builtins.str,
        *,
        enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> "Blueprint":
        '''
        :param blueprint_identifier: -
        :param enabled_regions: 
        :param manage_access_role: 
        :param parameters: 
        :param provisioning_role: 
        :param regional_parameters: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8394b004e672ea7b229a646a20862362133d6305db806a89376b8281f87d5e19)
            check_type(argname="argument blueprint_identifier", value=blueprint_identifier, expected_type=type_hints["blueprint_identifier"])
        options = BlueprintOptions(
            enabled_regions=enabled_regions,
            manage_access_role=manage_access_role,
            parameters=parameters,
            provisioning_role=provisioning_role,
            regional_parameters=regional_parameters,
        )

        return typing.cast("Blueprint", jsii.invoke(self, "enableBlueprint", [blueprint_identifier, options]))

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    @abc.abstractmethod
    def domain_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainId")
    @abc.abstractmethod
    def domain_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="managedAccount")
    @abc.abstractmethod
    def managed_account(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="portalUrl")
    @abc.abstractmethod
    def portal_url(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="status")
    @abc.abstractmethod
    def status(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _DomainBaseProxy(
    DomainBase,
    jsii.proxy_for(ResourceBase), # type: ignore[misc]
):
    @jsii.member(jsii_name="addSingleSignOn")
    def add_single_sign_on(
        self,
        *,
        sso_type: SingleSignOnType,
        user_assignment: typing.Optional[AssignmentType] = None,
    ) -> None:
        '''
        :param sso_type: 
        :param user_assignment: 

        :stability: experimental
        '''
        single_sign_on = SingleSignOn(
            sso_type=sso_type, user_assignment=user_assignment
        )

        return typing.cast(None, jsii.invoke(self, "addSingleSignOn", [single_sign_on]))

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="managedAccount")
    def managed_account(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedAccount"))

    @builtins.property
    @jsii.member(jsii_name="portalUrl")
    def portal_url(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "portalUrl"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DomainBase).__jsii_proxy_class__ = lambda : _DomainBaseProxy


@jsii.implements(IEnvironment)
class EnvironmentBase(
    ResourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.EnvironmentBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a14ceb05653b7f0c6e524c53d43e2159671f60d6224affcca3fe64d2178f3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDataSource")
    def add_data_source(
        self,
        name: builtins.str,
        *,
        configuration: IDataSourceConfiguration,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        publish_on_import: typing.Optional[builtins.bool] = None,
        recommendation: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[Schedule] = None,
    ) -> "DataSource":
        '''
        :param name: -
        :param configuration: 
        :param description: 
        :param enabled: 
        :param publish_on_import: 
        :param recommendation: 
        :param schedule: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1127e6e6485a517a01ace3e23937be9a94ba111e4b03efa490c736c0cfb907a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = DataSourceOptions(
            configuration=configuration,
            description=description,
            enabled=enabled,
            publish_on_import=publish_on_import,
            recommendation=recommendation,
            schedule=schedule,
        )

        return typing.cast("DataSource", jsii.invoke(self, "addDataSource", [name, options]))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    @abc.abstractmethod
    def aws_account_id(self) -> builtins.str:
        '''(experimental) The identifier of the AWS account in which an environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: AwsAccountId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    @abc.abstractmethod
    def aws_account_region(self) -> builtins.str:
        '''(experimental) The AWS Region in which an environment exists.

        :stability: experimental
        :cloudformationAttribute: AwsAccountRegion
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    @abc.abstractmethod
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedBy
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainId")
    @abc.abstractmethod
    def domain_id(self) -> builtins.str:
        '''(experimental) The identifier of the Amazon  domain in which the environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: DomainId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    @abc.abstractmethod
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentBlueprintId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    @abc.abstractmethod
    def environment_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentProfile")
    @abc.abstractmethod
    def environment_profile(self) -> IEnvironmentProfile:
        '''(experimental) The identifier of the environment profile with which the environment was created.

        :stability: experimental
        :cloudformationAttribute: EnvironmentProfileId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    @abc.abstractmethod
    def project(self) -> IProject:
        '''(experimental) The identifier of the project in which the environment exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="provider")
    @abc.abstractmethod
    def provider(self) -> builtins.str:
        '''(experimental) The provider of the environment.

        :stability: experimental
        :cloudformationAttribute: Provider
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="status")
    @abc.abstractmethod
    def status(self) -> builtins.str:
        '''(experimental) The status of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        ...


class _EnvironmentBaseProxy(
    EnvironmentBase,
    jsii.proxy_for(ResourceBase), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''(experimental) The identifier of the AWS account in which an environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: AwsAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''(experimental) The AWS Region in which an environment exists.

        :stability: experimental
        :cloudformationAttribute: AwsAccountRegion
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountRegion"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedBy
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''(experimental) The identifier of the Amazon  domain in which the environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: DomainId
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentBlueprintId
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentBlueprintId"))

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @builtins.property
    @jsii.member(jsii_name="environmentProfile")
    def environment_profile(self) -> IEnvironmentProfile:
        '''(experimental) The identifier of the environment profile with which the environment was created.

        :stability: experimental
        :cloudformationAttribute: EnvironmentProfileId
        '''
        return typing.cast(IEnvironmentProfile, jsii.get(self, "environmentProfile"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> IProject:
        '''(experimental) The identifier of the project in which the environment exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast(IProject, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        '''(experimental) The provider of the environment.

        :stability: experimental
        :cloudformationAttribute: Provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "provider"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, EnvironmentBase).__jsii_proxy_class__ = lambda : _EnvironmentBaseProxy


@jsii.implements(IEnvironmentProfile)
class EnvironmentProfileBase(
    ResourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-data-zone.EnvironmentProfileBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e99987a20aa95448cbed7a41c4585fd6755e0ada603840834983faeec47e0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> "Environment":
        '''
        :param id: -
        :param description: (experimental) The description of the environment.
        :param environment_role: (experimental) The ARN of the environment role.
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon environment.
        :param name: (experimental) The name of the Amazon environment.
        :param user_parameters: (experimental) The user parameters of this Amazon environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e579ad5f6993311b35c9f189e9d7d50108b85f437c654e6ed108e4093a0711dc)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = EnvironmentOptions(
            description=description,
            environment_role=environment_role,
            glossary_terms=glossary_terms,
            name=name,
            user_parameters=user_parameters,
        )

        return typing.cast("Environment", jsii.invoke(self, "addEnvironment", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    @abc.abstractmethod
    def aws_account_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    @abc.abstractmethod
    def aws_account_region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    @abc.abstractmethod
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment profile.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    @abc.abstractmethod
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environmentProfileId")
    @abc.abstractmethod
    def environment_profile_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment profile.

        :stability: experimental
        :attribute: Id
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    @abc.abstractmethod
    def project(self) -> IProject:
        '''(experimental) The identifier of a project in which an environment profile exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    @abc.abstractmethod
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...


class _EnvironmentProfileBaseProxy(
    EnvironmentProfileBase,
    jsii.proxy_for(ResourceBase), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountRegion"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment profile.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentBlueprintId"))

    @builtins.property
    @jsii.member(jsii_name="environmentProfileId")
    def environment_profile_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment profile.

        :stability: experimental
        :attribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentProfileId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> IProject:
        '''(experimental) The identifier of a project in which an environment profile exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast(IProject, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, EnvironmentProfileBase).__jsii_proxy_class__ = lambda : _EnvironmentProfileBaseProxy


class FormMetadata(
    FormMetadataBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.FormMetadata",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        project: "Project",
        description: typing.Optional[builtins.str] = None,
        smithy_model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        :param project: 
        :param description: 
        :param smithy_model: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfdced267f13185efffd6da1cf521d97be1b1111362027d219fb326a0b68a5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FormMetadataProps(
            name=name,
            project=project,
            description=description,
            smithy_model=smithy_model,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="formName")
    def form_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "formName"))

    @builtins.property
    @jsii.member(jsii_name="formRevision")
    def form_revision(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "formRevision"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        return typing.cast("Project", jsii.get(self, "project"))


class Glossary(
    GlossaryBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.Glossary",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        name: builtins.str,
        project: "Project",
        terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: 
        :param name: 
        :param project: 
        :param terms: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a0fd13fdc30aa8ef98dd5fd7146e60762ad753aa7c996f698e004c90b0fd73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GlossaryProps(
            description=description, name=name, project=project, terms=terms
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addGlossaryTerms")
    def add_glossary_terms(
        self,
        terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
    ) -> typing.List["GlossaryTerm"]:
        '''
        :param terms: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25528749924e697cef618675656ab5a432bf67f8b6816ad45e4704d35f6967d2)
            check_type(argname="argument terms", value=terms, expected_type=type_hints["terms"])
        return typing.cast(typing.List["GlossaryTerm"], jsii.invoke(self, "addGlossaryTerms", [terms]))

    @builtins.property
    @jsii.member(jsii_name="glossaryId")
    def glossary_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "glossaryId"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        return typing.cast("Project", jsii.get(self, "project"))


class GlossaryTerm(
    GlossaryTermBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.GlossaryTerm",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        glossary: IGlossary,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        long_description: typing.Optional[builtins.str] = None,
        short_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param glossary: 
        :param name: 
        :param description: 
        :param enabled: 
        :param long_description: 
        :param short_description: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738f8c6d797404d777894649973ad263f6c6d30c7e1984d0906d672cd39afc74)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GlossaryTermProps(
            glossary=glossary,
            name=name,
            description=description,
            enabled=enabled,
            long_description=long_description,
            short_description=short_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="glossary")
    def glossary(self) -> IGlossary:
        '''
        :stability: experimental
        '''
        return typing.cast(IGlossary, jsii.get(self, "glossary"))

    @builtins.property
    @jsii.member(jsii_name="glossaryTermId")
    def glossary_term_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "glossaryTermId"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        return typing.cast("Project", jsii.get(self, "project"))


class Project(ProjectBase, metaclass=jsii.JSIIMeta, jsii_type="cdk-data-zone.Project"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain: IDomain,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        forms: typing.Optional[Forms] = None,
        glossaries: typing.Optional[Glossaries] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain: (experimental) The identifier of a Amazon domain where the project exists.
        :param name: (experimental) The name of a project.
        :param description: (experimental) The description of a project.
        :param forms: 
        :param glossaries: 
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon project.
        :param management_role: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d50975878d385c12d4b5f684bd144183ee7ea64cff217e4acd9972fd4ac8d22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ProjectProps(
            domain=domain,
            name=name,
            description=description,
            forms=forms,
            glossaries=glossaries,
            glossary_terms=glossary_terms,
            management_role=management_role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addFormMetadata")
    def add_form_metadata(self, forms: Forms) -> None:
        '''
        :param forms: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1127b376251ad20c3d469f0076164366fd82f462ffffbee288657e4fb3fdfd7a)
            check_type(argname="argument forms", value=forms, expected_type=type_hints["forms"])
        return typing.cast(None, jsii.invoke(self, "addFormMetadata", [forms]))

    @jsii.member(jsii_name="addGlossaries")
    def add_glossaries(self, glossaries: Glossaries) -> None:
        '''
        :param glossaries: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34025c01dcffebf549132cedba6098d5b1a8a2cb4593dab6164cab8eff8d0c36)
            check_type(argname="argument glossaries", value=glossaries, expected_type=type_hints["glossaries"])
        return typing.cast(None, jsii.invoke(self, "addGlossaries", [glossaries]))

    @jsii.member(jsii_name="addGlossary")
    def add_glossary(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> Glossary:
        '''
        :param description: 
        :param name: 
        :param terms: 

        :stability: experimental
        '''
        options = GlossaryOptions(description=description, name=name, terms=terms)

        return typing.cast(Glossary, jsii.invoke(self, "addGlossary", [options]))

    @jsii.member(jsii_name="addGlossaryTerm")
    def add_glossary_term(self, term: builtins.str) -> None:
        '''
        :param term: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7f9ca2e0a2aaea268030e26ec68bc4d6ee8abb7d4a1dfdd7dba0d055049294)
            check_type(argname="argument term", value=term, expected_type=type_hints["term"])
        return typing.cast(None, jsii.invoke(self, "addGlossaryTerm", [term]))

    @jsii.member(jsii_name="addMember")
    def add_member(
        self,
        id: builtins.str,
        *,
        designation: typing.Optional[builtins.str] = None,
        group_identifier: typing.Optional[builtins.str] = None,
        user_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param designation: 
        :param group_identifier: 
        :param user_identifier: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0106f68484cf7a3e4ab6c2d567a7ef8ce31298e4f52dc637d2c40692da0a6326)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = MemberOptions(
            designation=designation,
            group_identifier=group_identifier,
            user_identifier=user_identifier,
        )

        return typing.cast(None, jsii.invoke(self, "addMember", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the project.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="managementRole")
    def management_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "managementRole"))

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> _aws_cdk_aws_datazone_ceddda9d.CfnProjectMembership:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_datazone_ceddda9d.CfnProjectMembership, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="projectDomainId")
    def project_domain_id(self) -> builtins.str:
        '''(experimental) The identifier of a Amazon  domain where the project exists.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectDomainId"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        '''(experimental) The identifier of a project.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the project was last updated.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))


class Blueprint(
    BlueprintBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.Blueprint",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain: IDomain,
        environment_blueprint_identifier: builtins.str,
        enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain: 
        :param environment_blueprint_identifier: 
        :param enabled_regions: 
        :param manage_access_role: 
        :param parameters: 
        :param provisioning_role: 
        :param regional_parameters: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d47d26ccb5bc6045752c8e7cc56c797389759bc97103c474b31b24b9313fa19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BlueprintProps(
            domain=domain,
            environment_blueprint_identifier=environment_blueprint_identifier,
            enabled_regions=enabled_regions,
            manage_access_role=manage_access_role,
            parameters=parameters,
            provisioning_role=provisioning_role,
            regional_parameters=regional_parameters,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addParameters")
    def add_parameters(
        self,
        region: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param region: -
        :param parameters: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7219a0bd26c826826c36a296c69d2a8ebbdc5e2cc3ee29397e89668f20910114)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        return typing.cast(None, jsii.invoke(self, "addParameters", [region, parameters]))

    @builtins.property
    @jsii.member(jsii_name="blueprintId")
    def blueprint_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "blueprintId"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="enabledRegions")
    def enabled_regions(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enabledRegions"))

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintIdentifier")
    def environment_blueprint_identifier(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentBlueprintIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="manageAccessRole")
    def manage_access_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "manageAccessRole"))

    @builtins.property
    @jsii.member(jsii_name="provisioningRole")
    def provisioning_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "provisioningRole"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was updated.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))


class DataSource(
    DataSourceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.DataSource",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        configuration: IDataSourceConfiguration,
        environment: IEnvironment,
        name: builtins.str,
        project: IProject,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        publish_on_import: typing.Optional[builtins.bool] = None,
        recommendation: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[Schedule] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param configuration: 
        :param environment: 
        :param name: 
        :param project: 
        :param description: 
        :param enabled: 
        :param publish_on_import: 
        :param recommendation: 
        :param schedule: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e23e9d2f1db96f6cdd09ab74fd016a0703795d6ee939b83e9b46b01716da88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataSourceProps(
            configuration=configuration,
            environment=environment,
            name=name,
            project=project,
            description=description,
            enabled=enabled,
            publish_on_import=publish_on_import,
            recommendation=recommendation,
            schedule=schedule,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The identifier of the data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> IEnvironment:
        '''(experimental) The ID of the environment in which the data source exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentId
        '''
        return typing.cast(IEnvironment, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

    @builtins.property
    @jsii.member(jsii_name="lastRunAssetCount")
    def last_run_asset_count(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''(experimental) The count of the assets created during the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAssetCount
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "lastRunAssetCount"))

    @builtins.property
    @jsii.member(jsii_name="lastRunAt")
    def last_run_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source run was last performed.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "lastRunAt"))

    @builtins.property
    @jsii.member(jsii_name="lastRunStatus")
    def last_run_status(self) -> builtins.str:
        '''(experimental) The status of the last data source run.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: LastRunStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "lastRunStatus"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> IProject:
        '''(experimental) The project ID included in the data source run activity.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast(IProject, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="publishOnImport")
    def publish_on_import(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "publishOnImport"))

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "recommendation"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the data source.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was updated.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[Schedule]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[Schedule], jsii.get(self, "schedule"))


class Domain(DomainBase, metaclass=jsii.JSIIMeta, jsii_type="cdk-data-zone.Domain"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        domain_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        single_sign_on: typing.Optional[typing.Union[SingleSignOn, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: (experimental) The name of the Amazon DataZone domain.
        :param description: (experimental) The description of the Amazon DataZone domain.
        :param domain_execution_role: (experimental) The domain execution role that is created when an Amazon DataZone domain is created. The domain execution role is created in the AWS account that houses the Amazon DataZone domain.
        :param encryption_key: (experimental) The identifier of the AWS Key Management Service (KMS) key that is used to encrypt the Amazon DataZone domain, metadata, and reporting data.
        :param single_sign_on: (experimental) The single sign-on details in Amazon DataZone.
        :param tags: (experimental) The tags specified for the Amazon DataZone domain.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01183080c547ab299e2a2e80c0b03778603522fbb8c9d3a0470ee2ae9846a1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainProps(
            name=name,
            description=description,
            domain_execution_role=domain_execution_role,
            encryption_key=encryption_key,
            single_sign_on=single_sign_on,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSingleSignOn")
    def add_single_sign_on(
        self,
        *,
        sso_type: SingleSignOnType,
        user_assignment: typing.Optional[AssignmentType] = None,
    ) -> None:
        '''
        :param sso_type: 
        :param user_assignment: 

        :stability: experimental
        '''
        single_sign_on = SingleSignOn(
            sso_type=sso_type, user_assignment=user_assignment
        )

        return typing.cast(None, jsii.invoke(self, "addSingleSignOn", [single_sign_on]))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was created.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainExecutionRole")
    def domain_execution_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "domainExecutionRole"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="managedAccount")
    def managed_account(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedAccount"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="portalUrl")
    def portal_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "portalUrl"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the data source was updated.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))


class Environment(
    EnvironmentBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.Environment",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        environment_profile: IEnvironmentProfile,
        name: builtins.str,
        project: IProject,
        description: typing.Optional[builtins.str] = None,
        environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param environment_profile: (experimental) The identifier of the environment profile that is used to create this Amazon environment.
        :param name: (experimental) The name of the Amazon environment.
        :param project: (experimental) The identifier of the Amazon project in which this environment is created.
        :param description: (experimental) The description of the environment.
        :param environment_role: (experimental) The ARN of the environment role.
        :param glossary_terms: (experimental) The glossary terms that can be used in this Amazon environment.
        :param user_parameters: (experimental) The user parameters of this Amazon environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29910e2c047e6cb7d822f4a3b82c1a0ea70d09be5b837b196e291518c0f991a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EnvironmentProps(
            environment_profile=environment_profile,
            name=name,
            project=project,
            description=description,
            environment_role=environment_role,
            glossary_terms=glossary_terms,
            user_parameters=user_parameters,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''(experimental) The identifier of the AWS account in which an environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: AwsAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''(experimental) The AWS Region in which an environment exists.

        :stability: experimental
        :cloudformationAttribute: AwsAccountRegion
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountRegion"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the environment was created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: CreatedBy
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''(experimental) The identifier of the Amazon  domain in which the environment exists.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: DomainId
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: EnvironmentBlueprintId
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentBlueprintId"))

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @builtins.property
    @jsii.member(jsii_name="environmentProfile")
    def environment_profile(self) -> IEnvironmentProfile:
        '''(experimental) The identifier of the environment profile with which the environment was created.

        :stability: experimental
        :cloudformationAttribute: EnvironmentProfileId
        '''
        return typing.cast(IEnvironmentProfile, jsii.get(self, "environmentProfile"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> IProject:
        '''(experimental) The identifier of the project in which the environment exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast(IProject, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        '''(experimental) The provider of the environment.

        :stability: experimental
        :cloudformationAttribute: Provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "provider"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the environment.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the environment was updated.

        :stability: experimental
        :attribute: true
        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))


class EnvironmentProfile(
    EnvironmentProfileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-data-zone.EnvironmentProfile",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        blueprint: IBlueprint,
        name: builtins.str,
        project: IProject,
        aws_account_id: typing.Optional[builtins.str] = None,
        aws_account_region: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironmentProfile.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param blueprint: (experimental) The identifier of a blueprint with which an environment profile is created.
        :param name: (experimental) The name of the environment profile.
        :param project: (experimental) The identifier of a project in which an environment profile exists.
        :param aws_account_id: (experimental) The identifier of an AWS account in which an environment profile exists. Default: the Domain account
        :param aws_account_region: (experimental) The AWS Region in which an environment profile exists. Default: the Domain region
        :param description: (experimental) The description of the environment profile.
        :param user_parameters: (experimental) The user parameters of this Amazon environment profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33686a4c9543d6c075de60ff94c614916313accc94544e817284164ade832c7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EnvironmentProfileProps(
            blueprint=blueprint,
            name=name,
            project=project,
            aws_account_id=aws_account_id,
            aws_account_region=aws_account_region,
            description=description,
            user_parameters=user_parameters,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountRegion")
    def aws_account_region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountRegion"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) The timestamp of when an environment profile was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        '''(experimental) The Amazon  user who created the environment profile.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="environmentBlueprintId")
    def environment_blueprint_id(self) -> builtins.str:
        '''(experimental) The identifier of a blueprint with which an environment profile is created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentBlueprintId"))

    @builtins.property
    @jsii.member(jsii_name="environmentProfileId")
    def environment_profile_id(self) -> builtins.str:
        '''(experimental) The identifier of the environment profile.

        :stability: experimental
        :attribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentProfileId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> IProject:
        '''(experimental) The identifier of a project in which an environment profile exists.

        :stability: experimental
        :cloudformationAttribute: ProjectId
        '''
        return typing.cast(IProject, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) The timestamp of when the environment profile was updated.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))


__all__ = [
    "AssignmentType",
    "Blueprint",
    "BlueprintBase",
    "BlueprintEnvironmentIdentifiers",
    "BlueprintOptions",
    "BlueprintProps",
    "CronOptions",
    "DataSource",
    "DataSourceBase",
    "DataSourceConfigurationBase",
    "DataSourceOptions",
    "DataSourceProps",
    "Domain",
    "DomainBase",
    "DomainProps",
    "Environment",
    "EnvironmentBase",
    "EnvironmentOptions",
    "EnvironmentProfile",
    "EnvironmentProfileBase",
    "EnvironmentProfileProps",
    "EnvironmentProps",
    "FilterConfiguration",
    "FilterExpression",
    "FormMetadata",
    "FormMetadataBase",
    "FormMetadataOptions",
    "FormMetadataProps",
    "Forms",
    "Glossaries",
    "Glossary",
    "GlossaryBase",
    "GlossaryOptions",
    "GlossaryProps",
    "GlossaryTerm",
    "GlossaryTermBase",
    "GlossaryTermOptions",
    "GlossaryTermProps",
    "GlueOptions",
    "IBlueprint",
    "IDataSource",
    "IDataSourceConfiguration",
    "IDomain",
    "IEnvironment",
    "IEnvironmentProfile",
    "IFormMetadata",
    "IGlossary",
    "IGlossaryTerm",
    "IProject",
    "IResource",
    "MemberOptions",
    "Project",
    "ProjectBase",
    "ProjectOptions",
    "ProjectProps",
    "RedshiftOptions",
    "ResourceBase",
    "Schedule",
    "SingleSignOn",
    "SingleSignOnType",
    "SourceOptions",
]

publication.publish()

def _typecheckingstub__9174e9e48b11fc149d0542cb6d797f68f53c56947552a33abfbb2c02f96fc524(
    *,
    enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5d519c2328168c0fc7d2f83cdd29d93512a17dd1179c3659c4156010685e52(
    *,
    domain: IDomain,
    environment_blueprint_identifier: builtins.str,
    enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947a0afbab5f8fb394387ef22cfb3a49ed5252de97be2b9b1a354db6a1f009ac(
    *,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    month: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
    week_day: typing.Optional[builtins.str] = None,
    year: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d31fb03f6e7a17261639cb6cecfc9f6030d51ba05d5e1f621e18c52e272f49(
    *,
    configuration: IDataSourceConfiguration,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    publish_on_import: typing.Optional[builtins.bool] = None,
    recommendation: typing.Optional[builtins.bool] = None,
    schedule: typing.Optional[Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c421054e1a8ec68e5fbd291de58b7620712135aa80aa4aac00ed7ed9c3a9b8(
    *,
    configuration: IDataSourceConfiguration,
    environment: IEnvironment,
    name: builtins.str,
    project: IProject,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    publish_on_import: typing.Optional[builtins.bool] = None,
    recommendation: typing.Optional[builtins.bool] = None,
    schedule: typing.Optional[Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be61ee14bceb92d33c880ff02266f1d05a6cdbb2ac48816a7e2a344cd6c3036f(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    domain_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    single_sign_on: typing.Optional[typing.Union[SingleSignOn, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664794b57fc9315d65327a443c89737ee5a48877ce6cc76518087a5e14c113db(
    *,
    description: typing.Optional[builtins.str] = None,
    environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce7a8b5af595307cf5e5a57ffffe8cb4ea40412a444f9b32567726d9ee9416e(
    *,
    blueprint: IBlueprint,
    name: builtins.str,
    project: IProject,
    aws_account_id: typing.Optional[builtins.str] = None,
    aws_account_region: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironmentProfile.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310ebc674182b1a77a8be6c07f83aa9b03eda25f34236464136dad18d5c49b5c(
    *,
    environment_profile: IEnvironmentProfile,
    name: builtins.str,
    project: IProject,
    description: typing.Optional[builtins.str] = None,
    environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0986bc3d0b93775c7380054ed7eef1eb47b04253092559571beeb2c689f80fb(
    *,
    database_name: builtins.str,
    filter_expressions: typing.Optional[typing.Sequence[typing.Union[FilterExpression, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d25925af03022c6278dec9408a538c2b630c8718cfce52cef0fb0bfbb113c7(
    *,
    expression: builtins.str,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a819549416a173f3d9a2ac9241fc5a11ed9c9de2155fea28d75e9bd61ecf4262(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    smithy_model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7a06fb4f8ed49c7a486693f21a93d98bd83dc206d4a93849d6ef79e7bf96e1(
    *,
    name: builtins.str,
    project: Project,
    description: typing.Optional[builtins.str] = None,
    smithy_model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4db4c02c2fb0dc84bddc127bf74d0f2c9bcd78fb3bce93af85b3ef162071ab5(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63acf890d658dc5eded567a6fff59c57245fe73e1bedb7be979fa726d56513fb(
    *options: FormMetadataOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70150c439ae952f7bcc7b1a2e279c30668bfa336ea9e48cc1e309be2eb7926fd(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f07aaa08eacd1bf8183d168acd09ee55f3496929f779ecd23bb81df97ddb96(
    *options: GlossaryOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34522afadc47cf22b048237a90a7f11811d2602ad1249c220a7c35e3e79c06d3(
    *,
    description: builtins.str,
    name: builtins.str,
    terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57d3ec706033ed8c378b2cb7657b3bf0375d7ccaf31ae4dfa275181495270fa(
    *,
    description: builtins.str,
    name: builtins.str,
    project: Project,
    terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee37fb28a680fae7dd63770e7012a0e0abbc53fa4a06b772a31f0606e13290c4(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    long_description: typing.Optional[builtins.str] = None,
    short_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f7dbf13e321db0e2c80848935eb374e79f4ab5699445d83e484a4da333d40d(
    *,
    glossary: IGlossary,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    long_description: typing.Optional[builtins.str] = None,
    short_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6cf000c38726d09ae0d29fb5be2383e80b10e5015924ad7c90d459fe70c585(
    terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073b6b415151bee91b07bbfbf7f89a996446093cd162308f6712b97d92bd20d1(
    *,
    designation: typing.Optional[builtins.str] = None,
    group_identifier: typing.Optional[builtins.str] = None,
    user_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b761796969f0d3e670ed3b0006657e72d98c1701c48439ffd336a6e7d59235ee(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    forms: typing.Optional[Forms] = None,
    glossaries: typing.Optional[Glossaries] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d47d1d493aefcb3756340c66339ea0fb5bf4e7e6e1c8b921088768b24aaa56e(
    *,
    domain: IDomain,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    forms: typing.Optional[Forms] = None,
    glossaries: typing.Optional[Glossaries] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2653735f026813879c695ad00ec9da3eb2ee8b45db72909b698dec0c236eb83(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d0be0fd72922e3b5144179fab0566e9caf316e037e370764fe12699af51531(
    *,
    sso_type: SingleSignOnType,
    user_assignment: typing.Optional[AssignmentType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462cf6a60c403adadbe13c3e507d2d99decf7241492bd212afd90cd0fca56719(
    *,
    filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
    data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653f241962f59123bb5f01155d6e25b61d2da7c5d6bf48a6e88193d19e243ace(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a0138fc421a725e636fb7cda918efc2a8164229bed82b6bc520b3fdd8006a4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d724a56bccbe14280ca9d1c4dc66868bba00415f1544e88afefbfbb51455b00d(
    terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38852639e497edbdd8194e6b2bb2d7c6cb79c43ad6992f02a0c0f20e65450d46(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542e7401c305eccdb74bbb1d633133befe1a3bcdc4493941a7f98c72859002a4(
    *,
    filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
    data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    auto_import_data_quality_result: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fac4ec4f68689051a6dd148a5d761cbad1aeef1c58e9a4aa49d387f359ad82(
    region: builtins.str,
    parameters: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83bce09fdde411da69d6f8e444344372d6c37585f218deebd3327d0207556cf(
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    forms: typing.Optional[Forms] = None,
    glossaries: typing.Optional[Glossaries] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee71a9b0868b645e54f0aac90cccca828ac7679dd777894102f9d7106eb4b88(
    blueprint_identifier: builtins.str,
    *,
    enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af8458257f33f2d7d1c0c007f6c3c8b72d490ada23b8989d1e23b0485d74c8e(
    name: builtins.str,
    *,
    configuration: IDataSourceConfiguration,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    publish_on_import: typing.Optional[builtins.bool] = None,
    recommendation: typing.Optional[builtins.bool] = None,
    schedule: typing.Optional[Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcca0809563154f3d4e97ccfb669481540ac60c4bfb9cdc1fc47baae323712b8(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95382963200337ac8e178328051aa7f1ea7b1073ae2b5a058592fe92965b3984(
    forms: Forms,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315c6b4f2e95ee7a5e2630172a762f7fb84549707b71f6b6a9a19715c738cbff(
    glossaries: Glossaries,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fd79973c1029cde79f05f570b9ff46b1de91f68a7c85719a7e5e8759518193(
    term: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54932b2748bbd8e2c08e2eb93bacf1eb74972f8ce656abe0e7b60f3f271e3a77(
    id: builtins.str,
    *,
    designation: typing.Optional[builtins.str] = None,
    group_identifier: typing.Optional[builtins.str] = None,
    user_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4436757b2f53ad06613c0be552854da3b637e053b8f0f354baa3ae5c98ace620(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b41948bfafe6f368a85395c3eded5f10deea30fb5ced358cae2167757c537d5(
    forms: Forms,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27742b00d372a9c06c2f87b7a8b40d5abc47e7998b4fd891435a822ebe1264a7(
    glossaries: Glossaries,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9995ec8b5f0b86f9ab0efc48d38efd5a011188dd21f03021e1015605025017c(
    term: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141d478e9d364f0a2559b5326365e433d92ca523d789881244b408401318fb4f(
    id: builtins.str,
    *,
    designation: typing.Optional[builtins.str] = None,
    group_identifier: typing.Optional[builtins.str] = None,
    user_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7716389965728144a006197d03926ab920aaa81e23ade4c0b7f8315c03eb55(
    *,
    filter_configurations: typing.Sequence[typing.Union[FilterConfiguration, typing.Dict[builtins.str, typing.Any]]],
    data_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    credentials: _aws_cdk_aws_secretsmanager_ceddda9d.Secret,
    name: builtins.str,
    redshift_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f683691be47fbe4d67b0c75bf2c725fe20eba7da5241acd66584e7176ca514c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ef75223420896e4239b46f9054d3eb7ca68855356bbf07a8bc2ccdfde3e80b(
    region: builtins.str,
    parameters: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961dbb93204583b2725c8fba135eb02e15928e1c32407bd5a6dd0cdd83f84ed3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28b2ea92bdf2ccea5a48be7a0247229d4388c6ac679464ec0b956895277f414(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5748c751cd6fa1e7c9a20e02cdd0d6970d7a0e29027ecb2538203719dda9981d(
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    forms: typing.Optional[Forms] = None,
    glossaries: typing.Optional[Glossaries] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8394b004e672ea7b229a646a20862362133d6305db806a89376b8281f87d5e19(
    blueprint_identifier: builtins.str,
    *,
    enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a14ceb05653b7f0c6e524c53d43e2159671f60d6224affcca3fe64d2178f3a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1127e6e6485a517a01ace3e23937be9a94ba111e4b03efa490c736c0cfb907a(
    name: builtins.str,
    *,
    configuration: IDataSourceConfiguration,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    publish_on_import: typing.Optional[builtins.bool] = None,
    recommendation: typing.Optional[builtins.bool] = None,
    schedule: typing.Optional[Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e99987a20aa95448cbed7a41c4585fd6755e0ada603840834983faeec47e0b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e579ad5f6993311b35c9f189e9d7d50108b85f437c654e6ed108e4093a0711dc(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfdced267f13185efffd6da1cf521d97be1b1111362027d219fb326a0b68a5c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    project: Project,
    description: typing.Optional[builtins.str] = None,
    smithy_model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a0fd13fdc30aa8ef98dd5fd7146e60762ad753aa7c996f698e004c90b0fd73(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    name: builtins.str,
    project: Project,
    terms: typing.Optional[typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25528749924e697cef618675656ab5a432bf67f8b6816ad45e4704d35f6967d2(
    terms: typing.Sequence[typing.Union[GlossaryTermOptions, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738f8c6d797404d777894649973ad263f6c6d30c7e1984d0906d672cd39afc74(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    glossary: IGlossary,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    long_description: typing.Optional[builtins.str] = None,
    short_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d50975878d385c12d4b5f684bd144183ee7ea64cff217e4acd9972fd4ac8d22(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain: IDomain,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    forms: typing.Optional[Forms] = None,
    glossaries: typing.Optional[Glossaries] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1127b376251ad20c3d469f0076164366fd82f462ffffbee288657e4fb3fdfd7a(
    forms: Forms,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34025c01dcffebf549132cedba6098d5b1a8a2cb4593dab6164cab8eff8d0c36(
    glossaries: Glossaries,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7f9ca2e0a2aaea268030e26ec68bc4d6ee8abb7d4a1dfdd7dba0d055049294(
    term: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0106f68484cf7a3e4ab6c2d567a7ef8ce31298e4f52dc637d2c40692da0a6326(
    id: builtins.str,
    *,
    designation: typing.Optional[builtins.str] = None,
    group_identifier: typing.Optional[builtins.str] = None,
    user_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d47d26ccb5bc6045752c8e7cc56c797389759bc97103c474b31b24b9313fa19(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain: IDomain,
    environment_blueprint_identifier: builtins.str,
    enabled_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    manage_access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    provisioning_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    regional_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7219a0bd26c826826c36a296c69d2a8ebbdc5e2cc3ee29397e89668f20910114(
    region: builtins.str,
    parameters: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e23e9d2f1db96f6cdd09ab74fd016a0703795d6ee939b83e9b46b01716da88(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    configuration: IDataSourceConfiguration,
    environment: IEnvironment,
    name: builtins.str,
    project: IProject,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    publish_on_import: typing.Optional[builtins.bool] = None,
    recommendation: typing.Optional[builtins.bool] = None,
    schedule: typing.Optional[Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01183080c547ab299e2a2e80c0b03778603522fbb8c9d3a0470ee2ae9846a1b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    domain_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    single_sign_on: typing.Optional[typing.Union[SingleSignOn, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29910e2c047e6cb7d822f4a3b82c1a0ea70d09be5b837b196e291518c0f991a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    environment_profile: IEnvironmentProfile,
    name: builtins.str,
    project: IProject,
    description: typing.Optional[builtins.str] = None,
    environment_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    glossary_terms: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironment.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33686a4c9543d6c075de60ff94c614916313accc94544e817284164ade832c7b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    blueprint: IBlueprint,
    name: builtins.str,
    project: IProject,
    aws_account_id: typing.Optional[builtins.str] = None,
    aws_account_region: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    user_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_datazone_ceddda9d.CfnEnvironmentProfile.EnvironmentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
