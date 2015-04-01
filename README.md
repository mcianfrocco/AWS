# AWS
Code for interacting with Amazon Web Services (AWS). 

## Dependencies
The following scripts assume:
* Amazon's command line interface tools (CLI Tools) are installed: http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/command-reference.html
* Path to CLI tools and AWS access & secret keys are specified as environmental variables: 

```
export JAVA_HOME=$(/usr/libexec/java_home)
export EC2_HOME=/usr/local/ec2/ec2-api-tools-1.7.3.0
export PATH=$PATH:$EC2_HOME/bin

export AWS_ACCESS_KEY=[access key]
export AWS_SECRET_KEY=[secret key]
export AWS_USER_ID=[user id]
```
