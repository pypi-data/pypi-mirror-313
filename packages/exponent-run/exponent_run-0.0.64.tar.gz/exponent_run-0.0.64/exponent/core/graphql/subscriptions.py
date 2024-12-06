AUTHENTICATED_USER_SUBSCRIPTION = """
    subscription {
            testAuthenticatedUser {
                __typename
                ... on UnauthenticatedError {
                    message
                }
                ...on Error {
                    message
                }
                ... on User {
                    userUuid
                }
            }
        }
"""

CHAT_EVENTS_SUBSCRIPTION = """
  subscription ChatEvents(
    $prompt: Prompt
    $codeBlockConfirmation: CodeBlockConfirmationResponse
    $fileWriteConfirmation: FileWriteConfirmationResponse
    $commandConfirmation: CommandConfirmationResponse
    $directAction: DirectAction
    $chatUuid: String!
    $parentUuid: String
    $model: LiteLLMModels!
    $strategyNameOverride: StrategyName
    $useToolsConfig: UseToolsMode!
    $depthLimit: Int!
    $requireConfirmation: Boolean
    $strategyNameOverride: StrategyName
  ) {
    authenticatedChat(
      chatInput: {
        prompt: $prompt
        codeBlockConfirmation: $codeBlockConfirmation
        fileWriteConfirmation: $fileWriteConfirmation
        commandConfirmation: $commandConfirmation
        directAction: $directAction
      }
      parentUuid: $parentUuid
      chatConfig: {
        chatUuid: $chatUuid
        model: $model
        useToolsConfig: $useToolsConfig
        requireConfirmation: $requireConfirmation
        strategyNameOverride: $strategyNameOverride
        depthLimit: $depthLimit
      }
    ) {
      __typename
      ... on UnauthenticatedError {
        __typename
        message
      }
      ... on Error {
        __typename
        message
      }
      ... on MessageChunkEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        role
        content
      }
      ... on MessageEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        role
        content
        attachments {
          ... on FileAttachment {
            file {
              filePath
              workingDirectory
            }
            content
          }
          ... on URLAttachment {
            url
            content
          }
        }
      }
      ... on CodeBlockChunkEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        language
        content
      }
      ... on CodeBlockEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        language
        content
        requireConfirmation
      }
      ... on CodeBlockConfirmationEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        codeBlockUuid
        accepted
      }
      ... on CodeExecutionEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        codeBlockUuid
        content
      }
      ... on CodeExecutionStartEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        codeBlockUuid
      }
      ... on FileWriteChunkEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        filePath
        language
        writeStrategy
        content
        writeContent {
          ... on EditContent {
            content
          }
          ... on NaturalEditContent {
            newFile
            originalFile
            naturalEdit
            errorContent
          }
        }
      }
      ... on FileWriteEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        filePath
        language
        writeStrategy
        content
        writeContent {
          ... on EditContent {
            content
          }
          ... on NaturalEditContent {
            newFile
            originalFile
            naturalEdit
            errorContent
          }
        }
        requireConfirmation
      }
      ... on FileWriteConfirmationEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        fileWriteUuid
        accepted
      }
      ... on FileWriteResultEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        fileWriteUuid
        content
      }
      ... on FileWriteStartEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        fileWriteUuid
      }
      ... on CommandChunkEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        data {
          __typename
          ... on ThinkingCommandData {
            type
            content
          }
          ... on FileReadCommandData {
            type
            filePath
            language
          }
          ... on FileOpenCommandData {
            type
            filePath
            language
          }
          ... on PrototypeCommandData {
            type
            commandName
            contentJson
            contentRendered
            contentRaw
          }
        }
      }
      ... on CommandEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        data {
          __typename
          ... on ThinkingCommandData {
            type
            content
          }
          ... on FileReadCommandData {
            type
            filePath
            language
          }
          ... on FileOpenCommandData {
            type
            filePath
            language
          }
          ... on PrototypeCommandData {
            type
            commandName
            contentJson
            contentRendered
            contentRaw
          }
        }
        requireConfirmation
      }
      ... on CommandConfirmationEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        commandUuid
        accepted
      }
      ... on CommandStartEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        commandUuid
      }
      ... on CommandResultEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        commandUuid
        content
      }
      ... on RemoteStartEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
      }
      ... on RemoteEndEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
      }
    }
  }
"""
