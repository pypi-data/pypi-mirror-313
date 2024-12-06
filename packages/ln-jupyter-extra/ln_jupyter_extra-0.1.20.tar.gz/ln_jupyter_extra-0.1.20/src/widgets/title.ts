import { Widget } from '@lumino/widgets';
import { JupyterFrontEnd } from '@jupyterlab/application';
class TitleWidget extends Widget {
  public nodeTitle: HTMLDivElement;
  public widget: Widget;
  constructor(options: any) {
    super();
    this.nodeTitle = document.createElement('div');
    this.nodeTitle.textContent = options.projectData.name || '';
    this.nodeTitle.style.cssText = 'margin-left:350px;margin-top:5px';
    this.widget = new Widget({ node: this.nodeTitle });
    this.widget.id = 'jupyter-title';
  }

  install(app: JupyterFrontEnd) {
    app.shell.add(this.widget, 'top', { rank: 501 });
  }
}

export default TitleWidget;
