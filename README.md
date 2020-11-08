# responder-sample
## Usage
- create init table
  ```
  python models.py
  ```
- run
  ```
  python run.py
  ```
- sample post command
  ```
  curl http://127.0.0.1:5042/api/todo -X POST -H "Content-Type: application/json" -d '{"name": "value", "text": "test"}'
  ```
