GET_CLOUD_CHAT_STATE_QUERY = """
query GetCloudChatState($chatUuid: String!) {
    cloudChatState(chatUuid: $chatUuid) {
        __typename
        ... on CloudConnectedState {
            chatUuid
            connectedState
            lastConnectedAt
            systemInfo {
                name
                cwd
                shell
                os
                git {
                    branch
                    remote
                }
            }
        }
        ... on UnauthenticatedError {
            message
        }
        ... on ChatNotFoundError {
            message
        }
    }
}
"""
