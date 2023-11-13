
#create base git_storage dir
mkdir -p ~/git_storage

cd ~/git_storage

#install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
source ~/.bashrc

#install node
nvm install 16

#install git
sudo yum update -y
sudo yum install git -y

#clone dynamodb-admin
git clone https://github.com/aaronshaf/dynamodb-admin.git
cd dynamodb-admin

#use sed to comment unrequired lines
sed -i 's/\ \ loadDynamoEndpoint(/\/\/loadDynamoEndpoint(/g' ./lib/backend.js
sed -i "s/return\ dynamoConfig/return\ {region:'us\-east\-1'}/g" ./lib/backend.js

#install dynamodb-admin
npm install

#run dynamodb-admin
node bin/dynamodb-admin.js &