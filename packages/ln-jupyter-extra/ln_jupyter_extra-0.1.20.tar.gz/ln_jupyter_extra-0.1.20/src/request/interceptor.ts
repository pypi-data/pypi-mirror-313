// 拦截器操作

import type {
  AxiosError,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig
} from 'axios';
import { Notification } from '@jupyterlab/apputils';
import { getStorage, MessageCodeError } from '../utils';

// const domain = window.location.href;
// const usercenter = window.location.origin + '/heros';
// setStorage(
//   'USREINFO',
//   '{"id":"9fedf53c3d784e74b9cf428c6825b78e","tenantId":"120273943618889609178","name":"systemuser","displayName":"systemuser","email":"hewenbin@leinao.ai","phoneNumber":"13333333333","status":1,"description":"描述1dedrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrhh苏奇亮xdfg","headImage":"https://hero-stg-miniogw.cnbita.com/file-open/9fedf53c3d784e74b9cf428c6825b78e/user_avatar/微信图片_20241126185157.png","productId":"heros","lastUpdatePwdTime":null,"lastLoginTime":"2024-12-02 21:48:58","tenantFlag":1,"wechatBindFlag":1,"createTime":"2024-11-01 02:30:36","updateTime":"2024-12-02 11:51:10","createUser":"9fedf53c3d784e74b9cf428c6825b78e","updateUser":"9fedf53c3d784e74b9cf428c6825b78e","tenantInfo":{"id":"120273943618889609178","name":"systemuser","contactUserId":"9fedf53c3d784e74b9cf428c6825b78e","contactName":null,"contactMobile":null,"status":1,"companyName":"马冉冒烟测试合肥","enterpriseState":3,"createType":1,"description":"描述1dedrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrhh苏奇亮xdfg","productId":"heros","createTime":"2024-11-01 02:30:34","updateTime":"2024-11-01 02:12:46","createUser":"9fedf53c3d784e74b9cf428c6825b78e","updateUser":"9fedf53c3d784e74b9cf428c6825b78e","email":null},"token":"aa0f0de7-d6e9-4e28-87f4-d97055e91928","bindFlag":1,"passwordSetType":1,"account":"systemuser"}'
// );

// setStorage('projectId', 'a13741493692264448241422');
// import type { UserInfoResult } from 'types-shared'

// 不需要经过处理的接口白名单
// const whiteList = ["login", "logout"];
interface IApiHookConfigModal {
  flag?: boolean;
  /**
   * auth 是否需要token认证 true需要 false不需要
   */
  auth?: boolean;
}

// message中的错误码
// const MessageCodeDic = [
//   -3, 10133, 10117, 10119, 10121, 10122, 10124, 10134, 10157, 10307, 10315,
//   61000
// ];
// message中的错误码
const MessageCodeDic = [1027];

// 处理请求头，一般比如在header加token
export const handlerRequest = (
  config: AxiosRequestConfig,
  apiHookConfig: IApiHookConfigModal
) => {
  if (!apiHookConfig.auth) {
    return config as InternalAxiosRequestConfig<any>;
  }
  const USREINFO = JSON.parse(getStorage('USREINFO') || '{}') || {};
  // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
  if (USREINFO.token) {
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    config.headers!.token = USREINFO.token;
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    config.headers!['X-Agent-Token'] =
      'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiIsImlhdCI6MTY3MzIzMTUzNiwiaXNzIjoia3ViZXNwaGVyZSIsIm5iZiI6MTY3MzIzMTUzNn0.7O9n5M-qzJPgl2gILJ8hXNuwDPlrxdrl8CEDMLCfTyQ';
  }
  return config as InternalAxiosRequestConfig<any>;
};

// 根据情况处理返回数据
export const handleResponse = (res: AxiosResponse): AxiosResponse => {
  // 如果后端返回的是code为0，则直接返回.data.data；如果不为0，则把massage也返回出去
  // todo 在某些情况下instance可能会有用处
  const { data } = res;
  const { code, message } = data.message;
  // 正常状态返回
  if (code === 0) {
    return data;
  }
  // 异常状态返回 根据不同的code判断接下来的操作
  switch (true) {
    // 未登录
    case MessageCodeDic.includes(code):
      console.log('未登录');
      break;
    case code === 401:
      // 未授权
      // noAuthError(JSON.parse(getStorage('USREINFO') || '{}') || {});
      if (message) {
        void Notification.error(message, { autoClose: 3000 });
      }
      break;
    case code !== 0:
      if (message) {
        void Notification.error(message, { autoClose: 3000 });
      }
  }
  return Promise.reject(res) as any;
};

export const handleResponseErr = async (error: AxiosError, flag = false) => {
  const { response, request } = error;
  if (response !== null) {
    // 当响应状态码为非2xx时，可以在这里进行错误处理
    // console.log(response.status);
    // console.log(response.data);
    // console.log(response.headers);
    // 判断http状态码非2xx时 是否存在业务代码的code
    //                     存在code 匹配全局message 匹配不上 判断是否有message
    //                                                          有：提示message
    //                                                          否：根据http状态码提示
    const {
      data: { message }
    } = response as AxiosResponse;
    if (!flag) {
      const { code = undefined, message = undefined } = response?.data
        ? (response.data as any).message || {}
        : {};
      // 登录过期 需要重新登录
      if (MessageCodeDic.includes(code)) {
        console.log('登录过期');
      } else if (response?.status === 401 && code === 401) {
        // 未授权
        if (message) {
          void Notification.error(message, { autoClose: 3000 });
        }
        // noAuthError(JSON.parse(getStorage('USREINFO') || '{}') || {});
      } else if (code !== 0) {
        // 现在的逻辑是 返回的数据code不是0 http状态码可能也不是0 所以需要在这里进行拦截
        if (message) {
          void Notification.error(message, { autoClose: 3000 });
        }
      } else {
        void Notification.error(
          MessageCodeError(
            message,
            MessageCodeError({ code: response?.status })
          )
        );
      }
    }

    if (message?.code) {
      // 异常状态返回 根据不同的code判断接下来的操作
      switch (true) {
        // 未登录
        case MessageCodeDic.includes(message?.code):
          console.log('未登录');
          break;
      }
    }
    // if (data) {
    //   return (await Promise.reject(data)) as any;
    // }
  } else if (
    error.code === 'ECONNABORTED' &&
    error.message.includes('timeout')
  ) {
    // 超时处理
    void Notification.warning('请求超时，请检查网络连接并重新尝试！');
  } else if (request !== null) {
    // 当没有响应时，可以在这里进行错误处理：个人建议无需处理
    void Notification.error(MessageCodeError({}));
  } else {
    // 其他错误，可以在这里进行错误处理
    void Notification.error(MessageCodeError({}));
    console.log('Error', error.message);
  }
  // 超时判断
  return await Promise.reject(error);
};
