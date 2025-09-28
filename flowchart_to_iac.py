# Install dependencies (run once)
apt-get install -y tesseract-ocr
pip install pytesseract opencv-python

# Upload your flowchart image (run and select file)
from google.colab import files
uploaded = files.upload()

import cv2
import pytesseract
from google.colab.patches import cv2_imshow

def extract_text(image_path):
    image = cv2.imread(image_path)
    print("Flowchart image preview:")
    cv2_imshow(image)  # Visual confirmation
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 3)
    text = pytesseract.image_to_string(thresh, config='--oem 3 --psm 6')
    return text

def detect_resources(text):
    keywords = {
        'VPC': 'aws_vpc',
        'EC2': 'aws_instance',
        'S3': 'aws_s3_bucket',
        'LOAD BALANCER': 'aws_elb',
        'RDS': 'aws_db_instance',
        'LAMBDA': 'aws_lambda_function',
        'BUCKET': 'aws_s3_bucket'
    }
    found_resources = []
    for key, val in keywords.items():
        if key in text.upper():
            found_resources.append(val)
    return found_resources

def generate_terraform_code(resources):
    blocks = []
    for r in resources:
        if r == 'aws_vpc':
            blocks.append('resource "aws_vpc" "main" {\n  cidr_block = "10.0.0.0/16"\n}')
        elif r == 'aws_instance':
            blocks.append('resource "aws_instance" "web" {\n  ami = "ami-0abcdef1234567890"\n  instance_type = "t2.micro"\n}')
        elif r == 'aws_s3_bucket':
            blocks.append('resource "aws_s3_bucket" "bucket" {\n  bucket = "example-bucket-name"\n}')
        elif r == 'aws_elb':
            blocks.append('resource "aws_elb" "lb" {\n  name = "example-load-balancer"\n  availability_zones = ["us-west-2a"]\n}')
        elif r == 'aws_db_instance':
            blocks.append('resource "aws_db_instance" "default" {\n  engine = "mysql"\n  instance_class = "db.t2.micro"\n  allocated_storage = 20\n  name = "mydb"\n  username = "foo"\n  password = "bar"\n  parameter_group_name = "default.mysql5.7"\n}')
        elif r == 'aws_lambda_function':
            blocks.append('resource "aws_lambda_function" "example" {\n  function_name = "example_lambda"\n  runtime = "python3.8"\n  role = aws_iam_role.iam_for_lambda.arn\n  handler = "lambda_function.lambda_handler"\n  filename = "lambda_function_payload.zip"\n}')
    return "\n\n".join(blocks)

# Main execution
image_filename = list(uploaded.keys())[0]
print(f"Processing image: {image_filename}")

ocr_text = extract_text(image_filename)
print("\nOCR Extracted Text:\n", ocr_text.strip())

resources_detected = detect_resources(ocr_text)
print("\nDetected Cloud Resources:")
if resources_detected:
    for res in resources_detected:
        print(f"- {res}")
else:
    print("None detected. Diagram likely has no standard cloud infrastructure components.")

print("\nGenerated Terraform IaC Snippets:\n")
terraform_code = generate_terraform_code(resources_detected)
if terraform_code:
    print(terraform_code)
else:
    print("No IaC generated due to unrecognized or missing cloud components.")
