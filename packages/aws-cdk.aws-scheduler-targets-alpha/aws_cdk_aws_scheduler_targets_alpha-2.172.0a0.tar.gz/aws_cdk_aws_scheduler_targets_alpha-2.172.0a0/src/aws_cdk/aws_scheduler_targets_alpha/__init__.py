r'''
# Amazon EventBridge Scheduler Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they
> become stable. We will only make breaking changes to address unforeseen API issues. Therefore,
> these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes
> will be announced in release notes. This means that while you may use them, you may need to
> update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[Amazon EventBridge Scheduler](https://aws.amazon.com/blogs/compute/introducing-amazon-eventbridge-scheduler/) is a feature from Amazon EventBridge
that allows you to create, run, and manage scheduled tasks at scale. With EventBridge Scheduler, you can schedule millions of one-time or recurring tasks across various AWS services without provisioning or managing underlying infrastructure.

This library contains integration classes for Amazon EventBridge Scheduler to call any
number of supported AWS Services.

The following targets are supported:

1. `targets.LambdaInvoke`: [Invoke an AWS Lambda function](#invoke-a-lambda-function)
2. `targets.StepFunctionsStartExecution`: [Start an AWS Step Function](#start-an-aws-step-function)
3. `targets.CodeBuildStartBuild`: [Start a CodeBuild job](#start-a-codebuild-job)
4. `targets.SqsSendMessage`: [Send a Message to an Amazon SQS Queue](#send-a-message-to-an-sqs-queue)
5. `targets.SnsPublish`: [Publish messages to an Amazon SNS topic](#publish-messages-to-an-amazon-sns-topic)
6. `targets.EventBridgePutEvents`: [Put Events on EventBridge](#send-events-to-an-eventbridge-event-bus)
7. `targets.InspectorStartAssessmentRun`: [Start an Amazon Inspector assessment run](#start-an-amazon-inspector-assessment-run)
8. `targets.KinesisStreamPutRecord`: [Put a record to an Amazon Kinesis Data Stream](#put-a-record-to-an-amazon-kinesis-data-stream)
9. `targets.KinesisDataFirehosePutRecord`: [Put a record to a Kinesis Data Firehose](#put-a-record-to-a-kinesis-data-firehose)
10. `targets.CodePipelineStartPipelineExecution`: [Start a CodePipeline execution](#start-a-codepipeline-execution)
11. `targets.SageMakerStartPipelineExecution`: [Start a SageMaker pipeline execution](#start-a-sagemaker-pipeline-execution)

## Invoke a Lambda function

Use the `LambdaInvoke` target to invoke a lambda function.

The code snippet below creates an event rule with a Lambda function as a target
called every hour by EventBridge Scheduler with a custom payload. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
import aws_cdk.aws_lambda as lambda_


fn = lambda_.Function(self, "MyFunc",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_inline("exports.handler = handler.toString()")
)

dlq = sqs.Queue(self, "DLQ",
    queue_name="MyDLQ"
)

target = targets.LambdaInvoke(fn,
    dead_letter_queue=dlq,
    max_event_age=Duration.minutes(1),
    retry_attempts=3,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    })
)

schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=target
)
```

## Start an AWS Step Function

Use the `StepFunctionsStartExecution` target to start a new execution on a StepFunction.

The code snippet below creates an event rule with a Step Function as a target
called every hour by EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks


payload = {
    "Name": "MyParameter",
    "Value": "🌥️"
}

put_parameter_step = tasks.CallAwsService(self, "PutParameter",
    service="ssm",
    action="putParameter",
    iam_resources=["*"],
    parameters={
        "Name.$": "$.Name",
        "Value.$": "$.Value",
        "Type": "String",
        "Overwrite": True
    }
)

state_machine = sfn.StateMachine(self, "StateMachine",
    definition_body=sfn.DefinitionBody.from_chainable(put_parameter_step)
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=targets.StepFunctionsStartExecution(state_machine,
        input=ScheduleTargetInput.from_object(payload)
    )
)
```

## Start a CodeBuild job

Use the `CodeBuildStartBuild` target to start a new build run on a CodeBuild project.

The code snippet below creates an event rule with a CodeBuild project as target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_codebuild as codebuild

# project: codebuild.Project


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.CodeBuildStartBuild(project)
)
```

## Send a Message To an SQS Queue

Use the `SqsSendMessage` target to send a message to an SQS Queue.

The code snippet below creates an event rule with an SQS Queue as a target
called every hour by EventBridge Scheduler with a custom payload.

Contains the `messageGroupId` to use when the target is a FIFO queue. If you specify
a FIFO queue as a target, the queue must have content-based deduplication enabled.

```python
payload = "test"
message_group_id = "id"
queue = sqs.Queue(self, "MyQueue",
    fifo=True,
    content_based_deduplication=True
)

target = targets.SqsSendMessage(queue,
    input=ScheduleTargetInput.from_text(payload),
    message_group_id=message_group_id
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(1)),
    target=target
)
```

## Publish messages to an Amazon SNS topic

Use the `SnsPublish` target to publish messages to an Amazon SNS topic.

The code snippets below create an event rule with a Amazon SNS topic as a target.
It's called every hour by Amazon EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_sns as sns


topic = sns.Topic(self, "Topic")

payload = {
    "message": "Hello scheduler!"
}

target = targets.SnsPublish(topic,
    input=ScheduleTargetInput.from_object(payload)
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=target
)
```

## Send events to an EventBridge event bus

Use the `EventBridgePutEvents` target to send events to an EventBridge event bus.

The code snippet below creates an event rule with an EventBridge event bus as a target
called every hour by EventBridge Scheduler with a custom event payload.

```python
import aws_cdk.aws_events as events


event_bus = events.EventBus(self, "EventBus",
    event_bus_name="DomainEvents"
)

event_entry = targets.EventBridgePutEventsEntry(
    event_bus=event_bus,
    source="PetService",
    detail=ScheduleTargetInput.from_object({"Name": "Fluffy"}),
    detail_type="🐶"
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=targets.EventBridgePutEvents(event_entry)
)
```

## Start an Amazon Inspector assessment run

Use the `InspectorStartAssessmentRun` target to start an Inspector assessment run.

The code snippet below creates an event rule with an assessment template as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_inspector as inspector

# assessment_template: inspector.CfnAssessmentTemplate


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.InspectorStartAssessmentRun(assessment_template)
)
```

## Put a record to an Amazon Kinesis Data Stream

Use the `KinesisStreamPutRecord` target to put a record to an Amazon Kinesis Data Stream.

The code snippet below creates an event rule with a stream as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_kinesis as kinesis


stream = kinesis.Stream(self, "MyStream")

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.KinesisStreamPutRecord(stream,
        partition_key="key"
    )
)
```

## Put a record to a Kinesis Data Firehose

Use the `KinesisDataFirehosePutRecord` target to put a record to a Kinesis Data Firehose delivery stream.

The code snippet below creates an event rule with a delivery stream as a target
called every hour by EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_kinesisfirehose_alpha as firehose
# delivery_stream: firehose.IDeliveryStream


payload = {
    "Data": "record"
}

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.KinesisDataFirehosePutRecord(delivery_stream,
        input=ScheduleTargetInput.from_object(payload)
    )
)
```

## Start a CodePipeline execution

Use the `CodePipelineStartPipelineExecution` target to start a new execution for a CodePipeline pipeline.

The code snippet below creates an event rule with a CodePipeline pipeline as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_codepipeline as codepipeline

# pipeline: codepipeline.Pipeline


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.CodePipelineStartPipelineExecution(pipeline)
)
```

## Start a SageMaker pipeline execution

Use the `SageMakerStartPipelineExecution` target to start a new execution for a SageMaker pipeline.

The code snippet below creates an event rule with a SageMaker pipeline as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_sagemaker as sagemaker

# pipeline: sagemaker.IPipeline


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.SageMakerStartPipelineExecution(pipeline,
        pipeline_parameter_list=[targets.SageMakerPipelineParameter(
            name="parameter-name",
            value="parameter-value"
        )]
    )
)
```
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
import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_ceddda9d
import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_inspector as _aws_cdk_aws_inspector_ceddda9d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import aws_cdk.aws_kinesisfirehose_alpha as _aws_cdk_aws_kinesisfirehose_alpha_30daaf29
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_sagemaker as _aws_cdk_aws_sagemaker_ceddda9d
import aws_cdk.aws_scheduler_alpha as _aws_cdk_aws_scheduler_alpha_61df44e1
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EventBridgePutEventsEntry",
    jsii_struct_bases=[],
    name_mapping={
        "detail": "detail",
        "detail_type": "detailType",
        "event_bus": "eventBus",
        "source": "source",
    },
)
class EventBridgePutEventsEntry:
    def __init__(
        self,
        *,
        detail: _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput,
        detail_type: builtins.str,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        source: builtins.str,
    ) -> None:
        '''(experimental) An entry to be sent to EventBridge.

        :param detail: (experimental) The event body. Can either be provided as an object or as a JSON-serialized string
        :param detail_type: (experimental) Used along with the source field to help identify the fields and values expected in the detail field. For example, events by CloudTrail have detail type "AWS API Call via CloudTrail"
        :param event_bus: (experimental) The event bus the entry will be sent to.
        :param source: (experimental) The service or application that caused this event to be generated. Example value: ``com.example.service``

        :see: https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEventsRequestEntry.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_events as events
            
            
            event_bus = events.EventBus(self, "EventBus",
                event_bus_name="DomainEvents"
            )
            
            event_entry = targets.EventBridgePutEventsEntry(
                event_bus=event_bus,
                source="PetService",
                detail=ScheduleTargetInput.from_object({"Name": "Fluffy"}),
                detail_type="🐶"
            )
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.hours(1)),
                target=targets.EventBridgePutEvents(event_entry)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b15c35d804ca95ff64ca0a6f312aaf0cec9780ee78849d0052cf3f113afad9)
            check_type(argname="argument detail", value=detail, expected_type=type_hints["detail"])
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detail": detail,
            "detail_type": detail_type,
            "event_bus": event_bus,
            "source": source,
        }

    @builtins.property
    def detail(self) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput:
        '''(experimental) The event body.

        Can either be provided as an object or as a JSON-serialized string

        :stability: experimental

        Example::

            ScheduleTargetInput.from_text("{\"instance-id\": \"i-1234567890abcdef0\", \"state\": \"terminated\"}")
            ScheduleTargetInput.from_object({"Message": "Hello from a friendly event :)"})
        '''
        result = self._values.get("detail")
        assert result is not None, "Required property 'detail' is missing"
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput, result)

    @builtins.property
    def detail_type(self) -> builtins.str:
        '''(experimental) Used along with the source field to help identify the fields and values expected in the detail field.

        For example, events by CloudTrail have detail type "AWS API Call via CloudTrail"

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html
        :stability: experimental
        '''
        result = self._values.get("detail_type")
        assert result is not None, "Required property 'detail_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_bus(self) -> _aws_cdk_aws_events_ceddda9d.IEventBus:
        '''(experimental) The event bus the entry will be sent to.

        :stability: experimental
        '''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.IEventBus, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) The service or application that caused this event to be generated.

        Example value: ``com.example.service``

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBridgePutEventsEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SageMakerPipelineParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class SageMakerPipelineParameter:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Properties for a pipeline parameter.

        :param name: (experimental) Name of parameter to start execution of a SageMaker Model Building Pipeline.
        :param value: (experimental) Value of parameter to start execution of a SageMaker Model Building Pipeline.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_scheduler_targets_alpha as scheduler_targets_alpha
            
            sage_maker_pipeline_parameter = scheduler_targets_alpha.SageMakerPipelineParameter(
                name="name",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1b671700562aea93d2c9aa01ca3ab4bbfcb0da81f14e336b02e175cc0e96bd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of parameter to start execution of a SageMaker Model Building Pipeline.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) Value of parameter to start execution of a SageMaker Model Building Pipeline.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerPipelineParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduleTargetBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.ScheduleTargetBase",
):
    '''(experimental) Base class for Schedule Targets.

    :stability: experimental
    '''

    def __init__(
        self,
        base_props: typing.Union["ScheduleTargetBaseProps", typing.Dict[builtins.str, typing.Any]],
        target_arn: builtins.str,
    ) -> None:
        '''
        :param base_props: -
        :param target_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e59e7b340dc335b31c4a0d18b1845659c5a575671ec4c54fa176892cb9bd54)
            check_type(argname="argument base_props", value=base_props, expected_type=type_hints["base_props"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        jsii.create(self.__class__, self, [base_props, target_arn])

    @jsii.member(jsii_name="addTargetActionToRole")
    @abc.abstractmethod
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''(experimental) Create a return a Schedule Target Configuration for the given schedule.

        :param schedule: -

        :return: a Schedule Target Configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e82b6bad0ce8e66d78921fb69afc41cc589ff68e7fde7d3a116a558622ba0b)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bind", [schedule]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d8230d421e6fe144b04cf440bae3b93c14a1af6ea5635fc876670037e3a4ee)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def _target_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


class _ScheduleTargetBaseProxy(ScheduleTargetBase):
    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610cc83281b440576390d0e3dbfaa9a65adba95233cb7ffdfba72197abc9da29)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduleTargetBase).__jsii_proxy_class__ = lambda : _ScheduleTargetBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.ScheduleTargetBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
    },
)
class ScheduleTargetBaseProps:
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Base properties for a Schedule Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sns as sns
            
            
            topic = sns.Topic(self, "Topic")
            
            payload = {
                "message": "Hello scheduler!"
            }
            
            target = targets.SnsPublish(topic,
                input=ScheduleTargetInput.from_object(payload)
            )
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.hours(1)),
                target=target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e05948e70de09bca87c06a271bef4e0b3a07893d3e2112141ebdce3856e9e80)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(experimental) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(experimental) Input passed to the target.

        :default: - no input.

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleTargetBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class SnsPublish(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SnsPublish",
):
    '''(experimental) Use an Amazon SNS topic as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "Topic")
        
        payload = {
            "message": "Hello scheduler!"
        }
        
        target = targets.SnsPublish(topic,
            input=ScheduleTargetInput.from_object(payload)
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.hours(1)),
            target=target
        )
    '''

    def __init__(
        self,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param topic: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b00545abc5c0db54c2d2809ed5b2f135fc5c44b02c318bc15d3634020e4633)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [topic, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6baf1dcdf0de6e124cffb230fe4fdc6f44a348db6477f1070fe2c1b55ef82665)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class SqsSendMessage(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SqsSendMessage",
):
    '''(experimental) Use an Amazon SQS Queue as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        payload = "test"
        message_group_id = "id"
        queue = sqs.Queue(self, "MyQueue",
            fifo=True,
            content_based_deduplication=True
        )
        
        target = targets.SqsSendMessage(queue,
            input=ScheduleTargetInput.from_text(payload),
            message_group_id=message_group_id
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(1)),
            target=target
        )
    '''

    def __init__(
        self,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        *,
        message_group_id: typing.Optional[builtins.str] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param queue: -
        :param message_group_id: (experimental) The FIFO message group ID to use as the target. This must be specified when the target is a FIFO queue. If you specify a FIFO queue as a target, the queue must have content-based deduplication enabled. A length of ``messageGroupId`` must be between 1 and 128. Default: - no message group ID
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4813eef9ae399e4e7240ac6b9346c654577bf97511e9a71e43ce8856a8293f77)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        props = SqsSendMessageProps(
            message_group_id=message_group_id,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [queue, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5ab2b88a54bc5208c7d14e9744c6597c0f0301de5b4c60bb95d90849069e33)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b4e499db09ce4b94c98ac3cf9054d519de93d540d51895429b6af27d162a12)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SqsSendMessageProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "message_group_id": "messageGroupId",
    },
)
class SqsSendMessageProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a SQS Queue Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param message_group_id: (experimental) The FIFO message group ID to use as the target. This must be specified when the target is a FIFO queue. If you specify a FIFO queue as a target, the queue must have content-based deduplication enabled. A length of ``messageGroupId`` must be between 1 and 128. Default: - no message group ID

        :stability: experimental
        :exampleMetadata: infused

        Example::

            payload = "test"
            message_group_id = "id"
            queue = sqs.Queue(self, "MyQueue",
                fifo=True,
                content_based_deduplication=True
            )
            
            target = targets.SqsSendMessage(queue,
                input=ScheduleTargetInput.from_text(payload),
                message_group_id=message_group_id
            )
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(1)),
                target=target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54bd4b76ef8c8d82a414b1afa05a0f9628f07ff40b7ecdd1db2ed2ee30fd9c7)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(experimental) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(experimental) Input passed to the target.

        :default: - no input.

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The FIFO message group ID to use as the target.

        This must be specified when the target is a FIFO queue. If you specify
        a FIFO queue as a target, the queue must have content-based deduplication enabled.

        A length of ``messageGroupId`` must be between 1 and 128.

        :default: - no message group ID

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sqsparameters.html#cfn-scheduler-schedule-sqsparameters-messagegroupid
        :stability: experimental
        '''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsSendMessageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class StepFunctionsStartExecution(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.StepFunctionsStartExecution",
):
    '''(experimental) Use an AWS Step function as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_stepfunctions as sfn
        import aws_cdk.aws_stepfunctions_tasks as tasks
        
        
        payload = {
            "Name": "MyParameter",
            "Value": "🌥️"
        }
        
        put_parameter_step = tasks.CallAwsService(self, "PutParameter",
            service="ssm",
            action="putParameter",
            iam_resources=["*"],
            parameters={
                "Name.$": "$.Name",
                "Value.$": "$.Value",
                "Type": "String",
                "Overwrite": True
            }
        )
        
        state_machine = sfn.StateMachine(self, "StateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(put_parameter_step)
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.hours(1)),
            target=targets.StepFunctionsStartExecution(state_machine,
                input=ScheduleTargetInput.from_object(payload)
            )
        )
    '''

    def __init__(
        self,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param state_machine: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2f5731f4fe761fad561cdd5177904d0685abe6cc827da58894e4519f3104d2)
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [state_machine, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16c6a822df4449b80b3088cf438b74a5c925845e7b3fe17b5671a96deceef76)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class CodeBuildStartBuild(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.CodeBuildStartBuild",
):
    '''(experimental) Use an AWS CodeBuild as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codebuild as codebuild
        
        # project: codebuild.Project
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.CodeBuildStartBuild(project)
        )
    '''

    def __init__(
        self,
        project: _aws_cdk_aws_codebuild_ceddda9d.IProject,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param project: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee4f6daae6be7c2365ab2dfb373e3d4a03c594923664bb691da6e3795d41b16)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [project, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474fd9928553c6c25206d5a8cd8a15397a1e8091bdc5173fc92abdd167cfda07)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class CodePipelineStartPipelineExecution(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.CodePipelineStartPipelineExecution",
):
    '''(experimental) Use an AWS CodePipeline pipeline as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codepipeline as codepipeline
        
        # pipeline: codepipeline.Pipeline
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.CodePipelineStartPipelineExecution(pipeline)
        )
    '''

    def __init__(
        self,
        pipeline: _aws_cdk_aws_codepipeline_ceddda9d.IPipeline,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1179b8a788d46a78ad80abd38cd8f227eaf4ff63c93fb2ce58abfb9cf84a57aa)
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [pipeline, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f97647f2f639edabbd7fc4d342abe0f255a5960ef5840c029bfc32962fa9769)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class EventBridgePutEvents(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EventBridgePutEvents",
):
    '''(experimental) Send an event to an AWS EventBridge by AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_events as events
        
        
        event_bus = events.EventBus(self, "EventBus",
            event_bus_name="DomainEvents"
        )
        
        event_entry = targets.EventBridgePutEventsEntry(
            event_bus=event_bus,
            source="PetService",
            detail=ScheduleTargetInput.from_object({"Name": "Fluffy"}),
            detail_type="🐶"
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.hours(1)),
            target=targets.EventBridgePutEvents(event_entry)
        )
    '''

    def __init__(
        self,
        entry: typing.Union[EventBridgePutEventsEntry, typing.Dict[builtins.str, typing.Any]],
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param entry: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae28df8ed7b4d4cf0069c2078c852156338afac2e79eb10ab690c790a1efde31)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [entry, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d3987aace1577c0609c760b353ffad7b4806705694003c15c7ef457008811e)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe563fb16e465141154d47511f2ad5007930fbbc4c511a584457cd7a4285e684)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class InspectorStartAssessmentRun(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.InspectorStartAssessmentRun",
):
    '''(experimental) Use an Amazon Inspector as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_inspector as inspector
        
        # assessment_template: inspector.CfnAssessmentTemplate
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.InspectorStartAssessmentRun(assessment_template)
        )
    '''

    def __init__(
        self,
        template: _aws_cdk_aws_inspector_ceddda9d.CfnAssessmentTemplate,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param template: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7bbb3c9d358edb684284e6061143edea14a918d787e7b0de0abe8074adc3a8)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [template, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62115ee3101d95125c22cd00ce69aefcbf38ba32a31ec38c5fe32386b72a485)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class KinesisDataFirehosePutRecord(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.KinesisDataFirehosePutRecord",
):
    '''(experimental) Use an Amazon Kinesis Data Firehose as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesisfirehose_alpha as firehose
        # delivery_stream: firehose.IDeliveryStream
        
        
        payload = {
            "Data": "record"
        }
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.KinesisDataFirehosePutRecord(delivery_stream,
                input=ScheduleTargetInput.from_object(payload)
            )
        )
    '''

    def __init__(
        self,
        delivery_stream: _aws_cdk_aws_kinesisfirehose_alpha_30daaf29.IDeliveryStream,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param delivery_stream: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb875c4ec6397c775b17f7b09e25adcfa6aa6b53eec3b8b56759ae0b39843aa7)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [delivery_stream, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7660f070b14c8b2d46ed63567629542d411ed4e55bfbfab5ffa95dee46eff8)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class KinesisStreamPutRecord(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.KinesisStreamPutRecord",
):
    '''(experimental) Use an Amazon Kinesis Data Streams as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesis as kinesis
        
        
        stream = kinesis.Stream(self, "MyStream")
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.KinesisStreamPutRecord(stream,
                partition_key="key"
            )
        )
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
        *,
        partition_key: builtins.str,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param stream: -
        :param partition_key: (experimental) The shard to which EventBridge Scheduler sends the event. The length must be between 1 and 256.
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da8609af671f7e313f5b3391e0c519b97069ce30e7f39aaae4028df271ad968)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = KinesisStreamPutRecordProps(
            partition_key=partition_key,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [stream, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00e0c64cae92c47512d2b31480147546bdac967e14a67f989fced9ea65977ab)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901c2c170b31144628352155381f9212d91d6a15a1323004e8a2a1fc86211850)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.KinesisStreamPutRecordProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "partition_key": "partitionKey",
    },
)
class KinesisStreamPutRecordProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        partition_key: builtins.str,
    ) -> None:
        '''(experimental) Properties for a Kinesis Data Streams Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param partition_key: (experimental) The shard to which EventBridge Scheduler sends the event. The length must be between 1 and 256.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_kinesis as kinesis
            
            
            stream = kinesis.Stream(self, "MyStream")
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(60)),
                target=targets.KinesisStreamPutRecord(stream,
                    partition_key="key"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450b2e09dbbdf0b1ab8f7ab50d92ab0bc3784cd7aebcc42382aa41af77149cf6)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(experimental) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(experimental) Input passed to the target.

        :default: - no input.

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def partition_key(self) -> builtins.str:
        '''(experimental) The shard to which EventBridge Scheduler sends the event.

        The length must be between 1 and 256.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-kinesisparameters.html
        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisStreamPutRecordProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class LambdaInvoke(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.LambdaInvoke",
):
    '''(experimental) Use an AWS Lambda function as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # fn: lambda.Function
        
        
        target = targets.LambdaInvoke(fn,
            input=ScheduleTargetInput.from_object({
                "payload": "useful"
            })
        )
        
        schedule = Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(10)),
            target=target,
            description="This is a test schedule that invokes a lambda function every 10 minutes."
        )
    '''

    def __init__(
        self,
        func: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param func: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cee0b6faf4f1c2dcade061e69cf02b9c302a868d55e47f591978024f5da0075)
            check_type(argname="argument func", value=func, expected_type=type_hints["func"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [func, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bceedc3f4419f27eac20d417a223b3233c972e163393fd278acd75b7129d89)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class SageMakerStartPipelineExecution(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SageMakerStartPipelineExecution",
):
    '''(experimental) Use a SageMaker pipeline as a target for AWS EventBridge Scheduler.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sagemaker as sagemaker
        
        # pipeline: sagemaker.IPipeline
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.SageMakerStartPipelineExecution(pipeline,
                pipeline_parameter_list=[targets.SageMakerPipelineParameter(
                    name="parameter-name",
                    value="parameter-value"
                )]
            )
        )
    '''

    def __init__(
        self,
        pipeline: _aws_cdk_aws_sagemaker_ceddda9d.IPipeline,
        *,
        pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param pipeline_parameter_list: (experimental) List of parameter names and values to use when executing the SageMaker Model Building Pipeline. The length must be between 0 and 200. Default: - no pipeline parameter list
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cd1e092f776a22386cfd27fc1778ae00bc42ca6e1f29df07ab3c760bf88329)
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
        props = SageMakerStartPipelineExecutionProps(
            pipeline_parameter_list=pipeline_parameter_list,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [pipeline, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a618244e0553e568cdf781844a2bbc64b2127af3cf8d23bbd6e2083ab5b1838)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param schedule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0401259d77c4f97bb1b7a40ff1a9f35512d38224dee98a520446b9b7876f9acd)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [schedule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SageMakerStartPipelineExecutionProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "pipeline_parameter_list": "pipelineParameterList",
    },
)
class SageMakerStartPipelineExecutionProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for a SageMaker Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param pipeline_parameter_list: (experimental) List of parameter names and values to use when executing the SageMaker Model Building Pipeline. The length must be between 0 and 200. Default: - no pipeline parameter list

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sagemaker as sagemaker
            
            # pipeline: sagemaker.IPipeline
            
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(60)),
                target=targets.SageMakerStartPipelineExecution(pipeline,
                    pipeline_parameter_list=[targets.SageMakerPipelineParameter(
                        name="parameter-name",
                        value="parameter-value"
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c01c7fd9ffc99ab1f2f2a61c89fe87963adc09f9e04fb878a3007c33ce123c)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument pipeline_parameter_list", value=pipeline_parameter_list, expected_type=type_hints["pipeline_parameter_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if pipeline_parameter_list is not None:
            self._values["pipeline_parameter_list"] = pipeline_parameter_list

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(experimental) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(experimental) Input passed to the target.

        :default: - no input.

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def pipeline_parameter_list(
        self,
    ) -> typing.Optional[typing.List[SageMakerPipelineParameter]]:
        '''(experimental) List of parameter names and values to use when executing the SageMaker Model Building Pipeline.

        The length must be between 0 and 200.

        :default: - no pipeline parameter list

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameters.html#cfn-scheduler-schedule-sagemakerpipelineparameters-pipelineparameterlist
        :stability: experimental
        '''
        result = self._values.get("pipeline_parameter_list")
        return typing.cast(typing.Optional[typing.List[SageMakerPipelineParameter]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerStartPipelineExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CodeBuildStartBuild",
    "CodePipelineStartPipelineExecution",
    "EventBridgePutEvents",
    "EventBridgePutEventsEntry",
    "InspectorStartAssessmentRun",
    "KinesisDataFirehosePutRecord",
    "KinesisStreamPutRecord",
    "KinesisStreamPutRecordProps",
    "LambdaInvoke",
    "SageMakerPipelineParameter",
    "SageMakerStartPipelineExecution",
    "SageMakerStartPipelineExecutionProps",
    "ScheduleTargetBase",
    "ScheduleTargetBaseProps",
    "SnsPublish",
    "SqsSendMessage",
    "SqsSendMessageProps",
    "StepFunctionsStartExecution",
]

publication.publish()

def _typecheckingstub__c3b15c35d804ca95ff64ca0a6f312aaf0cec9780ee78849d0052cf3f113afad9(
    *,
    detail: _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput,
    detail_type: builtins.str,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1b671700562aea93d2c9aa01ca3ab4bbfcb0da81f14e336b02e175cc0e96bd(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e59e7b340dc335b31c4a0d18b1845659c5a575671ec4c54fa176892cb9bd54(
    base_props: typing.Union[ScheduleTargetBaseProps, typing.Dict[builtins.str, typing.Any]],
    target_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e82b6bad0ce8e66d78921fb69afc41cc589ff68e7fde7d3a116a558622ba0b(
    schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d8230d421e6fe144b04cf440bae3b93c14a1af6ea5635fc876670037e3a4ee(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610cc83281b440576390d0e3dbfaa9a65adba95233cb7ffdfba72197abc9da29(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e05948e70de09bca87c06a271bef4e0b3a07893d3e2112141ebdce3856e9e80(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b00545abc5c0db54c2d2809ed5b2f135fc5c44b02c318bc15d3634020e4633(
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baf1dcdf0de6e124cffb230fe4fdc6f44a348db6477f1070fe2c1b55ef82665(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4813eef9ae399e4e7240ac6b9346c654577bf97511e9a71e43ce8856a8293f77(
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    *,
    message_group_id: typing.Optional[builtins.str] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5ab2b88a54bc5208c7d14e9744c6597c0f0301de5b4c60bb95d90849069e33(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b4e499db09ce4b94c98ac3cf9054d519de93d540d51895429b6af27d162a12(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54bd4b76ef8c8d82a414b1afa05a0f9628f07ff40b7ecdd1db2ed2ee30fd9c7(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2f5731f4fe761fad561cdd5177904d0685abe6cc827da58894e4519f3104d2(
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16c6a822df4449b80b3088cf438b74a5c925845e7b3fe17b5671a96deceef76(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee4f6daae6be7c2365ab2dfb373e3d4a03c594923664bb691da6e3795d41b16(
    project: _aws_cdk_aws_codebuild_ceddda9d.IProject,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474fd9928553c6c25206d5a8cd8a15397a1e8091bdc5173fc92abdd167cfda07(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1179b8a788d46a78ad80abd38cd8f227eaf4ff63c93fb2ce58abfb9cf84a57aa(
    pipeline: _aws_cdk_aws_codepipeline_ceddda9d.IPipeline,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f97647f2f639edabbd7fc4d342abe0f255a5960ef5840c029bfc32962fa9769(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae28df8ed7b4d4cf0069c2078c852156338afac2e79eb10ab690c790a1efde31(
    entry: typing.Union[EventBridgePutEventsEntry, typing.Dict[builtins.str, typing.Any]],
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d3987aace1577c0609c760b353ffad7b4806705694003c15c7ef457008811e(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe563fb16e465141154d47511f2ad5007930fbbc4c511a584457cd7a4285e684(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7bbb3c9d358edb684284e6061143edea14a918d787e7b0de0abe8074adc3a8(
    template: _aws_cdk_aws_inspector_ceddda9d.CfnAssessmentTemplate,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62115ee3101d95125c22cd00ce69aefcbf38ba32a31ec38c5fe32386b72a485(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb875c4ec6397c775b17f7b09e25adcfa6aa6b53eec3b8b56759ae0b39843aa7(
    delivery_stream: _aws_cdk_aws_kinesisfirehose_alpha_30daaf29.IDeliveryStream,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7660f070b14c8b2d46ed63567629542d411ed4e55bfbfab5ffa95dee46eff8(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da8609af671f7e313f5b3391e0c519b97069ce30e7f39aaae4028df271ad968(
    stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
    *,
    partition_key: builtins.str,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00e0c64cae92c47512d2b31480147546bdac967e14a67f989fced9ea65977ab(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901c2c170b31144628352155381f9212d91d6a15a1323004e8a2a1fc86211850(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450b2e09dbbdf0b1ab8f7ab50d92ab0bc3784cd7aebcc42382aa41af77149cf6(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    partition_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cee0b6faf4f1c2dcade061e69cf02b9c302a868d55e47f591978024f5da0075(
    func: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bceedc3f4419f27eac20d417a223b3233c972e163393fd278acd75b7129d89(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cd1e092f776a22386cfd27fc1778ae00bc42ca6e1f29df07ab3c760bf88329(
    pipeline: _aws_cdk_aws_sagemaker_ceddda9d.IPipeline,
    *,
    pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a618244e0553e568cdf781844a2bbc64b2127af3cf8d23bbd6e2083ab5b1838(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0401259d77c4f97bb1b7a40ff1a9f35512d38224dee98a520446b9b7876f9acd(
    schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c01c7fd9ffc99ab1f2f2a61c89fe87963adc09f9e04fb878a3007c33ce123c(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
