## UCSC Extension Assignment - CloudFormation
Assignment to create a web server via a cloud formation stack

### Project Instructions
1. Create an Amazon EC2 instance running an Ubuntu AMI with: 

- A new EBS volume attached 
- *TODO:* new Elastic IP address (public IP) 
-  SSH keypair.  

    The Ubuntu AMI can be either 16.04 or 18.04 (64-bit).

    Also create a security group that allows SSH (port 22) 
and HTTP (port 80) access from your laptop 
(you can use 0.0.0.0/0 for simplicity).

    Don't forget to create mount point in the file system 
for your new EBS volume.

    You can use an existing VPC & subnet or create them.

    Finally create a new file, using a provisioner, with the 
string "Hello, world!", in the new EBS volume.

    Show your work and show the contents of the new file.

 

2. Enhance #1 as follows. 
    
    After creating the EC2 instance with a new EBS volume, 
    use a provisioner to install a web server (nginx, 
    apache, or use the simple one that comes with python).

    Show your work and show that you get the 
    web server's default web page.
