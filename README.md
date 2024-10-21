# ParseNimbus: Cloud-based Document Processing System

ParseNimbus is a cloud-based document processing solution that not only manages various document types like invoices and contracts but also automates their review and categorization based on departmental needs. The primary purpose of the project is to streamline the document handling process by leveraging AWS services and Python automation. Once a document is uploaded, the system processes it and extracts key information relevant to the respective department. 

For example, when handling documents for the Finance department, the system focuses on extracting crucial data such as the amount to be paid, the vendor’s account number, and the vendor’s name. All other details are secondary. This precise focus ensures that the relevant information is quickly identified and saved in the cloud, enhancing the efficiency of the document review process.

The infrastructure for ParseNimbus is set up using Terraform scripts, allowing for a seamless, automated, and scalable cloud environment. By using services like Amazon S3 for secure storage, EC2 for compute resources, Textract for data extraction, and SQS for asynchronous communication, ParseNimbus ensures an efficient and organized approach to document management. The combination of these services, along with Python automation, enables the application to be adaptable to different document types and departmental needs, providing an effective solution for businesses that require rapid and accurate document processing.

## Key Features of ParseNimbus


### <strong>End-to-End Automation of Document Processing</strong> 

ParseNimbus automates the entire document workflow, from uploading to processing, extracting key data, and saving the results. For example, the Finance department focuses on essential information like the vendor's name, account number, and payment details, while the system handles everything else automatically.

This boosts operational efficiency by eliminating manual steps and reducing human error. It also allows employees to focus on critical tasks while the system processes documents in the background.

### <strong>Department-Specific Data Extraction</strong> 

ParseNimbus tailors document processing for each department. For instance, the Finance department extracts payment-related data, while other departments can configure their own data needs, such as legal clauses for contracts.

This customization ensures that each department receives only relevant information, reducing data overload and improving accuracy across different workflows.

### <strong>Scalable Processing</strong> 

ParseNimbus can easily scale to handle increasing document volumes, whether processing a single document or thousands. The system adapts to demand without affecting performance.

This scalability ensures the system remains efficient as your organization grows, handling more documents without additional configuration.

ParseNimbus can easily scale to handle increasing document volumes, whether processing a single document or thousands. The system adapts to demand without affecting performance.


### <strong>Cloud Integration</strong> 

With tight integration of cloud services like S3, EC2, and Textract, ParseNimbus ensures reliable document storage, secure credential management, and on-demand computing resources for high availability and performance.

This cloud-native approach leverages scalable resources and ensures that all document processing is secure, reliable, and adaptable to changing needs.

### <strong>Flexible and Extensible</strong> 

ParseNimbus is built for easy customization. As business needs change, new workflows or document types can be added without disrupting existing processes.

This flexibility ensures the system can evolve with the business, allowing for future expansions and integrations with minimal effort.

### <strong>Efficient Document Retrieval</strong> 

Processed documents are organized in department-specific folders for easy retrieval. Users can quickly access processed data (e.g., finance_data.json) for review and download.

This organization simplifies the review process and improves productivity by ensuring that processed data is readily accessible.

## Command Execution

After the whole infrastructure of aws is set-up using the `main.tf` script, here are the commands that I have executed one-by-one for managing and using the services.

### ssh into the aws ec2 instance

`ssh -i myways_ec2_keypair.pem ubuntu@<public_ip_of_ubuntu_instance>`

### Install python3 and Pip

`sudo apt install python3 python3-pip`

### Set Up Python Virtual Environment

`python3 -m venv myenv`
`source myenv/bin/activate`

### Install the aws cli on the ec2 instance

`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`

* ##### Unzip the installer

`sudo apt-get install unzip -y`

* ##### Run the AWS CLI installer

`sudo ./aws/install`

* ##### Verify the Installation

`aws --version`

### Configure AWS CLI

`aws configure`
###### Enter your AWS Access Key ID, AWS Secret Access Key, Default region, and Default output format when prompted,using the IAM role and in the Users section, generate the access keys

### Activate Virtual Environment

`source myenv/bin/activate`

### Install dependencies like boto3 inside the python virtual environment

`pip install boto3`

### Make python script named `document_processing.py`

`vim document_processing.py`

######	After creating the .py script, paste the code provided in the github repository.

### Upload the pdf file to the s3 bucket

`aws s3 cp SampleInvoice.pdf s3://myways-s3-bucket-2184/`

### Send message to the SQS Queue

`aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/3240XXXXX890/document-processing-queue_2184 \ --message-body "{\"bucket_name\":\"myways-s3-bucket-2184\", \"file_key\":\"SampleInvoice.pdf\"}" --region us-east-1`

### Run the Document Processing Script

`python3 document_processing.py`

### Verify the processed data in the s3 bucket

`aws s3 ls s3://myways-s3-bucket-2184/processed/finance/`

### Download the Processed Data

`aws s3 cp s3://myways-s3-bucket-2184/processed/finance/finance_data.json`

### View the Processed Data

`cat finance_data.json`
## Execution Flow

* #### Document Upload
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Document Upload: A document (e.g., `SampleInvoice.pdf`) is uploaded to the S3 bucket (`myways-s3-bucket-2184`).

* #### SQS Message sent
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A message is being sent to the SQS queue document-processing-queue_2184 with a bucket and file key of the uploaded document.

* #### Transaction processing:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The `document_processing.py` script runs on an EC2 instance.
It retrieves the SQS message, downloads a document from an S3 bucket, and then processes it through AWS Textract or similar tools.
The extracted data is converted into department-specific outputs, such as the finance department seeing amount and vendor information.

* #### Save Processed Data
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The processed data (e.g., `finance_data.json`) are stored back in a different location in the S3 bucket (`processed/finance/`).

* #### Deletion of SQS Message
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The SQS message is deleted after processing the document, hence complete work task.

## Results

* #### SSH into the ec2 instance locally
![ssh](Images/ssh.png)

* #### Activating the python virtual environment.
![python virtual environment](Images/Activating%20the%20python%20virtual%20environment.png)

* #### Uploading the file to the s3 bucket.
![Upload to s3 bucket](Images/Upload%20the%20file%20to%20s3%20bucket.png)

* #### Sending message to SQS Queue.
![sqs queue](Images/sqs%20message.png)

* #### Run the Document Processing Script.
![Run the Document Processing Script](Images/Run%20the%20Document%20Processing%20Script.png)

* #### Verifying the Processed Data in S3.
![Verify the Processed Data in S3](Images/Verify%20the%20Processed%20Data%20in%20S3.png)

* #### Downloading the Processed Data for Review.
![Downloading the Processed Data for Review](Images/Download%20the%20Processed%20Data%20for%20Review.png)

* ####  Viewing the Processed Data.
![ View the Processed Data](Images/View%20the%20processed%20data.png)

# Part 2: Application Deployment on Kubernetes Using Helm
## Application: Apache

I am deploying an Apache server on a Kubernetes cluster, monitoring it using Prometheus and Grafana, and configuring dashboards to visualize performance data.

## Set Up Kubernetes Environment (Minikube)

Note: Already installed minikube and kubectl.

Start minikube using the command: 
`minikube start`

Verify setup by running the command:
`kubectl get nodes`

## Containerizing the Apache Server using Helm

Create helm chart: `helm create apache-chart`

Modify the `values.yaml` file as below

![values.yaml](Images/resource_valueYAML.png)&nbsp;&nbsp;&nbsp;&nbsp;
![values.yaml](Images/valueImage.png)

* Deploy the chart using Helm 
`helm upgrade --install apache-app ./apache-chart`

* Check that the service is running 
`kubectl get services`

* Retrieve the NodePort assigned to the Apache Service 
`kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services apache-app-apache-chart`

* Retrieve the IP address of the node 
`kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}"`

* Using port forwarding to access locally
`kubectl port-forward svc/apache-app-apache-chart 9090:80`

* Verify the Apache Deployment by typing the below link in the browser
`http://localhost:9090`

After this you see the default " It works! " from Apache, same as in the below image\
![apacheBrowser.yaml](Images/apacheBrowser.png)

## Setting up the monitoring with Prometheus

Install Prometheus with the below commands

* `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
* `helm repo update`
* `helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace`

Check if the Prometheus Pods are running

* `kubectl get pods -n monitoring`

The terminal window will be like below
![Prometheus.yaml](Images/PromeMonitoring.png)

After that, access the Prometheus UI using the below command

* `kubectl port-forward -n monitoring svc/prometheus-server 9091:80`

The terminal window will look like below

![Promui.yaml](Images/PromUI.png)

Now you can visit the Prometheus dashboard using 
`http://localhost:9091`

## Setting up visualization using Grafana

Add the Grafana Helm Repository

* `helm repo add grafana https://grafana.github.io/helm-charts`
* `helm repo update`

Install Grafana using helm
`helm install grafana grafana/grafana --namespace monitoring`

Check that Grafana is working
`kubectl get pods -n monitoring`

The terminal would look like this
![Grafana.yaml](Images/Grafana.png)

Now forward traffic from your local machine's port 3000 to the Grafana service's port 80 inside your Kubernetes cluster, enabling you to access the Grafana dashboard locally 
`kubectl port-forward -n monitoring svc/grafana 3000:80`

The terminal would look like below
![GrafanaForward.yaml](Images/GrafanaForwarding.png)

Now you can access Grafana using
`http://localhost:3000`

The username will be `admin`, the password you can get by running this command on powershell `kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | %{[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_))}`

## Add Prometheus as a Data Source

In Grafana go to `Dashboard` and there click on `Add Visualization`, then further make sure the `Data source` at the bottom is set as `prometheus`

Select the metric as `up` and then click on `Run queries` and click `Apply` at the top right corner to save the panel to dashboard. 

## Dashboard Of Prometheus After successfull execution

Write `up` in the query and click `Execute`
![PDash.yaml](Images/PrometheusDashboard.png)

## Dashboard Of Grafana After successfull execution

![GraDash.yaml](Images/GrafanaDash.png)