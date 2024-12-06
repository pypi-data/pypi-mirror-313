import { Widget } from '@lumino/widgets';
import { consoleIcon } from '@jupyterlab/ui-components';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { IStatusBar } from '@jupyterlab/statusbar';

class LogMonitorWidget extends Widget {
  constructor() {
    super();
    this.addClass('jp-log-monitor');
    this.id = 'jp-log-monitor-version';
    this.title.caption = 'Log Monitor';
    this.title.label = '日志监控';
    this.title.icon = consoleIcon;
    this.title.closable = true;

    // 创建日志容器
    this.logContainer = document.createElement('div');
    this.logContainer.className = 'jp-log-container';
    this.logContainer.style.cssText = `
        padding: 10px;
        height: 200px;
        overflow-y: auto;
        background-color: var(--jp-layout-color1);
        font-family: var(--jp-code-font-family);
        font-size: var(--jp-code-font-size);
      `;

    // 添加工具栏
    const toolbar = document.createElement('div');
    toolbar.className = 'jp-log-toolbar';
    toolbar.style.cssText = `
        padding: 5px;
        display: flex;
        justify-content: space-between;
        background-color: var(--jp-toolbar-background);
        border-bottom: var(--jp-border-width) solid var(--jp-border-color1);
      `;

    // 添加清除按钮
    const clearButton = document.createElement('button');
    clearButton.textContent = 'Clear Logs';
    clearButton.className = 'jp-Button';
    clearButton.onclick = () => this.clearLogs();
    toolbar.appendChild(clearButton);

    this.node.appendChild(toolbar);
    this.node.appendChild(this.logContainer);

    // 模拟一些初始日志
    this.addLog('Log monitor initialized 1');
  }

  readonly logContainer: HTMLDivElement;

  // 添加日志的方法
  addLog(message: string): void {
    const logEntry = document.createElement('div');
    logEntry.className = 'jp-log-entry';
    logEntry.style.cssText = `
        padding: 2px 5px;
        border-bottom: 1px solid var(--jp-border-color2);
      `;

    const timestamp = new Date().toLocaleTimeString();
    logEntry.textContent = `[${timestamp}] ${message}`;

    this.logContainer.appendChild(logEntry);
    this.logContainer.scrollTop = this.logContainer.scrollHeight;
  }

  // 清除日志的方法
  clearLogs(): void {
    this.logContainer.innerHTML = '';
    this.addLog('Logs cleared');
  }

  install(app: JupyterFrontEnd, statusBar: IStatusBar) {
    const logCommandId = 'toggle-logs';
    app.commands.addCommand(logCommandId, {
      label: 'ToggleLog',
      execute: () => {
        if (this && this.isAttached) {
          // 如果面板已经打开，隐藏或关闭它
          this.close(); // 关闭面板但不销毁
        } else if (this) {
          // 如果面板存在但已关闭，再次打开它
          app.shell.add(this, 'down', { rank: 1000 });
          app.shell.activateById(this.id); // 激活该面板
        } else {
          // 如果面板尚未创建，创建并添加
          const logMonitor = new LogMonitorWidget();
          logMonitor.node.style.marginLeft = '300px'; // 保证从左侧开始对齐
          app.shell.add(logMonitor, 'down', { rank: 1000 });
          app.shell.activateById(logMonitor.id); // 激活该面板
        }
      }
    });
    const logStatusItem = new Widget();
    logStatusItem.addClass('jp-mod-highlighted');

    // Create the button content
    const logButton = document.createElement('div');
    logButton.innerHTML = `
        <span class="jp-StatusBar-TextItem">
          日志监控
        </span>
      `;
    logStatusItem.node.appendChild(logButton);
    logStatusItem.node.onclick = () => {
      app.commands.execute(logCommandId);
    };

    statusBar.registerStatusItem('log-status', {
      item: logStatusItem,
      align: 'left',
      rank: 1000
    });
  }
}

export default LogMonitorWidget;
