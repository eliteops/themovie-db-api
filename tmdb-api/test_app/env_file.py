from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

python_path = os.getenv("PYTHONPATH")
print(f"here is the path => {python_path}")