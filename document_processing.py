import boto3
import json

# Initializing the AWS clients for S3, SQS, and Textract using boto3
# Specifying the 'us-east-1' region since all the services are in the same region
s3_client = boto3.client('s3', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')
textract_client = boto3.client('textract', region_name='us-east-1')

# Defining the SQS queue URL where document processing requests are sent
queue_url = 'https://sqs.us-east-1.amazonaws.com/3240XXXXX4890/document-processing-queue_2184'

# Defining the S3 bucket name where documents are stored
bucket_name = 'parsenimbus-s3-bucket-2184'


# This function retrieves the document (PDF, image, etc.) from an Amazon S3 bucket.
def retrieve_document_from_s3(bucket_name, file_key):
    """Retrieve the document from S3."""

    # Fetching the document from the specified S3 bucket and file (file name)
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    
    # Read and return the document's binary content
    return response['Body'].read()


# This function extracts text from the document using AWS Textract.
def extract_text_from_document(document_bytes):
    """Extract text from the document using AWS Textract."""

    # Using AWS Textract's detect_document_text API to extract text from the document
    response = textract_client.detect_document_text(
        Document={'Bytes': document_bytes}
    )

    # Initialize an empty list to store the extracted lines of text
    text_blocks = []

    # Iterating through the response's blocks and extract only lines of text
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_blocks.append(block['Text'])

    # Return the list of extracted text blocks
    return text_blocks


# This function extracts finance-specific information from the text lines returned by Textract.
def extract_finance_data(textract_response):
    """Extract finance-specific data: Vendor Name, Account Number, Total Amount."""

    # Initialize a dictionary to store the extracted finance-related data
    finance_data = {
        'Vendor Name': None,
        'Account Number': None,
        'Total Amount': None
    }

    # Loop through the lines of text and extract finance-related details
    for line in textract_response:
        # Extracting the vendor name if the line contains 'Vendor Name'
        if 'Vendor Name' in line:
            finance_data['Vendor Name'] = line.split(':')[-1].strip()

        # Extracting the account number if the line contains 'Account Number'
        if 'Account Number' in line:
            finance_data['Account Number'] = line.split(':')[-1].strip()

        # Extracting the total amount if the line contains 'Total Amount' or 'Amount Due'
        if 'Total Amount' in line or 'Amount Due' in line:
            finance_data['Total Amount'] = line.split(':')[-1].strip()
    
    # Returning the extracted finance-related data
    return finance_data

# This function saves the extracted finance data back to the S3 bucket as a JSON file.
def save_to_s3(bucket_name, file_key, data):
    """Save extracted data to S3."""

    # Convert the data dictionary to a JSON string and upload it to the specified S3 bucket
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(data))
    
    # Print confirmation that the data has been successfully saved    
    print(f"Data saved to {file_key}")

#This is the main function that continuously polls the SQS queue, processes incoming messages, and triggers document processing.
def process_document(queue_url):
    """Poll the SQS queue and process the document."""
    while True:
        # Fetch up to 1 message from the SQS queue (long polling with 10 seconds wait time)
        response = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)

        # If there are any messages in the queue
        if 'Messages' in response:
            # Loop through each message (here we expect only one message)
            for message in response['Messages']:

                # Parse the message body as a JSON object
                body = json.loads(message['Body'])

                # Extract the S3 bucket name and file key from the message
                bucket_name = body['bucket_name']
                file_key = body['file_key']

                # Retrieve the document from the S3 bucket
                document = retrieve_document_from_s3(bucket_name, file_key)

                # Use Textract to extract text from the document
                textract_response = extract_text_from_document(document)
                
                # Extract finance-related data (like Vendor Name, Account Number, Total Amount) 
                finance_data = extract_finance_data(textract_response)
                
                # Save the extracted finance data as a JSON file in the 'processed/finance/' folder in S3 
                save_to_s3(bucket_name, f'processed/finance/finance_data.json', finance_data)
                
                # Delete the processed message from the SQS queue to prevent reprocessing
                sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

                # Print confirmation that the message has been processed and deleted
                print("Message processed and deleted from queue.")
        else:
            # If no messages are available in the queue, print a message and continue polling
            print("No messages in the queue.")

# Start the document processing by polling the SQS queue for messages
process_document(queue_url)