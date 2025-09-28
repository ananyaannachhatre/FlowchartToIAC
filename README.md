# Flowchart to Terraform IaC Generator

This project converts a flowchart image into basic Terraform Infrastructure-as-Code (IaC) snippets.

## How It Works

1. **OCR Extraction**  
   - The user uploads a flowchart image.
   - The script uses **Tesseract OCR** and **OpenCV** to read and extract text from the image.

2. **Cloud Resource Detection**  
   - Extracted text is scanned for keywords like `VPC`, `EC2`, `S3`, `RDS`, `LAMBDA`, etc.
   - Each detected keyword is mapped to its corresponding Terraform resource type.

3. **Terraform Code Generation**  
   - Based on detected components, predefined Terraform resource blocks are generated.
   - Example:
     - `VPC` → `aws_vpc`
     - `EC2` → `aws_instance`
     - `S3` or `BUCKET` → `aws_s3_bucket`

## Workflow Summary

Upload Flowchart Image → OCR Text Extraction → Detect Cloud Components → Generate Terraform Snippets

---

This is an initial prototype and can be expanded to support more complex diagrams and cloud providers.
