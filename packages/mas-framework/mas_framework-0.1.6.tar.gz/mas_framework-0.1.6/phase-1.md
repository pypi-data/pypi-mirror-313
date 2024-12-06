# Transport Layer Enhancement Plan - Phase 1

## Overview
This document outlines the plan to enhance the MAS transport layer to ensure message isolation, prevent duplicates, and eliminate cross-talk between components. The goal is to create a robust MVP that maintains simplicity while ensuring message integrity and proper routing.

## Core Concepts

### 1. Topic Structure
The system will use a structured topic hierarchy for message routing:

```
{agent_id}/inbox     # Personal inbox for each agent
{agent_id}/outbox    # Messages sent by the agent (for tracking/debugging)
system/discovery     # Discovery service messages only
system/errors       # System-wide error notifications
```

#### Topic Rules:
1. Each agent can only subscribe to its own inbox
2. Only the transport service can write to inboxes
3. System topics are protected and only accessible by core services
4. Outbox topics are write-only for agents (used for debugging/tracking)

### 2. Message Validation
Messages must be validated at multiple levels:

```python
class MessageValidator:
    """Ensures messages meet system requirements and security rules."""
    
    def validate(self, message: Message) -> bool:
        """
        Validates a message against all system rules.
        
        Validation Steps:
        1. Structure validation
        2. Sender verification
        3. Target verification
        4. Permissions check
        5. Message type validation
        """
        return (
            self._validate_structure(message) and
            self._validate_sender(message) and
            self._validate_target(message) and
            self._validate_permissions(message) and
            self._validate_message_type(message)
        )
    
    def _validate_structure(self, message: Message) -> bool:
        """
        Validates message structure:
        - Has valid UUID
        - Has timestamp
        - Has sender_id and target_id
        - Has valid message_type
        - Has non-empty payload
        """
        pass

    def _validate_sender(self, message: Message) -> bool:
        """
        Validates message sender:
        - Sender exists in system
        - Sender is active
        - Sender token is valid
        """
        pass

    def _validate_target(self, message: Message) -> bool:
        """
        Validates message target:
        - Target exists in system
        - Target is active
        - Target can receive this message type
        """
        pass

    def _validate_permissions(self, message: Message) -> bool:
        """
        Validates sender permissions:
        - Can send this message type
        - Can send to this target
        - Meets rate limiting requirements
        """
        pass

    def _validate_message_type(self, message: Message) -> bool:
        """
        Validates message type:
        - Type is registered in system
        - Type matches expected flow
        - Type is allowed for sender/target pair
        """
        pass
```

### 3. Message Deduplication
Implement time-window based deduplication:

```python
class MessageDeduplicator:
    """Prevents duplicate message processing within a time window."""
    
    def __init__(self, window_minutes: int = 5):
        self.window_minutes = window_minutes
        self.seen_messages: Dict[str, datetime] = {}
        self._cleanup_lock = asyncio.Lock()
    
    async def is_duplicate(self, message: Message) -> bool:
        """
        Checks if message is a duplicate within time window.
        Also triggers cleanup of old entries.
        """
        await self._cleanup_old_messages()
        
        message_key = self._get_message_key(message)
        if message_key in self.seen_messages:
            return True
            
        self.seen_messages[message_key] = datetime.now(UTC)
        return False
    
    def _get_message_key(self, message: Message) -> str:
        """
        Creates unique key for message:
        {message_id}:{sender_id}:{target_id}:{message_type}
        """
        return f"{message.id}:{message.sender_id}:{message.target_id}:{message.message_type}"
    
    async def _cleanup_old_messages(self) -> None:
        """Removes messages outside the time window."""
        async with self._cleanup_lock:
            cutoff = datetime.now(UTC) - timedelta(minutes=self.window_minutes)
            self.seen_messages = {
                k: v for k, v in self.seen_messages.items()
                if v >= cutoff
            }
```

### 4. Message Routing
Implement intelligent message routing:

```python
class MessageRouter:
    """Routes messages to appropriate topics based on type and target."""
    
    def get_route(self, message: Message) -> str:
        """
        Determines correct topic for message.
        
        Routing Rules:
        1. Discovery messages -> system/discovery
        2. Error messages -> system/errors
        3. Agent messages -> {target_id}/inbox
        4. Copy to sender's outbox for tracking
        """
        if message.message_type in [
            MessageType.REGISTRATION_REQUEST,
            MessageType.DISCOVERY_REQUEST
        ]:
            return "system/discovery"
            
        if message.message_type == MessageType.ERROR:
            return "system/errors"
            
        return f"{message.target_id}/inbox"
    
    def get_debug_route(self, message: Message) -> str:
        """Gets outbox topic for message tracking."""
        return f"{message.sender_id}/outbox"
```

### 5. Enhanced Transport Service
Integrate all components:

```python
class TransportService:
    """
    Enhanced transport service with validation, deduplication,
    and proper routing.
    """
    
    def __init__(self, transport: ITransport):
        self.transport = transport
        self.validator = MessageValidator()
        self.router = MessageRouter()
        self.deduplicator = MessageDeduplicator()
        self._subscriptions = SubscriptionManager()
        
    async def send_message(self, message: Message) -> None:
        """
        Sends a message through the transport system.
        
        Flow:
        1. Validate message
        2. Check for duplicates
        3. Determine route
        4. Publish to route
        5. Copy to debug topic (if enabled)
        """
        # Validate
        if not self.validator.validate(message):
            raise InvalidMessageError("Message failed validation")
            
        # Check duplicates
        if await self.deduplicator.is_duplicate(message):
            logger.warning(f"Dropping duplicate message {message.id}")
            return
            
        # Get route
        route = self.router.get_route(message)
        
        # Publish
        try:
            await self.transport.publish(route, message)
            
            # Debug copy
            if self.debug_enabled:
                debug_route = self.router.get_debug_route(message)
                await self.transport.publish(debug_route, message)
                
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise
```

## Implementation Phases

### Phase 1A: Topic Structure (Week 1)
1. Update transport interface for structured topics
2. Implement topic validation
3. Update subscription management
4. Add topic access control

### Phase 1B: Message Validation (Week 1-2)
1. Implement MessageValidator
2. Add validation to transport service
3. Add validation logging
4. Test validation rules

### Phase 1C: Deduplication (Week 2)
1. Implement MessageDeduplicator
2. Add cleanup mechanism
3. Add duplicate detection logging
4. Test time window behavior

### Phase 1D: Message Routing (Week 2-3)
1. Implement MessageRouter
2. Add debug routing
3. Update transport service
4. Test routing rules

## Testing Strategy

### Unit Tests
1. Topic validation
2. Message validation rules
3. Deduplication logic
4. Routing rules
5. Transport service integration

### Integration Tests
1. End-to-end message flow
2. Multi-agent scenarios
3. Error handling
4. Rate limiting
5. Debug topic testing

### Load Tests
1. Concurrent message handling
2. Deduplication under load
3. Topic scaling
4. Memory usage monitoring

## Monitoring Points
1. Message validation failures
2. Duplicate attempts
3. Routing decisions
4. Topic access violations
5. Service performance metrics

## Success Criteria
1. No message cross-talk
2. No duplicate deliveries
3. Clear message tracking
4. Proper error handling
5. Stable under load

## Rollback Plan
1. Keep old topic structure
2. Version new components
3. Implement feature flags
4. Maintain backward compatibility
5. Document rollback procedures

## Future Enhancements
1. Message persistence
2. Advanced routing rules
3. Enhanced security
4. Performance optimizations
5. Advanced debugging tools 