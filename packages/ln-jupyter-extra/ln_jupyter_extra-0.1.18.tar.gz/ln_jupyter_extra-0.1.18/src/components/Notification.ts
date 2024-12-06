import { Notification } from '@jupyterlab/apputils';
import { ReadonlyJSONValue } from '@lumino/coreutils';

/**
 * 通知服务类
 */
export class NotificationService {
  /**
   * 成功通知
   * @param message 消息内容
   * @param options 额外配置
   */
  static success(
    message: string,
    options?: Notification.IOptions<ReadonlyJSONValue>
  ): void {
    Notification.success(message, options);
  }

  /**
   * 错误通知
   * @param message 消息内容
   * @param options 额外配置
   */
  static error(
    message: string,
    options?: Notification.IOptions<ReadonlyJSONValue>
  ): void {
    Notification.error(message, options);
  }

  /**
   * 警告通知
   * @param message 消息内容
   * @param options 额外配置
   */
  static warning(
    message: string,
    options?: Notification.IOptions<ReadonlyJSONValue>
  ): void {
    Notification.warning(message, options);
  }

  /**
   * 信息通知
   * @param message 消息内容
   * @param options 额外配置
   */
  static info(
    message: string,
    options?: Notification.IOptions<ReadonlyJSONValue>
  ): void {
    Notification.info(message, options);
  }
}
