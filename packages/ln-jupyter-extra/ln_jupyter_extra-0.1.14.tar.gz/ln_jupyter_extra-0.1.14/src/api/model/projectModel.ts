export interface IPageParams {
  pageNum?: number;
  pageSize?: number;
}

/** 项目ID */
export interface IForkListParams extends IPageParams {
  projectId: string;
}

export interface IGetListParams extends IPageParams {
  bucketName: string;
  dir: string;
}

export interface IFileProxyAfterTokenParams {
  expires?: number;
  businessId: string;
  businessType: number;
}
