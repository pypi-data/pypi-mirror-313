import type {
  AxiosError,
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse
} from 'axios';
import axios from 'axios';
import { baseConfig } from './baseConfig';
import {
  handleResponse,
  handleResponseErr,
  handlerRequest
} from './interceptor';

interface IApiHookConfigModal {
  flag?: boolean;
  auth?: boolean;
  skipErrorResponseInterceptor?: boolean; // 是否跳过错误响应拦截器
}

/**
 * axios 封装
 * 20230217
 */
export class Request {
  instance: AxiosInstance;
  flag: boolean;
  auth: boolean;
  skipErrorResponseInterceptor: boolean;
  /**
   *
   * @param config 默认配置
   * @param flag 是否是第三方接口 默认为第三方接口 true
   */
  constructor(config: AxiosRequestConfig, apiHookConfig: IApiHookConfigModal) {
    const {
      flag = true,
      auth = true,
      skipErrorResponseInterceptor = false
    } = apiHookConfig;
    this.flag = flag;
    this.auth = auth;
    this.skipErrorResponseInterceptor = skipErrorResponseInterceptor;
    this.instance = axios.create(config);
    this.initRequestInterceptor(this.instance);
    this.initResponseInterceptor(this.instance);
  }

  // 请求拦截器
  initRequestInterceptor(instance: AxiosInstance) {
    instance.interceptors.request.use(
      (config: AxiosRequestConfig) => {
        // 一般会请求拦截里面加token，用于后端的验证
        return handlerRequest(config, {
          flag: this.flag,
          auth: this.auth
        });
      },
      async (err: AxiosError) => await Promise.reject(err)
    );
  }

  // response拦截器
  initResponseInterceptor(instance: AxiosInstance) {
    instance.interceptors.response.use(
      (res: AxiosResponse) => {
        // 系统如果有自定义code也可以在这里处理
        if (!this.flag) {
          return handleResponse(res);
        }
        return res;
      },
      async (err: AxiosError) => {
        // 根据skipErrorResponseInterceptor决定是否跳过错误处理
        if (this.skipErrorResponseInterceptor) {
          return Promise.reject(err);
        } else {
          return await handleResponseErr(err, this.flag); // 状态码返回内容
        }
      }
    );
  }

  // 请求方法
  private async request<T = any>(config: AxiosRequestConfig): Promise<T> {
    return await this.instance
      .request(config)
      .then((res: AxiosResponse<T>) => (this.flag ? res : res.data) as any);
  }

  public async get<T = any>(url: string, config?: AxiosRequestConfig) {
    return await this.request<T>({ method: 'get', url, ...config });
  }

  public async post<T = any>(url: string, config?: AxiosRequestConfig) {
    return await this.request<T>({ method: 'post', url, ...config });
  }

  public async put<T = any>(url: string, config?: AxiosRequestConfig) {
    return await this.request<T>({ method: 'put', url, ...config });
  }

  public async delete<T = any>(url: string, config?: AxiosRequestConfig) {
    return await this.request<T>({ method: 'delete', url, ...config });
  }
}

// 默认导出Request实例
export default new Request(baseConfig, { flag: false });

// 自定义处理接口200时报错信息Request实例
export const customRequest = new Request(baseConfig, { flag: true });
// 自定义处理接口非200时报错信息Request实例
export const customErrorRequest = new Request(baseConfig, {
  flag: false,
  skipErrorResponseInterceptor: true
});
// 不需要token但是需要拦截器
export const notAuthRequest = new Request(baseConfig, {
  flag: false,
  auth: false
});

// 不需要token不用在意返回格式但是需要拦截器
export const noAuthFormatRequest = new Request(baseConfig, {
  flag: true,
  auth: false
});

// 不需要token不用在意返回格式不需要返回拦截器
export const noAllRequest = new Request(baseConfig, {
  flag: true,
  auth: false,
  skipErrorResponseInterceptor: true
});

// 第三方接口导出Request实例; 也可以直接引入Request类，然后传入不同的config
export const otherRequest = new Request({}, {});
// 不需要token但是需要拦截器
export const customNotAuthRequest = new Request(baseConfig, {
  flag: true,
  auth: false
});
