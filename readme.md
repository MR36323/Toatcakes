
# Toatcakes ETL 

ETL pipeline, written in Python and Terraform, hosted on AWS, for deriving business analytics for a simulated tote bag business. 

## Context

For our final project at [Northcoders](https://www.northcoders.com/), we were tasked with implementing and testing an ETL pipeline, for a simulated tote bag business. The pipeline extracts data from an OLTP database, before transforming and placing it into a remote OLAP Postgres database. The business required that the pipeline be hosted on AWS, and that changes to select parts of the OLTP database be reflected in the OLAP within 30 minutes. 

Some key features of the project:

- Lambda Functions: The first, for extracting data from the OLTP, if there had been a relevant change. The second, for reformating the extracted data into a star schema. The third, for placing the transformed data into the OLAP, taking the form of an Amazon RDS Postgres database. 
- S3 Buckets: The Extract Lambda and Transform Lambda functions store their data in seperate S3 Buckets. The data is treated as immutable.
- Cloudwatch: Alerts are sent to an email address should any Lambda Function error.
- Step Functions and Eventbridge: The Lambda Functions are strung together by AWS Step functions, which is trigger every 20 minutes by the Eventbridge.

## Deployment

1. Install the latest version of [Python](https://www.python.org/downloads/). 

2. Configure AWS Secrets Manager to hold two secrets: credentials for the Totesys database, and credentials for the Postgres Data Warehouse. These need to be referenced as ``prod/totesys`` and ``prod/warehouse``. Do this on the AWS console.

3. For deploying AWS infrastructure, you will need to [install Docker](https://docs.docker.com/engine/install/). If using Docker app, this must be running when you apply Terraform.

4. Some tests will skip if you do not have a active connection to appropriate test Postgres database. Be sure to activate this if needed. The relevant tests are in ``tests/test_load_data_to_warehouse.py``

5. Run the Makefile like so: 

```bash
  make requirements
  make dev-setup
  make run-checks
```

6. [Install Terraform](https://developer.hashicorp.com/terraform/install)

7. Run Terraform. From repo root:

```bash
  cd terraform
  terraform init 
  terraform plan
  terraform apply
```

Terraform will prompt you for an email address. This is for Cloudwatch alerts, but you can input a dummy value, if you do not want them. 

8. Check all is well by logging into the AWS console. Things to check include: 

- Does Eventbridge trigger every 20 minutes?
- Are Step Functions working?
- Is data being placed in S3 buckets?

## Authors

- [@Mburns1212](https://www.github.com/Mburns1212)
- [@beth-suffield](https://www.github.com/beth-suffield)
- [@lathiuu](https://www.github.com/lathiuu)
- [@rajnijain19](https://www.github.com/rajnijain19)
- [@MR36323](https://www.github.com/MR36323)


## Acknowledgements

 - [Northcoders](https://www.northcoders.com/)
