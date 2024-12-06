r'''
# Amazon Bedrock Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Language**                                                                                   | **Package**                             |
| :--------------------------------------------------------------------------------------------- | --------------------------------------- |
| ![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) TypeScript | `@cdklabs/generative-ai-cdk-constructs` |
| ![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python             | `cdklabs.generative_ai_cdk_constructs`  |

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that offers a choice of foundation models (FMs) along with a broad set of capabilities for building generative AI applications.

This construct library includes CloudFormation L1 resources to deploy Bedrock features.

## Table of contents

* [API](#api)
* [Knowledge Bases](#knowledge-bases)
* [Agents](#agents)
* [Guardrails](#bedrock-guardrails)
* [Prompt management](#prompt-management)
* [Application inference profile](#application-inference-profile)

## API

See the [API documentation](../../../apidocs/namespaces/bedrock/README.md).

## Knowledge Bases

With Knowledge Bases for Amazon Bedrock, you can give FMs and agents contextual information from your company’s private data sources for Retrieval Augmented Generation (RAG) to deliver more relevant, accurate, and customized responses.

### Create a Knowledge Base

A vector index on a vector store is required to create a Knowledge Base. This construct currently supports [Amazon OpenSearch Serverless](../opensearchserverless), [Amazon RDS Aurora PostgreSQL](../amazonaurora/), [Pinecone](../pinecone/) . By default, this resource will create an OpenSearch Serverless vector collection and index for each Knowledge Base you create, but you can provide an existing collection and/or index to have more control. For other resources you need to have the vector stores already created and credentials stored in AWS Secrets Manager. For Aurora, the construct provides an option to create a default `AmazonAuroraDefaultVectorStore` construct that will provision the vector store backed by Amazon Aurora for you. To learn more you can read [here](../amazonaurora/README.md).

The resource accepts an `instruction` prop that is provided to any Bedrock Agent it is associated with so the agent can decide when to query the Knowledge Base.

Amazon Bedrock Knowledge Bases currently only supports S3 as a data source. The `S3DataSource` resource is used to configure how the Knowledge Base handles the data source.

Example of `OpenSearch Serverless`:

TypeScript

```python
import * as s3 from "aws-cdk-lib/aws-s3";
import { bedrock } from "@cdklabs/generative-ai-cdk-constructs";

const kb = new bedrock.KnowledgeBase(this, "KnowledgeBase", {
  embeddingsModel: bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
  instruction: "Use this knowledge base to answer questions about books. " + "It contains the full text of novels.",
});

const docBucket = new s3.Bucket(this, "DocBucket");

new bedrock.S3DataSource(this, "DataSource", {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: "books",
  chunkingStrategy: bedrock.ChunkingStrategy.fixedSize({
    maxTokens: 500,
    overlapPercentage: 20,
  }),
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock
)

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            embeddings_model= bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)

```

Example of `Amazon RDS Aurora PostgreSQL`:

TypeScript

```python
import * as s3 from "aws-cdk-lib/aws-s3";
import { amazonaurora, bedrock } from "@cdklabs/generative-ai-cdk-constructs";

// Dimension of your vector embedding
embeddingsModelVectorDimension = 1024;
const auroraDb = new amazonaurora.AmazonAuroraVectorStore(stack, "AuroraDefaultVectorStore", {
  embeddingsModelVectorDimension: embeddingsModelVectorDimension,
});

const kb = new bedrock.KnowledgeBase(this, "KnowledgeBase", {
  vectorStore: auroraDb,
  embeddingsModelVectorDimension: embeddingsModelVectorDimension,
  instruction: "Use this knowledge base to answer questions about books. " + "It contains the full text of novels.",
});

const docBucket = new s3.Bucket(this, "DocBucket");

new bedrock.S3DataSource(this, "DataSource", {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: "books",
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
    aws_rds as rds,
    aws_ec2 as ec2,
    Stack,
    ArnFormat
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    amazonaurora,
)

# Dimension of your vector embedding
embeddings_model_vector_dimension = 1024
aurora_db = amazonaurora.AmazonAuroraVectorStore(self, 'AuroraDefaultVectorStore',
  embeddings_model_vector_dimension=embeddings_model_vector_dimension
)

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            vector_store= aurora_db,
            embeddings_model_vector_dimension=embeddings_model_vector_dimension,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)

```

Example of importing existing `Amazon RDS Aurora PostgreSQL` using `fromExistingAuroraVectorStore()` method.
**Note** - you need to provide `clusterIdentifier`, `databaseName`, `vpc`, `secret` and `auroraSecurityGroupId` used in deployment of your existing RDS Amazon Aurora DB, as well as `embeddingsModel` that you want to be used by a Knowledge Base for chunking:

TypeScript

```python
import * as s3 from "aws-cdk-lib/aws-s3";
import { amazonaurora, bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const auroraDb = aurora.AmazonAuroraVectorStore.fromExistingAuroraVectorStore(stack, 'ExistingAuroraVectorStore', {
  clusterIdentifier: 'aurora-serverless-vector-cluster',
  databaseName: 'bedrock_vector_db',
  schemaName: 'bedrock_integration',
  tableName: 'bedrock_kb',
  vectorField: 'embedding',
  textField: 'chunks',
  metadataField: 'metadata',
  primaryKeyField: 'id',
  embeddingsModel: bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
  vpc: cdk.aws_ec2.Vpc.fromLookup(stack, 'VPC', {
    vpcId: 'vpc-0c1a234567ee8bc90',
  }),
  auroraSecurityGroupId: 'sg-012ef345678c98a76',,
  secret: cdk.aws_rds.DatabaseSecret.fromSecretCompleteArn(
    stack,
    'Secret',
    cdk.Stack.of(stack).formatArn({
      service: 'secretsmanager',
      resource: 'secret',
      resourceName: 'rds-db-credentials/cluster-1234567890',
      region: cdk.Stack.of(stack).region,
      account: cdk.Stack.of(stack).account,
      arnFormat: cdk.ArnFormat.COLON_RESOURCE_NAME,
    }),
  ),
});

const kb = new bedrock.KnowledgeBase(this, "KnowledgeBase", {
  vectorStore: auroraDb,
  embeddingsModel: bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
  instruction:
    "Use this knowledge base to answer questions about books. " +
    "It contains the full text of novels.",
});

const docBucket = new s3.Bucket(this, "DocBucket");

new bedrock.S3DataSource(this, "DataSource", {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: "books",
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
    aws_rds as rds,
    aws_ec2 as ec2,
    Stack,
    ArnFormat
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    amazonaurora,
)

aurora_db = amazonaurora.AmazonAuroraVectorStore.from_existing_aurora_vector_store(
    self, 'ExistingAuroraVectorStore',
    cluster_identifier='aurora-serverless-vector-cluster',
    database_name='bedrock_vector_db',
    schema_name='bedrock_integration',
    table_name='bedrock_kb',
    vector_field='embedding',
    text_field='chunks',
    metadata_field='metadata',
    primary_key_field='id',
    embeddings_model=bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
    vpc=ec2.Vpc.from_lookup(self, 'VPC', vpc_id='vpc-0c1a234567ee8bc90'),
    aurora_security_group_id='sg-012ef345678c98a76',,
    secret=rds.DatabaseSecret.from_secret_complete_arn(
        self,
        'Secret',
        Stack.of(self).format_arn(
            service= 'secretsmanager',
            resource= 'secret',
            resource_name= 'rds-db-credentials/cluster-1234567890',
            region= Stack.of(self).region,
            account= Stack.of(self).account,
            arn_format= ArnFormat.COLON_RESOURCE_NAME
        )
    )
)

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            vector_store= aurora_db,
            embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)
```

Example of `Pinecone` (manual, you must have Pinecone vector store created):

TypeScript

```python
import * as s3 from "aws-cdk-lib/aws-s3";
import { pinecone, bedrock } from "@cdklabs/generative-ai-cdk-constructs";

const pineconeds = new pinecone.PineconeVectorStore({
  connectionString: "https://your-index-1234567.svc.gcp-starter.pinecone.io",
  credentialsSecretArn: "arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name",
  textField: "question",
  metadataField: "metadata",
});

const kb = new bedrock.KnowledgeBase(this, "KnowledgeBase", {
  vectorStore: pineconeds,
  embeddingsModel: bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
  instruction: "Use this knowledge base to answer questions about books. " + "It contains the full text of novels.",
});

const docBucket = new s3.Bucket(this, "DocBucket");

new bedrock.S3DataSource(this, "DataSource", {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: "books",
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    pinecone,
)

pineconevs = pinecone.PineconeVectorStore(
            connection_string='https://your-index-1234567.svc.gcp-starter.pinecone.io',
            credentials_secret_arn='arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
            text_field='question',
            metadata_field='metadata'
        )

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            vector_store= pineconevs,
            embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
)
```

#### Knowledge Base - Data Sources

Data sources are the various repositories or systems from which information is extracted and ingested into the
knowledge base. These sources provide the raw content that will be processed, indexed, and made available for
querying within the knowledge base system. Data sources can include various types of systems such as document
management systems, databases, file storage systems, and content management platforms. Suuported Data Sources
include Amazon S3 buckets, Web Crawlers, SharePoint sites, Salesforce instances, and Confluence spaces.

* **Amazon S3**. You can either create a new data source using the `bedrock.S3DataSource(..)` class, or using the
  `kb.addS3DataSource(..)`.
* **Web Crawler**. You can either create a new data source using the `bedrock.WebCrawlerDataSource(..)` class, or using the
  `kb.addWebCrawlerDataSource(..)`.
* **Confluence**. You can either create a new data source using the `bedrock.ConfluenceDataSource(..)` class, or using the
  `kb.addConfluenceDataSource(..)`.
* **SharePoint**. You can either create a new data source using the `bedrock.SharePointDataSource(..)` class, or using the
  `kb.addSharePointDataSource(..)`.
* **Salesforce**. You can either create a new data source using the `bedrock.SalesforceDataSource(..)` class, or using the
  `kb.addSalesforceDataSource(..)`.

Typescript

```python
const app = new cdk.App();
const stack = new cdk.Stack(app, "aws-cdk-bedrock-data-sources-integ-test");

const kb = new KnowledgeBase(stack, "MyKnowledgeBase", {
  name: "MyKnowledgeBase",
  embeddingsModel: BedrockFoundationModel.COHERE_EMBED_MULTILINGUAL_V3,
});

const bucket = new Bucket(stack, "Bucket", {});
const lambdaFunction = new Function(stack, "MyFunction", {
  runtime: cdk.aws_lambda.Runtime.PYTHON_3_9,
  handler: "index.handler",
  code: cdk.aws_lambda.Code.fromInline('print("Hello, World!")'),
});

const secret = new Secret(stack, "Secret");
const key = new Key(stack, "Key");

kb.addWebCrawlerDataSource({
  sourceUrls: ["https://docs.aws.amazon.com/"],
  chunkingStrategy: ChunkingStrategy.HIERARCHICAL_COHERE,
  customTransformation: CustomTransformation.lambda({
    lambdaFunction: lambdaFunction,
    s3BucketUri: `s3://${bucket.bucketName}/chunk-processor/`,
  }),
});

kb.addS3DataSource({
  bucket,
  chunkingStrategy: ChunkingStrategy.SEMANTIC,
  parsingStrategy: ParsingStategy.foundationModel({
    model: BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  }),
});

kb.addConfluenceDataSource({
  dataSourceName: "TestDataSource",
  authSecret: secret,
  kmsKey: key,
  confluenceUrl: "https://example.atlassian.net",
  filters: [
    {
      objectType: ConfluenceObjectType.ATTACHMENT,
      includePatterns: [".*\\.pdf"],
      excludePatterns: [".*private.*\\.pdf"],
    },
    {
      objectType: ConfluenceObjectType.PAGE,
      includePatterns: [".*public.*\\.pdf"],
      excludePatterns: [".*confidential.*\\.pdf"],
    },
  ],
});

kb.addSalesforceDataSource({
  authSecret: secret,
  endpoint: "https://your-instance.my.salesforce.com",
  kmsKey: key,
  filters: [
    {
      objectType: SalesforceObjectType.ATTACHMENT,
      includePatterns: [".*\\.pdf"],
      excludePatterns: [".*private.*\\.pdf"],
    },
    {
      objectType: SalesforceObjectType.CONTRACT,
      includePatterns: [".*public.*\\.pdf"],
      excludePatterns: [".*confidential.*\\.pdf"],
    },
  ],
});

kb.addSharePointDataSource({
  dataSourceName: "SharepointDataSource",
  authSecret: secret,
  kmsKey: key,
  domain: "yourdomain",
  siteUrls: ["https://yourdomain.sharepoint.com/sites/mysite"],
  tenantId: "888d0b57-69f1-4fb8-957f-e1f0bedf64de",
  filters: [
    {
      objectType: SharePointObjectType.PAGE,
      includePatterns: [".*\\.pdf"],
      excludePatterns: [".*private.*\\.pdf"],
    },
    {
      objectType: SharePointObjectType.FILE,
      includePatterns: [".*public.*\\.pdf"],
      excludePatterns: [".*confidential.*\\.pdf"],
    },
  ],
});
```

Python

```python
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_secretsmanager as secretsmanager,
    aws_kms as kms
)
from constructs import Construct
from cdklabs.generative_ai_cdk_constructs import (
    bedrock
)

class PythonTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        kb = bedrock.KnowledgeBase(self, 'MyKnowledgeBase',
                    embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_MULTILINGUAL_V3,
                )

        docBucket = s3.Bucket(self, 'Bucket')

        function = _lambda.Function(self, 'MyFunction',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='index.handler',
            code=_lambda.Code.from_inline('print("Hello, World!")'),
        )

        kb.add_web_crawler_data_source(
            source_urls= ['https://docs.aws.amazon.com/'],
            chunking_strategy= bedrock.ChunkingStrategy.HIERARCHICAL_COHERE,
            custom_transformation= bedrock.CustomTransformation.lambda_(
                lambda_function= function,
                s3_bucket_uri= f's3://{docBucket.bucket_name}/chunk-processor/'
            )
        )

        kb.add_s3_data_source(
            bucket= docBucket,
            chunking_strategy= bedrock.ChunkingStrategy.SEMANTIC,
            parsing_strategy= bedrock.ParsingStategy.foundation_model(
                parsing_model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0.as_i_model(self)
            )
        )

        secret = secretsmanager.Secret(self, 'Secret')
        key = kms.Key(self, 'Key')

        kb.add_confluence_data_source(
            data_source_name='TestDataSource',
            auth_secret=secret,
            kms_key=key,
            confluence_url='https://example.atlassian.net',
            filters=[
                bedrock.ConfluenceCrawlingFilters(
                    object_type=bedrock.ConfluenceObjectType.ATTACHMENT,
                    include_patterns= [".*\\.pdf"],
                    exclude_patterns= [".*private.*\\.pdf"],
                ),
                bedrock.ConfluenceCrawlingFilters(
                    object_type=bedrock.ConfluenceObjectType.PAGE,
                    include_patterns= [".*public.*\\.pdf"],
                    exclude_patterns= [".*confidential.*\\.pdf"],
                ),
            ]
        )

        kb.add_salesforce_data_source(
            auth_secret=secret,
            endpoint='https://your-instance.my.salesforce.com',
            kms_key=key,
            filters=[
                bedrock.SalesforceCrawlingFilters(
                    object_type=bedrock.SalesforceObjectType.ATTACHMENT,
                    include_patterns= [".*\\.pdf"],
                    exclude_patterns= [".*private.*\\.pdf"],
                ),
                bedrock.SalesforceCrawlingFilters(
                    object_type=bedrock.SalesforceObjectType.CONTRACT,
                    include_patterns= [".*public.*\\.pdf"],
                    exclude_patterns= [".*confidential.*\\.pdf"],
                ),
            ]
        )

        kb.add_share_point_data_source(
            data_source_name='SharepointDataSource',
            auth_secret=secret,
            kms_key=key,
            domain='yourDomain',
            site_urls= ['https://yourdomain.sharepoint.com/sites/mysite'],
            tenant_id='888d0b57-69f1-4fb8-957f-e1f0bedf64de',
            filters=[
                bedrock.SharePointCrawlingFilters(
                    object_type=bedrock.SharePointObjectType.PAGE,
                    include_patterns= [".*\\.pdf"],
                    exclude_patterns= [".*private.*\\.pdf"],
                ),
                bedrock.SharePointCrawlingFilters(
                    object_type=bedrock.SharePointObjectType.FILE,
                    include_patterns= [".*public.*\\.pdf"],
                    exclude_patterns= [".*confidential.*\\.pdf"],
                ),
            ]
        )

```

#### Knowledge Base - Chunking Strategies

* **Default Chunking**: Applies Fixed Chunking with the default chunk size of 300 tokens and 20% overlap.

  TypeScript

  ```python
  ChunkingStrategy.DEFAULT;
  ```

  Python

  ```python
  ChunkingStrategy.DEFAULT;
  ```
* **Fixed Size Chunking**: This method divides the data into fixed-size chunks, with each chunk
  containing a predetermined number of tokens. This strategy is useful when the data is uniform
  in size and structure.
  Typescript

  TypeScript

  ```python
  // Fixed Size Chunking with sane defaults.
  ChunkingStrategy.FIXED_SIZE;

  // Fixed Size Chunking with custom values.
  ChunkingStrategy.fixedSize({ maxTokens: 200, overlapPercentage: 25 });
  ```

  Python

  ```python
  # Fixed Size Chunking with sane defaults.
  ChunkingStrategy.FIXED_SIZE;

  # Fixed Size Chunking with custom values.
  ChunkingStrategy.fixed_size(
    max_tokens= 200,
    overlap_percentage= 25
  )
  ```
* **Hierarchical Chunking**: This strategy organizes data into layers of chunks, with the first
  layer containing large chunks and the second layer containing smaller chunks derived from the first.
  It is ideal for data with inherent hierarchies or nested structures.

  TypeScript

  ```python
  // Hierarchical Chunking with the default for Cohere Models.
  ChunkingStrategy.HIERARCHICAL_COHERE;

  // Hierarchical Chunking with the default for Titan Models.
  ChunkingStrategy.HIERARCHICAL_TITAN;

  // Hierarchical Chunking with custom values. Tthe maximum chunk size depends on the model.
  // Amazon Titan Text Embeddings: 8192. Cohere Embed models: 512
  ChunkingStrategy.hierarchical({
    overlapTokens: 60,
    maxParentTokenSize: 1500,
    maxChildTokenSize: 300,
  });
  ```

  Python

  ```python
  # Hierarchical Chunking with the default for Cohere Models.
  ChunkingStrategy.HIERARCHICAL_COHERE

  # Hierarchical Chunking with the default for Titan Models.
  ChunkingStrategy.HIERARCHICAL_TITAN

  # Hierarchical Chunking with custom values. Tthe maximum chunk size depends on the model.
  # Amazon Titan Text Embeddings: 8192. Cohere Embed models: 512
  chunking_strategy= ChunkingStrategy.hierarchical(
      overlap_tokens=60,
      max_parent_token_size=1500,
      max_child_token_size=300
  )
  ```
* **Semantic Chunking**: This method splits data into smaller documents based on groups of similar
  content derived from the text using natural language processing. It helps preserve contextual
  relationships and ensures accurate and contextually appropriate results.

  TypeScript

  ```python
  // Semantic Chunking with sane defaults.
  ChunkingStrategy.SEMANTIC;

  // Semantic Chunking with custom values.
  ChunkingStrategy.semantic({ bufferSize: 0, breakpointPercentileThreshold: 95, maxTokens: 300 });
  ```

  Python

  ```python
  # Semantic Chunking with sane defaults.
  ChunkingStrategy.SEMANTIC

  # Semantic Chunking with custom values.
  ChunkingStrategy.semantic(
    buffer_size=0,
    breakpoint_percentile_threshold=95,
    max_tokens=300
  )
  ```
* **No Chunking**: This strategy treats each file as one chunk. If you choose this option,
  you may want to pre-process your documents by splitting them into separate files.

  TypeScript

  ```python
  ChunkingStrategy.NONE;
  ```

  Python

  ```python
  ChunkingStrategy.NONE;
  ```

#### Knowledge Base - Parsing Strategy

A parsing strategy in Amazon Bedrock is a configuration that determines how the service
processes and interprets the contents of a document. It involves converting the document's
contents into text and splitting it into smaller chunks for analysis. Amazon Bedrock offers
two parsing strategies:

* **Default Parsing Strategy**: This strategy converts the document's contents into text
  and splits it into chunks using a predefined approach. It is suitable for most use cases
  but may not be optimal for specific document types or requirements.
* **Foundation Model Parsing Strategy**: This strategy uses a foundation model to describe
  the contents of the document. It is particularly useful for improved processing of PDF files
  with tables and images. To use this strategy, set the `parsingStrategy` in a data source as below.

  TypeScript

  ```python
  bedrock.ParsingStategy.foundationModel({
    model: BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  });
  ```

  Python

  ```python
  bedrock.ParsingStategy.foundation_model(
      parsing_model=BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0
  )
  ```

#### Knowledge Base - Custom Transformation

Custom Transformation in Amazon Bedrock is a feature that allows you to create and apply
custom processing steps to documents moving through a data source ingestion pipeline.

Custom Transformation uses AWS Lambda functions to process documents, enabling you to
perform custom operations such as data extraction, normalization, or enrichment. To
create a custom transformation, set the `customTransformation` in a data source as below.

TypeScript

```python
CustomTransformation.lambda({
lambdaFunction: lambdaFunction,
s3BucketUri: `s3://${bucket.bucketName}/chunk-processor/`,
}),
```

Python

```python
CustomTransformation.lambda_(
  lambda_function= function,
  s3_bucket_uri= f's3://{docBucket.bucket_name}/chunk-processor/'
)
```

## Agents

Enable generative AI applications to execute multistep tasks across company systems and data sources.

### Create an Agent

The following example creates an Agent with a simple instruction and default prompts that consults a Knowledge Base.

TypeScript

```python
const agent = new bedrock.Agent(this, "Agent", {
  foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
  instruction: "You are a helpful and friendly agent that answers questions about literature.",
});

agent.addKnowledgeBase(kb);
```

Python

```python
agent = bedrock.Agent(
    self,
    "Agent",
    foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
    instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
)
  agent.add_knowledge_base(kb);
```

You can also use system defined inference profiles to enable cross region inference requests for supported models. For instance:

TypeScript

```python
const cris = bedrock.CrossRegionInferenceProfile.fromConfig({
  geoRegion: bedrock.CrossRegionInferenceProfileRegion.US,
  model: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
});

const agent = new bedrock.Agent(this, 'Agent', {
  foundationModel: cris,
  instruction: 'You are a helpful and friendly agent that answers questions about agriculture.'
});
```

Python

```python
cris = bedrock.CrossRegionInferenceProfile.from_config(
  geo_region= bedrock.CrossRegionInferenceProfileRegion.US,
  model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0
)

agent = bedrock.Agent(
    self,
    "Agent",
    foundation_model=cris,
    instruction="You are a helpful and friendly agent that answers questions about agriculture.",
)
```

For more information on cross region inference, please refer to [System defined inference profiles](#system-defined-inference-profiles)

### Action Groups

An action group defines functions your agent can call. The functions are Lambda functions. The action group uses an OpenAPI schema to tell the agent what your functions do and how to call them.

```python
const actionGroupFunction = new lambda_python.PythonFunction(this, "ActionGroupFunction", {
  runtime: lambda.Runtime.PYTHON_3_12,
  entry: path.join(__dirname, "../lambda/action-group"),
});

const actionGroup = new bedrock.AgentActionGroup(this, "MyActionGroup", {
  actionGroupName: "query-library",
  description: "Use these functions to get information about the books in the library.",
  actionGroupExecutor: {
    lambda: actionGroupFunction,
  },
  actionGroupState: "ENABLED",
  apiSchema: bedrock.ApiSchema.fromAsset(path.join(__dirname, "action-group.yaml")),
});

agent.addActionGroup(actionGroup);
```

Python

```python

action_group_function = PythonFunction(
            self,
            "LambdaFunction",
            runtime=Runtime.PYTHON_3_12,
            entry="./lambda",
            index="app.py",
            handler="lambda_handler",
)

actionGroup = bedrock.AgentActionGroup(self,
    "MyActionGroup",
    action_group_name="query-library",
    description="Use these functions to get information about the books in the library.",
    action_group_executor= bedrock.ActionGroupExecutor(
      lambda_=action_group_function
    ),
    action_group_state="ENABLED",
    api_schema=bedrock.ApiSchema.from_asset("action-group.yaml"))

agent.add_action_group(actionGroup)
```

### Prepare the Agent

The `Agent` constructs take an optional parameter `shouldPrepareAgent` to indicate that the Agent should be prepared after any updates to an agent, Knowledge Base association, or action group. This may increase the time to create and update those resources. By default, this value is false .

Creating an agent alias will not prepare the agent, so if you create an alias with `addAlias` or by providing an `aliasName` when creating the agent then you should set `shouldPrepareAgent` to ***true***.

#### Prompt Overrides

Bedrock Agents allows you to customize the prompts and LLM configuration for its different steps. You can disable steps or create a new prompt template. Prompt templates can be inserted from plain text files.

TypeScript

```python
import { readFileSync } from "fs";

const orchestration = readFileSync("prompts/orchestration.txt", "utf-8");
const agent = new bedrock.Agent(this, "Agent", {
  foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
  instruction: "You are a helpful and friendly agent that answers questions about literature.",
  promptOverrideConfiguration: {
    promptConfigurations: [
      {
        promptType: bedrock.PromptType.PRE_PROCESSING,
        promptState: bedrock.PromptState.DISABLED,
        promptCreationMode: bedrock.PromptCreationMode.OVERRIDDEN,
        basePromptTemplate: "disabled",
        inferenceConfiguration: {
          temperature: 0.0,
          topP: 1,
          topK: 250,
          maximumLength: 1,
          stopSequences: ["\n\nHuman:"],
        },
      },
      {
        promptType: bedrock.PromptType.ORCHESTRATION,
        basePromptTemplate: orchestration,
        promptState: bedrock.PromptState.ENABLED,
        promptCreationMode: bedrock.PromptCreationMode.OVERRIDDEN,
        inferenceConfiguration: {
          temperature: 0.0,
          topP: 1,
          topK: 250,
          maximumLength: 2048,
          stopSequences: ["</invoke>", "</answer>", "</error>"],
        },
      },
    ],
  },
});
```

Python

```python
orchestration = open('prompts/orchestration.txt', encoding="utf-8").read()
agent = bedrock.Agent(self, "Agent",
            foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
            instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
            prompt_override_configuration= bedrock.PromptOverrideConfiguration(
                prompt_configurations=[
                    bedrock.PromptConfiguration(
                        prompt_type=bedrock.PromptType.PRE_PROCESSING,
                        prompt_state=bedrock.PromptState.DISABLED,
                        prompt_creation_mode=bedrock.PromptCreationMode.OVERRIDDEN,
                        base_prompt_template="disabled",
                        inference_configuration=bedrock.InferenceConfiguration(
                            temperature=0.0,
                            top_k=250,
                            top_p=1,
                            maximum_length=1,
                            stop_sequences=['\n\nHuman:'],
                        )
                    ),
                    bedrock.PromptConfiguration(
                        prompt_type=bedrock.PromptType.ORCHESTRATION,
                        prompt_state=bedrock.PromptState.ENABLED,
                        prompt_creation_mode=bedrock.PromptCreationMode.OVERRIDDEN,
                        base_prompt_template=orchestration,
                        inference_configuration=bedrock.InferenceConfiguration(
                            temperature=0.0,
                            top_k=250,
                            top_p=1,
                            maximum_length=2048,
                            stop_sequences=['</invoke>', '</answer>', '</error>'],
                        )
                    )
                ]
            ),
        )
```

### Agent Alias

After you have sufficiently iterated on your working draft and are satisfied with the behavior of your agent, you can set it up for deployment and integration into your application by creating aliases of your agent.

To deploy your agent, you need to create an alias. During alias creation, Amazon Bedrock automatically creates a version of your agent. The alias points to this newly created version. You can point the alias to a previously created version if necessary. You then configure your application to make API calls to that alias.

By default, the `Agent` resource does not create any aliases, and you can use the 'DRAFT' version.

#### Tracking the latest version

The `Agent` resource optionally takes an `aliasName` property that, if defined, will create an Alias that creates a new version on every change.

TypeScript

```python
const agent = new bedrock.Agent(this, "Agent", {
  foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
  instruction: "You are a helpful and friendly agent that answers questions about literature.",
  knowledgeBases: [kb],
  aliasName: "latest",
});
```

Python

```python
agent = bedrock.Agent(
    self,
    "Agent",
    foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
    instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
    knowledge_bases= [kb],
    alias_name='latest'
)
```

#### Specific version

Using the `addAlias` method you can create aliases with a specific agent version.

TypeScript

```python
agent.addAlias({
  aliasName: "prod",
  agentVersion: "12",
});
```

Python

```python
agent.add_alias(
    alias_name='prod',
    agent_version='12'
)
```

Alternatively, you can use the `AgentAlias` resource if you want to create an Alias for an existing Agent.

TypeScript

```python
const alias = new bedrock.AgentAlias(this, "ProdAlias", {
  agentId: "ABCDE12345",
  aliasName: "prod",
  agentVersion: "12",
});
```

Python

```python
alias = bedrock.AgentAlias(self, 'ProdAlias',
    agent_id='ABCDE12345',
    alias_name='prod',
    agent_version='12'
)
```

## Bedrock Guardrails

Amazon Bedrock's Guardrails feature enables you to implement robust governance and control mechanisms for your generative AI applications, ensuring alignment with your specific use cases and responsible AI policies. Guardrails empowers you to create multiple tailored policy configurations, each designed to address the unique requirements and constraints of different use cases. These policy configurations can then be seamlessly applied across multiple foundation models (FMs) and Agents, ensuring a consistent user experience and standardizing safety, security, and privacy controls throughout your generative AI ecosystem.

With Guardrails, you can define and enforce granular, customizable policies to precisely govern the behavior of your generative AI applications. You can configure the following policies in a guardrail to avoid undesirable and harmful content and remove sensitive information for privacy protection.

Content filters – Adjust filter strengths to block input prompts or model responses containing harmful content.

Denied topics – Define a set of topics that are undesirable in the context of your application. These topics will be blocked if detected in user queries or model responses.

Word filters – Configure filters to block undesirable words, phrases, and profanity. Such words can include offensive terms, competitor names etc.

Sensitive information filters – Block or mask sensitive information such as personally identifiable information (PII) or custom regex in user inputs and model responses.

You can create a Guardrail with a minimum blockedInputMessaging ,blockedOutputsMessaging and default content filter policy.

TypeScript

```python
const guardrails = new bedrock.Guardrail(this, "bedrockGuardrails", {
  name: "my-BedrockGuardrails",
  description: "Legal ethical guardrails.",
});

// Optional - Add Sensitive information filters

guardrail.addPIIFilter({
  type: PIIType.General.ADDRESS,
  action: GuardrailAction.ANONYMIZE,
});

guardrail.addRegexFilter({
  name: "TestRegexFilter",
  description: "This is a test regex filter",
  pattern: "/^[A-Z]{2}d{6}$/",
  action: bedrock.GuardrailAction.ANONYMIZE,
});

// Optional - Add contextual grounding

guardrail.addContextualGroundingFilter({
  type: ContextualGroundingFilterType.GROUNDING,
  threshold: 0.95,
});

guardrail.addContextualGroundingFilter({
  type: ContextualGroundingFilterType.RELEVANCE,
  threshold: 0.95,
});

// Optional - Add Denied topics . You can use a Topic or create your custom Topic

guardrail.addDeniedTopicFilter(Topic.FINANCIAL_ADVICE);
guardrail.addDeniedTopicFilter(
  Topic.custom({
    name: "Legal_Advice",
    definition:
      "Offering guidance or suggestions on legal matters, legal actions, interpretation of laws, or legal rights and responsibilities.",
    examples: [
      "Can I sue someone for this?",
      "What are my legal rights in this situation?",
      "Is this action against the law?",
      "What should I do to file a legal complaint?",
      "Can you explain this law to me?",
    ],
  })
);

// Optional - Add Word filters. You can upload words from a file with addWordFilterFromFile function.
guardrail.addWordFilter("drugs");
guardrail.addManagedWordListFilter(ManagedWordFilterType.PROFANITY);
guardrails.addWordFilterFromFile("./scripts/wordsPolicy.csv");

// versioning - if you change any guardrail configuration, a new version will be created
guardrails.createVersion("testversion");

// Importing existing guardrail
const importedGuardrail = bedrock.Guardrail.fromGuardrailAttributes(stack, "TestGuardrail", {
  guardrailArn: "arn:aws:bedrock:us-east-1:123456789012:guardrail/oygh3o8g7rtl",
  guardrailVersion: "1", //optional
  kmsKey: kmsKey, //optional
});

// Importing Guardrails created through the L1 CDK CfnGuardrail construct
const cfnGuardrail = new CfnGuardrail(this, "MyCfnGuardrail", {
  blockedInputMessaging: "blockedInputMessaging",
  blockedOutputsMessaging: "blockedOutputsMessaging",
  name: "namemycfnguardrails",
  wordPolicyConfig: {
    wordsConfig: [
      {
        text: "drugs",
      },
    ],
  },
});

const importedGuardrail = bedrock.Guardrail.fromCfnGuardrail(cfnGuardrail);
```

Python

```python
    guardrail = bedrock.Guardrail(self, 'myGuardrails',
        name='my-BedrockGuardrails',
        description= "Legal ethical guardrails.")

    # Optional - Add Sensitive information filters

    guardrail.add_pii_filter(
        type= bedrock.pii_type.General.ADDRESS,
        action= bedrock.GuardrailAction.ANONYMIZE,
    )

    guardrail.add_regex_filter(
        name= "TestRegexFilter",
        description= "This is a test regex filter",
        pattern= "/^[A-Z]{2}d{6}$/",
        action= bedrock.GuardrailAction.ANONYMIZE,
    )

    # Optional - Add contextual grounding

    guardrail.add_contextual_grounding_filter(
        type= bedrock.ContextualGroundingFilterType.GROUNDING,
        threshold= 0.95,
    )

    # Optional - Add Denied topics . You can use default Topic or create your custom Topic with createTopic function. The default Topics can also be overwritten.

    guardrail.add_contextual_grounding_filter(
        type= bedrock.ContextualGroundingFilterType.RELEVANCE,
        threshold= 0.95,
    )

    guardrail.add_denied_topic_filter(bedrock.Topic.FINANCIAL_ADVICE)

    guardrail.add_denied_topic_filter(
      bedrock.Topic.custom(
        name= "Legal_Advice",
        definition=
            "Offering guidance or suggestions on legal matters, legal actions, interpretation of laws, or legal rights and responsibilities.",
        examples= [
            "Can I sue someone for this?",
            "What are my legal rights in this situation?",
            "Is this action against the law?",
            "What should I do to file a legal complaint?",
            "Can you explain this law to me?",
        ]
      )
    )

    # Optional - Add Word filters. You can upload words from a file with addWordFilterFromFile function.
    guardrail.add_word_filter("drugs")
    guardrail.add_managed_word_list_filter(bedrock.ManagedWordFilterType.PROFANITY)
    guardrail.add_word_filter_from_file("./scripts/wordsPolicy.csv")

    # versioning - if you change any guardrail configuration, a new version will be created
    guardrail.create_version("testversion")

    # Importing existing guardrail
    imported_guardrail = bedrock.Guardrail.from_guardrail_attributes(self, "TestGuardrail",
      guardrail_arn="arn:aws:bedrock:us-east-1:123456789012:guardrail/oygh3o8g7rtl",
      guardrail_version="1",
      kms_key=kms_key
    )

    # Importing Guardrails created through the L1 CDK CfnGuardrail construct
    cfn_guardrail = cfnbedrock.CfnGuardrail(self, "MyCfnGuardrail",
        blocked_input_messaging="blockedInputMessaging",
        blocked_outputs_messaging="blockedOutputsMessaging",
        name="name",

        # the properties below are optional
        word_policy_config=cfnbedrock.CfnGuardrail.WordPolicyConfigProperty(
            words_config=[cfnbedrock.CfnGuardrail.WordConfigProperty(
                text="drugs"
            )]
        )
    )

    imported_guardrail = bedrock.Guardrail.from_cfn_guardrail(cfn_guardrail)



```

## Prompt management

Amazon Bedrock provides the ability to create and save prompts using Prompt management so that you can save
time by applying the same prompt to different workflows. You can include variables in the prompt so that you can
adjust the prompt for different use case.

The `Prompt` resource allows you to create a new prompt.
Example of `Prompt`:

**TypeScript**

```python
const cmk = new kms.Key(this, "cmk", {});
const claudeModel = BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0;

const variant1 = PromptVariant.text({
  variantName: "variant1",
  model: claudeModel,
  promptVariables: ["topic"],
  promptText: "This is my first text prompt. Please summarize our conversation on: {{topic}}.",
  inferenceConfiguration: {
    temperature: 1.0,
    topP: 0.999,
    maxTokens: 2000,
  },
});

const prompt1 = new Prompt(this, "prompt1", {
  promptName: "prompt1",
  description: "my first prompt",
  defaultVariant: variant1,
  variants: [variant1],
  encryptionKey: cmk,
});
```

### Prompt Variants

Prompt variants in the context of Amazon Bedrock refer to alternative configurations of a prompt,
including its message or the model and inference configurations used. Prompt variants allow you
to create different versions of a prompt, test them, and save the variant that works best for
your use case. You can add prompt variants to a prompt by creating a `PromptVariant` object and
specify the variants on prompt creation, or by using the `.addVariant(..)` method on a `Prompt` object.

Example of `PromptVariant`:

**TypeScript**

```python
...

const variant2 = PromptVariant.text({
  variantName: "variant2",
  model: claudeModel,
  promptVariables: [ "topic" ],
  promptText: "This is my second text prompt. Please summarize our conversation on: {{topic}}.",
  inferenceConfiguration: {
    temperature: 0.5,
    topP: 0.999,
    maxTokens: 2000,
  },
});

prompt1.addVariant(variant2);
```

### Prompt Version

A prompt version is a snapshot of a prompt at a specific point in time that you
create when you are satisfied with a set of configurations. Versions allow you to
deploy your prompt and easily switch between different configurations for your
prompt and update your application with the most appropriate version for your
use-case.

You can create a Prompt version by using the `PromptVersion` class or by using the `.createVersion(..)`
on a `Prompt` object. It is recommended to use the `.createVersion(..)` method. It uses a hash based mechanism
to update the version whenever a certain configuration property changes.

**TypeScript**

```python
new PromptVersion(prompt1, "my first version");
```

or alternatively:

```python
prompt1.createVersion("my first version");
```

## System defined inference profiles

You can build a CrossRegionInferenceProfile using a system defined inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. You can find the system defined inference profiles by navigating to your console (Amazon Bedrock -> Cross-region inference) or programmatically, for instance using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_inference_profiles.html).

Before using creating a CrossRegionInferenceProfile, ensure that you have access to the models and regions defined in the inference profiles. For instance, if you see the system defined inference profile "us.anthropic.claude-3-5-sonnet-20241022-v2:0" defined in your region, the table mentions that inference requests will be routed to US East (Virginia) us-east-1, US East (Ohio) us-east-2 and US West (Oregon) us-west-2. Thus, you need to have model access enabled in those regions for the model `anthropic.claude-3-5-sonnet-20241022-v2:0`. You can then create the CrossRegionInferenceProfile as follows:

TypeScript

```python
const cris = bedrock.CrossRegionInferenceProfile.fromConfig({
  geoRegion: bedrock.CrossRegionInferenceProfileRegion.US,
  model: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0
});
```

Python

```python
cris = bedrock.CrossRegionInferenceProfile.from_config(
  geo_region= bedrock.CrossRegionInferenceProfileRegion.US,
  model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0
)
```

## Application inference profile

You can create an application inference profile with one or more Regions to track usage and costs when invoking a model.

To create an application inference profile for one Region, specify a foundation model. Usage and costs for requests made to that Region with that model will be tracked.

To create an application inference profile for multiple Regions, specify a cross region (system-defined) inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. Usage and costs for requests made to the Regions in the inference profile will be tracked. You can find the system defined inference profiles by navigating to your console (Amazon Bedrock -> Cross-region inference) or programmatically, for instance using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_inference_profiles.html):

```
bedrock = session.client("bedrock", region_name="us-east-1")
bedrock.list_inference_profiles(typeEquals='SYSTEM_DEFINED')
```

Before using application inference profiles, ensure that:

* You have appropriate IAM permissions
* You have access to the models and regions defined in the inference profiles
* Ensure proper configuration of the required API permissions for inference profile-related actions

Specifically the role you are assuming needs to have permissions for following actions in the IAM policy

```
"Action": [
      "bedrock:GetInferenceProfile",
      "bedrock:ListInferenceProfiles",
      "bedrock:DeleteInferenceProfile"
      "bedrock:TagResource",
      "bedrock:UntagResource",
      "bedrock:ListTagsForResource"
  ]
```

You can restrict to specific resources by applying "Resources" tag in the IAM policy.

```
"Resource": ["arn:aws:bedrock:*:*:application-inference-profile/*"]
```

TypeScript

```python
// Create an application inference profile for one Region
// You can use the 'bedrock.BedrockFoundationModel' or pass the arn as a string
const appInfProfile1 = new ApplicationInferenceProfile(this, 'myapplicationprofile', {
  inferenceProfileName: 'claude 3 sonnet v1',
  modelSource: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  tags: [{key: 'test', value: 'test'}]
});

// To create an application inference profile across regions, specify the cross region inference profile
const cris = bedrock.CrossRegionInferenceProfile.fromConfig({
  geoRegion: bedrock.CrossRegionInferenceProfileRegion.US,
  model: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0
});

const appInfProfile2 = new ApplicationInferenceProfile(this, 'myapplicationprofile2', {
  inferenceProfileName: 'claude 3 sonnet v1',
  modelSource: cris
});

// Import a Cfn L1 construct created application inference profile
const cfnapp = new CfnApplicationInferenceProfile(this, 'mytestaip3', {
  inferenceProfileName: 'mytest',
  modelSource: {
    copyFrom: 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0',
  },
});

const appInfProfile3 = bedrock.ApplicationInferenceProfile.fromCfnApplicationInferenceProfile(cfnapp);

// Import an inference profile through attributes
const appInfProfile4 = bedrock.ApplicationInferenceProfile.fromApplicationInferenceProfileAttributes(this, 'TestAIP', {
  inferenceProfileArn: 'arn:aws:bedrock:us-east-1:XXXXX:application-inference-profile/ID',
  inferenceProfileIdentifier: 'arn:aws:bedrock:us-east-1:XXXXXXX:application-inference-profile/ID',
});
```

Python

```python

# Create an application inference profile for one Region
# You can use the 'bedrock.BedrockFoundationModel' or pass the arn as a string
appInfProfile1 = bedrock.ApplicationInferenceProfile(self, 'myapplicationprofile',
  inference_profile_name='claude 3 sonnet v1',
  model_source=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
  tags=[CfnTag(
    key="key",
    value="value"
  )]
)

# To create an application inference profile across regions, specify the cross region inference profile
cris = bedrock.CrossRegionInferenceProfile.from_config(
  geo_region= bedrock.CrossRegionInferenceProfileRegion.US,
  model= bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V2_0
)

appInfProfile2 = bedrock.ApplicationInferenceProfile(self, 'myapplicationprofile2',
  inference_profile_name='claude 35 sonnet v2',
  model_source=cris
)

# Import an inference profile through attributes
appInfProfile3 = bedrock.ApplicationInferenceProfile.from_application_inference_profile_attributes(self, 'TestAIP',
  inference_profile_arn='arn:aws:bedrock:us-east-1:XXXXX:application-inference-profile/ID',
  inference_profile_identifier='arn:aws:bedrock:us-east-1:XXXXXXX:application-inference-profile/ID',
)

# Import a Cfn L1 construct created application inference profile
cfnaip = CfnApplicationInferenceProfile(this, 'mytestaip4',
  inference_profile_name='mytest',
  model_source= CfnApplicationInferenceProfile.InferenceProfileModelSourceProperty(
    copy_from='arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
  ),
)

appInfProfile4 = bedrock.ApplicationInferenceProfile.from_cfn_application_inference_profile(cfnaip);
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

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_bedrock as _aws_cdk_aws_bedrock_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from ..amazonaurora import (
    AmazonAuroraVectorStore as _AmazonAuroraVectorStore_bde12a1e,
    ExistingAmazonAuroraVectorStore as _ExistingAmazonAuroraVectorStore_f7ccb819,
)
from ..opensearch_vectorindex import VectorIndex as _VectorIndex_e5d266e9
from ..opensearchserverless import VectorCollection as _VectorCollection_91bfdaa9
from ..pinecone import PineconeVectorStore as _PineconeVectorStore_c017c196
from .pii_type import (
    CanadaSpecific as _CanadaSpecific_f80239d8,
    Finance as _Finance_2430d674,
    General as _General_e613aa3a,
    InformationTechnology as _InformationTechnology_2f99a404,
    UKSpecific as _UKSpecific_c9314648,
    USASpecific as _USASpecific_fa88de63,
)


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ActionGroupExecutor",
    jsii_struct_bases=[],
    name_mapping={"custom_control": "customControl", "lambda_": "lambda"},
)
class ActionGroupExecutor:
    def __init__(
        self,
        *,
        custom_control: typing.Optional[builtins.str] = None,
        lambda_: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    ) -> None:
        '''
        :param custom_control: (experimental) To return the action group invocation results directly in the InvokeAgent response, specify RETURN_CONTROL .
        :param lambda_: (experimental) The Lambda function containing the business logic that is carried out upon invoking the action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2b432e6f12d6f658754ea77c80d65dbc15752f8cc95a3cb553790484127754)
            check_type(argname="argument custom_control", value=custom_control, expected_type=type_hints["custom_control"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_control is not None:
            self._values["custom_control"] = custom_control
        if lambda_ is not None:
            self._values["lambda_"] = lambda_

    @builtins.property
    def custom_control(self) -> typing.Optional[builtins.str]:
        '''(experimental) To return the action group invocation results directly in the InvokeAgent response, specify RETURN_CONTROL .

        :stability: experimental
        '''
        result = self._values.get("custom_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction]:
        '''(experimental) The Lambda function containing the business logic that is carried out upon invoking the action.

        :stability: experimental
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionGroupExecutor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AddAgentAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias_name": "aliasName",
        "agent_version": "agentVersion",
        "description": "description",
    },
)
class AddAgentAliasProps:
    def __init__(
        self,
        *,
        alias_name: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to add an Alias to an Agent.

        :param alias_name: (experimental) The name for the agent alias.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param description: (experimental) Description for the agent alias.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44b9cf8594977e12593faffc73197189c6b8c803579e66de51dc986e13c8d2a)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias_name": alias_name,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def alias_name(self) -> builtins.str:
        '''(experimental) The name for the agent alias.

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the agent to associate with the agent alias.

        :default: - Creates a new version of the agent.

        :stability: experimental
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the agent alias.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddAgentAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Agent(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Agent",
):
    '''(experimental) Deploy a Bedrock Agent.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        foundation_model: "IInvokable",
        instruction: builtins.str,
        action_groups: typing.Optional[typing.Sequence["AgentActionGroup"]] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_user_input: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        guardrail_configuration: typing.Optional[typing.Union["GuardrailConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        knowledge_bases: typing.Optional[typing.Sequence["KnowledgeBase"]] = None,
        name: typing.Optional[builtins.str] = None,
        prompt_override_configuration: typing.Optional[typing.Union["PromptOverrideConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        should_prepare_agent: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param foundation_model: (experimental) The Bedrock text foundation model for the agent to use.
        :param instruction: (experimental) A narrative instruction to provide the agent as context.
        :param action_groups: (experimental) AgentActionGroup to make available to the agent. Default: - No AgentActionGroup is used.
        :param alias_name: (experimental) Name of the alias for the agent. Default: - No alias is created.
        :param description: (experimental) A description of the agent. Default: - No description is provided.
        :param enable_user_input: (experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance. Default: - False
        :param encryption_key: (experimental) KMS encryption key to use for the agent. Default: - An AWS managed key is used.
        :param existing_role: (experimental) The existing IAM Role for the agent with a trust policy that allows the Bedrock service to assume the role.
        :param guardrail_configuration: (experimental) Guardrail configuration. Warning: If you provide a guardrail configuration through the constructor, you will need to provide the correct permissions for your agent to access the guardrails. If you want the permissions to be configured on your behalf, use the addGuardrail method. Default: - No guardrails associated to the agent.
        :param idle_session_ttl: (experimental) How long sessions should be kept open for the agent. Default: - 1 hour
        :param knowledge_bases: (experimental) Knowledge Bases to make available to the agent. Default: - No knowledge base is used.
        :param name: (experimental) The name of the agent. Default: - A name is automatically generated.
        :param prompt_override_configuration: (experimental) Overrides for the agent. Default: - No overrides are provided.
        :param should_prepare_agent: (experimental) Whether to prepare the agent for use. Default: - false
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627af24bb5e1ca4b3ebb82ecbd7a3f01cb1f5177248afdccbc1d0ffab70726de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentProps(
            foundation_model=foundation_model,
            instruction=instruction,
            action_groups=action_groups,
            alias_name=alias_name,
            description=description,
            enable_user_input=enable_user_input,
            encryption_key=encryption_key,
            existing_role=existing_role,
            guardrail_configuration=guardrail_configuration,
            idle_session_ttl=idle_session_ttl,
            knowledge_bases=knowledge_bases,
            name=name,
            prompt_override_configuration=prompt_override_configuration,
            should_prepare_agent=should_prepare_agent,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addActionGroup")
    def add_action_group(self, action_group: "AgentActionGroup") -> None:
        '''(experimental) Add action group to the agent.

        :param action_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417f1714f331f713e989d70b6417dbb800ceedf7de8245c42ba72cde605b3504)
            check_type(argname="argument action_group", value=action_group, expected_type=type_hints["action_group"])
        return typing.cast(None, jsii.invoke(self, "addActionGroup", [action_group]))

    @jsii.member(jsii_name="addActionGroups")
    def add_action_groups(
        self,
        action_groups: typing.Sequence["AgentActionGroup"],
    ) -> None:
        '''(experimental) Add action groups to the agent.

        :param action_groups: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd86fd4e92aa0f8ee4a2b95a5ad405d539c55043eec94bf739fcc7fc1455d7a4)
            check_type(argname="argument action_groups", value=action_groups, expected_type=type_hints["action_groups"])
        return typing.cast(None, jsii.invoke(self, "addActionGroups", [action_groups]))

    @jsii.member(jsii_name="addAlias")
    def add_alias(
        self,
        *,
        alias_name: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> "AgentAlias":
        '''(experimental) Add an alias to the agent.

        :param alias_name: (experimental) The name for the agent alias.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param description: (experimental) Description for the agent alias.

        :stability: experimental
        '''
        props = AddAgentAliasProps(
            alias_name=alias_name, agent_version=agent_version, description=description
        )

        return typing.cast("AgentAlias", jsii.invoke(self, "addAlias", [props]))

    @jsii.member(jsii_name="addGuardrail")
    def add_guardrail(self, guardrail: "IGuardrail") -> None:
        '''(experimental) Add guardrail to the agent.

        :param guardrail: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c85531cb630c4447db8a8385837856811c9de1f8891137d8afe73a3e03cd62)
            check_type(argname="argument guardrail", value=guardrail, expected_type=type_hints["guardrail"])
        return typing.cast(None, jsii.invoke(self, "addGuardrail", [guardrail]))

    @jsii.member(jsii_name="addKnowledgeBase")
    def add_knowledge_base(self, knowledge_base: "KnowledgeBase") -> None:
        '''(experimental) Add knowledge base to the agent.

        :param knowledge_base: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ea7a1a86c29879ce5949318dae4e0d40df1772332d09e26ac0eebfde38479d)
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        return typing.cast(None, jsii.invoke(self, "addKnowledgeBase", [knowledge_base]))

    @jsii.member(jsii_name="addKnowledgeBases")
    def add_knowledge_bases(
        self,
        knowledge_bases: typing.Sequence["KnowledgeBase"],
    ) -> None:
        '''(experimental) Add knowledge bases to the agent.

        :param knowledge_bases: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2617bd17ab91665385e57477c5d00b6dfffcd0be05ebe697f1f2d4ff1abc87)
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
        return typing.cast(None, jsii.invoke(self, "addKnowledgeBases", [knowledge_bases]))

    @builtins.property
    @jsii.member(jsii_name="agentArn")
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentArn"))

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="agentInstance")
    def agent_instance(self) -> _aws_cdk_aws_bedrock_ceddda9d.CfnAgent:
        '''(experimental) Instance of Agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnAgent, jsii.get(self, "agentInstance"))

    @builtins.property
    @jsii.member(jsii_name="agentversion")
    def agentversion(self) -> builtins.str:
        '''(experimental) The version for the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentversion"))

    @builtins.property
    @jsii.member(jsii_name="foundationModel")
    def foundation_model(self) -> "IInvokable":
        '''(experimental) The model used by the agent.

        :stability: experimental
        '''
        return typing.cast("IInvokable", jsii.get(self, "foundationModel"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''(experimental) The IAM role for the agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasId"))

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the agent alias.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasName"))

    @builtins.property
    @jsii.member(jsii_name="actionGroups")
    def action_groups(
        self,
    ) -> typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty]:
        '''(experimental) A list of action groups associated with the agent.

        :stability: experimental
        :private: true
        '''
        return typing.cast(typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty], jsii.get(self, "actionGroups"))

    @action_groups.setter
    def action_groups(
        self,
        value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362bb8b9135358d9388689544abcd0d0c9e8e45ae46a6dc95b075f20007b92ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="knowledgeBases")
    def knowledge_bases(
        self,
    ) -> typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty]:
        '''(experimental) A list of KnowledgeBases associated with the agent.

        :default: - No knowledge base is used.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty], jsii.get(self, "knowledgeBases"))

    @knowledge_bases.setter
    def knowledge_bases(
        self,
        value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8a2ba31fca57d8bfcd42f9f0c012e95f4a9a95f52fe008b4777fe99b12b466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBases", value) # pyright: ignore[reportArgumentType]


class AgentActionGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentActionGroup",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        action_group_name: builtins.str,
        action_group_executor: typing.Optional[typing.Union[ActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]] = None,
        action_group_state: typing.Optional[builtins.str] = None,
        api_schema: typing.Optional["ApiSchema"] = None,
        description: typing.Optional[builtins.str] = None,
        function_schema: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        parent_action_group_signature: typing.Optional[builtins.str] = None,
        skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param action_group_name: (experimental) The name of the action group. Default: - a name is generated by CloudFormation.
        :param action_group_executor: 
        :param action_group_state: (experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request.
        :param api_schema: (experimental) Contains details about the S3 object containing the OpenAPI schema for the action group. For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_.
        :param description: (experimental) A description of the action group.
        :param function_schema: (experimental) Defines functions that each define parameters that the agent needs to invoke from the user.
        :param parent_action_group_signature: (experimental) If you specify this value as AMAZON.UserInput, the agent will prompt additional information from the user when it doesn't have enough information to respond to an utterance. Leave this field blank if you don't want the agent to prompt additional information.
        :param skip_resource_in_use_check_on_delete: (experimental) Specifies whether the agent should skip the resource in use check on delete.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3c9934294b04067f270151310db783e3b9ecde240109d0eed3c691351ae119)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentActionGroupProps(
            action_group_name=action_group_name,
            action_group_executor=action_group_executor,
            action_group_state=action_group_state,
            api_schema=api_schema,
            description=description,
            function_schema=function_schema,
            parent_action_group_signature=parent_action_group_signature,
            skip_resource_in_use_check_on_delete=skip_resource_in_use_check_on_delete,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="actionGroupName")
    def action_group_name(self) -> builtins.str:
        '''(experimental) The unique identifier of the action group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "actionGroupName"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupProperty")
    def action_group_property(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty:
        '''(experimental) The action group.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty, jsii.get(self, "actionGroupProperty"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupExecutor")
    def action_group_executor(self) -> typing.Optional[ActionGroupExecutor]:
        '''(experimental) The Lambda function containing the business logic that is carried out upon invoking the action.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ActionGroupExecutor], jsii.get(self, "actionGroupExecutor"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupState")
    def action_group_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) The action group state.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionGroupState"))

    @builtins.property
    @jsii.member(jsii_name="apiSchema")
    def api_schema(self) -> typing.Optional["ApiSchemaConfig"]:
        '''(experimental) The API schema.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ApiSchemaConfig"], jsii.get(self, "apiSchema"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="functionSchema")
    def function_schema(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty]:
        '''(experimental) A list of action groups associated with the agent.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty], jsii.get(self, "functionSchema"))

    @builtins.property
    @jsii.member(jsii_name="parentActionGroupSignature")
    def parent_action_group_signature(self) -> typing.Optional[builtins.str]:
        '''(experimental) The parent action group signature.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentActionGroupSignature"))

    @builtins.property
    @jsii.member(jsii_name="skipResourceInUseCheckOnDelete")
    def skip_resource_in_use_check_on_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The skip resource in use check on delete.

        :default: - false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipResourceInUseCheckOnDelete"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentActionGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_group_name": "actionGroupName",
        "action_group_executor": "actionGroupExecutor",
        "action_group_state": "actionGroupState",
        "api_schema": "apiSchema",
        "description": "description",
        "function_schema": "functionSchema",
        "parent_action_group_signature": "parentActionGroupSignature",
        "skip_resource_in_use_check_on_delete": "skipResourceInUseCheckOnDelete",
    },
)
class AgentActionGroupProps:
    def __init__(
        self,
        *,
        action_group_name: builtins.str,
        action_group_executor: typing.Optional[typing.Union[ActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]] = None,
        action_group_state: typing.Optional[builtins.str] = None,
        api_schema: typing.Optional["ApiSchema"] = None,
        description: typing.Optional[builtins.str] = None,
        function_schema: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        parent_action_group_signature: typing.Optional[builtins.str] = None,
        skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param action_group_name: (experimental) The name of the action group. Default: - a name is generated by CloudFormation.
        :param action_group_executor: 
        :param action_group_state: (experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request.
        :param api_schema: (experimental) Contains details about the S3 object containing the OpenAPI schema for the action group. For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_.
        :param description: (experimental) A description of the action group.
        :param function_schema: (experimental) Defines functions that each define parameters that the agent needs to invoke from the user.
        :param parent_action_group_signature: (experimental) If you specify this value as AMAZON.UserInput, the agent will prompt additional information from the user when it doesn't have enough information to respond to an utterance. Leave this field blank if you don't want the agent to prompt additional information.
        :param skip_resource_in_use_check_on_delete: (experimental) Specifies whether the agent should skip the resource in use check on delete.

        :stability: experimental
        '''
        if isinstance(action_group_executor, dict):
            action_group_executor = ActionGroupExecutor(**action_group_executor)
        if isinstance(function_schema, dict):
            function_schema = _aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty(**function_schema)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47b674f810daa9a7bde371ad21ea6944cc41d81e91b4c04fca71b8f52c01288)
            check_type(argname="argument action_group_name", value=action_group_name, expected_type=type_hints["action_group_name"])
            check_type(argname="argument action_group_executor", value=action_group_executor, expected_type=type_hints["action_group_executor"])
            check_type(argname="argument action_group_state", value=action_group_state, expected_type=type_hints["action_group_state"])
            check_type(argname="argument api_schema", value=api_schema, expected_type=type_hints["api_schema"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument function_schema", value=function_schema, expected_type=type_hints["function_schema"])
            check_type(argname="argument parent_action_group_signature", value=parent_action_group_signature, expected_type=type_hints["parent_action_group_signature"])
            check_type(argname="argument skip_resource_in_use_check_on_delete", value=skip_resource_in_use_check_on_delete, expected_type=type_hints["skip_resource_in_use_check_on_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group_name": action_group_name,
        }
        if action_group_executor is not None:
            self._values["action_group_executor"] = action_group_executor
        if action_group_state is not None:
            self._values["action_group_state"] = action_group_state
        if api_schema is not None:
            self._values["api_schema"] = api_schema
        if description is not None:
            self._values["description"] = description
        if function_schema is not None:
            self._values["function_schema"] = function_schema
        if parent_action_group_signature is not None:
            self._values["parent_action_group_signature"] = parent_action_group_signature
        if skip_resource_in_use_check_on_delete is not None:
            self._values["skip_resource_in_use_check_on_delete"] = skip_resource_in_use_check_on_delete

    @builtins.property
    def action_group_name(self) -> builtins.str:
        '''(experimental) The name of the action group.

        :default: - a name is generated by CloudFormation.

        :stability: experimental
        '''
        result = self._values.get("action_group_name")
        assert result is not None, "Required property 'action_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_group_executor(self) -> typing.Optional[ActionGroupExecutor]:
        '''
        :stability: experimental
        '''
        result = self._values.get("action_group_executor")
        return typing.cast(typing.Optional[ActionGroupExecutor], result)

    @builtins.property
    def action_group_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request.

        :stability: experimental
        '''
        result = self._values.get("action_group_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_schema(self) -> typing.Optional["ApiSchema"]:
        '''(experimental) Contains details about the S3 object containing the OpenAPI schema for the action group.

        For more information, see
        `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_.

        :stability: experimental
        '''
        result = self._values.get("api_schema")
        return typing.cast(typing.Optional["ApiSchema"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the action group.

        :stability: experimental
        :remarks: This object is a Union. Only one member of this object can be specified or returned.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_schema(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty]:
        '''(experimental) Defines functions that each define parameters that the agent needs to invoke from the user.

        :stability: experimental
        '''
        result = self._values.get("function_schema")
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty], result)

    @builtins.property
    def parent_action_group_signature(self) -> typing.Optional[builtins.str]:
        '''(experimental) If you specify this value as AMAZON.UserInput, the agent will prompt additional information from the user when it doesn't have enough information to respond to an utterance. Leave this field blank if you don't want the agent to prompt additional information.

        :stability: experimental
        '''
        result = self._values.get("parent_action_group_signature")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_resource_in_use_check_on_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the agent should skip the resource in use check on delete.

        :stability: experimental
        '''
        result = self._values.get("skip_resource_in_use_check_on_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentActionGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_id": "agentId",
        "agent_version": "agentVersion",
        "alias_name": "aliasName",
        "description": "description",
        "resource_updates": "resourceUpdates",
        "tags": "tags",
    },
)
class AgentAliasProps:
    def __init__(
        self,
        *,
        agent_id: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Interface to create a new Agent Alias.

        :param agent_id: (experimental) The unique identifier of the agent.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param alias_name: (experimental) The name for the agent alias. Default: - 'latest'
        :param description: (experimental) Description for the agent alias.
        :param resource_updates: (experimental) The list of resource update timestamps to let CloudFormation determine when to update the alias.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cae66eefc5f4c5599e0686171b63cba4b3c09493c31167b8afaa8bff00da6cc)
            check_type(argname="argument agent_id", value=agent_id, expected_type=type_hints["agent_id"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resource_updates", value=resource_updates, expected_type=type_hints["resource_updates"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_id": agent_id,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if description is not None:
            self._values["description"] = description
        if resource_updates is not None:
            self._values["resource_updates"] = resource_updates
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent.

        :stability: experimental
        '''
        result = self._values.get("agent_id")
        assert result is not None, "Required property 'agent_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the agent to associate with the agent alias.

        :default: - Creates a new version of the agent.

        :stability: experimental
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the agent alias.

        :default: - 'latest'

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the agent alias.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_updates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The list of resource update timestamps to let CloudFormation determine when to update the alias.

        :stability: experimental
        '''
        result = self._values.get("resource_updates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentProps",
    jsii_struct_bases=[],
    name_mapping={
        "foundation_model": "foundationModel",
        "instruction": "instruction",
        "action_groups": "actionGroups",
        "alias_name": "aliasName",
        "description": "description",
        "enable_user_input": "enableUserInput",
        "encryption_key": "encryptionKey",
        "existing_role": "existingRole",
        "guardrail_configuration": "guardrailConfiguration",
        "idle_session_ttl": "idleSessionTTL",
        "knowledge_bases": "knowledgeBases",
        "name": "name",
        "prompt_override_configuration": "promptOverrideConfiguration",
        "should_prepare_agent": "shouldPrepareAgent",
        "tags": "tags",
    },
)
class AgentProps:
    def __init__(
        self,
        *,
        foundation_model: "IInvokable",
        instruction: builtins.str,
        action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_user_input: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        guardrail_configuration: typing.Optional[typing.Union["GuardrailConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        knowledge_bases: typing.Optional[typing.Sequence["KnowledgeBase"]] = None,
        name: typing.Optional[builtins.str] = None,
        prompt_override_configuration: typing.Optional[typing.Union["PromptOverrideConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        should_prepare_agent: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for a Bedrock Agent.

        :param foundation_model: (experimental) The Bedrock text foundation model for the agent to use.
        :param instruction: (experimental) A narrative instruction to provide the agent as context.
        :param action_groups: (experimental) AgentActionGroup to make available to the agent. Default: - No AgentActionGroup is used.
        :param alias_name: (experimental) Name of the alias for the agent. Default: - No alias is created.
        :param description: (experimental) A description of the agent. Default: - No description is provided.
        :param enable_user_input: (experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance. Default: - False
        :param encryption_key: (experimental) KMS encryption key to use for the agent. Default: - An AWS managed key is used.
        :param existing_role: (experimental) The existing IAM Role for the agent with a trust policy that allows the Bedrock service to assume the role.
        :param guardrail_configuration: (experimental) Guardrail configuration. Warning: If you provide a guardrail configuration through the constructor, you will need to provide the correct permissions for your agent to access the guardrails. If you want the permissions to be configured on your behalf, use the addGuardrail method. Default: - No guardrails associated to the agent.
        :param idle_session_ttl: (experimental) How long sessions should be kept open for the agent. Default: - 1 hour
        :param knowledge_bases: (experimental) Knowledge Bases to make available to the agent. Default: - No knowledge base is used.
        :param name: (experimental) The name of the agent. Default: - A name is automatically generated.
        :param prompt_override_configuration: (experimental) Overrides for the agent. Default: - No overrides are provided.
        :param should_prepare_agent: (experimental) Whether to prepare the agent for use. Default: - false
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if isinstance(guardrail_configuration, dict):
            guardrail_configuration = GuardrailConfiguration(**guardrail_configuration)
        if isinstance(prompt_override_configuration, dict):
            prompt_override_configuration = PromptOverrideConfiguration(**prompt_override_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5254c1c0482eaa66699188ff0467d936350a386bbe823d4ef46c9ba982f91c)
            check_type(argname="argument foundation_model", value=foundation_model, expected_type=type_hints["foundation_model"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument action_groups", value=action_groups, expected_type=type_hints["action_groups"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_user_input", value=enable_user_input, expected_type=type_hints["enable_user_input"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument guardrail_configuration", value=guardrail_configuration, expected_type=type_hints["guardrail_configuration"])
            check_type(argname="argument idle_session_ttl", value=idle_session_ttl, expected_type=type_hints["idle_session_ttl"])
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument prompt_override_configuration", value=prompt_override_configuration, expected_type=type_hints["prompt_override_configuration"])
            check_type(argname="argument should_prepare_agent", value=should_prepare_agent, expected_type=type_hints["should_prepare_agent"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "foundation_model": foundation_model,
            "instruction": instruction,
        }
        if action_groups is not None:
            self._values["action_groups"] = action_groups
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if description is not None:
            self._values["description"] = description
        if enable_user_input is not None:
            self._values["enable_user_input"] = enable_user_input
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if guardrail_configuration is not None:
            self._values["guardrail_configuration"] = guardrail_configuration
        if idle_session_ttl is not None:
            self._values["idle_session_ttl"] = idle_session_ttl
        if knowledge_bases is not None:
            self._values["knowledge_bases"] = knowledge_bases
        if name is not None:
            self._values["name"] = name
        if prompt_override_configuration is not None:
            self._values["prompt_override_configuration"] = prompt_override_configuration
        if should_prepare_agent is not None:
            self._values["should_prepare_agent"] = should_prepare_agent
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def foundation_model(self) -> "IInvokable":
        '''(experimental) The Bedrock text foundation model for the agent to use.

        :stability: experimental
        '''
        result = self._values.get("foundation_model")
        assert result is not None, "Required property 'foundation_model' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def instruction(self) -> builtins.str:
        '''(experimental) A narrative instruction to provide the agent as context.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        assert result is not None, "Required property 'instruction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_groups(self) -> typing.Optional[typing.List[AgentActionGroup]]:
        '''(experimental) AgentActionGroup to make available to the agent.

        :default: - No AgentActionGroup  is used.

        :stability: experimental
        '''
        result = self._values.get("action_groups")
        return typing.cast(typing.Optional[typing.List[AgentActionGroup]], result)

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the alias for the agent.

        :default: - No alias is created.

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the agent.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_user_input(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance.

        :default: - False

        :stability: experimental
        '''
        result = self._values.get("enable_user_input")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) KMS encryption key to use for the agent.

        :default: - An AWS managed key is used.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''(experimental) The existing IAM Role for the agent with a trust policy that allows the Bedrock service to assume the role.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def guardrail_configuration(self) -> typing.Optional["GuardrailConfiguration"]:
        '''(experimental) Guardrail configuration.

        Warning: If you provide a guardrail configuration through the constructor,
        you will need to provide the correct permissions for your agent to access
        the guardrails. If you want the permissions to be configured on your behalf,
        use the addGuardrail method.

        :default: - No guardrails associated to the agent.

        :stability: experimental
        '''
        result = self._values.get("guardrail_configuration")
        return typing.cast(typing.Optional["GuardrailConfiguration"], result)

    @builtins.property
    def idle_session_ttl(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) How long sessions should be kept open for the agent.

        :default: - 1 hour

        :stability: experimental
        '''
        result = self._values.get("idle_session_ttl")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def knowledge_bases(self) -> typing.Optional[typing.List["KnowledgeBase"]]:
        '''(experimental) Knowledge Bases to make available to the agent.

        :default: - No knowledge base is used.

        :stability: experimental
        '''
        result = self._values.get("knowledge_bases")
        return typing.cast(typing.Optional[typing.List["KnowledgeBase"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the agent.

        :default: - A name is automatically generated.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prompt_override_configuration(
        self,
    ) -> typing.Optional["PromptOverrideConfiguration"]:
        '''(experimental) Overrides for the agent.

        :default: - No overrides are provided.

        :stability: experimental
        '''
        result = self._values.get("prompt_override_configuration")
        return typing.cast(typing.Optional["PromptOverrideConfiguration"], result)

    @builtins.property
    def should_prepare_agent(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to prepare the agent for use.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("should_prepare_agent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiSchema(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApiSchema",
):
    '''(experimental) Bedrock Agents Action Group API Schema definition.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, path: builtins.str) -> "InlineApiSchema":
        '''(experimental) Loads the API Schema from a local disk path.

        :param path: Path to the Open API schema file in yaml or JSON.

        :return: ``InlineApiSchema`` with the contents of ``path``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9707019db7cf1339382bbfdc3c35863966765af6485a09c40c302a504ad6876d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("InlineApiSchema", jsii.sinvoke(cls, "fromAsset", [path]))

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> "S3ApiSchema":
        '''(experimental) API Schema as an S3 object.

        :param bucket: The S3 bucket.
        :param key: The object key.

        :return: ``S3ApiSchema`` with the S3 bucket and key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3690bdbded4fc41debce4f674af4ba9794363c793e9f2f52ac27a4069270b3a3)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("S3ApiSchema", jsii.sinvoke(cls, "fromBucket", [bucket, key]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, schema: builtins.str) -> "InlineApiSchema":
        '''(experimental) Inline code for API Schema.

        :param schema: The actual Open API schema.

        :return: ``InlineApiSchema`` with inline schema

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2792cc1fa0f16747e3820d17877eef4b648c9b158bc65527d5d5c852652166)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        return typing.cast("InlineApiSchema", jsii.sinvoke(cls, "fromInline", [schema]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "ApiSchemaConfig":
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        :stability: experimental
        '''
        ...


class _ApiSchemaProxy(ApiSchema):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "ApiSchemaConfig":
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63a27d3f3e9a3d4c529eccceaa09a947c740c16c6fc454bb2b8aaf2030cee7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("ApiSchemaConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApiSchema).__jsii_proxy_class__ = lambda : _ApiSchemaProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApiSchemaConfig",
    jsii_struct_bases=[],
    name_mapping={"payload": "payload", "s3": "s3"},
)
class ApiSchemaConfig:
    def __init__(
        self,
        *,
        payload: typing.Optional[builtins.str] = None,
        s3: typing.Optional[typing.Union["S3Identifier", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Result of binding ``ApiSchema`` into an ``ActionGroup``.

        :param payload: (experimental) The JSON or YAML-formatted payload defining the OpenAPI schema for the action group. (mutually exclusive with ``s3``)
        :param s3: (experimental) Contains details about the S3 object containing the OpenAPI schema for the action group. (mutually exclusive with ``payload``)

        :stability: experimental
        '''
        if isinstance(s3, dict):
            s3 = S3Identifier(**s3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a607944f95610e7de935c34b4ac51de5be66c1a19adb648c5e285f3ef483bbe7)
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if payload is not None:
            self._values["payload"] = payload
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''(experimental) The JSON or YAML-formatted payload defining the OpenAPI schema for the action group.

        (mutually exclusive with ``s3``)

        :stability: experimental
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional["S3Identifier"]:
        '''(experimental) Contains details about the S3 object containing the OpenAPI schema for the action group.

        (mutually exclusive with ``payload``)

        :stability: experimental
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["S3Identifier"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApplicationInferenceProfileAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "inference_profile_arn": "inferenceProfileArn",
        "inference_profile_identifier": "inferenceProfileIdentifier",
    },
)
class ApplicationInferenceProfileAttributes:
    def __init__(
        self,
        *,
        inference_profile_arn: builtins.str,
        inference_profile_identifier: builtins.str,
    ) -> None:
        '''(experimental) ****************************************************************************                     ATTRS FOR IMPORTED CONSTRUCT ***************************************************************************.

        :param inference_profile_arn: (experimental) The ARN of the application inference profile.
        :param inference_profile_identifier: (experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ea34e402b2535f2082177ac38775e1034896579d3693772035c4f45ca2d654)
            check_type(argname="argument inference_profile_arn", value=inference_profile_arn, expected_type=type_hints["inference_profile_arn"])
            check_type(argname="argument inference_profile_identifier", value=inference_profile_identifier, expected_type=type_hints["inference_profile_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inference_profile_arn": inference_profile_arn,
            "inference_profile_identifier": inference_profile_identifier,
        }

    @builtins.property
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        result = self._values.get("inference_profile_arn")
        assert result is not None, "Required property 'inference_profile_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inference_profile_identifier(self) -> builtins.str:
        '''(experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        result = self._values.get("inference_profile_identifier")
        assert result is not None, "Required property 'inference_profile_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInferenceProfileAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApplicationInferenceProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "inference_profile_name": "inferenceProfileName",
        "model_source": "modelSource",
        "description": "description",
        "tags": "tags",
    },
)
class ApplicationInferenceProfileProps:
    def __init__(
        self,
        *,
        inference_profile_name: builtins.str,
        model_source: "IInvokable",
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for creating a ApplicationInferenceProfile.

        :param inference_profile_name: (experimental) The name of the inference profile.
        :param model_source: (experimental) To create an application inference profile for one Region, specify a foundation model. Usage and costs for requests made to that Region with that model will be tracked. To create an application inference profile for multiple Regions, specify a cross region (system-defined) inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. Usage and costs for requests made to the Regions in the inference profile will be tracked.
        :param description: (experimental) Description of the inference profile.
        :param tags: (experimental) A list of tags associated with the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c9200d651e22ff89688db78ff2bdec2a56b7d93a7d2cb347b49efafe13b581c)
            check_type(argname="argument inference_profile_name", value=inference_profile_name, expected_type=type_hints["inference_profile_name"])
            check_type(argname="argument model_source", value=model_source, expected_type=type_hints["model_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inference_profile_name": inference_profile_name,
            "model_source": model_source,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def inference_profile_name(self) -> builtins.str:
        '''(experimental) The name of the inference profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-applicationinferenceprofile.html#cfn-bedrock-applicationinferenceprofile-inferenceprofilename
        :stability: experimental
        '''
        result = self._values.get("inference_profile_name")
        assert result is not None, "Required property 'inference_profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_source(self) -> "IInvokable":
        '''(experimental) To create an application inference profile for one Region, specify a foundation model.

        Usage and costs for requests made to that Region with that model will be tracked.

        To create an application inference profile for multiple Regions,
        specify a cross region (system-defined) inference profile.
        The inference profile will route requests to the Regions defined in
        the cross region (system-defined) inference profile that you choose.
        Usage and costs for requests made to the Regions in the inference profile will be tracked.

        :stability: experimental
        '''
        result = self._values.get("model_source")
        assert result is not None, "Required property 'model_source' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the inference profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-applicationinferenceprofile.html#cfn-bedrock-applicationinferenceprofile-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''(experimental) A list of tags associated with the inference profile.

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationInferenceProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.BedrockFoundationModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "supports_agents": "supportsAgents",
        "supports_cross_region": "supportsCrossRegion",
        "supports_knowledge_base": "supportsKnowledgeBase",
        "vector_dimensions": "vectorDimensions",
    },
)
class BedrockFoundationModelProps:
    def __init__(
        self,
        *,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1a21a71ca2d85f4b0cb18a5ce955b8c59bb0c4403b3d6f750c90739061d548)
            check_type(argname="argument supports_agents", value=supports_agents, expected_type=type_hints["supports_agents"])
            check_type(argname="argument supports_cross_region", value=supports_cross_region, expected_type=type_hints["supports_cross_region"])
            check_type(argname="argument supports_knowledge_base", value=supports_knowledge_base, expected_type=type_hints["supports_knowledge_base"])
            check_type(argname="argument vector_dimensions", value=vector_dimensions, expected_type=type_hints["vector_dimensions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if supports_agents is not None:
            self._values["supports_agents"] = supports_agents
        if supports_cross_region is not None:
            self._values["supports_cross_region"] = supports_cross_region
        if supports_knowledge_base is not None:
            self._values["supports_knowledge_base"] = supports_knowledge_base
        if vector_dimensions is not None:
            self._values["vector_dimensions"] = vector_dimensions

    @builtins.property
    def supports_agents(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Bedrock Agents can use this model.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_agents")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supports_cross_region(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Can be used with a Cross-Region Inference Profile.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_cross_region")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supports_knowledge_base(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Bedrock Knowledge Base can use this model.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_knowledge_base")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vector_dimensions(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Embedding models have different vector dimensions.

        Only applicable for embedding models.

        :stability: experimental
        '''
        result = self._values.get("vector_dimensions")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockFoundationModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChunkingStrategy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ChunkingStrategy",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fixedSize")
    @builtins.classmethod
    def fixed_size(
        cls,
        *,
        max_tokens: jsii.Number,
        overlap_percentage: jsii.Number,
    ) -> "ChunkingStrategy":
        '''(experimental) Method for customizing a fixed sized chunking strategy.

        :param max_tokens: The maximum number of tokens to include in a chunk.
        :param overlap_percentage: The percentage of overlap between adjacent chunks of a data source.

        :stability: experimental
        '''
        props = _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.FixedSizeChunkingConfigurationProperty(
            max_tokens=max_tokens, overlap_percentage=overlap_percentage
        )

        return typing.cast("ChunkingStrategy", jsii.sinvoke(cls, "fixedSize", [props]))

    @jsii.member(jsii_name="hierarchical")
    @builtins.classmethod
    def hierarchical(
        cls,
        *,
        max_child_token_size: jsii.Number,
        max_parent_token_size: jsii.Number,
        overlap_tokens: jsii.Number,
    ) -> "ChunkingStrategy":
        '''(experimental) Method for customizing a hierarchical chunking strategy.

        For custom chunking, the maximum token chunk size depends on the model.

        - Amazon Titan Text Embeddings: 8192
        - Cohere Embed models: 512

        :param max_child_token_size: (experimental) Maximum number of tokens that a child chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param max_parent_token_size: (experimental) Maximum number of tokens that a parent chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param overlap_tokens: (experimental) The overlap tokens between adjacent chunks.

        :stability: experimental
        '''
        props = HierarchicalChunkingProps(
            max_child_token_size=max_child_token_size,
            max_parent_token_size=max_parent_token_size,
            overlap_tokens=overlap_tokens,
        )

        return typing.cast("ChunkingStrategy", jsii.sinvoke(cls, "hierarchical", [props]))

    @jsii.member(jsii_name="semantic")
    @builtins.classmethod
    def semantic(
        cls,
        *,
        breakpoint_percentile_threshold: jsii.Number,
        buffer_size: jsii.Number,
        max_tokens: jsii.Number,
    ) -> "ChunkingStrategy":
        '''(experimental) Method for customizing a semantic chunking strategy.

        For custom chunking, the maximum token chunk size depends on the model.

        - Amazon Titan Text Embeddings: 8192
        - Cohere Embed models: 512

        :param breakpoint_percentile_threshold: The dissimilarity threshold for splitting chunks.
        :param buffer_size: The buffer size.
        :param max_tokens: The maximum number of tokens that a chunk can contain.

        :stability: experimental
        '''
        props = _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SemanticChunkingConfigurationProperty(
            breakpoint_percentile_threshold=breakpoint_percentile_threshold,
            buffer_size=buffer_size,
            max_tokens=max_tokens,
        )

        return typing.cast("ChunkingStrategy", jsii.sinvoke(cls, "semantic", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT")
    def DEFAULT(cls) -> "ChunkingStrategy":
        '''(experimental) Fixed Sized Chunking with the default chunk size of 300 tokens and 20% overlap.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "DEFAULT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FIXED_SIZE")
    def FIXED_SIZE(cls) -> "ChunkingStrategy":
        '''(experimental) Fixed Sized Chunking with the default chunk size of 300 tokens and 20% overlap.

        You can adjust these values based on your specific requirements using the
        ``ChunkingStrategy.fixedSize(params)`` method.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "FIXED_SIZE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIERARCHICAL_COHERE")
    def HIERARCHICAL_COHERE(cls) -> "ChunkingStrategy":
        '''(experimental) Hierarchical Chunking with the default for Cohere Models.

        - Overlap tokens: 30
        - Max parent token size: 500
        - Max child token size: 100

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "HIERARCHICAL_COHERE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIERARCHICAL_TITAN")
    def HIERARCHICAL_TITAN(cls) -> "ChunkingStrategy":
        '''(experimental) Hierarchical Chunking with the default for Titan Models.

        - Overlap tokens: 60
        - Max parent token size: 1500
        - Max child token size: 300

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "HIERARCHICAL_TITAN"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NONE")
    def NONE(cls) -> "ChunkingStrategy":
        '''(experimental) Amazon Bedrock treats each file as one chunk.

        Suitable for documents that
        are already pre-processed or text split.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "NONE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SEMANTIC")
    def SEMANTIC(cls) -> "ChunkingStrategy":
        '''(experimental) Semantic Chunking with the default of bufferSize: 0, breakpointPercentileThreshold: 95, and maxTokens: 300.

        You can adjust these values based on your specific requirements using the
        ``ChunkingStrategy.semantic(params)`` method.

        :stability: experimental
        '''
        return typing.cast("ChunkingStrategy", jsii.sget(cls, "SEMANTIC"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    @abc.abstractmethod
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        ...

    @configuration.setter
    @abc.abstractmethod
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty,
    ) -> None:
        ...


class _ChunkingStrategyProxy(ChunkingStrategy):
    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8c95b7bfa78b1915cee9f049873d2af67238c73953179ae4f9479b54751ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ChunkingStrategy).__jsii_proxy_class__ = lambda : _ChunkingStrategyProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CommonPromptVariantProps",
    jsii_struct_bases=[],
    name_mapping={"model": "model", "variant_name": "variantName"},
)
class CommonPromptVariantProps:
    def __init__(self, *, model: "IInvokable", variant_name: builtins.str) -> None:
        '''
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2752ca933595bdb580dc70b29b9d7fea9196785967ed1f46d44fff8b435477)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model": model,
            "variant_name": variant_name,
        }

    @builtins.property
    def model(self) -> "IInvokable":
        '''(experimental) The model which is used to run the prompt.

        The model could be a foundation
        model, a custom model, or a provisioned model.

        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def variant_name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        result = self._values.get("variant_name")
        assert result is not None, "Required property 'variant_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonPromptVariantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceCrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class ConfluenceCrawlingFilters:
    def __init__(
        self,
        *,
        object_type: "ConfluenceObjectType",
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Defines filters for crawling Confluence content.

        These filters allow you to include or exclude specific content based on object types and patterns.

        - For Spaces: Use the unique space key
        - For Pages: Use the main page title
        - For Blogs: Use the main blog title
        - For Comments: Use "Re: Page/Blog Title"
        - For Attachments: Use the filename with extension

        :param object_type: (experimental) The type of Confluence object to apply the filters to.
        :param exclude_patterns: (experimental) Regular expression patterns to exclude content. Content matching these patterns will not be crawled, even if it matches an include pattern.
        :param include_patterns: (experimental) Regular expression patterns to include content. If specified, only content matching these patterns will be crawled.

        :stability: experimental
        :remarks:

        - You can specify inclusion and exclusion patterns using regular expressions.
        - If both inclusion and exclusion patterns match a document, the exclusion takes precedence.

        Example::

            {
              objectType: ConfluenceObjectType.ATTACHMENT,
              excludePatterns: [".*private.*\\.pdf"]
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba4b91ab5b955d9d72d8af6f07cdc07ac568ef117419de41dca7871ad32d6b8)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type": object_type,
        }
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def object_type(self) -> "ConfluenceObjectType":
        '''(experimental) The type of Confluence object to apply the filters to.

        :stability: experimental
        '''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast("ConfluenceObjectType", result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to exclude content.

        Content matching these patterns will not be crawled, even if it matches an include pattern.

        :stability: experimental
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to include content.

        If specified, only content matching these patterns will be crawled.

        :stability: experimental
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfluenceCrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSourceAuthType"
)
class ConfluenceDataSourceAuthType(enum.Enum):
    '''(experimental) The different authentication types available to connect to your Confluence instance.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/confluence-data-source-connector.html#configuration-confluence-connector
    :stability: experimental
    '''

    OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"
    '''(experimental) Your secret authentication credentials in AWS Secrets Manager should include: - ``confluenceAppKey`` - ``confluenceAppSecret`` - ``confluenceAccessToken`` - ``confluenceRefreshToken``.

    :stability: experimental
    '''
    BASIC = "BASIC"
    '''(experimental) Your secret authentication credentials in AWS Secrets Manager should include:  - ``username`` (email of admin account)  - ``password`` (API token).

    :stability: experimental
    '''


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceObjectType"
)
class ConfluenceObjectType(enum.Enum):
    '''(experimental) Represents the different types of content objects in Confluence that can be crawled by the data source.

    :stability: experimental
    '''

    SPACE = "SPACE"
    '''
    :stability: experimental
    '''
    PAGE = "PAGE"
    '''
    :stability: experimental
    '''
    BLOG = "BLOG"
    '''
    :stability: experimental
    '''
    COMMENT = "COMMENT"
    '''
    :stability: experimental
    '''
    ATTACHMENT = "ATTACHMENT"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContentFilter",
    jsii_struct_bases=[],
    name_mapping={
        "input_strength": "inputStrength",
        "output_strength": "outputStrength",
        "type": "type",
    },
)
class ContentFilter:
    def __init__(
        self,
        *,
        input_strength: "ContentFilterStrength",
        output_strength: "ContentFilterStrength",
        type: "ContentFilterType",
    ) -> None:
        '''(experimental) Interface to declare a content filter.

        :param input_strength: (experimental) The strength of the content filter to apply to prompts / user input.
        :param output_strength: (experimental) The strength of the content filter to apply to model responses.
        :param type: (experimental) The type of harmful category that the content filter is applied to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a9140c0049260b2d312c4a80d1b958e9761476560ef6b565d603fce991e815)
            check_type(argname="argument input_strength", value=input_strength, expected_type=type_hints["input_strength"])
            check_type(argname="argument output_strength", value=output_strength, expected_type=type_hints["output_strength"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_strength": input_strength,
            "output_strength": output_strength,
            "type": type,
        }

    @builtins.property
    def input_strength(self) -> "ContentFilterStrength":
        '''(experimental) The strength of the content filter to apply to prompts / user input.

        :stability: experimental
        '''
        result = self._values.get("input_strength")
        assert result is not None, "Required property 'input_strength' is missing"
        return typing.cast("ContentFilterStrength", result)

    @builtins.property
    def output_strength(self) -> "ContentFilterStrength":
        '''(experimental) The strength of the content filter to apply to model responses.

        :stability: experimental
        '''
        result = self._values.get("output_strength")
        assert result is not None, "Required property 'output_strength' is missing"
        return typing.cast("ContentFilterStrength", result)

    @builtins.property
    def type(self) -> "ContentFilterType":
        '''(experimental) The type of harmful category that the content filter is applied to.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ContentFilterType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContentFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContentFilterStrength"
)
class ContentFilterStrength(enum.Enum):
    '''(experimental) The strength of the content filter.

    As you increase the filter strength,
    the likelihood of filtering harmful content increases and the probability
    of seeing harmful content in your application reduces.

    :stability: experimental
    '''

    NONE = "NONE"
    '''
    :stability: experimental
    '''
    LOW = "LOW"
    '''
    :stability: experimental
    '''
    MEDIUM = "MEDIUM"
    '''
    :stability: experimental
    '''
    HIGH = "HIGH"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContentFilterType")
class ContentFilterType(enum.Enum):
    '''(experimental) The type of harmful category usable in a content filter.

    :stability: experimental
    '''

    SEXUAL = "SEXUAL"
    '''(experimental) Describes input prompts and model responses that indicates sexual interest, activity, or arousal using direct or indirect references to body parts, physical traits, or sex.

    :stability: experimental
    '''
    VIOLENCE = "VIOLENCE"
    '''(experimental) Describes input prompts and model responses that includes glorification of or threats to inflict physical pain, hurt, or injury toward a person, group or thing.

    :stability: experimental
    '''
    HATE = "HATE"
    '''(experimental) Describes input prompts and model responses that discriminate, criticize, insult, denounce, or dehumanize a person or group on the basis of an identity (such as race, ethnicity, gender, religion, sexual orientation, ability, and national origin).

    :stability: experimental
    '''
    INSULTS = "INSULTS"
    '''(experimental) Describes input prompts and model responses that includes demeaning, humiliating, mocking, insulting, or belittling language.

    This type of language is also labeled
    as bullying.

    :stability: experimental
    '''
    MISCONDUCT = "MISCONDUCT"
    '''(experimental) Describes input prompts and model responses that seeks or provides information about engaging in misconduct activity, or harming, defrauding, or taking advantage of a person, group or institution.

    :stability: experimental
    '''
    PROMPT_ATTACK = "PROMPT_ATTACK"
    '''(experimental) Enable to detect and block user inputs attempting to override system instructions.

    To avoid misclassifying system prompts as a prompt attack and ensure that the filters
    are selectively applied to user inputs, use input tagging.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContextualGroundingFilter",
    jsii_struct_bases=[],
    name_mapping={"threshold": "threshold", "type": "type"},
)
class ContextualGroundingFilter:
    def __init__(
        self,
        *,
        threshold: jsii.Number,
        type: "ContextualGroundingFilterType",
    ) -> None:
        '''(experimental) Interface to define a Contextual Grounding Filter.

        :param threshold: (experimental) The threshold for the contextual grounding filter. - ``0`` (blocks nothing) - ``0.99`` (blocks almost everything)
        :param type: (experimental) The type of contextual grounding filter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e4288f485be62d723f6fe133287e8c88a90f455b2dec35e5c4095e4ba4cd69)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "type": type,
        }

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''(experimental) The threshold for the contextual grounding filter.

        - ``0`` (blocks nothing)
        - ``0.99`` (blocks almost everything)

        :stability: experimental
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> "ContextualGroundingFilterType":
        '''(experimental) The type of contextual grounding filter.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ContextualGroundingFilterType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContextualGroundingFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ContextualGroundingFilterType"
)
class ContextualGroundingFilterType(enum.Enum):
    '''(experimental) The type of contextual grounding filter.

    :stability: experimental
    '''

    GROUNDING = "GROUNDING"
    '''(experimental) Grounding score represents the confidence that the model response is factually correct and grounded in the source.

    If the model response has a lower score than
    the defined threshold, the response will be blocked and the configured blocked
    message will be returned to the user. A higher threshold level blocks more responses.

    :stability: experimental
    '''
    RELEVANCE = "RELEVANCE"
    '''(experimental) Relevance score represents the confidence that the model response is relevant to the user's query.

    If the model response has a lower score than the defined
    threshold, the response will be blocked and the configured blocked message will
    be returned to the user. A higher threshold level blocks more responses.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class CrawlingFilters:
    def __init__(
        self,
        *,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) The filters (regular expression patterns) to include or exclude in the crawling in accordance with your scope.

        :param exclude_patterns: (experimental) Exclude paths.
        :param include_patterns: (experimental) Include patterns.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8789f899b4cf122996f24d6718a644cc2bc6a74788ac86472a28afaba4e33f)
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Exclude paths.

        :stability: experimental
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Include patterns.

        :stability: experimental
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrawlingScope")
class CrawlingScope(enum.Enum):
    '''(experimental) The scope of the crawling.

    :stability: experimental
    '''

    HOST_ONLY = "HOST_ONLY"
    '''(experimental) Crawls only web pages that belong to the same host or primary domain.

    :stability: experimental
    '''
    SUBDOMAINS = "SUBDOMAINS"
    '''(experimental) Includes subdomains in addition to the host or primary domain, i.e. web pages that contain "aws.amazon.com" can also include sub domain "docs.aws.amazon.com".

    :stability: experimental
    '''
    DEFAULT = "DEFAULT"
    '''(experimental) Limit crawling to web pages that belong to the same host and with the same initial URL path.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrossRegionInferenceProfileProps",
    jsii_struct_bases=[],
    name_mapping={"geo_region": "geoRegion", "model": "model"},
)
class CrossRegionInferenceProfileProps:
    def __init__(
        self,
        *,
        geo_region: "CrossRegionInferenceProfileRegion",
        model: "BedrockFoundationModel",
    ) -> None:
        '''(experimental) ****************************************************************************                       PROPS FOR NEW CONSTRUCT ***************************************************************************.

        :param geo_region: (experimental) The geographic region where the traffic is going to be distributed. Routing factors in user traffic, demand and utilization of resources.
        :param model: (experimental) A model supporting cross-region inference.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0779b391b71e321d48d3445f56e45aa413e6050e51f0b7161ca653bdbdd424ab)
            check_type(argname="argument geo_region", value=geo_region, expected_type=type_hints["geo_region"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "geo_region": geo_region,
            "model": model,
        }

    @builtins.property
    def geo_region(self) -> "CrossRegionInferenceProfileRegion":
        '''(experimental) The geographic region where the traffic is going to be distributed.

        Routing
        factors in user traffic, demand and utilization of resources.

        :stability: experimental
        '''
        result = self._values.get("geo_region")
        assert result is not None, "Required property 'geo_region' is missing"
        return typing.cast("CrossRegionInferenceProfileRegion", result)

    @builtins.property
    def model(self) -> "BedrockFoundationModel":
        '''(experimental) A model supporting cross-region inference.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference-support.html
        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast("BedrockFoundationModel", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossRegionInferenceProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrossRegionInferenceProfileRegion"
)
class CrossRegionInferenceProfileRegion(enum.Enum):
    '''
    :stability: experimental
    '''

    EU = "EU"
    '''(experimental) Cross-region Inference Identifier for the European area.

    According to the model chosen, this might include:

    - Frankfurt (``eu-central-1``)
    - Ireland (``eu-west-1``)
    - Paris (``eu-west-3``)

    :stability: experimental
    '''
    US = "US"
    '''(experimental) Cross-region Inference Identifier for the United States area.

    According to the model chosen, this might include:

    - N. Virginia (``us-east-1``)
    - Oregon (``us-west-2``)
    - Ohio (``us-east-2``)

    :stability: experimental
    '''
    APAC = "APAC"
    '''(experimental) Cross-region Inference Identifier for the Asia-Pacific area.

    According to the model chosen, this might include:

    - Tokyo (``ap-northeast-1``)
    - Seoul (``ap-northeast-2``)
    - Mumbai (``ap-south-1``)
    - Singapore (``ap-southeast-1``)
    - Sydney (``ap-southeast-2``)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CustomTopicProps",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition", "examples": "examples", "name": "name"},
)
class CustomTopicProps:
    def __init__(
        self,
        *,
        definition: builtins.str,
        examples: typing.Sequence[builtins.str],
        name: builtins.str,
    ) -> None:
        '''(experimental) Interface for creating a custom Topic.

        :param definition: (experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic. Avoid starting with "don't".
        :param examples: (experimental) Representative phrases that refer to the topic. These phrases can represent a user input or a model response. Add up to 5 phrases, up to 100 characters each.
        :param name: (experimental) The name of the topic to deny.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afa8690bf8def1351745b409bf75b1c9388f7690948642485ab500130f04eab)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument examples", value=examples, expected_type=type_hints["examples"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "examples": examples,
            "name": name,
        }

    @builtins.property
    def definition(self) -> builtins.str:
        '''(experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic.

        Avoid starting with "don't".

        :stability: experimental

        Example::

            `Investment advice refers to inquiries, guidance, or recommendations
            regarding the management or allocation of funds or assets with the goal of
            generating returns or achieving specific financial objectives.`
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def examples(self) -> typing.List[builtins.str]:
        '''(experimental) Representative phrases that refer to the topic.

        These phrases can represent
        a user input or a model response. Add up to 5 phrases, up to 100 characters
        each.

        :stability: experimental

        Example::

            "Where should I invest my money?"
        '''
        result = self._values.get("examples")
        assert result is not None, "Required property 'examples' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the topic to deny.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomTransformation(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CustomTransformation",
):
    '''(experimental) Represents a custom transformation configuration for a data source ingestion.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html#kb-custom-transformation
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="lambda")
    @builtins.classmethod
    def lambda_(
        cls,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        s3_bucket_uri: builtins.str,
    ) -> "CustomTransformation":
        '''(experimental) This feature allows you to use a Lambda function to inject your own logic into the knowledge base ingestion process.

        :param lambda_function: (experimental) The Lambda function to use for custom document processing.
        :param s3_bucket_uri: (experimental) An S3 bucket URL/path to store input documents for Lambda processing and to store the output of the processed documents.

        :see: https://github.com/aws-samples/amazon-bedrock-samples/blob/main/knowledge-bases/features-examples/02-optimizing-accuracy-retrieved-results/advanced_chunking_options.ipynb
        :stability: experimental
        '''
        props = LambdaCustomTransformationProps(
            lambda_function=lambda_function, s3_bucket_uri=s3_bucket_uri
        )

        return typing.cast("CustomTransformation", jsii.sinvoke(cls, "lambda", [props]))

    @jsii.member(jsii_name="generatePolicyStatements")
    @abc.abstractmethod
    def generate_policy_statements(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :param scope: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="configuration")
    @abc.abstractmethod
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this custom transformation configuration.

        :stability: experimental
        '''
        ...

    @configuration.setter
    @abc.abstractmethod
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty,
    ) -> None:
        ...


class _CustomTransformationProxy(CustomTransformation):
    @jsii.member(jsii_name="generatePolicyStatements")
    def generate_policy_statements(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898a06e70f7f1a8abcf9e8433317e047be3a6f52316351b0d22de8a49154fb6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement], jsii.invoke(self, "generatePolicyStatements", [scope]))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this custom transformation configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ea7d98a453ed23a6d13ca01317dfc8f56bd010bb3d771347e4898118887260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CustomTransformation).__jsii_proxy_class__ = lambda : _CustomTransformationProxy


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataDeletionPolicy"
)
class DataDeletionPolicy(enum.Enum):
    '''(experimental) Specifies the policy for handling data when a data source resource is deleted.

    This policy affects the vector embeddings created from the data source.

    :stability: experimental
    '''

    DELETE = "DELETE"
    '''(experimental) Deletes all vector embeddings derived from the data source upon deletion of a data source resource.

    :stability: experimental
    '''
    RETAIN = "RETAIN"
    '''(experimental) Retains all vector embeddings derived from the data source even after deletion of a data source resource.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
    },
)
class DataSourceAssociationProps:
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> None:
        '''(experimental) Properties common for creating any of the different data source types.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3370fd8035498a3339649efe16f36fa523a3b651e8f4e3f2f7cc83f1af7f2c0)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional["ParsingStategy"]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional["ParsingStategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceType")
class DataSourceType(enum.Enum):
    '''(experimental) Represents the types of data sources that can be associated to an Knowledge Base.

    :stability: experimental
    '''

    S3 = "S3"
    '''(experimental) Amazon S3 Bucket data source.

    :stability: experimental
    '''
    CONFLUENCE = "CONFLUENCE"
    '''(experimental) Confluence Cloud Instance data source.

    :stability: experimental
    '''
    SALESFORCE = "SALESFORCE"
    '''(experimental) Salesforce instance data source.

    :stability: experimental
    '''
    SHAREPOINT = "SHAREPOINT"
    '''(experimental) Microsoft SharePoint instance data source.

    :stability: experimental
    '''
    WEB_CRAWLER = "WEB_CRAWLER"
    '''(experimental) Web Crawler data source.

    Extracts content from authorized public web pages using a crawler.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.FoundationModelParsingStategyProps",
    jsii_struct_bases=[],
    name_mapping={"parsing_model": "parsingModel", "parsing_prompt": "parsingPrompt"},
)
class FoundationModelParsingStategyProps:
    def __init__(
        self,
        *,
        parsing_model: "IInvokable",
        parsing_prompt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring a Foundation Model parsing strategy.

        :param parsing_model: (experimental) The Foundation Model to use for parsing non-textual information. Currently supported models are Claude 3 Sonnet and Claude 3 Haiku.
        :param parsing_prompt: (experimental) Custom prompt to instruct the parser on how to interpret the document. Default: - Uses the default instruction prompt as provided in the AWS Console.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed85f0ccfdf38b650635f35650195519e14f924af93233cef46e2fd5af61295)
            check_type(argname="argument parsing_model", value=parsing_model, expected_type=type_hints["parsing_model"])
            check_type(argname="argument parsing_prompt", value=parsing_prompt, expected_type=type_hints["parsing_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parsing_model": parsing_model,
        }
        if parsing_prompt is not None:
            self._values["parsing_prompt"] = parsing_prompt

    @builtins.property
    def parsing_model(self) -> "IInvokable":
        '''(experimental) The Foundation Model to use for parsing non-textual information.

        Currently supported models are Claude 3 Sonnet and Claude 3 Haiku.

        :stability: experimental
        '''
        result = self._values.get("parsing_model")
        assert result is not None, "Required property 'parsing_model' is missing"
        return typing.cast("IInvokable", result)

    @builtins.property
    def parsing_prompt(self) -> typing.Optional[builtins.str]:
        '''(experimental) Custom prompt to instruct the parser on how to interpret the document.

        :default: - Uses the default instruction prompt as provided in the AWS Console.

        :stability: experimental
        '''
        result = self._values.get("parsing_prompt")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FoundationModelParsingStategyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailAction")
class GuardrailAction(enum.Enum):
    '''(experimental) Guardrail action when a sensitive entity is detected.

    :stability: experimental
    '''

    BLOCK = "BLOCK"
    '''(experimental) If sensitive information is detected in the prompt or response, the guardrail blocks all the content and returns a message that you configure.

    :stability: experimental
    '''
    ANONYMIZE = "ANONYMIZE"
    '''(experimental) If sensitive information is detected in the model response, the guardrail masks it with an identifier, the sensitive information is masked and replaced with identifier tags (for example: [NAME-1], [NAME-2], [EMAIL-1], etc.).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "guardrail_arn": "guardrailArn",
        "guardrail_version": "guardrailVersion",
        "kms_key": "kmsKey",
    },
)
class GuardrailAttributes:
    def __init__(
        self,
        *,
        guardrail_arn: builtins.str,
        guardrail_version: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''(experimental) ****************************************************************************                     ATTRS FOR IMPORTED CONSTRUCT ***************************************************************************.

        :param guardrail_arn: (experimental) The ARN of the guardrail. At least one of guardrailArn or guardrailId must be defined in order to initialize a guardrail ref.
        :param guardrail_version: (experimental) The version of the guardrail. Default: "DRAFT"
        :param kms_key: (experimental) The KMS key of the guardrail if custom encryption is configured. Default: undefined - Means data is encrypted by default with a AWS-managed key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b140b7ab54824449cb92973af6b36eb6cf61ab0c9257fdf79c5d510e1f60ff)
            check_type(argname="argument guardrail_arn", value=guardrail_arn, expected_type=type_hints["guardrail_arn"])
            check_type(argname="argument guardrail_version", value=guardrail_version, expected_type=type_hints["guardrail_version"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "guardrail_arn": guardrail_arn,
        }
        if guardrail_version is not None:
            self._values["guardrail_version"] = guardrail_version
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        At least one of guardrailArn or guardrailId must be
        defined in order to initialize a guardrail ref.

        :stability: experimental
        '''
        result = self._values.get("guardrail_arn")
        assert result is not None, "Required property 'guardrail_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def guardrail_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the guardrail.

        :default: "DRAFT"

        :stability: experimental
        '''
        result = self._values.get("guardrail_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key of the guardrail if custom encryption is configured.

        :default: undefined - Means data is encrypted by default with a AWS-managed key

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardrailAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "guardrail_id": "guardrailId",
        "guardrail_version": "guardrailVersion",
    },
)
class GuardrailConfiguration:
    def __init__(
        self,
        *,
        guardrail_id: typing.Optional[builtins.str] = None,
        guardrail_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Details about the guardrail associated with the agent.

        :param guardrail_id: 
        :param guardrail_version: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b314d3bddf3fd29e4b1ac5c7c60a1586a89802b85336bbd334b733d34813692)
            check_type(argname="argument guardrail_id", value=guardrail_id, expected_type=type_hints["guardrail_id"])
            check_type(argname="argument guardrail_version", value=guardrail_version, expected_type=type_hints["guardrail_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if guardrail_id is not None:
            self._values["guardrail_id"] = guardrail_id
        if guardrail_version is not None:
            self._values["guardrail_version"] = guardrail_version

    @builtins.property
    def guardrail_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("guardrail_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guardrail_version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("guardrail_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardrailConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "blocked_input_messaging": "blockedInputMessaging",
        "blocked_outputs_messaging": "blockedOutputsMessaging",
        "content_filters": "contentFilters",
        "contextual_grounding_filters": "contextualGroundingFilters",
        "denied_topics": "deniedTopics",
        "description": "description",
        "kms_key": "kmsKey",
        "managed_word_list_filters": "managedWordListFilters",
        "pii_filters": "piiFilters",
        "regex_filters": "regexFilters",
        "word_filters": "wordFilters",
    },
)
class GuardrailProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        blocked_input_messaging: typing.Optional[builtins.str] = None,
        blocked_outputs_messaging: typing.Optional[builtins.str] = None,
        content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        denied_topics: typing.Optional[typing.Sequence["Topic"]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        managed_word_list_filters: typing.Optional[typing.Sequence["ManagedWordFilterType"]] = None,
        pii_filters: typing.Optional[typing.Sequence[typing.Union["PIIFilter", typing.Dict[builtins.str, typing.Any]]]] = None,
        regex_filters: typing.Optional[typing.Sequence[typing.Union["RegexFilter", typing.Dict[builtins.str, typing.Any]]]] = None,
        word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for creating a Guardrail.

        :param name: (experimental) The name of the guardrail.
        :param blocked_input_messaging: (experimental) The message to return when the guardrail blocks a prompt. Default: "Sorry, your query violates our usage policy."
        :param blocked_outputs_messaging: (experimental) The message to return when the guardrail blocks a model response. Default: "Sorry, I am unable to answer your question because of our usage policy."
        :param content_filters: (experimental) The content filters to apply to the guardrail. Note, if one of
        :param contextual_grounding_filters: (experimental) The contextual grounding filters to apply to the guardrail.
        :param denied_topics: (experimental) Up to 30 denied topics to block user inputs or model responses associated with the topic.
        :param description: (experimental) The description of the guardrail.
        :param kms_key: (experimental) A custom KMS key to use for encrypting data. Default: "Your data is encrypted by default with a key that AWS owns and manages for you."
        :param managed_word_list_filters: (experimental) The managed word filters to apply to the guardrail.
        :param pii_filters: (experimental) The PII filters to apply to the guardrail.
        :param regex_filters: (experimental) The regular expression (regex) filters to apply to the guardrail.
        :param word_filters: (experimental) The word filters to apply to the guardrail.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9d19859a6750c938be49617894f02e36de79c2e5a05a9cb6d6eac91e68d0ea)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument blocked_input_messaging", value=blocked_input_messaging, expected_type=type_hints["blocked_input_messaging"])
            check_type(argname="argument blocked_outputs_messaging", value=blocked_outputs_messaging, expected_type=type_hints["blocked_outputs_messaging"])
            check_type(argname="argument content_filters", value=content_filters, expected_type=type_hints["content_filters"])
            check_type(argname="argument contextual_grounding_filters", value=contextual_grounding_filters, expected_type=type_hints["contextual_grounding_filters"])
            check_type(argname="argument denied_topics", value=denied_topics, expected_type=type_hints["denied_topics"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument managed_word_list_filters", value=managed_word_list_filters, expected_type=type_hints["managed_word_list_filters"])
            check_type(argname="argument pii_filters", value=pii_filters, expected_type=type_hints["pii_filters"])
            check_type(argname="argument regex_filters", value=regex_filters, expected_type=type_hints["regex_filters"])
            check_type(argname="argument word_filters", value=word_filters, expected_type=type_hints["word_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if blocked_input_messaging is not None:
            self._values["blocked_input_messaging"] = blocked_input_messaging
        if blocked_outputs_messaging is not None:
            self._values["blocked_outputs_messaging"] = blocked_outputs_messaging
        if content_filters is not None:
            self._values["content_filters"] = content_filters
        if contextual_grounding_filters is not None:
            self._values["contextual_grounding_filters"] = contextual_grounding_filters
        if denied_topics is not None:
            self._values["denied_topics"] = denied_topics
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if managed_word_list_filters is not None:
            self._values["managed_word_list_filters"] = managed_word_list_filters
        if pii_filters is not None:
            self._values["pii_filters"] = pii_filters
        if regex_filters is not None:
            self._values["regex_filters"] = regex_filters
        if word_filters is not None:
            self._values["word_filters"] = word_filters

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the guardrail.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blocked_input_messaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) The message to return when the guardrail blocks a prompt.

        :default: "Sorry, your query violates our usage policy."

        :stability: experimental
        '''
        result = self._values.get("blocked_input_messaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blocked_outputs_messaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) The message to return when the guardrail blocks a model response.

        :default: "Sorry, I am unable to answer your question because of our usage policy."

        :stability: experimental
        '''
        result = self._values.get("blocked_outputs_messaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_filters(self) -> typing.Optional[typing.List[ContentFilter]]:
        '''(experimental) The content filters to apply to the guardrail.

        Note, if one of

        :stability: experimental
        '''
        result = self._values.get("content_filters")
        return typing.cast(typing.Optional[typing.List[ContentFilter]], result)

    @builtins.property
    def contextual_grounding_filters(
        self,
    ) -> typing.Optional[typing.List[ContextualGroundingFilter]]:
        '''(experimental) The contextual grounding filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("contextual_grounding_filters")
        return typing.cast(typing.Optional[typing.List[ContextualGroundingFilter]], result)

    @builtins.property
    def denied_topics(self) -> typing.Optional[typing.List["Topic"]]:
        '''(experimental) Up to 30 denied topics to block user inputs or model responses associated with the topic.

        :stability: experimental
        '''
        result = self._values.get("denied_topics")
        return typing.cast(typing.Optional[typing.List["Topic"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the guardrail.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) A custom KMS key to use for encrypting data.

        :default: "Your data is encrypted by default with a key that AWS owns and manages for you."

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def managed_word_list_filters(
        self,
    ) -> typing.Optional[typing.List["ManagedWordFilterType"]]:
        '''(experimental) The managed word filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("managed_word_list_filters")
        return typing.cast(typing.Optional[typing.List["ManagedWordFilterType"]], result)

    @builtins.property
    def pii_filters(self) -> typing.Optional[typing.List["PIIFilter"]]:
        '''(experimental) The PII filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("pii_filters")
        return typing.cast(typing.Optional[typing.List["PIIFilter"]], result)

    @builtins.property
    def regex_filters(self) -> typing.Optional[typing.List["RegexFilter"]]:
        '''(experimental) The regular expression (regex) filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("regex_filters")
        return typing.cast(typing.Optional[typing.List["RegexFilter"]], result)

    @builtins.property
    def word_filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The word filters to apply to the guardrail.

        :stability: experimental
        '''
        result = self._values.get("word_filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardrailProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.HierarchicalChunkingProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_child_token_size": "maxChildTokenSize",
        "max_parent_token_size": "maxParentTokenSize",
        "overlap_tokens": "overlapTokens",
    },
)
class HierarchicalChunkingProps:
    def __init__(
        self,
        *,
        max_child_token_size: jsii.Number,
        max_parent_token_size: jsii.Number,
        overlap_tokens: jsii.Number,
    ) -> None:
        '''
        :param max_child_token_size: (experimental) Maximum number of tokens that a child chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param max_parent_token_size: (experimental) Maximum number of tokens that a parent chunk can contain. Keep in mind the maximum chunk size depends on the embedding model chosen.
        :param overlap_tokens: (experimental) The overlap tokens between adjacent chunks.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832a5183cc17b41fd7587d09a661c1bc3796489cafca2ed06677f49aa94a717d)
            check_type(argname="argument max_child_token_size", value=max_child_token_size, expected_type=type_hints["max_child_token_size"])
            check_type(argname="argument max_parent_token_size", value=max_parent_token_size, expected_type=type_hints["max_parent_token_size"])
            check_type(argname="argument overlap_tokens", value=overlap_tokens, expected_type=type_hints["overlap_tokens"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_child_token_size": max_child_token_size,
            "max_parent_token_size": max_parent_token_size,
            "overlap_tokens": overlap_tokens,
        }

    @builtins.property
    def max_child_token_size(self) -> jsii.Number:
        '''(experimental) Maximum number of tokens that a child chunk can contain.

        Keep in mind the maximum chunk size depends on the embedding model chosen.

        :stability: experimental
        '''
        result = self._values.get("max_child_token_size")
        assert result is not None, "Required property 'max_child_token_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_parent_token_size(self) -> jsii.Number:
        '''(experimental) Maximum number of tokens that a parent chunk can contain.

        Keep in mind the maximum chunk size depends on the embedding model chosen.

        :stability: experimental
        '''
        result = self._values.get("max_parent_token_size")
        assert result is not None, "Required property 'max_parent_token_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def overlap_tokens(self) -> jsii.Number:
        '''(experimental) The overlap tokens between adjacent chunks.

        :stability: experimental
        '''
        result = self._values.get("overlap_tokens")
        assert result is not None, "Required property 'overlap_tokens' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HierarchicalChunkingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IAgentAlias")
class IAgentAlias(typing_extensions.Protocol):
    '''(experimental) Interface for both Imported and CDK-created Agent Aliases.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent.

        :stability: experimental

        Example::

            `DNCJJYQKSU`
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental

        Example::

            `arn:aws:bedrock:us-east-1:123456789012:agent-alias/DNCJJYQKSU/TCLCITFZTN`
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental

        Example::

            `TCLCITFZTN`
        '''
        ...


class _IAgentAliasProxy:
    '''(experimental) Interface for both Imported and CDK-created Agent Aliases.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IAgentAlias"

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent.

        :stability: experimental

        Example::

            `DNCJJYQKSU`
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental

        Example::

            `arn:aws:bedrock:us-east-1:123456789012:agent-alias/DNCJJYQKSU/TCLCITFZTN`
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental

        Example::

            `TCLCITFZTN`
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAgentAlias).__jsii_proxy_class__ = lambda : _IAgentAliasProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IDataSource")
class IDataSource(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Specifies interface for resources created with CDK or imported into CDK.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        ...


class _IDataSourceProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Specifies interface for resources created with CDK or imported into CDK.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IDataSource"

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDataSource).__jsii_proxy_class__ = lambda : _IDataSourceProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IGuardrail")
class IGuardrail(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a Guardrail, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:guardrail/yympzo398ipq"@attributeundefined
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental

        Example::

            "yympzo398ipq"@attributeundefined
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this guardrail.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The version of the guardrail.

        If no explicit version is created,
        this will default to "DRAFT"

        :stability: experimental
        '''
        ...

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        ...

    @jsii.member(jsii_name="grantApply")
    def grant_apply(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to apply the guardrail.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IGuardrailProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a Guardrail, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IGuardrail"

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:guardrail/yympzo398ipq"@attributeundefined
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailArn"))

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental

        Example::

            "yympzo398ipq"@attributeundefined
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The version of the guardrail.

        If no explicit version is created,
        this will default to "DRAFT"

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailVersion"))

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa86b82cfa7566549e30a1d5b954f23d8c26046bfa7cc0af976bc3c76faa6d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailVersion", value) # pyright: ignore[reportArgumentType]

    @jsii.member(jsii_name="grantApply")
    def grant_apply(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to apply the guardrail.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ba62eccfee612703b786064d7f93d108f9f738d3af81886e81a1528ede7a98)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantApply", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGuardrail).__jsii_proxy_class__ = lambda : _IGuardrailProxy


@jsii.interface(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IInferenceProfile"
)
class IInferenceProfile(typing_extensions.Protocol):
    '''(experimental) Represents a ApplicationInferenceProfile, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "InferenceProfileType":
        '''(experimental) The type of inference profile.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the inference profile.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IInferenceProfileProxy:
    '''(experimental) Represents a ApplicationInferenceProfile, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IInferenceProfile"

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "InferenceProfileType":
        '''(experimental) The type of inference profile.

        :stability: experimental
        '''
        return typing.cast("InferenceProfileType", jsii.get(self, "type"))

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the inference profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e05b919b09e86b619e07b4ef364b84ec6c2406d5ea1bca6a3cc89fa68153ec7)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInferenceProfile).__jsii_proxy_class__ = lambda : _IInferenceProfileProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IInvokable")
class IInvokable(typing_extensions.Protocol):
    '''(experimental) Represents an Amazon Bedrock abstraction on which you can run the ``Invoke`` API.

    This can be a Foundational Model,
    a Custom Model, or an Inference Profile.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Bedrock invokable abstraction.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the invokable abstraction.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IInvokableProxy:
    '''(experimental) Represents an Amazon Bedrock abstraction on which you can run the ``Invoke`` API.

    This can be a Foundational Model,
    a Custom Model, or an Inference Profile.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IInvokable"

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Bedrock invokable abstraction.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the invokable abstraction.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29403dd1f5d63fdfa42529ed12671747a327e8f838334b096c8d604ee0871773)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInvokable).__jsii_proxy_class__ = lambda : _IInvokableProxy


@jsii.interface(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IKnowledgeBase"
)
class IKnowledgeBase(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a Knowledge Base, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/KB12345678"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addConfluenceDataSource")
    def add_confluence_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "ConfluenceDataSource":
        '''(experimental) Add a Confluence data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addS3DataSource")
    def add_s3_data_source(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "S3DataSource":
        '''(experimental) Add an S3 data source to the knowledge base.

        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSalesforceDataSource")
    def add_salesforce_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SalesforceCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SalesforceDataSource":
        '''(experimental) Add a Salesforce data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSharePointDataSource")
    def add_share_point_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SharePointCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SharePointDataSource":
        '''(experimental) Add a SharePoint data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addWebCrawlerDataSource")
    def add_web_crawler_data_source(
        self,
        *,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "WebCrawlerDataSource":
        '''(experimental) Add a web crawler data source to the knowledge base.

        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        ...


class _IKnowledgeBaseProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a Knowledge Base, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IKnowledgeBase"

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/KB12345678"
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role associated with the knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @jsii.member(jsii_name="addConfluenceDataSource")
    def add_confluence_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "ConfluenceDataSource":
        '''(experimental) Add a Confluence data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = ConfluenceDataSourceAssociationProps(
            auth_secret=auth_secret,
            confluence_url=confluence_url,
            auth_type=auth_type,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("ConfluenceDataSource", jsii.invoke(self, "addConfluenceDataSource", [props]))

    @jsii.member(jsii_name="addS3DataSource")
    def add_s3_data_source(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "S3DataSource":
        '''(experimental) Add an S3 data source to the knowledge base.

        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = S3DataSourceAssociationProps(
            bucket=bucket,
            inclusion_prefixes=inclusion_prefixes,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("S3DataSource", jsii.invoke(self, "addS3DataSource", [props]))

    @jsii.member(jsii_name="addSalesforceDataSource")
    def add_salesforce_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SalesforceCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SalesforceDataSource":
        '''(experimental) Add a Salesforce data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SalesforceDataSourceAssociationProps(
            auth_secret=auth_secret,
            endpoint=endpoint,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SalesforceDataSource", jsii.invoke(self, "addSalesforceDataSource", [props]))

    @jsii.member(jsii_name="addSharePointDataSource")
    def add_share_point_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SharePointCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SharePointDataSource":
        '''(experimental) Add a SharePoint data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SharePointDataSourceAssociationProps(
            auth_secret=auth_secret,
            domain=domain,
            site_urls=site_urls,
            tenant_id=tenant_id,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SharePointDataSource", jsii.invoke(self, "addSharePointDataSource", [props]))

    @jsii.member(jsii_name="addWebCrawlerDataSource")
    def add_web_crawler_data_source(
        self,
        *,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "WebCrawlerDataSource":
        '''(experimental) Add a web crawler data source to the knowledge base.

        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = WebCrawlerDataSourceAssociationProps(
            source_urls=source_urls,
            crawling_rate=crawling_rate,
            crawling_scope=crawling_scope,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("WebCrawlerDataSource", jsii.invoke(self, "addWebCrawlerDataSource", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IKnowledgeBase).__jsii_proxy_class__ = lambda : _IKnowledgeBaseProxy


@jsii.interface(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.IPrompt")
class IPrompt(typing_extensions.Protocol):
    '''(experimental) Represents a Prompt, either created with CDK or imported.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental

        Example::

            "PROMPT12345"
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :default: - "DRAFT"

        :stability: experimental
        '''
        ...

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        ...


class _IPromptProxy:
    '''(experimental) Represents a Prompt, either created with CDK or imported.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdklabs/generative-ai-cdk-constructs.bedrock.IPrompt"

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptArn"))

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental

        Example::

            "PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :default: - "DRAFT"

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptVersion"))

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5960928d16109614db9d88a976b6813f338475a6d9bd76b0987c904ec8128c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptVersion", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPrompt).__jsii_proxy_class__ = lambda : _IPromptProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InferenceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_length": "maximumLength",
        "stop_sequences": "stopSequences",
        "temperature": "temperature",
        "top_k": "topK",
        "top_p": "topP",
    },
)
class InferenceConfiguration:
    def __init__(
        self,
        *,
        maximum_length: jsii.Number,
        stop_sequences: typing.Sequence[builtins.str],
        temperature: jsii.Number,
        top_k: jsii.Number,
        top_p: jsii.Number,
    ) -> None:
        '''(experimental) LLM inference configuration.

        :param maximum_length: (experimental) The maximum number of tokens to generate in the response. Integer min 0 max 4096
        :param stop_sequences: (experimental) A list of stop sequences. A stop sequence is a sequence of characters that causes the model to stop generating the response. length 0-4
        :param temperature: (experimental) The likelihood of the model selecting higher-probability options while generating a response. A lower value makes the model more likely to choose higher-probability options, while a higher value makes the model more likely to choose lower-probability options. Floating point min 0 max 1
        :param top_k: (experimental) While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for topK is the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set topK to 50, the model selects the next token from among the top 50 most likely choices. Integer min 0 max 500
        :param top_p: (experimental) While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for Top P determines the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set topP to 80, the model only selects the next token from the top 80% of the probability distribution of next tokens. Floating point min 0 max 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befd502c2937a36c672491bd2695d4ec887944e821efe023f2dc44cff4137750)
            check_type(argname="argument maximum_length", value=maximum_length, expected_type=type_hints["maximum_length"])
            check_type(argname="argument stop_sequences", value=stop_sequences, expected_type=type_hints["stop_sequences"])
            check_type(argname="argument temperature", value=temperature, expected_type=type_hints["temperature"])
            check_type(argname="argument top_k", value=top_k, expected_type=type_hints["top_k"])
            check_type(argname="argument top_p", value=top_p, expected_type=type_hints["top_p"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_length": maximum_length,
            "stop_sequences": stop_sequences,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        }

    @builtins.property
    def maximum_length(self) -> jsii.Number:
        '''(experimental) The maximum number of tokens to generate in the response.

        Integer

        min 0
        max 4096

        :stability: experimental
        '''
        result = self._values.get("maximum_length")
        assert result is not None, "Required property 'maximum_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stop_sequences(self) -> typing.List[builtins.str]:
        '''(experimental) A list of stop sequences.

        A stop sequence is a sequence of characters that
        causes the model to stop generating the response.

        length 0-4

        :stability: experimental
        '''
        result = self._values.get("stop_sequences")
        assert result is not None, "Required property 'stop_sequences' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def temperature(self) -> jsii.Number:
        '''(experimental) The likelihood of the model selecting higher-probability options while generating a response.

        A lower value makes the model more likely to choose
        higher-probability options, while a higher value makes the model more
        likely to choose lower-probability options.

        Floating point

        min 0
        max 1

        :stability: experimental
        '''
        result = self._values.get("temperature")
        assert result is not None, "Required property 'temperature' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def top_k(self) -> jsii.Number:
        '''(experimental) While generating a response, the model determines the probability of the following token at each point of generation.

        The value that you set for
        topK is the number of most-likely candidates from which the model chooses
        the next token in the sequence. For example, if you set topK to 50, the
        model selects the next token from among the top 50 most likely choices.

        Integer

        min 0
        max 500

        :stability: experimental
        '''
        result = self._values.get("top_k")
        assert result is not None, "Required property 'top_k' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def top_p(self) -> jsii.Number:
        '''(experimental) While generating a response, the model determines the probability of the following token at each point of generation.

        The value that you set for
        Top P determines the number of most-likely candidates from which the model
        chooses the next token in the sequence. For example, if you set topP to
        80, the model only selects the next token from the top 80% of the
        probability distribution of next tokens.

        Floating point

        min 0
        max 1

        :stability: experimental
        '''
        result = self._values.get("top_p")
        assert result is not None, "Required property 'top_p' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InferenceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInferenceProfile, _aws_cdk_ceddda9d.IResource)
class InferenceProfileBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InferenceProfileBase",
):
    '''(experimental) Abstract base class for a ApplicationInferenceProfile.

    Contains methods and attributes valid for ApplicationInferenceProfiles either created with CDK or imported.

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
            type_hints = typing.get_type_hints(_typecheckingstub__e47a0e32efc3020834d43d9c5523a26c5aa4f43e016164f6b0291a29938455be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the cross-region inference profile.

        Does not grant permissions to use the model in the profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e018efd836bd4c5f724810d840738657b70936f17c80063e2affbcd56a59c5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    @abc.abstractmethod
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    @abc.abstractmethod
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> "InferenceProfileType":
        '''(experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        ...


class _InferenceProfileBaseProxy(
    InferenceProfileBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "InferenceProfileType":
        '''(experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        return typing.cast("InferenceProfileType", jsii.get(self, "type"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InferenceProfileBase).__jsii_proxy_class__ = lambda : _InferenceProfileBaseProxy


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InferenceProfileType"
)
class InferenceProfileType(enum.Enum):
    '''(experimental) These are the values used by the API when using aws bedrock get-inference-profile --inference-profile-identifier XXXXXXX.

    :stability: experimental
    '''

    SYSTEM_DEFINED = "SYSTEM_DEFINED"
    '''(experimental) An inference profile that is created by AWS.

    These are profiles such as cross-region
    which help you distributed traffic across a geographic region.

    :stability: experimental
    '''
    APPLICATION = "APPLICATION"
    '''(experimental) An inference profile that is user-created.

    These are profiles that help
    you track costs or metrics.

    :stability: experimental
    '''


class InlineApiSchema(
    ApiSchema,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InlineApiSchema",
):
    '''(experimental) API Schema from a string value.

    :stability: experimental
    '''

    def __init__(self, schema: builtins.str) -> None:
        '''
        :param schema: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeb00812cdcb551f5f688ee295d8f225db974111b8872709130c22fef51592f)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        jsii.create(self.__class__, self, [schema])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> ApiSchemaConfig:
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429693913d097a23421c6ed72f2363c20d20bbc2d34b374921e37cf4ac8d4157)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ApiSchemaConfig, jsii.invoke(self, "bind", [_scope]))


@jsii.implements(IKnowledgeBase)
class KnowledgeBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KnowledgeBase",
):
    '''(experimental) Deploys a Bedrock Knowledge Base and configures a backend by OpenSearch Serverless, Pinecone, Redis Enterprise Cloud or Amazon Aurora PostgreSQL.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        embeddings_model: "BedrockFoundationModel",
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        index_name: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vector_field: typing.Optional[builtins.str] = None,
        vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
        vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param embeddings_model: (experimental) The embeddings model for the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with a policy statement granting permission to invoke the specific embeddings model. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param index_name: (experimental) The name of the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-index'
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.
        :param name: (experimental) The name of the knowledge base.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false
        :param vector_field: (experimental) The name of the field in the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-vector'
        :param vector_index: (experimental) The vector index for the OpenSearch Serverless backed knowledge base. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - A new vector index is created on the Vector Collection if vector store is of ``VectorCollection`` type.
        :param vector_store: (experimental) The vector store for the knowledge base. Must be either of type ``VectorCollection``, ``RedisEnterpriseVectorStore``, ``PineconeVectorStore`` or ``AmazonAuroraVectorStore``. Default: - A new OpenSearch Serverless vector collection is created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a416de40b883dde9bcfa680e69b09d8d8005e4e5d67e2254f09ebebb1b516bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = KnowledgeBaseProps(
            embeddings_model=embeddings_model,
            description=description,
            existing_role=existing_role,
            index_name=index_name,
            instruction=instruction,
            knowledge_base_state=knowledge_base_state,
            name=name,
            tags=tags,
            vector_field=vector_field,
            vector_index=vector_index,
            vector_store=vector_store,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromKnowledgeBaseAttributes")
    @builtins.classmethod
    def from_knowledge_base_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        execution_role_arn: builtins.str,
        knowledge_base_id: builtins.str,
    ) -> IKnowledgeBase:
        '''
        :param scope: -
        :param id: -
        :param execution_role_arn: (experimental) The Service Execution Role associated with the knowledge base.
        :param knowledge_base_id: (experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a654bef0899e37e420b95286d5ec50496932a793679c6d7ba80f00f62f49140)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = KnowledgeBaseAttributes(
            execution_role_arn=execution_role_arn, knowledge_base_id=knowledge_base_id
        )

        return typing.cast(IKnowledgeBase, jsii.sinvoke(cls, "fromKnowledgeBaseAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addConfluenceDataSource")
    def add_confluence_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "ConfluenceDataSource":
        '''(experimental) Add a Confluence data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = ConfluenceDataSourceAssociationProps(
            auth_secret=auth_secret,
            confluence_url=confluence_url,
            auth_type=auth_type,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("ConfluenceDataSource", jsii.invoke(self, "addConfluenceDataSource", [props]))

    @jsii.member(jsii_name="addS3DataSource")
    def add_s3_data_source(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "S3DataSource":
        '''(experimental) Add an S3 data source to the knowledge base.

        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = S3DataSourceAssociationProps(
            bucket=bucket,
            inclusion_prefixes=inclusion_prefixes,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("S3DataSource", jsii.invoke(self, "addS3DataSource", [props]))

    @jsii.member(jsii_name="addSalesforceDataSource")
    def add_salesforce_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SalesforceCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SalesforceDataSource":
        '''(experimental) Add a Salesforce data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SalesforceDataSourceAssociationProps(
            auth_secret=auth_secret,
            endpoint=endpoint,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SalesforceDataSource", jsii.invoke(self, "addSalesforceDataSource", [props]))

    @jsii.member(jsii_name="addSharePointDataSource")
    def add_share_point_data_source(
        self,
        *,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union["SharePointCrawlingFilters", typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "SharePointDataSource":
        '''(experimental) Add a SharePoint data source to the knowledge base.

        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = SharePointDataSourceAssociationProps(
            auth_secret=auth_secret,
            domain=domain,
            site_urls=site_urls,
            tenant_id=tenant_id,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("SharePointDataSource", jsii.invoke(self, "addSharePointDataSource", [props]))

    @jsii.member(jsii_name="addWebCrawlerDataSource")
    def add_web_crawler_data_source(
        self,
        *,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional["ParsingStategy"] = None,
    ) -> "WebCrawlerDataSource":
        '''(experimental) Add a web crawler data source to the knowledge base.

        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = WebCrawlerDataSourceAssociationProps(
            source_urls=source_urls,
            crawling_rate=crawling_rate,
            crawling_scope=crawling_scope,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast("WebCrawlerDataSource", jsii.invoke(self, "addWebCrawlerDataSource", [props]))

    @jsii.member(jsii_name="associateToAgent")
    def associate_to_agent(self, agent: Agent) -> None:
        '''(experimental) Associate knowledge base with an agent.

        :param agent: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca7cf4ff7c6392dfc7cae12d95e046e86c711e76659c1c94e920f30da3a066c)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        return typing.cast(None, jsii.invoke(self, "associateToAgent", [agent]))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''(experimental) The description knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseInstance")
    def knowledge_base_instance(self) -> _aws_cdk_aws_bedrock_ceddda9d.CfnKnowledgeBase:
        '''(experimental) Instance of knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnKnowledgeBase, jsii.get(self, "knowledgeBaseInstance"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseState")
    def knowledge_base_state(self) -> builtins.str:
        '''(experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseState"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role the Knowledge Base uses to access the vector store and data source.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="vectorStore")
    def vector_store(
        self,
    ) -> typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]:
        '''(experimental) The vector store for the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196], jsii.get(self, "vectorStore"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KnowledgeBaseAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role_arn": "executionRoleArn",
        "knowledge_base_id": "knowledgeBaseId",
    },
)
class KnowledgeBaseAttributes:
    def __init__(
        self,
        *,
        execution_role_arn: builtins.str,
        knowledge_base_id: builtins.str,
    ) -> None:
        '''(experimental) Properties for importing a knowledge base outside of this stack.

        :param execution_role_arn: (experimental) The Service Execution Role associated with the knowledge base.
        :param knowledge_base_id: (experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54154af2e4de900e9c2f362f003646235da0359709893f7760cdc5484b06d24)
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
            "knowledge_base_id": knowledge_base_id,
        }

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''(experimental) The Service Execution Role associated with the knowledge base.

        :stability: experimental

        Example::

            "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForKnowledgeBaseawscdkbdgeBaseKB12345678"
        '''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental

        Example::

            "KB12345678"
        '''
        result = self._values.get("knowledge_base_id")
        assert result is not None, "Required property 'knowledge_base_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KnowledgeBaseAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KnowledgeBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "embeddings_model": "embeddingsModel",
        "description": "description",
        "existing_role": "existingRole",
        "index_name": "indexName",
        "instruction": "instruction",
        "knowledge_base_state": "knowledgeBaseState",
        "name": "name",
        "tags": "tags",
        "vector_field": "vectorField",
        "vector_index": "vectorIndex",
        "vector_store": "vectorStore",
    },
)
class KnowledgeBaseProps:
    def __init__(
        self,
        *,
        embeddings_model: "BedrockFoundationModel",
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        index_name: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vector_field: typing.Optional[builtins.str] = None,
        vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
        vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
    ) -> None:
        '''(experimental) Properties for a knowledge base.

        :param embeddings_model: (experimental) The embeddings model for the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with a policy statement granting permission to invoke the specific embeddings model. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param index_name: (experimental) The name of the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-index'
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.
        :param name: (experimental) The name of the knowledge base.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false
        :param vector_field: (experimental) The name of the field in the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-vector'
        :param vector_index: (experimental) The vector index for the OpenSearch Serverless backed knowledge base. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - A new vector index is created on the Vector Collection if vector store is of ``VectorCollection`` type.
        :param vector_store: (experimental) The vector store for the knowledge base. Must be either of type ``VectorCollection``, ``RedisEnterpriseVectorStore``, ``PineconeVectorStore`` or ``AmazonAuroraVectorStore``. Default: - A new OpenSearch Serverless vector collection is created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77925ffb8d3d9f229cccdf4b13498db4e9b0c20ca077db0cbe11892e0b36d5f)
            check_type(argname="argument embeddings_model", value=embeddings_model, expected_type=type_hints["embeddings_model"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument knowledge_base_state", value=knowledge_base_state, expected_type=type_hints["knowledge_base_state"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vector_field", value=vector_field, expected_type=type_hints["vector_field"])
            check_type(argname="argument vector_index", value=vector_index, expected_type=type_hints["vector_index"])
            check_type(argname="argument vector_store", value=vector_store, expected_type=type_hints["vector_store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "embeddings_model": embeddings_model,
        }
        if description is not None:
            self._values["description"] = description
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if index_name is not None:
            self._values["index_name"] = index_name
        if instruction is not None:
            self._values["instruction"] = instruction
        if knowledge_base_state is not None:
            self._values["knowledge_base_state"] = knowledge_base_state
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if vector_field is not None:
            self._values["vector_field"] = vector_field
        if vector_index is not None:
            self._values["vector_index"] = vector_index
        if vector_store is not None:
            self._values["vector_store"] = vector_store

    @builtins.property
    def embeddings_model(self) -> "BedrockFoundationModel":
        '''(experimental) The embeddings model for the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("embeddings_model")
        assert result is not None, "Required property 'embeddings_model' is missing"
        return typing.cast("BedrockFoundationModel", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) Existing IAM role with a policy statement granting permission to invoke the specific embeddings model.

        Any entity (e.g., an AWS service or application) that assumes
        this role will be able to invoke or use the
        specified embeddings model within the Bedrock service.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def index_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the vector index.

        If vectorStore is not of type ``VectorCollection``,
        do not include this property as it will throw error.

        :default: - 'bedrock-knowledge-base-default-index'

        :stability: experimental
        '''
        result = self._values.get("index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative description of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_base_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vector_field(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the field in the vector index.

        If vectorStore is not of type ``VectorCollection``,
        do not include this property as it will throw error.

        :default: - 'bedrock-knowledge-base-default-vector'

        :stability: experimental
        '''
        result = self._values.get("vector_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vector_index(self) -> typing.Optional[_VectorIndex_e5d266e9]:
        '''(experimental) The vector index for the OpenSearch Serverless backed knowledge base.

        If vectorStore is not of type ``VectorCollection``, do not include
        this property as it will throw error.

        :default:

        - A new vector index is created on the Vector Collection
        if vector store is of ``VectorCollection`` type.

        :stability: experimental
        '''
        result = self._values.get("vector_index")
        return typing.cast(typing.Optional[_VectorIndex_e5d266e9], result)

    @builtins.property
    def vector_store(
        self,
    ) -> typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]]:
        '''(experimental) The vector store for the knowledge base.

        Must be either of
        type ``VectorCollection``, ``RedisEnterpriseVectorStore``,
        ``PineconeVectorStore`` or ``AmazonAuroraVectorStore``.

        :default: - A new OpenSearch Serverless vector collection is created.

        :stability: experimental
        '''
        result = self._values.get("vector_store")
        return typing.cast(typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.LambdaCustomTransformationProps",
    jsii_struct_bases=[],
    name_mapping={"lambda_function": "lambdaFunction", "s3_bucket_uri": "s3BucketUri"},
)
class LambdaCustomTransformationProps:
    def __init__(
        self,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        s3_bucket_uri: builtins.str,
    ) -> None:
        '''(experimental) Properties for configuring a Lambda-based custom transformation.

        :param lambda_function: (experimental) The Lambda function to use for custom document processing.
        :param s3_bucket_uri: (experimental) An S3 bucket URL/path to store input documents for Lambda processing and to store the output of the processed documents.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762879178fd972fbfc85b23a5a96fe26104fbaf3791957f75d2f92316a91cc7a)
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
            check_type(argname="argument s3_bucket_uri", value=s3_bucket_uri, expected_type=type_hints["s3_bucket_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_function": lambda_function,
            "s3_bucket_uri": s3_bucket_uri,
        }

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''(experimental) The Lambda function to use for custom document processing.

        :stability: experimental
        '''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def s3_bucket_uri(self) -> builtins.str:
        '''(experimental) An S3 bucket URL/path to store input documents for Lambda processing and to store the output of the processed documents.

        :stability: experimental

        Example::

            "s3://my-bucket/chunk-processor/"
        '''
        result = self._values.get("s3_bucket_uri")
        assert result is not None, "Required property 's3_bucket_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaCustomTransformationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ManagedWordFilterType"
)
class ManagedWordFilterType(enum.Enum):
    '''(experimental) The managed word type filter available for guardrails.

    :stability: experimental
    '''

    PROFANITY = "PROFANITY"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PIIFilter",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "type": "type"},
)
class PIIFilter:
    def __init__(
        self,
        *,
        action: GuardrailAction,
        type: typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648],
    ) -> None:
        '''(experimental) Interface to define a PII Filter.

        :param action: (experimental) The action to take when PII is detected.
        :param type: (experimental) The type of PII to filter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68aa36b0ead1124a53b5c01582eeed48828bdcc66f87d80565fddd7cc232b72e)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "type": type,
        }

    @builtins.property
    def action(self) -> GuardrailAction:
        '''(experimental) The action to take when PII is detected.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(GuardrailAction, result)

    @builtins.property
    def type(
        self,
    ) -> typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648]:
        '''(experimental) The type of PII to filter.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PIIFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ParserMode")
class ParserMode(enum.Enum):
    '''(experimental) Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the promptType.

    If you set the field as OVERRIDEN, the
    overrideLambda field in the PromptOverrideConfiguration must be specified
    with the ARN of a Lambda function.

    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''
    :stability: experimental
    '''
    OVERRIDDEN = "OVERRIDDEN"
    '''
    :stability: experimental
    '''


class ParsingStategy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ParsingStategy",
):
    '''(experimental) Represents an advanced parsing strategy configuration for Knowledge Base ingestion.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html#kb-advanced-parsing
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="foundationModel")
    @builtins.classmethod
    def foundation_model(
        cls,
        *,
        parsing_model: IInvokable,
        parsing_prompt: typing.Optional[builtins.str] = None,
    ) -> "ParsingStategy":
        '''(experimental) Creates a Foundation Model-based parsing strategy for extracting non-textual information from documents such as tables and charts.

        - Additional costs apply when using advanced parsing due to foundation model usage.
        - There are limits on file types (PDF) and total data that can be parsed using advanced parsing.

        :param parsing_model: (experimental) The Foundation Model to use for parsing non-textual information. Currently supported models are Claude 3 Sonnet and Claude 3 Haiku.
        :param parsing_prompt: (experimental) Custom prompt to instruct the parser on how to interpret the document. Default: - Uses the default instruction prompt as provided in the AWS Console.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html#kb-ds-supported-doc-formats-limits
        :stability: experimental
        '''
        props = FoundationModelParsingStategyProps(
            parsing_model=parsing_model, parsing_prompt=parsing_prompt
        )

        return typing.cast("ParsingStategy", jsii.sinvoke(cls, "foundationModel", [props]))

    @jsii.member(jsii_name="generatePolicyStatements")
    @abc.abstractmethod
    def generate_policy_statements(
        self,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="configuration")
    @abc.abstractmethod
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        ...

    @configuration.setter
    @abc.abstractmethod
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty,
    ) -> None:
        ...


class _ParsingStategyProxy(ParsingStategy):
    @jsii.member(jsii_name="generatePolicyStatements")
    def generate_policy_statements(
        self,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement], jsii.invoke(self, "generatePolicyStatements", []))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty:
        '''(experimental) The CloudFormation property representation of this configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20f93031aefe7465a4c9b7b8cbf589b874a8c6abd25dd259847d7c99f2c292b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ParsingStategy).__jsii_proxy_class__ = lambda : _ParsingStategyProxy


@jsii.implements(IPrompt)
class Prompt(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Prompt",
):
    '''(experimental) Prompts are a specific set of inputs that guide FMs on Amazon Bedrock to generate an appropriate response or output for a given task or instruction.

    You can optimize the prompt for specific use cases and models.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html
    :stability: experimental
    :resource: AWS::Bedrock::Prompt
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prompt_name: builtins.str,
        default_variant: typing.Optional["PromptVariant"] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        variants: typing.Optional[typing.Sequence["PromptVariant"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param prompt_name: (experimental) The name of the prompt.
        :param default_variant: (experimental) The Prompt Variant that will be used by default. Default: - No default variant provided.
        :param description: (experimental) A description of what the prompt does. Default: - No description provided.
        :param kms_key: (experimental) The KMS key that the prompt is encrypted with. Default: - AWS owned and managed key.
        :param variants: (experimental) The variants of your prompt. Variants can use different messages, models, or configurations so that you can compare their outputs to decide the best variant for your use case. Maximum of 3 variants.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28412a5d8ac170fe3a64e61ef6ae3f19e2ab4831e4f173b4d9dd49819888b236)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PromptProps(
            prompt_name=prompt_name,
            default_variant=default_variant,
            description=description,
            kms_key=kms_key,
            variants=variants,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPromptAttributes")
    @builtins.classmethod
    def from_prompt_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prompt_arn: builtins.str,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        prompt_version: typing.Optional[builtins.str] = None,
    ) -> IPrompt:
        '''
        :param scope: -
        :param id: -
        :param prompt_arn: (experimental) The ARN of the prompt.
        :param kms_key: (experimental) Optional KMS encryption key associated with this prompt.
        :param prompt_version: (experimental) The version of the prompt. Default: - "DRAFT"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493e34f209102ea802c9e52bb8d42086b43ec2f571efc98a8d11938b5c35926c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = PromptAttributes(
            prompt_arn=prompt_arn, kms_key=kms_key, prompt_version=prompt_version
        )

        return typing.cast(IPrompt, jsii.sinvoke(cls, "fromPromptAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addVariant")
    def add_variant(self, variant: "PromptVariant") -> None:
        '''(experimental) Adds a prompt variant.

        :param variant: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfa6edec3745b41e32e786ccd9bf47e56b752a48a1204aefa620f6425599454)
            check_type(argname="argument variant", value=variant, expected_type=type_hints["variant"])
        return typing.cast(None, jsii.invoke(self, "addVariant", [variant]))

    @jsii.member(jsii_name="createVersion")
    def create_version(
        self,
        description: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Creates a prompt version, a static snapshot of your prompt that can be deployed to production.

        :param description: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc07b4411e1c17474873d667b41d3c8be2fd1ca6adf765c3090c15136423d774)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(builtins.str, jsii.invoke(self, "createVersion", [description]))

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptArn"))

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental

        Example::

            "PROMPT12345"
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptId"))

    @builtins.property
    @jsii.member(jsii_name="promptName")
    def prompt_name(self) -> builtins.str:
        '''(experimental) The name of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptName"))

    @builtins.property
    @jsii.member(jsii_name="variants")
    def variants(self) -> typing.List["PromptVariant"]:
        '''(experimental) The variants of the prompt.

        :stability: experimental
        '''
        return typing.cast(typing.List["PromptVariant"], jsii.get(self, "variants"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key that the prompt is encrypted with.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptVersion"))

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30a1a38bb8b0d638d069ad28bc55cbba27373d5af3489817853bd7e1dc88410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_arn": "promptArn",
        "kms_key": "kmsKey",
        "prompt_version": "promptVersion",
    },
)
class PromptAttributes:
    def __init__(
        self,
        *,
        prompt_arn: builtins.str,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        prompt_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) ****************************************************************************                     ATTRS FOR IMPORTED CONSTRUCT ***************************************************************************.

        :param prompt_arn: (experimental) The ARN of the prompt.
        :param kms_key: (experimental) Optional KMS encryption key associated with this prompt.
        :param prompt_version: (experimental) The version of the prompt. Default: - "DRAFT"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cd66a5ef99991ddde61b718842ff11d482414cb8db73961c80294c681f3502)
            check_type(argname="argument prompt_arn", value=prompt_arn, expected_type=type_hints["prompt_arn"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument prompt_version", value=prompt_version, expected_type=type_hints["prompt_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt_arn": prompt_arn,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if prompt_version is not None:
            self._values["prompt_version"] = prompt_version

    @builtins.property
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345"
        '''
        result = self._values.get("prompt_arn")
        assert result is not None, "Required property 'prompt_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def prompt_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the prompt.

        :default: - "DRAFT"

        :stability: experimental
        '''
        result = self._values.get("prompt_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPrompt)
class PromptBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptBase",
):
    '''(experimental) Abstract base class for a Prompt.

    Contains methods and attributes valid for Promtps either created with CDK or imported.

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
            type_hints = typing.get_type_hints(_typecheckingstub__416e615710246dc6fdddab19da69a2adde0b7094028409f64cc9e0c153344b57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantGet")
    def grant_get(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to get the prompt.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6010854ea9d0c593f1187eff0dbb1c606b73ff1be68e89b0d245291215123a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantGet", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="promptArn")
    @abc.abstractmethod
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptId")
    @abc.abstractmethod
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    @abc.abstractmethod
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    @abc.abstractmethod
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :stability: experimental
        '''
        ...

    @prompt_version.setter
    @abc.abstractmethod
    def prompt_version(self, value: builtins.str) -> None:
        ...


class _PromptBaseProxy(
    PromptBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="promptArn")
    def prompt_arn(self) -> builtins.str:
        '''(experimental) The ARN of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptArn"))

    @builtins.property
    @jsii.member(jsii_name="promptId")
    def prompt_id(self) -> builtins.str:
        '''(experimental) The ID of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS encryption key associated with this prompt.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="promptVersion")
    def prompt_version(self) -> builtins.str:
        '''(experimental) The version of the prompt.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "promptVersion"))

    @prompt_version.setter
    def prompt_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e18fab10acf8af328be25f79340aeb64cc011327127be967f99f267d6b6c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptVersion", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PromptBase).__jsii_proxy_class__ = lambda : _PromptBaseProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "base_prompt_template": "basePromptTemplate",
        "inference_configuration": "inferenceConfiguration",
        "prompt_creation_mode": "promptCreationMode",
        "prompt_state": "promptState",
        "prompt_type": "promptType",
        "parser_mode": "parserMode",
    },
)
class PromptConfiguration:
    def __init__(
        self,
        *,
        base_prompt_template: builtins.str,
        inference_configuration: typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]],
        prompt_creation_mode: "PromptCreationMode",
        prompt_state: "PromptState",
        prompt_type: "PromptType",
        parser_mode: typing.Optional[ParserMode] = None,
    ) -> None:
        '''(experimental) Contains configurations to override a prompt template in one part of an agent sequence.

        :param base_prompt_template: (experimental) Defines the prompt template with which to replace the default prompt template. length 0-100000
        :param inference_configuration: (experimental) Contains inference parameters to use when the agent invokes a foundation model in the part of the agent sequence defined by the promptType.
        :param prompt_creation_mode: (experimental) Specifies whether to override the default prompt template for this promptType. Set this value to OVERRIDDEN to use the prompt that you provide in the basePromptTemplate. If you leave it as DEFAULT, the agent uses a default prompt template.
        :param prompt_state: (experimental) Specifies whether to allow the agent to carry out the step specified in the promptType. If you set this value to DISABLED, the agent skips that step. The default state for each promptType is as follows:: PRE_PROCESSING – ENABLED ORCHESTRATION – ENABLED KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED POST_PROCESSING – DISABLED
        :param prompt_type: (experimental) The step in the agent sequence that this prompt configuration applies to.
        :param parser_mode: (experimental) Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the promptType. If you set the field as OVERRIDEN, the overrideLambda field in the PromptOverrideConfiguration must be specified with the ARN of a Lambda function.

        :stability: experimental
        '''
        if isinstance(inference_configuration, dict):
            inference_configuration = InferenceConfiguration(**inference_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e333bbbacb815921d7a258c01d4d87250548623e984fd2e844c23791ddeeed)
            check_type(argname="argument base_prompt_template", value=base_prompt_template, expected_type=type_hints["base_prompt_template"])
            check_type(argname="argument inference_configuration", value=inference_configuration, expected_type=type_hints["inference_configuration"])
            check_type(argname="argument prompt_creation_mode", value=prompt_creation_mode, expected_type=type_hints["prompt_creation_mode"])
            check_type(argname="argument prompt_state", value=prompt_state, expected_type=type_hints["prompt_state"])
            check_type(argname="argument prompt_type", value=prompt_type, expected_type=type_hints["prompt_type"])
            check_type(argname="argument parser_mode", value=parser_mode, expected_type=type_hints["parser_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_prompt_template": base_prompt_template,
            "inference_configuration": inference_configuration,
            "prompt_creation_mode": prompt_creation_mode,
            "prompt_state": prompt_state,
            "prompt_type": prompt_type,
        }
        if parser_mode is not None:
            self._values["parser_mode"] = parser_mode

    @builtins.property
    def base_prompt_template(self) -> builtins.str:
        '''(experimental) Defines the prompt template with which to replace the default prompt template.

        length 0-100000

        :stability: experimental
        '''
        result = self._values.get("base_prompt_template")
        assert result is not None, "Required property 'base_prompt_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inference_configuration(self) -> InferenceConfiguration:
        '''(experimental) Contains inference parameters to use when the agent invokes a foundation model in the part of the agent sequence defined by the promptType.

        :stability: experimental
        '''
        result = self._values.get("inference_configuration")
        assert result is not None, "Required property 'inference_configuration' is missing"
        return typing.cast(InferenceConfiguration, result)

    @builtins.property
    def prompt_creation_mode(self) -> "PromptCreationMode":
        '''(experimental) Specifies whether to override the default prompt template for this promptType.

        Set this value to OVERRIDDEN to use the prompt that you
        provide in the basePromptTemplate. If you leave it as DEFAULT, the agent
        uses a default prompt template.

        :stability: experimental
        '''
        result = self._values.get("prompt_creation_mode")
        assert result is not None, "Required property 'prompt_creation_mode' is missing"
        return typing.cast("PromptCreationMode", result)

    @builtins.property
    def prompt_state(self) -> "PromptState":
        '''(experimental) Specifies whether to allow the agent to carry out the step specified in the promptType.

        If you set this value to DISABLED, the agent skips that
        step. The default state for each promptType is as follows::

           PRE_PROCESSING – ENABLED
           ORCHESTRATION – ENABLED
           KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED
           POST_PROCESSING – DISABLED

        :stability: experimental
        '''
        result = self._values.get("prompt_state")
        assert result is not None, "Required property 'prompt_state' is missing"
        return typing.cast("PromptState", result)

    @builtins.property
    def prompt_type(self) -> "PromptType":
        '''(experimental) The step in the agent sequence that this prompt configuration applies to.

        :stability: experimental
        '''
        result = self._values.get("prompt_type")
        assert result is not None, "Required property 'prompt_type' is missing"
        return typing.cast("PromptType", result)

    @builtins.property
    def parser_mode(self) -> typing.Optional[ParserMode]:
        '''(experimental) Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the promptType.

        If you set the field as OVERRIDEN, the
        overrideLambda field in the PromptOverrideConfiguration must be specified
        with the ARN of a Lambda function.

        :stability: experimental
        '''
        result = self._values.get("parser_mode")
        return typing.cast(typing.Optional[ParserMode], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptCreationMode"
)
class PromptCreationMode(enum.Enum):
    '''(experimental) Specifies whether to override the default prompt template for this promptType.

    Set this value to OVERRIDDEN to use the prompt that you
    provide in the basePromptTemplate. If you leave it as DEFAULT, the agent
    uses a default prompt template.

    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''
    :stability: experimental
    '''
    OVERRIDDEN = "OVERRIDDEN"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptOverrideConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_configurations": "promptConfigurations",
        "override_lambda": "overrideLambda",
    },
)
class PromptOverrideConfiguration:
    def __init__(
        self,
        *,
        prompt_configurations: typing.Sequence[typing.Union[PromptConfiguration, typing.Dict[builtins.str, typing.Any]]],
        override_lambda: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Contains configurations to override prompts in different parts of an agent sequence.

        :param prompt_configurations: (experimental) Contains configurations to override a prompt template in one part of an agent sequence.
        :param override_lambda: (experimental) The ARN of the Lambda function to use when parsing the raw foundation model output in parts of the agent sequence. If you specify this field, at least one of the promptConfigurations must contain a parserMode value that is set to OVERRIDDEN.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87069825e4e1447731b12e085f8869b15f2bd52ca2b57df2d0342674371c9580)
            check_type(argname="argument prompt_configurations", value=prompt_configurations, expected_type=type_hints["prompt_configurations"])
            check_type(argname="argument override_lambda", value=override_lambda, expected_type=type_hints["override_lambda"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt_configurations": prompt_configurations,
        }
        if override_lambda is not None:
            self._values["override_lambda"] = override_lambda

    @builtins.property
    def prompt_configurations(self) -> typing.List[PromptConfiguration]:
        '''(experimental) Contains configurations to override a prompt template in one part of an agent sequence.

        :stability: experimental
        '''
        result = self._values.get("prompt_configurations")
        assert result is not None, "Required property 'prompt_configurations' is missing"
        return typing.cast(typing.List[PromptConfiguration], result)

    @builtins.property
    def override_lambda(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the Lambda function to use when parsing the raw foundation model output in parts of the agent sequence.

        If you specify this field,
        at least one of the promptConfigurations must contain a parserMode value
        that is set to OVERRIDDEN.

        :stability: experimental
        '''
        result = self._values.get("override_lambda")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptOverrideConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptProps",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_name": "promptName",
        "default_variant": "defaultVariant",
        "description": "description",
        "kms_key": "kmsKey",
        "variants": "variants",
    },
)
class PromptProps:
    def __init__(
        self,
        *,
        prompt_name: builtins.str,
        default_variant: typing.Optional["PromptVariant"] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        variants: typing.Optional[typing.Sequence["PromptVariant"]] = None,
    ) -> None:
        '''(experimental) ****************************************************************************                       PROPS FOR NEW CONSTRUCT ***************************************************************************.

        :param prompt_name: (experimental) The name of the prompt.
        :param default_variant: (experimental) The Prompt Variant that will be used by default. Default: - No default variant provided.
        :param description: (experimental) A description of what the prompt does. Default: - No description provided.
        :param kms_key: (experimental) The KMS key that the prompt is encrypted with. Default: - AWS owned and managed key.
        :param variants: (experimental) The variants of your prompt. Variants can use different messages, models, or configurations so that you can compare their outputs to decide the best variant for your use case. Maximum of 3 variants.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed24724d2a2267a3662057e3f507a648a9688b88f50d099de8ac08580da8541)
            check_type(argname="argument prompt_name", value=prompt_name, expected_type=type_hints["prompt_name"])
            check_type(argname="argument default_variant", value=default_variant, expected_type=type_hints["default_variant"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument variants", value=variants, expected_type=type_hints["variants"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt_name": prompt_name,
        }
        if default_variant is not None:
            self._values["default_variant"] = default_variant
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if variants is not None:
            self._values["variants"] = variants

    @builtins.property
    def prompt_name(self) -> builtins.str:
        '''(experimental) The name of the prompt.

        :stability: experimental
        '''
        result = self._values.get("prompt_name")
        assert result is not None, "Required property 'prompt_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_variant(self) -> typing.Optional["PromptVariant"]:
        '''(experimental) The Prompt Variant that will be used by default.

        :default: - No default variant provided.

        :stability: experimental
        '''
        result = self._values.get("default_variant")
        return typing.cast(typing.Optional["PromptVariant"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of what the prompt does.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key that the prompt is encrypted with.

        :default: - AWS owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def variants(self) -> typing.Optional[typing.List["PromptVariant"]]:
        '''(experimental) The variants of your prompt.

        Variants can use different messages, models,
        or configurations so that you can compare their outputs to decide the best
        variant for your use case. Maximum of 3 variants.

        :stability: experimental
        '''
        result = self._values.get("variants")
        return typing.cast(typing.Optional[typing.List["PromptVariant"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptState")
class PromptState(enum.Enum):
    '''(experimental) Specifies whether to allow the agent to carry out the step specified in the promptType.

    If you set this value to DISABLED, the agent skips that step.
    The default state for each promptType is as follows::

       PRE_PROCESSING – ENABLED
       ORCHESTRATION – ENABLED
       KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED
       POST_PROCESSING – DISABLED

    :stability: experimental
    '''

    ENABLED = "ENABLED"
    '''
    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''
    :stability: experimental
    '''


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptTemplateType"
)
class PromptTemplateType(enum.Enum):
    '''
    :stability: experimental
    '''

    TEXT = "TEXT"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptType")
class PromptType(enum.Enum):
    '''(experimental) The step in the agent sequence that this prompt configuration applies to.

    :stability: experimental
    '''

    PRE_PROCESSING = "PRE_PROCESSING"
    '''
    :stability: experimental
    '''
    ORCHESTRATION = "ORCHESTRATION"
    '''
    :stability: experimental
    '''
    POST_PROCESSING = "POST_PROCESSING"
    '''
    :stability: experimental
    '''
    KNOWLEDGE_BASE_RESPONSE_GENERATION = "KNOWLEDGE_BASE_RESPONSE_GENERATION"
    '''
    :stability: experimental
    '''


class PromptVariant(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptVariant",
):
    '''(experimental) Variants are specific sets of inputs that guide FMs on Amazon Bedrock to generate an appropriate response or output for a given task or instruction.

    You can optimize the prompt for specific use cases and models.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="text")
    @builtins.classmethod
    def text(
        cls,
        *,
        prompt_text: builtins.str,
        prompt_variables: typing.Sequence[builtins.str],
        inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        model: IInvokable,
        variant_name: builtins.str,
    ) -> "PromptVariant":
        '''(experimental) Static method to create a text template.

        :param prompt_text: (experimental) The text prompt. Variables are used by encolsing its name with double curly braces as in ``{{variable_name}}``.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.
        :param inference_configuration: (experimental) Inference configuration for the Text Prompt.
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.

        :stability: experimental
        '''
        props = TextPromptVariantProps(
            prompt_text=prompt_text,
            prompt_variables=prompt_variables,
            inference_configuration=inference_configuration,
            model=model,
            variant_name=variant_name,
        )

        return typing.cast("PromptVariant", jsii.sinvoke(cls, "text", [props]))

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        ...

    @name.setter
    @abc.abstractmethod
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    @abc.abstractmethod
    def template_configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty:
        '''(experimental) The template configuration.

        :stability: experimental
        '''
        ...

    @template_configuration.setter
    @abc.abstractmethod
    def template_configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty,
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="templateType")
    @abc.abstractmethod
    def template_type(self) -> PromptTemplateType:
        '''(experimental) The type of prompt template.

        :stability: experimental
        '''
        ...

    @template_type.setter
    @abc.abstractmethod
    def template_type(self, value: PromptTemplateType) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inferenceConfiguration")
    @abc.abstractmethod
    def inference_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty]:
        '''(experimental) The inference configuration.

        :stability: experimental
        '''
        ...

    @inference_configuration.setter
    @abc.abstractmethod
    def inference_configuration(
        self,
        value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="modelId")
    @abc.abstractmethod
    def model_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The unique identifier of the model with which to run inference on the prompt.

        :stability: experimental
        '''
        ...

    @model_id.setter
    @abc.abstractmethod
    def model_id(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _PromptVariantProxy(PromptVariant):
    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47858dac9c23ea6d5fe047093eb7c553df8379b538751a421229fcd6090a3d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    def template_configuration(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty:
        '''(experimental) The template configuration.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty, jsii.get(self, "templateConfiguration"))

    @template_configuration.setter
    def template_configuration(
        self,
        value: _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfacc76ecbab5bd528fdafd1e6e9ea9558ae6b7f7404301dfde9e66ae3ed865c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateType")
    def template_type(self) -> PromptTemplateType:
        '''(experimental) The type of prompt template.

        :stability: experimental
        '''
        return typing.cast(PromptTemplateType, jsii.get(self, "templateType"))

    @template_type.setter
    def template_type(self, value: PromptTemplateType) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb21a09b18d3af2233c1a12de246544b29d61535df0d28d7f9fb947c1b2668d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceConfiguration")
    def inference_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty]:
        '''(experimental) The inference configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty], jsii.get(self, "inferenceConfiguration"))

    @inference_configuration.setter
    def inference_configuration(
        self,
        value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868e405119ddf957e9771368dbe10acb67f0d6f0dc2fe35578128be175024448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The unique identifier of the model with which to run inference on the prompt.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelId"))

    @model_id.setter
    def model_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94db700745c23c237379ad0e9208bfa80e98851952c0558325390455e764cd02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelId", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PromptVariant).__jsii_proxy_class__ = lambda : _PromptVariantProxy


class PromptVersion(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptVersion",
):
    '''(experimental) Creates a version of the prompt.

    Use this to create a static snapshot of your prompt that can be deployed
    to production. Versions allow you to easily switch between different
    configurations for your prompt and update your application with the most
    appropriate version for your use-case.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-deploy.html
    :stability: experimental
    :resource: AWS::Bedrock::PromptVersion
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prompt: Prompt,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param prompt: (experimental) The prompt to use for this version.
        :param description: (experimental) The description of the prompt version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6daa6c79624257e31d9072fc0f20e2f2fc9397635524aa9d067fb36cc7cbbc53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PromptVersionProps(prompt=prompt, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="prompt")
    def prompt(self) -> Prompt:
        '''(experimental) The prompt used by this version.

        :stability: experimental
        '''
        return typing.cast(Prompt, jsii.get(self, "prompt"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) The version of the prompt that was created.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="versionArn")
    def version_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the prompt version.

        :stability: experimental

        Example::

            "arn:aws:bedrock:us-east-1:123456789012:prompt/PROMPT12345:1"
        '''
        return typing.cast(builtins.str, jsii.get(self, "versionArn"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptVersionProps",
    jsii_struct_bases=[],
    name_mapping={"prompt": "prompt", "description": "description"},
)
class PromptVersionProps:
    def __init__(
        self,
        *,
        prompt: Prompt,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prompt: (experimental) The prompt to use for this version.
        :param description: (experimental) The description of the prompt version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49af665e03ae5aea14b78e3aee6d9f0d78722f97c5b289cb5dc844a1cf90815)
            check_type(argname="argument prompt", value=prompt, expected_type=type_hints["prompt"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt": prompt,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def prompt(self) -> Prompt:
        '''(experimental) The prompt to use for this version.

        :stability: experimental
        '''
        result = self._values.get("prompt")
        assert result is not None, "Required property 'prompt' is missing"
        return typing.cast(Prompt, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the prompt version.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.RegexFilter",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "name": "name",
        "pattern": "pattern",
        "description": "description",
    },
)
class RegexFilter:
    def __init__(
        self,
        *,
        action: GuardrailAction,
        name: builtins.str,
        pattern: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A Regular expression (regex) filter for sensitive information.

        :param action: (experimental) The action to take when a regex match is detected.
        :param name: (experimental) The name of the regex filter.
        :param pattern: (experimental) The regular expression pattern to match.
        :param description: (experimental) The description of the regex filter.

        :stability: experimental

        Example::

            const regexFilter: RegexFilter = {
              name: "my-custom-filter",
              action: SensitiveInfoGuardrailAction.BLOCK,
              pattern: "\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b",
            };
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a46345c7df17f55020986d90b7ae90f85b55d19822b9b2574bc1ff9831b2d20)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
            "pattern": pattern,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def action(self) -> GuardrailAction:
        '''(experimental) The action to take when a regex match is detected.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(GuardrailAction, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the regex filter.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''(experimental) The regular expression pattern to match.

        :stability: experimental
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the regex filter.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegexFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ApiSchema(
    ApiSchema,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3ApiSchema",
):
    '''(experimental) API Schema in an S3 object.

    :stability: experimental
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: -
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c4db74d64f90be972766dae3c6ab8b2ee388726bb4dec1fa1458939ab93a5f)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [bucket, key])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> ApiSchemaConfig:
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd50c8c86df0f0a2a5a95b774555d2e2c1d079404953f77717653ea8e3f768a)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ApiSchemaConfig, jsii.invoke(self, "bind", [_scope]))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "bucket": "bucket",
        "inclusion_prefixes": "inclusionPrefixes",
    },
)
class S3DataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Interface to add a new S3DataSource to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937192d503ab06e7d72cb5fca8edb1e0959f925784ef831da357511f9247a9ec)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket that contains the data source.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The prefixes of the objects in the bucket that should be included in the data source.

        :default: - All objects in the bucket.

        :stability: experimental
        '''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSourceProps",
    jsii_struct_bases=[S3DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "bucket": "bucket",
        "inclusion_prefixes": "inclusionPrefixes",
        "knowledge_base": "knowledgeBase",
    },
)
class S3DataSourceProps(S3DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new S3 Data Source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061fd79f5c6cc3fdad0a0fcccc8c2a083f5deeb769270d6795cc47edeeaecc0b)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket that contains the data source.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The prefixes of the objects in the bucket that should be included in the data source.

        :default: - All objects in the bucket.

        :stability: experimental
        '''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3Identifier",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket_name": "s3BucketName", "s3_object_key": "s3ObjectKey"},
)
class S3Identifier:
    def __init__(
        self,
        *,
        s3_bucket_name: builtins.str,
        s3_object_key: builtins.str,
    ) -> None:
        '''(experimental) Result of the bind when ``S3ApiSchema`` is used.

        :param s3_bucket_name: (experimental) The name of the S3 bucket.
        :param s3_object_key: (experimental) The S3 object key containing the resource.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8dfefeb74c7ac32b2ae5113a03ce2743b27b34cfa67e342053f0fb90d0050f0)
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket_name": s3_bucket_name,
            "s3_object_key": s3_object_key,
        }

    @builtins.property
    def s3_bucket_name(self) -> builtins.str:
        '''(experimental) The name of the S3 bucket.

        :stability: experimental
        '''
        result = self._values.get("s3_bucket_name")
        assert result is not None, "Required property 's3_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_object_key(self) -> builtins.str:
        '''(experimental) The S3 object key containing the resource.

        :stability: experimental
        '''
        result = self._values.get("s3_object_key")
        assert result is not None, "Required property 's3_object_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Identifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceCrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class SalesforceCrawlingFilters:
    def __init__(
        self,
        *,
        object_type: "SalesforceObjectType",
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Defines the crawling filters for Salesforce data ingestion.

        :param object_type: (experimental) The Salesforce object type to which this filter applies.
        :param exclude_patterns: (experimental) Regular expression patterns to exclude specific content.
        :param include_patterns: (experimental) Regular expression patterns to include specific content.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ba2de3246503cef86100625445a5010d4594edc17ad5fe4ba4d35b9c066463)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type": object_type,
        }
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def object_type(self) -> "SalesforceObjectType":
        '''(experimental) The Salesforce object type to which this filter applies.

        :stability: experimental
        '''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast("SalesforceObjectType", result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to exclude specific content.

        :stability: experimental
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regular expression patterns to include specific content.

        :stability: experimental
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SalesforceCrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "endpoint": "endpoint",
        "filters": "filters",
    },
)
class SalesforceDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9630b4dd940c86a5fa5c47ae28d9a991c3d58e7b9c5432ba828cb2cb213d00)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "endpoint": endpoint,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The Salesforce host URL or instance URL.

        :stability: experimental

        Example::

            "https://company.salesforce.com/"
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SalesforceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SalesforceCrawlingFilters]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SalesforceDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSourceAuthType"
)
class SalesforceDataSourceAuthType(enum.Enum):
    '''(experimental) Represents the authentication types available for connecting to a Salesforce data source.

    :stability: experimental
    '''

    OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"
    '''(experimental) Your secret authentication credentials in AWS Secrets Manager should include: - ``consumerKey`` (app client ID) - ``consumerSecret`` (client secret) - ``authenticationUrl``.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSourceProps",
    jsii_struct_bases=[SalesforceDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "endpoint": "endpoint",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class SalesforceDataSourceProps(SalesforceDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dc3117cebd56970b3e49e262627a6133820bc4f98949e5002679327375f4f3)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "endpoint": endpoint,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The Salesforce host URL or instance URL.

        :stability: experimental

        Example::

            "https://company.salesforce.com/"
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SalesforceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SalesforceCrawlingFilters]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SalesforceDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceObjectType"
)
class SalesforceObjectType(enum.Enum):
    '''(experimental) Represents the Salesforce object types that can be accessed by the data source connector.

    :stability: experimental
    '''

    ACCOUNT = "ACCOUNT"
    '''
    :stability: experimental
    '''
    ATTACHMENT = "ATTACHMENT"
    '''
    :stability: experimental
    '''
    CAMPAIGN = "CAMPAIGN"
    '''
    :stability: experimental
    '''
    CONTENT_VERSION = "CONTENT_VERSION"
    '''
    :stability: experimental
    '''
    PARTNER = "PARTNER"
    '''
    :stability: experimental
    '''
    PRICEBOOK_2 = "PRICEBOOK_2"
    '''
    :stability: experimental
    '''
    CASE = "CASE"
    '''
    :stability: experimental
    '''
    CONTACT = "CONTACT"
    '''
    :stability: experimental
    '''
    CONTRACT = "CONTRACT"
    '''
    :stability: experimental
    '''
    DOCUMENT = "DOCUMENT"
    '''
    :stability: experimental
    '''
    IDEA = "IDEA"
    '''
    :stability: experimental
    '''
    LEAD = "LEAD"
    '''
    :stability: experimental
    '''
    OPPORTUNITY = "OPPORTUNITY"
    '''
    :stability: experimental
    '''
    PRODUCT_2 = "PRODUCT_2"
    '''
    :stability: experimental
    '''
    SOLUTION = "SOLUTION"
    '''
    :stability: experimental
    '''
    TASK = "TASK"
    '''
    :stability: experimental
    '''
    FEED_ITEM = "FEED_ITEM"
    '''
    :stability: experimental
    '''
    FEED_COMMENT = "FEED_COMMENT"
    '''
    :stability: experimental
    '''
    KNOWLEDGE_KAV = "KNOWLEDGE_KAV"
    '''
    :stability: experimental
    '''
    USER = "USER"
    '''
    :stability: experimental
    '''
    COLLABORATION_GROUP = "COLLABORATION_GROUP"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointCrawlingFilters",
    jsii_struct_bases=[],
    name_mapping={
        "object_type": "objectType",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
    },
)
class SharePointCrawlingFilters:
    def __init__(
        self,
        *,
        object_type: "SharePointObjectType",
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Defines the crawling filters for SharePoint data ingestion.

        These filters allow
        you to specify which content should be included or excluded during the crawling process.
        If you specify an inclusion and exclusion filter and both match a document,
        the exclusion filter takes precedence and the document isn’t crawled.

        :param object_type: (experimental) The SharePoint object type this filter applies to.
        :param exclude_patterns: (experimental) Optional array of regular expression patterns to exclude specific content. Content matching these patterns will be skipped during crawling.
        :param include_patterns: (experimental) Optional array of regular expression patterns to include specific content. Only content matching these patterns will be crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc66a84b3c3b22e2879cf44c3edf17abf1ec9c5fb2ebee76fab9d6455ad43867)
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type": object_type,
        }
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns

    @builtins.property
    def object_type(self) -> "SharePointObjectType":
        '''(experimental) The SharePoint object type this filter applies to.

        :stability: experimental
        '''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast("SharePointObjectType", result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional array of regular expression patterns to exclude specific content.

        Content matching these patterns will be skipped during crawling.

        :stability: experimental

        Example::

            ['.*private.*', '.*confidential.*']
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional array of regular expression patterns to include specific content.

        Only content matching these patterns will be crawled.

        :stability: experimental

        Example::

            ['.*public.*', '.*shared.*']
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharePointCrawlingFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "domain": "domain",
        "site_urls": "siteUrls",
        "tenant_id": "tenantId",
        "filters": "filters",
    },
)
class SharePointDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c756d6075defa355f5293064dde03559d8f435bbe0f49037277d8587875a983f)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument site_urls", value=site_urls, expected_type=type_hints["site_urls"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "domain": domain,
            "site_urls": site_urls,
            "tenant_id": tenant_id,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''(experimental) The domain of your SharePoint instance or site URL/URLs.

        :stability: experimental

        Example::

            "yourdomain"
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The SharePoint site URL/URLs.

        Must start with “https”. All URLs must start with same protocol.

        :stability: experimental

        Example::

            ["https://yourdomain.sharepoint.com/sites/mysite"]
        '''
        result = self._values.get("site_urls")
        assert result is not None, "Required property 'site_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''(experimental) The identifier of your Microsoft 365 tenant.

        :stability: experimental

        Example::

            "d1c035a6-1dcf-457d-97e3"
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SharePointCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SharePointCrawlingFilters]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharePointDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSourceAuthType"
)
class SharePointDataSourceAuthType(enum.Enum):
    '''(experimental) Represents the authentication types available for connecting to a SharePoint data source.

    :stability: experimental
    '''

    OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"
    '''(experimental) OAuth 2.0 Client Credentials flow for authentication with SharePoint. Your secret authentication credentials in AWS Secrets Manager should include: - ``username``: The admin username for SharePoint authentication - ``password``: The admin password associated with the username - ``clientId``: The client ID (also known as application ID) - ``clientSecret``: The client secret.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSourceProps",
    jsii_struct_bases=[SharePointDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "domain": "domain",
        "site_urls": "siteUrls",
        "tenant_id": "tenantId",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class SharePointDataSourceProps(SharePointDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cac4a3c20de6d6ae043e36137b1e8760f3e2ae41c065f2a00a80740ce91b38)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument site_urls", value=site_urls, expected_type=type_hints["site_urls"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "domain": domain,
            "site_urls": site_urls,
            "tenant_id": tenant_id,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''(experimental) The domain of your SharePoint instance or site URL/URLs.

        :stability: experimental

        Example::

            "yourdomain"
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The SharePoint site URL/URLs.

        Must start with “https”. All URLs must start with same protocol.

        :stability: experimental

        Example::

            ["https://yourdomain.sharepoint.com/sites/mysite"]
        '''
        result = self._values.get("site_urls")
        assert result is not None, "Required property 'site_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''(experimental) The identifier of your Microsoft 365 tenant.

        :stability: experimental

        Example::

            "d1c035a6-1dcf-457d-97e3"
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[SharePointCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[SharePointCrawlingFilters]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharePointDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointObjectType"
)
class SharePointObjectType(enum.Enum):
    '''(experimental) Represents the SharePoint object types that can be accessed by the data source connector.

    :stability: experimental
    '''

    PAGE = "PAGE"
    '''(experimental) Represents a SharePoint page, which typically contains web parts and content.

    :stability: experimental
    '''
    EVENT = "EVENT"
    '''(experimental) Represents a calendar event in SharePoint.

    :stability: experimental
    '''
    FILE = "FILE"
    '''(experimental) Represents a file stored in SharePoint document libraries.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.TextPromptVariantProps",
    jsii_struct_bases=[CommonPromptVariantProps],
    name_mapping={
        "model": "model",
        "variant_name": "variantName",
        "prompt_text": "promptText",
        "prompt_variables": "promptVariables",
        "inference_configuration": "inferenceConfiguration",
    },
)
class TextPromptVariantProps(CommonPromptVariantProps):
    def __init__(
        self,
        *,
        model: IInvokable,
        variant_name: builtins.str,
        prompt_text: builtins.str,
        prompt_variables: typing.Sequence[builtins.str],
        inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param model: (experimental) The model which is used to run the prompt. The model could be a foundation model, a custom model, or a provisioned model.
        :param variant_name: (experimental) The name of the prompt variant.
        :param prompt_text: (experimental) The text prompt. Variables are used by encolsing its name with double curly braces as in ``{{variable_name}}``.
        :param prompt_variables: (experimental) The variables in the prompt template that can be filled in at runtime.
        :param inference_configuration: (experimental) Inference configuration for the Text Prompt.

        :stability: experimental
        '''
        if isinstance(inference_configuration, dict):
            inference_configuration = _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty(**inference_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd54adac2df83b870909830e4b8468b5d71a8b9dac001336a6076238c87d3c3d)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument prompt_text", value=prompt_text, expected_type=type_hints["prompt_text"])
            check_type(argname="argument prompt_variables", value=prompt_variables, expected_type=type_hints["prompt_variables"])
            check_type(argname="argument inference_configuration", value=inference_configuration, expected_type=type_hints["inference_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model": model,
            "variant_name": variant_name,
            "prompt_text": prompt_text,
            "prompt_variables": prompt_variables,
        }
        if inference_configuration is not None:
            self._values["inference_configuration"] = inference_configuration

    @builtins.property
    def model(self) -> IInvokable:
        '''(experimental) The model which is used to run the prompt.

        The model could be a foundation
        model, a custom model, or a provisioned model.

        :stability: experimental
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast(IInvokable, result)

    @builtins.property
    def variant_name(self) -> builtins.str:
        '''(experimental) The name of the prompt variant.

        :stability: experimental
        '''
        result = self._values.get("variant_name")
        assert result is not None, "Required property 'variant_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prompt_text(self) -> builtins.str:
        '''(experimental) The text prompt.

        Variables are used by encolsing its name with double curly braces
        as in ``{{variable_name}}``.

        :stability: experimental
        '''
        result = self._values.get("prompt_text")
        assert result is not None, "Required property 'prompt_text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prompt_variables(self) -> typing.List[builtins.str]:
        '''(experimental) The variables in the prompt template that can be filled in at runtime.

        :stability: experimental
        '''
        result = self._values.get("prompt_variables")
        assert result is not None, "Required property 'prompt_variables' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def inference_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty]:
        '''(experimental) Inference configuration for the Text Prompt.

        :stability: experimental
        '''
        result = self._values.get("inference_configuration")
        return typing.cast(typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextPromptVariantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Topic(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Topic",
):
    '''(experimental) Defines a topic to deny.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        definition: builtins.str,
        examples: typing.Sequence[builtins.str],
        name: builtins.str,
    ) -> None:
        '''
        :param definition: (experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic. Avoid starting with "don't".
        :param examples: (experimental) Representative phrases that refer to the topic. These phrases can represent a user input or a model response. Add up to 5 phrases, up to 100 characters each.
        :param name: (experimental) The name of the topic to deny.

        :stability: experimental
        '''
        props = CustomTopicProps(definition=definition, examples=examples, name=name)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        *,
        definition: builtins.str,
        examples: typing.Sequence[builtins.str],
        name: builtins.str,
    ) -> "Topic":
        '''
        :param definition: (experimental) Provide a clear definition to detect and block user inputs and FM responses that fall into this topic. Avoid starting with "don't".
        :param examples: (experimental) Representative phrases that refer to the topic. These phrases can represent a user input or a model response. Add up to 5 phrases, up to 100 characters each.
        :param name: (experimental) The name of the topic to deny.

        :stability: experimental
        '''
        props = CustomTopicProps(definition=definition, examples=examples, name=name)

        return typing.cast("Topic", jsii.sinvoke(cls, "custom", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FINANCIAL_ADVICE")
    def FINANCIAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "FINANCIAL_ADVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INNOPROPRIATE_CONTENT")
    def INNOPROPRIATE_CONTENT(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "INNOPROPRIATE_CONTENT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LEGAL_ADVICE")
    def LEGAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "LEGAL_ADVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEDICAL_ADVICE")
    def MEDICAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "MEDICAL_ADVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="POLITICAL_ADVICE")
    def POLITICAL_ADVICE(cls) -> "Topic":
        '''
        :stability: experimental
        '''
        return typing.cast("Topic", jsii.sget(cls, "POLITICAL_ADVICE"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        '''(experimental) Definition of the topic.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the topic to deny.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="examples")
    def examples(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Representative phrases that refer to the topic.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "examples"))


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.TransformationStep"
)
class TransformationStep(enum.Enum):
    '''(experimental) Defines the step in the ingestion process where the custom transformation is applied.

    :stability: experimental
    '''

    POST_CHUNKING = "POST_CHUNKING"
    '''(experimental) Processes documents after they have been converted into chunks.

    This allows for custom chunk-level metadata addition or custom post-chunking logic.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.WebCrawlerDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "source_urls": "sourceUrls",
        "crawling_rate": "crawlingRate",
        "crawling_scope": "crawlingScope",
        "filters": "filters",
    },
)
class WebCrawlerDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None

        :stability: experimental
        '''
        if isinstance(filters, dict):
            filters = CrawlingFilters(**filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2d4384933474c1f544b514a9796e0d1ce1eea63851d2a0cbad594f4b1d4830)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument source_urls", value=source_urls, expected_type=type_hints["source_urls"])
            check_type(argname="argument crawling_rate", value=crawling_rate, expected_type=type_hints["crawling_rate"])
            check_type(argname="argument crawling_scope", value=crawling_scope, expected_type=type_hints["crawling_scope"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_urls": source_urls,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if crawling_rate is not None:
            self._values["crawling_rate"] = crawling_rate
        if crawling_scope is not None:
            self._values["crawling_scope"] = crawling_scope
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def source_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.

        :stability: experimental
        '''
        result = self._values.get("source_urls")
        assert result is not None, "Required property 'source_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def crawling_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The max rate at which pages are crawled, up to 300 per minute per host.

        Higher values will decrease sync time but increase the load on the host.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("crawling_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def crawling_scope(self) -> typing.Optional[CrawlingScope]:
        '''(experimental) The scope of the crawling.

        :default: - CrawlingScope.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("crawling_scope")
        return typing.cast(typing.Optional[CrawlingScope], result)

    @builtins.property
    def filters(self) -> typing.Optional[CrawlingFilters]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[CrawlingFilters], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebCrawlerDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.WebCrawlerDataSourceProps",
    jsii_struct_bases=[WebCrawlerDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "source_urls": "sourceUrls",
        "crawling_rate": "crawlingRate",
        "crawling_scope": "crawlingScope",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class WebCrawlerDataSourceProps(WebCrawlerDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if isinstance(filters, dict):
            filters = CrawlingFilters(**filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7f1066a3d54b5b87f6d6542c10949f6480a3b99f641342456db80c76a73a8c)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument source_urls", value=source_urls, expected_type=type_hints["source_urls"])
            check_type(argname="argument crawling_rate", value=crawling_rate, expected_type=type_hints["crawling_rate"])
            check_type(argname="argument crawling_scope", value=crawling_scope, expected_type=type_hints["crawling_scope"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_urls": source_urls,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if crawling_rate is not None:
            self._values["crawling_rate"] = crawling_rate
        if crawling_scope is not None:
            self._values["crawling_scope"] = crawling_scope
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def source_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.

        :stability: experimental
        '''
        result = self._values.get("source_urls")
        assert result is not None, "Required property 'source_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def crawling_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The max rate at which pages are crawled, up to 300 per minute per host.

        Higher values will decrease sync time but increase the load on the host.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("crawling_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def crawling_scope(self) -> typing.Optional[CrawlingScope]:
        '''(experimental) The scope of the crawling.

        :default: - CrawlingScope.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("crawling_scope")
        return typing.cast(typing.Optional[CrawlingScope], result)

    @builtins.property
    def filters(self) -> typing.Optional[CrawlingFilters]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[CrawlingFilters], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebCrawlerDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAgentAlias)
class AgentAlias(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAlias",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent_id: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param agent_id: (experimental) The unique identifier of the agent.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param alias_name: (experimental) The name for the agent alias. Default: - 'latest'
        :param description: (experimental) Description for the agent alias.
        :param resource_updates: (experimental) The list of resource update timestamps to let CloudFormation determine when to update the alias.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5252a70a25f0e579966376a7e29bb2527a503dda1a1fed24527d3559affff2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentAliasProps(
            agent_id=agent_id,
            agent_version=agent_version,
            alias_name=alias_name,
            description=description,
            resource_updates=resource_updates,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAliasArn")
    @builtins.classmethod
    def from_alias_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        alias_arn: builtins.str,
    ) -> IAgentAlias:
        '''(experimental) Brings an Agent Alias from an existing one created outside of CDK.

        :param scope: -
        :param id: -
        :param alias_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2021fc1116b8fac10f4b9c0002cd564598aef3381a39953228ad73589ad9b8ba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument alias_arn", value=alias_arn, expected_type=type_hints["alias_arn"])
        return typing.cast(IAgentAlias, jsii.sinvoke(cls, "fromAliasArn", [scope, id, alias_arn]))

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental

        Example::

            `arn:aws:bedrock:us-east-1:123456789012:agent-alias/DNCJJYQKSU/TCLCITFZTN`
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental

        Example::

            `TCLCITFZTN`
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasId"))

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        '''(experimental) The name for the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasName"))


@jsii.implements(IInvokable)
class ApplicationInferenceProfile(
    InferenceProfileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApplicationInferenceProfile",
):
    '''(experimental) Class to create a ApplicationInferenceProfile with CDK.

    These are inference profiles created by users (user defined).
    This helps to track costs and model usage.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-create.html
    :stability: experimental
    :resource: AWS::Bedrock::ApplicationInferenceProfile
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        inference_profile_name: builtins.str,
        model_source: IInvokable,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param inference_profile_name: (experimental) The name of the inference profile.
        :param model_source: (experimental) To create an application inference profile for one Region, specify a foundation model. Usage and costs for requests made to that Region with that model will be tracked. To create an application inference profile for multiple Regions, specify a cross region (system-defined) inference profile. The inference profile will route requests to the Regions defined in the cross region (system-defined) inference profile that you choose. Usage and costs for requests made to the Regions in the inference profile will be tracked.
        :param description: (experimental) Description of the inference profile.
        :param tags: (experimental) A list of tags associated with the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9295fc37ecfd5ba15c3b4b32661816cc911d30425b0457d6d9e73aab82dc7f58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationInferenceProfileProps(
            inference_profile_name=inference_profile_name,
            model_source=model_source,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationInferenceProfileAttributes")
    @builtins.classmethod
    def from_application_inference_profile_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        inference_profile_arn: builtins.str,
        inference_profile_identifier: builtins.str,
    ) -> IInferenceProfile:
        '''(experimental) Import a ApplicationInferenceProfile given its attributes.

        :param scope: -
        :param id: -
        :param inference_profile_arn: (experimental) The ARN of the application inference profile.
        :param inference_profile_identifier: (experimental) The ID or Amazon Resource Name (ARN) of the inference profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08499f882d34a991b6ff994ce67891aa81aad629aea208a0d363fe07aa2d8b5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ApplicationInferenceProfileAttributes(
            inference_profile_arn=inference_profile_arn,
            inference_profile_identifier=inference_profile_identifier,
        )

        return typing.cast(IInferenceProfile, jsii.sinvoke(cls, "fromApplicationInferenceProfileAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromCfnApplicationInferenceProfile")
    @builtins.classmethod
    def from_cfn_application_inference_profile(
        cls,
        cfn_application_inference_profile: _aws_cdk_aws_bedrock_ceddda9d.CfnApplicationInferenceProfile,
    ) -> IInferenceProfile:
        '''(experimental) Import a low-level L1 Cfn ApplicationInferenceProfile.

        :param cfn_application_inference_profile: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4756b25b5d6740797b0f293da1e552a81883343f282122c5ff5fadb11eeb76b3)
            check_type(argname="argument cfn_application_inference_profile", value=cfn_application_inference_profile, expected_type=type_hints["cfn_application_inference_profile"])
        return typing.cast(IInferenceProfile, jsii.sinvoke(cls, "fromCfnApplicationInferenceProfile", [cfn_application_inference_profile]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the application inference profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7315621579f5e4f7d30f4502f1eeff997dba6cf3f1b3fa9f44a777ac8142ef07)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the application inference profile (AIP).

        Does not grant permissions to use the model/cross-region profile in the AIP.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cee844d1aa1c3aa02aa8a059e448586063f79d5157d71fc62c9035f258d4a04)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''(experimental) Time Stamp for ApplicationInferenceProfile creation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileModel")
    def inference_profile_model(self) -> IInvokable:
        '''(experimental) The underlying model/cross-region model used by the application inference profile.

        :stability: experimental
        '''
        return typing.cast(IInvokable, jsii.get(self, "inferenceProfileModel"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileName")
    def inference_profile_name(self) -> builtins.str:
        '''(experimental) The name of the application inference profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileName"))

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) This equals to the inferenceProfileArn property, useful just to implement IInvokable interface.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The status of the application inference profile.

        ACTIVE means that the inference profile is ready to be used.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> InferenceProfileType:
        '''(experimental) The type of the inference profile.

        The following types are possible:
        SYSTEM_DEFINED – The inference profile is defined by Amazon Bedrock.
        You can route inference requests across regions with these inference profiles.
        APPLICATION – The inference profile was created by a user.
        This type of inference profile can track metrics and costs when invoking the model in it.
        The inference profile may route requests to one or multiple regions.

        :stability: experimental
        '''
        return typing.cast(InferenceProfileType, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''(experimental) Time Stamp for ApplicationInferenceProfile update.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))


@jsii.implements(IInvokable)
class BedrockFoundationModel(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.BedrockFoundationModel",
):
    '''(experimental) Bedrock models.

    If you need to use a model name that doesn't exist as a static member, you
    can instantiate a ``BedrockFoundationModel`` object, e.g: ``new BedrockFoundationModel('my-model')``.

    :stability: experimental
    '''

    def __init__(
        self,
        value: builtins.str,
        *,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param value: -
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a81fd58f8932cf2d8dbd47ee14e3d74d82d0d0245523bd77f54c7a3ebe2a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        props = BedrockFoundationModelProps(
            supports_agents=supports_agents,
            supports_cross_region=supports_cross_region,
            supports_knowledge_base=supports_knowledge_base,
            vector_dimensions=vector_dimensions,
        )

        jsii.create(self.__class__, self, [value, props])

    @jsii.member(jsii_name="fromCdkFoundationModel")
    @builtins.classmethod
    def from_cdk_foundation_model(
        cls,
        model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModel,
        *,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> "BedrockFoundationModel":
        '''
        :param model_id: -
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e574ebd23afcb2cd940b46095855d515345af1851202b2050e4beae0b61b0797)
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
        props = BedrockFoundationModelProps(
            supports_agents=supports_agents,
            supports_cross_region=supports_cross_region,
            supports_knowledge_base=supports_knowledge_base,
            vector_dimensions=vector_dimensions,
        )

        return typing.cast("BedrockFoundationModel", jsii.sinvoke(cls, "fromCdkFoundationModel", [model_id, props]))

    @jsii.member(jsii_name="fromCdkFoundationModelId")
    @builtins.classmethod
    def from_cdk_foundation_model_id(
        cls,
        model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModelIdentifier,
        *,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_cross_region: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> "BedrockFoundationModel":
        '''
        :param model_id: -
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_cross_region: (experimental) Can be used with a Cross-Region Inference Profile. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e6ba9edf9949ffdb893690a97303140d822c69b491d2f36a23884f599a2c01)
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
        props = BedrockFoundationModelProps(
            supports_agents=supports_agents,
            supports_cross_region=supports_cross_region,
            supports_knowledge_base=supports_knowledge_base,
            vector_dimensions=vector_dimensions,
        )

        return typing.cast("BedrockFoundationModel", jsii.sinvoke(cls, "fromCdkFoundationModelId", [model_id, props]))

    @jsii.member(jsii_name="asArn")
    def as_arn(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.str:
        '''(experimental) Returns the ARN of the foundation model in the following format: ``arn:${Partition}:bedrock:${Region}::foundation-model/${ResourceId}``.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0736a1f1795a1917c49125732e66d2d15e2a25a6b98ac778b58a6ed32dc0df7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.str, jsii.invoke(self, "asArn", [construct]))

    @jsii.member(jsii_name="asIModel")
    def as_i_model(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.IModel:
        '''
        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da72b0f5ffa432a07504325247590f94f501d9e78a5f834d66e81cfc7e0273f1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.IModel, jsii.invoke(self, "asIModel", [construct]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the Foundation Model in the stack region.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51a4f667d4d649aafa9ba1bacf7d35b00909caf39e4001910a74850fc7131df)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="grantInvokeAllRegions")
    def grant_invoke_all_regions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the Foundation Model in all regions.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d3c75724e9e59d672c6ddd0ebf03051252caf48c764eeff6f38c9dbc5d4750)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvokeAllRegions", [grantee]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_NOVA_LITE_V1")
    def AMAZON_NOVA_LITE_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_NOVA_LITE_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_NOVA_MICRO_V1")
    def AMAZON_NOVA_MICRO_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_NOVA_MICRO_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_NOVA_PRO_V1")
    def AMAZON_NOVA_PRO_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_NOVA_PRO_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_PREMIER_V1_0")
    def AMAZON_TITAN_PREMIER_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_TITAN_PREMIER_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TEXT_EXPRESS_V1")
    def AMAZON_TITAN_TEXT_EXPRESS_V1(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           AMAZON *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_TITAN_TEXT_EXPRESS_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_5_HAIKU_V1_0")
    def ANTHROPIC_CLAUDE_3_5_HAIKU_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_5_HAIKU_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_5_SONNET_V1_0")
    def ANTHROPIC_CLAUDE_3_5_SONNET_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_5_SONNET_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_5_SONNET_V2_0")
    def ANTHROPIC_CLAUDE_3_5_SONNET_V2_0(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           ANTHROPIC *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_5_SONNET_V2_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_HAIKU_V1_0")
    def ANTHROPIC_CLAUDE_HAIKU_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_HAIKU_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_INSTANT_V1_2")
    def ANTHROPIC_CLAUDE_INSTANT_V1_2(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_INSTANT_V1_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_OPUS_V1_0")
    def ANTHROPIC_CLAUDE_OPUS_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_OPUS_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_SONNET_V1_0")
    def ANTHROPIC_CLAUDE_SONNET_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_SONNET_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2")
    def ANTHROPIC_CLAUDE_V2(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_1")
    def ANTHROPIC_CLAUDE_V2_1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_ENGLISH_V3")
    def COHERE_EMBED_ENGLISH_V3(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           COHERE *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "COHERE_EMBED_ENGLISH_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_MULTILINGUAL_V3")
    def COHERE_EMBED_MULTILINGUAL_V3(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "COHERE_EMBED_MULTILINGUAL_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_2_11B_INSTRUCT_V1")
    def META_LLAMA_3_2_11_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''(experimental) **************************************************************************                           META *************************************************************************.

        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_2_11B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_2_1B_INSTRUCT_V1")
    def META_LLAMA_3_2_1_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_2_1B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_2_3B_INSTRUCT_V1")
    def META_LLAMA_3_2_3_B_INSTRUCT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "META_LLAMA_3_2_3B_INSTRUCT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V1")
    def TITAN_EMBED_TEXT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V2_1024")
    def TITAN_EMBED_TEXT_V2_1024(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V2_1024"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V2_256")
    def TITAN_EMBED_TEXT_V2_256(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V2_256"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V2_512")
    def TITAN_EMBED_TEXT_V2_512(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V2_512"))

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Bedrock invokable abstraction.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @builtins.property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelArn"))

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> builtins.str:
        '''(experimental) **************************************************************************                           Constructor *************************************************************************.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelId"))

    @builtins.property
    @jsii.member(jsii_name="supportsAgents")
    def supports_agents(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsAgents"))

    @builtins.property
    @jsii.member(jsii_name="supportsCrossRegion")
    def supports_cross_region(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsCrossRegion"))

    @builtins.property
    @jsii.member(jsii_name="supportsKnowledgeBase")
    def supports_knowledge_base(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsKnowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="vectorDimensions")
    def vector_dimensions(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vectorDimensions"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSourceAssociationProps",
    jsii_struct_bases=[DataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "confluence_url": "confluenceUrl",
        "auth_type": "authType",
        "filters": "filters",
    },
)
class ConfluenceDataSourceAssociationProps(DataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Interface to add a new data source to an existing KB.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825542cfcf1e14b8a9bbb49badd630cea24320a1c93de247ce04dade6510a396)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument confluence_url", value=confluence_url, expected_type=type_hints["confluence_url"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "confluence_url": confluence_url,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def confluence_url(self) -> builtins.str:
        '''(experimental) The Confluence host URL or instance URL.

        :stability: experimental

        Example::

            https://example.atlassian.net
        '''
        result = self._values.get("confluence_url")
        assert result is not None, "Required property 'confluence_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_type(self) -> typing.Optional[ConfluenceDataSourceAuthType]:
        '''(experimental) The supported authentication method to connect to the data source.

        :default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS

        :stability: experimental
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[ConfluenceDataSourceAuthType], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[ConfluenceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[ConfluenceCrawlingFilters]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfluenceDataSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSourceProps",
    jsii_struct_bases=[ConfluenceDataSourceAssociationProps],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "custom_transformation": "customTransformation",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_name": "dataSourceName",
        "description": "description",
        "kms_key": "kmsKey",
        "parsing_strategy": "parsingStrategy",
        "auth_secret": "authSecret",
        "confluence_url": "confluenceUrl",
        "auth_type": "authType",
        "filters": "filters",
        "knowledge_base": "knowledgeBase",
    },
)
class ConfluenceDataSourceProps(ConfluenceDataSourceAssociationProps):
    def __init__(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        knowledge_base: IKnowledgeBase,
    ) -> None:
        '''(experimental) Interface to create a new standalone data source object.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14df6d19dffd71a4d3ac18b026e201bc33f4eabb05690ed07f68835b4c37b32)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument custom_transformation", value=custom_transformation, expected_type=type_hints["custom_transformation"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument auth_secret", value=auth_secret, expected_type=type_hints["auth_secret"])
            check_type(argname="argument confluence_url", value=confluence_url, expected_type=type_hints["confluence_url"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_secret": auth_secret,
            "confluence_url": confluence_url,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if custom_transformation is not None:
            self._values["custom_transformation"] = custom_transformation
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parsing_strategy is not None:
            self._values["parsing_strategy"] = parsing_strategy
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking stategy to use for splitting your documents or content.

        The chunks are then converted to embeddings and written to the vector
        index allowing for similarity search and retrieval of the content.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def custom_transformation(self) -> typing.Optional[CustomTransformation]:
        '''(experimental) The custom transformation strategy to use.

        :default: - No custom transformation is used.

        :stability: experimental
        '''
        result = self._values.get("custom_transformation")
        return typing.cast(typing.Optional[CustomTransformation], result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[DataDeletionPolicy]:
        '''(experimental) The data deletion policy to apply to the data source.

        :default: - Sets the data deletion policy to the default of the data source type.

        :stability: experimental
        '''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[DataDeletionPolicy], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - A new name will be generated.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the data source.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: - Service owned and managed key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parsing_strategy(self) -> typing.Optional[ParsingStategy]:
        '''(experimental) The parsing strategy to use.

        :default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        result = self._values.get("parsing_strategy")
        return typing.cast(typing.Optional[ParsingStategy], result)

    @builtins.property
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL.

        Secret must start with "AmazonBedrock-".

        :stability: experimental
        '''
        result = self._values.get("auth_secret")
        assert result is not None, "Required property 'auth_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def confluence_url(self) -> builtins.str:
        '''(experimental) The Confluence host URL or instance URL.

        :stability: experimental

        Example::

            https://example.atlassian.net
        '''
        result = self._values.get("confluence_url")
        assert result is not None, "Required property 'confluence_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_type(self) -> typing.Optional[ConfluenceDataSourceAuthType]:
        '''(experimental) The supported authentication method to connect to the data source.

        :default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS

        :stability: experimental
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[ConfluenceDataSourceAuthType], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[ConfluenceCrawlingFilters]]:
        '''(experimental) The filters (regular expression patterns) for the crawling.

        If there's a conflict, the exclude pattern takes precedence.

        :default: None - all your content is crawled.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[ConfluenceCrawlingFilters]], result)

    @builtins.property
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base to associate with the data source.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(IKnowledgeBase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfluenceDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInvokable, IInferenceProfile)
class CrossRegionInferenceProfile(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.CrossRegionInferenceProfile",
):
    '''(experimental) Cross-region inference enables you to seamlessly manage unplanned traffic bursts by utilizing compute across different AWS Regions.

    With cross-region
    inference, you can distribute traffic across multiple AWS Regions, enabling
    higher throughput and enhanced resilience during periods of peak demands.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromConfig")
    @builtins.classmethod
    def from_config(
        cls,
        *,
        geo_region: CrossRegionInferenceProfileRegion,
        model: BedrockFoundationModel,
    ) -> "CrossRegionInferenceProfile":
        '''
        :param geo_region: (experimental) The geographic region where the traffic is going to be distributed. Routing factors in user traffic, demand and utilization of resources.
        :param model: (experimental) A model supporting cross-region inference.

        :stability: experimental
        '''
        config = CrossRegionInferenceProfileProps(geo_region=geo_region, model=model)

        return typing.cast("CrossRegionInferenceProfile", jsii.sinvoke(cls, "fromConfig", [config]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Gives the appropriate policies to invoke and use the Foundation Model.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f472f27b5fa3d24da2ba8a7f195c5e15bd841db7f86b5c297fc541b722f61ac6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantInvoke", [grantee]))

    @jsii.member(jsii_name="grantProfileUsage")
    def grant_profile_usage(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants appropriate permissions to use the cross-region inference profile.

        Does not grant permissions to use the model in the profile.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93fff43e7d1f97fa19dd910168fe2f7ff3f51b42c62d60e9b28f154c02abdf57)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantProfileUsage", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileArn")
    def inference_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application inference profile.

        :stability: experimental

        Example::

            'arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0'
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileId")
    def inference_profile_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the inference profile.

        :stability: experimental

        Example::

            'us.anthropic.claude-3-5-sonnet-20240620-v1:0'
        '''
        return typing.cast(builtins.str, jsii.get(self, "inferenceProfileId"))

    @builtins.property
    @jsii.member(jsii_name="inferenceProfileModel")
    def inference_profile_model(self) -> BedrockFoundationModel:
        '''(experimental) The underlying model supporting cross-region inference.

        :stability: experimental
        '''
        return typing.cast(BedrockFoundationModel, jsii.get(self, "inferenceProfileModel"))

    @builtins.property
    @jsii.member(jsii_name="invokableArn")
    def invokable_arn(self) -> builtins.str:
        '''(experimental) This equals to the inferenceProfileArn property, useful just to implement IInvokable interface.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "invokableArn"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> InferenceProfileType:
        '''(experimental) The type of inference profile.

        :stability: experimental

        Example::

            InferenceProfileType.SYSTEM_DEFINED
        '''
        return typing.cast(InferenceProfileType, jsii.get(self, "type"))


@jsii.implements(IDataSource)
class DataSourceBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceBase",
):
    '''(experimental) Specifies the base class for all data source resources (imported and new).

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
            type_hints = typing.get_type_hints(_typecheckingstub__7bd33be0b5b715618515a9e14205bd91556c356258bedc630996b5ce10baf76f)
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
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        ...


class _DataSourceBaseProxy(
    DataSourceBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DataSourceBase).__jsii_proxy_class__ = lambda : _DataSourceBaseProxy


class DataSourceNew(
    DataSourceBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSourceNew",
):
    '''(experimental) Specifies the base class for all NEW data source resources of ANY type.

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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd726166f60d1f4704e8a674b6b10ffb8ada8138d51b0fb6cd7ff76f8b98644)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="formatAsCfnProps")
    def format_as_cfn_props(
        self,
        props: typing.Union[DataSourceAssociationProps, typing.Dict[builtins.str, typing.Any]],
        *,
        type: builtins.str,
        confluence_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ConfluenceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.S3DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        salesforce_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SalesforceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        share_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SharePointDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        web_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.WebDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSourceProps:
        '''(experimental) Formats the data source configuration properties for CloudFormation.

        :param props: -
        :param type: The type of data source.
        :param confluence_configuration: The configuration information to connect to Confluence as your data source. .. epigraph:: Confluence data source connector is in preview release and is subject to change.
        :param s3_configuration: The configuration information to connect to Amazon S3 as your data source.
        :param salesforce_configuration: The configuration information to connect to Salesforce as your data source. .. epigraph:: Salesforce data source connector is in preview release and is subject to change.
        :param share_point_configuration: The configuration information to connect to SharePoint as your data source. .. epigraph:: SharePoint data source connector is in preview release and is subject to change.
        :param web_configuration: The configuration of web URLs to crawl for your data source. You should be authorized to crawl the URLs. .. epigraph:: Crawling web URLs as your data source is in preview release and is subject to change.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff20dd4f9a8695235fc5ad3f8044d1b2ab4c308a247f269a7667225817ffa47f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        data_source_configuration = _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.DataSourceConfigurationProperty(
            type=type,
            confluence_configuration=confluence_configuration,
            s3_configuration=s3_configuration,
            salesforce_configuration=salesforce_configuration,
            share_point_configuration=share_point_configuration,
            web_configuration=web_configuration,
        )

        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSourceProps, jsii.invoke(self, "formatAsCfnProps", [props, data_source_configuration]))

    @jsii.member(jsii_name="handleCommonPermissions")
    def handle_common_permissions(
        self,
        *,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''(experimental) Adds appropriate permissions to the KB execution role needed by the data source.

        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        props = DataSourceAssociationProps(
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "handleCommonPermissions", [props]))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    @abc.abstractmethod
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    @abc.abstractmethod
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    @abc.abstractmethod
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    @abc.abstractmethod
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    @abc.abstractmethod
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        ...


class _DataSourceNewProxy(
    DataSourceNew,
    jsii.proxy_for(DataSourceBase), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DataSourceNew).__jsii_proxy_class__ = lambda : _DataSourceNewProxy


@jsii.implements(IGuardrail)
class GuardrailBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.GuardrailBase",
):
    '''(experimental) Abstract base class for a Guardrail.

    Contains methods and attributes valid for Guardrails either created with CDK or imported.

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
            type_hints = typing.get_type_hints(_typecheckingstub__efd3735db5e3fe2e0ab1bdcc83a66314e304f7420d3c02093aaa2f59d0c028ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantApply")
    def grant_apply(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to apply the guardrail.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96bf842a81e21fd1954424599cbfcd6aa0d8d29978b87d0221427d57ac30a99a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantApply", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    @abc.abstractmethod
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    @abc.abstractmethod
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    @abc.abstractmethod
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key of the guardrail if custom encryption is configured.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    @abc.abstractmethod
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        ...

    @guardrail_version.setter
    @abc.abstractmethod
    def guardrail_version(self, value: builtins.str) -> None:
        ...


class _GuardrailBaseProxy(
    GuardrailBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailArn"))

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailId"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key of the guardrail if custom encryption is configured.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailVersion"))

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3213cd2c4a16450e0a0e2f790d34031e9f57737b870372668dd1026cdbc75470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailVersion", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, GuardrailBase).__jsii_proxy_class__ = lambda : _GuardrailBaseProxy


class S3DataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSource",
):
    '''(experimental) Sets up an S3 Data Source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param bucket: (experimental) The bucket that contains the data source.
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fbbb836e75c99d63b1aecb8d429a451f727eaf6d350fa9c8a3e73f4932c719)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3DataSourceProps(
            knowledge_base=knowledge_base,
            bucket=bucket,
            inclusion_prefixes=inclusion_prefixes,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket associated with the data source.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class SalesforceDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SalesforceDataSource",
):
    '''(experimental) Sets up an data source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        endpoint: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Salesforce instance URL. Secret must start with "AmazonBedrock-".
        :param endpoint: (experimental) The Salesforce host URL or instance URL.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24d143c738c77349d9a94ed93b630e764b1d3c773aec262ad85df95b6be2129)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SalesforceDataSourceProps(
            knowledge_base=knowledge_base,
            auth_secret=auth_secret,
            endpoint=endpoint,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authSecret")
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "authSecret"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        '''(experimental) The Salesforce host URL or instance URL.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class SharePointDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.SharePointDataSource",
):
    '''(experimental) Sets up an data source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        domain: builtins.str,
        site_urls: typing.Sequence[builtins.str],
        tenant_id: builtins.str,
        filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Sharepoint instance URL. Secret must start with "AmazonBedrock-".
        :param domain: (experimental) The domain of your SharePoint instance or site URL/URLs.
        :param site_urls: (experimental) The SharePoint site URL/URLs. Must start with “https”. All URLs must start with same protocol.
        :param tenant_id: (experimental) The identifier of your Microsoft 365 tenant.
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a767e627d5bb3db391024a83258857573d524cc605c090521fdd3266c3253351)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SharePointDataSourceProps(
            knowledge_base=knowledge_base,
            auth_secret=auth_secret,
            domain=domain,
            site_urls=site_urls,
            tenant_id=tenant_id,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authSecret")
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "authSecret"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        '''(experimental) The domain name of your SharePoint instance.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="siteUrls")
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The SharePoint site URL/URLs.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "siteUrls"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class WebCrawlerDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.WebCrawlerDataSource",
):
    '''(experimental) Sets up a web crawler data source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        source_urls: typing.Sequence[builtins.str],
        crawling_rate: typing.Optional[jsii.Number] = None,
        crawling_scope: typing.Optional[CrawlingScope] = None,
        filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param source_urls: (experimental) The source urls in the format ``https://www.sitename.com``. Maximum of 100 URLs.
        :param crawling_rate: (experimental) The max rate at which pages are crawled, up to 300 per minute per host. Higher values will decrease sync time but increase the load on the host. Default: 300
        :param crawling_scope: (experimental) The scope of the crawling. Default: - CrawlingScope.DEFAULT
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e8107d76623400258117634288819beb4c9790e20e7ae484c9025d9dded738)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebCrawlerDataSourceProps(
            knowledge_base=knowledge_base,
            source_urls=source_urls,
            crawling_rate=crawling_rate,
            crawling_scope=crawling_scope,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="crawlingRate")
    def crawling_rate(self) -> jsii.Number:
        '''(experimental) The max rate at which pages are crawled.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "crawlingRate"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="siteUrls")
    def site_urls(self) -> typing.List[builtins.str]:
        '''(experimental) The max rate at which pages are crawled.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "siteUrls"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class ConfluenceDataSource(
    DataSourceNew,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ConfluenceDataSource",
):
    '''(experimental) Sets up a Confluence Data Source to be added to a knowledge base.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/confluence-data-source-connector.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base: IKnowledgeBase,
        auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        confluence_url: builtins.str,
        auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        custom_transformation: typing.Optional[CustomTransformation] = None,
        data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parsing_strategy: typing.Optional[ParsingStategy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param knowledge_base: (experimental) The knowledge base to associate with the data source.
        :param auth_secret: (experimental) The AWS Secrets Manager secret that stores your authentication credentials for your Confluence instance URL. Secret must start with "AmazonBedrock-".
        :param confluence_url: (experimental) The Confluence host URL or instance URL.
        :param auth_type: (experimental) The supported authentication method to connect to the data source. Default: ConfluenceDataSourceAuthType.OAUTH2_CLIENT_CREDENTIALS
        :param filters: (experimental) The filters (regular expression patterns) for the crawling. If there's a conflict, the exclude pattern takes precedence. Default: None - all your content is crawled.
        :param chunking_strategy: (experimental) The chunking stategy to use for splitting your documents or content. The chunks are then converted to embeddings and written to the vector index allowing for similarity search and retrieval of the content. Default: ChunkingStrategy.DEFAULT
        :param custom_transformation: (experimental) The custom transformation strategy to use. Default: - No custom transformation is used.
        :param data_deletion_policy: (experimental) The data deletion policy to apply to the data source. Default: - Sets the data deletion policy to the default of the data source type.
        :param data_source_name: (experimental) The name of the data source. Default: - A new name will be generated.
        :param description: (experimental) A description of the data source. Default: - No description is provided.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: - Service owned and managed key.
        :param parsing_strategy: (experimental) The parsing strategy to use. Default: - No Parsing Stategy is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38f8a816fb7d23775a4ed11b9b014cd4c8776d9580e4dae986abe72268d6d4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConfluenceDataSourceProps(
            knowledge_base=knowledge_base,
            auth_secret=auth_secret,
            confluence_url=confluence_url,
            auth_type=auth_type,
            filters=filters,
            chunking_strategy=chunking_strategy,
            custom_transformation=custom_transformation,
            data_deletion_policy=data_deletion_policy,
            data_source_name=data_source_name,
            description=description,
            kms_key=kms_key,
            parsing_strategy=parsing_strategy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authSecret")
    def auth_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''(experimental) The AWS Secrets Manager secret that stores your authentication credentials.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "authSecret"))

    @builtins.property
    @jsii.member(jsii_name="confluenceUrl")
    def confluence_url(self) -> builtins.str:
        '''(experimental) The Confluence host URL or instance URL.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "confluenceUrl"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental

        Example::

            'JHUEVXUZMU'
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceType")
    def data_source_type(self) -> DataSourceType:
        '''(experimental) The type of data source.

        :stability: experimental
        '''
        return typing.cast(DataSourceType, jsii.get(self, "dataSourceType"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBase")
    def knowledge_base(self) -> IKnowledgeBase:
        '''(experimental) The knowledge base associated with the data source.

        :stability: experimental
        '''
        return typing.cast(IKnowledgeBase, jsii.get(self, "knowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


class DataSource(
    DataSourceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.DataSource",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromDataSourceId")
    @builtins.classmethod
    def from_data_source_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        data_source_id: builtins.str,
    ) -> IDataSource:
        '''
        :param scope: -
        :param id: -
        :param data_source_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91bb2023285f784980074a6bd9353d73694f701da8c5417daa958a6ed92e7c61)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument data_source_id", value=data_source_id, expected_type=type_hints["data_source_id"])
        return typing.cast(IDataSource, jsii.sinvoke(cls, "fromDataSourceId", [scope, id, data_source_id]))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))


class Guardrail(
    GuardrailBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Guardrail",
):
    '''(experimental) Class to create a Guardrail with CDK.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        blocked_input_messaging: typing.Optional[builtins.str] = None,
        blocked_outputs_messaging: typing.Optional[builtins.str] = None,
        content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        denied_topics: typing.Optional[typing.Sequence[Topic]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        managed_word_list_filters: typing.Optional[typing.Sequence[ManagedWordFilterType]] = None,
        pii_filters: typing.Optional[typing.Sequence[typing.Union[PIIFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        regex_filters: typing.Optional[typing.Sequence[typing.Union[RegexFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: (experimental) The name of the guardrail.
        :param blocked_input_messaging: (experimental) The message to return when the guardrail blocks a prompt. Default: "Sorry, your query violates our usage policy."
        :param blocked_outputs_messaging: (experimental) The message to return when the guardrail blocks a model response. Default: "Sorry, I am unable to answer your question because of our usage policy."
        :param content_filters: (experimental) The content filters to apply to the guardrail. Note, if one of
        :param contextual_grounding_filters: (experimental) The contextual grounding filters to apply to the guardrail.
        :param denied_topics: (experimental) Up to 30 denied topics to block user inputs or model responses associated with the topic.
        :param description: (experimental) The description of the guardrail.
        :param kms_key: (experimental) A custom KMS key to use for encrypting data. Default: "Your data is encrypted by default with a key that AWS owns and manages for you."
        :param managed_word_list_filters: (experimental) The managed word filters to apply to the guardrail.
        :param pii_filters: (experimental) The PII filters to apply to the guardrail.
        :param regex_filters: (experimental) The regular expression (regex) filters to apply to the guardrail.
        :param word_filters: (experimental) The word filters to apply to the guardrail.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd0388fb62544574fdce33c495357bb3e4ab10d5b21f074fb9b6bce8f730e44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GuardrailProps(
            name=name,
            blocked_input_messaging=blocked_input_messaging,
            blocked_outputs_messaging=blocked_outputs_messaging,
            content_filters=content_filters,
            contextual_grounding_filters=contextual_grounding_filters,
            denied_topics=denied_topics,
            description=description,
            kms_key=kms_key,
            managed_word_list_filters=managed_word_list_filters,
            pii_filters=pii_filters,
            regex_filters=regex_filters,
            word_filters=word_filters,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCfnGuardrail")
    @builtins.classmethod
    def from_cfn_guardrail(
        cls,
        cfn_guardrail: _aws_cdk_aws_bedrock_ceddda9d.CfnGuardrail,
    ) -> IGuardrail:
        '''(experimental) Import a low-level L1 Cfn Guardrail.

        :param cfn_guardrail: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b6644b9376e16a02bd94086914855232ac81bd6c18fc520f8750a4a6a15cff)
            check_type(argname="argument cfn_guardrail", value=cfn_guardrail, expected_type=type_hints["cfn_guardrail"])
        return typing.cast(IGuardrail, jsii.sinvoke(cls, "fromCfnGuardrail", [cfn_guardrail]))

    @jsii.member(jsii_name="fromGuardrailAttributes")
    @builtins.classmethod
    def from_guardrail_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        guardrail_arn: builtins.str,
        guardrail_version: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> IGuardrail:
        '''(experimental) Import a guardrail given its attributes.

        :param scope: -
        :param id: -
        :param guardrail_arn: (experimental) The ARN of the guardrail. At least one of guardrailArn or guardrailId must be defined in order to initialize a guardrail ref.
        :param guardrail_version: (experimental) The version of the guardrail. Default: "DRAFT"
        :param kms_key: (experimental) The KMS key of the guardrail if custom encryption is configured. Default: undefined - Means data is encrypted by default with a AWS-managed key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac4fce8c7366950317863b5de6e9ccb7926adb829fd43d67af111921b6fe60a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = GuardrailAttributes(
            guardrail_arn=guardrail_arn,
            guardrail_version=guardrail_version,
            kms_key=kms_key,
        )

        return typing.cast(IGuardrail, jsii.sinvoke(cls, "fromGuardrailAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addContentFilter")
    def add_content_filter(
        self,
        *,
        input_strength: ContentFilterStrength,
        output_strength: ContentFilterStrength,
        type: ContentFilterType,
    ) -> None:
        '''(experimental) Adds a content filter to the guardrail.

        :param input_strength: (experimental) The strength of the content filter to apply to prompts / user input.
        :param output_strength: (experimental) The strength of the content filter to apply to model responses.
        :param type: (experimental) The type of harmful category that the content filter is applied to.

        :stability: experimental
        '''
        filter = ContentFilter(
            input_strength=input_strength, output_strength=output_strength, type=type
        )

        return typing.cast(None, jsii.invoke(self, "addContentFilter", [filter]))

    @jsii.member(jsii_name="addContextualGroundingFilter")
    def add_contextual_grounding_filter(
        self,
        *,
        threshold: jsii.Number,
        type: ContextualGroundingFilterType,
    ) -> None:
        '''(experimental) Adds a contextual grounding filter to the guardrail.

        :param threshold: (experimental) The threshold for the contextual grounding filter. - ``0`` (blocks nothing) - ``0.99`` (blocks almost everything)
        :param type: (experimental) The type of contextual grounding filter.

        :stability: experimental
        '''
        filter = ContextualGroundingFilter(threshold=threshold, type=type)

        return typing.cast(None, jsii.invoke(self, "addContextualGroundingFilter", [filter]))

    @jsii.member(jsii_name="addDeniedTopicFilter")
    def add_denied_topic_filter(self, filter: Topic) -> None:
        '''(experimental) Adds a denied topic filter to the guardrail.

        :param filter: The denied topic filter to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692157e64cb60b32896dffcc96ff8ad03d713b97963615da507d483b512c865e)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        return typing.cast(None, jsii.invoke(self, "addDeniedTopicFilter", [filter]))

    @jsii.member(jsii_name="addManagedWordListFilter")
    def add_managed_word_list_filter(self, filter: ManagedWordFilterType) -> None:
        '''(experimental) Adds a managed word list filter to the guardrail.

        :param filter: The managed word list filter to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1550b5555345ccffe24c169c8da1cf1ecf54d33d7d26c1a8e1558a75eaa04299)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        return typing.cast(None, jsii.invoke(self, "addManagedWordListFilter", [filter]))

    @jsii.member(jsii_name="addPIIFilter")
    def add_pii_filter(
        self,
        *,
        action: GuardrailAction,
        type: typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648],
    ) -> None:
        '''(experimental) Adds a PII filter to the guardrail.

        :param action: (experimental) The action to take when PII is detected.
        :param type: (experimental) The type of PII to filter.

        :stability: experimental
        '''
        filter = PIIFilter(action=action, type=type)

        return typing.cast(None, jsii.invoke(self, "addPIIFilter", [filter]))

    @jsii.member(jsii_name="addRegexFilter")
    def add_regex_filter(
        self,
        *,
        action: GuardrailAction,
        name: builtins.str,
        pattern: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Adds a regex filter to the guardrail.

        :param action: (experimental) The action to take when a regex match is detected.
        :param name: (experimental) The name of the regex filter.
        :param pattern: (experimental) The regular expression pattern to match.
        :param description: (experimental) The description of the regex filter.

        :stability: experimental
        '''
        filter = RegexFilter(
            action=action, name=name, pattern=pattern, description=description
        )

        return typing.cast(None, jsii.invoke(self, "addRegexFilter", [filter]))

    @jsii.member(jsii_name="addWordFilter")
    def add_word_filter(self, filter: builtins.str) -> None:
        '''(experimental) Adds a word filter to the guardrail.

        :param filter: The word filter to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b12e8cf2ba55857bc5666a519e1ecd649c5d3b91bef66f1347adeefa1aa890)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        return typing.cast(None, jsii.invoke(self, "addWordFilter", [filter]))

    @jsii.member(jsii_name="addWordFilterFromFile")
    def add_word_filter_from_file(self, file_path: builtins.str) -> None:
        '''(experimental) Adds a word filter to the guardrail.

        :param file_path: The location of the word filter file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a0c18147e5b1c9acba7a307ef8418fbd3d0c93d1b437ebddea0c1bf85d022a)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(None, jsii.invoke(self, "addWordFilterFromFile", [file_path]))

    @jsii.member(jsii_name="createVersion")
    def create_version(
        self,
        description: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Create a version for the guardrail.

        :param description: The description of the version.

        :return: The guardrail version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369d6b13c2eb78c16c6cc80e126b921de08cc17315fb782cbeff1efc9a981bfc)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(builtins.str, jsii.invoke(self, "createVersion", [description]))

    @builtins.property
    @jsii.member(jsii_name="contentFilters")
    def content_filters(self) -> typing.List[ContentFilter]:
        '''(experimental) The content filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[ContentFilter], jsii.get(self, "contentFilters"))

    @builtins.property
    @jsii.member(jsii_name="contextualGroundingFilters")
    def contextual_grounding_filters(self) -> typing.List[ContextualGroundingFilter]:
        '''(experimental) The contextual grounding filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[ContextualGroundingFilter], jsii.get(self, "contextualGroundingFilters"))

    @builtins.property
    @jsii.member(jsii_name="deniedTopics")
    def denied_topics(self) -> typing.List[Topic]:
        '''(experimental) The denied topic filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[Topic], jsii.get(self, "deniedTopics"))

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        '''(experimental) The ARN of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailArn"))

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        '''(experimental) The ID of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailId"))

    @builtins.property
    @jsii.member(jsii_name="hash")
    def hash(self) -> builtins.str:
        '''(experimental) The computed hash of the guardrail properties.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "hash"))

    @builtins.property
    @jsii.member(jsii_name="managedWordListFilters")
    def managed_word_list_filters(self) -> typing.List[ManagedWordFilterType]:
        '''(experimental) The managed word list filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[ManagedWordFilterType], jsii.get(self, "managedWordListFilters"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the guardrail.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="piiFilters")
    def pii_filters(self) -> typing.List[PIIFilter]:
        '''(experimental) The PII filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[PIIFilter], jsii.get(self, "piiFilters"))

    @builtins.property
    @jsii.member(jsii_name="regexFilters")
    def regex_filters(self) -> typing.List[RegexFilter]:
        '''(experimental) The regex filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[RegexFilter], jsii.get(self, "regexFilters"))

    @builtins.property
    @jsii.member(jsii_name="wordFilters")
    def word_filters(self) -> typing.List[builtins.str]:
        '''(experimental) The word filters applied by the guardrail.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "wordFilters"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used to encrypt data.

        :default: undefined - "Data is encrypted by default with a key that AWS owns and manages for you"

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))

    @builtins.property
    @jsii.member(jsii_name="guardrailVersion")
    def guardrail_version(self) -> builtins.str:
        '''(experimental) The version of the guardrail.

        By default, this value will always be ``DRAFT`` unless an explicit version is created.
        For an explicit version created, this will usually be a number (e.g. for Version 1 just enter "1")

        :default: - "DRAFT"

        :stability: experimental

        Example::

            "1"
        '''
        return typing.cast(builtins.str, jsii.get(self, "guardrailVersion"))

    @guardrail_version.setter
    def guardrail_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587892fea6ede7e5e05e003ef091d1b5fc420c347657acd1011cba3e2b3ee75d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailVersion", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ActionGroupExecutor",
    "AddAgentAliasProps",
    "Agent",
    "AgentActionGroup",
    "AgentActionGroupProps",
    "AgentAlias",
    "AgentAliasProps",
    "AgentProps",
    "ApiSchema",
    "ApiSchemaConfig",
    "ApplicationInferenceProfile",
    "ApplicationInferenceProfileAttributes",
    "ApplicationInferenceProfileProps",
    "BedrockFoundationModel",
    "BedrockFoundationModelProps",
    "ChunkingStrategy",
    "CommonPromptVariantProps",
    "ConfluenceCrawlingFilters",
    "ConfluenceDataSource",
    "ConfluenceDataSourceAssociationProps",
    "ConfluenceDataSourceAuthType",
    "ConfluenceDataSourceProps",
    "ConfluenceObjectType",
    "ContentFilter",
    "ContentFilterStrength",
    "ContentFilterType",
    "ContextualGroundingFilter",
    "ContextualGroundingFilterType",
    "CrawlingFilters",
    "CrawlingScope",
    "CrossRegionInferenceProfile",
    "CrossRegionInferenceProfileProps",
    "CrossRegionInferenceProfileRegion",
    "CustomTopicProps",
    "CustomTransformation",
    "DataDeletionPolicy",
    "DataSource",
    "DataSourceAssociationProps",
    "DataSourceBase",
    "DataSourceNew",
    "DataSourceType",
    "FoundationModelParsingStategyProps",
    "Guardrail",
    "GuardrailAction",
    "GuardrailAttributes",
    "GuardrailBase",
    "GuardrailConfiguration",
    "GuardrailProps",
    "HierarchicalChunkingProps",
    "IAgentAlias",
    "IDataSource",
    "IGuardrail",
    "IInferenceProfile",
    "IInvokable",
    "IKnowledgeBase",
    "IPrompt",
    "InferenceConfiguration",
    "InferenceProfileBase",
    "InferenceProfileType",
    "InlineApiSchema",
    "KnowledgeBase",
    "KnowledgeBaseAttributes",
    "KnowledgeBaseProps",
    "LambdaCustomTransformationProps",
    "ManagedWordFilterType",
    "PIIFilter",
    "ParserMode",
    "ParsingStategy",
    "Prompt",
    "PromptAttributes",
    "PromptBase",
    "PromptConfiguration",
    "PromptCreationMode",
    "PromptOverrideConfiguration",
    "PromptProps",
    "PromptState",
    "PromptTemplateType",
    "PromptType",
    "PromptVariant",
    "PromptVersion",
    "PromptVersionProps",
    "RegexFilter",
    "S3ApiSchema",
    "S3DataSource",
    "S3DataSourceAssociationProps",
    "S3DataSourceProps",
    "S3Identifier",
    "SalesforceCrawlingFilters",
    "SalesforceDataSource",
    "SalesforceDataSourceAssociationProps",
    "SalesforceDataSourceAuthType",
    "SalesforceDataSourceProps",
    "SalesforceObjectType",
    "SharePointCrawlingFilters",
    "SharePointDataSource",
    "SharePointDataSourceAssociationProps",
    "SharePointDataSourceAuthType",
    "SharePointDataSourceProps",
    "SharePointObjectType",
    "TextPromptVariantProps",
    "Topic",
    "TransformationStep",
    "WebCrawlerDataSource",
    "WebCrawlerDataSourceAssociationProps",
    "WebCrawlerDataSourceProps",
    "pii_type",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import pii_type

def _typecheckingstub__7d2b432e6f12d6f658754ea77c80d65dbc15752f8cc95a3cb553790484127754(
    *,
    custom_control: typing.Optional[builtins.str] = None,
    lambda_: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44b9cf8594977e12593faffc73197189c6b8c803579e66de51dc986e13c8d2a(
    *,
    alias_name: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627af24bb5e1ca4b3ebb82ecbd7a3f01cb1f5177248afdccbc1d0ffab70726de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    foundation_model: IInvokable,
    instruction: builtins.str,
    action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_user_input: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    guardrail_configuration: typing.Optional[typing.Union[GuardrailConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    knowledge_bases: typing.Optional[typing.Sequence[KnowledgeBase]] = None,
    name: typing.Optional[builtins.str] = None,
    prompt_override_configuration: typing.Optional[typing.Union[PromptOverrideConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    should_prepare_agent: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417f1714f331f713e989d70b6417dbb800ceedf7de8245c42ba72cde605b3504(
    action_group: AgentActionGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd86fd4e92aa0f8ee4a2b95a5ad405d539c55043eec94bf739fcc7fc1455d7a4(
    action_groups: typing.Sequence[AgentActionGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c85531cb630c4447db8a8385837856811c9de1f8891137d8afe73a3e03cd62(
    guardrail: IGuardrail,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ea7a1a86c29879ce5949318dae4e0d40df1772332d09e26ac0eebfde38479d(
    knowledge_base: KnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2617bd17ab91665385e57477c5d00b6dfffcd0be05ebe697f1f2d4ff1abc87(
    knowledge_bases: typing.Sequence[KnowledgeBase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362bb8b9135358d9388689544abcd0d0c9e8e45ae46a6dc95b075f20007b92ec(
    value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8a2ba31fca57d8bfcd42f9f0c012e95f4a9a95f52fe008b4777fe99b12b466(
    value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3c9934294b04067f270151310db783e3b9ecde240109d0eed3c691351ae119(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    action_group_name: builtins.str,
    action_group_executor: typing.Optional[typing.Union[ActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]] = None,
    action_group_state: typing.Optional[builtins.str] = None,
    api_schema: typing.Optional[ApiSchema] = None,
    description: typing.Optional[builtins.str] = None,
    function_schema: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    parent_action_group_signature: typing.Optional[builtins.str] = None,
    skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47b674f810daa9a7bde371ad21ea6944cc41d81e91b4c04fca71b8f52c01288(
    *,
    action_group_name: builtins.str,
    action_group_executor: typing.Optional[typing.Union[ActionGroupExecutor, typing.Dict[builtins.str, typing.Any]]] = None,
    action_group_state: typing.Optional[builtins.str] = None,
    api_schema: typing.Optional[ApiSchema] = None,
    description: typing.Optional[builtins.str] = None,
    function_schema: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.FunctionSchemaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    parent_action_group_signature: typing.Optional[builtins.str] = None,
    skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cae66eefc5f4c5599e0686171b63cba4b3c09493c31167b8afaa8bff00da6cc(
    *,
    agent_id: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5254c1c0482eaa66699188ff0467d936350a386bbe823d4ef46c9ba982f91c(
    *,
    foundation_model: IInvokable,
    instruction: builtins.str,
    action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_user_input: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    guardrail_configuration: typing.Optional[typing.Union[GuardrailConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    knowledge_bases: typing.Optional[typing.Sequence[KnowledgeBase]] = None,
    name: typing.Optional[builtins.str] = None,
    prompt_override_configuration: typing.Optional[typing.Union[PromptOverrideConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    should_prepare_agent: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9707019db7cf1339382bbfdc3c35863966765af6485a09c40c302a504ad6876d(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3690bdbded4fc41debce4f674af4ba9794363c793e9f2f52ac27a4069270b3a3(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2792cc1fa0f16747e3820d17877eef4b648c9b158bc65527d5d5c852652166(
    schema: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63a27d3f3e9a3d4c529eccceaa09a947c740c16c6fc454bb2b8aaf2030cee7a(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a607944f95610e7de935c34b4ac51de5be66c1a19adb648c5e285f3ef483bbe7(
    *,
    payload: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[S3Identifier, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ea34e402b2535f2082177ac38775e1034896579d3693772035c4f45ca2d654(
    *,
    inference_profile_arn: builtins.str,
    inference_profile_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9200d651e22ff89688db78ff2bdec2a56b7d93a7d2cb347b49efafe13b581c(
    *,
    inference_profile_name: builtins.str,
    model_source: IInvokable,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1a21a71ca2d85f4b0cb18a5ce955b8c59bb0c4403b3d6f750c90739061d548(
    *,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8c95b7bfa78b1915cee9f049873d2af67238c73953179ae4f9479b54751ebf(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ChunkingConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2752ca933595bdb580dc70b29b9d7fea9196785967ed1f46d44fff8b435477(
    *,
    model: IInvokable,
    variant_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba4b91ab5b955d9d72d8af6f07cdc07ac568ef117419de41dca7871ad32d6b8(
    *,
    object_type: ConfluenceObjectType,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a9140c0049260b2d312c4a80d1b958e9761476560ef6b565d603fce991e815(
    *,
    input_strength: ContentFilterStrength,
    output_strength: ContentFilterStrength,
    type: ContentFilterType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e4288f485be62d723f6fe133287e8c88a90f455b2dec35e5c4095e4ba4cd69(
    *,
    threshold: jsii.Number,
    type: ContextualGroundingFilterType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8789f899b4cf122996f24d6718a644cc2bc6a74788ac86472a28afaba4e33f(
    *,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0779b391b71e321d48d3445f56e45aa413e6050e51f0b7161ca653bdbdd424ab(
    *,
    geo_region: CrossRegionInferenceProfileRegion,
    model: BedrockFoundationModel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afa8690bf8def1351745b409bf75b1c9388f7690948642485ab500130f04eab(
    *,
    definition: builtins.str,
    examples: typing.Sequence[builtins.str],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898a06e70f7f1a8abcf9e8433317e047be3a6f52316351b0d22de8a49154fb6c(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ea7d98a453ed23a6d13ca01317dfc8f56bd010bb3d771347e4898118887260(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.CustomTransformationConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3370fd8035498a3339649efe16f36fa523a3b651e8f4e3f2f7cc83f1af7f2c0(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed85f0ccfdf38b650635f35650195519e14f924af93233cef46e2fd5af61295(
    *,
    parsing_model: IInvokable,
    parsing_prompt: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b140b7ab54824449cb92973af6b36eb6cf61ab0c9257fdf79c5d510e1f60ff(
    *,
    guardrail_arn: builtins.str,
    guardrail_version: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b314d3bddf3fd29e4b1ac5c7c60a1586a89802b85336bbd334b733d34813692(
    *,
    guardrail_id: typing.Optional[builtins.str] = None,
    guardrail_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9d19859a6750c938be49617894f02e36de79c2e5a05a9cb6d6eac91e68d0ea(
    *,
    name: builtins.str,
    blocked_input_messaging: typing.Optional[builtins.str] = None,
    blocked_outputs_messaging: typing.Optional[builtins.str] = None,
    content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    denied_topics: typing.Optional[typing.Sequence[Topic]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    managed_word_list_filters: typing.Optional[typing.Sequence[ManagedWordFilterType]] = None,
    pii_filters: typing.Optional[typing.Sequence[typing.Union[PIIFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex_filters: typing.Optional[typing.Sequence[typing.Union[RegexFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832a5183cc17b41fd7587d09a661c1bc3796489cafca2ed06677f49aa94a717d(
    *,
    max_child_token_size: jsii.Number,
    max_parent_token_size: jsii.Number,
    overlap_tokens: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa86b82cfa7566549e30a1d5b954f23d8c26046bfa7cc0af976bc3c76faa6d16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ba62eccfee612703b786064d7f93d108f9f738d3af81886e81a1528ede7a98(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e05b919b09e86b619e07b4ef364b84ec6c2406d5ea1bca6a3cc89fa68153ec7(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29403dd1f5d63fdfa42529ed12671747a327e8f838334b096c8d604ee0871773(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5960928d16109614db9d88a976b6813f338475a6d9bd76b0987c904ec8128c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befd502c2937a36c672491bd2695d4ec887944e821efe023f2dc44cff4137750(
    *,
    maximum_length: jsii.Number,
    stop_sequences: typing.Sequence[builtins.str],
    temperature: jsii.Number,
    top_k: jsii.Number,
    top_p: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47a0e32efc3020834d43d9c5523a26c5aa4f43e016164f6b0291a29938455be(
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

def _typecheckingstub__43e018efd836bd4c5f724810d840738657b70936f17c80063e2affbcd56a59c5(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeb00812cdcb551f5f688ee295d8f225db974111b8872709130c22fef51592f(
    schema: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429693913d097a23421c6ed72f2363c20d20bbc2d34b374921e37cf4ac8d4157(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a416de40b883dde9bcfa680e69b09d8d8005e4e5d67e2254f09ebebb1b516bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    embeddings_model: BedrockFoundationModel,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    index_name: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vector_field: typing.Optional[builtins.str] = None,
    vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
    vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a654bef0899e37e420b95286d5ec50496932a793679c6d7ba80f00f62f49140(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    execution_role_arn: builtins.str,
    knowledge_base_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca7cf4ff7c6392dfc7cae12d95e046e86c711e76659c1c94e920f30da3a066c(
    agent: Agent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54154af2e4de900e9c2f362f003646235da0359709893f7760cdc5484b06d24(
    *,
    execution_role_arn: builtins.str,
    knowledge_base_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77925ffb8d3d9f229cccdf4b13498db4e9b0c20ca077db0cbe11892e0b36d5f(
    *,
    embeddings_model: BedrockFoundationModel,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    index_name: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vector_field: typing.Optional[builtins.str] = None,
    vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
    vector_store: typing.Optional[typing.Union[_ExistingAmazonAuroraVectorStore_f7ccb819, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762879178fd972fbfc85b23a5a96fe26104fbaf3791957f75d2f92316a91cc7a(
    *,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    s3_bucket_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68aa36b0ead1124a53b5c01582eeed48828bdcc66f87d80565fddd7cc232b72e(
    *,
    action: GuardrailAction,
    type: typing.Union[_General_e613aa3a, _Finance_2430d674, _InformationTechnology_2f99a404, _USASpecific_fa88de63, _CanadaSpecific_f80239d8, _UKSpecific_c9314648],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20f93031aefe7465a4c9b7b8cbf589b874a8c6abd25dd259847d7c99f2c292b(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ParsingConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28412a5d8ac170fe3a64e61ef6ae3f19e2ab4831e4f173b4d9dd49819888b236(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prompt_name: builtins.str,
    default_variant: typing.Optional[PromptVariant] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    variants: typing.Optional[typing.Sequence[PromptVariant]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493e34f209102ea802c9e52bb8d42086b43ec2f571efc98a8d11938b5c35926c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prompt_arn: builtins.str,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    prompt_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfa6edec3745b41e32e786ccd9bf47e56b752a48a1204aefa620f6425599454(
    variant: PromptVariant,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc07b4411e1c17474873d667b41d3c8be2fd1ca6adf765c3090c15136423d774(
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30a1a38bb8b0d638d069ad28bc55cbba27373d5af3489817853bd7e1dc88410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cd66a5ef99991ddde61b718842ff11d482414cb8db73961c80294c681f3502(
    *,
    prompt_arn: builtins.str,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    prompt_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416e615710246dc6fdddab19da69a2adde0b7094028409f64cc9e0c153344b57(
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

def _typecheckingstub__0e6010854ea9d0c593f1187eff0dbb1c606b73ff1be68e89b0d245291215123a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e18fab10acf8af328be25f79340aeb64cc011327127be967f99f267d6b6c92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e333bbbacb815921d7a258c01d4d87250548623e984fd2e844c23791ddeeed(
    *,
    base_prompt_template: builtins.str,
    inference_configuration: typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]],
    prompt_creation_mode: PromptCreationMode,
    prompt_state: PromptState,
    prompt_type: PromptType,
    parser_mode: typing.Optional[ParserMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87069825e4e1447731b12e085f8869b15f2bd52ca2b57df2d0342674371c9580(
    *,
    prompt_configurations: typing.Sequence[typing.Union[PromptConfiguration, typing.Dict[builtins.str, typing.Any]]],
    override_lambda: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed24724d2a2267a3662057e3f507a648a9688b88f50d099de8ac08580da8541(
    *,
    prompt_name: builtins.str,
    default_variant: typing.Optional[PromptVariant] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    variants: typing.Optional[typing.Sequence[PromptVariant]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47858dac9c23ea6d5fe047093eb7c553df8379b538751a421229fcd6090a3d99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfacc76ecbab5bd528fdafd1e6e9ea9558ae6b7f7404301dfde9e66ae3ed865c(
    value: _aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptTemplateConfigurationProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb21a09b18d3af2233c1a12de246544b29d61535df0d28d7f9fb947c1b2668d(
    value: PromptTemplateType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868e405119ddf957e9771368dbe10acb67f0d6f0dc2fe35578128be175024448(
    value: typing.Optional[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptInferenceConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94db700745c23c237379ad0e9208bfa80e98851952c0558325390455e764cd02(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6daa6c79624257e31d9072fc0f20e2f2fc9397635524aa9d067fb36cc7cbbc53(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prompt: Prompt,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49af665e03ae5aea14b78e3aee6d9f0d78722f97c5b289cb5dc844a1cf90815(
    *,
    prompt: Prompt,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a46345c7df17f55020986d90b7ae90f85b55d19822b9b2574bc1ff9831b2d20(
    *,
    action: GuardrailAction,
    name: builtins.str,
    pattern: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c4db74d64f90be972766dae3c6ab8b2ee388726bb4dec1fa1458939ab93a5f(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd50c8c86df0f0a2a5a95b774555d2e2c1d079404953f77717653ea8e3f768a(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937192d503ab06e7d72cb5fca8edb1e0959f925784ef831da357511f9247a9ec(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061fd79f5c6cc3fdad0a0fcccc8c2a083f5deeb769270d6795cc47edeeaecc0b(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8dfefeb74c7ac32b2ae5113a03ce2743b27b34cfa67e342053f0fb90d0050f0(
    *,
    s3_bucket_name: builtins.str,
    s3_object_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ba2de3246503cef86100625445a5010d4594edc17ad5fe4ba4d35b9c066463(
    *,
    object_type: SalesforceObjectType,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9630b4dd940c86a5fa5c47ae28d9a991c3d58e7b9c5432ba828cb2cb213d00(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    endpoint: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dc3117cebd56970b3e49e262627a6133820bc4f98949e5002679327375f4f3(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    endpoint: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc66a84b3c3b22e2879cf44c3edf17abf1ec9c5fb2ebee76fab9d6455ad43867(
    *,
    object_type: SharePointObjectType,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c756d6075defa355f5293064dde03559d8f435bbe0f49037277d8587875a983f(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    domain: builtins.str,
    site_urls: typing.Sequence[builtins.str],
    tenant_id: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cac4a3c20de6d6ae043e36137b1e8760f3e2ae41c065f2a00a80740ce91b38(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    domain: builtins.str,
    site_urls: typing.Sequence[builtins.str],
    tenant_id: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd54adac2df83b870909830e4b8468b5d71a8b9dac001336a6076238c87d3c3d(
    *,
    model: IInvokable,
    variant_name: builtins.str,
    prompt_text: builtins.str,
    prompt_variables: typing.Sequence[builtins.str],
    inference_configuration: typing.Optional[typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnPrompt.PromptModelInferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2d4384933474c1f544b514a9796e0d1ce1eea63851d2a0cbad594f4b1d4830(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    source_urls: typing.Sequence[builtins.str],
    crawling_rate: typing.Optional[jsii.Number] = None,
    crawling_scope: typing.Optional[CrawlingScope] = None,
    filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7f1066a3d54b5b87f6d6542c10949f6480a3b99f641342456db80c76a73a8c(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    source_urls: typing.Sequence[builtins.str],
    crawling_rate: typing.Optional[jsii.Number] = None,
    crawling_scope: typing.Optional[CrawlingScope] = None,
    filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5252a70a25f0e579966376a7e29bb2527a503dda1a1fed24527d3559affff2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent_id: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2021fc1116b8fac10f4b9c0002cd564598aef3381a39953228ad73589ad9b8ba(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    alias_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9295fc37ecfd5ba15c3b4b32661816cc911d30425b0457d6d9e73aab82dc7f58(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    inference_profile_name: builtins.str,
    model_source: IInvokable,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08499f882d34a991b6ff994ce67891aa81aad629aea208a0d363fe07aa2d8b5d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    inference_profile_arn: builtins.str,
    inference_profile_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4756b25b5d6740797b0f293da1e552a81883343f282122c5ff5fadb11eeb76b3(
    cfn_application_inference_profile: _aws_cdk_aws_bedrock_ceddda9d.CfnApplicationInferenceProfile,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7315621579f5e4f7d30f4502f1eeff997dba6cf3f1b3fa9f44a777ac8142ef07(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cee844d1aa1c3aa02aa8a059e448586063f79d5157d71fc62c9035f258d4a04(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a81fd58f8932cf2d8dbd47ee14e3d74d82d0d0245523bd77f54c7a3ebe2a31(
    value: builtins.str,
    *,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e574ebd23afcb2cd940b46095855d515345af1851202b2050e4beae0b61b0797(
    model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModel,
    *,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e6ba9edf9949ffdb893690a97303140d822c69b491d2f36a23884f599a2c01(
    model_id: _aws_cdk_aws_bedrock_ceddda9d.FoundationModelIdentifier,
    *,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_cross_region: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0736a1f1795a1917c49125732e66d2d15e2a25a6b98ac778b58a6ed32dc0df7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da72b0f5ffa432a07504325247590f94f501d9e78a5f834d66e81cfc7e0273f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51a4f667d4d649aafa9ba1bacf7d35b00909caf39e4001910a74850fc7131df(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d3c75724e9e59d672c6ddd0ebf03051252caf48c764eeff6f38c9dbc5d4750(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825542cfcf1e14b8a9bbb49badd630cea24320a1c93de247ce04dade6510a396(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    confluence_url: builtins.str,
    auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14df6d19dffd71a4d3ac18b026e201bc33f4eabb05690ed07f68835b4c37b32(
    *,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    confluence_url: builtins.str,
    auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    knowledge_base: IKnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f472f27b5fa3d24da2ba8a7f195c5e15bd841db7f86b5c297fc541b722f61ac6(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fff43e7d1f97fa19dd910168fe2f7ff3f51b42c62d60e9b28f154c02abdf57(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd33be0b5b715618515a9e14205bd91556c356258bedc630996b5ce10baf76f(
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

def _typecheckingstub__2fd726166f60d1f4704e8a674b6b10ffb8ada8138d51b0fb6cd7ff76f8b98644(
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

def _typecheckingstub__ff20dd4f9a8695235fc5ad3f8044d1b2ab4c308a247f269a7667225817ffa47f(
    props: typing.Union[DataSourceAssociationProps, typing.Dict[builtins.str, typing.Any]],
    *,
    type: builtins.str,
    confluence_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.ConfluenceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.S3DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SalesforceDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    share_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.SharePointDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource.WebDataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd3735db5e3fe2e0ab1bdcc83a66314e304f7420d3c02093aaa2f59d0c028ef(
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

def _typecheckingstub__96bf842a81e21fd1954424599cbfcd6aa0d8d29978b87d0221427d57ac30a99a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3213cd2c4a16450e0a0e2f790d34031e9f57737b870372668dd1026cdbc75470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fbbb836e75c99d63b1aecb8d429a451f727eaf6d350fa9c8a3e73f4932c719(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24d143c738c77349d9a94ed93b630e764b1d3c773aec262ad85df95b6be2129(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    endpoint: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SalesforceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a767e627d5bb3db391024a83258857573d524cc605c090521fdd3266c3253351(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    domain: builtins.str,
    site_urls: typing.Sequence[builtins.str],
    tenant_id: builtins.str,
    filters: typing.Optional[typing.Sequence[typing.Union[SharePointCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e8107d76623400258117634288819beb4c9790e20e7ae484c9025d9dded738(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    source_urls: typing.Sequence[builtins.str],
    crawling_rate: typing.Optional[jsii.Number] = None,
    crawling_scope: typing.Optional[CrawlingScope] = None,
    filters: typing.Optional[typing.Union[CrawlingFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38f8a816fb7d23775a4ed11b9b014cd4c8776d9580e4dae986abe72268d6d4b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base: IKnowledgeBase,
    auth_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    confluence_url: builtins.str,
    auth_type: typing.Optional[ConfluenceDataSourceAuthType] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[ConfluenceCrawlingFilters, typing.Dict[builtins.str, typing.Any]]]] = None,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    custom_transformation: typing.Optional[CustomTransformation] = None,
    data_deletion_policy: typing.Optional[DataDeletionPolicy] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parsing_strategy: typing.Optional[ParsingStategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91bb2023285f784980074a6bd9353d73694f701da8c5417daa958a6ed92e7c61(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    data_source_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd0388fb62544574fdce33c495357bb3e4ab10d5b21f074fb9b6bce8f730e44(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    blocked_input_messaging: typing.Optional[builtins.str] = None,
    blocked_outputs_messaging: typing.Optional[builtins.str] = None,
    content_filters: typing.Optional[typing.Sequence[typing.Union[ContentFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    contextual_grounding_filters: typing.Optional[typing.Sequence[typing.Union[ContextualGroundingFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    denied_topics: typing.Optional[typing.Sequence[Topic]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    managed_word_list_filters: typing.Optional[typing.Sequence[ManagedWordFilterType]] = None,
    pii_filters: typing.Optional[typing.Sequence[typing.Union[PIIFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex_filters: typing.Optional[typing.Sequence[typing.Union[RegexFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    word_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b6644b9376e16a02bd94086914855232ac81bd6c18fc520f8750a4a6a15cff(
    cfn_guardrail: _aws_cdk_aws_bedrock_ceddda9d.CfnGuardrail,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac4fce8c7366950317863b5de6e9ccb7926adb829fd43d67af111921b6fe60a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    guardrail_arn: builtins.str,
    guardrail_version: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692157e64cb60b32896dffcc96ff8ad03d713b97963615da507d483b512c865e(
    filter: Topic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1550b5555345ccffe24c169c8da1cf1ecf54d33d7d26c1a8e1558a75eaa04299(
    filter: ManagedWordFilterType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b12e8cf2ba55857bc5666a519e1ecd649c5d3b91bef66f1347adeefa1aa890(
    filter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a0c18147e5b1c9acba7a307ef8418fbd3d0c93d1b437ebddea0c1bf85d022a(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369d6b13c2eb78c16c6cc80e126b921de08cc17315fb782cbeff1efc9a981bfc(
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587892fea6ede7e5e05e003ef091d1b5fc420c347657acd1011cba3e2b3ee75d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
