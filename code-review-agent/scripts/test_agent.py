import asyncio, sys
sys.path.insert(0, ".")
from backend.agent.code_review_agent import CodeReviewAgent

SAMPLE_CODE = '''
import pickle, subprocess

def login(username, password):
    conn = get_db()
    query = "SELECT * FROM users WHERE name='" + username + "'"
    user = conn.execute(query).fetchone()
    if user and user["password"] == password:
        return True
    return False

def run_command(cmd):
    subprocess.call(cmd, shell=True)

def load_data(data):
    return pickle.loads(data)
'''

async def main():
    agent = CodeReviewAgent()
    result = await agent.review_code(SAMPLE_CODE, "login.py", "Python")
    print(f"\nScore: {result.overall_score}/100")
    print(f"Summary: {result.review_summary}")
    print(f"\nFound {len(result.issues)} issues:")
    for issue in result.issues:
        print(f"  [{issue.priority}] {issue.title} — {issue.cwe_reference or 'no CWE'}")

asyncio.run(main())