# Creating the network
create_network(){
printf "Creating Network \n"
gcloud compute networks create default
gcloud compute firewall-rules create default-allow-icmp --network default --allow icmp --source-ranges 0.0.0.0/0
gcloud compute firewall-rules create default-allow-ssh --network default --allow tcp:22 --source-ranges 0.0.0.0/0
gcloud compute firewall-rules create default-allow-internal --network default --allow tcp:0-65535,udp:0-65535,icmp --source-ranges 10.128.0.0/9
gcloud config set disable_prompts true
}

# Run the VMs
create_vms(){
printf "Creating VM server-instance \n"
gcloud compute instances create server-instance --zone=northamerica-northeast1-a 
sleep 2

printf "Getting IP of VM server-instance \n"
gcloud compute instances list --filter="server-instance" --format "get(networkInterfaces[0].networkIP)" > 	server-ip.txt

printf "Creating VM client-instance \n" 
gcloud compute instances create client-instance --zone=northamerica-northeast1-a 
sleep 2

printf "Transferring (1/6) Files to server-instance\n"
gcloud compute scp "server-impl.py" $USER@server-instance:server-impl.py --zone=northamerica-northeast1-a
printf "Transferring (2/6) Files to server-instance\n"
gcloud compute scp "server-ip.txt" $USER@server-instance:server-ip.txt --zone=northamerica-northeast1-a
printf "Transferring (3/6) Files to server-instance\n"
gcloud compute scp --recurse "data" $USER@server-instance:data --zone=northamerica-northeast1-a
printf "Transferring (4/6) Files to server-instance\n"
gcloud compute scp "bucket_data.json" $USER@server-instance:bucket_data.json --zone=northamerica-northeast1-a
printf "Transferring (5/6) Files to server-instance\n"
gcloud compute scp "prashasti-karlekar-fall2022-firebase.json" $USER@server-instance:prashasti-karlekar-fall2022-firebase.json --zone=northamerica-northeast1-a
printf "Transferring (6/6) Files to server-instance\n"
gcloud compute scp "requirements.txt" $USER@server-instance:requirements.txt --zone=northamerica-northeast1-a


sleep 2

printf "Transferring (1/2) Files to client-instance \n"
gcloud compute scp "client-impl.py" $USER@client-instance:client-impl.py --zone=northamerica-northeast1-a
printf "Transferring (2/2) Files to client-instance\n"
gcloud compute scp "server-ip.txt" $USER@client-instance:server-ip.txt --zone=northamerica-northeast1-a
sleep 2


}

run(){
	# gcloud compute scp "server-impl.py" $USER@server-instance:server-impl.py --zone=northamerica-northeast1-a
	# gcloud compute scp "client-impl.py" $USER@client-instance:client-impl.py --zone=northamerica-northeast1-a
printf "Installing the requirements \n"
gcloud compute ssh server-instance --zone=northamerica-northeast1-a --command="sudo apt-get install python3-pip -y && pip install pip --upgrade"
gcloud compute ssh server-instance --zone=northamerica-northeast1-a --command="pip3 install -r requirements.txt"

printf "Running server-instance in Background \n"
gcloud compute ssh server-instance --zone=northamerica-northeast1-a  --command="python3 server-impl.py" & 
sleep 5

printf "Running client-instance \n"
printf "Client-instance is open for testing...please wait for the menu \n"
gcloud compute ssh client-instance --zone=northamerica-northeast1-a --command='python3 client-impl.py'
}

# Stop the VMs
stop_vms(){
printf "Stopping VMS \n"
	gcloud compute instances stop client-instance server-instance --zone=northamerica-northeast1-a
}

# Delete the VMs
delete_vms(){
printf "Deleting VMS \n"
	gcloud compute instances delete client-instance server-instance --zone=northamerica-northeast1-a
}

# Delete default network
delete_network(){
printf "Deleting Network \n"
gcloud compute firewall-rules delete default-allow-icmp
gcloud compute firewall-rules delete default-allow-ssh
gcloud compute firewall-rules delete default-allow-internal
gcloud compute networks delete default
}

# Create storage bucket
create_bucket(){
	printf "Creating Bucket \n"
	gcloud storage buckets create gs://prashasti_kvstore --location=US-EAST1 --uniform-bucket-level-access
	printf "Copying JSON file to storage bucket \n"
	# gsutil cp kvstore_1.json gs://prashasti_kvstore
	gcloud storage cp bucket_data.json gs://prashasti_kvstore
}

# Delete storage bucket
delete_bucket(){
	printf "Deleting Bucket \n"
	gcloud storage rm --recursive gs://prashasti_kvstore/
}



# Menu
while :
do

	echo "---------------------------------"
	echo "	      KV-STORE ON GCP"
	echo "	         M E N U" 
	echo "---------------------------------"
	
	echo "1. Create Default Network"
	echo "2. Create Server-instance and Client-instance"
	echo "3. Create Storage Bucket & Copy JSON file to Storage Bucket"	
	echo "4. Run the instances"
	echo "5. Stop Server-instance and Client-instance"
	echo "6. Delete Storage Bucket"
	echo "7. Delete Server-instance and Client-instance"
	echo "8. Delete Default Network & Firewalls"	
	echo "9. Exit"
	echo "---------------------------------"
	echo "Please create network first if Server-instance and Client-instance fails to run/start"
	read -r -p "Enter your choice [1-9] : " c
	
	case $c in
		1) echo 'Creating Default Network';create_network;;
		2) echo 'Creating and Transfering files to Server and Client Instances';create_vms;;
		3) echo 'Creating Storage Bucket & Copying JSON file to Storage Bucket';create_bucket;;
		4) echo 'Run the instances';run;;
		5) echo 'Stopping Server and Client';stop_vms;;
		6) echo 'Deleting Bucket';delete_bucket;;
		7) echo 'Deleting Server and Client Instances';delete_vms;;
		8) echo 'Deleting Default Network & Firewalls';delete_network;;
		9) break;;		 
		*) echo "Select between 1 to 9 only"
	esac
done
