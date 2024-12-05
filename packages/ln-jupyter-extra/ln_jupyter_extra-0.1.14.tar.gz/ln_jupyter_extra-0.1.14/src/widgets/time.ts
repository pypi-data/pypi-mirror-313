import { Widget } from '@lumino/widgets';
import { JupyterFrontEnd } from '@jupyterlab/application';
class UsageTimeWidget extends Widget {
  private startTime: number; // 添加类型声明
  constructor() {
    super();
    this.id = 'usage-time-widget';
    this.title.label = '使用时间';
    this.title.closable = true;
    this.addClass('usage-time-widget');
    this.startTime = Date.now(); // 记录启动时间
    this.updateUsageTime();
    setInterval(() => this.updateUsageTime(), 1000); // 每秒更新
  }

  updateUsageTime() {
    const elapsedTime = Math.floor((Date.now() - this.startTime) / 1000); // 计算已用时间（秒）
    const hours = Math.floor(elapsedTime / 3600);
    const minutes = Math.floor((elapsedTime % 3600) / 60);
    const seconds = elapsedTime % 60;

    this.node.style.cssText = 'margin-top:5px';
    this.node.innerText = `已使用时间: ${hours}小时 ${minutes}分钟 ${seconds}秒`;
  }

  install(app: JupyterFrontEnd) {
    app.shell.add(this, 'top', {
      rank: 998
    });
  }
}

export default UsageTimeWidget;
