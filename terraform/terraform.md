# Steps to provision Google infrastructure

- [Steps to provision Google infrastructure](#steps-to-provision-google-infrastructure)
  - [Prerequisities](#prerequisities)
  - [Install terraform](#install-terraform)
  - [Provision Google infrastructure](#provision-google-infrastructure)
  - [Verify provisioned infrastructure](#verify-provisioned-infrastructure)

## Prerequisities
1. Create Google cloud account for new user otherwise use your existing account
2. Create a new Project
   https://console.cloud.google.com
   https://console.cloud.google.com/projectselector2/home/dashboard?organizationId=0&supportedpurview=project
Choose a Project ID to use througout the project
![](images/project.png)

3. Enable APIs
   From Navigation menu
   Go to Compute Engine and enable API
   Go to Bigquery and enable API
4. [Download](https://git-scm.com/downloads) and install Git Bash for windows (Assuming you are working from a windows laptop) otherwise use the operating system compatible to your machine
5. Generate ssh key
   Open Git Bash
   ```
   mkdir .ssh
   ssh-keygen -t rsa -f ~/.ssh/gcp -C <your name> -b 2048
   ```
   Add the public key generated, gcp.pub, in this case to your google cloud account
   From Navigation menu, go to compute engine->Settings->metadata->SSH Keys->ADD SSH KEY
   Add the contents of the public key to the ssh key field
   ![](images/ssh.png)
6. Create service account
   From Navigation menu, go to IAM and Admin->service accounts->create service account
   ![](images/service_account1.png)
   ![](images/service_account2.png)
   Compute admin, Storage admin, and bigquery admin roles have been assigned to the service account. You may give more granular roles.
   Go to manage keys and add json key
   ![](images/service_account3.png)
   ![](images/service_account4.png)  
   Copy the contents of the json key to terraform/keys folder on the VM.
7. grant service account access to the compute service account
   ![](images/service_account5.png)

## Install terraform
1. Go to https://developer.hashicorp.com/terraform/install and download the terraform binaries to a terraform folder
   ![](images/terraform1.png)
```
unzip terraform_1.7.5_windows_amd64.zip
rm terraform_1.7.5_windows_amd64.zip
```

**Add the terraform folder path to PATH environment variable**
1. Copy [main.tf](main.tf) and [variables.tf](variables.tf) to the terraform folder
2. Ensure the json key is under terraform/keys folder
3. Test terraform command works
   ![](images/terraform2.png)

## Provision Google infrastructure
Running terraform will provision the following google cloud infrastructure components  
* Compute instance with Ubuntu os  
* Storage bucket  
* Bigquery dataset  
* static IP address  
* Firewall access to jupyter, spark, and mage ports  
terraform init
![](images/terraform3.png)
terraform plan "my_plan.out"
![](images/terraform4.png)
![](images/terraform54.png)
![](images/terraform6.png)
![](images/terraform7.png)
![](images/terraform8.png)
terraform apply "my_plan.out"
![](images/terraform9.png)


## Verify provisioned infrastructure
From Navigation menu
Go to Compute Engine -> VM instance
![](images/terraform10.png)

Go to VPC Network->Firewall
![](images/terraform11.png)

Go to Cloud Storage->Buckets
![](images/terraform12.png)

Go to BigQuery
![](images/terraform13.png)

ssh to the VM machine  
create file ~/.ssh/config
![](images/terraform14.png)
![](images/terraform15.png)
