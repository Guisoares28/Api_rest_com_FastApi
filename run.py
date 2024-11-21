from datetime import datetime, timezone

import uvicorn

if __name__ == "__main__":
    print(datetime.now(timezone.utc))
    uvicorn.run("app.main:app", port=8000)