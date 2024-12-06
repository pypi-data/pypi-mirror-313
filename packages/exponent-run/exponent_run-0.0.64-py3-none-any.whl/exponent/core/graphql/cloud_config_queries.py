GET_CLOUD_CONFIGS_QUERY: str = """
    query {
        cloudConfigs {
            __typename
            ... on UnauthenticatedError {
                message
            }
            ... on CloudConfigs {
                configs {
                    cloudConfigUuid
                    githubOrgName
                    githubRepoName
                    setupCommands
                    repoUrl
                }
            }
        }
    }
"""

CREATE_CLOUD_CONFIG_MUTATION: str = """
    mutation CreateCloudConfig(
        $githubOrgName: String!,
        $githubRepoName: String!,
        $setupCommands: [String!],
    ) {
        createCloudConfig(
            input: {
                githubOrgName: $githubOrgName,
                githubRepoName: $githubRepoName,
                setupCommands: $setupCommands,
            }
        ) {
            __typename
            ... on UnauthenticatedError {
                message
            }
            ... on CloudConfig {
                cloudConfigUuid
                githubOrgName
                githubRepoName
                setupCommands
                repoUrl
            }
        }
    }
"""

UPDATE_CLOUD_CONFIG_MUTATION: str = """
    mutation UpdateCloudConfig(
        $cloudConfigUuid: String!,
        $githubOrgName: String!,
        $githubRepoName: String!,
        $setupCommands: [String!],
    ) {
        updateCloudConfig(
            cloudConfigUuid: $cloudConfigUuid,
            input: {
                githubOrgName: $githubOrgName,
                githubRepoName: $githubRepoName,
                setupCommands: $setupCommands,
            }
        ) {
            __typename
            ... on UnauthenticatedError {
                message
            }
            ... on CloudConfig {
                cloudConfigUuid
                githubOrgName
                githubRepoName
                setupCommands
                repoUrl
            }
        }
    }
"""
