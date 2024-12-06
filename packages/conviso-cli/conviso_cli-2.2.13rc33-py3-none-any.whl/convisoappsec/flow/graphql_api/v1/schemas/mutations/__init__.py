CREATE_ASSET = """ 
mutation (
  $companyId: Int!,
  $name: String!,
  $scanType: AssetScan!
) {
  createAsset(
    input: {
      companyId: $companyId,
      name: $name,
      scanType: $scanType
    }
  ) {
    asset {
      id
      name
      createdAt
    }
    errors
  }
}
"""

UPDATE_ASSET = """
mutation (
  $id: ID!,
  $companyId: Int!,
  $name: String!,
  $tecnologyList: [String!],
  $repoUrl: String
) {
  updateAsset(
    input: {
      id: $id,
      companyId: $companyId,
      name: $name,
      tecnologyList: $tecnologyList,
      repoUrl: $repoUrl
    }
  ) {
    asset {
      id
    }
  }
}
"""

CREATE_PROJECT = """
mutation (
  $companyId: Int!,
  $assetsIds: [Int!],
  $label: String!,
  $startDate: ISO8601Date!,
  $goal: String!,
  $scope: String!
) {
  createProject (
    input: {
      companyId: $companyId,
      assetsIds: $assetsIds,
      label: $label,
      startDate: $startDate,
      typeId: 33,
      playbooksIds: 1,
      goal: $goal,
      scope: $scope
    }
  ) {
    project {
      id
      apiCode
      assets {
        id
      }
    }
    errors
  }
}
"""

UPDATE_PROJECT = """
mutation (
  $projectId: ID!,
  $assetsIds: [Int!]
) {
  updateProject (
    input: {
      id: $projectId,
      assetsIds: $assetsIds
    }
  ) {
    msg
  }
}
"""

IMPORT_SBOM = """
mutation (
  $file: Upload!,
  $assetId: ID!,
  $companyId: ID!
) {
  importSbom(
    input: {
      file: $file,
      assetId: $assetId,
      companyId: $companyId
    }
  ) {
    success
  }
}
"""

LOG_AST_ERROR = """
mutation (
  $companyId: ID!,
  $assetId: ID!,
  $log: String!
) {
  logAstError(
    input: {
      companyId: $companyId,
      assetId: $assetId,
      log: $log
    }
  ) {
    success
  }
}
"""

CREATE_DEPLOY = """
mutation (
  $assetId: ID!,
  $previousCommit: String!,
  $currentCommit: String!,
  $branchName: String,
  $diffContent: Upload!
) {
  createDeploy(
    input: {
      assetId: $assetId,
      previousCommit: $previousCommit,
      currentCommit: $currentCommit,
      branchName: $branchName,
      diffContent: $diffContent
    }
  ) {
    deploy {
      id
    }
  }
}
"""
