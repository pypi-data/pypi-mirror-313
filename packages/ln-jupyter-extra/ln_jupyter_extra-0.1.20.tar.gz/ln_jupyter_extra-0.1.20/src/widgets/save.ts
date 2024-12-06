import { JupyterFrontEnd } from '@jupyterlab/application';
import { saveIcon } from '@jupyterlab/ui-components';
import { CommandToolbarButton } from '@jupyterlab/apputils';

class SaveButton extends CommandToolbarButton {
  constructor(app: JupyterFrontEnd) {
    // 调用父类构造函数
    const COMMAND_ID = 'version-list:save';
    app.commands.addCommand(COMMAND_ID, {
      label: '保存',
      icon: saveIcon,
      execute: () => {
        console.log('保存');
        this.handleSave();
      }
    });
    super({
      commands: app.commands,
      id: COMMAND_ID
    });

    // 设置按钮的唯一 ID
    this.id = 'version-list-save-button';
  }

  install(app: JupyterFrontEnd): void {
    app.shell.add(this, 'top', {
      rank: 1000
    });
  }

  private handleSave(): void {
    // 这里添加保存逻辑
    console.log('执行保存操作');
  }
}

export default SaveButton;
