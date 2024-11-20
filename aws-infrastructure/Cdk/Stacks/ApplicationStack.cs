using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.ECS;
using Amazon.CDK.AWS.ElasticLoadBalancingV2;
using Amazon.CDK.AWS.Logs;
using Amazon.CDK.AWS.SecretsManager;
using System.Collections.Generic;
using NetworkMode = Amazon.CDK.AWS.ECS.NetworkMode;
using Secret = Amazon.CDK.AWS.ECS.Secret;

namespace Cdk.Stacks;

public class ApplicationStack : Stack
{
    public ApplicationStack(Construct scope, string id, ApplicationStackProps props) : base(scope, id, props)
    {
        var domainName = scope.Node.TryGetContext("zoneName") as string ?? throw new ArgumentException("zoneName is required");
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


        AddFrontendContainer(props, taskDefinition, service, domainName);
        AddBackendContainer(props, taskDefinition, service, domainName);
        
    }

    private static void AddBackendContainer(ApplicationStackProps props, TaskDefinition taskDefinition, BaseService service, string domainName)
    {
        var backendImageTarball = service.Node.TryGetContext("backendImageTarball") as string;
        taskDefinition.AddContainer("Backend",
            new ContainerDefinitionOptions
            {
                Essential = true,
                Secrets = CreteBackendSecretEnvironmentVariables(props),
                Environment = CreateBackendEnvironmentVariables(props, domainName),
                PortMappings =
                [
                    new PortMapping
                    {
                        ContainerPort = 8000,
                        HostPort = 8000
                    }
                ],
                Image = string.IsNullOrEmpty(backendImageTarball) ? ContainerImage.FromRegistry("signalen/backend:latest", new RepositoryImageProps()) : ContainerImage.FromTarball(backendImageTarball),
                Logging = LogDriver.AwsLogs(new AwsLogDriverProps
                {
                    LogRetention = RetentionDays.ONE_DAY,
                    Mode = AwsLogDriverMode.NON_BLOCKING,
                    StreamPrefix = "backend"
                })
            });

        service.RegisterLoadBalancerTargets(new EcsTarget
        {
            ContainerName = "Backend",
            NewTargetGroupId = "Backend",
            Listener = ListenerConfig.ApplicationListener(props.Listener, new AddApplicationTargetsProps
            {
                Protocol = ApplicationProtocol.HTTP,
                Conditions = [
                    ListenerCondition.HostHeaders([$"api.{domainName}"])
                ],
                Priority = 20
            })
        });
    }

    private static void AddFrontendContainer(ApplicationStackProps props, TaskDefinition taskDefinition, BaseService service, string domainName)
    {
        var frontendImageTarball = service.Node.TryGetContext("frontendImageTarball") as string;
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


    private static Dictionary<string, Secret> CreteBackendSecretEnvironmentVariables(ApplicationStackProps props)
    {
        return new Dictionary<string, Amazon.CDK.AWS.ECS.Secret>
        {
            {
                "DATABASE_USER",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.DatabaseSecret, "username")
            },
            {
                "DATABASE_PASSWORD",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.DatabaseSecret, "password")
            },
            {
                "DATABASE_HOST_OVERRIDE",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.DatabaseSecret, "host")
            },
            {
                "DATABASE_PORT_OVERRIDE",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.DatabaseSecret, "port")
            },
            {
                "EMAIL_HOST_USER",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.MaiSecret, "username")
            },
            {
                "EMAIL_HOST_PASSWORD",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.MaiSecret, "password")
            },
            {
                "RABBITMQ_USER",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.RabbitSecret, "username")
            },
            {
                "RABBITMQ_PASSWORD",
                Amazon.CDK.AWS.ECS.Secret.FromSecretsManager(props.RabbitSecret, "password")
            },
        };
    }

    private static Dictionary<string, string> CreateBackendEnvironmentVariables(ApplicationStackProps props, string domainName)
    {
        return new Dictionary<string, string>
        {
            { "SECRET_KEY", "insecure" },
            { "DJANGO_DEBUG", "False" },
            { "LOGGING_LEVEL", "INFO" },
            { "ALLOWED_HOSTS", "*" },
            { "FRONTEND_URL", $"http://{domainName}" },
            { "DWH_MEDIA_ROOT", "/dwh_media" },
            { "CORS_ALLOW_ALL_ORIGINS", "True" },
            { "DATABASE_NAME", "signals" },
            { "PUB_JWKS", "" },
            { "JWKS_URL", "http://dex:5556/keys" },
            { "USER_ID_FIELDS", "email" },
            { "SIGNALS_AUTH_ALWAYS_OK", "True" },
            { "TEST_LOGIN", "signals.admin@example.com" },
            { "SECURE_SSL_REDIRECT", "True" },
            { "SESSION_COOKIE_SECURE", "True" },
            { "CSRF_COOKIE_SECURE", "True" },
            { "ELASTICSEARCH_HOST", "elasticsearch:9200" },
            { "EMAIL_HOST", $"email.{Aws.REGION}.amazonaws.com" },
            { "EMAIL_PORT", "465" },
            { "EMAIL_USE_SSL", "True" },
            { "MY_SIGNALS_ENABLED", "True" },
            { "SIGNAL_HISTORY_LOG_ENABLED", "True" },
            { "OIDC_RP_CLIENT_ID", "signals" },
            { "OIDC_RP_CLIENT_SECRET", "insecure" },
            { "OIDC_OP_AUTHORIZATION_ENDPOINT", "http://127.0.0.1:5556/auth" },
            { "OIDC_OP_TOKEN_ENDPOINT", "http://dex:5556/token" },
            { "OIDC_OP_USER_ENDPOINT", "http://dex:5556/userinfo" },
            { "OIDC_OP_JWKS_ENDPOINT", "http://dex:5556/keys" },
            { "SILK_ENABLED", "False" },
            { "SILK_PROFILING_ENABLED", "False" },
            { "SILK_AUTHENTICATION_ENABLED", "False" },
            { "SESSION_SUPPORT_ON_TOKEN_AUTHENTICATION", "False" },
            { "SYSTEM_MAIL_FEEDBACK_RECEIVED_ENABLED", "True" },
            { "REPORTER_MAIL_HANDLED_NEGATIVE_CONTACT_ENABLED", "True" },
            { "SIGNAL_HISTORY_LOG_ENABLED", "True" },
            { "MAINTENANCE_MODE", "False" },
            { "RABBITMQ_HOST", props.RabbitHost}
        };
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