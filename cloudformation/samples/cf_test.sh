STACKNAME=$1
echo $STACKNAME
aws cloudformation validate-template --template-body file://./cf_merge_test.yaml
aws cloudformation create-stack --stack-name $STACKNAME --template-body file://./cf_merge_test.yaml        
aws cloudformation list-stacks
