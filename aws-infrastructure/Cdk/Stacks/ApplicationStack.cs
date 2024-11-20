using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.ECS;
using Amazon.CDK.AWS.ElasticLoadBalancingV2;
using Amazon.CDK.AWS.Logs;
using Amazon.CDK.AWS.SecretsManager;
using NetworkMode = Amazon.CDK.AWS.ECS.NetworkMode;
using Secret = Amazon.CDK.AWS.ECS.Secret;

namespace Cdk.Stacks;

public class ApplicationStack : Stack
{
    public ApplicationStack(Construct scope, string id, ApplicationStackProps props) : base(scope, id, props)
    {
        var domainName = scope.Node.TryGetContext("zoneName") as string ?? throw new ArgumentException("zoneName is required");
        var frontendImageTarball = scope.Node.TryGetContext("frontendImageTarball") as string;
        var cluster = new Cluster(this, "Cluster", new ClusterProps
        {
            Vpc = props.Vpc
        });

        var taskDefinition = new TaskDefinition(this, "Signalen", new TaskDefinitionProps
        {
            Compatibility = Compatibility.FARGATE,
            NetworkMode = NetworkMode.AWS_VPC,
            MemoryMiB = "512",
            Cpu = "256",
            RuntimePlatform = new RuntimePlatform
            {
                CpuArchitecture = CpuArchitecture.X86_64,
                OperatingSystemFamily = OperatingSystemFamily.LINUX
            }
        });

        var service = new FargateService(this, "Service",
            new FargateServiceProps
            {
                Cluster = cluster,
                TaskDefinition = taskDefinition,
                DesiredCount = 1,
                MinHealthyPercent = 0,
                MaxHealthyPercent = 200,
                SecurityGroups = props.ApplicationSecurityGroups,
                PlatformVersion = FargatePlatformVersion.LATEST,
                VpcSubnets = new SubnetSelection { SubnetType = SubnetType.PUBLIC },
                HealthCheckGracePeriod = Duration.Seconds(0),
                AssignPublicIp = true
            });


        taskDefinition.AddContainer("Frontend",
                new ContainerDefinitionOptions
                {
                    Essential = true,
                    PortMappings =
                    [
                        new PortMapping
                        {
                            ContainerPort = 8080,
                            HostPort = 8080
                        }
                    ],
                    Image = string.IsNullOrEmpty(frontendImageTarball) ? ContainerImage.FromRegistry("signalen/frontend:latest", new RepositoryImageProps()) : ContainerImage.FromTarball(frontendImageTarball),
                    Logging = LogDriver.AwsLogs(new AwsLogDriverProps
                    {
                        LogRetention = RetentionDays.ONE_DAY,
                        Mode = AwsLogDriverMode.NON_BLOCKING,
                        StreamPrefix = "frontend"
                    })
                });

        service.RegisterLoadBalancerTargets(new EcsTarget
        {
            ContainerName = "Frontend",
            NewTargetGroupId = "Frontend",
            Listener = ListenerConfig.ApplicationListener(props.Listener, new AddApplicationTargetsProps
            {
                Protocol = ApplicationProtocol.HTTP,
                Conditions = [
                        ListenerCondition.HostHeaders([domainName])
                    ],
                Priority = 10
            })
        });

    }

}

public class ApplicationStackProps(Vpc vpc, ApplicationListener listener, ISecurityGroup[] applicationSecurityGroups, ISecret databaseSecret, ISecret rabbitSecret, ISecret maiSecret, string rabbitHost) : StackProps
{
    public IVpc Vpc { get; init; } = vpc;
    public ApplicationListener Listener { get; } = listener;
    public ISecurityGroup[] ApplicationSecurityGroups { get; } = applicationSecurityGroups;
    public ISecret DatabaseSecret { get; } = databaseSecret;
    public ISecret RabbitSecret { get; } = rabbitSecret;
    public ISecret MaiSecret { get; } = maiSecret;
    public string RabbitHost { get; } = rabbitHost;
}