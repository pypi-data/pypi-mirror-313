import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  IRouter
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { IStatusBar } from '@jupyterlab/statusbar';
import createVersion from './widgets/createVersion';
import VersionListSidebarWidget from './widgets/version';
import DataSetListSidebarWidget from './widgets/dataset';
import UsageTimeWidget from './widgets/time';
import LogMonitorWidget from './widgets/log';
import TitleWidget from './widgets/title';
import { getProjectDetail } from './api/project';
import { Notification } from '@jupyterlab/apputils';
import VariableInspectorPlugins from './widgets/variable/index';

/**
 * Activate the ln-notebook extension.
 *
 * @param app - The JupyterLab Application instance
 * @param palette - The command palette instance
 * @param restorer - The application layout restorer
 * @param statusBar - The status bar instance
 *
 * @returns A promise that resolves when the extension has been activated
 */

async function activate(
  app: JupyterFrontEnd,
  palette: ICommandPalette,
  restorer: ILayoutRestorer | null,
  statusBar: IStatusBar,
  router: IRouter | undefined
): Promise<void> {
  console.log('Activating ln-jupyter-extra extension...');

  await new Promise(resolve => setTimeout(resolve, 100));

  if (router) {
    // 尝试获取路由信息的备选方案
    const currentUrl = window.location.href;
    const queryString = currentUrl.split('?')[1];
    const urlParams = new URLSearchParams(queryString);
    const notebookProjectId =
      urlParams.get('nId') || 'a13794788668076032978243';
    if (!notebookProjectId) {
      Notification.error('项目ID未获取到', { autoClose: 3000 });
    } else {
      try {
        console.log('Initial route:', notebookProjectId || 'Route not ready');

        const projectData = await getProjectDetail(notebookProjectId || '');

        const timeWidget = new UsageTimeWidget();
        timeWidget.install(app);

        const sidebarWidget = new VersionListSidebarWidget();
        sidebarWidget.install(app);

        const sidebarDataSet = new DataSetListSidebarWidget({ projectData });
        sidebarDataSet.install(app);

        const titleWidget = new TitleWidget({ projectData });
        titleWidget.install(app);

        const createVersionBtn = new createVersion(app);
        createVersionBtn.install(app);

        const logMonitor = new LogMonitorWidget();
        logMonitor.install(app, statusBar);

        console.log('ln-jupyter-extra extension activated successfully!');
      } catch (error) {
        console.error('Error during activation:', error);
        Notification.error('插件激活失败');
      }
    }
  }
}

const lnPlugin: JupyterFrontEndPlugin<void> = {
  id: 'ln-notebook:plugin',
  description: 'leinao extra jupyter plugin',
  autoStart: true,
  requires: [ICommandPalette, ILayoutRestorer, IStatusBar, IRouter],
  activate: activate
};

const plugins = [lnPlugin, ...VariableInspectorPlugins];
export default plugins;
