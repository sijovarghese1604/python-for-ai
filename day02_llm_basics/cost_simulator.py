from dataclasses import dataclass, field
from typing import Literal

Role = Literal["system", "user", "assistant"]
INPUT_PRICE = 3.0     # USD per 1M input tokens (example price)
OUTPUT_PRICE = 15.0   # USD per 1M output tokens (example price)
USD_TO_INR = 88       # approximate

def estimate_tokens(text: str) -> int:
    # Rough rule: 1 token ≈ 4 characters of English
    return max(1, len(text) // 4)

@dataclass
class Message:
    role: Role
    content: str

@dataclass
class Conversation:
    messages: list[Message] = field(default_factory=list)
    total_cost: float = 0.0
    max_history: int = 4

    def send(self, user_text: str, reply_text: str) -> None:
        # 1. Add the new user message to history
        self.messages.append(Message("user", user_text))
        
        # 2. The API is stateless, so we send last few messages as per max_history
        recent = self.messages[1:][-self.max_history:]
        input_tokens = sum(estimate_tokens(m.content) for m in [self.messages[0],*recent])
        output_tokens = estimate_tokens(reply_text)

        # 3. Calculate the cost of this one call
        cost = (input_tokens / 1_000_000 * INPUT_PRICE
                + output_tokens / 1_000_000 * OUTPUT_PRICE)
        self.total_cost += cost

        # 4. Save the model's reply into history for the next turn
        self.messages.append(Message("assistant", reply_text))
        print(f"Turn {len(self.messages)//2}: input={input_tokens:>5} "
              f"output={output_tokens:>4} cost=${cost:.5f}")

# A system prompt, repeated to make it realistically long
chat = Conversation([Message("system", "You are a compliance assistant. " * 20)])
question = "Can I buy 100 shares of TCS this week? " * 3
answer = "Based on the pre-clearance policy, you need approval first because... " * 8

for _ in range(5):
    chat.send(question, answer)

print(f"Total: ${chat.total_cost:.4f} (~Rs {chat.total_cost * USD_TO_INR:.2f})")