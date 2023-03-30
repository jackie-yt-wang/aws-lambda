# Install AWS CLI
sudo apt install -y awscli

# Install Pipenv
pipx install poetry

# Create a new virtual environment and install project dependencies
pip install requests
pip install pandas
pip install boto3
pip install toml
pip install dotenv
pip install sqlalchemy
pip install pymysql

# Set execute permission on run.py
chmod +x run.sh

# Create a log directory
mkdir -p log