mkdir my-lambda-layer && cd my-lambda-layer
mkdir -p aws-layer/python/lib/python3.8/site-packages
pipenv requirements > requirements.txt
pip install -r requirements.txt --no-deps -t aws-layer/python/lib/python3.8/site-packages/
cd aws-layer
zip -r9 lambda-layer.zip .
