# Chain Message Example

This example demonstrates a simple chain of 4 agents passing messages in sequence:
Agent 1 -> Agent 2 -> Agent 3 -> Agent 4 -> Agent 1

The chain completes after the message has made one full circuit.

## Running the Example

1. Make sure Redis is running locally on default port (6379)
2. Run the example:
   ```bash
   python -m examples.chain.main
   ```

Expected output: 