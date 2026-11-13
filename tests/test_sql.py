import sqlite3
import re

def test_all_queries():
    conn = sqlite3.connect("database/b2b_growth.db")
    cursor = conn.cursor()

    with open("sql/analytical_queries.sql", "r", encoding="utf-8") as f:
        content = f.read()

    # Split on semicolon, ignoring comments
    statements = content.split(";")
    query_count = 0

    for stmt in statements:
        # Strip comments
        lines = [line for line in stmt.split("\n") if not line.strip().startswith("--")]
        cleaned = " ".join(lines).strip()
        if not cleaned:
            continue
        
        query_count += 1
        try:
            cursor.execute(cleaned)
            rows = cursor.fetchall()
            print(f"Query {query_count:2d}: Executed successfully ({len(rows)} rows returned)")
        except Exception as e:
            print(f"Query {query_count:2d}: FAILED: {e}")
            print(f"Statement: {cleaned[:100]}...")
            conn.close()
            return False

    conn.close()
    print(f"\nAll {query_count} queries executed flawlessly against SQLite database!")
    return True

if __name__ == "__main__":
    test_all_queries()

