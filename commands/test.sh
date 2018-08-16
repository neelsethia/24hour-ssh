aws ec2 describe-instances --instance-ids i-0f92810d97eb6f7c5 --query 'Reservations[*].Instances[*].PublicIpAddress'
ssh ec2-user@34.218.49.172
telnet 34.218.49.172 22