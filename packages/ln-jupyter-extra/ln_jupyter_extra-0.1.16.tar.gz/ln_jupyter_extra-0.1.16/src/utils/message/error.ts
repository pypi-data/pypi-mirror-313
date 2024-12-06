/**
 * @author: zhayuechao@leinao.ai
 * @function: MessageCodeError
 * @description: 将错误码 翻译为中文提示给用户 非业务的code码处理
 *               也可以处理http状态码错误：500、400...
 *               处理流程：1、判断接口是否状态码为非200（即：失败）
 *                       2、是：处理http状态码错误 并提示codeDic对应的错误信息
 *                       3、否：判断接口返回的code是否正确 不正确则提示codeDic对应的错误信息
 */
type ErrorData = Record<number | string, string>;

interface IMsgCodeResponse {
  code?: number;
  status?: number;
  message?: string;
}

// 错误码对应字典值 code => message
// 注：涉及具体业务的code不要放到这里 例如：code为1001 在A业务中提示的是参数不能为空
//                                               在B业务中提示的是删除失败...
export const codeDic: ErrorData = {
  1001: '参数不能为空',
  1002: '参数不能为null',
  1003: '参数类型错误',
  1004: '空指针错误',
  1005: '参数验证失败',
  1020: '不支持表情符号',
  1021: '用户名错误',
  1022: '帐号错误',
  1023: '密码错误',
  1024: '用户名或密码错误',
  1025: '帐号或密码错误',
  1026: '验证码错误',
  1200: '资源操作错误',
  1201: '资源添加错误',
  1202: '资源删除错误',
  1203: '资源更新错误',
  1204: '资源查询错误',
  1205: '资源查询数据为空',
  1206: '不允许重复资源',
  1300: '文件操作错误',
  1301: '文件未找到',
  1302: '文件访问被拒绝',
  1303: '文件读取失败',
  1304: '文件写入失败',
  1305: '文件创建失败',
  1306: '文件删除失败',
  1307: '文件复制错误',
  1308: '文件移动失败',

  1309: '文件目录未找到',
  1310: '文件目录拒绝访问',
  1311: '文件目录读取失败',
  1312: '文件目录写入失败',

  1400: '请求第三方组件失败',
  1401: '请求第三方组件超时',
  1402: '第三方组件响应错误',
  1403: '请求内部组件错误',
  1404: '请求内部组件超时',
  1405: '内部组件响应错误',

  400: '请求失败',
  401: '未经授权',
  403: '被禁止的',
  404: '请求不存在',
  405: '不允许此请求方法',

  500: '内部服务器错误',
  502: '网关错误',
  503: '服务不可用',
  504: '网关超时'
};

/**
 *
 * @param data 服务端返回数据结构 {code: 0, message: 'message'}
 * @returns error message
 * @description 判断code是否为number 是：优先匹配code 在字典中对应的提示文字 其次提示data.message 最后提示defaultMsg
 *                                  否：提示defaultMsg
 */
export const MessageCodeError = (
  data: IMsgCodeResponse,
  defaultMsg = '系统异常，请联系管理员！'
): string => {
  return typeof data.code === 'number'
    ? (codeDic[data.code] || data.message) ?? defaultMsg
    : defaultMsg;
  // return (codeDic[data.code] || data.message) ?? defaultMsg
};
