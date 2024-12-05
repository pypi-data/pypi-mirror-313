r'''
# Data Landing Zone

<!-- TOC -->

* [Getting Started](#getting-started)

  * [Typescript](#typescript)
  * [Python](#python-example)
* [Key Features](#key-features)
* [Intended Audience](#intended-audience)
* [Core Principles](#core-principles)
* [Integrated AWS Services](#integrated-aws-services)
* [How it works](#how-it-works)
* [Sponsors](#sponsors)
* [Contributing](#contributing)
* [Docs](#docs)
* [Roadmap](#roadmap)

<!-- TOC -->

The **Data Landing Zone (DLZ)** is a CDK construct designed to accelerate AI and data-related projects. It provides an
opinionated Landing Zone, laying the foundation for a multi-account AWS strategy, so you can focus on delivering data
and AI solutions.

The DLZ can be deployed in existing AWS Organizations or used in greenfield projects. It supports setups ranging
from small organizations with a few accounts to large enterprises with hundreds of accounts.

See the Documentation Website: https://datalandingzone.com/ for more information.

The CDK construct is available in both TypeScript and Python. Example GitHub repositories showing usage:

* [TypeScript Example GitHub Repo](https://github.com/DataChefHQ/aws-data-landing-zone-example-typescript)
* [Python Example GitHub Repo](https://github.com/DataChefHQ/aws-data-landing-zone-example-python)

## Getting Started

### Typescript

Install the [aws-data-landing-zone](https://www.npmjs.com/package/aws-data-landing-zone) CDK construct from NPM:

```bash
npm install aws-data-landing-zone
```

Use the construct as a stack in your CDK application. Replace the `organizationId`, `ouId`, `ous`, `accountId`, and
`regions` with your own values as per AWS Control Tower & AWS Organizations.

The example below shows a simple DLZ setup with two accounts, one for development and one for production, creating
two non-overlapping VPCs in two regions in each account.

```python
import {App} from 'aws-cdk-lib';
import { DataLandingZone } from '@DataChefHQ/data-landing-zone';

const app = new App();
const dlz = new DataLandingZone(app, {
  ...
  regions: {
    global: Region.EU_WEST_1,
    regional: [Region.US_EAST_1],
  },
  organization: {
    organizationId: 'o-0f5h921gk9',
    root: { accounts: { management: { accountId: '123456789012', }, }, },
    ous: {
      workloads: {
        ouId: 'ou-h2l0-gjr36ikn',
        accounts: [{
            name: 'development',
            accountId: '123456789012',
            type: DlzAccountType.DEVELOP,
            vpcs: [
              Defaults.vpcClassB3Private3Public(0, Region.US_EAST_1),
              Defaults.vpcClassB3Private3Public(1, Region.EU_WEST_1),
            ],
          },{
            name: 'production',
            accountId: '123456789012',
            type: DlzAccountType.PRODUCTION,
            vpcs: [
              Defaults.vpcClassB3Private3Public(2, Region.US_EAST_1),
              Defaults.vpcClassB3Private3Public(3, Region.EU_WEST_1),
            ],
          },

          ...AS MANY ACCOUNTS AS DESIRED...

          ]
      },
   },
   ...
 }
});
```

Continue reading [Getting Started](https://datalandingzone.com/getting-started/) on the DLZ documentation site.

### Python

Install the [aws-data-landing-zone](https://pypi.org/project/aws-data-landing-zone/#description) CDK construct from PyPi:

```bash
pip install aws-data-landing-zone
```

Use the construct as a stack in your CDK application. Replace the `organizationId`, `ouId`, `ous`, `accountId`, and
`regions` with your own values as per AWS Control Tower & AWS Organizations.

The example below shows a simple DLZ setup with two accounts, one for development and one for production, creating
two non-overlapping VPCs in two regions in each account.

```python
#!/usr/bin/env python3
import aws_cdk as cdk
import recipes_dlz as dlz

app = cdk.App()
dlz.DataLandingZone(app,
    local_profile="ct-sandbox-exported",
    regions=dlz.DlzRegions(
        global_=dlz.Region.EU_WEST_1,
        regional=[dlz.Region.US_EAST_1],
    ),
    organization=dlz.DLzOrganization(
        organization_id='o-0f5h921gk9',
        root=dlz.RootOptions(
            accounts=dlz.OrgRootAccounts(
                management=dlz.DLzManagementAccount(account_id='123456789012'),
            ),
        ),
        ous=dlz.OrgOus(
            workloads=dlz.OrgOuWorkloads(
                ou_id='ou-h2l0-gjr36ikn',
                accounts=[
                    dlz.DLzAccount(
                        name='development',
                        account_id='123456789012',
                        type=dlz.DlzAccountType.DEVELOP,
                        vpcs=[
                            dlz.Defaults.vpc_class_b3_private3_public(0, dlz.Region.US_EAST_1),
                            dlz.Defaults.vpc_class_b3_private3_public(1, dlz.Region.EU_WEST_1),
                        ]
                    ),
                    dlz.DLzAccount(
                        name='production',
                        account_id='123456789012',
                        type=dlz.DlzAccountType.PRODUCTION,
                        vpcs=[
                            dlz.Defaults.vpc_class_b3_private3_public(2, dlz.Region.US_EAST_1),
                            dlz.Defaults.vpc_class_b3_private3_public(3, dlz.Region.EU_WEST_1),
                        ]
                    ),
                ],
            ),
        )
    ),
)
app.synth()
```

Continue reading [Getting Started](https://datalandingzone.com/getting-started/) on the DLZ documentation site.

## Key Features

Notable features of the DLZ include:

* A CDK construct that can be used in TS and Python
* Opinionated but configurable and extendable. Each stack and nested component can be extended if needed.
* Leverages AWS Control Tower. Works with existing or new AWS Control Tower setups.
* Suitable for greenfield projects or integration with existing AWS resources.
* Deployable using any build systems like GitHub, GitLab, Jenkins, or locally.
* Generates compliance reports, reporting the Control Tower Standards, SecurityHub controls, Config Rules and
  Service Control Policies enabled in each account.
* Implements an internal wave- and stage-based deployment strategy for dependency management.
* Includes helper scripts and Standard Operating Procedures (SOPs) for routine tasks.
* Accompanied by comprehensive documentation.

## Intended Audience

The DLZ handles the responsibilities and routine tasks typically managed by a Cloud Center of Excellence (CCoE) team.
It's easy enough for Data Engineers to use on their own, but flexible enough to be customized and fine-tuned by
experienced Cloud Engineers.

It's important to establish the following responsibilities to understand what is in and out of scope for the DLZ:

* **In scope** - Any CCoE responsibilities and tasks, such as account management, security, networking, compliance, etc.
* **Out of scope** - Application development, data engineering, and data science tasks.

## Core Principles

The DLZ adheres to the following principles:

1. Opinionated but configurable defaults to suit diverse needs.
2. High levels of automation with manual SOPs where needed.
3. Simplicity and ease of understanding over complexity
4. Focused scope, limited to Landing Zone responsibilities.

## Integrated AWS Services

* **AWS Organizations:** Seamless multi-account management.
* **AWS Budgets:** Track spending by tags with notifications via Slack, Teams, or email.
* **Service Control Policies (SCPs):** Manage service deny lists.
* **Tag Policies:** Enforce resource tagging for spend tracking and ownership.
* **Control Tower Controls:** Opinionated defaults for preventive, detective, and proactive standards.
* **AWS Security Hub** and **AWS Config:** Additional standards not covered by Control Tower. Notifications are
  delivered via Slack, Teams, or email
* **Network Management:**

  * Non-overlapping **VPCs** across accounts.
  * **NAT Gateways** or instances for outbound private access.
  * **VPC Peering** for cross-account/region communication.
  * **Bastion Hosts** with **AWS SSM** for secure private resource access.
  * Simplified routing configurations.
* **IAM Identity Center (SSO):**

  * User management with **AWS Identity Store** or external IDPs (e.g., Google, Active Directory).
  * Manage **Permission Sets**
  * Manage **Access Groups** to assign Users to Accounts with a given Permission Set
* **Permission Boundaries:** Prevent privilege escalation for all IAM roles and users.
* Configure **Lake Formation** for Data Lake management, including:

  * General settings, like admins, version and setting hybrid iam mode
  * Create **Tags** and specify their permissions for use within the same account and when sharing to other accounts.
  * Optionally, set **Tag Permissions** on Tags. This is usually out of scope for DLZ, but can be configured.

## How it works

The DLZ defines all accounts and resources in a single CDK construct that can be used in Typescript or Python CDK
project.

The DLZ deploys resources into specified AWS accounts. These accounts must be created manually (SOP provided) in the
workloads OU, and their Account IDs must be provided in the DLZ configuration. Each account is designated
as either `development` or `production` to enable controlled, staged deployments, including the option for manual
approvals in production environments.

The construct processes the provided configuration to create logical deployment layers for resources. Each layer
consists of a Global Wave and optionally one or more Regional Waves. This structure ensures that all `global` stacks
for the accounts are deployed before the `regional` stacks. Resources in the `global` stack are region-independent, such
as IAM roles, whereas resources like VPCs can be deployed in both `global` and `regional` stacks if configured as such.

Continue reading the [Introduction](https://datalandingzone.com/introduction/) on the Data Landing Zone documentation site.

## Sponsors

Proudly sponsored and created by [DataChef](https://datachef.co.za/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for more info

## Docs

Can be found at https://datalandingzone.com/

## Roadmap

Can be found in the [here](https://github.com/orgs/DataChefHQ/projects/4)
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
import aws_cdk.aws_budgets as _aws_cdk_aws_budgets_ceddda9d
import aws_cdk.aws_chatbot as _aws_cdk_aws_chatbot_ceddda9d
import aws_cdk.aws_controltower as _aws_cdk_aws_controltower_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_organizations as _aws_cdk_aws_organizations_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sso as _aws_cdk_aws_sso_ceddda9d
import cdk_express_pipeline as _cdk_express_pipeline_9801c4a1
import constructs as _constructs_77d1e7e8


class AccountChatbots(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.AccountChatbots",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addSlackChannel")
    @builtins.classmethod
    def add_slack_channel(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        guardrail_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]] = None,
        logging_level: typing.Optional[_aws_cdk_aws_chatbot_ceddda9d.LoggingLevel] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        notification_topics: typing.Optional[typing.Sequence[_aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> _aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration:
        '''
        :param scope: -
        :param id: -
        :param slack_channel_configuration_name: The name of Slack channel configuration.
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot. To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.
        :param guardrail_policies: A list of IAM managed policies that are applied as channel guardrails. Default: - The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Default: LoggingLevel.NONE
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param notification_topics: The SNS topics that deliver notifications to AWS Chatbot. Default: None
        :param role: The permission role of Slack channel configuration. Default: - A role will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d75b413d9441f6011ff7a26ced44e3d3e131ffd42d93f7ab7d7fb91d1f50661)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        chatbot_props = _aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfigurationProps(
            slack_channel_configuration_name=slack_channel_configuration_name,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            guardrail_policies=guardrail_policies,
            logging_level=logging_level,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            notification_topics=notification_topics,
            role=role,
        )

        return typing.cast(_aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration, jsii.sinvoke(cls, "addSlackChannel", [scope, id, chatbot_props]))

    @jsii.member(jsii_name="existsSlackChannel")
    @builtins.classmethod
    def exists_slack_channel(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
    ) -> builtins.bool:
        '''
        :param scope: -
        :param slack_channel_configuration_name: 
        :param slack_channel_id: 
        :param slack_workspace_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beb2f4f62037429f2d11a36471ad469e3affb167ffcac5a92fdb10f4a070a88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        chatbot_props = SlackChannel(
            slack_channel_configuration_name=slack_channel_configuration_name,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
        )

        return typing.cast(builtins.bool, jsii.sinvoke(cls, "existsSlackChannel", [scope, chatbot_props]))

    @jsii.member(jsii_name="findSlackChannel")
    @builtins.classmethod
    def find_slack_channel(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
    ) -> _aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration:
        '''
        :param scope: -
        :param slack_channel_configuration_name: 
        :param slack_channel_id: 
        :param slack_workspace_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d79f537e6d9cfd7b530701576571f87bb131ef46e198f06d0aa23c9886303c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        chatbot_props = SlackChannel(
            slack_channel_configuration_name=slack_channel_configuration_name,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
        )

        return typing.cast(_aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration, jsii.sinvoke(cls, "findSlackChannel", [scope, chatbot_props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="slackChatBots")
    def slack_chat_bots(
        cls,
    ) -> typing.Mapping[builtins.str, _aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration]:  # pyright: ignore [reportGeneralTypeIssues,reportRedeclaration]
        return typing.cast(typing.Mapping[builtins.str, _aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration], jsii.sget(cls, "slackChatBots"))

    @slack_chat_bots.setter # type: ignore[no-redef]
    def slack_chat_bots(
        cls,
        value: typing.Mapping[builtins.str, _aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63801243c6145aee99d7be6a52e351bd62d8bc4f1d6dc07b7947ea344e10fece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "slackChatBots", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-data-landing-zone.AuditStacks",
    jsii_struct_bases=[],
    name_mapping={"global_": "global"},
)
class AuditStacks:
    def __init__(self, *, global_: "AuditGlobalStack") -> None:
        '''
        :param global_: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ca5436fcb484c55eec119b25d6a31d4eb5a0553d2eacb6f758de330d9cfbe5)
            check_type(argname="argument global_", value=global_, expected_type=type_hints["global_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "global_": global_,
        }

    @builtins.property
    def global_(self) -> "AuditGlobalStack":
        result = self._values.get("global_")
        assert result is not None, "Required property 'global_' is missing"
        return typing.cast("AuditGlobalStack", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuditStacks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.BaseSharedTagProps",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals", "specific_values": "specificValues"},
)
class BaseSharedTagProps:
    def __init__(
        self,
        *,
        principals: typing.Sequence[builtins.str],
        specific_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param principals: A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.
        :param specific_values: OPTIONAL - A list of specific values of the tag that can be shared. All possible values if omitted.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b559c6c485e7fdaa87214275f77db21c4be3aaf1bfc191cd62a9a6937b07261b)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument specific_values", value=specific_values, expected_type=type_hints["specific_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principals": principals,
        }
        if specific_values is not None:
            self._values["specific_values"] = specific_values

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.'''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def specific_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''OPTIONAL - A list of specific values of the tag that can be shared.

        All possible values if omitted.
        '''
        result = self._values.get("specific_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseSharedTagProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.BastionHost",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "location": "location",
        "name": "name",
    },
)
class BastionHost:
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        location: "NetworkAddress",
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: The bastion instance EC2 type.
        :param location: The location where the Bastion will exist. The network address must target a specific subnet
        :param name: The name of the Bastion, defaults to 'default', specify the name if there are more than one per account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2cb69a9750eb61b200f419207a31a68cee01d3348c0e4613150cb34d1e4cfd)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
            "location": location,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        '''The bastion instance EC2 type.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, result)

    @builtins.property
    def location(self) -> "NetworkAddress":
        '''The location where the Bastion will exist.

        The network address must target a specific subnet
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast("NetworkAddress", result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bastion, defaults to 'default', specify the name if there are more than one per account.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionHost(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.BudgetSubscribers",
    jsii_struct_bases=[],
    name_mapping={"emails": "emails", "slack": "slack"},
)
class BudgetSubscribers:
    def __init__(
        self,
        *,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        slack: typing.Optional[typing.Union["SlackChannel", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param emails: 
        :param slack: 
        '''
        if isinstance(slack, dict):
            slack = SlackChannel(**slack)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282be6b5a9ccbee8083d992f0211e955891d27c0b48f2f574ab8e91d786addaa)
            check_type(argname="argument emails", value=emails, expected_type=type_hints["emails"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if emails is not None:
            self._values["emails"] = emails
        if slack is not None:
            self._values["slack"] = slack

    @builtins.property
    def emails(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def slack(self) -> typing.Optional["SlackChannel"]:
        result = self._values.get("slack")
        return typing.cast(typing.Optional["SlackChannel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetSubscribers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DLzAccount",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "name": "name",
        "type": "type",
        "default_notification": "defaultNotification",
        "lake_formation": "lakeFormation",
        "vpcs": "vpcs",
    },
)
class DLzAccount:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        name: builtins.str,
        type: "DlzAccountType",
        default_notification: typing.Optional[typing.Union["NotificationDetailsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        lake_formation: typing.Optional[typing.Sequence[typing.Union["DlzLakeFormationProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpcs: typing.Optional[typing.Sequence[typing.Union["DlzVpcProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param account_id: 
        :param name: 
        :param type: 
        :param default_notification: Default notifications settings for the account. Defines settings for email notifications or the slack channel details. This will override the organization level defaultNotification.
        :param lake_formation: LakeFormation settings and tags.
        :param vpcs: 
        '''
        if isinstance(default_notification, dict):
            default_notification = NotificationDetailsProps(**default_notification)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b344243292003fa647f9fb13ce28a54ff3b50dab37803f184c592fad2ee6478f)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument default_notification", value=default_notification, expected_type=type_hints["default_notification"])
            check_type(argname="argument lake_formation", value=lake_formation, expected_type=type_hints["lake_formation"])
            check_type(argname="argument vpcs", value=vpcs, expected_type=type_hints["vpcs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "name": name,
            "type": type,
        }
        if default_notification is not None:
            self._values["default_notification"] = default_notification
        if lake_formation is not None:
            self._values["lake_formation"] = lake_formation
        if vpcs is not None:
            self._values["vpcs"] = vpcs

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "DlzAccountType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("DlzAccountType", result)

    @builtins.property
    def default_notification(self) -> typing.Optional["NotificationDetailsProps"]:
        '''Default notifications settings for the account.

        Defines settings for email notifications or the slack channel details.
        This will override the organization level defaultNotification.
        '''
        result = self._values.get("default_notification")
        return typing.cast(typing.Optional["NotificationDetailsProps"], result)

    @builtins.property
    def lake_formation(self) -> typing.Optional[typing.List["DlzLakeFormationProps"]]:
        '''LakeFormation settings and tags.'''
        result = self._values.get("lake_formation")
        return typing.cast(typing.Optional[typing.List["DlzLakeFormationProps"]], result)

    @builtins.property
    def vpcs(self) -> typing.Optional[typing.List["DlzVpcProps"]]:
        result = self._values.get("vpcs")
        return typing.cast(typing.Optional[typing.List["DlzVpcProps"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DLzAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DLzManagementAccount",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId"},
)
class DLzManagementAccount:
    def __init__(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a19f78bcdb9bf21f1e19f607435a0bbb721d78633ea2243aeb6b20855317449)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DLzManagementAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DLzOrganization",
    jsii_struct_bases=[],
    name_mapping={"organization_id": "organizationId", "ous": "ous", "root": "root"},
)
class DLzOrganization:
    def __init__(
        self,
        *,
        organization_id: builtins.str,
        ous: typing.Union["OrgOus", typing.Dict[builtins.str, typing.Any]],
        root: typing.Union["RootOptions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param organization_id: 
        :param ous: 
        :param root: 
        '''
        if isinstance(ous, dict):
            ous = OrgOus(**ous)
        if isinstance(root, dict):
            root = RootOptions(**root)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18589fd274506fd010b902ea469bde990dfacaf0004a299e29d6545e328eb158)
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
            check_type(argname="argument ous", value=ous, expected_type=type_hints["ous"])
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "organization_id": organization_id,
            "ous": ous,
            "root": root,
        }

    @builtins.property
    def organization_id(self) -> builtins.str:
        result = self._values.get("organization_id")
        assert result is not None, "Required property 'organization_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ous(self) -> "OrgOus":
        result = self._values.get("ous")
        assert result is not None, "Required property 'ous' is missing"
        return typing.cast("OrgOus", result)

    @builtins.property
    def root(self) -> "RootOptions":
        result = self._values.get("root")
        assert result is not None, "Required property 'root' is missing"
        return typing.cast("RootOptions", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DLzOrganization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLandingZone(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DataLandingZone",
):
    def __init__(
        self,
        app: _aws_cdk_ceddda9d.App,
        props: typing.Union["DataLandingZoneProps", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Create a new Data Landing Zone.

        :param app: The CDK App.
        :param props: The DataLandingZoneProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b77304187f3a7eec71abe26e2f24630a339a7643aa355c54307d1ac8e16ecc)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        _ = ForceNoPythonArgumentLifting()

        jsii.create(self.__class__, self, [app, props, _])

    @jsii.member(jsii_name="stageManagement")
    def stage_management(self) -> "ManagementStack":
        return typing.cast("ManagementStack", jsii.invoke(self, "stageManagement", []))

    @builtins.property
    @jsii.member(jsii_name="auditStacks")
    def audit_stacks(self) -> AuditStacks:
        return typing.cast(AuditStacks, jsii.get(self, "auditStacks"))

    @audit_stacks.setter
    def audit_stacks(self, value: AuditStacks) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8d8cfa804a878147787bce94ed7b000d79dea96a5035244df709f3e42dbfd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditStacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStacks")
    def log_stacks(self) -> "LogStacks":
        return typing.cast("LogStacks", jsii.get(self, "logStacks"))

    @log_stacks.setter
    def log_stacks(self, value: "LogStacks") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7f4623d332e87faa8befdf0d19b5894aaab05539bbe35c13f1e7b5f32acacc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managementStack")
    def management_stack(self) -> "ManagementStack":
        return typing.cast("ManagementStack", jsii.get(self, "managementStack"))

    @management_stack.setter
    def management_stack(self, value: "ManagementStack") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1ef579c74a4708bdf38f6935a86f802d9e5ff60688e4ad8f839de0eddaa1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementStack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadGlobalDataServicesPhase1Stacks")
    def workload_global_data_services_phase1_stacks(
        self,
    ) -> typing.List["WorkloadGlobalDataServicesPhase1Stack"]:
        return typing.cast(typing.List["WorkloadGlobalDataServicesPhase1Stack"], jsii.get(self, "workloadGlobalDataServicesPhase1Stacks"))

    @workload_global_data_services_phase1_stacks.setter
    def workload_global_data_services_phase1_stacks(
        self,
        value: typing.List["WorkloadGlobalDataServicesPhase1Stack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8aa98ab0e13da9342ce4fb09cb9d06784dbfd05bb8c9055b87b90f1a22ac9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadGlobalDataServicesPhase1Stacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadGlobalNetworkConnectionsPhase1Stacks")
    def workload_global_network_connections_phase1_stacks(
        self,
    ) -> typing.List["WorkloadGlobalNetworkConnectionsPhase1Stack"]:
        return typing.cast(typing.List["WorkloadGlobalNetworkConnectionsPhase1Stack"], jsii.get(self, "workloadGlobalNetworkConnectionsPhase1Stacks"))

    @workload_global_network_connections_phase1_stacks.setter
    def workload_global_network_connections_phase1_stacks(
        self,
        value: typing.List["WorkloadGlobalNetworkConnectionsPhase1Stack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a277403bafb3009ba04dd48c7f087d505d6fe225131886a50258944c94eecc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadGlobalNetworkConnectionsPhase1Stacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadGlobalNetworkConnectionsPhase2Stacks")
    def workload_global_network_connections_phase2_stacks(
        self,
    ) -> typing.List["WorkloadGlobalNetworkConnectionsPhase2Stack"]:
        return typing.cast(typing.List["WorkloadGlobalNetworkConnectionsPhase2Stack"], jsii.get(self, "workloadGlobalNetworkConnectionsPhase2Stacks"))

    @workload_global_network_connections_phase2_stacks.setter
    def workload_global_network_connections_phase2_stacks(
        self,
        value: typing.List["WorkloadGlobalNetworkConnectionsPhase2Stack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85f042a7a8a1ef2236e100ff174a3bcd7e861ba455d89073ee514c4267ac18b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadGlobalNetworkConnectionsPhase2Stacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadGlobalNetworkConnectionsPhase3Stacks")
    def workload_global_network_connections_phase3_stacks(
        self,
    ) -> typing.List["WorkloadGlobalNetworkConnectionsPhase3Stack"]:
        return typing.cast(typing.List["WorkloadGlobalNetworkConnectionsPhase3Stack"], jsii.get(self, "workloadGlobalNetworkConnectionsPhase3Stacks"))

    @workload_global_network_connections_phase3_stacks.setter
    def workload_global_network_connections_phase3_stacks(
        self,
        value: typing.List["WorkloadGlobalNetworkConnectionsPhase3Stack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e227a57ecac9966da94c0e58510b51a9867e1f2f9811cad72a4af305e0a84392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadGlobalNetworkConnectionsPhase3Stacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadGlobalStacks")
    def workload_global_stacks(self) -> typing.List["WorkloadGlobalStack"]:
        return typing.cast(typing.List["WorkloadGlobalStack"], jsii.get(self, "workloadGlobalStacks"))

    @workload_global_stacks.setter
    def workload_global_stacks(self, value: typing.List["WorkloadGlobalStack"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb0448902aed2ba432ac8ce3b5482a514437c0a81fb2a66be8a5b73b99c0264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadGlobalStacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadRegionalDataServicesPhase1Stacks")
    def workload_regional_data_services_phase1_stacks(
        self,
    ) -> typing.List["WorkloadRegionalDataServicesPhase1Stack"]:
        return typing.cast(typing.List["WorkloadRegionalDataServicesPhase1Stack"], jsii.get(self, "workloadRegionalDataServicesPhase1Stacks"))

    @workload_regional_data_services_phase1_stacks.setter
    def workload_regional_data_services_phase1_stacks(
        self,
        value: typing.List["WorkloadRegionalDataServicesPhase1Stack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b6d85bde2374f0d011498bd1e186bb41abc7184486e2c42dff6a9aedcf1a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadRegionalDataServicesPhase1Stacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadRegionalNetworkConnectionsPhase2Stacks")
    def workload_regional_network_connections_phase2_stacks(
        self,
    ) -> typing.List["WorkloadRegionalNetworkConnectionsPhase2Stack"]:
        return typing.cast(typing.List["WorkloadRegionalNetworkConnectionsPhase2Stack"], jsii.get(self, "workloadRegionalNetworkConnectionsPhase2Stacks"))

    @workload_regional_network_connections_phase2_stacks.setter
    def workload_regional_network_connections_phase2_stacks(
        self,
        value: typing.List["WorkloadRegionalNetworkConnectionsPhase2Stack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8db637c190c369de7d443a21a0abdf8bce7871238ff2f65be86638f1760bbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadRegionalNetworkConnectionsPhase2Stacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadRegionalNetworkConnectionsPhase3Stacks")
    def workload_regional_network_connections_phase3_stacks(
        self,
    ) -> typing.List["WorkloadRegionalNetworkConnectionsPhase3Stack"]:
        return typing.cast(typing.List["WorkloadRegionalNetworkConnectionsPhase3Stack"], jsii.get(self, "workloadRegionalNetworkConnectionsPhase3Stacks"))

    @workload_regional_network_connections_phase3_stacks.setter
    def workload_regional_network_connections_phase3_stacks(
        self,
        value: typing.List["WorkloadRegionalNetworkConnectionsPhase3Stack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c26991a55be9b76068285c9aa0e8d85bcaad74035579d207f7d2d1ce0ad43e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadRegionalNetworkConnectionsPhase3Stacks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadRegionalStacks")
    def workload_regional_stacks(self) -> typing.List["WorkloadRegionalStack"]:
        return typing.cast(typing.List["WorkloadRegionalStack"], jsii.get(self, "workloadRegionalStacks"))

    @workload_regional_stacks.setter
    def workload_regional_stacks(
        self,
        value: typing.List["WorkloadRegionalStack"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a5540e11ebcf2d5a9662c974c122d507568ba798295da7581c14054a11460b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadRegionalStacks", value) # pyright: ignore[reportArgumentType]


class DataLandingZoneClient(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DataLandingZoneClient",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bastionSecurityGroupId")
    @builtins.classmethod
    def bastion_security_group_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bastion_name: typing.Optional[builtins.str] = None,
        account_name: builtins.str,
        region: builtins.str,
    ) -> builtins.str:
        '''Fetches the bastion security group ID from the SSM Parameter Store.

        :param scope: - The scope of the construct.
        :param id: - The id of the construct.
        :param bastion_name: 
        :param account_name: 
        :param region: 

        :return: - The security group ID of the bastion
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14760a7e9daee1783371458d8eecbf8879764ca3635ba5b7527e49b73d2549e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLandingZoneClientBastionProps(
            bastion_name=bastion_name, account_name=account_name, region=region
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "bastionSecurityGroupId", [scope, id, props]))

    @jsii.member(jsii_name="notificationTopicArn")
    @builtins.classmethod
    def notification_topic_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> builtins.str:
        '''Fetches the notification topic ARN from the SSM Parameter Store.

        :param scope: - The scope of the construct.
        :param id: - The id of the construct.

        :return: - The ARN of the notification topic
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0170dd4979fb727a950e482bd3ec769c8231f76716d9896a8e41d2373b8d3c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "notificationTopicArn", [scope, id]))

    @jsii.member(jsii_name="permissionsBoundaryArn")
    @builtins.classmethod
    def permissions_boundary_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> builtins.str:
        '''Fetches the permissions boundary ARN from the SSM Parameter Store.

        :param scope: - The scope of the construct.
        :param id: - The id of the construct.

        :return: - The ARN of the permissions boundary
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb969cefcf30682e210baa18fba5281c6cd8dc1fbc057c5cf66c06508822dae6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "permissionsBoundaryArn", [scope, id]))

    @jsii.member(jsii_name="routeTableId")
    @builtins.classmethod
    def route_table_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        route_table: builtins.str,
        vpc_name: builtins.str,
        account_name: builtins.str,
        region: builtins.str,
    ) -> builtins.str:
        '''Fetches the route table ID from the SSM Parameter Store.

        :param scope: - The scope of the construct.
        :param id: - The id of the construct.
        :param route_table: 
        :param vpc_name: 
        :param account_name: 
        :param region: 

        :return: - The ID of the route table
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aee38186b48fb466a7b906bd6854f768db30be21e31d802f33999b500d6b617)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLandingZoneClientRouteTableIdProps(
            route_table=route_table,
            vpc_name=vpc_name,
            account_name=account_name,
            region=region,
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "routeTableId", [scope, id, props]))

    @jsii.member(jsii_name="subnetId")
    @builtins.classmethod
    def subnet_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        route_table: builtins.str,
        subnet_name: builtins.str,
        vpc_name: builtins.str,
        account_name: builtins.str,
        region: builtins.str,
    ) -> builtins.str:
        '''Fetches the subnet ID from the SSM Parameter Store.

        :param scope: - The scope of the construct.
        :param id: - The id of the construct.
        :param route_table: 
        :param subnet_name: 
        :param vpc_name: 
        :param account_name: 
        :param region: 

        :return: - The ID of the subnet
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91adc9857eafe8793b09810f7f4809c71c044752b23610870539566bde3bf705)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLandingZoneClientSubnetIdProps(
            route_table=route_table,
            subnet_name=subnet_name,
            vpc_name=vpc_name,
            account_name=account_name,
            region=region,
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "subnetId", [scope, id, props]))

    @jsii.member(jsii_name="vpcId")
    @builtins.classmethod
    def vpc_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc_name: builtins.str,
        account_name: builtins.str,
        region: builtins.str,
    ) -> builtins.str:
        '''Fetches the VPC ID from the SSM Parameter Store.

        :param scope: - The scope of the construct.
        :param id: - The id of the construct.
        :param vpc_name: 
        :param account_name: 
        :param region: 

        :return: - The ID of the VPC
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01558c92dc56ea0868468c972083bf9301adf2cd2c8484cb7ef80a547efecc7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLandingZoneClientVpcIdProps(
            vpc_name=vpc_name, account_name=account_name, region=region
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "vpcId", [scope, id, props]))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DataLandingZoneClientProps",
    jsii_struct_bases=[],
    name_mapping={"account_name": "accountName", "region": "region"},
)
class DataLandingZoneClientProps:
    def __init__(self, *, account_name: builtins.str, region: builtins.str) -> None:
        '''
        :param account_name: 
        :param region: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f449134d3e1792b7f1f4320b7bd9b6965a4302c9bac0ba752f5802e5a1a996d0)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "region": region,
        }

    @builtins.property
    def account_name(self) -> builtins.str:
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLandingZoneClientProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DataLandingZoneClientRouteTableIdProps",
    jsii_struct_bases=[DataLandingZoneClientProps],
    name_mapping={
        "account_name": "accountName",
        "region": "region",
        "route_table": "routeTable",
        "vpc_name": "vpcName",
    },
)
class DataLandingZoneClientRouteTableIdProps(DataLandingZoneClientProps):
    def __init__(
        self,
        *,
        account_name: builtins.str,
        region: builtins.str,
        route_table: builtins.str,
        vpc_name: builtins.str,
    ) -> None:
        '''
        :param account_name: 
        :param region: 
        :param route_table: 
        :param vpc_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b5e979d27944d3a0cae7a0665939fd5788881938a8e78cf579da84f234d40f)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "region": region,
            "route_table": route_table,
            "vpc_name": vpc_name,
        }

    @builtins.property
    def account_name(self) -> builtins.str:
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_table(self) -> builtins.str:
        result = self._values.get("route_table")
        assert result is not None, "Required property 'route_table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_name(self) -> builtins.str:
        result = self._values.get("vpc_name")
        assert result is not None, "Required property 'vpc_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLandingZoneClientRouteTableIdProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DataLandingZoneClientSubnetIdProps",
    jsii_struct_bases=[DataLandingZoneClientProps],
    name_mapping={
        "account_name": "accountName",
        "region": "region",
        "route_table": "routeTable",
        "subnet_name": "subnetName",
        "vpc_name": "vpcName",
    },
)
class DataLandingZoneClientSubnetIdProps(DataLandingZoneClientProps):
    def __init__(
        self,
        *,
        account_name: builtins.str,
        region: builtins.str,
        route_table: builtins.str,
        subnet_name: builtins.str,
        vpc_name: builtins.str,
    ) -> None:
        '''
        :param account_name: 
        :param region: 
        :param route_table: 
        :param subnet_name: 
        :param vpc_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09352a173f9149cf4e1ff39d20ae951eaa4345a58b2bbeb815cea35090eb2c87)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
            check_type(argname="argument subnet_name", value=subnet_name, expected_type=type_hints["subnet_name"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "region": region,
            "route_table": route_table,
            "subnet_name": subnet_name,
            "vpc_name": vpc_name,
        }

    @builtins.property
    def account_name(self) -> builtins.str:
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_table(self) -> builtins.str:
        result = self._values.get("route_table")
        assert result is not None, "Required property 'route_table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_name(self) -> builtins.str:
        result = self._values.get("subnet_name")
        assert result is not None, "Required property 'subnet_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_name(self) -> builtins.str:
        result = self._values.get("vpc_name")
        assert result is not None, "Required property 'vpc_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLandingZoneClientSubnetIdProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DataLandingZoneClientVpcIdProps",
    jsii_struct_bases=[DataLandingZoneClientProps],
    name_mapping={
        "account_name": "accountName",
        "region": "region",
        "vpc_name": "vpcName",
    },
)
class DataLandingZoneClientVpcIdProps(DataLandingZoneClientProps):
    def __init__(
        self,
        *,
        account_name: builtins.str,
        region: builtins.str,
        vpc_name: builtins.str,
    ) -> None:
        '''
        :param account_name: 
        :param region: 
        :param vpc_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6fd60032038fee1a643f3f5d4a856840d347c5bfa5778e2a370fdb243cff02)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "region": region,
            "vpc_name": vpc_name,
        }

    @builtins.property
    def account_name(self) -> builtins.str:
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_name(self) -> builtins.str:
        result = self._values.get("vpc_name")
        assert result is not None, "Required property 'vpc_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLandingZoneClientVpcIdProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DataLandingZoneProps",
    jsii_struct_bases=[],
    name_mapping={
        "budgets": "budgets",
        "local_profile": "localProfile",
        "mandatory_tags": "mandatoryTags",
        "organization": "organization",
        "regions": "regions",
        "security_hub_notifications": "securityHubNotifications",
        "additional_mandatory_tags": "additionalMandatoryTags",
        "default_notification": "defaultNotification",
        "deny_service_list": "denyServiceList",
        "deployment_platform": "deploymentPlatform",
        "iam_identity_center": "iamIdentityCenter",
        "iam_policy_permission_boundary": "iamPolicyPermissionBoundary",
        "network": "network",
        "print_deployment_order": "printDeploymentOrder",
        "print_report": "printReport",
        "save_report": "saveReport",
    },
)
class DataLandingZoneProps:
    def __init__(
        self,
        *,
        budgets: typing.Sequence[typing.Union["DlzBudgetProps", typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union["MandatoryTags", typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union["DlzRegions", typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union["SecurityHubNotification", typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union["DlzTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union["NotificationDetailsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union["DeploymentPlatform", typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union["IamIdentityCenterProps", typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union["IamPolicyPermissionsBoundaryProps", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["Network", typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if isinstance(mandatory_tags, dict):
            mandatory_tags = MandatoryTags(**mandatory_tags)
        if isinstance(organization, dict):
            organization = DLzOrganization(**organization)
        if isinstance(regions, dict):
            regions = DlzRegions(**regions)
        if isinstance(default_notification, dict):
            default_notification = NotificationDetailsProps(**default_notification)
        if isinstance(deployment_platform, dict):
            deployment_platform = DeploymentPlatform(**deployment_platform)
        if isinstance(iam_identity_center, dict):
            iam_identity_center = IamIdentityCenterProps(**iam_identity_center)
        if isinstance(iam_policy_permission_boundary, dict):
            iam_policy_permission_boundary = IamPolicyPermissionsBoundaryProps(**iam_policy_permission_boundary)
        if isinstance(network, dict):
            network = Network(**network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5bd8adbb27064bd1c139bab0940042c73398d282308158866d9a650ef5390ad)
            check_type(argname="argument budgets", value=budgets, expected_type=type_hints["budgets"])
            check_type(argname="argument local_profile", value=local_profile, expected_type=type_hints["local_profile"])
            check_type(argname="argument mandatory_tags", value=mandatory_tags, expected_type=type_hints["mandatory_tags"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument security_hub_notifications", value=security_hub_notifications, expected_type=type_hints["security_hub_notifications"])
            check_type(argname="argument additional_mandatory_tags", value=additional_mandatory_tags, expected_type=type_hints["additional_mandatory_tags"])
            check_type(argname="argument default_notification", value=default_notification, expected_type=type_hints["default_notification"])
            check_type(argname="argument deny_service_list", value=deny_service_list, expected_type=type_hints["deny_service_list"])
            check_type(argname="argument deployment_platform", value=deployment_platform, expected_type=type_hints["deployment_platform"])
            check_type(argname="argument iam_identity_center", value=iam_identity_center, expected_type=type_hints["iam_identity_center"])
            check_type(argname="argument iam_policy_permission_boundary", value=iam_policy_permission_boundary, expected_type=type_hints["iam_policy_permission_boundary"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument print_deployment_order", value=print_deployment_order, expected_type=type_hints["print_deployment_order"])
            check_type(argname="argument print_report", value=print_report, expected_type=type_hints["print_report"])
            check_type(argname="argument save_report", value=save_report, expected_type=type_hints["save_report"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "budgets": budgets,
            "local_profile": local_profile,
            "mandatory_tags": mandatory_tags,
            "organization": organization,
            "regions": regions,
            "security_hub_notifications": security_hub_notifications,
        }
        if additional_mandatory_tags is not None:
            self._values["additional_mandatory_tags"] = additional_mandatory_tags
        if default_notification is not None:
            self._values["default_notification"] = default_notification
        if deny_service_list is not None:
            self._values["deny_service_list"] = deny_service_list
        if deployment_platform is not None:
            self._values["deployment_platform"] = deployment_platform
        if iam_identity_center is not None:
            self._values["iam_identity_center"] = iam_identity_center
        if iam_policy_permission_boundary is not None:
            self._values["iam_policy_permission_boundary"] = iam_policy_permission_boundary
        if network is not None:
            self._values["network"] = network
        if print_deployment_order is not None:
            self._values["print_deployment_order"] = print_deployment_order
        if print_report is not None:
            self._values["print_report"] = print_report
        if save_report is not None:
            self._values["save_report"] = save_report

    @builtins.property
    def budgets(self) -> typing.List["DlzBudgetProps"]:
        result = self._values.get("budgets")
        assert result is not None, "Required property 'budgets' is missing"
        return typing.cast(typing.List["DlzBudgetProps"], result)

    @builtins.property
    def local_profile(self) -> builtins.str:
        '''The the AWS CLI profile that will be used to run the Scripts.

        For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume
        the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and
        should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts
        but the ``bootstrap`` script requires full admin access.
        '''
        result = self._values.get("local_profile")
        assert result is not None, "Required property 'local_profile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mandatory_tags(self) -> "MandatoryTags":
        '''The values of the mandatory tags that all resources must have.

        The following values are already specified and used by the DLZ constructs

        - Owner: [infra]
        - Project: [dlz]
        - Environment: [dlz]
        '''
        result = self._values.get("mandatory_tags")
        assert result is not None, "Required property 'mandatory_tags' is missing"
        return typing.cast("MandatoryTags", result)

    @builtins.property
    def organization(self) -> DLzOrganization:
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(DLzOrganization, result)

    @builtins.property
    def regions(self) -> "DlzRegions":
        result = self._values.get("regions")
        assert result is not None, "Required property 'regions' is missing"
        return typing.cast("DlzRegions", result)

    @builtins.property
    def security_hub_notifications(self) -> typing.List["SecurityHubNotification"]:
        result = self._values.get("security_hub_notifications")
        assert result is not None, "Required property 'security_hub_notifications' is missing"
        return typing.cast(typing.List["SecurityHubNotification"], result)

    @builtins.property
    def additional_mandatory_tags(self) -> typing.Optional[typing.List["DlzTag"]]:
        '''List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort.

        Mandatory tags are defined in Defaults.mandatoryTags() which are:

        - Owner, the team responsible for the resource
        - Project, the project the resource is part of
        - Environment, the environment the resource is part of

        It creates:

        1. A tag policy in the organization
        2. An SCP on the organization that all CFN stacks must have these tags when created
        3. An AWS Config rule that checks for these tags on all CFN stacks and resources

        For all stacks created by DLZ the following tags are applied:

        - Owner: infra
        - Project: dlz
        - Environment: dlz

        :default: Defaults.mandatoryTags()
        '''
        result = self._values.get("additional_mandatory_tags")
        return typing.cast(typing.Optional[typing.List["DlzTag"]], result)

    @builtins.property
    def default_notification(self) -> typing.Optional["NotificationDetailsProps"]:
        '''Default notification settings for the organization.

        Allows you to define the
        email notfication settings or slack channel settings. If the account level defaultNotification
        is defined those will be used for the account instead of this defaultNotification which
        acts as the fallback.
        '''
        result = self._values.get("default_notification")
        return typing.cast(typing.Optional["NotificationDetailsProps"], result)

    @builtins.property
    def deny_service_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of services to deny in the organization SCP.

        If not specified, the default defined by

        :default: DataLandingZone.defaultDenyServiceList()
        '''
        result = self._values.get("deny_service_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deployment_platform(self) -> typing.Optional["DeploymentPlatform"]:
        result = self._values.get("deployment_platform")
        return typing.cast(typing.Optional["DeploymentPlatform"], result)

    @builtins.property
    def iam_identity_center(self) -> typing.Optional["IamIdentityCenterProps"]:
        '''IAM Identity Center configuration.'''
        result = self._values.get("iam_identity_center")
        return typing.cast(typing.Optional["IamIdentityCenterProps"], result)

    @builtins.property
    def iam_policy_permission_boundary(
        self,
    ) -> typing.Optional["IamPolicyPermissionsBoundaryProps"]:
        '''IAM Policy Permission Boundary.'''
        result = self._values.get("iam_policy_permission_boundary")
        return typing.cast(typing.Optional["IamPolicyPermissionsBoundaryProps"], result)

    @builtins.property
    def network(self) -> typing.Optional["Network"]:
        result = self._values.get("network")
        return typing.cast(typing.Optional["Network"], result)

    @builtins.property
    def print_deployment_order(self) -> typing.Optional[builtins.bool]:
        '''Print the deployment order to the console.

        :default: true
        '''
        result = self._values.get("print_deployment_order")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def print_report(self) -> typing.Optional[builtins.bool]:
        '''Print the report grouped by account, type and aggregated regions to the console.

        :default: true
        '''
        result = self._values.get("print_report")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def save_report(self) -> typing.Optional[builtins.bool]:
        '''Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder.

        :default: true
        '''
        result = self._values.get("save_report")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLandingZoneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.DatabaseAction")
class DatabaseAction(enum.Enum):
    DESCRIBE = "DESCRIBE"
    ALTER = "ALTER"
    DROP = "DROP"
    CREATE_TABLE = "CREATE_TABLE"


class Defaults(metaclass=jsii.JSIIMeta, jsii_type="aws-data-landing-zone.Defaults"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="budgets")
    @builtins.classmethod
    def budgets(
        cls,
        org_total: jsii.Number,
        infra_dlz: jsii.Number,
        *,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        slack: typing.Optional[typing.Union["SlackChannel", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> typing.List["DlzBudgetProps"]:
        '''Budgets for the organization.

        :param org_total: Total budget for the organization in USD.
        :param infra_dlz: Budget for this DLZ project identified by tags Owner=infra, Project=dlz in USD.
        :param emails: 
        :param slack: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb302fd608aa006f4b4741f0e5897bb244b6b7e9fe38b5a7ec48177953596cbc)
            check_type(argname="argument org_total", value=org_total, expected_type=type_hints["org_total"])
            check_type(argname="argument infra_dlz", value=infra_dlz, expected_type=type_hints["infra_dlz"])
        subscribers = BudgetSubscribers(emails=emails, slack=slack)

        return typing.cast(typing.List["DlzBudgetProps"], jsii.sinvoke(cls, "budgets", [org_total, infra_dlz, subscribers]))

    @jsii.member(jsii_name="denyServiceList")
    @builtins.classmethod
    def deny_service_list(cls) -> typing.List[builtins.str]:
        '''- List of services that are denied in the organization.'''
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "denyServiceList", []))

    @jsii.member(jsii_name="iamIdentityCenterPermissionSets")
    @builtins.classmethod
    def iam_identity_center_permission_sets(
        cls,
    ) -> typing.List["IamIdentityCenterPermissionSetProps"]:
        '''Provides the AWS managed policy ``AdministratorAccess`` and ``ReadOnlyAccess`` as permission sets.'''
        return typing.cast(typing.List["IamIdentityCenterPermissionSetProps"], jsii.sinvoke(cls, "iamIdentityCenterPermissionSets", []))

    @jsii.member(jsii_name="mandatoryTags")
    @builtins.classmethod
    def mandatory_tags(
        cls,
        *,
        budgets: typing.Sequence[typing.Union["DlzBudgetProps", typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union["MandatoryTags", typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union["DlzRegions", typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union["SecurityHubNotification", typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union["DlzTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union["NotificationDetailsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union["DeploymentPlatform", typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union["IamIdentityCenterProps", typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union["IamPolicyPermissionsBoundaryProps", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["Network", typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> typing.List["DlzTag"]:
        '''- Mandatory tags for the organization.

        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        return typing.cast(typing.List["DlzTag"], jsii.sinvoke(cls, "mandatoryTags", [props]))

    @jsii.member(jsii_name="rootControls")
    @builtins.classmethod
    def root_controls(cls) -> typing.List["DlzControlTowerStandardControls"]:
        '''Control Tower Controls applied to all the OUs in the organization.'''
        return typing.cast(typing.List["DlzControlTowerStandardControls"], jsii.sinvoke(cls, "rootControls", []))

    @jsii.member(jsii_name="vpcClassB3Private3Public")
    @builtins.classmethod
    def vpc_class_b3_private3_public(
        cls,
        third_octet_mask: jsii.Number,
        region: "Region",
    ) -> "DlzVpcProps":
        '''Creates a VPC configuration with 2 route tables, one used as public and the other private, each with 3 subnets.

        Each subnet has a /19 CIDR block. The VPC CIDR is ``10.${thirdOctetMask}.0.0/16``
        There will be remaining space:

        - 10.x.192.0/19
        - 10.x.224.0/19

        :param third_octet_mask: the third octet of the VPC CIDR.
        :param region: the region where the VPC will be created.

        :return: a VPC configuration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ebc403b477ed4f716493d8c533b5abe6b553a5f790054e162427f71d32ddad)
            check_type(argname="argument third_octet_mask", value=third_octet_mask, expected_type=type_hints["third_octet_mask"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast("DlzVpcProps", jsii.sinvoke(cls, "vpcClassB3Private3Public", [third_octet_mask, region]))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DeploymentPlatform",
    jsii_struct_bases=[],
    name_mapping={"git_hub": "gitHub"},
)
class DeploymentPlatform:
    def __init__(
        self,
        *,
        git_hub: typing.Optional[typing.Union["DeploymentPlatformGitHub", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param git_hub: 
        '''
        if isinstance(git_hub, dict):
            git_hub = DeploymentPlatformGitHub(**git_hub)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f044dcbb477c02103b334166b1e5bca4b76efdfa31dacc2eded0247ab4d40be7)
            check_type(argname="argument git_hub", value=git_hub, expected_type=type_hints["git_hub"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if git_hub is not None:
            self._values["git_hub"] = git_hub

    @builtins.property
    def git_hub(self) -> typing.Optional["DeploymentPlatformGitHub"]:
        result = self._values.get("git_hub")
        return typing.cast(typing.Optional["DeploymentPlatformGitHub"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentPlatform(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DeploymentPlatformGitHub",
    jsii_struct_bases=[],
    name_mapping={"references": "references"},
)
class DeploymentPlatformGitHub:
    def __init__(
        self,
        *,
        references: typing.Sequence[typing.Union["GitHubReference", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param references: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5005427f43f51b96b1589b0a588b2cfc8497aa93892aead054d80cfd827a6c87)
            check_type(argname="argument references", value=references, expected_type=type_hints["references"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "references": references,
        }

    @builtins.property
    def references(self) -> typing.List["GitHubReference"]:
        result = self._values.get("references")
        assert result is not None, "Required property 'references' is missing"
        return typing.cast(typing.List["GitHubReference"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentPlatformGitHub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzAccountNetwork",
    jsii_struct_bases=[],
    name_mapping={"dlz_account": "dlzAccount", "vpcs": "vpcs"},
)
class DlzAccountNetwork:
    def __init__(
        self,
        *,
        dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
        vpcs: typing.Sequence[typing.Union["NetworkEntityVpc", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param dlz_account: 
        :param vpcs: 
        '''
        if isinstance(dlz_account, dict):
            dlz_account = DLzAccount(**dlz_account)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512e485c7ab01d7cef0c5f99c0e820955310f24bb0020f5ceda8189e1f2f5280)
            check_type(argname="argument dlz_account", value=dlz_account, expected_type=type_hints["dlz_account"])
            check_type(argname="argument vpcs", value=vpcs, expected_type=type_hints["vpcs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dlz_account": dlz_account,
            "vpcs": vpcs,
        }

    @builtins.property
    def dlz_account(self) -> DLzAccount:
        result = self._values.get("dlz_account")
        assert result is not None, "Required property 'dlz_account' is missing"
        return typing.cast(DLzAccount, result)

    @builtins.property
    def vpcs(self) -> typing.List["NetworkEntityVpc"]:
        result = self._values.get("vpcs")
        assert result is not None, "Required property 'vpcs' is missing"
        return typing.cast(typing.List["NetworkEntityVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzAccountNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlzAccountNetworks(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzAccountNetworks",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="add")
    def add(
        self,
        dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
        *,
        address: "NetworkAddress",
        route_tables: typing.Sequence[typing.Union["NetworkEntityRouteTable", typing.Dict[builtins.str, typing.Any]]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.CfnVPC,
    ) -> None:
        '''
        :param dlz_account: -
        :param address: 
        :param route_tables: 
        :param vpc: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb530e1229f02fd59610813d10c92642a5ba4a9ecc869e8eff7c025f92b6d6b)
            check_type(argname="argument dlz_account", value=dlz_account, expected_type=type_hints["dlz_account"])
        network_entity_vpc = NetworkEntityVpc(
            address=address, route_tables=route_tables, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "add", [dlz_account, network_entity_vpc]))

    @jsii.member(jsii_name="getEntitiesForAddress")
    def get_entities_for_address(
        self,
        network_address: "NetworkAddress",
        match_on_address: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[typing.List[DlzAccountNetwork]]:
        '''Get NetworkEntities for the given ``networkAddress`` and match on the given ``matchOnAddress``.

        For example, if the
        ``networkAddress`` is a routeTable address and ``matchOnAddress`` has a value of ``vpc`` then it will return all
        NetworkEntities that have the same VPC as the ``networkAddress``. Or, if the ``matchOnAddress`` has a value of
        ``region`` then it will return all NetworkEntities that have the same VPC region as the ``networkAddress``.

        If the ``matchOnAddress`` is ``account`` then the complete NetworkEntity will be returned.
        Else, if ``matchOnAddress`` is ``region``, ``vpc``, ``routeTable`` or ``subnet`` then a partial NetworkEntity will be returned.
        The ``vpcs`` ``routeTables`` and ``subnets`` will be filtered to only include those that match the ``networkAddress``. A value of
        ``undefined`` will automatically detect the level of the ``networkAddress`` and use that as the ``matchOnAddress``.

        Example:

        Given we have these NetworkEntity[]:

        1. project-1-develop.us-east-1.default.private
        2. project-1-develop.eu-west-1.default.private
        3. project-1-production.eu-west-1.default.private

        - If the ``networkAddress`` has a ``routeTable`` address of: ``project-1-develop.us-east-1.default.private`` and the
          ``matchOnAddress`` value is **``routeTable``**. Then it will only match the **first** entry of
          ``project-1-develop.us-east-1.default.private`` and return a partial NetworkEntity with the VPC, and only
          the routeTables and subnets that have the same routeTable address.
        - If the ``networkAddress`` has the same ``routeTable`` address of: ``project-1-develop.us-east-1.default.private`` and the
          ``matchOnAddress`` value is changed to **``vpc``**. Then it will match the **first** and **second** entries
          and return the complete NetworkEntity for each.

        :param network_address: -
        :param match_on_address: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7ded183cf91cea2d37994735f20379d6769e6583eca362598f16d2dedda1ac)
            check_type(argname="argument network_address", value=network_address, expected_type=type_hints["network_address"])
            check_type(argname="argument match_on_address", value=match_on_address, expected_type=type_hints["match_on_address"])
        return typing.cast(typing.Optional[typing.List[DlzAccountNetwork]], jsii.invoke(self, "getEntitiesForAddress", [network_address, match_on_address]))


@jsii.enum(jsii_type="aws-data-landing-zone.DlzAccountType")
class DlzAccountType(enum.Enum):
    DEVELOP = "DEVELOP"
    PRODUCTION = "PRODUCTION"


class DlzBudget(metaclass=jsii.JSIIMeta, jsii_type="aws-data-landing-zone.DlzBudget"):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        amount: jsii.Number,
        name: builtins.str,
        subscribers: typing.Union[BudgetSubscribers, typing.Dict[builtins.str, typing.Any]],
        for_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param amount: 
        :param name: 
        :param subscribers: 
        :param for_tags: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f1244110d2fd7ecaf753ef011c7fa503aa48b98d70664100b5311886824052)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DlzBudgetProps(
            amount=amount, name=name, subscribers=subscribers, for_tags=for_tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cfnBudget")
    def cfn_budget(self) -> _aws_cdk_aws_budgets_ceddda9d.CfnBudget:
        return typing.cast(_aws_cdk_aws_budgets_ceddda9d.CfnBudget, jsii.get(self, "cfnBudget"))

    @builtins.property
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> _aws_cdk_aws_sns_ceddda9d.Topic:
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.Topic, jsii.get(self, "notificationTopic"))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzBudgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "amount": "amount",
        "name": "name",
        "subscribers": "subscribers",
        "for_tags": "forTags",
    },
)
class DlzBudgetProps:
    def __init__(
        self,
        *,
        amount: jsii.Number,
        name: builtins.str,
        subscribers: typing.Union[BudgetSubscribers, typing.Dict[builtins.str, typing.Any]],
        for_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param amount: 
        :param name: 
        :param subscribers: 
        :param for_tags: 
        '''
        if isinstance(subscribers, dict):
            subscribers = BudgetSubscribers(**subscribers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c79cf48597aa3bcfab58f9fd6e3cd61e3c18a49a7910a4275a6a24b93184379)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
            check_type(argname="argument for_tags", value=for_tags, expected_type=type_hints["for_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "amount": amount,
            "name": name,
            "subscribers": subscribers,
        }
        if for_tags is not None:
            self._values["for_tags"] = for_tags

    @builtins.property
    def amount(self) -> jsii.Number:
        result = self._values.get("amount")
        assert result is not None, "Required property 'amount' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscribers(self) -> BudgetSubscribers:
        result = self._values.get("subscribers")
        assert result is not None, "Required property 'subscribers' is missing"
        return typing.cast(BudgetSubscribers, result)

    @builtins.property
    def for_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("for_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzBudgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.DlzControlTowerControlFormat")
class DlzControlTowerControlFormat(enum.Enum):
    LEGACY = "LEGACY"
    STANDARD = "STANDARD"


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzControlTowerControlIdNameProps",
    jsii_struct_bases=[],
    name_mapping={"eu_west1": "euWest1", "us_east1": "usEast1"},
)
class DlzControlTowerControlIdNameProps:
    def __init__(self, *, eu_west1: builtins.str, us_east1: builtins.str) -> None:
        '''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Do not export any of the controls in the folders, they do not conform to JSII, class names are snake case caps and the controlIdName properties are also snake case caps. This will cause the JSII build to fail. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        :param eu_west1: 
        :param us_east1: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c86c3b125e32a441f79170b43d426a3dcb7c3fa6914c1b1e598564d4645f9d)
            check_type(argname="argument eu_west1", value=eu_west1, expected_type=type_hints["eu_west1"])
            check_type(argname="argument us_east1", value=us_east1, expected_type=type_hints["us_east1"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "eu_west1": eu_west1,
            "us_east1": us_east1,
        }

    @builtins.property
    def eu_west1(self) -> builtins.str:
        result = self._values.get("eu_west1")
        assert result is not None, "Required property 'eu_west1' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def us_east1(self) -> builtins.str:
        result = self._values.get("us_east1")
        assert result is not None, "Required property 'us_east1' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzControlTowerControlIdNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzControlTowerEnabledControlProps",
    jsii_struct_bases=[],
    name_mapping={
        "applied_ou": "appliedOu",
        "control": "control",
        "control_tower_account_id": "controlTowerAccountId",
        "control_tower_region": "controlTowerRegion",
        "organization_id": "organizationId",
        "tags": "tags",
    },
)
class DlzControlTowerEnabledControlProps:
    def __init__(
        self,
        *,
        applied_ou: builtins.str,
        control: "IDlzControlTowerControl",
        control_tower_account_id: builtins.str,
        control_tower_region: "Region",
        organization_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param applied_ou: 
        :param control: 
        :param control_tower_account_id: 
        :param control_tower_region: 
        :param organization_id: 
        :param tags: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f901129156101ff8fda3b28b4d50e412e0cfa7d9799278300679bd46e6d978)
            check_type(argname="argument applied_ou", value=applied_ou, expected_type=type_hints["applied_ou"])
            check_type(argname="argument control", value=control, expected_type=type_hints["control"])
            check_type(argname="argument control_tower_account_id", value=control_tower_account_id, expected_type=type_hints["control_tower_account_id"])
            check_type(argname="argument control_tower_region", value=control_tower_region, expected_type=type_hints["control_tower_region"])
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "applied_ou": applied_ou,
            "control": control,
            "control_tower_account_id": control_tower_account_id,
            "control_tower_region": control_tower_region,
            "organization_id": organization_id,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def applied_ou(self) -> builtins.str:
        result = self._values.get("applied_ou")
        assert result is not None, "Required property 'applied_ou' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control(self) -> "IDlzControlTowerControl":
        result = self._values.get("control")
        assert result is not None, "Required property 'control' is missing"
        return typing.cast("IDlzControlTowerControl", result)

    @builtins.property
    def control_tower_account_id(self) -> builtins.str:
        result = self._values.get("control_tower_account_id")
        assert result is not None, "Required property 'control_tower_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_tower_region(self) -> "Region":
        result = self._values.get("control_tower_region")
        assert result is not None, "Required property 'control_tower_region' is missing"
        return typing.cast("Region", result)

    @builtins.property
    def organization_id(self) -> builtins.str:
        result = self._values.get("organization_id")
        assert result is not None, "Required property 'organization_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzControlTowerEnabledControlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.DlzControlTowerSpecializedControls")
class DlzControlTowerSpecializedControls(enum.Enum):
    '''Controls that take parameters.'''

    CT_MULTISERVICE_PV_1 = "CT_MULTISERVICE_PV_1"


@jsii.enum(jsii_type="aws-data-landing-zone.DlzControlTowerStandardControls")
class DlzControlTowerStandardControls(enum.Enum):
    '''Controls that do not take parameters.'''

    AWS_GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS = "AWS_GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"
    AWS_GR_ENCRYPTED_VOLUMES = "AWS_GR_ENCRYPTED_VOLUMES"
    AWS_GR_RDS_INSTANCE_PUBLIC_ACCESS_CHECK = "AWS_GR_RDS_INSTANCE_PUBLIC_ACCESS_CHECK"
    AWS_GR_RDS_SNAPSHOTS_PUBLIC_PROHIBITED = "AWS_GR_RDS_SNAPSHOTS_PUBLIC_PROHIBITED"
    AWS_GR_RDS_STORAGE_ENCRYPTED = "AWS_GR_RDS_STORAGE_ENCRYPTED"
    AWS_GR_RESTRICTED_SSH = "AWS_GR_RESTRICTED_SSH"
    AWS_GR_RESTRICT_ROOT_USER = "AWS_GR_RESTRICT_ROOT_USER"
    AWS_GR_RESTRICT_ROOT_USER_ACCESS_KEYS = "AWS_GR_RESTRICT_ROOT_USER_ACCESS_KEYS"
    AWS_GR_ROOT_ACCOUNT_MFA_ENABLED = "AWS_GR_ROOT_ACCOUNT_MFA_ENABLED"
    AWS_GR_S3_BUCKET_PUBLIC_READ_PROHIBITED = "AWS_GR_S3_BUCKET_PUBLIC_READ_PROHIBITED"
    AWS_GR_S3_BUCKET_PUBLIC_WRITE_PROHIBITED = "AWS_GR_S3_BUCKET_PUBLIC_WRITE_PROHIBITED"
    SH_SECRETS_MANAGER_3 = "SH_SECRETS_MANAGER_3"


class DlzLakeFormation(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzLakeFormation",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        admins: typing.Sequence[builtins.str],
        permissions: typing.Sequence[typing.Union["LakePermission", typing.Dict[builtins.str, typing.Any]]],
        region: "Region",
        tags: typing.Sequence[typing.Union["LFTagSharable", typing.Dict[builtins.str, typing.Any]]],
        cross_account_version: typing.Optional[jsii.Number] = None,
        hybrid_mode: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param admins: A list of strings representing the IAM role ARNs.
        :param permissions: A list of permission settings, specifying which Lake Formation permissions apply to which principals.
        :param region: The region where LakeFormation will be created in.
        :param tags: A list of Lake Formation tags that can be shared across accounts and principals.
        :param cross_account_version: OPTIONAL - Version for cross-account data sharing. Defaults to ``4``. Read more {@link https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account.html here}.
        :param hybrid_mode: OPTIONAL - Select ``true`` to use both IAM and Lake Formation for data access, or ``false`` to use Lake Formation only. Defaults to ``false``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58099e8819e666b11f3bb86b027f9ee73dd9c920541175f77b5cf7f83bb3221b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        lf_props = DlzLakeFormationProps(
            admins=admins,
            permissions=permissions,
            region=region,
            tags=tags,
            cross_account_version=cross_account_version,
            hybrid_mode=hybrid_mode,
        )

        jsii.create(self.__class__, self, [scope, id, lf_props])


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzLakeFormationProps",
    jsii_struct_bases=[],
    name_mapping={
        "admins": "admins",
        "permissions": "permissions",
        "region": "region",
        "tags": "tags",
        "cross_account_version": "crossAccountVersion",
        "hybrid_mode": "hybridMode",
    },
)
class DlzLakeFormationProps:
    def __init__(
        self,
        *,
        admins: typing.Sequence[builtins.str],
        permissions: typing.Sequence[typing.Union["LakePermission", typing.Dict[builtins.str, typing.Any]]],
        region: "Region",
        tags: typing.Sequence[typing.Union["LFTagSharable", typing.Dict[builtins.str, typing.Any]]],
        cross_account_version: typing.Optional[jsii.Number] = None,
        hybrid_mode: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param admins: A list of strings representing the IAM role ARNs.
        :param permissions: A list of permission settings, specifying which Lake Formation permissions apply to which principals.
        :param region: The region where LakeFormation will be created in.
        :param tags: A list of Lake Formation tags that can be shared across accounts and principals.
        :param cross_account_version: OPTIONAL - Version for cross-account data sharing. Defaults to ``4``. Read more {@link https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account.html here}.
        :param hybrid_mode: OPTIONAL - Select ``true`` to use both IAM and Lake Formation for data access, or ``false`` to use Lake Formation only. Defaults to ``false``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b953472db56618beed88515ddf1867ef2ae2d9efaf7e48fe25f5c307a8c39f27)
            check_type(argname="argument admins", value=admins, expected_type=type_hints["admins"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument cross_account_version", value=cross_account_version, expected_type=type_hints["cross_account_version"])
            check_type(argname="argument hybrid_mode", value=hybrid_mode, expected_type=type_hints["hybrid_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admins": admins,
            "permissions": permissions,
            "region": region,
            "tags": tags,
        }
        if cross_account_version is not None:
            self._values["cross_account_version"] = cross_account_version
        if hybrid_mode is not None:
            self._values["hybrid_mode"] = hybrid_mode

    @builtins.property
    def admins(self) -> typing.List[builtins.str]:
        '''A list of strings representing the IAM role ARNs.'''
        result = self._values.get("admins")
        assert result is not None, "Required property 'admins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.List["LakePermission"]:
        '''A list of permission settings, specifying which Lake Formation permissions apply to which principals.'''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast(typing.List["LakePermission"], result)

    @builtins.property
    def region(self) -> "Region":
        '''The region where LakeFormation will be created in.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast("Region", result)

    @builtins.property
    def tags(self) -> typing.List["LFTagSharable"]:
        '''A list of Lake Formation tags that can be shared across accounts and principals.'''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.List["LFTagSharable"], result)

    @builtins.property
    def cross_account_version(self) -> typing.Optional[jsii.Number]:
        '''OPTIONAL - Version for cross-account data sharing.

        Defaults to ``4``. Read more {@link https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account.html here}.
        '''
        result = self._values.get("cross_account_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hybrid_mode(self) -> typing.Optional[builtins.bool]:
        '''OPTIONAL - Select ``true`` to use both IAM and Lake Formation for data access, or ``false`` to use Lake Formation only.

        Defaults to ``false``.

        :note:

        ``false`` is currently not working due to issue with AWS API.
        You will have do disable hybrid mode manually via the AWS console.
        See {@link https://github.com/pulumi/pulumi-aws/issues/4366}
        '''
        result = self._values.get("hybrid_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzLakeFormationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzRegions",
    jsii_struct_bases=[],
    name_mapping={"global_": "global", "regional": "regional"},
)
class DlzRegions:
    def __init__(
        self,
        *,
        global_: "Region",
        regional: typing.Sequence["Region"],
    ) -> None:
        '''
        :param global_: Also known as the Home region for Control Tower.
        :param regional: The other regions to support (do not specify the global region again).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8690f9a9ede108c6bcdaf9ac39351278b758b89f49947a520acb7a43d28e996)
            check_type(argname="argument global_", value=global_, expected_type=type_hints["global_"])
            check_type(argname="argument regional", value=regional, expected_type=type_hints["regional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "global_": global_,
            "regional": regional,
        }

    @builtins.property
    def global_(self) -> "Region":
        '''Also known as the Home region for Control Tower.'''
        result = self._values.get("global_")
        assert result is not None, "Required property 'global_' is missing"
        return typing.cast("Region", result)

    @builtins.property
    def regional(self) -> typing.List["Region"]:
        '''The other regions to support (do not specify the global region again).'''
        result = self._values.get("regional")
        assert result is not None, "Required property 'regional' is missing"
        return typing.cast(typing.List["Region"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzRegions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzRouteTableProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "subnets": "subnets"},
)
class DlzRouteTableProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        subnets: typing.Sequence[typing.Union["DlzSubnetProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param name: 
        :param subnets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d550fdadc16deef3c3fa519fc8fe6ae66ec1100359faff47b2cabc491962abce)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "subnets": subnets,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnets(self) -> typing.List["DlzSubnetProps"]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List["DlzSubnetProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzRouteTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzServiceControlPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "statements": "statements",
        "description": "description",
        "tags": "tags",
        "target_ids": "targetIds",
    },
)
class DlzServiceControlPolicyProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        statements: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: 
        :param statements: 
        :param description: 
        :param tags: 
        :param target_ids: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339e74dad0d62fcf661f597315cddbc97479e01ae0aac9a889b70b3f7530a7f7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_ids", value=target_ids, expected_type=type_hints["target_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "statements": statements,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags
        if target_ids is not None:
            self._values["target_ids"] = target_ids

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statements(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        result = self._values.get("statements")
        assert result is not None, "Required property 'statements' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("target_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzServiceControlPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlzSsmReader(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzSsmReader",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getValue")
    @builtins.classmethod
    def get_value(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        account_id: builtins.str,
        region: builtins.str,
        name: builtins.str,
        fetch_type: typing.Optional[builtins.str] = None,
        with_decryption: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''Get the value of an SSM Parameter Store value.

        Fetch type ``always`` will always fetch the value from SSM Parameter Store, this will produce a CDK diff every time.
        Fetch type ``value-change`` will fetch the value from SSM Parameter Store only when the value changes, this will not
        produce a CDK diff every time.

        :param scope: -
        :param id: -
        :param account_id: -
        :param region: -
        :param name: -
        :param fetch_type: -
        :param with_decryption: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a750ebf35f5b18890d68a60379e4fd4a6623af7c34f4dfc5976df7b7e216728)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument fetch_type", value=fetch_type, expected_type=type_hints["fetch_type"])
            check_type(argname="argument with_decryption", value=with_decryption, expected_type=type_hints["with_decryption"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getValue", [scope, id, account_id, region, name, fetch_type, with_decryption]))


class DlzSsmReaderStackCache(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzSsmReaderStackCache",
):
    '''Get the value of an SSM Parameter Store value.

    This method will reuse the same CustomResource, reducing the number
    of lookups to the same resource within a stack.
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getValue")
    def get_value(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        account_id: builtins.str,
        region: builtins.str,
        name: builtins.str,
        fetch_type: typing.Optional[builtins.str] = None,
        with_decryption: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''Fetch type ``always`` will always fetch the value from SSM Parameter Store, this will produce a CDK diff every time.

        Fetch type ``value-change`` will fetch the value from SSM Parameter Store only when the value changes, this will not
        produce a CDK diff every time.

        :param scope: -
        :param id: -
        :param account_id: -
        :param region: -
        :param name: -
        :param fetch_type: -
        :param with_decryption: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff738bdc23336d5dfb4f61d6f358f5b502a9b9117a546ddb1014ac82b15f473e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument fetch_type", value=fetch_type, expected_type=type_hints["fetch_type"])
            check_type(argname="argument with_decryption", value=with_decryption, expected_type=type_hints["with_decryption"])
        return typing.cast(builtins.str, jsii.invoke(self, "getValue", [scope, id, account_id, region, name, fetch_type, with_decryption]))


class DlzStack(
    _cdk_express_pipeline_9801c4a1.ExpressStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union["DlzStackNameProps", typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    ) -> None:
        '''
        :param scope: -
        :param env: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5675fcb2f9b9558df55bcbabc917f8c3af2fd22e59753e170f23a892fab52571)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = DlzStackProps(env=env, name=name, stage=stage)

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="exportValue")
    def export_value(
        self,
        exported_value: typing.Any,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Create a CloudFormation Export for a string value.

        Returns a string representing the corresponding Fn.importValue() expression for this Export. You can control the name for the export by passing the name option.

        If you don’t supply a value for name, the value you’re exporting must be a Resource attribute (for example: bucket.bucketName) and it will be given the same name as the automatic cross-stack reference that would be created if you used the attribute in another Stack.

        One of the uses for this method is to remove the relationship between two Stacks established by automatic cross-stack references. It will temporarily ensure that the CloudFormation Export still exists while you remove the reference from the consuming stack. After that, you can remove the resource and the manual export.

        :param exported_value: -
        :param description: The description of the outputs. Default: - No description
        :param name: The name of the export to create. Default: - A name is automatically chosen
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44f8fc940b0c8025f281d43de49eb64ce0e725bde84b7c499e42605259bd239)
            check_type(argname="argument exported_value", value=exported_value, expected_type=type_hints["exported_value"])
        options = _aws_cdk_ceddda9d.ExportValueOptions(
            description=description, name=name
        )

        return typing.cast(builtins.str, jsii.invoke(self, "exportValue", [exported_value, options]))

    @jsii.member(jsii_name="resourceName")
    def resource_name(self, resource_id: builtins.str) -> builtins.str:
        '''Create unique ResourceNames.

        :param resource_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7aaacd505d6d9c4f34e64a62dc72f113097deb45d69c02f0c8ea41859b7957)
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "resourceName", [resource_id]))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzStackNameProps",
    jsii_struct_bases=[],
    name_mapping={
        "region": "region",
        "stack": "stack",
        "account": "account",
        "ou": "ou",
    },
)
class DlzStackNameProps:
    def __init__(
        self,
        *,
        region: builtins.str,
        stack: builtins.str,
        account: typing.Optional[builtins.str] = None,
        ou: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param region: 
        :param stack: 
        :param account: 
        :param ou: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54aa0affd8f5d154af48a1b55ba11c9f04d5e896247b3e19d65cedecb9499af)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument ou", value=ou, expected_type=type_hints["ou"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region": region,
            "stack": stack,
        }
        if account is not None:
            self._values["account"] = account
        if ou is not None:
            self._values["ou"] = ou

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack(self) -> builtins.str:
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ou(self) -> typing.Optional[builtins.str]:
        result = self._values.get("ou")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzStackNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzStackProps",
    jsii_struct_bases=[],
    name_mapping={"env": "env", "name": "name", "stage": "stage"},
)
class DlzStackProps:
    def __init__(
        self,
        *,
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    ) -> None:
        '''
        :param env: 
        :param name: 
        :param stage: 
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if isinstance(name, dict):
            name = DlzStackNameProps(**name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ced4c8941535fc8ecdb8829ab9e3d868f46668eac861f5eeee5eab8121dde11)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env": env,
            "name": name,
            "stage": stage,
        }

    @builtins.property
    def env(self) -> _aws_cdk_ceddda9d.Environment:
        result = self._values.get("env")
        assert result is not None, "Required property 'env' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Environment, result)

    @builtins.property
    def name(self) -> DlzStackNameProps:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(DlzStackNameProps, result)

    @builtins.property
    def stage(self) -> _cdk_express_pipeline_9801c4a1.ExpressStage:
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(_cdk_express_pipeline_9801c4a1.ExpressStage, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzSubnetProps",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr", "name": "name", "az": "az"},
)
class DlzSubnetProps:
    def __init__(
        self,
        *,
        cidr: builtins.str,
        name: builtins.str,
        az: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cidr: The CIDR block of the subnet.
        :param name: The name of the subnet, must be unique within the routeTable.
        :param az: Optional. The Availability Zone of the subnet, if not specified a random AZ will be selected
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14071e2e7b1beecaffa587aa061908789508df30ab0a2c5904b8b455202bbcf7)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument az", value=az, expected_type=type_hints["az"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "name": name,
        }
        if az is not None:
            self._values["az"] = az

    @builtins.property
    def cidr(self) -> builtins.str:
        '''The CIDR block of the subnet.'''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the subnet, must be unique within the routeTable.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def az(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Availability Zone of the subnet, if not specified a random AZ will be selected
        '''
        result = self._values.get("az")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzSubnetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzTag",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class DlzTag:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: 
        :param values: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f26963db2ae43eedfd364e6a59a2cbde80c46ae927a969354aef6437e213b3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzTagPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "policy_tags": "policyTags",
        "description": "description",
        "tags": "tags",
        "target_ids": "targetIds",
    },
)
class DlzTagPolicyProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        policy_tags: typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: 
        :param policy_tags: 
        :param description: 
        :param tags: 
        :param target_ids: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33502afb73bb9e9b8b9242e3297ae17f0b78d08d6c168ea7509982cefcbe648c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_tags", value=policy_tags, expected_type=type_hints["policy_tags"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_ids", value=target_ids, expected_type=type_hints["target_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_tags": policy_tags,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags
        if target_ids is not None:
            self._values["target_ids"] = target_ids

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_tags(self) -> typing.List[DlzTag]:
        result = self._values.get("policy_tags")
        assert result is not None, "Required property 'policy_tags' is missing"
        return typing.cast(typing.List[DlzTag], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("target_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzTagPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlzVpc(metaclass=jsii.JSIIMeta, jsii_type="aws-data-landing-zone.DlzVpc"):
    def __init__(
        self,
        dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
        dlz_stack: DlzStack,
        dlz_vpc: typing.Union["DlzVpcProps", typing.Dict[builtins.str, typing.Any]],
        network_nats: typing.Optional[typing.Sequence[typing.Union["NetworkNat", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param dlz_account: -
        :param dlz_stack: -
        :param dlz_vpc: -
        :param network_nats: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc864233a41939de528d6ea19dfa0d68821e458d7a785701873c2750716cf96)
            check_type(argname="argument dlz_account", value=dlz_account, expected_type=type_hints["dlz_account"])
            check_type(argname="argument dlz_stack", value=dlz_stack, expected_type=type_hints["dlz_stack"])
            check_type(argname="argument dlz_vpc", value=dlz_vpc, expected_type=type_hints["dlz_vpc"])
            check_type(argname="argument network_nats", value=network_nats, expected_type=type_hints["network_nats"])
        jsii.create(self.__class__, self, [dlz_account, dlz_stack, dlz_vpc, network_nats])

    @builtins.property
    @jsii.member(jsii_name="networkEntityVpc")
    def network_entity_vpc(self) -> "NetworkEntityVpc":
        return typing.cast("NetworkEntityVpc", jsii.get(self, "networkEntityVpc"))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DlzVpcProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr": "cidr",
        "name": "name",
        "region": "region",
        "route_tables": "routeTables",
    },
)
class DlzVpcProps:
    def __init__(
        self,
        *,
        cidr: builtins.str,
        name: builtins.str,
        region: "Region",
        route_tables: typing.Sequence[typing.Union[DlzRouteTableProps, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param cidr: The CIDR block of the VPC.
        :param name: The name of the VPC, must be unique within the region.
        :param region: The region where the VPC will be created.
        :param route_tables: The route tables to be created in the VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7486cc9fc6f87493ab652a743b15c22d0bd06d03597e324eabccf3ec18b63a40)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument route_tables", value=route_tables, expected_type=type_hints["route_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "name": name,
            "region": region,
            "route_tables": route_tables,
        }

    @builtins.property
    def cidr(self) -> builtins.str:
        '''The CIDR block of the VPC.'''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the VPC, must be unique within the region.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> "Region":
        '''The region where the VPC will be created.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast("Region", result)

    @builtins.property
    def route_tables(self) -> typing.List[DlzRouteTableProps]:
        '''The route tables to be created in the VPC.'''
        result = self._values.get("route_tables")
        assert result is not None, "Required property 'route_tables' is missing"
        return typing.cast(typing.List[DlzRouteTableProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlzVpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.ForceNoPythonArgumentLifting",
    jsii_struct_bases=[],
    name_mapping={},
)
class ForceNoPythonArgumentLifting:
    def __init__(self) -> None:
        '''This is a type that is used to force JSII to not "argument lift" the arguments.

        Use it as the last argument of
        user facing function that you want to prevent argument lifting on. Example::

           public async diffAll(props: DataLandingZoneProps, _: ForceNoPythonArgumentLifting = {})

           export class DataLandingZone {
             constructor(app: App, props: DataLandingZoneProps, _: ForceNoPythonArgumentLifting = {}) {

        Then just call the function/constructor and "forget about the last parameter". It's an ugly hack but acceptable for
        the time being. Tracking issue: https://github.com/aws/jsii/issues/4721
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForceNoPythonArgumentLifting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.GitHubReference",
    jsii_struct_bases=[],
    name_mapping={"owner": "owner", "repo": "repo", "filter": "filter"},
)
class GitHubReference:
    def __init__(
        self,
        *,
        owner: builtins.str,
        repo: builtins.str,
        filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param owner: The owner of the GitHub repository.
        :param repo: The repository name.
        :param filter: For a complete list of filters see https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect#understanding-the-oidc-token. Some common Examples: - specific environment ``environment:ENVIRONMENT-NAME`` - specific branch ``ref:refs/heads/BRANCH-NAME`` - specific tag ``ref:refs/tags/TAG-NAME`` - only PRs ``pull_request`` A ``*`` can be used for most parts like ``ENVIRONMENT-NAME``, ``BRANCH-NAME``, ``TAG-NAME``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e0ef86c3068d0b854aa83d4f1b59acc0d2885df25802c71f8b6205c3f03497)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repo", value=repo, expected_type=type_hints["repo"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner": owner,
            "repo": repo,
        }
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def owner(self) -> builtins.str:
        '''The owner of the GitHub repository.'''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo(self) -> builtins.str:
        '''The repository name.'''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''For a complete list of filters see https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect#understanding-the-oidc-token.

        Some common Examples:

        - specific environment ``environment:ENVIRONMENT-NAME``
        - specific branch ``ref:refs/heads/BRANCH-NAME``
        - specific tag ``ref:refs/tags/TAG-NAME``
        - only PRs ``pull_request``

        A ``*`` can be used for most parts like ``ENVIRONMENT-NAME``, ``BRANCH-NAME``, ``TAG-NAME``
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.GlobalVariables",
    jsii_struct_bases=[],
    name_mapping={
        "dlz_account_networks": "dlzAccountNetworks",
        "ncp1": "ncp1",
        "ncp2": "ncp2",
        "ncp3": "ncp3",
    },
)
class GlobalVariables:
    def __init__(
        self,
        *,
        dlz_account_networks: DlzAccountNetworks,
        ncp1: typing.Union["GlobalVariablesNcp1", typing.Dict[builtins.str, typing.Any]],
        ncp2: typing.Union["GlobalVariablesNcp2", typing.Dict[builtins.str, typing.Any]],
        ncp3: typing.Union["GlobalVariablesNcp3", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dlz_account_networks: 
        :param ncp1: 
        :param ncp2: 
        :param ncp3: 
        '''
        if isinstance(ncp1, dict):
            ncp1 = GlobalVariablesNcp1(**ncp1)
        if isinstance(ncp2, dict):
            ncp2 = GlobalVariablesNcp2(**ncp2)
        if isinstance(ncp3, dict):
            ncp3 = GlobalVariablesNcp3(**ncp3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0155b91147435bd7f83ea1bf2a259a429f49c29f38904ac043ceb3f22c1303cf)
            check_type(argname="argument dlz_account_networks", value=dlz_account_networks, expected_type=type_hints["dlz_account_networks"])
            check_type(argname="argument ncp1", value=ncp1, expected_type=type_hints["ncp1"])
            check_type(argname="argument ncp2", value=ncp2, expected_type=type_hints["ncp2"])
            check_type(argname="argument ncp3", value=ncp3, expected_type=type_hints["ncp3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dlz_account_networks": dlz_account_networks,
            "ncp1": ncp1,
            "ncp2": ncp2,
            "ncp3": ncp3,
        }

    @builtins.property
    def dlz_account_networks(self) -> DlzAccountNetworks:
        result = self._values.get("dlz_account_networks")
        assert result is not None, "Required property 'dlz_account_networks' is missing"
        return typing.cast(DlzAccountNetworks, result)

    @builtins.property
    def ncp1(self) -> "GlobalVariablesNcp1":
        result = self._values.get("ncp1")
        assert result is not None, "Required property 'ncp1' is missing"
        return typing.cast("GlobalVariablesNcp1", result)

    @builtins.property
    def ncp2(self) -> "GlobalVariablesNcp2":
        result = self._values.get("ncp2")
        assert result is not None, "Required property 'ncp2' is missing"
        return typing.cast("GlobalVariablesNcp2", result)

    @builtins.property
    def ncp3(self) -> "GlobalVariablesNcp3":
        result = self._values.get("ncp3")
        assert result is not None, "Required property 'ncp3' is missing"
        return typing.cast("GlobalVariablesNcp3", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.GlobalVariablesNcp1",
    jsii_struct_bases=[],
    name_mapping={"vpc_peering_role_keys": "vpcPeeringRoleKeys"},
)
class GlobalVariablesNcp1:
    def __init__(self, *, vpc_peering_role_keys: typing.Sequence[builtins.str]) -> None:
        '''
        :param vpc_peering_role_keys: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3037077464cb9af3024fd58894d08534c6be30f5e5a8f73f218bf251669e4c0c)
            check_type(argname="argument vpc_peering_role_keys", value=vpc_peering_role_keys, expected_type=type_hints["vpc_peering_role_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_peering_role_keys": vpc_peering_role_keys,
        }

    @builtins.property
    def vpc_peering_role_keys(self) -> typing.List[builtins.str]:
        result = self._values.get("vpc_peering_role_keys")
        assert result is not None, "Required property 'vpc_peering_role_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalVariablesNcp1(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.GlobalVariablesNcp2",
    jsii_struct_bases=[],
    name_mapping={
        "owner_vpc_ids": "ownerVpcIds",
        "peering_connections": "peeringConnections",
        "peering_role_arns": "peeringRoleArns",
    },
)
class GlobalVariablesNcp2:
    def __init__(
        self,
        *,
        owner_vpc_ids: DlzSsmReaderStackCache,
        peering_connections: typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.CfnVPCPeeringConnection],
        peering_role_arns: DlzSsmReaderStackCache,
    ) -> None:
        '''
        :param owner_vpc_ids: 
        :param peering_connections: 
        :param peering_role_arns: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de59b0f0ec5b2ff47010678d6b47a111ea30c0f55007d5eeba3b0b95b12354b8)
            check_type(argname="argument owner_vpc_ids", value=owner_vpc_ids, expected_type=type_hints["owner_vpc_ids"])
            check_type(argname="argument peering_connections", value=peering_connections, expected_type=type_hints["peering_connections"])
            check_type(argname="argument peering_role_arns", value=peering_role_arns, expected_type=type_hints["peering_role_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner_vpc_ids": owner_vpc_ids,
            "peering_connections": peering_connections,
            "peering_role_arns": peering_role_arns,
        }

    @builtins.property
    def owner_vpc_ids(self) -> DlzSsmReaderStackCache:
        result = self._values.get("owner_vpc_ids")
        assert result is not None, "Required property 'owner_vpc_ids' is missing"
        return typing.cast(DlzSsmReaderStackCache, result)

    @builtins.property
    def peering_connections(
        self,
    ) -> typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.CfnVPCPeeringConnection]:
        result = self._values.get("peering_connections")
        assert result is not None, "Required property 'peering_connections' is missing"
        return typing.cast(typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.CfnVPCPeeringConnection], result)

    @builtins.property
    def peering_role_arns(self) -> DlzSsmReaderStackCache:
        result = self._values.get("peering_role_arns")
        assert result is not None, "Required property 'peering_role_arns' is missing"
        return typing.cast(DlzSsmReaderStackCache, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalVariablesNcp2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.GlobalVariablesNcp3",
    jsii_struct_bases=[],
    name_mapping={
        "route_tables_ssm_cache": "routeTablesSsmCache",
        "vpc_peering_connection_ids": "vpcPeeringConnectionIds",
    },
)
class GlobalVariablesNcp3:
    def __init__(
        self,
        *,
        route_tables_ssm_cache: DlzSsmReaderStackCache,
        vpc_peering_connection_ids: DlzSsmReaderStackCache,
    ) -> None:
        '''
        :param route_tables_ssm_cache: 
        :param vpc_peering_connection_ids: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87b00f355d35a5e2dba8d710842de061a9db204d166101735f3cdac4cb7eb73)
            check_type(argname="argument route_tables_ssm_cache", value=route_tables_ssm_cache, expected_type=type_hints["route_tables_ssm_cache"])
            check_type(argname="argument vpc_peering_connection_ids", value=vpc_peering_connection_ids, expected_type=type_hints["vpc_peering_connection_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "route_tables_ssm_cache": route_tables_ssm_cache,
            "vpc_peering_connection_ids": vpc_peering_connection_ids,
        }

    @builtins.property
    def route_tables_ssm_cache(self) -> DlzSsmReaderStackCache:
        result = self._values.get("route_tables_ssm_cache")
        assert result is not None, "Required property 'route_tables_ssm_cache' is missing"
        return typing.cast(DlzSsmReaderStackCache, result)

    @builtins.property
    def vpc_peering_connection_ids(self) -> DlzSsmReaderStackCache:
        result = self._values.get("vpc_peering_connection_ids")
        assert result is not None, "Required property 'vpc_peering_connection_ids' is missing"
        return typing.cast(DlzSsmReaderStackCache, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalVariablesNcp3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-data-landing-zone.IDlzControlTowerControl")
class IDlzControlTowerControl(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="controlFriendlyName")
    def control_friendly_name(
        self,
    ) -> typing.Union[DlzControlTowerStandardControls, DlzControlTowerSpecializedControls]:
        '''The short name of the control, example: AWS-GR_ENCRYPTED_VOLUMES.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="controlIdName")
    def control_id_name(self) -> DlzControlTowerControlIdNameProps:
        '''The control ID name used to construct the controlIdentifier, example: AWS-GR_ENCRYPTED_VOLUMES This can differ from the controlFriendlyName for newer controls.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of the control.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="externalLink")
    def external_link(self) -> builtins.str:
        '''External link to the control documentation.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> DlzControlTowerControlFormat:
        '''The format of the control, LEGACY or STANDARD LEGACY controls include the control name in the controlIdentifier STANDARD controls do not include the control name in the controlIdentifier and can not be applied to the Security OU.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Optional parameters for the control.'''
        ...


class _IDlzControlTowerControlProxy:
    __jsii_type__: typing.ClassVar[str] = "aws-data-landing-zone.IDlzControlTowerControl"

    @builtins.property
    @jsii.member(jsii_name="controlFriendlyName")
    def control_friendly_name(
        self,
    ) -> typing.Union[DlzControlTowerStandardControls, DlzControlTowerSpecializedControls]:
        '''The short name of the control, example: AWS-GR_ENCRYPTED_VOLUMES.'''
        return typing.cast(typing.Union[DlzControlTowerStandardControls, DlzControlTowerSpecializedControls], jsii.get(self, "controlFriendlyName"))

    @builtins.property
    @jsii.member(jsii_name="controlIdName")
    def control_id_name(self) -> DlzControlTowerControlIdNameProps:
        '''The control ID name used to construct the controlIdentifier, example: AWS-GR_ENCRYPTED_VOLUMES This can differ from the controlFriendlyName for newer controls.'''
        return typing.cast(DlzControlTowerControlIdNameProps, jsii.get(self, "controlIdName"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of the control.'''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="externalLink")
    def external_link(self) -> builtins.str:
        '''External link to the control documentation.'''
        return typing.cast(builtins.str, jsii.get(self, "externalLink"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> DlzControlTowerControlFormat:
        '''The format of the control, LEGACY or STANDARD LEGACY controls include the control name in the controlIdentifier STANDARD controls do not include the control name in the controlIdentifier and can not be applied to the Security OU.'''
        return typing.cast(DlzControlTowerControlFormat, jsii.get(self, "format"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Optional parameters for the control.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "parameters"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDlzControlTowerControl).__jsii_proxy_class__ = lambda : _IDlzControlTowerControlProxy


@jsii.interface(jsii_type="aws-data-landing-zone.IReportResource")
class IReportResource(typing_extensions.Protocol):
    '''Behavioral, used with Inheritance.'''

    @builtins.property
    @jsii.member(jsii_name="reportResource")
    def report_resource(self) -> "ReportResource":
        ...


class _IReportResourceProxy:
    '''Behavioral, used with Inheritance.'''

    __jsii_type__: typing.ClassVar[str] = "aws-data-landing-zone.IReportResource"

    @builtins.property
    @jsii.member(jsii_name="reportResource")
    def report_resource(self) -> "ReportResource":
        return typing.cast("ReportResource", jsii.get(self, "reportResource"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReportResource).__jsii_proxy_class__ = lambda : _IReportResourceProxy


@jsii.enum(jsii_type="aws-data-landing-zone.IamIdentityAccounts")
class IamIdentityAccounts(enum.Enum):
    ROOT = "ROOT"
    SECURITY_LOG = "SECURITY_LOG"
    SECURITY_AUDIT = "SECURITY_AUDIT"


class IamIdentityCenter(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.IamIdentityCenter",
):
    '''The IAM Identity Center.'''

    def __init__(
        self,
        dlz_stack: DlzStack,
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        *,
        arn: builtins.str,
        id: builtins.str,
        store_id: builtins.str,
        access_groups: typing.Optional[typing.Sequence[typing.Union["IamIdentityCenterAccessGroupProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        permission_sets: typing.Optional[typing.Sequence[typing.Union["IamIdentityCenterPermissionSetProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        users: typing.Optional[typing.Sequence[typing.Union["IdentityStoreUserProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param dlz_stack: -
        :param organization: -
        :param arn: 
        :param id: 
        :param store_id: 
        :param access_groups: 
        :param permission_sets: 
        :param users: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6069fd6f28c7b582fe6a9e53e2daece20c8d6fd0480e8da5b1cdd6d28b6de979)
            check_type(argname="argument dlz_stack", value=dlz_stack, expected_type=type_hints["dlz_stack"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
        iam_identity_center = IamIdentityCenterProps(
            arn=arn,
            id=id,
            store_id=store_id,
            access_groups=access_groups,
            permission_sets=permission_sets,
            users=users,
        )

        jsii.create(self.__class__, self, [dlz_stack, organization, iam_identity_center])


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IamIdentityCenterAccessGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_names": "accountNames",
        "name": "name",
        "permission_set_name": "permissionSetName",
        "description": "description",
        "user_names": "userNames",
    },
)
class IamIdentityCenterAccessGroupProps:
    def __init__(
        self,
        *,
        account_names: typing.Sequence[builtins.str],
        name: builtins.str,
        permission_set_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''An access group in the IAM Identity Center.

        :param account_names: 
        :param name: 
        :param permission_set_name: 
        :param description: 
        :param user_names: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3737a13593afab1af80a835eca002d158ea1d0ddd47b2f5b453501c060ce6d9d)
            check_type(argname="argument account_names", value=account_names, expected_type=type_hints["account_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permission_set_name", value=permission_set_name, expected_type=type_hints["permission_set_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument user_names", value=user_names, expected_type=type_hints["user_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_names": account_names,
            "name": name,
            "permission_set_name": permission_set_name,
        }
        if description is not None:
            self._values["description"] = description
        if user_names is not None:
            self._values["user_names"] = user_names

    @builtins.property
    def account_names(self) -> typing.List[builtins.str]:
        result = self._values.get("account_names")
        assert result is not None, "Required property 'account_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission_set_name(self) -> builtins.str:
        result = self._values.get("permission_set_name")
        assert result is not None, "Required property 'permission_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_names(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("user_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamIdentityCenterAccessGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamIdentityCenterGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.IamIdentityCenterGroup",
):
    '''A group of users in the IAM Identity Center.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        accounts: typing.Sequence[builtins.str],
        identity_store_id: builtins.str,
        name: builtins.str,
        permission_set: _aws_cdk_aws_sso_ceddda9d.CfnPermissionSet,
        sso_arn: builtins.str,
        users: typing.Sequence[typing.Union["IamIdentityCenterGroupUser", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param accounts: 
        :param identity_store_id: 
        :param name: 
        :param permission_set: 
        :param sso_arn: 
        :param users: 
        :param description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf381d25cf7d4c2cc6a890f27f3ff8112a5d20d026d99608a183065947d17d01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IamIdentityCenterGroupProps(
            accounts=accounts,
            identity_store_id=identity_store_id,
            name=name,
            permission_set=permission_set,
            sso_arn=sso_arn,
            users=users,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IamIdentityCenterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "accounts": "accounts",
        "identity_store_id": "identityStoreId",
        "name": "name",
        "permission_set": "permissionSet",
        "sso_arn": "ssoArn",
        "users": "users",
        "description": "description",
    },
)
class IamIdentityCenterGroupProps:
    def __init__(
        self,
        *,
        accounts: typing.Sequence[builtins.str],
        identity_store_id: builtins.str,
        name: builtins.str,
        permission_set: _aws_cdk_aws_sso_ceddda9d.CfnPermissionSet,
        sso_arn: builtins.str,
        users: typing.Sequence[typing.Union["IamIdentityCenterGroupUser", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''A group of users in the IAM Identity Center.

        :param accounts: 
        :param identity_store_id: 
        :param name: 
        :param permission_set: 
        :param sso_arn: 
        :param users: 
        :param description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cffd81a956e1c484ae6938e53f3059990c30fd868bcef8cc2f8bcdf02d36f8)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permission_set", value=permission_set, expected_type=type_hints["permission_set"])
            check_type(argname="argument sso_arn", value=sso_arn, expected_type=type_hints["sso_arn"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "identity_store_id": identity_store_id,
            "name": name,
            "permission_set": permission_set,
            "sso_arn": sso_arn,
            "users": users,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def accounts(self) -> typing.List[builtins.str]:
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def identity_store_id(self) -> builtins.str:
        result = self._values.get("identity_store_id")
        assert result is not None, "Required property 'identity_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission_set(self) -> _aws_cdk_aws_sso_ceddda9d.CfnPermissionSet:
        result = self._values.get("permission_set")
        assert result is not None, "Required property 'permission_set' is missing"
        return typing.cast(_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet, result)

    @builtins.property
    def sso_arn(self) -> builtins.str:
        result = self._values.get("sso_arn")
        assert result is not None, "Required property 'sso_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def users(self) -> typing.List["IamIdentityCenterGroupUser"]:
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.List["IamIdentityCenterGroupUser"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamIdentityCenterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IamIdentityCenterGroupUser",
    jsii_struct_bases=[],
    name_mapping={"user_id": "userId", "user_name": "userName"},
)
class IamIdentityCenterGroupUser:
    def __init__(self, *, user_id: builtins.str, user_name: builtins.str) -> None:
        '''A user in the IAM Identity Center.

        :param user_id: 
        :param user_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4d113e8de3c819ea64049ef4ecdd94bf0bd4c7f073c1108fb83d9c5a42d176)
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_id": user_id,
            "user_name": user_name,
        }

    @builtins.property
    def user_id(self) -> builtins.str:
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamIdentityCenterGroupUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IamIdentityCenterPermissionSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "inline_policy_statement": "inlinePolicyStatement",
        "managed_policy_arns": "managedPolicyArns",
        "permissions_boundary": "permissionsBoundary",
        "session_duration": "sessionDuration",
    },
)
class IamIdentityCenterPermissionSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        inline_policy_statement: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyStatement] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_boundary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        session_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''A permission set in the IAM Identity Center.

        :param name: 
        :param description: 
        :param inline_policy_statement: 
        :param managed_policy_arns: 
        :param permissions_boundary: 
        :param session_duration: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a293b93390461ef7e7d9b1b438f936e46703143de016f19627bb0f53bb4600)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument inline_policy_statement", value=inline_policy_statement, expected_type=type_hints["inline_policy_statement"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument session_duration", value=session_duration, expected_type=type_hints["session_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if inline_policy_statement is not None:
            self._values["inline_policy_statement"] = inline_policy_statement
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if session_duration is not None:
            self._values["session_duration"] = session_duration

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_policy_statement(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        result = self._values.get("inline_policy_statement")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyStatement], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty]]:
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty]], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamIdentityCenterPermissionSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IamIdentityCenterProps",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "id": "id",
        "store_id": "storeId",
        "access_groups": "accessGroups",
        "permission_sets": "permissionSets",
        "users": "users",
    },
)
class IamIdentityCenterProps:
    def __init__(
        self,
        *,
        arn: builtins.str,
        id: builtins.str,
        store_id: builtins.str,
        access_groups: typing.Optional[typing.Sequence[typing.Union[IamIdentityCenterAccessGroupProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        permission_sets: typing.Optional[typing.Sequence[typing.Union[IamIdentityCenterPermissionSetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        users: typing.Optional[typing.Sequence[typing.Union["IdentityStoreUserProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param arn: 
        :param id: 
        :param store_id: 
        :param access_groups: 
        :param permission_sets: 
        :param users: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d53e4270ba7108bc74b395e1cffc1d1641584d585582b9f4d7faae37db1576c)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument store_id", value=store_id, expected_type=type_hints["store_id"])
            check_type(argname="argument access_groups", value=access_groups, expected_type=type_hints["access_groups"])
            check_type(argname="argument permission_sets", value=permission_sets, expected_type=type_hints["permission_sets"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "id": id,
            "store_id": store_id,
        }
        if access_groups is not None:
            self._values["access_groups"] = access_groups
        if permission_sets is not None:
            self._values["permission_sets"] = permission_sets
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def arn(self) -> builtins.str:
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def store_id(self) -> builtins.str:
        result = self._values.get("store_id")
        assert result is not None, "Required property 'store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_groups(
        self,
    ) -> typing.Optional[typing.List[IamIdentityCenterAccessGroupProps]]:
        result = self._values.get("access_groups")
        return typing.cast(typing.Optional[typing.List[IamIdentityCenterAccessGroupProps]], result)

    @builtins.property
    def permission_sets(
        self,
    ) -> typing.Optional[typing.List[IamIdentityCenterPermissionSetProps]]:
        result = self._values.get("permission_sets")
        return typing.cast(typing.Optional[typing.List[IamIdentityCenterPermissionSetProps]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List["IdentityStoreUserProps"]]:
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List["IdentityStoreUserProps"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamIdentityCenterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.IamIdentityPermissionSets")
class IamIdentityPermissionSets(enum.Enum):
    ADMIN = "ADMIN"
    READ_ONLY = "READ_ONLY"
    CATALOG = "CATALOG"


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IamPolicyPermissionsBoundaryProps",
    jsii_struct_bases=[],
    name_mapping={"policy_statement": "policyStatement"},
)
class IamPolicyPermissionsBoundaryProps:
    def __init__(
        self,
        *,
        policy_statement: typing.Union[_aws_cdk_aws_iam_ceddda9d.PolicyStatementProps, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param policy_statement: 
        '''
        if isinstance(policy_statement, dict):
            policy_statement = _aws_cdk_aws_iam_ceddda9d.PolicyStatementProps(**policy_statement)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa1ebd0e004c4d731c7a8b9904e55f5a3f2323e96551e478958a2fb249f8762)
            check_type(argname="argument policy_statement", value=policy_statement, expected_type=type_hints["policy_statement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_statement": policy_statement,
        }

    @builtins.property
    def policy_statement(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyStatementProps:
        result = self._values.get("policy_statement")
        assert result is not None, "Required property 'policy_statement' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyStatementProps, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamPolicyPermissionsBoundaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityStoreUser(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.IdentityStoreUser",
):
    '''A user in the IAM Identity Center.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        display_name: builtins.str,
        email: typing.Union["IdentityStoreUserEmailsProps", typing.Dict[builtins.str, typing.Any]],
        identity_store_id: builtins.str,
        name: typing.Union["IdentityStoreUserNameProps", typing.Dict[builtins.str, typing.Any]],
        user_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param display_name: 
        :param email: 
        :param identity_store_id: 
        :param name: 
        :param user_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212948c252d85e1c740c847bb3da25b0c6546c2944f3a557a2401e201f962874)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IdentityStoreUserPropsExt(
            display_name=display_name,
            email=email,
            identity_store_id=identity_store_id,
            name=name,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fetchCodeDirectory")
    @builtins.classmethod
    def fetch_code_directory(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fetchCodeDirectory", []))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IdentityStoreUserEmailsProps",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value", "primary": "primary"},
)
class IdentityStoreUserEmailsProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        value: builtins.str,
        primary: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''The email of a user in the IAM Identity Center.

        :param type: 
        :param value: 
        :param primary: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5fdcdaf1cbd4062e1f15ec5f89804de2aad2a692933a24c73a6277c37fe1ce)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }
        if primary is not None:
            self._values["primary"] = primary

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("primary")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityStoreUserEmailsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IdentityStoreUserNameProps",
    jsii_struct_bases=[],
    name_mapping={
        "family_name": "familyName",
        "formatted": "formatted",
        "given_name": "givenName",
        "honorific_prefix": "honorificPrefix",
        "honorific_suffix": "honorificSuffix",
        "middle_name": "middleName",
    },
)
class IdentityStoreUserNameProps:
    def __init__(
        self,
        *,
        family_name: builtins.str,
        formatted: builtins.str,
        given_name: builtins.str,
        honorific_prefix: typing.Optional[builtins.str] = None,
        honorific_suffix: typing.Optional[builtins.str] = None,
        middle_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The name of a user in the IAM Identity Center.

        :param family_name: 
        :param formatted: 
        :param given_name: 
        :param honorific_prefix: 
        :param honorific_suffix: 
        :param middle_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb68731a1540f928babde3bd9479adf50a83ad91f8919f01c91396c7345d806)
            check_type(argname="argument family_name", value=family_name, expected_type=type_hints["family_name"])
            check_type(argname="argument formatted", value=formatted, expected_type=type_hints["formatted"])
            check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
            check_type(argname="argument honorific_prefix", value=honorific_prefix, expected_type=type_hints["honorific_prefix"])
            check_type(argname="argument honorific_suffix", value=honorific_suffix, expected_type=type_hints["honorific_suffix"])
            check_type(argname="argument middle_name", value=middle_name, expected_type=type_hints["middle_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "family_name": family_name,
            "formatted": formatted,
            "given_name": given_name,
        }
        if honorific_prefix is not None:
            self._values["honorific_prefix"] = honorific_prefix
        if honorific_suffix is not None:
            self._values["honorific_suffix"] = honorific_suffix
        if middle_name is not None:
            self._values["middle_name"] = middle_name

    @builtins.property
    def family_name(self) -> builtins.str:
        result = self._values.get("family_name")
        assert result is not None, "Required property 'family_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def formatted(self) -> builtins.str:
        result = self._values.get("formatted")
        assert result is not None, "Required property 'formatted' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def given_name(self) -> builtins.str:
        result = self._values.get("given_name")
        assert result is not None, "Required property 'given_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def honorific_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("honorific_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def honorific_suffix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("honorific_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def middle_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("middle_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityStoreUserNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IdentityStoreUserProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "surname": "surname", "user_name": "userName"},
)
class IdentityStoreUserProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        surname: builtins.str,
        user_name: builtins.str,
    ) -> None:
        '''A user in the IAM Identity Center.

        :param name: 
        :param surname: 
        :param user_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04930dd85e755e2d6af07e4203ccd2dd864b8d8bf9306521c4d18e48cbec3228)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "surname": surname,
            "user_name": user_name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def surname(self) -> builtins.str:
        result = self._values.get("surname")
        assert result is not None, "Required property 'surname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityStoreUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.IdentityStoreUserPropsExt",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "email": "email",
        "identity_store_id": "identityStoreId",
        "name": "name",
        "user_name": "userName",
    },
)
class IdentityStoreUserPropsExt:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        email: typing.Union[IdentityStoreUserEmailsProps, typing.Dict[builtins.str, typing.Any]],
        identity_store_id: builtins.str,
        name: typing.Union[IdentityStoreUserNameProps, typing.Dict[builtins.str, typing.Any]],
        user_name: builtins.str,
    ) -> None:
        '''A user in the IAM Identity Center.

        :param display_name: 
        :param email: 
        :param identity_store_id: 
        :param name: 
        :param user_name: 
        '''
        if isinstance(email, dict):
            email = IdentityStoreUserEmailsProps(**email)
        if isinstance(name, dict):
            name = IdentityStoreUserNameProps(**name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729785b0f4f0054bacb120036ec98908185e34e32fc2c1b138fe021a185eaf1d)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "email": email,
            "identity_store_id": identity_store_id,
            "name": name,
            "user_name": user_name,
        }

    @builtins.property
    def display_name(self) -> builtins.str:
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> IdentityStoreUserEmailsProps:
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(IdentityStoreUserEmailsProps, result)

    @builtins.property
    def identity_store_id(self) -> builtins.str:
        result = self._values.get("identity_store_id")
        assert result is not None, "Required property 'identity_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> IdentityStoreUserNameProps:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(IdentityStoreUserNameProps, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityStoreUserPropsExt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.LFTag",
    jsii_struct_bases=[],
    name_mapping={"tag_key": "tagKey", "tag_values": "tagValues"},
)
class LFTag:
    def __init__(
        self,
        *,
        tag_key: builtins.str,
        tag_values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param tag_key: 
        :param tag_values: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94a03f25837494d40a0166756b67590aa4f3ddd2f9ec960e6c64f72903d3ef6)
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag_key": tag_key,
            "tag_values": tag_values,
        }

    @builtins.property
    def tag_key(self) -> builtins.str:
        result = self._values.get("tag_key")
        assert result is not None, "Required property 'tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_values(self) -> typing.List[builtins.str]:
        result = self._values.get("tag_values")
        assert result is not None, "Required property 'tag_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LFTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.LFTagSharable",
    jsii_struct_bases=[LFTag],
    name_mapping={"tag_key": "tagKey", "tag_values": "tagValues", "share": "share"},
)
class LFTagSharable(LFTag):
    def __init__(
        self,
        *,
        tag_key: builtins.str,
        tag_values: typing.Sequence[builtins.str],
        share: typing.Optional[typing.Union["ShareProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tag_key: 
        :param tag_values: 
        :param share: OPTIONAL - Configuration detailing how the tag can be shared with specified principals.
        '''
        if isinstance(share, dict):
            share = ShareProps(**share)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0a32854356a8e5cb6db695bab6838d4317df838e0398df9e9bd54b66980fae)
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            check_type(argname="argument share", value=share, expected_type=type_hints["share"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag_key": tag_key,
            "tag_values": tag_values,
        }
        if share is not None:
            self._values["share"] = share

    @builtins.property
    def tag_key(self) -> builtins.str:
        result = self._values.get("tag_key")
        assert result is not None, "Required property 'tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_values(self) -> typing.List[builtins.str]:
        result = self._values.get("tag_values")
        assert result is not None, "Required property 'tag_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def share(self) -> typing.Optional["ShareProps"]:
        '''OPTIONAL - Configuration detailing how the tag can be shared with specified principals.'''
        result = self._values.get("share")
        return typing.cast(typing.Optional["ShareProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LFTagSharable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.LakePermission",
    jsii_struct_bases=[],
    name_mapping={
        "database_actions": "databaseActions",
        "principals": "principals",
        "tags": "tags",
        "database_actions_with_grant": "databaseActionsWithGrant",
        "table_actions": "tableActions",
        "table_actions_with_grant": "tableActionsWithGrant",
    },
)
class LakePermission:
    def __init__(
        self,
        *,
        database_actions: typing.Sequence[DatabaseAction],
        principals: typing.Sequence[builtins.str],
        tags: typing.Sequence[typing.Union[LFTag, typing.Dict[builtins.str, typing.Any]]],
        database_actions_with_grant: typing.Optional[typing.Sequence[DatabaseAction]] = None,
        table_actions: typing.Optional[typing.Sequence["TableAction"]] = None,
        table_actions_with_grant: typing.Optional[typing.Sequence["TableAction"]] = None,
    ) -> None:
        '''
        :param database_actions: Actions that can be performed on databases, using Lake Formation Tag Based Access Control.
        :param principals: A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.
        :param tags: LF tags associated with the permissions, used to specify fine-grained access controls.
        :param database_actions_with_grant: OPTIONAL - Actions on databases with grant option, allowing grantees to further grant these permissions.
        :param table_actions: OPTIONAL - Actions that can be performed on tables, using Lake Formation Lake Formation Tag Based Access Control.
        :param table_actions_with_grant: OPTIONAL - Actions on tables with grant option, allowing grantees to further grant these permissions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741c7525e6c48e0f33c59d67c0cf6c154351deafad9062dd517b33be993570a6)
            check_type(argname="argument database_actions", value=database_actions, expected_type=type_hints["database_actions"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument database_actions_with_grant", value=database_actions_with_grant, expected_type=type_hints["database_actions_with_grant"])
            check_type(argname="argument table_actions", value=table_actions, expected_type=type_hints["table_actions"])
            check_type(argname="argument table_actions_with_grant", value=table_actions_with_grant, expected_type=type_hints["table_actions_with_grant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_actions": database_actions,
            "principals": principals,
            "tags": tags,
        }
        if database_actions_with_grant is not None:
            self._values["database_actions_with_grant"] = database_actions_with_grant
        if table_actions is not None:
            self._values["table_actions"] = table_actions
        if table_actions_with_grant is not None:
            self._values["table_actions_with_grant"] = table_actions_with_grant

    @builtins.property
    def database_actions(self) -> typing.List[DatabaseAction]:
        '''Actions that can be performed on databases, using Lake Formation Tag Based Access Control.'''
        result = self._values.get("database_actions")
        assert result is not None, "Required property 'database_actions' is missing"
        return typing.cast(typing.List[DatabaseAction], result)

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.'''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.List[LFTag]:
        '''LF tags associated with the permissions, used to specify fine-grained access controls.'''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.List[LFTag], result)

    @builtins.property
    def database_actions_with_grant(
        self,
    ) -> typing.Optional[typing.List[DatabaseAction]]:
        '''OPTIONAL - Actions on databases with grant option, allowing grantees to further grant these permissions.'''
        result = self._values.get("database_actions_with_grant")
        return typing.cast(typing.Optional[typing.List[DatabaseAction]], result)

    @builtins.property
    def table_actions(self) -> typing.Optional[typing.List["TableAction"]]:
        '''OPTIONAL - Actions that can be performed on tables, using Lake Formation Lake Formation Tag Based Access Control.'''
        result = self._values.get("table_actions")
        return typing.cast(typing.Optional[typing.List["TableAction"]], result)

    @builtins.property
    def table_actions_with_grant(self) -> typing.Optional[typing.List["TableAction"]]:
        '''OPTIONAL - Actions on tables with grant option, allowing grantees to further grant these permissions.'''
        result = self._values.get("table_actions_with_grant")
        return typing.cast(typing.Optional[typing.List["TableAction"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LakePermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogGlobalStack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.LogGlobalStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    ) -> None:
        '''
        :param scope: -
        :param env: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720e79ae794a29ad346c0022819309dba88ebc4a048caa4f8d4947844b9c56c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = DlzStackProps(env=env, name=name, stage=stage)

        jsii.create(self.__class__, self, [scope, props])


class LogRegionalStack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.LogRegionalStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    ) -> None:
        '''
        :param scope: -
        :param env: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f2b10d5e07ab0640a966ed0e138ac233a48dfc8318910e40cce6a7a8cf8e40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = DlzStackProps(env=env, name=name, stage=stage)

        jsii.create(self.__class__, self, [scope, props])


@jsii.data_type(
    jsii_type="aws-data-landing-zone.LogStacks",
    jsii_struct_bases=[],
    name_mapping={},
)
class LogStacks:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStacks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagementStack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.ManagementStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        stack_props: typing.Union[DlzStackProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union["MandatoryTags", typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union["SecurityHubNotification", typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union["NotificationDetailsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["Network", typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param stack_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d69f61e690c5df8ed09485eb394157170fdb81b4178db4b123a67b356f4938)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stack_props", value=stack_props, expected_type=type_hints["stack_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, stack_props, props])

    @jsii.member(jsii_name="budgets")
    def budgets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "budgets", []))

    @jsii.member(jsii_name="deploymentPlatformGitHub")
    def deployment_platform_git_hub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "deploymentPlatformGitHub", []))

    @jsii.member(jsii_name="iamIdentityCenter")
    def iam_identity_center(self) -> None:
        '''IAM Identity Center.'''
        return typing.cast(None, jsii.invoke(self, "iamIdentityCenter", []))

    @jsii.member(jsii_name="iamPermissionBoundary")
    def iam_permission_boundary(self) -> None:
        '''IAM Policy Permission Boundary.'''
        return typing.cast(None, jsii.invoke(self, "iamPermissionBoundary", []))

    @jsii.member(jsii_name="suspendedOuPolicies")
    def suspended_ou_policies(self) -> None:
        '''Service Control Policies and Tag Policies  applied at the OU level because we won't need any customizations per account.'''
        return typing.cast(None, jsii.invoke(self, "suspendedOuPolicies", []))

    @jsii.member(jsii_name="workloadAccountsOrgPolicies")
    def workload_accounts_org_policies(self) -> None:
        '''Service Control Policies and Tag Policies applied at the account level to enable customization per account.'''
        return typing.cast(None, jsii.invoke(self, "workloadAccountsOrgPolicies", []))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.MandatoryTags",
    jsii_struct_bases=[],
    name_mapping={
        "environment": "environment",
        "owner": "owner",
        "project": "project",
    },
)
class MandatoryTags:
    def __init__(
        self,
        *,
        environment: typing.Sequence[builtins.str],
        owner: typing.Sequence[builtins.str],
        project: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param environment: 
        :param owner: 
        :param project: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785d4d277df5b1660a9532d1cfb85da5b40cded4cbac9d82e8bfe551449a74d2)
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "environment": environment,
            "owner": owner,
            "project": project,
        }

    @builtins.property
    def environment(self) -> typing.List[builtins.str]:
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.List[builtins.str]:
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def project(self) -> typing.List[builtins.str]:
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MandatoryTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.Network",
    jsii_struct_bases=[],
    name_mapping={
        "bastion_hosts": "bastionHosts",
        "connections": "connections",
        "nats": "nats",
    },
)
class Network:
    def __init__(
        self,
        *,
        bastion_hosts: typing.Optional[typing.Sequence[typing.Union[BastionHost, typing.Dict[builtins.str, typing.Any]]]] = None,
        connections: typing.Optional[typing.Union["NetworkConnection", typing.Dict[builtins.str, typing.Any]]] = None,
        nats: typing.Optional[typing.Sequence[typing.Union["NetworkNat", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param bastion_hosts: 
        :param connections: 
        :param nats: 
        '''
        if isinstance(connections, dict):
            connections = NetworkConnection(**connections)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112a25d4b6227cb0a6c04a06c1217ddef8adfe64820a82b120dd719d1a9a5a7e)
            check_type(argname="argument bastion_hosts", value=bastion_hosts, expected_type=type_hints["bastion_hosts"])
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            check_type(argname="argument nats", value=nats, expected_type=type_hints["nats"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bastion_hosts is not None:
            self._values["bastion_hosts"] = bastion_hosts
        if connections is not None:
            self._values["connections"] = connections
        if nats is not None:
            self._values["nats"] = nats

    @builtins.property
    def bastion_hosts(self) -> typing.Optional[typing.List[BastionHost]]:
        result = self._values.get("bastion_hosts")
        return typing.cast(typing.Optional[typing.List[BastionHost]], result)

    @builtins.property
    def connections(self) -> typing.Optional["NetworkConnection"]:
        result = self._values.get("connections")
        return typing.cast(typing.Optional["NetworkConnection"], result)

    @builtins.property
    def nats(self) -> typing.Optional[typing.List["NetworkNat"]]:
        result = self._values.get("nats")
        return typing.cast(typing.Optional[typing.List["NetworkNat"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Network(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkAddress(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.NetworkAddress",
):
    def __init__(
        self,
        account: builtins.str,
        region: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[builtins.str] = None,
        route_table: typing.Optional[builtins.str] = None,
        subnet: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: -
        :param region: -
        :param vpc: -
        :param route_table: -
        :param subnet: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4797252545276129c66b07c9e6958c7c9323a09c9fe7556964b1ac32b0ca79f2)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        jsii.create(self.__class__, self, [account, region, vpc, route_table, subnet])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, props: builtins.str) -> "NetworkAddress":
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccefa74d81aa3039300d6e0d5a6d669ad1a9106dddde0f73715a7040925e6341)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast("NetworkAddress", jsii.sinvoke(cls, "fromString", [props]))

    @jsii.member(jsii_name="isAccountAddress")
    def is_account_address(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isAccountAddress", []))

    @jsii.member(jsii_name="isRegionAddress")
    def is_region_address(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isRegionAddress", []))

    @jsii.member(jsii_name="isRouteTableAddress")
    def is_route_table_address(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isRouteTableAddress", []))

    @jsii.member(jsii_name="isSubnetAddress")
    def is_subnet_address(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isSubnetAddress", []))

    @jsii.member(jsii_name="isVpcAddress")
    def is_vpc_address(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isVpcAddress", []))

    @jsii.member(jsii_name="matches")
    def matches(self, other: "NetworkAddress") -> builtins.bool:
        '''
        :param other: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d644760208a526116d94f74d430798c804f5cdb88a2923f168f82bec17f8b2ed)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(builtins.bool, jsii.invoke(self, "matches", [other]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "account"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="routeTable")
    def route_table(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeTable"))

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnet"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkConnection",
    jsii_struct_bases=[],
    name_mapping={"vpc_peering": "vpcPeering"},
)
class NetworkConnection:
    def __init__(
        self,
        *,
        vpc_peering: typing.Sequence[typing.Union["NetworkConnectionVpcPeering", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param vpc_peering: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e136f40784f5abbaba433b1b5f84fbf67b51e92245cacc63f9d7747b7a744a7)
            check_type(argname="argument vpc_peering", value=vpc_peering, expected_type=type_hints["vpc_peering"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_peering": vpc_peering,
        }

    @builtins.property
    def vpc_peering(self) -> typing.List["NetworkConnectionVpcPeering"]:
        result = self._values.get("vpc_peering")
        assert result is not None, "Required property 'vpc_peering' is missing"
        return typing.cast(typing.List["NetworkConnectionVpcPeering"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkConnectionVpcPeering",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "source": "source"},
)
class NetworkConnectionVpcPeering:
    def __init__(self, *, destination: NetworkAddress, source: NetworkAddress) -> None:
        '''
        :param destination: 
        :param source: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe835250156aeaa207e060e70cc219cd51331f50d00e6197cd10099c73d4ee5)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "source": source,
        }

    @builtins.property
    def destination(self) -> NetworkAddress:
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(NetworkAddress, result)

    @builtins.property
    def source(self) -> NetworkAddress:
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(NetworkAddress, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionVpcPeering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkEntityRouteTable",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "route_table": "routeTable",
        "subnets": "subnets",
    },
)
class NetworkEntityRouteTable:
    def __init__(
        self,
        *,
        address: NetworkAddress,
        route_table: _aws_cdk_aws_ec2_ceddda9d.CfnRouteTable,
        subnets: typing.Sequence[typing.Union["NetworkEntitySubnet", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param address: 
        :param route_table: 
        :param subnets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b85423ba33fe52684a4c7c02199fa8988477ddd396b0685a33cf42dec51ed1)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "route_table": route_table,
            "subnets": subnets,
        }

    @builtins.property
    def address(self) -> NetworkAddress:
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(NetworkAddress, result)

    @builtins.property
    def route_table(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnRouteTable:
        result = self._values.get("route_table")
        assert result is not None, "Required property 'route_table' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnRouteTable, result)

    @builtins.property
    def subnets(self) -> typing.List["NetworkEntitySubnet"]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List["NetworkEntitySubnet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkEntityRouteTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkEntitySubnet",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "subnet": "subnet"},
)
class NetworkEntitySubnet:
    def __init__(
        self,
        *,
        address: NetworkAddress,
        subnet: _aws_cdk_aws_ec2_ceddda9d.CfnSubnet,
    ) -> None:
        '''
        :param address: 
        :param subnet: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cba2945d93c18c494e150c68ca0c73597d4ab3679e1d501b859d93e95323fc4)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "subnet": subnet,
        }

    @builtins.property
    def address(self) -> NetworkAddress:
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(NetworkAddress, result)

    @builtins.property
    def subnet(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnSubnet:
        result = self._values.get("subnet")
        assert result is not None, "Required property 'subnet' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnSubnet, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkEntitySubnet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkEntityVpc",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "route_tables": "routeTables", "vpc": "vpc"},
)
class NetworkEntityVpc:
    def __init__(
        self,
        *,
        address: NetworkAddress,
        route_tables: typing.Sequence[typing.Union[NetworkEntityRouteTable, typing.Dict[builtins.str, typing.Any]]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.CfnVPC,
    ) -> None:
        '''
        :param address: 
        :param route_tables: 
        :param vpc: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f49f7dbf2c409a299c1bcf24ba217dd26f3d81b8558efa09818341a7e6b106)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument route_tables", value=route_tables, expected_type=type_hints["route_tables"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "route_tables": route_tables,
            "vpc": vpc,
        }

    @builtins.property
    def address(self) -> NetworkAddress:
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(NetworkAddress, result)

    @builtins.property
    def route_tables(self) -> typing.List[NetworkEntityRouteTable]:
        result = self._values.get("route_tables")
        assert result is not None, "Required property 'route_tables' is missing"
        return typing.cast(typing.List[NetworkEntityRouteTable], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnVPC:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnVPC, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkEntityVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkNat",
    jsii_struct_bases=[],
    name_mapping={
        "allow_access_from": "allowAccessFrom",
        "location": "location",
        "name": "name",
        "type": "type",
    },
)
class NetworkNat:
    def __init__(
        self,
        *,
        allow_access_from: typing.Sequence[NetworkAddress],
        location: NetworkAddress,
        name: builtins.str,
        type: typing.Union["NetworkNatType", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param allow_access_from: The route tables that should route to the NAT. Must be in the same Account, Region and VPC as the NAT.
        :param location: The location where the NAT will exist. The network address must target a specific subnet
        :param name: The name of the NAT Gateway to easily identify it.
        :param type: The type of NAT to create.
        '''
        if isinstance(type, dict):
            type = NetworkNatType(**type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b52f8661cab04102c607b79e74e7156e0dbdcb50edbdefaf1aaa5ba830acb28)
            check_type(argname="argument allow_access_from", value=allow_access_from, expected_type=type_hints["allow_access_from"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_access_from": allow_access_from,
            "location": location,
            "name": name,
            "type": type,
        }

    @builtins.property
    def allow_access_from(self) -> typing.List[NetworkAddress]:
        '''The route tables that should route to the NAT.

        Must be in the same Account, Region and VPC as the NAT.
        '''
        result = self._values.get("allow_access_from")
        assert result is not None, "Required property 'allow_access_from' is missing"
        return typing.cast(typing.List[NetworkAddress], result)

    @builtins.property
    def location(self) -> NetworkAddress:
        '''The location where the NAT will exist.

        The network address must target a specific subnet
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(NetworkAddress, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the NAT Gateway to easily identify it.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "NetworkNatType":
        '''The type of NAT to create.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("NetworkNatType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkNat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkNatGateway",
    jsii_struct_bases=[],
    name_mapping={"eip": "eip"},
)
class NetworkNatGateway:
    def __init__(
        self,
        *,
        eip: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param eip: 
        '''
        if isinstance(eip, dict):
            eip = _aws_cdk_aws_ec2_ceddda9d.CfnEIPProps(**eip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55cb6d0b5850b86e263d952cf073d6b5812ff49c926be806386269bd9c6e8e3)
            check_type(argname="argument eip", value=eip, expected_type=type_hints["eip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if eip is not None:
            self._values["eip"] = eip

    @builtins.property
    def eip(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps]:
        result = self._values.get("eip")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkNatGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkNatInstance",
    jsii_struct_bases=[],
    name_mapping={"instance_type": "instanceType", "eip": "eip"},
)
class NetworkNatInstance:
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        eip: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param instance_type: 
        :param eip: 
        '''
        if isinstance(eip, dict):
            eip = _aws_cdk_aws_ec2_ceddda9d.CfnEIPProps(**eip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc63f643c5aaf3aa3fab3e40997f4e5c00106f791cbe395682f8acf0dbb57b66)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument eip", value=eip, expected_type=type_hints["eip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
        }
        if eip is not None:
            self._values["eip"] = eip

    @builtins.property
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, result)

    @builtins.property
    def eip(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps]:
        result = self._values.get("eip")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkNatInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NetworkNatType",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "instance": "instance"},
)
class NetworkNatType:
    def __init__(
        self,
        *,
        gateway: typing.Optional[typing.Union[NetworkNatGateway, typing.Dict[builtins.str, typing.Any]]] = None,
        instance: typing.Optional[typing.Union[NetworkNatInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gateway: 
        :param instance: 
        '''
        if isinstance(gateway, dict):
            gateway = NetworkNatGateway(**gateway)
        if isinstance(instance, dict):
            instance = NetworkNatInstance(**instance)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630d95da854f2caf4c6788bd7758e4b4169a0cd16d6ad906f2f1274ed8de85d5)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway is not None:
            self._values["gateway"] = gateway
        if instance is not None:
            self._values["instance"] = instance

    @builtins.property
    def gateway(self) -> typing.Optional[NetworkNatGateway]:
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[NetworkNatGateway], result)

    @builtins.property
    def instance(self) -> typing.Optional[NetworkNatInstance]:
        result = self._values.get("instance")
        return typing.cast(typing.Optional[NetworkNatInstance], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkNatType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.NotificationDetailsProps",
    jsii_struct_bases=[],
    name_mapping={"emails": "emails", "slack": "slack"},
)
class NotificationDetailsProps:
    def __init__(
        self,
        *,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        slack: typing.Optional[typing.Union["SlackChannel", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param emails: 
        :param slack: 
        '''
        if isinstance(slack, dict):
            slack = SlackChannel(**slack)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af70c422a041a832d88717146a8aefbbd5baec30108b8da3bd257605dcbf5a6b)
            check_type(argname="argument emails", value=emails, expected_type=type_hints["emails"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if emails is not None:
            self._values["emails"] = emails
        if slack is not None:
            self._values["slack"] = slack

    @builtins.property
    def emails(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def slack(self) -> typing.Optional["SlackChannel"]:
        result = self._values.get("slack")
        return typing.cast(typing.Optional["SlackChannel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationDetailsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.OrgOuSecurity",
    jsii_struct_bases=[],
    name_mapping={"accounts": "accounts", "ou_id": "ouId"},
)
class OrgOuSecurity:
    def __init__(
        self,
        *,
        accounts: typing.Union["OrgOuSecurityAccounts", typing.Dict[builtins.str, typing.Any]],
        ou_id: builtins.str,
    ) -> None:
        '''
        :param accounts: 
        :param ou_id: 
        '''
        if isinstance(accounts, dict):
            accounts = OrgOuSecurityAccounts(**accounts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f34e757cce49396a45cbfc7ead91e5c7dce3c2d76c2e4b0bd7da2b39745295)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument ou_id", value=ou_id, expected_type=type_hints["ou_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "ou_id": ou_id,
        }

    @builtins.property
    def accounts(self) -> "OrgOuSecurityAccounts":
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast("OrgOuSecurityAccounts", result)

    @builtins.property
    def ou_id(self) -> builtins.str:
        result = self._values.get("ou_id")
        assert result is not None, "Required property 'ou_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOuSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.OrgOuSecurityAccounts",
    jsii_struct_bases=[],
    name_mapping={"audit": "audit", "log": "log"},
)
class OrgOuSecurityAccounts:
    def __init__(
        self,
        *,
        audit: typing.Union[DLzManagementAccount, typing.Dict[builtins.str, typing.Any]],
        log: typing.Union[DLzManagementAccount, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param audit: 
        :param log: 
        '''
        if isinstance(audit, dict):
            audit = DLzManagementAccount(**audit)
        if isinstance(log, dict):
            log = DLzManagementAccount(**log)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f29b2b57c9ddd33d371990ce96f70dcdc72df3857c74315a1fd1ffb46803bcb)
            check_type(argname="argument audit", value=audit, expected_type=type_hints["audit"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audit": audit,
            "log": log,
        }

    @builtins.property
    def audit(self) -> DLzManagementAccount:
        result = self._values.get("audit")
        assert result is not None, "Required property 'audit' is missing"
        return typing.cast(DLzManagementAccount, result)

    @builtins.property
    def log(self) -> DLzManagementAccount:
        result = self._values.get("log")
        assert result is not None, "Required property 'log' is missing"
        return typing.cast(DLzManagementAccount, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOuSecurityAccounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.OrgOuSuspended",
    jsii_struct_bases=[],
    name_mapping={"ou_id": "ouId"},
)
class OrgOuSuspended:
    def __init__(self, *, ou_id: builtins.str) -> None:
        '''
        :param ou_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4573748c48dc91941ec335b61a6e324a01d9062b5fcb4c4f5f1429d9c2a6e4a)
            check_type(argname="argument ou_id", value=ou_id, expected_type=type_hints["ou_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ou_id": ou_id,
        }

    @builtins.property
    def ou_id(self) -> builtins.str:
        result = self._values.get("ou_id")
        assert result is not None, "Required property 'ou_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOuSuspended(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.OrgOuWorkloads",
    jsii_struct_bases=[],
    name_mapping={"accounts": "accounts", "ou_id": "ouId"},
)
class OrgOuWorkloads:
    def __init__(
        self,
        *,
        accounts: typing.Sequence[typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]]],
        ou_id: builtins.str,
    ) -> None:
        '''
        :param accounts: 
        :param ou_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d03ce67a3c30402794278f91346790936b6174e4002bf766fda9cc90fdaa7f)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument ou_id", value=ou_id, expected_type=type_hints["ou_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "ou_id": ou_id,
        }

    @builtins.property
    def accounts(self) -> typing.List[DLzAccount]:
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(typing.List[DLzAccount], result)

    @builtins.property
    def ou_id(self) -> builtins.str:
        result = self._values.get("ou_id")
        assert result is not None, "Required property 'ou_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOuWorkloads(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.OrgOus",
    jsii_struct_bases=[],
    name_mapping={
        "security": "security",
        "suspended": "suspended",
        "workloads": "workloads",
    },
)
class OrgOus:
    def __init__(
        self,
        *,
        security: typing.Union[OrgOuSecurity, typing.Dict[builtins.str, typing.Any]],
        suspended: typing.Union[OrgOuSuspended, typing.Dict[builtins.str, typing.Any]],
        workloads: typing.Union[OrgOuWorkloads, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param security: 
        :param suspended: 
        :param workloads: 
        '''
        if isinstance(security, dict):
            security = OrgOuSecurity(**security)
        if isinstance(suspended, dict):
            suspended = OrgOuSuspended(**suspended)
        if isinstance(workloads, dict):
            workloads = OrgOuWorkloads(**workloads)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e17514f4d2625b6cc5fa1419d3f2b35daa43ff1ea54148d2e42ea833e6e70ab)
            check_type(argname="argument security", value=security, expected_type=type_hints["security"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument workloads", value=workloads, expected_type=type_hints["workloads"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security": security,
            "suspended": suspended,
            "workloads": workloads,
        }

    @builtins.property
    def security(self) -> OrgOuSecurity:
        result = self._values.get("security")
        assert result is not None, "Required property 'security' is missing"
        return typing.cast(OrgOuSecurity, result)

    @builtins.property
    def suspended(self) -> OrgOuSuspended:
        result = self._values.get("suspended")
        assert result is not None, "Required property 'suspended' is missing"
        return typing.cast(OrgOuSuspended, result)

    @builtins.property
    def workloads(self) -> OrgOuWorkloads:
        result = self._values.get("workloads")
        assert result is not None, "Required property 'workloads' is missing"
        return typing.cast(OrgOuWorkloads, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.OrgRootAccounts",
    jsii_struct_bases=[],
    name_mapping={"management": "management"},
)
class OrgRootAccounts:
    def __init__(
        self,
        *,
        management: typing.Union[DLzManagementAccount, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param management: 
        '''
        if isinstance(management, dict):
            management = DLzManagementAccount(**management)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606ce365c1ad865f5392055804622d3b5b4d0ddd5600d5abba5c366218405bf5)
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "management": management,
        }

    @builtins.property
    def management(self) -> DLzManagementAccount:
        result = self._values.get("management")
        assert result is not None, "Required property 'management' is missing"
        return typing.cast(DLzManagementAccount, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgRootAccounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.Ou")
class Ou(enum.Enum):
    SECURITY = "SECURITY"
    WORKLOADS = "WORKLOADS"
    SUSPENDED = "SUSPENDED"


@jsii.data_type(
    jsii_type="aws-data-landing-zone.PartialOu",
    jsii_struct_bases=[],
    name_mapping={"ou_id": "ouId", "accounts": "accounts"},
)
class PartialOu:
    def __init__(
        self,
        *,
        ou_id: builtins.str,
        accounts: typing.Optional[typing.Sequence[typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param ou_id: 
        :param accounts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36ba8cd3f05ce17a729fa92f765c69c2671d05a45519f8bdf5b1bb4c0347894)
            check_type(argname="argument ou_id", value=ou_id, expected_type=type_hints["ou_id"])
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ou_id": ou_id,
        }
        if accounts is not None:
            self._values["accounts"] = accounts

    @builtins.property
    def ou_id(self) -> builtins.str:
        result = self._values.get("ou_id")
        assert result is not None, "Required property 'ou_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accounts(self) -> typing.Optional[typing.List[DLzAccount]]:
        result = self._values.get("accounts")
        return typing.cast(typing.Optional[typing.List[DLzAccount]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PartialOu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.Region")
class Region(enum.Enum):
    '''Control Tower Supported Regions as listed here https://docs.aws.amazon.com/controltower/latest/userguide/region-how.html with the regions that might have partial or no support for SecurityHub Standard mentioned in the comment https://docs.aws.amazon.com/controltower/latest/userguide/security-hub-controls.html#sh-unsupported-regions Last updated: 22 Mar 2024.'''

    US_EAST_1 = "US_EAST_1"
    '''N.

    Virginia
    '''
    US_EAST_2 = "US_EAST_2"
    '''Ohio.'''
    US_WEST_1 = "US_WEST_1"
    '''N.

    California
    '''
    US_WEST_2 = "US_WEST_2"
    '''Oregon.'''
    CA_CENTRAL_1 = "CA_CENTRAL_1"
    '''Canada (Central).'''
    EU_WEST_1 = "EU_WEST_1"
    '''Ireland.'''
    EU_WEST_2 = "EU_WEST_2"
    '''London.'''
    EU_WEST_3 = "EU_WEST_3"
    '''Paris.'''
    EU_CENTRAL_1 = "EU_CENTRAL_1"
    '''Frankfurt.'''
    EU_CENTRAL_2 = "EU_CENTRAL_2"
    '''Zurich.'''
    EU_NORTH_1 = "EU_NORTH_1"
    '''Stockholm.'''
    EU_SOUTH_1 = "EU_SOUTH_1"
    '''Milan.'''
    EU_SOUTH_2 = "EU_SOUTH_2"
    '''Spain.'''
    AP_NORTHEAST_1 = "AP_NORTHEAST_1"
    '''Tokyo.'''
    AP_NORTHEAST_2 = "AP_NORTHEAST_2"
    '''Seoul.'''
    AP_NORTHEAST_3 = "AP_NORTHEAST_3"
    '''Osaka.'''
    AP_SOUTHEAST_1 = "AP_SOUTHEAST_1"
    '''Singapore.'''
    AP_SOUTHEAST_2 = "AP_SOUTHEAST_2"
    '''Sydney, Melbourne.'''
    AP_SOUTHEAST_3 = "AP_SOUTHEAST_3"
    '''Jakarta No Control Tower SecurityHub Standard support.'''
    AP_SOUTHEAST_4 = "AP_SOUTHEAST_4"
    '''Melbourne No Control Tower SecurityHub Standard support.'''
    AP_EAST_1 = "AP_EAST_1"
    '''Hong Kong No Control Tower SecurityHub Standard support.'''
    SA_EAST_1 = "SA_EAST_1"
    '''Sao Paulo.'''
    AF_SOUTH_1 = "AF_SOUTH_1"
    '''Cape Town No Control Tower SecurityHub Standard support.'''
    ME_SOUTH_1 = "ME_SOUTH_1"
    '''Bahrain, UAE, Tel Aviv No Control Tower SecurityHub Standard support.'''
    ME_CENTRAL_1 = "ME_CENTRAL_1"
    '''UAE No Control Tower SecurityHub Standard support.'''
    IL_CENTRAL_1 = "IL_CENTRAL_1"
    '''Israel No Control Tower SecurityHub Standard support.'''
    AP_SOUTH_2 = "AP_SOUTH_2"
    '''Hyderabad No Control Tower SecurityHub Standard support.'''


class Report(metaclass=jsii.JSIIMeta, jsii_type="aws-data-landing-zone.Report"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addReportForAccountRegion")
    @builtins.classmethod
    def add_report_for_account_region(
        cls,
        account_name: builtins.str,
        region: builtins.str,
        *,
        description: builtins.str,
        external_link: builtins.str,
        name: builtins.str,
        type: "ReportType",
    ) -> None:
        '''
        :param account_name: -
        :param region: -
        :param description: 
        :param external_link: 
        :param name: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc449229300537412606dd27e8a89c496d8053bd1277601326c955bb9c765cb)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        report_resource = ReportResource(
            description=description, external_link=external_link, name=name, type=type
        )

        return typing.cast(None, jsii.sinvoke(cls, "addReportForAccountRegion", [account_name, region, report_resource]))

    @jsii.member(jsii_name="addReportForAccountRegions")
    @builtins.classmethod
    def add_report_for_account_regions(
        cls,
        account_name: builtins.str,
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        *,
        description: builtins.str,
        external_link: builtins.str,
        name: builtins.str,
        type: "ReportType",
    ) -> None:
        '''
        :param account_name: -
        :param regions: -
        :param description: 
        :param external_link: 
        :param name: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e5973b06d1aff0aca71eeea28d66b88f909cb86e0427f279b90c7bec79413d)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        report_resource = ReportResource(
            description=description, external_link=external_link, name=name, type=type
        )

        return typing.cast(None, jsii.sinvoke(cls, "addReportForAccountRegions", [account_name, regions, report_resource]))

    @jsii.member(jsii_name="addReportForOuAccountRegions")
    @builtins.classmethod
    def add_report_for_ou_account_regions(
        cls,
        partial_ou: typing.Union[PartialOu, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        *,
        description: builtins.str,
        external_link: builtins.str,
        name: builtins.str,
        type: "ReportType",
    ) -> None:
        '''
        :param partial_ou: -
        :param regions: -
        :param description: 
        :param external_link: 
        :param name: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f47a0bacec1440d23980b20c3a352762f29c2cb3c62f635f9c90d93a048b49)
            check_type(argname="argument partial_ou", value=partial_ou, expected_type=type_hints["partial_ou"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        report_resource = ReportResource(
            description=description, external_link=external_link, name=name, type=type
        )

        return typing.cast(None, jsii.sinvoke(cls, "addReportForOuAccountRegions", [partial_ou, regions, report_resource]))

    @jsii.member(jsii_name="addReportForSecurityOuAccountRegions")
    @builtins.classmethod
    def add_report_for_security_ou_account_regions(
        cls,
        security_ou: typing.Union[OrgOuSecurity, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        *,
        description: builtins.str,
        external_link: builtins.str,
        name: builtins.str,
        type: "ReportType",
    ) -> None:
        '''
        :param security_ou: -
        :param regions: -
        :param description: 
        :param external_link: 
        :param name: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da4e845f0e288eab548c0a1b8103817635fbeb580550a21f4e52571cd071171)
            check_type(argname="argument security_ou", value=security_ou, expected_type=type_hints["security_ou"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        report_resource = ReportResource(
            description=description, external_link=external_link, name=name, type=type
        )

        return typing.cast(None, jsii.sinvoke(cls, "addReportForSecurityOuAccountRegions", [security_ou, regions, report_resource]))

    @jsii.member(jsii_name="printConsoleReport")
    @builtins.classmethod
    def print_console_report(cls) -> None:
        return typing.cast(None, jsii.sinvoke(cls, "printConsoleReport", []))

    @jsii.member(jsii_name="saveConsoleReport")
    @builtins.classmethod
    def save_console_report(cls) -> None:
        return typing.cast(None, jsii.sinvoke(cls, "saveConsoleReport", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="reports")
    def reports(cls) -> typing.List["ReportItem"]:  # pyright: ignore [reportGeneralTypeIssues,reportRedeclaration]
        return typing.cast(typing.List["ReportItem"], jsii.sget(cls, "reports"))

    @reports.setter # type: ignore[no-redef]
    def reports(cls, value: typing.List["ReportItem"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856f2b03255b0804a51c67f00f543e51cec490d9ec33c1e7476dbafdf55a3617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "reports", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-data-landing-zone.ReportResource",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "external_link": "externalLink",
        "name": "name",
        "type": "type",
    },
)
class ReportResource:
    def __init__(
        self,
        *,
        description: builtins.str,
        external_link: builtins.str,
        name: builtins.str,
        type: "ReportType",
    ) -> None:
        '''
        :param description: 
        :param external_link: 
        :param name: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49bef332105b230c86aaf0a7b69fb27bab248377f1547f308c0cf8f68e128783)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_link", value=external_link, expected_type=type_hints["external_link"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "external_link": external_link,
            "name": name,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_link(self) -> builtins.str:
        result = self._values.get("external_link")
        assert result is not None, "Required property 'external_link' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "ReportType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ReportType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReportResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.ReportType")
class ReportType(enum.Enum):
    CONTROL_TOWER_CONTROL = "CONTROL_TOWER_CONTROL"
    CONFIG_RULE = "CONFIG_RULE"
    SECURITY_HUB_STANDARD = "SECURITY_HUB_STANDARD"
    TAG_POLICY = "TAG_POLICY"
    SERVICE_CONTROL_POLICY = "SERVICE_CONTROL_POLICY"


@jsii.data_type(
    jsii_type="aws-data-landing-zone.RootOptions",
    jsii_struct_bases=[],
    name_mapping={"accounts": "accounts", "controls": "controls"},
)
class RootOptions:
    def __init__(
        self,
        *,
        accounts: typing.Union[OrgRootAccounts, typing.Dict[builtins.str, typing.Any]],
        controls: typing.Optional[typing.Sequence[DlzControlTowerStandardControls]] = None,
    ) -> None:
        '''
        :param accounts: 
        :param controls: Control Tower Controls applied to all the OUs in the organization.
        '''
        if isinstance(accounts, dict):
            accounts = OrgRootAccounts(**accounts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6607c7d387d6e944e5632eec7f93574b7d98c934d4512dcfca5429b25022cb)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument controls", value=controls, expected_type=type_hints["controls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
        }
        if controls is not None:
            self._values["controls"] = controls

    @builtins.property
    def accounts(self) -> OrgRootAccounts:
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(OrgRootAccounts, result)

    @builtins.property
    def controls(self) -> typing.Optional[typing.List[DlzControlTowerStandardControls]]:
        '''Control Tower Controls applied to all the OUs in the organization.'''
        result = self._values.get("controls")
        return typing.cast(typing.Optional[typing.List[DlzControlTowerStandardControls]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RootOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Scripts(metaclass=jsii.JSIIMeta, jsii_type="aws-data-landing-zone.Scripts"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="boostrapAll")
    def boostrap_all(
        self,
        props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
        bootstrap_role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Bootstraps all accounts in all regions as defined by the config.

        :param props: -
        :param bootstrap_role_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc9bc9aae2524a3bab49c1aad2f44c3334432f02eef685410ff1463184b64d6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument bootstrap_role_name", value=bootstrap_role_name, expected_type=type_hints["bootstrap_role_name"])
        return typing.cast(None, jsii.ainvoke(self, "boostrapAll", [props, bootstrap_role_name]))

    @jsii.member(jsii_name="configureCostAllocationTags")
    def configure_cost_allocation_tags(
        self,
        props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Sets the Cost Allocation Tags for the organization.

        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c549b7d6c4faf3759ade9a1f2b24c58d365a09fe522e820c098b90ff75dfb1ee)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        _ = ForceNoPythonArgumentLifting()

        return typing.cast(None, jsii.ainvoke(self, "configureCostAllocationTags", [props, _]))

    @jsii.member(jsii_name="deployAll")
    def deploy_all(
        self,
        props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''CDK deploy all stacks.

        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05e9b7fddb47e361ba40d610b2d338af4e3371273b1131c3e321732bb5a22b3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        _ = ForceNoPythonArgumentLifting()

        return typing.cast(None, jsii.ainvoke(self, "deployAll", [props, _]))

    @jsii.member(jsii_name="deploySelect")
    def deploy_select(
        self,
        props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
        id: builtins.str,
    ) -> None:
        '''CDK deploy stacks identified by the id.

        :param props: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544619e03e32ce22b6368ba8d8d58c9bdea6e8535aed76a325f294befb225ae7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(None, jsii.ainvoke(self, "deploySelect", [props, id]))

    @jsii.member(jsii_name="diffAll")
    def diff_all(
        self,
        props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''CDK diff all stacks.

        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c13acfd0b5dfa172519cdfaf97422c384054cfebb740d77ab7eb396c59d259)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        _ = ForceNoPythonArgumentLifting()

        return typing.cast(None, jsii.ainvoke(self, "diffAll", [props, _]))

    @jsii.member(jsii_name="diffSelect")
    def diff_select(
        self,
        props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
        id: builtins.str,
    ) -> None:
        '''CDK diff stacks identified by the id.

        :param props: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6696a886afc4754fe7591025ce14d98042ca7b767f3a1e325589a50907b2198f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(None, jsii.ainvoke(self, "diffSelect", [props, id]))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.SecurityHubNotification",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "notification": "notification",
        "severity": "severity",
        "workflow_status": "workflowStatus",
    },
)
class SecurityHubNotification:
    def __init__(
        self,
        *,
        id: builtins.str,
        notification: typing.Union["SecurityHubNotificationProps", typing.Dict[builtins.str, typing.Any]],
        severity: typing.Optional[typing.Sequence["SecurityHubNotificationSeverity"]] = None,
        workflow_status: typing.Optional[typing.Sequence["SecurityHubNotificationSWorkflowStatus"]] = None,
    ) -> None:
        '''
        :param id: 
        :param notification: 
        :param severity: 
        :param workflow_status: 
        '''
        if isinstance(notification, dict):
            notification = SecurityHubNotificationProps(**notification)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e854a03d546ed12020dfb78447f9f686114130cc4f3098c32be960de4e3c598c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification", value=notification, expected_type=type_hints["notification"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument workflow_status", value=workflow_status, expected_type=type_hints["workflow_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "notification": notification,
        }
        if severity is not None:
            self._values["severity"] = severity
        if workflow_status is not None:
            self._values["workflow_status"] = workflow_status

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification(self) -> "SecurityHubNotificationProps":
        result = self._values.get("notification")
        assert result is not None, "Required property 'notification' is missing"
        return typing.cast("SecurityHubNotificationProps", result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional[typing.List["SecurityHubNotificationSeverity"]]:
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.List["SecurityHubNotificationSeverity"]], result)

    @builtins.property
    def workflow_status(
        self,
    ) -> typing.Optional[typing.List["SecurityHubNotificationSWorkflowStatus"]]:
        result = self._values.get("workflow_status")
        return typing.cast(typing.Optional[typing.List["SecurityHubNotificationSWorkflowStatus"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityHubNotification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.SecurityHubNotificationProps",
    jsii_struct_bases=[],
    name_mapping={"emails": "emails", "slack": "slack"},
)
class SecurityHubNotificationProps:
    def __init__(
        self,
        *,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        slack: typing.Optional[typing.Union["SlackChannel", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param emails: 
        :param slack: 
        '''
        if isinstance(slack, dict):
            slack = SlackChannel(**slack)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997c41afa8168361be6a92beb218300fca22fd51ee75c7689ae20b2452421107)
            check_type(argname="argument emails", value=emails, expected_type=type_hints["emails"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if emails is not None:
            self._values["emails"] = emails
        if slack is not None:
            self._values["slack"] = slack

    @builtins.property
    def emails(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def slack(self) -> typing.Optional["SlackChannel"]:
        result = self._values.get("slack")
        return typing.cast(typing.Optional["SlackChannel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityHubNotificationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.SecurityHubNotificationSWorkflowStatus")
class SecurityHubNotificationSWorkflowStatus(enum.Enum):
    '''https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_Workflow.html.'''

    NEW = "NEW"
    NOTIFIED = "NOTIFIED"
    SUPPRESSED = "SUPPRESSED"
    RESOLVED = "RESOLVED"


@jsii.enum(jsii_type="aws-data-landing-zone.SecurityHubNotificationSeverity")
class SecurityHubNotificationSeverity(enum.Enum):
    '''https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_Severity.html.'''

    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@jsii.data_type(
    jsii_type="aws-data-landing-zone.ShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "with_external_account": "withExternalAccount",
        "within_account": "withinAccount",
    },
)
class ShareProps:
    def __init__(
        self,
        *,
        with_external_account: typing.Optional[typing.Sequence[typing.Union["SharedExternal", typing.Dict[builtins.str, typing.Any]]]] = None,
        within_account: typing.Optional[typing.Sequence[typing.Union["SharedInternal", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param with_external_account: Configurations for sharing LF-Tags with external AWS accounts.
        :param within_account: Configurations for sharing LF-Tags with principals within the same AWS account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f486fdddb8882f5cfc65103fba2e9564c68c613fa8e6f4a647b2d7c479488c1)
            check_type(argname="argument with_external_account", value=with_external_account, expected_type=type_hints["with_external_account"])
            check_type(argname="argument within_account", value=within_account, expected_type=type_hints["within_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if with_external_account is not None:
            self._values["with_external_account"] = with_external_account
        if within_account is not None:
            self._values["within_account"] = within_account

    @builtins.property
    def with_external_account(self) -> typing.Optional[typing.List["SharedExternal"]]:
        '''Configurations for sharing LF-Tags with external AWS accounts.'''
        result = self._values.get("with_external_account")
        return typing.cast(typing.Optional[typing.List["SharedExternal"]], result)

    @builtins.property
    def within_account(self) -> typing.Optional[typing.List["SharedInternal"]]:
        '''Configurations for sharing LF-Tags with principals within the same AWS account.'''
        result = self._values.get("within_account")
        return typing.cast(typing.Optional[typing.List["SharedInternal"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.SharedExternal",
    jsii_struct_bases=[BaseSharedTagProps],
    name_mapping={
        "principals": "principals",
        "specific_values": "specificValues",
        "tag_actions": "tagActions",
        "tag_actions_with_grant": "tagActionsWithGrant",
    },
)
class SharedExternal(BaseSharedTagProps):
    def __init__(
        self,
        *,
        principals: typing.Sequence[builtins.str],
        specific_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_actions: typing.Sequence["TagAction"],
        tag_actions_with_grant: typing.Optional[typing.Sequence["TagAction"]] = None,
    ) -> None:
        '''
        :param principals: A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.
        :param specific_values: OPTIONAL - A list of specific values of the tag that can be shared. All possible values if omitted.
        :param tag_actions: A list of actions that can be performed on the tag. Only ``TagAction.DESCRIBE`` and ``TagAction.ASSOCIATE`` are allowed.
        :param tag_actions_with_grant: A list of actions on the tag with grant option, allowing grantees to further grant these permissions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8933cd307fea6cae69e46193541fb6f4719526676560978d1b02a84dee49d1b)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument specific_values", value=specific_values, expected_type=type_hints["specific_values"])
            check_type(argname="argument tag_actions", value=tag_actions, expected_type=type_hints["tag_actions"])
            check_type(argname="argument tag_actions_with_grant", value=tag_actions_with_grant, expected_type=type_hints["tag_actions_with_grant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principals": principals,
            "tag_actions": tag_actions,
        }
        if specific_values is not None:
            self._values["specific_values"] = specific_values
        if tag_actions_with_grant is not None:
            self._values["tag_actions_with_grant"] = tag_actions_with_grant

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.'''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def specific_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''OPTIONAL - A list of specific values of the tag that can be shared.

        All possible values if omitted.
        '''
        result = self._values.get("specific_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_actions(self) -> typing.List["TagAction"]:
        '''A list of actions that can be performed on the tag.

        Only ``TagAction.DESCRIBE`` and ``TagAction.ASSOCIATE`` are allowed.
        '''
        result = self._values.get("tag_actions")
        assert result is not None, "Required property 'tag_actions' is missing"
        return typing.cast(typing.List["TagAction"], result)

    @builtins.property
    def tag_actions_with_grant(self) -> typing.Optional[typing.List["TagAction"]]:
        '''A list of actions on the tag with grant option, allowing grantees to further grant these permissions.'''
        result = self._values.get("tag_actions_with_grant")
        return typing.cast(typing.Optional[typing.List["TagAction"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharedExternal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.SharedInternal",
    jsii_struct_bases=[BaseSharedTagProps],
    name_mapping={
        "principals": "principals",
        "specific_values": "specificValues",
        "tag_actions": "tagActions",
        "tag_actions_with_grant": "tagActionsWithGrant",
    },
)
class SharedInternal(BaseSharedTagProps):
    def __init__(
        self,
        *,
        principals: typing.Sequence[builtins.str],
        specific_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_actions: typing.Sequence["TagAction"],
        tag_actions_with_grant: typing.Optional[typing.Sequence["TagAction"]] = None,
    ) -> None:
        '''
        :param principals: A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.
        :param specific_values: OPTIONAL - A list of specific values of the tag that can be shared. All possible values if omitted.
        :param tag_actions: A list of actions that can be performed on the tag.
        :param tag_actions_with_grant: A list of actions on the tag with grant option, allowing grantees to further grant these permissions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d8d1f8a6a3c10cf19eaac05e1d67906bae08567ed72e2bc2b68e71cc614c9a)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument specific_values", value=specific_values, expected_type=type_hints["specific_values"])
            check_type(argname="argument tag_actions", value=tag_actions, expected_type=type_hints["tag_actions"])
            check_type(argname="argument tag_actions_with_grant", value=tag_actions_with_grant, expected_type=type_hints["tag_actions_with_grant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principals": principals,
            "tag_actions": tag_actions,
        }
        if specific_values is not None:
            self._values["specific_values"] = specific_values
        if tag_actions_with_grant is not None:
            self._values["tag_actions_with_grant"] = tag_actions_with_grant

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''A list of principal identity ARNs (e.g., AWS accounts, IAM roles/users) that the permissions apply to.'''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def specific_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''OPTIONAL - A list of specific values of the tag that can be shared.

        All possible values if omitted.
        '''
        result = self._values.get("specific_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_actions(self) -> typing.List["TagAction"]:
        '''A list of actions that can be performed on the tag.'''
        result = self._values.get("tag_actions")
        assert result is not None, "Required property 'tag_actions' is missing"
        return typing.cast(typing.List["TagAction"], result)

    @builtins.property
    def tag_actions_with_grant(self) -> typing.Optional[typing.List["TagAction"]]:
        '''A list of actions on the tag with grant option, allowing grantees to further grant these permissions.'''
        result = self._values.get("tag_actions_with_grant")
        return typing.cast(typing.Optional[typing.List["TagAction"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharedInternal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-data-landing-zone.SlackChannel",
    jsii_struct_bases=[],
    name_mapping={
        "slack_channel_configuration_name": "slackChannelConfigurationName",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
    },
)
class SlackChannel:
    def __init__(
        self,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
    ) -> None:
        '''
        :param slack_channel_configuration_name: 
        :param slack_channel_id: 
        :param slack_workspace_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3338a132d632cd1a36dc4507ebe49513af577cd8fbb3e489ef39911da0f577e9)
            check_type(argname="argument slack_channel_configuration_name", value=slack_channel_configuration_name, expected_type=type_hints["slack_channel_configuration_name"])
            check_type(argname="argument slack_channel_id", value=slack_channel_id, expected_type=type_hints["slack_channel_id"])
            check_type(argname="argument slack_workspace_id", value=slack_workspace_id, expected_type=type_hints["slack_workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "slack_channel_configuration_name": slack_channel_configuration_name,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }

    @builtins.property
    def slack_channel_configuration_name(self) -> builtins.str:
        result = self._values.get("slack_channel_configuration_name")
        assert result is not None, "Required property 'slack_channel_configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_channel_id(self) -> builtins.str:
        result = self._values.get("slack_channel_id")
        assert result is not None, "Required property 'slack_channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_workspace_id(self) -> builtins.str:
        result = self._values.get("slack_workspace_id")
        assert result is not None, "Required property 'slack_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackChannel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-data-landing-zone.TableAction")
class TableAction(enum.Enum):
    DESCRIBE = "DESCRIBE"
    SELECT = "SELECT"
    DELETE = "DELETE"
    INSERT = "INSERT"
    DROP = "DROP"
    ALTER = "ALTER"


@jsii.enum(jsii_type="aws-data-landing-zone.TagAction")
class TagAction(enum.Enum):
    DESCRIBE = "DESCRIBE"
    ASSOCIATE = "ASSOCIATE"
    ALTER = "ALTER"
    DROP = "DROP"


@jsii.data_type(
    jsii_type="aws-data-landing-zone.WorkloadAccountProps",
    jsii_struct_bases=[DlzStackProps],
    name_mapping={
        "env": "env",
        "name": "name",
        "stage": "stage",
        "dlz_account": "dlzAccount",
        "global_variables": "globalVariables",
    },
)
class WorkloadAccountProps(DlzStackProps):
    def __init__(
        self,
        *,
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
        dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
        global_variables: typing.Union[GlobalVariables, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param env: 
        :param name: 
        :param stage: 
        :param dlz_account: 
        :param global_variables: 
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if isinstance(name, dict):
            name = DlzStackNameProps(**name)
        if isinstance(dlz_account, dict):
            dlz_account = DLzAccount(**dlz_account)
        if isinstance(global_variables, dict):
            global_variables = GlobalVariables(**global_variables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760bd95205aea37f01978923f411d9f8dbda399f17b1efb4f1e88a4f333cfc84)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument dlz_account", value=dlz_account, expected_type=type_hints["dlz_account"])
            check_type(argname="argument global_variables", value=global_variables, expected_type=type_hints["global_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env": env,
            "name": name,
            "stage": stage,
            "dlz_account": dlz_account,
            "global_variables": global_variables,
        }

    @builtins.property
    def env(self) -> _aws_cdk_ceddda9d.Environment:
        result = self._values.get("env")
        assert result is not None, "Required property 'env' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Environment, result)

    @builtins.property
    def name(self) -> DlzStackNameProps:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(DlzStackNameProps, result)

    @builtins.property
    def stage(self) -> _cdk_express_pipeline_9801c4a1.ExpressStage:
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(_cdk_express_pipeline_9801c4a1.ExpressStage, result)

    @builtins.property
    def dlz_account(self) -> DLzAccount:
        result = self._values.get("dlz_account")
        assert result is not None, "Required property 'dlz_account' is missing"
        return typing.cast(DLzAccount, result)

    @builtins.property
    def global_variables(self) -> GlobalVariables:
        result = self._values.get("global_variables")
        assert result is not None, "Required property 'global_variables' is missing"
        return typing.cast(GlobalVariables, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadAccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadGlobalDataServicesPhase1Stack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadGlobalDataServicesPhase1Stack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
        global_variables: typing.Union[GlobalVariables, typing.Dict[builtins.str, typing.Any]],
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    ) -> None:
        '''
        :param scope: -
        :param dlz_account: 
        :param global_variables: 
        :param env: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7dfcab6f6ec52c4a0926cc31735046cf2ef46a1a9dc40f2c43c34b4cf2189a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        workload_account_props = WorkloadAccountProps(
            dlz_account=dlz_account,
            global_variables=global_variables,
            env=env,
            name=name,
            stage=stage,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props])


class WorkloadGlobalNetworkConnectionsPhase1Stack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadGlobalNetworkConnectionsPhase1Stack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param workload_account_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1d265f33a935e8443ccd2d1330910bb286227474064800ee15294875251c7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument workload_account_props", value=workload_account_props, expected_type=type_hints["workload_account_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props, props])

    @jsii.member(jsii_name="createPeeringRole")
    def create_peering_role(
        self,
        from_: typing.Union[DlzAccountNetwork, typing.Dict[builtins.str, typing.Any]],
        *,
        dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
        vpcs: typing.Sequence[typing.Union[NetworkEntityVpc, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param from_: -
        :param dlz_account: 
        :param vpcs: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdd2b0ee1a4b84882318c06b3ee48f28c5182b29fc13f5efe135af54ca72b69)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
        to = DlzAccountNetwork(dlz_account=dlz_account, vpcs=vpcs)

        return typing.cast(None, jsii.invoke(self, "createPeeringRole", [from_, to]))


class WorkloadGlobalNetworkConnectionsPhase2Stack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadGlobalNetworkConnectionsPhase2Stack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param workload_account_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e09cdc01f9793ceb52bb5063c355d15f995e93d78df12e8553620af7dc2f3e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument workload_account_props", value=workload_account_props, expected_type=type_hints["workload_account_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props, props])


class WorkloadGlobalNetworkConnectionsPhase3Stack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadGlobalNetworkConnectionsPhase3Stack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param workload_account_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53057bcbd88e07cea3272264f50b7c37d8a4ae07b0546463e4a5c520d6f4ddaa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument workload_account_props", value=workload_account_props, expected_type=type_hints["workload_account_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props, props])


class WorkloadGlobalStack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadGlobalStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param workload_account_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4208b0c483d8ba9649225a0315a8819854473fdf8868b3036d89f470666f5560)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument workload_account_props", value=workload_account_props, expected_type=type_hints["workload_account_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props, props])

    @jsii.member(jsii_name="defaultNotifications")
    def default_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "defaultNotifications", []))

    @jsii.member(jsii_name="ssmAssumeCrossAccountRole")
    def ssm_assume_cross_account_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "ssmAssumeCrossAccountRole", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="defaultPolicyStatement")
    def default_policy_statement(cls) -> _aws_cdk_aws_iam_ceddda9d.PolicyStatementProps:  # pyright: ignore [reportGeneralTypeIssues,reportRedeclaration]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyStatementProps, jsii.sget(cls, "defaultPolicyStatement"))

    @default_policy_statement.setter # type: ignore[no-redef]
    def default_policy_statement(
        cls,
        value: _aws_cdk_aws_iam_ceddda9d.PolicyStatementProps,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beed160bf521df0073ce2355ce338a06bc35b82bfe69f830dca1ce3e0c1b0c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "defaultPolicyStatement", value) # pyright: ignore[reportArgumentType]


class WorkloadRegionalDataServicesPhase1Stack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadRegionalDataServicesPhase1Stack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
        global_variables: typing.Union[GlobalVariables, typing.Dict[builtins.str, typing.Any]],
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    ) -> None:
        '''
        :param scope: -
        :param dlz_account: 
        :param global_variables: 
        :param env: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3755454ede4603ec3f6596b7165c14a39161d80d8b4804e8c2b43c0ac462ad5a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        workload_account_props = WorkloadAccountProps(
            dlz_account=dlz_account,
            global_variables=global_variables,
            env=env,
            name=name,
            stage=stage,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props])


class WorkloadRegionalNetworkConnectionsPhase2Stack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadRegionalNetworkConnectionsPhase2Stack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param workload_account_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85c90671bce3968e217dd8cd79827cf5678cf91c4278fc59ecb5957809dd30e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument workload_account_props", value=workload_account_props, expected_type=type_hints["workload_account_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props, props])


class WorkloadRegionalNetworkConnectionsPhase3Stack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadRegionalNetworkConnectionsPhase3Stack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param workload_account_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7a033738f5a5804d1cae45643733bb63975d3037d287c7706311b08523886b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument workload_account_props", value=workload_account_props, expected_type=type_hints["workload_account_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props, props])


class WorkloadRegionalStack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.WorkloadRegionalStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param workload_account_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc8999da777d0bfdc67eb72fb9d581b185a02f00387e3ecf61fd8ed85d9d6f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument workload_account_props", value=workload_account_props, expected_type=type_hints["workload_account_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, workload_account_props, props])


class AuditGlobalStack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.AuditGlobalStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        stack_props: typing.Union[DlzStackProps, typing.Dict[builtins.str, typing.Any]],
        *,
        budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
        local_profile: builtins.str,
        mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
        organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
        regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
        security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
        additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
        iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
        print_deployment_order: typing.Optional[builtins.bool] = None,
        print_report: typing.Optional[builtins.bool] = None,
        save_report: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param stack_props: -
        :param budgets: 
        :param local_profile: The the AWS CLI profile that will be used to run the Scripts. For the ``bootstrap`` script, this profile must be an Admin of the root management account and it must be able to assume the ``AWSControlTowerExecution`` role created by ControlTower. This is an extremely powerful set of credentials and should be treated with care. The permissions can be reduced for the everyday use of the ``diff`` and ``deploy`` scripts but the ``bootstrap`` script requires full admin access.
        :param mandatory_tags: The values of the mandatory tags that all resources must have. The following values are already specified and used by the DLZ constructs - Owner: [infra] - Project: [dlz] - Environment: [dlz]
        :param organization: 
        :param regions: 
        :param security_hub_notifications: 
        :param additional_mandatory_tags: List of additional mandatory tags that all resources must have. Not all resources support tags, this is a best-effort. Mandatory tags are defined in Defaults.mandatoryTags() which are: - Owner, the team responsible for the resource - Project, the project the resource is part of - Environment, the environment the resource is part of It creates: 1. A tag policy in the organization 2. An SCP on the organization that all CFN stacks must have these tags when created 3. An AWS Config rule that checks for these tags on all CFN stacks and resources For all stacks created by DLZ the following tags are applied: - Owner: infra - Project: dlz - Environment: dlz Default: Defaults.mandatoryTags()
        :param default_notification: Default notification settings for the organization. Allows you to define the email notfication settings or slack channel settings. If the account level defaultNotification is defined those will be used for the account instead of this defaultNotification which acts as the fallback.
        :param deny_service_list: List of services to deny in the organization SCP. If not specified, the default defined by Default: DataLandingZone.defaultDenyServiceList()
        :param deployment_platform: 
        :param iam_identity_center: IAM Identity Center configuration.
        :param iam_policy_permission_boundary: IAM Policy Permission Boundary.
        :param network: 
        :param print_deployment_order: Print the deployment order to the console. Default: true
        :param print_report: Print the report grouped by account, type and aggregated regions to the console. Default: true
        :param save_report: Save the raw report items and the reports grouped by account to a ``./.dlz-reports`` folder. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b7aa5602704918d8dcb377a5b1a7de4532dc40712aa0589f36bab688fecad1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stack_props", value=stack_props, expected_type=type_hints["stack_props"])
        props = DataLandingZoneProps(
            budgets=budgets,
            local_profile=local_profile,
            mandatory_tags=mandatory_tags,
            organization=organization,
            regions=regions,
            security_hub_notifications=security_hub_notifications,
            additional_mandatory_tags=additional_mandatory_tags,
            default_notification=default_notification,
            deny_service_list=deny_service_list,
            deployment_platform=deployment_platform,
            iam_identity_center=iam_identity_center,
            iam_policy_permission_boundary=iam_policy_permission_boundary,
            network=network,
            print_deployment_order=print_deployment_order,
            print_report=print_report,
            save_report=save_report,
        )

        jsii.create(self.__class__, self, [scope, stack_props, props])

    @jsii.member(jsii_name="securityHubNotifications")
    def security_hub_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "securityHubNotifications", []))


class AuditRegionalStack(
    DlzStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.AuditRegionalStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
        name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
        stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    ) -> None:
        '''
        :param scope: -
        :param env: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2643f4f27dbe64ea9341b69369726d6065441f40bdb0b7ed11726ddda951b377)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = DlzStackProps(env=env, name=name, stage=stage)

        jsii.create(self.__class__, self, [scope, props])


@jsii.data_type(
    jsii_type="aws-data-landing-zone.DataLandingZoneClientBastionProps",
    jsii_struct_bases=[DataLandingZoneClientProps],
    name_mapping={
        "account_name": "accountName",
        "region": "region",
        "bastion_name": "bastionName",
    },
)
class DataLandingZoneClientBastionProps(DataLandingZoneClientProps):
    def __init__(
        self,
        *,
        account_name: builtins.str,
        region: builtins.str,
        bastion_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: 
        :param region: 
        :param bastion_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec8b557f269181ebc2de3eba18225a9acefd49cec9a3602e1b4b135b962298d)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bastion_name", value=bastion_name, expected_type=type_hints["bastion_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "region": region,
        }
        if bastion_name is not None:
            self._values["bastion_name"] = bastion_name

    @builtins.property
    def account_name(self) -> builtins.str:
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bastion_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bastion_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLandingZoneClientBastionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IReportResource)
class DlzControlTowerEnabledControl(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzControlTowerEnabledControl",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        applied_ou: builtins.str,
        control: IDlzControlTowerControl,
        control_tower_account_id: builtins.str,
        control_tower_region: Region,
        organization_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param applied_ou: 
        :param control: 
        :param control_tower_account_id: 
        :param control_tower_region: 
        :param organization_id: 
        :param tags: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f82156470dc5012a4a499f3929373a1330e9ede934fea887ce7f0c959d5b40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DlzControlTowerEnabledControlProps(
            applied_ou=applied_ou,
            control=control,
            control_tower_account_id=control_tower_account_id,
            control_tower_region=control_tower_region,
            organization_id=organization_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="canBeAppliedToSecurityOU")
    @builtins.classmethod
    def can_be_applied_to_security_ou(
        cls,
        control: IDlzControlTowerControl,
    ) -> builtins.bool:
        '''Check if the control can be applied to the Security OU.

        Only LEGACY controls can be applied to the Security OU.

        :param control: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa17093d5f2a6f73a325c1116d6081300309814c489050df3cf3f9ee4073c428)
            check_type(argname="argument control", value=control, expected_type=type_hints["control"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "canBeAppliedToSecurityOU", [control]))

    @builtins.property
    @jsii.member(jsii_name="control")
    def control(self) -> _aws_cdk_aws_controltower_ceddda9d.CfnEnabledControl:
        return typing.cast(_aws_cdk_aws_controltower_ceddda9d.CfnEnabledControl, jsii.get(self, "control"))

    @builtins.property
    @jsii.member(jsii_name="reportResource")
    def report_resource(self) -> ReportResource:
        return typing.cast(ReportResource, jsii.get(self, "reportResource"))


@jsii.implements(IReportResource)
class DlzServiceControlPolicy(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzServiceControlPolicy",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        statements: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        :param statements: 
        :param description: 
        :param tags: 
        :param target_ids: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343f3857644dc5a42c82c96c4d1030f0299e3f275d60e048800763e30622f4db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DlzServiceControlPolicyProps(
            name=name,
            statements=statements,
            description=description,
            tags=tags,
            target_ids=target_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="denyCfnStacksWithoutStandardTags")
    @builtins.classmethod
    def deny_cfn_stacks_without_standard_tags(
        cls,
        tags: typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]],
    ) -> _aws_cdk_aws_iam_ceddda9d.PolicyStatement:
        '''
        :param tags: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb54e42cc3979524a125e7457d67f201377206833f72d2630d03bcc0d278243)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyStatement, jsii.sinvoke(cls, "denyCfnStacksWithoutStandardTags", [tags]))

    @jsii.member(jsii_name="denyIamPolicyActionStatements")
    @builtins.classmethod
    def deny_iam_policy_action_statements(
        cls,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement], jsii.sinvoke(cls, "denyIamPolicyActionStatements", []))

    @jsii.member(jsii_name="denyServiceActionStatements")
    @builtins.classmethod
    def deny_service_action_statements(
        cls,
        service_actions: typing.Sequence[builtins.str],
    ) -> _aws_cdk_aws_iam_ceddda9d.PolicyStatement:
        '''
        :param service_actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b7b5b08b50aca7ecd5a676843244d0895f6770f408351a8db1afe664372d4c)
            check_type(argname="argument service_actions", value=service_actions, expected_type=type_hints["service_actions"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyStatement, jsii.sinvoke(cls, "denyServiceActionStatements", [service_actions]))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> _aws_cdk_aws_organizations_ceddda9d.CfnPolicy:
        return typing.cast(_aws_cdk_aws_organizations_ceddda9d.CfnPolicy, jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="reportResource")
    def report_resource(self) -> ReportResource:
        return typing.cast(ReportResource, jsii.get(self, "reportResource"))


@jsii.implements(IReportResource)
class DlzTagPolicy(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-data-landing-zone.DlzTagPolicy",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        policy_tags: typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        :param policy_tags: 
        :param description: 
        :param tags: 
        :param target_ids: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e015201d6a8092a7bf0e52071f256aac6e7b6219ecce8348f7691ec8b617bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DlzTagPolicyProps(
            name=name,
            policy_tags=policy_tags,
            description=description,
            tags=tags,
            target_ids=target_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> _aws_cdk_aws_organizations_ceddda9d.CfnPolicy:
        return typing.cast(_aws_cdk_aws_organizations_ceddda9d.CfnPolicy, jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="reportResource")
    def report_resource(self) -> ReportResource:
        return typing.cast(ReportResource, jsii.get(self, "reportResource"))


@jsii.data_type(
    jsii_type="aws-data-landing-zone.ReportItem",
    jsii_struct_bases=[ReportResource],
    name_mapping={
        "description": "description",
        "external_link": "externalLink",
        "name": "name",
        "type": "type",
        "account_name": "accountName",
        "applied_from": "appliedFrom",
        "region": "region",
    },
)
class ReportItem(ReportResource):
    def __init__(
        self,
        *,
        description: builtins.str,
        external_link: builtins.str,
        name: builtins.str,
        type: ReportType,
        account_name: builtins.str,
        applied_from: builtins.str,
        region: builtins.str,
    ) -> None:
        '''
        :param description: 
        :param external_link: 
        :param name: 
        :param type: 
        :param account_name: 
        :param applied_from: 
        :param region: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d50a507299d2e3ce4428be5c55882552aee95930c19e0da595c3e4066455916)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_link", value=external_link, expected_type=type_hints["external_link"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument applied_from", value=applied_from, expected_type=type_hints["applied_from"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "external_link": external_link,
            "name": name,
            "type": type,
            "account_name": account_name,
            "applied_from": applied_from,
            "region": region,
        }

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_link(self) -> builtins.str:
        result = self._values.get("external_link")
        assert result is not None, "Required property 'external_link' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> ReportType:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(ReportType, result)

    @builtins.property
    def account_name(self) -> builtins.str:
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def applied_from(self) -> builtins.str:
        result = self._values.get("applied_from")
        assert result is not None, "Required property 'applied_from' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReportItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccountChatbots",
    "AuditGlobalStack",
    "AuditRegionalStack",
    "AuditStacks",
    "BaseSharedTagProps",
    "BastionHost",
    "BudgetSubscribers",
    "DLzAccount",
    "DLzManagementAccount",
    "DLzOrganization",
    "DataLandingZone",
    "DataLandingZoneClient",
    "DataLandingZoneClientBastionProps",
    "DataLandingZoneClientProps",
    "DataLandingZoneClientRouteTableIdProps",
    "DataLandingZoneClientSubnetIdProps",
    "DataLandingZoneClientVpcIdProps",
    "DataLandingZoneProps",
    "DatabaseAction",
    "Defaults",
    "DeploymentPlatform",
    "DeploymentPlatformGitHub",
    "DlzAccountNetwork",
    "DlzAccountNetworks",
    "DlzAccountType",
    "DlzBudget",
    "DlzBudgetProps",
    "DlzControlTowerControlFormat",
    "DlzControlTowerControlIdNameProps",
    "DlzControlTowerEnabledControl",
    "DlzControlTowerEnabledControlProps",
    "DlzControlTowerSpecializedControls",
    "DlzControlTowerStandardControls",
    "DlzLakeFormation",
    "DlzLakeFormationProps",
    "DlzRegions",
    "DlzRouteTableProps",
    "DlzServiceControlPolicy",
    "DlzServiceControlPolicyProps",
    "DlzSsmReader",
    "DlzSsmReaderStackCache",
    "DlzStack",
    "DlzStackNameProps",
    "DlzStackProps",
    "DlzSubnetProps",
    "DlzTag",
    "DlzTagPolicy",
    "DlzTagPolicyProps",
    "DlzVpc",
    "DlzVpcProps",
    "ForceNoPythonArgumentLifting",
    "GitHubReference",
    "GlobalVariables",
    "GlobalVariablesNcp1",
    "GlobalVariablesNcp2",
    "GlobalVariablesNcp3",
    "IDlzControlTowerControl",
    "IReportResource",
    "IamIdentityAccounts",
    "IamIdentityCenter",
    "IamIdentityCenterAccessGroupProps",
    "IamIdentityCenterGroup",
    "IamIdentityCenterGroupProps",
    "IamIdentityCenterGroupUser",
    "IamIdentityCenterPermissionSetProps",
    "IamIdentityCenterProps",
    "IamIdentityPermissionSets",
    "IamPolicyPermissionsBoundaryProps",
    "IdentityStoreUser",
    "IdentityStoreUserEmailsProps",
    "IdentityStoreUserNameProps",
    "IdentityStoreUserProps",
    "IdentityStoreUserPropsExt",
    "LFTag",
    "LFTagSharable",
    "LakePermission",
    "LogGlobalStack",
    "LogRegionalStack",
    "LogStacks",
    "ManagementStack",
    "MandatoryTags",
    "Network",
    "NetworkAddress",
    "NetworkConnection",
    "NetworkConnectionVpcPeering",
    "NetworkEntityRouteTable",
    "NetworkEntitySubnet",
    "NetworkEntityVpc",
    "NetworkNat",
    "NetworkNatGateway",
    "NetworkNatInstance",
    "NetworkNatType",
    "NotificationDetailsProps",
    "OrgOuSecurity",
    "OrgOuSecurityAccounts",
    "OrgOuSuspended",
    "OrgOuWorkloads",
    "OrgOus",
    "OrgRootAccounts",
    "Ou",
    "PartialOu",
    "Region",
    "Report",
    "ReportItem",
    "ReportResource",
    "ReportType",
    "RootOptions",
    "Scripts",
    "SecurityHubNotification",
    "SecurityHubNotificationProps",
    "SecurityHubNotificationSWorkflowStatus",
    "SecurityHubNotificationSeverity",
    "ShareProps",
    "SharedExternal",
    "SharedInternal",
    "SlackChannel",
    "TableAction",
    "TagAction",
    "WorkloadAccountProps",
    "WorkloadGlobalDataServicesPhase1Stack",
    "WorkloadGlobalNetworkConnectionsPhase1Stack",
    "WorkloadGlobalNetworkConnectionsPhase2Stack",
    "WorkloadGlobalNetworkConnectionsPhase3Stack",
    "WorkloadGlobalStack",
    "WorkloadRegionalDataServicesPhase1Stack",
    "WorkloadRegionalNetworkConnectionsPhase2Stack",
    "WorkloadRegionalNetworkConnectionsPhase3Stack",
    "WorkloadRegionalStack",
]

publication.publish()

def _typecheckingstub__3d75b413d9441f6011ff7a26ced44e3d3e131ffd42d93f7ab7d7fb91d1f50661(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    guardrail_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]] = None,
    logging_level: typing.Optional[_aws_cdk_aws_chatbot_ceddda9d.LoggingLevel] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    notification_topics: typing.Optional[typing.Sequence[_aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beb2f4f62037429f2d11a36471ad469e3affb167ffcac5a92fdb10f4a070a88(
    scope: _constructs_77d1e7e8.Construct,
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d79f537e6d9cfd7b530701576571f87bb131ef46e198f06d0aa23c9886303c(
    scope: _constructs_77d1e7e8.Construct,
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63801243c6145aee99d7be6a52e351bd62d8bc4f1d6dc07b7947ea344e10fece(
    value: typing.Mapping[builtins.str, _aws_cdk_aws_chatbot_ceddda9d.SlackChannelConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ca5436fcb484c55eec119b25d6a31d4eb5a0553d2eacb6f758de330d9cfbe5(
    *,
    global_: AuditGlobalStack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b559c6c485e7fdaa87214275f77db21c4be3aaf1bfc191cd62a9a6937b07261b(
    *,
    principals: typing.Sequence[builtins.str],
    specific_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2cb69a9750eb61b200f419207a31a68cee01d3348c0e4613150cb34d1e4cfd(
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    location: NetworkAddress,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282be6b5a9ccbee8083d992f0211e955891d27c0b48f2f574ab8e91d786addaa(
    *,
    emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    slack: typing.Optional[typing.Union[SlackChannel, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b344243292003fa647f9fb13ce28a54ff3b50dab37803f184c592fad2ee6478f(
    *,
    account_id: builtins.str,
    name: builtins.str,
    type: DlzAccountType,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    lake_formation: typing.Optional[typing.Sequence[typing.Union[DlzLakeFormationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpcs: typing.Optional[typing.Sequence[typing.Union[DlzVpcProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a19f78bcdb9bf21f1e19f607435a0bbb721d78633ea2243aeb6b20855317449(
    *,
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18589fd274506fd010b902ea469bde990dfacaf0004a299e29d6545e328eb158(
    *,
    organization_id: builtins.str,
    ous: typing.Union[OrgOus, typing.Dict[builtins.str, typing.Any]],
    root: typing.Union[RootOptions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b77304187f3a7eec71abe26e2f24630a339a7643aa355c54307d1ac8e16ecc(
    app: _aws_cdk_ceddda9d.App,
    props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8d8cfa804a878147787bce94ed7b000d79dea96a5035244df709f3e42dbfd6(
    value: AuditStacks,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7f4623d332e87faa8befdf0d19b5894aaab05539bbe35c13f1e7b5f32acacc(
    value: LogStacks,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1ef579c74a4708bdf38f6935a86f802d9e5ff60688e4ad8f839de0eddaa1c8(
    value: ManagementStack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8aa98ab0e13da9342ce4fb09cb9d06784dbfd05bb8c9055b87b90f1a22ac9bc(
    value: typing.List[WorkloadGlobalDataServicesPhase1Stack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a277403bafb3009ba04dd48c7f087d505d6fe225131886a50258944c94eecc2(
    value: typing.List[WorkloadGlobalNetworkConnectionsPhase1Stack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85f042a7a8a1ef2236e100ff174a3bcd7e861ba455d89073ee514c4267ac18b(
    value: typing.List[WorkloadGlobalNetworkConnectionsPhase2Stack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e227a57ecac9966da94c0e58510b51a9867e1f2f9811cad72a4af305e0a84392(
    value: typing.List[WorkloadGlobalNetworkConnectionsPhase3Stack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb0448902aed2ba432ac8ce3b5482a514437c0a81fb2a66be8a5b73b99c0264(
    value: typing.List[WorkloadGlobalStack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b6d85bde2374f0d011498bd1e186bb41abc7184486e2c42dff6a9aedcf1a66(
    value: typing.List[WorkloadRegionalDataServicesPhase1Stack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8db637c190c369de7d443a21a0abdf8bce7871238ff2f65be86638f1760bbee(
    value: typing.List[WorkloadRegionalNetworkConnectionsPhase2Stack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c26991a55be9b76068285c9aa0e8d85bcaad74035579d207f7d2d1ce0ad43e1(
    value: typing.List[WorkloadRegionalNetworkConnectionsPhase3Stack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a5540e11ebcf2d5a9662c974c122d507568ba798295da7581c14054a11460b(
    value: typing.List[WorkloadRegionalStack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14760a7e9daee1783371458d8eecbf8879764ca3635ba5b7527e49b73d2549e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bastion_name: typing.Optional[builtins.str] = None,
    account_name: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0170dd4979fb727a950e482bd3ec769c8231f76716d9896a8e41d2373b8d3c2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb969cefcf30682e210baa18fba5281c6cd8dc1fbc057c5cf66c06508822dae6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aee38186b48fb466a7b906bd6854f768db30be21e31d802f33999b500d6b617(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    route_table: builtins.str,
    vpc_name: builtins.str,
    account_name: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91adc9857eafe8793b09810f7f4809c71c044752b23610870539566bde3bf705(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    route_table: builtins.str,
    subnet_name: builtins.str,
    vpc_name: builtins.str,
    account_name: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01558c92dc56ea0868468c972083bf9301adf2cd2c8484cb7ef80a547efecc7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc_name: builtins.str,
    account_name: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f449134d3e1792b7f1f4320b7bd9b6965a4302c9bac0ba752f5802e5a1a996d0(
    *,
    account_name: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b5e979d27944d3a0cae7a0665939fd5788881938a8e78cf579da84f234d40f(
    *,
    account_name: builtins.str,
    region: builtins.str,
    route_table: builtins.str,
    vpc_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09352a173f9149cf4e1ff39d20ae951eaa4345a58b2bbeb815cea35090eb2c87(
    *,
    account_name: builtins.str,
    region: builtins.str,
    route_table: builtins.str,
    subnet_name: builtins.str,
    vpc_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6fd60032038fee1a643f3f5d4a856840d347c5bfa5778e2a370fdb243cff02(
    *,
    account_name: builtins.str,
    region: builtins.str,
    vpc_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bd8adbb27064bd1c139bab0940042c73398d282308158866d9a650ef5390ad(
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb302fd608aa006f4b4741f0e5897bb244b6b7e9fe38b5a7ec48177953596cbc(
    org_total: jsii.Number,
    infra_dlz: jsii.Number,
    *,
    emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    slack: typing.Optional[typing.Union[SlackChannel, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ebc403b477ed4f716493d8c533b5abe6b553a5f790054e162427f71d32ddad(
    third_octet_mask: jsii.Number,
    region: Region,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f044dcbb477c02103b334166b1e5bca4b76efdfa31dacc2eded0247ab4d40be7(
    *,
    git_hub: typing.Optional[typing.Union[DeploymentPlatformGitHub, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5005427f43f51b96b1589b0a588b2cfc8497aa93892aead054d80cfd827a6c87(
    *,
    references: typing.Sequence[typing.Union[GitHubReference, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512e485c7ab01d7cef0c5f99c0e820955310f24bb0020f5ceda8189e1f2f5280(
    *,
    dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
    vpcs: typing.Sequence[typing.Union[NetworkEntityVpc, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb530e1229f02fd59610813d10c92642a5ba4a9ecc869e8eff7c025f92b6d6b(
    dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
    *,
    address: NetworkAddress,
    route_tables: typing.Sequence[typing.Union[NetworkEntityRouteTable, typing.Dict[builtins.str, typing.Any]]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.CfnVPC,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7ded183cf91cea2d37994735f20379d6769e6583eca362598f16d2dedda1ac(
    network_address: NetworkAddress,
    match_on_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f1244110d2fd7ecaf753ef011c7fa503aa48b98d70664100b5311886824052(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    amount: jsii.Number,
    name: builtins.str,
    subscribers: typing.Union[BudgetSubscribers, typing.Dict[builtins.str, typing.Any]],
    for_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c79cf48597aa3bcfab58f9fd6e3cd61e3c18a49a7910a4275a6a24b93184379(
    *,
    amount: jsii.Number,
    name: builtins.str,
    subscribers: typing.Union[BudgetSubscribers, typing.Dict[builtins.str, typing.Any]],
    for_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c86c3b125e32a441f79170b43d426a3dcb7c3fa6914c1b1e598564d4645f9d(
    *,
    eu_west1: builtins.str,
    us_east1: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f901129156101ff8fda3b28b4d50e412e0cfa7d9799278300679bd46e6d978(
    *,
    applied_ou: builtins.str,
    control: IDlzControlTowerControl,
    control_tower_account_id: builtins.str,
    control_tower_region: Region,
    organization_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58099e8819e666b11f3bb86b027f9ee73dd9c920541175f77b5cf7f83bb3221b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    admins: typing.Sequence[builtins.str],
    permissions: typing.Sequence[typing.Union[LakePermission, typing.Dict[builtins.str, typing.Any]]],
    region: Region,
    tags: typing.Sequence[typing.Union[LFTagSharable, typing.Dict[builtins.str, typing.Any]]],
    cross_account_version: typing.Optional[jsii.Number] = None,
    hybrid_mode: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b953472db56618beed88515ddf1867ef2ae2d9efaf7e48fe25f5c307a8c39f27(
    *,
    admins: typing.Sequence[builtins.str],
    permissions: typing.Sequence[typing.Union[LakePermission, typing.Dict[builtins.str, typing.Any]]],
    region: Region,
    tags: typing.Sequence[typing.Union[LFTagSharable, typing.Dict[builtins.str, typing.Any]]],
    cross_account_version: typing.Optional[jsii.Number] = None,
    hybrid_mode: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8690f9a9ede108c6bcdaf9ac39351278b758b89f49947a520acb7a43d28e996(
    *,
    global_: Region,
    regional: typing.Sequence[Region],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d550fdadc16deef3c3fa519fc8fe6ae66ec1100359faff47b2cabc491962abce(
    *,
    name: builtins.str,
    subnets: typing.Sequence[typing.Union[DlzSubnetProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339e74dad0d62fcf661f597315cddbc97479e01ae0aac9a889b70b3f7530a7f7(
    *,
    name: builtins.str,
    statements: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a750ebf35f5b18890d68a60379e4fd4a6623af7c34f4dfc5976df7b7e216728(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    account_id: builtins.str,
    region: builtins.str,
    name: builtins.str,
    fetch_type: typing.Optional[builtins.str] = None,
    with_decryption: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff738bdc23336d5dfb4f61d6f358f5b502a9b9117a546ddb1014ac82b15f473e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    account_id: builtins.str,
    region: builtins.str,
    name: builtins.str,
    fetch_type: typing.Optional[builtins.str] = None,
    with_decryption: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5675fcb2f9b9558df55bcbabc917f8c3af2fd22e59753e170f23a892fab52571(
    scope: _constructs_77d1e7e8.Construct,
    *,
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44f8fc940b0c8025f281d43de49eb64ce0e725bde84b7c499e42605259bd239(
    exported_value: typing.Any,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7aaacd505d6d9c4f34e64a62dc72f113097deb45d69c02f0c8ea41859b7957(
    resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54aa0affd8f5d154af48a1b55ba11c9f04d5e896247b3e19d65cedecb9499af(
    *,
    region: builtins.str,
    stack: builtins.str,
    account: typing.Optional[builtins.str] = None,
    ou: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ced4c8941535fc8ecdb8829ab9e3d868f46668eac861f5eeee5eab8121dde11(
    *,
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14071e2e7b1beecaffa587aa061908789508df30ab0a2c5904b8b455202bbcf7(
    *,
    cidr: builtins.str,
    name: builtins.str,
    az: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f26963db2ae43eedfd364e6a59a2cbde80c46ae927a969354aef6437e213b3(
    *,
    name: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33502afb73bb9e9b8b9242e3297ae17f0b78d08d6c168ea7509982cefcbe648c(
    *,
    name: builtins.str,
    policy_tags: typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc864233a41939de528d6ea19dfa0d68821e458d7a785701873c2750716cf96(
    dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
    dlz_stack: DlzStack,
    dlz_vpc: typing.Union[DlzVpcProps, typing.Dict[builtins.str, typing.Any]],
    network_nats: typing.Optional[typing.Sequence[typing.Union[NetworkNat, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7486cc9fc6f87493ab652a743b15c22d0bd06d03597e324eabccf3ec18b63a40(
    *,
    cidr: builtins.str,
    name: builtins.str,
    region: Region,
    route_tables: typing.Sequence[typing.Union[DlzRouteTableProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e0ef86c3068d0b854aa83d4f1b59acc0d2885df25802c71f8b6205c3f03497(
    *,
    owner: builtins.str,
    repo: builtins.str,
    filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0155b91147435bd7f83ea1bf2a259a429f49c29f38904ac043ceb3f22c1303cf(
    *,
    dlz_account_networks: DlzAccountNetworks,
    ncp1: typing.Union[GlobalVariablesNcp1, typing.Dict[builtins.str, typing.Any]],
    ncp2: typing.Union[GlobalVariablesNcp2, typing.Dict[builtins.str, typing.Any]],
    ncp3: typing.Union[GlobalVariablesNcp3, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3037077464cb9af3024fd58894d08534c6be30f5e5a8f73f218bf251669e4c0c(
    *,
    vpc_peering_role_keys: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de59b0f0ec5b2ff47010678d6b47a111ea30c0f55007d5eeba3b0b95b12354b8(
    *,
    owner_vpc_ids: DlzSsmReaderStackCache,
    peering_connections: typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.CfnVPCPeeringConnection],
    peering_role_arns: DlzSsmReaderStackCache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87b00f355d35a5e2dba8d710842de061a9db204d166101735f3cdac4cb7eb73(
    *,
    route_tables_ssm_cache: DlzSsmReaderStackCache,
    vpc_peering_connection_ids: DlzSsmReaderStackCache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6069fd6f28c7b582fe6a9e53e2daece20c8d6fd0480e8da5b1cdd6d28b6de979(
    dlz_stack: DlzStack,
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    *,
    arn: builtins.str,
    id: builtins.str,
    store_id: builtins.str,
    access_groups: typing.Optional[typing.Sequence[typing.Union[IamIdentityCenterAccessGroupProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    permission_sets: typing.Optional[typing.Sequence[typing.Union[IamIdentityCenterPermissionSetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    users: typing.Optional[typing.Sequence[typing.Union[IdentityStoreUserProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3737a13593afab1af80a835eca002d158ea1d0ddd47b2f5b453501c060ce6d9d(
    *,
    account_names: typing.Sequence[builtins.str],
    name: builtins.str,
    permission_set_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf381d25cf7d4c2cc6a890f27f3ff8112a5d20d026d99608a183065947d17d01(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    accounts: typing.Sequence[builtins.str],
    identity_store_id: builtins.str,
    name: builtins.str,
    permission_set: _aws_cdk_aws_sso_ceddda9d.CfnPermissionSet,
    sso_arn: builtins.str,
    users: typing.Sequence[typing.Union[IamIdentityCenterGroupUser, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cffd81a956e1c484ae6938e53f3059990c30fd868bcef8cc2f8bcdf02d36f8(
    *,
    accounts: typing.Sequence[builtins.str],
    identity_store_id: builtins.str,
    name: builtins.str,
    permission_set: _aws_cdk_aws_sso_ceddda9d.CfnPermissionSet,
    sso_arn: builtins.str,
    users: typing.Sequence[typing.Union[IamIdentityCenterGroupUser, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4d113e8de3c819ea64049ef4ecdd94bf0bd4c7f073c1108fb83d9c5a42d176(
    *,
    user_id: builtins.str,
    user_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a293b93390461ef7e7d9b1b438f936e46703143de016f19627bb0f53bb4600(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    inline_policy_statement: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyStatement] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_boundary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    session_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d53e4270ba7108bc74b395e1cffc1d1641584d585582b9f4d7faae37db1576c(
    *,
    arn: builtins.str,
    id: builtins.str,
    store_id: builtins.str,
    access_groups: typing.Optional[typing.Sequence[typing.Union[IamIdentityCenterAccessGroupProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    permission_sets: typing.Optional[typing.Sequence[typing.Union[IamIdentityCenterPermissionSetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    users: typing.Optional[typing.Sequence[typing.Union[IdentityStoreUserProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa1ebd0e004c4d731c7a8b9904e55f5a3f2323e96551e478958a2fb249f8762(
    *,
    policy_statement: typing.Union[_aws_cdk_aws_iam_ceddda9d.PolicyStatementProps, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212948c252d85e1c740c847bb3da25b0c6546c2944f3a557a2401e201f962874(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    display_name: builtins.str,
    email: typing.Union[IdentityStoreUserEmailsProps, typing.Dict[builtins.str, typing.Any]],
    identity_store_id: builtins.str,
    name: typing.Union[IdentityStoreUserNameProps, typing.Dict[builtins.str, typing.Any]],
    user_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5fdcdaf1cbd4062e1f15ec5f89804de2aad2a692933a24c73a6277c37fe1ce(
    *,
    type: builtins.str,
    value: builtins.str,
    primary: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb68731a1540f928babde3bd9479adf50a83ad91f8919f01c91396c7345d806(
    *,
    family_name: builtins.str,
    formatted: builtins.str,
    given_name: builtins.str,
    honorific_prefix: typing.Optional[builtins.str] = None,
    honorific_suffix: typing.Optional[builtins.str] = None,
    middle_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04930dd85e755e2d6af07e4203ccd2dd864b8d8bf9306521c4d18e48cbec3228(
    *,
    name: builtins.str,
    surname: builtins.str,
    user_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729785b0f4f0054bacb120036ec98908185e34e32fc2c1b138fe021a185eaf1d(
    *,
    display_name: builtins.str,
    email: typing.Union[IdentityStoreUserEmailsProps, typing.Dict[builtins.str, typing.Any]],
    identity_store_id: builtins.str,
    name: typing.Union[IdentityStoreUserNameProps, typing.Dict[builtins.str, typing.Any]],
    user_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94a03f25837494d40a0166756b67590aa4f3ddd2f9ec960e6c64f72903d3ef6(
    *,
    tag_key: builtins.str,
    tag_values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0a32854356a8e5cb6db695bab6838d4317df838e0398df9e9bd54b66980fae(
    *,
    tag_key: builtins.str,
    tag_values: typing.Sequence[builtins.str],
    share: typing.Optional[typing.Union[ShareProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741c7525e6c48e0f33c59d67c0cf6c154351deafad9062dd517b33be993570a6(
    *,
    database_actions: typing.Sequence[DatabaseAction],
    principals: typing.Sequence[builtins.str],
    tags: typing.Sequence[typing.Union[LFTag, typing.Dict[builtins.str, typing.Any]]],
    database_actions_with_grant: typing.Optional[typing.Sequence[DatabaseAction]] = None,
    table_actions: typing.Optional[typing.Sequence[TableAction]] = None,
    table_actions_with_grant: typing.Optional[typing.Sequence[TableAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720e79ae794a29ad346c0022819309dba88ebc4a048caa4f8d4947844b9c56c5(
    scope: _constructs_77d1e7e8.Construct,
    *,
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f2b10d5e07ab0640a966ed0e138ac233a48dfc8318910e40cce6a7a8cf8e40(
    scope: _constructs_77d1e7e8.Construct,
    *,
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d69f61e690c5df8ed09485eb394157170fdb81b4178db4b123a67b356f4938(
    scope: _constructs_77d1e7e8.Construct,
    stack_props: typing.Union[DlzStackProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785d4d277df5b1660a9532d1cfb85da5b40cded4cbac9d82e8bfe551449a74d2(
    *,
    environment: typing.Sequence[builtins.str],
    owner: typing.Sequence[builtins.str],
    project: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112a25d4b6227cb0a6c04a06c1217ddef8adfe64820a82b120dd719d1a9a5a7e(
    *,
    bastion_hosts: typing.Optional[typing.Sequence[typing.Union[BastionHost, typing.Dict[builtins.str, typing.Any]]]] = None,
    connections: typing.Optional[typing.Union[NetworkConnection, typing.Dict[builtins.str, typing.Any]]] = None,
    nats: typing.Optional[typing.Sequence[typing.Union[NetworkNat, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4797252545276129c66b07c9e6958c7c9323a09c9fe7556964b1ac32b0ca79f2(
    account: builtins.str,
    region: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[builtins.str] = None,
    route_table: typing.Optional[builtins.str] = None,
    subnet: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccefa74d81aa3039300d6e0d5a6d669ad1a9106dddde0f73715a7040925e6341(
    props: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d644760208a526116d94f74d430798c804f5cdb88a2923f168f82bec17f8b2ed(
    other: NetworkAddress,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e136f40784f5abbaba433b1b5f84fbf67b51e92245cacc63f9d7747b7a744a7(
    *,
    vpc_peering: typing.Sequence[typing.Union[NetworkConnectionVpcPeering, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe835250156aeaa207e060e70cc219cd51331f50d00e6197cd10099c73d4ee5(
    *,
    destination: NetworkAddress,
    source: NetworkAddress,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b85423ba33fe52684a4c7c02199fa8988477ddd396b0685a33cf42dec51ed1(
    *,
    address: NetworkAddress,
    route_table: _aws_cdk_aws_ec2_ceddda9d.CfnRouteTable,
    subnets: typing.Sequence[typing.Union[NetworkEntitySubnet, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cba2945d93c18c494e150c68ca0c73597d4ab3679e1d501b859d93e95323fc4(
    *,
    address: NetworkAddress,
    subnet: _aws_cdk_aws_ec2_ceddda9d.CfnSubnet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f49f7dbf2c409a299c1bcf24ba217dd26f3d81b8558efa09818341a7e6b106(
    *,
    address: NetworkAddress,
    route_tables: typing.Sequence[typing.Union[NetworkEntityRouteTable, typing.Dict[builtins.str, typing.Any]]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.CfnVPC,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b52f8661cab04102c607b79e74e7156e0dbdcb50edbdefaf1aaa5ba830acb28(
    *,
    allow_access_from: typing.Sequence[NetworkAddress],
    location: NetworkAddress,
    name: builtins.str,
    type: typing.Union[NetworkNatType, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55cb6d0b5850b86e263d952cf073d6b5812ff49c926be806386269bd9c6e8e3(
    *,
    eip: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc63f643c5aaf3aa3fab3e40997f4e5c00106f791cbe395682f8acf0dbb57b66(
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    eip: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnEIPProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630d95da854f2caf4c6788bd7758e4b4169a0cd16d6ad906f2f1274ed8de85d5(
    *,
    gateway: typing.Optional[typing.Union[NetworkNatGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    instance: typing.Optional[typing.Union[NetworkNatInstance, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af70c422a041a832d88717146a8aefbbd5baec30108b8da3bd257605dcbf5a6b(
    *,
    emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    slack: typing.Optional[typing.Union[SlackChannel, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f34e757cce49396a45cbfc7ead91e5c7dce3c2d76c2e4b0bd7da2b39745295(
    *,
    accounts: typing.Union[OrgOuSecurityAccounts, typing.Dict[builtins.str, typing.Any]],
    ou_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f29b2b57c9ddd33d371990ce96f70dcdc72df3857c74315a1fd1ffb46803bcb(
    *,
    audit: typing.Union[DLzManagementAccount, typing.Dict[builtins.str, typing.Any]],
    log: typing.Union[DLzManagementAccount, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4573748c48dc91941ec335b61a6e324a01d9062b5fcb4c4f5f1429d9c2a6e4a(
    *,
    ou_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d03ce67a3c30402794278f91346790936b6174e4002bf766fda9cc90fdaa7f(
    *,
    accounts: typing.Sequence[typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]]],
    ou_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e17514f4d2625b6cc5fa1419d3f2b35daa43ff1ea54148d2e42ea833e6e70ab(
    *,
    security: typing.Union[OrgOuSecurity, typing.Dict[builtins.str, typing.Any]],
    suspended: typing.Union[OrgOuSuspended, typing.Dict[builtins.str, typing.Any]],
    workloads: typing.Union[OrgOuWorkloads, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606ce365c1ad865f5392055804622d3b5b4d0ddd5600d5abba5c366218405bf5(
    *,
    management: typing.Union[DLzManagementAccount, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36ba8cd3f05ce17a729fa92f765c69c2671d05a45519f8bdf5b1bb4c0347894(
    *,
    ou_id: builtins.str,
    accounts: typing.Optional[typing.Sequence[typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc449229300537412606dd27e8a89c496d8053bd1277601326c955bb9c765cb(
    account_name: builtins.str,
    region: builtins.str,
    *,
    description: builtins.str,
    external_link: builtins.str,
    name: builtins.str,
    type: ReportType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e5973b06d1aff0aca71eeea28d66b88f909cb86e0427f279b90c7bec79413d(
    account_name: builtins.str,
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    *,
    description: builtins.str,
    external_link: builtins.str,
    name: builtins.str,
    type: ReportType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f47a0bacec1440d23980b20c3a352762f29c2cb3c62f635f9c90d93a048b49(
    partial_ou: typing.Union[PartialOu, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    *,
    description: builtins.str,
    external_link: builtins.str,
    name: builtins.str,
    type: ReportType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da4e845f0e288eab548c0a1b8103817635fbeb580550a21f4e52571cd071171(
    security_ou: typing.Union[OrgOuSecurity, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    *,
    description: builtins.str,
    external_link: builtins.str,
    name: builtins.str,
    type: ReportType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856f2b03255b0804a51c67f00f543e51cec490d9ec33c1e7476dbafdf55a3617(
    value: typing.List[ReportItem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bef332105b230c86aaf0a7b69fb27bab248377f1547f308c0cf8f68e128783(
    *,
    description: builtins.str,
    external_link: builtins.str,
    name: builtins.str,
    type: ReportType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6607c7d387d6e944e5632eec7f93574b7d98c934d4512dcfca5429b25022cb(
    *,
    accounts: typing.Union[OrgRootAccounts, typing.Dict[builtins.str, typing.Any]],
    controls: typing.Optional[typing.Sequence[DlzControlTowerStandardControls]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc9bc9aae2524a3bab49c1aad2f44c3334432f02eef685410ff1463184b64d6(
    props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
    bootstrap_role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c549b7d6c4faf3759ade9a1f2b24c58d365a09fe522e820c098b90ff75dfb1ee(
    props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05e9b7fddb47e361ba40d610b2d338af4e3371273b1131c3e321732bb5a22b3(
    props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544619e03e32ce22b6368ba8d8d58c9bdea6e8535aed76a325f294befb225ae7(
    props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c13acfd0b5dfa172519cdfaf97422c384054cfebb740d77ab7eb396c59d259(
    props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6696a886afc4754fe7591025ce14d98042ca7b767f3a1e325589a50907b2198f(
    props: typing.Union[DataLandingZoneProps, typing.Dict[builtins.str, typing.Any]],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e854a03d546ed12020dfb78447f9f686114130cc4f3098c32be960de4e3c598c(
    *,
    id: builtins.str,
    notification: typing.Union[SecurityHubNotificationProps, typing.Dict[builtins.str, typing.Any]],
    severity: typing.Optional[typing.Sequence[SecurityHubNotificationSeverity]] = None,
    workflow_status: typing.Optional[typing.Sequence[SecurityHubNotificationSWorkflowStatus]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997c41afa8168361be6a92beb218300fca22fd51ee75c7689ae20b2452421107(
    *,
    emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    slack: typing.Optional[typing.Union[SlackChannel, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f486fdddb8882f5cfc65103fba2e9564c68c613fa8e6f4a647b2d7c479488c1(
    *,
    with_external_account: typing.Optional[typing.Sequence[typing.Union[SharedExternal, typing.Dict[builtins.str, typing.Any]]]] = None,
    within_account: typing.Optional[typing.Sequence[typing.Union[SharedInternal, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8933cd307fea6cae69e46193541fb6f4719526676560978d1b02a84dee49d1b(
    *,
    principals: typing.Sequence[builtins.str],
    specific_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_actions: typing.Sequence[TagAction],
    tag_actions_with_grant: typing.Optional[typing.Sequence[TagAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d8d1f8a6a3c10cf19eaac05e1d67906bae08567ed72e2bc2b68e71cc614c9a(
    *,
    principals: typing.Sequence[builtins.str],
    specific_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_actions: typing.Sequence[TagAction],
    tag_actions_with_grant: typing.Optional[typing.Sequence[TagAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3338a132d632cd1a36dc4507ebe49513af577cd8fbb3e489ef39911da0f577e9(
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760bd95205aea37f01978923f411d9f8dbda399f17b1efb4f1e88a4f333cfc84(
    *,
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
    dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
    global_variables: typing.Union[GlobalVariables, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7dfcab6f6ec52c4a0926cc31735046cf2ef46a1a9dc40f2c43c34b4cf2189a(
    scope: _constructs_77d1e7e8.Construct,
    *,
    dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
    global_variables: typing.Union[GlobalVariables, typing.Dict[builtins.str, typing.Any]],
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1d265f33a935e8443ccd2d1330910bb286227474064800ee15294875251c7a(
    scope: _constructs_77d1e7e8.Construct,
    workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdd2b0ee1a4b84882318c06b3ee48f28c5182b29fc13f5efe135af54ca72b69(
    from_: typing.Union[DlzAccountNetwork, typing.Dict[builtins.str, typing.Any]],
    *,
    dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
    vpcs: typing.Sequence[typing.Union[NetworkEntityVpc, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e09cdc01f9793ceb52bb5063c355d15f995e93d78df12e8553620af7dc2f3e0(
    scope: _constructs_77d1e7e8.Construct,
    workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53057bcbd88e07cea3272264f50b7c37d8a4ae07b0546463e4a5c520d6f4ddaa(
    scope: _constructs_77d1e7e8.Construct,
    workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4208b0c483d8ba9649225a0315a8819854473fdf8868b3036d89f470666f5560(
    scope: _constructs_77d1e7e8.Construct,
    workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beed160bf521df0073ce2355ce338a06bc35b82bfe69f830dca1ce3e0c1b0c7d(
    value: _aws_cdk_aws_iam_ceddda9d.PolicyStatementProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3755454ede4603ec3f6596b7165c14a39161d80d8b4804e8c2b43c0ac462ad5a(
    scope: _constructs_77d1e7e8.Construct,
    *,
    dlz_account: typing.Union[DLzAccount, typing.Dict[builtins.str, typing.Any]],
    global_variables: typing.Union[GlobalVariables, typing.Dict[builtins.str, typing.Any]],
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85c90671bce3968e217dd8cd79827cf5678cf91c4278fc59ecb5957809dd30e(
    scope: _constructs_77d1e7e8.Construct,
    workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7a033738f5a5804d1cae45643733bb63975d3037d287c7706311b08523886b(
    scope: _constructs_77d1e7e8.Construct,
    workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc8999da777d0bfdc67eb72fb9d581b185a02f00387e3ecf61fd8ed85d9d6f0(
    scope: _constructs_77d1e7e8.Construct,
    workload_account_props: typing.Union[WorkloadAccountProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b7aa5602704918d8dcb377a5b1a7de4532dc40712aa0589f36bab688fecad1(
    scope: _constructs_77d1e7e8.Construct,
    stack_props: typing.Union[DlzStackProps, typing.Dict[builtins.str, typing.Any]],
    *,
    budgets: typing.Sequence[typing.Union[DlzBudgetProps, typing.Dict[builtins.str, typing.Any]]],
    local_profile: builtins.str,
    mandatory_tags: typing.Union[MandatoryTags, typing.Dict[builtins.str, typing.Any]],
    organization: typing.Union[DLzOrganization, typing.Dict[builtins.str, typing.Any]],
    regions: typing.Union[DlzRegions, typing.Dict[builtins.str, typing.Any]],
    security_hub_notifications: typing.Sequence[typing.Union[SecurityHubNotification, typing.Dict[builtins.str, typing.Any]]],
    additional_mandatory_tags: typing.Optional[typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_notification: typing.Optional[typing.Union[NotificationDetailsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_service_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_platform: typing.Optional[typing.Union[DeploymentPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_identity_center: typing.Optional[typing.Union[IamIdentityCenterProps, typing.Dict[builtins.str, typing.Any]]] = None,
    iam_policy_permission_boundary: typing.Optional[typing.Union[IamPolicyPermissionsBoundaryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[Network, typing.Dict[builtins.str, typing.Any]]] = None,
    print_deployment_order: typing.Optional[builtins.bool] = None,
    print_report: typing.Optional[builtins.bool] = None,
    save_report: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2643f4f27dbe64ea9341b69369726d6065441f40bdb0b7ed11726ddda951b377(
    scope: _constructs_77d1e7e8.Construct,
    *,
    env: typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]],
    name: typing.Union[DlzStackNameProps, typing.Dict[builtins.str, typing.Any]],
    stage: _cdk_express_pipeline_9801c4a1.ExpressStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec8b557f269181ebc2de3eba18225a9acefd49cec9a3602e1b4b135b962298d(
    *,
    account_name: builtins.str,
    region: builtins.str,
    bastion_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f82156470dc5012a4a499f3929373a1330e9ede934fea887ce7f0c959d5b40(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    applied_ou: builtins.str,
    control: IDlzControlTowerControl,
    control_tower_account_id: builtins.str,
    control_tower_region: Region,
    organization_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa17093d5f2a6f73a325c1116d6081300309814c489050df3cf3f9ee4073c428(
    control: IDlzControlTowerControl,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343f3857644dc5a42c82c96c4d1030f0299e3f275d60e048800763e30622f4db(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    statements: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb54e42cc3979524a125e7457d67f201377206833f72d2630d03bcc0d278243(
    tags: typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b7b5b08b50aca7ecd5a676843244d0895f6770f408351a8db1afe664372d4c(
    service_actions: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e015201d6a8092a7bf0e52071f256aac6e7b6219ecce8348f7691ec8b617bd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    policy_tags: typing.Sequence[typing.Union[DlzTag, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d50a507299d2e3ce4428be5c55882552aee95930c19e0da595c3e4066455916(
    *,
    description: builtins.str,
    external_link: builtins.str,
    name: builtins.str,
    type: ReportType,
    account_name: builtins.str,
    applied_from: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
