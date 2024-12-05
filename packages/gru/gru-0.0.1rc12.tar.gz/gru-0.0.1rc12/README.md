# Overview

Canso is a Managed Data and Feature Platform for operationalizing Machine Learning initiatives. The goal of Canso is to enable ML Teams (Data Engineers, Data Scientists, ML Engineers) to define their requirements in a declarative and standardized manner via a concise [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) without having to focus on writing custom code for Features, DAGs etc and managing infrastructure. This enables ML teams to 
- Iterate fast i.e. move from development to production in hours/days as opposed to weeks
- Promote Reliability i.e build standardized ML pipelines


Canso's core focus is on user experience and speed of iteration, without compromising on reliability -

- Define data sources where features can be created and computed.
- Specify data sinks where processed data is stored after a successful ML pipeline run.
- Define Machine Learning features in a standardized manner on top of existing Datasources and deploy them. These features can be used while Model training as well as for Model inference. Canso supports Raw, Derived and Streaming features currently.
- Register and deploy features to execute the ML pipeline.


# User Experience


# Getting Started

### 1. Install Gru Package
For installing gru package will need to username and PAT as password.
- A Personal Access Token (PAT) is a kind of key that authenticates a user across all applications they have access to.

```python
pip3 install git+https://github.com/Yugen-ai/gru.git
```


### 2. Create Yugen client

```python
yugen_client = YugenClient(access_token=access_token, config_path="./gru/config.yaml")
```


### 3. Define a s3 Data Source

```python
s3_data_source_obj = S3DataSource(
    name="survey_telemetry_data",
    bucket="internal-ml-demos",
    base_key="recsys/survey-data/phase3_3/survey-telemetry/",
    varying_key_suffix_format="%Y-%m-%d/%H%M",
    varying_key_suffix_freq="30min",
    time_offset=0,
    description="random desc of data source",
    owners=["xyz"],
    created_at=datetime.now(),
    file_type=CSVType(header=True),
    schema=schema_obj,
    event_timestamp_field="time",
    event_timestamp_format="yyyy-MM-dd HH:mm:ssXXX",
)
```


### 4. Register Data Source

```python
yugen_client.register(s3_data_source_obj)
```

### 5. Define a Raw Feature

```python
raw_feature = RawFeature(
    name="avg_order_val_3_days",
    description="Avg order per cusotmer for last 3 days",
    data_type=DataType.FLOAT,
    source_name=["survey_telemetry_data"],
    staging_sink=["s3_sink_ml_yugen_internal"],
    online_sink=["elasticache-redis-yugen"],
    owners=["vanshika@yugen.ai"],
    entity=["test"],
    feature_logic=FeatureLogic(
        field=["ad_id"],
        filter="""ad_id is NOT NULL""",
        transform=SlidingWindowAggregation(
            function="avg",
            partition_by="provider",
            order_by="cpi",
            # rangeBetween= {"frame_start": 1, "frame_end": 6},
            rowsBetween={"frame_start": 1, "frame_end": 2},
        ),
        time_window="3d",
        groupby_keys=["project_id"],
        timestamp_field="time",
        timestamp_format="yyyy-MM-dd HH:mm:ssXXX",
    ),
    online=True,
    offline=True,
    schedule="0 0 * * *",
    active=True,
    start_time=datetime(2023, 4, 1, 0, 0, 0),
)
```

### 6. Register Raw Feature

```python
yugen_client.register(raw_feature)
```


### 7. Dry run Raw Feature

```python
yugen_client.dry_run("avg_order_val_3_days", entity_type=EntityType.RAW_FEATURE, start_date=datetime(2023, 4, 1, 0, 0, 0), end_date=datetime(2023, 4, 2, 0, 0, 0))
```


### 8. Deploy Raw Feature

```python
yugen_client.deploy("avg_order_val_3_days", EntityType.RAW_FEATURE)
```

### 9. Define a Derived Feature

```python
derived_feature = DerivedFeature(
    name="total_purchases",
    description="Total purchase amount for the store",
    staging_sink=["s3_sink_ml_yugen_internal"],
    online_sink=["elasticache-redis-yugen"],
    data_type=DataType.FLOAT,
    owners=["all-ds@company.com"],
    schedule="0 0 * * *",
    entity=["CASE WHEN cpi> 0.5 THEN 10 ELSE 0 END"],
    online=False,
    offline=True,
    transform=multiply("avg_orders_last_3_days", "number_users"),
    start_time=datetime(2022, 8, 26, 0, 0, 0),
)
```

### 10. Register Derived Feature

```python
yugen_client.register(derived_feature)
```

### 11. Dry run Derived Feature

```python
yugen_client.dry_run("total_purchases", entity_type=EntityType.DERIVED_FEATURE, start_date=datetime(2022, 8, 26, 0, 0, 0), end_date=datetime(2022, 8, 27, 0, 0, 0))
```

### 12. Deploy Derived Feature

```python
yugen_client.deploy("total_purchases", EntityType.DERIVED_FEATURE)
```

### 13. Define Pre-Processing Transform

```python
ppt = PreProcessingTransform(
    transform_name="user_avg_spend_transform_final_testing_for_dry_run",
    description="test preprocess transform",
    data_source_names=["marketing_survey_data_info", "data_telemetry_info"],
    data_source_lookback_config={
        "marketing_survey_data_info": "1d",
        "data_telemetry_info": "1d",
    },
    staging_sink=["s3_sink_ml_yugen_internal"],
    logic=sql_logic,
    schedule="0 0 * * *",
    output_schema=schema_obj,
    owners=["john.doe@company.ai"],
    active=True,
    transform_start_time=datetime(2022, 8, 27, 0, 0, 0),
)
```

### 14. Register Pre-Processing Transform

```python
yugen_client.register(ppt)
```

### 15. Dry run Pre-Processing Transform

```python
yugen_client.dry_run(
    "user_avg_spend_transform_final_testing_for_dry_run",
    entity_type=EntityType.PRE_PROCESSING_TRANSFORM,
    start_date=datetime(2022, 8, 27, 0, 0, 0),
    end_date=datetime(2022, 8, 28, 0, 0, 0),
)
```

### 16. Deploy Pre-Processing Transform

```python
yugen_client.deploy(
    "user_avg_spend_transform_final_testing_for_dry_run", EntityType.PRE_PROCESSING_TRANSFORM
)
```

### 17. Define Training Data 

```python
training_run = TrainingData(
    name="example_training_run",
    description="A sample run to generate training data",
    historical_data_source="user_events",
    entities=["project_id","cpi"],
    features=["raw_for_testing_gtd","raw_for_testing_gtd_for_telemetry","raw_for_testing_gtd_for_survey","raw_for_testing_gtd_for_user_events","raw_for_testing_gtd_for_weather_forecats"],
    ttl=5,
    owners=["john.doe@company.ai"],
)
```

### 18. Register Training Data

```python
yugen_client.register(training_run)
```

### 19. Deploy Training Data

```python
yugen_client.deploy("example_training_run", EntityType.TRAINING_DATA)
```

### 20. Define Infrastructure Data

```python
register_infrastructure = RegisterInfrastructure(
    client_id="platform-release-1",
    cloud_provider="aws",
    cluster_name="yugen-platform-v2",
    region="ap-south-1",
    subnet_ids=["subnet-4b250507", "subnet-fac53691", "subnet-86cea5fd"],
    resource_node_group_instance_types={
        "instance_types": {"node_group_1": "t3.medium", "node_group_2": "t3.large",}
    },
    resource_node_group_scaling_config={
        "scaling_config": {
            "node_group_1": {"max_size": 6, "min_size": 2, "desired_size": 3},
            "node_group_2": {"max_size": 6, "min_size": 2, "desired_size": 3,},
        }
    },
    admins=[
        "arn:aws:iam::832344679060:user/ashish.prajapati@yugen.ai",
        "arn:aws:iam::832344679060:user/john.doe@company.ai",
        "arn:aws:iam::832344679060:user/sandeep.mishra@yugen.ai",
        "arn:aws:iam::832344679060:user/shaktimaan@yugen.ai",
        "arn:aws:iam::832344679060:user/shashank.mishra@yugen.ai",
        "arn:aws:iam::832344679060:user/soumanta@yugen.ai",
        "arn:aws:iam::832344679060:user/vanshika.agrawal@yugen.ai",
    ],
    airflow_users={
        "admin": {
            "username": "admin",
            "password": "yugen@123",
            "email": "admin@example.com",
            "firstName": "admin",
            "lastName": "admin",
        }
    },
    slack_details={
        "failure_alerts": {
            "host_url": "https://hooks.slack.com/services",
            "host_password": "/TSRAELEL9/B04Q09X9W75/PhfxMaFBE81ZBXjeAktTTIyN",
        },
        "notifications": {
            "host_url": "https://hooks.slack.com/services",
            "host_password": "/TSRAELEL9/B04Q09X9W75/PhfxMaFBE81ZBXjeAktTTIyN",
        },
    },
    created_at =datetime(2023, 4, 28, 0, 0, 0),
    
)


```

### 21. Register Infrastructure Data

```python
yugen_client.register(register_infrastructure)
```

### 22. Deploy Infrastructure Data

```python
yugen_client.deploy("platform-release-1_yugen-platform-v2_2023-04-28 00:00:00", EntityType.INFRASTRUCTURE)
```

# Roadmap

## DataSources

### Batch
- [x] S3
- [ ] GCS
- [ ] RedShift
- [ ] BigQuery
- [ ] Snowflake

### Streaming
- [x] Kafka

## DataSinks

### Online DataSinks

Online data sinks offers real-time data storage for fast write operations. 
It ensures low-latency access to data, 
making it suitable for applications requiring immediate data retrieval and updates, 
such as retrieval for ML predictions.
Currently, Canso supports Redis cache for storing data online.

### Offline DataSinks

Offline data sinks provides durable and scalable storage for batch-processed and historical data. 
It supports large volumes of data with high reliability, 
making it ideal for data warehousing and archival storage. 
Currently, Canso supports S3 storing data offline.

### Batch
- [x] S3
- [x] Redis
- [ ] RedShift
- [ ] DynamoDB

### Streaming
- [ ] Kafka

## Online Feature Store

- [x] Elasticache for Redis (AWS)
- [ ] Memorystore for Redis (GCP)
- [ ] DynamoDB
- [ ] Bigtable