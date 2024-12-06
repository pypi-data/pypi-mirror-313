EVENTS_FOR_CHAT_QUERY: str = """query EventsForChat($chatUuid: String!) {
  eventsForChat(chatUuid: $chatUuid) {
    ... on EventHistory {
      events {
        ... on GraphExponentEvent {
          eventUuid
        }
      }
    }
  }
}
"""
