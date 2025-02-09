To generate a requirements.txt file, you can manually create it or use the following command after installing the necessary packages in your virtual environment:

pip freeze > requirements.txt

Setting Up the Virtual Environment

If you haven't already set up the virtual environment, follow these steps:

a. Create a Virtual Environment (if you haven't done this already):

Open your terminal and run:

python3 -m env

 cd into bin 
 
source activate

After activation, your terminal prompt should change, indicating you're now inside the virtual environment.

c. Install the Dependencies:

Once the virtual environment is activated, install the required packages from the requirements.txt file:

sudo pip3 install scapy

pip install -r requirements.txt Or sudo pip3 install scapy

This command will install scapy (and any other libraries listed in the requirements.txt file) inside the virtual environment.

d. Run the Script: inside the the virtual machine

Now that everything is set up, you can run the port scanner script as follows:

python3 scan.py

The script will now run within the isolated virtual environment, ensuring that dependencies are separate from your system Python installation.

 Verify the Installation
 
If you need to verify that everything was installed properly in your virtual environment, you can check installed packages using:

pip list

It should show scapy as an installed package.

 Deactivating the Virtual Environment
 
Once you're done working in the virtual environment, you can deactivate it by running:

deactivate


