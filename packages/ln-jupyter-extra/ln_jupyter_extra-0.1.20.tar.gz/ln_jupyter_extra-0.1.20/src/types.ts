export interface IVersion {
  id: string;
  projectId: string;
  originVersionId: string;
  version: string;
  defaultFlag: number;
  status: number;
  checkReason: any;
  description: string;
  tagName: any;
  clusterId: string;
  bucketId: string;
  bucketCrName: string;
  bucketStorageType: string;
  bucketPath: string;
  createTime: string;
  createUser: string;
  updateTime: string;
  updateUser: string;
}

export interface ITag {
  id: string;
  businessType: number;
  businessId: string;
  name: string;
  tenantId: string;
  label: string;
  createTime: string;
  createUser: string;
  updateTime: string;
  updateUser: string;
}

export interface IDataset {
  id: string;
  projectId: string;
  name: string;
  businessType: number;
  businessId: string;
  bucketPath: string;
  createTime: string;
  createUser: string;
  updateTime: string;
  updateUser: string;
  fileList?: any[];
}

export interface IProjectData {
  tenantName: string;
  userLoginName: string;
  userDisplayName: string;
  userHeadImage: string;
  tenantFlag: number;
  wechatBindFlag: any;
  id: string;
  originProjectId: string;
  jobId: string;
  jobState: any;
  name: string;
  fileSourceType: number;
  status: number;
  description: string;
  viewNum: number;
  collectNum: number;
  collectStatus: boolean;
  forkNum: number;
  createTime: string;
  createUser: string;
  updateTime: string;
  updateUser: string;
  projectVersionList: IVersion[];
  tagList: ITag[];
  storageList: IDataset[];
}
