import { Widget } from '@lumino/widgets';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { getTaskDetail } from '../api/project';
import { Notification } from '@jupyterlab/apputils';

class UsageTimeWidget extends Widget {
  startTime: number; // 添加类型声明
  constructor() {
    super();
    this.id = 'usage-time-widget';
    this.title.label = '使用时间';
    this.title.closable = true;
    this.addClass('usage-time-widget');
    this.startTime = 0; // 记录启动时间
    this.updateUsageTime();
    setInterval(() => this.updateUsageTime(), 60000); // 每秒更新
  }

  async updateUsageTime() {
    const taskId = localStorage.getItem('taskId') || '';
    if (taskId) {
      const taskData = await getTaskDetail(taskId);
      this.node.innerText = `已使用时间: ${taskData.runHours} h`;
    } else {
      Notification.error('任务ID未获取到', { autoClose: 3000 });
    }
  }

  install(app: JupyterFrontEnd) {
    app.shell.add(this, 'top', {
      rank: 998
    });
  }
}

export default UsageTimeWidget;
