build:
	mkdir layer
	cp ssm_securestring_cfn_macro/requirements.txt layer/requirements.txt	
	cd layer; pip3 install --target . -r requirements.txt
	sam build

deploy:
	sam deploy --stack-name ssm-securestring-cfn-macro --template-file .aws-sam/build/template.yaml --capabilities CAPABILITY_NAMED_IAM --resolve-s3

delete:
	sam delete --stack-name ssm-securestring-cfn-macro
 
clean:
	rm -rf .aws-sam
	rm -rf layer
	rm -rf __pycache__
	rm -rf ssm_securestring_cfn_macro/__pycache__
	rm -rf ssm_securestring_cfn_macro/ssm/__pycache__
