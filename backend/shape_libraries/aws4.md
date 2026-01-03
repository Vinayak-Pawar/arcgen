# AWS 4.0 Shape Library

AWS 2025 icon library for draw.io diagrams. This library contains 1000+ AWS service icons.

## Usage

In your mxCell style attribute, use:
```
style="shape=mxgraph.aws4.SERVICE_NAME;fillColor=#FF9900;"
```

## Common AWS Services

### Compute
- **EC2**: `shape=mxgraph.aws4.ec2`
- **Lambda**: `shape=mxgraph.aws4.lambda_function`
- **ECS**: `shape=mxgraph.aws4.ecs`
- **EKS**: `shape=mxgraph.aws4.eks_cloud`
- **Fargate**: `shape=mxgraph.aws4.fargate`

### Storage
- **S3**: `shape=mxgraph.aws4.s3`
- **EBS**: `shape=mxgraph.aws4.ebs`
- **EFS**: `shape=mxgraph.aws4.efs`
- **Glacier**: `shape=mxgraph.aws4.glacier`

### Database
- **RDS**: `shape=mxgraph.aws4.rds`
- **DynamoDB**: `shape=mxgraph.aws4.dynamodb`
- **Aurora**: `shape=mxgraph.aws4.aurora`
- **ElastiCache**: `shape=mxgraph.aws4.elasticache`
- **Redshift**: `shape=mxgraph.aws4.redshift`

### Networking
- **VPC**: `shape=mxgraph.aws4.vpc`
- **Route 53**: `shape=mxgraph.aws4.route_53`
- **CloudFront**: `shape=mxgraph.aws4.cloudfront`
- **API Gateway**: `shape=mxgraph.aws4.api_gateway`
- **ELB**: `shape=mxgraph.aws4.elastic_load_balancing`
- **Direct Connect**: `shape=mxgraph.aws4.direct_connect`

### Security
- **IAM**: `shape=mxgraph.aws4.iam`
- **Cognito**: `shape=mxgraph.aws4.cognito`
- **KMS**: `shape=mxgraph.aws4.key_management_service`
- **WAF**: `shape=mxgraph.aws4.waf`
- **Shield**: `shape=mxgraph.aws4.shield`

### Messaging & Integration
- **SQS**: `shape=mxgraph.aws4.sqs`
- **SNS**: `shape=mxgraph.aws4.sns`
- **EventBridge**: `shape=mxgraph.aws4.eventbridge`
- **Step Functions**: `shape=mxgraph.aws4.step_functions`

### Analytics
- **Kinesis**: `shape=mxgraph.aws4.kinesis`
- **Athena**: `shape=mxgraph.aws4.athena`
- **EMR**: `shape=mxgraph.aws4.emr`
- **Glue**: `shape=mxgraph.aws4.glue`

### Machine Learning
- **SageMaker**: `shape=mxgraph.aws4.sagemaker`
- **Rekognition**: `shape=mxgraph.aws4.rekognition`
- **Comprehend**: `shape=mxgraph.aws4.comprehend`

### Monitoring & Management
- **CloudWatch**: `shape=mxgraph.aws4.cloudwatch`
- **CloudTrail**: `shape=mxgraph.aws4.cloudtrail`
- **Config**: `shape=mxgraph.aws4.config`
- **Systems Manager**: `shape=mxgraph.aws4.systems_manager`

### Containers
- **ECR**: `shape=mxgraph.aws4.ecr`
- **App Runner**: `shape=mxgraph.aws4.app_runner`

### Developer Tools
- **CodeCommit**: `shape=mxgraph.aws4.codecommit`
- **CodeBuild**: `shape=mxgraph.aws4.codebuild`
- **CodeDeploy**: `shape=mxgraph.aws4.codedeploy`
- **CodePipeline**: `shape=mxgraph.aws4.codepipeline`

## Example Usage

```xml
<mxCell id="2" value="EC2 Instance" 
  style="shape=mxgraph.aws4.ec2;fillColor=#FF9900;strokeColor=#232F3E;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="78" height="78" as="geometry"/>
</mxCell>

<mxCell id="3" value="S3 Bucket" 
  style="shape=mxgraph.aws4.s3;fillColor=#7AA116;strokeColor=#232F3E;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="78" height="78" as="geometry"/>
</mxCell>

<mxCell id="4" value="RDS Database" 
  style="shape=mxgraph.aws4.rds;fillColor=#3334B9;strokeColor=#232F3E;" 
  vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="78" height="78" as="geometry"/>
</mxCell>
```

## Color Guidelines

AWS uses specific colors for different service categories:
- **Compute**: Orange (#FF9900)
- **Storage**: Green (#7AA116)
- **Database**: Blue (#3334B9)
- **Networking**: Purple (#8C4FFF)
- **Security**: Red (#DD344C)
- **Analytics**: Pink (#E7157B)
- **Machine Learning**: Teal (#01A88D)

Always use `strokeColor=#232F3E` (AWS dark gray) for shape borders.

## Tips

1. Always call `get_shape_library("aws4")` before generating AWS diagrams
2. Use exact shape names as listed above
3. Include fillColor for better visual appearance
4. Keep icon sizes around 78x78 pixels for consistency
5. Add descriptive value attributes for clarity
