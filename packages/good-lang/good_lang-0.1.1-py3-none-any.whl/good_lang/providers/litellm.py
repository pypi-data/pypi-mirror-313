import litellm
import os

if os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY"):
    litellm.log_raw_request_response = True
    litellm.success_callback = ["langfuse"]


__all__ = ["litellm"]
