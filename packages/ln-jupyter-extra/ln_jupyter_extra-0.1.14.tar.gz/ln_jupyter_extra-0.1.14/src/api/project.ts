import request, { customRequest } from '../request/index';
// const _baseUrlCommon = '/gateway/foundation/api/v1';
const _baseUrl = '/gateway/training/api/v1/notebook';
const _baseUrlToken = '/gateway/foundation/api/v1';
const _baseUrlFile = '/gateway/file-proxy/api/v1';
import type * as ProjectModel from './model/projectModel';

export const getProjectVersionList = async (
  data: ProjectModel.IForkListParams
) => {
  return await request.post(_baseUrl + '/version/action/page', {
    data
  });
};

/** 获取项目详情*/
export const getProjectDetail = async (id: any) => {
  return await request.get(_baseUrl + '/project/' + id);
};

// 查询文件列表
export const getFileList = async (
  data: ProjectModel.IGetListParams,
  authToken: string,
  clusterId = 'local'
) => {
  const headers = {
    Authorization: `Bearer ${authToken}`
  };
  const region = clusterId;
  return await customRequest.get(_baseUrlFile + '/list', {
    params: { ...data, region },
    headers
  });
};

// 获取文件代理服务token（查询共享对象（模型或数据集）的文件token）
export const getFileProxyToken = async (
  data: ProjectModel.IFileProxyAfterTokenParams
) => {
  return await request.post(_baseUrlToken + '/shares/action/file/token', {
    data
  });
};

/** 新增版本 */
export const addProjectVersion = async (data: any) => {
  return await request.post(_baseUrl + '/version', {
    data
  });
};
